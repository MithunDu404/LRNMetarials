# Handling 1 Million Requests per Second — Part 1

## The Scale of the Challenge

The goal of this lesson is to simulate being one of the busiest routes in the world, handling more than a million HTTP requests per second. As a reference point for what "busiest" really means: AWS's WAF (Web Application Firewall — the service that acts as a security guard in front of applications running in AWS) is one of the busiest routes in the world, and a few years ago it was handling more than 400 million requests per second globally. Trillion-scale traffic doesn't exist yet, but hundreds of millions to a million requests per second is within reach of what a well-engineered system can do — and that's the target for this exercise.

This is explicitly framed as an extreme, high-stakes environment: the scale of companies like Uber, Netflix, and parts of Apple and Google. The exercise will involve launching infrastructure with hundreds of CPU cores across multiple machines, costing hundreds of thousands of dollars a year to run if kept up permanently, and moving terabytes of data per minute.

### Why the Usual Assumptions Break Down

A common claim in normal-scale system design is "the database is always the bottleneck." At this scale that assumption doesn't hold — you actively don't want your database to be the bottleneck, because if it becomes the constraint, scaling it up to keep pace becomes prohibitively expensive.

At this scale, a mistake is not a bug — a bug is considered unacceptable, something you should never get close to. A "mistake" here means something subtler: choosing an algorithm or approach that is $O(n)$ when it should be $O(\log n)$. The "it works, ship it" mentality that's tolerable in most software engineering becomes ruinous here — it can cost a company millions of dollars very quickly. Even events with a probability as low as one in a million become relevant, because at this request volume such an event happens roughly once a minute. This means the "just a programmer" mindset isn't sufficient; you need to think about probability, math, and engineering tradeoffs directly.

The video's own framing: only a handful of companies in the world ever operate at this scale, and reaching it takes serious engineering effort — but it is also described as thrilling, "roller coaster scary," with the added twist that here you actually can crash (i.e., lose real money through cloud costs or mistakes).

### Practical Disclaimer on Cost

The local portions of the exercise (running on a personal machine) are free to replicate. But once the lesson moves into the cloud (AWS), the infrastructure described costs real money — quoted at around $30/hour, or roughly $20,000/month if left running. A single mistake in configuration could cost tens of dollars or more almost instantly. The advice given: unless you're already comfortable with cloud cost management, just watch this part rather than reproducing it yourself.

### Technologies Used

The lesson will touch SQL, Unix, multi-threading and clustering, Redis, Node.js, and C++. Node.js is used for prototyping and initial benchmarking, but the reasoning given is that mainstream high-level languages/runtimes — Node.js, Python, Java — are not efficient enough at this extreme scale, since every fraction of a millisecond or byte of overhead compounds massively when multiplied by a million requests per second. C++ is introduced later as the way to actually approach the 1-million target. Knowledge of C++ or Node is not required to follow along — the concepts will be explained in plain terms. AWS is used for the cloud portion, but the same principles would apply equally on Google Cloud, Azure, or self-hosted physical machines.

### Prerequisites

To get full value from the lesson, you should already know:

- Basic SQL (`SELECT`, `INSERT`, `UPDATE`).
- Some backend development experience — what an HTTP request is, having built or called an API in any language.
- Basic computer architecture: what a CPU core is, what a thread is, that memory (RAM) is much faster than disk, and that machines communicate over a network card (e.g., via Ethernet).
- Byte/bit conversion: 1 byte = 8 bits, so 1 GB = 8 Gb (gigabits). This distinction matters throughout because network throughput is usually quoted in bits, not bytes.
- What Node.js is at a conceptual level — a system-level runtime (comparable to Java/Spring) capable of file I/O, spawning processes/threads, and networking, as opposed to a browser-side framework like React. Running a simple "Hello World" in Node is recommended but not required.
- Basic SSH usage and terminal commands (navigating directories, creating/deleting files).

## CPU Utilization and Threading Fundamentals

Before touching any networking code, the lesson establishes how to read CPU usage correctly, because resource monitoring is treated as mandatory at this scale — there's no way to reason about a million-requests-per-second system without constantly watching core-level and total CPU numbers.

### Core Utilization

A CPU has multiple cores, and each core at any instant is either doing work or sitting idle (idle meaning literally doing nothing — not even a trivial operation). Core utilization over some time window is defined as:

$$\text{Core Utilization} = \frac{\text{Total Time} - \text{Idle Time}}{\text{Total Time}} \times 100$$

Worked example: if you look at the last hour (total time = 60 minutes) and the core was idle for 30 of those minutes, utilization is $\frac{60-30}{60} \times 100 = 50\%$.

### CPU Utilization (Two Reporting Methods)

Since a CPU has many cores, overall CPU utilization is obtained by summing the individual core utilizations. There are two conventions for reporting this sum:

- **Method 1**: Just add up all core utilizations directly. If you have 4 cores and all are fully utilized, this produces 400%.
- **Method 2**: Take the same sum and divide by the number of cores, normalizing the result to a maximum of 100%. In the same 4-fully-utilized-cores example, this produces 100%.

Different operating systems and monitoring tools default to different methods (and some let you choose), so when you see a CPU percentage, you need to know which convention is being used before you can interpret it.

### Demonstration: Single-Threaded vs Multi-Threaded Load

To make this concrete, two small scripts are used (in the accompanying repository, in Node, but the logic is language-agnostic):

- `singlethread.js`: an infinite `while (true)` loop, doing no useful work but keeping the CPU busy.
- `multithread.js`: spawns multiple threads (12 in the example, since the demo machine has 12 cores), each running the same `while (true)` loop.

**Key rule**: a single thread can only ever occupy one CPU core at a time. Running the single-threaded script and checking a system monitor (Task Manager on Windows, System Monitor on Linux, Activity Monitor on Mac) shows the Node process pinned near 100% (Method 1) or a value like 25% if the monitor is using Method 2 on a 4-core machine — because it's saturating exactly one core. Meanwhile, total system CPU still shows a large amount of idle time, since only one of many cores is busy.

To actually use more than one core simultaneously, you must explicitly spawn additional threads (or processes). Running `multithread.js` with 12 threads on a 12-core machine drives the process's reported usage up to roughly 1200% under Method 1 (900%+ was observed with background load from screen recording), and — crucially — drives total system idle CPU down to 0%, because now every core has a queue of work and none of them get a chance to idle.

This distinction — one thread = one core at a time, and you must parallelize explicitly to use more — becomes the throughline for scaling the HTTP server later: raw single-process performance leaves most of the machine's cores idle, and the entire performance strategy will revolve around actually occupying all available cores.

## Benchmarking a Simple Node Server

### The Baseline Route

Using a small repository ("Node 1 million requests per second"), the simplest possible route is defined: `/simple`, which just returns a JSON message (`{"message": "hi"}`). The implementation language doesn't conceptually matter — Python, Go, Rust, or Java/Spring would behave the same way. Sending a single request manually (via browser or Postman) to `localhost:3001/simple` returns the JSON in about 12 milliseconds. Each such completed request/response cycle (getting a 200 status and a body back) counts as "one request" for the purposes of the exercise. Two auxiliary services — Redis and Postgres — are also connected at startup but not used yet.

### Introducing Autocannon

To generate large volumes of requests automatically (since no human can click "send" thousands of times a second), the tool **Autocannon** (installed via `npm i -g autocannon`) is used. It simulates many simultaneous clients hitting an endpoint and reports how many requests per second the server can sustain.

Example invocation:

```bash
autocannon -c 20 -d 20 -p 2 -m GET http://localhost:3001/simple
```

- `-c 20`: number of concurrent connections.
- `-d 20`: duration of the test in seconds.
- `-p 2`: pipelining factor — how many requests are sent back-to-back on a connection before waiting for responses.
- `-m GET`: HTTP method.
- (An additional flag, `-w`, controls how many worker threads Autocannon itself uses to generate load — important once the client machine also needs to use many cores to produce enough traffic.)

Running this against `/simple` yielded about 18,000 requests per second, all returning HTTP 200, with roughly 300,000 total requests sent and about 90 MB of data moved over 20 seconds.

### Understanding Autocannon's Concurrency Model

The relationship between `-c`, `-p`, and `-w` is explained with a concrete mental model: imagine a client machine (running Autocannon) and a server machine, connected over the network, with the server's network interface being the entry point for all traffic.

Worked example with `-w 2 -c 6 -p 2`:

- `-w 2` spawns 2 worker threads on the client, meaning the client itself can perform 2 things at once.
- `-c 6` opens 6 total TCP connections to the server — split evenly across the 2 worker threads, so each thread manages 3 connections.
- `-p 2` means each connection sends 2 requests immediately, back-to-back, before waiting on responses (rather than sending one request, waiting for the reply, then sending the next).

From this, a key derived quantity: the number of concurrent requests the server is handling at any given instant is $c \times p$. In this example, $6 \times 2 = 12$ concurrent in-flight requests at any moment.

### Reading Autocannon's Output

Autocannon runs the test as a series of samples (e.g., 20 one-second samples over a 20-second run) and reports statistics across them. The number to focus on is the **average** requests/second. It also reports percentiles and extremes — e.g., a worst-case sample of 16,000 req/s and a best case of 18,000 req/s, averaging to 18,000 req/s overall.

### The Reference Local Machine

The benchmarking machine used for this portion is a Mac Studio: 12 CPU cores, 32 GB RAM, and a 10 Gbit network interface (≈1.25 GB/s). It costs roughly $2,000 to purchase, and amortized over three years including electricity, roughly $60/month to "run." These numbers are established deliberately as a baseline, because later the lesson moves to cloud machines roughly 10x more powerful, and the comparison is meant to highlight just how much of a jump that represents.

At 18,000 req/s on `/simple`, the machine is clearly underutilized — there's a large amount of idle CPU, partly because Express itself introduces framework overhead.

## Framework Overhead: Express vs. Fastify vs. a Custom "CP" Framework

Because framework overhead becomes significant at scale, three equivalent implementations of the same routes are compared, all in the same repository:

- **Express** — the standard, widely-used Node framework, known to have relatively higher per-request overhead.
- **Fastify** — a Node framework that markets itself (per its own npm page) as roughly 3x faster than Express.
- **CP** — a custom, zero-dependency framework built from scratch for this project, currently about 500 lines of code, designed to mimic Express's API/features while staying as close as possible to raw Node performance.

Benchmarks on `/simple` (same Autocannon parameters, e.g. `-c 5 -w 1`):

- **Fastify**: averaged around 66,000 req/s (with a peak run near 77,000), confirming its claimed advantage over Express.
- **Express**: averaged around 20,000 req/s under the same conditions — several times slower than Fastify.
- **CP**: around 73,000 req/s, i.e., comparable to or slightly better than Fastify, and far above Express.

Repeated testing across multiple instance counts and connection/worker settings confirmed the pattern: CP tracks very closely with Fastify's request-per-second numbers and consistently outperforms Express, while remaining simple enough to read and understand end-to-end (no hidden "magic"). Because of this — near-raw-Node performance, Express-like ergonomics, and full code transparency — **CP is chosen as the framework for the rest of the video's testing.**

## Testing a More Realistic Route

`/simple` is about as trivial as an endpoint can be, so a more representative route is introduced: a `PATCH` request that includes path variables, query parameters, and a JSON request body. On the server side, it performs a few lightweight operations (e.g., validating that an ID is numeric) and constructs a sizeable dummy response — an array-based payload amounting to several kilobytes of JSON (around 700 lines, ~32 KB) — before responding. This is meant to mimic a typical real-world API response, which returns meaningfully more than a one-line message.

### Single-Instance Performance

Running Autocannon against this route (same style of command, but now including `-b` for the JSON request body and a `Content-Type: application/json` header, with `-c 5 -d 20 -p 2 -w 1`) dropped throughput to about 8,000 requests per second — roughly 10x slower than the `/simple` route. Over the 20-second run this moved about 5 GB of data. Checking Activity Monitor showed the single Node process pegged at 100% CPU on one core, while the machine overall still had significant idle capacity — the process was CPU-bound on a single core, unable to spread the extra work (data generation, JSON serialization) across other cores.

### Scaling with Clustering (PM2)

Since a single Node process can only use one core, the next step is to run **multiple instances of the same process in cluster mode** using PM2, a Node process manager. An "ecosystem" config file (already present in the repo) tells PM2 to launch one instance per CPU core — 12 instances on this 12-core Mac Studio (`pm2 start ecosystem`). PM2 automatically arranges for one parent process to receive incoming traffic and distribute (load-balance) it across the worker instances, without any code changes to the application itself.

Progression of results on the `/patch`-style route:

1. **Single process**: ~8,000 req/s, one core fully used, rest of machine mostly idle.
2. **12 clustered instances (initial Autocannon settings)**: jumped to ~36,000 req/s, with idle CPU dropping to about 30% — most, but not all, cores now active.
3. **Increasing Autocannon's own concurrency** (raising connections to 20 and Autocannon's worker count to 6, so the client itself can generate enough load to actually saturate the server): idle CPU on the server dropped to 0%, and the Autocannon client process itself climbed to about 200% CPU usage. This pushed throughput to about 42,000 req/s.
4. With the screen recording paused (removing its CPU overhead), the same setup averaged closer to 50,000 req/s, and cumulatively handled 1 million total requests — but critically, that total was spread over the full 20-second test window, not delivered within a single second. The real target is 1 million requests *per second*, and a single (very powerful) Mac Studio doing roughly 50,000/s is nowhere near sufficient.

This gap — needing to go from ~50,000 req/s on a maxed-out 12-core workstation to 1,000,000 req/s — motivates the move to much larger, purpose-built cloud infrastructure.

## Moving to AWS

### Cost and Safety Disclaimer

Before provisioning anything, an explicit warning is repeated: the setup about to be launched costs roughly $30/hour, or on the order of $20,000/month if left running continuously. Anyone without direct AWS experience is advised not to replicate this part hands-on, since a small misconfiguration can generate a large, unexpected bill. The presenter notes their own comfort comes from years of AWS experience and active cost management.

### EC2 and Instance Selection

AWS EC2 (Elastic Compute Cloud) is the service used to provision virtual machines ("launch computers"). It offers over 600 instance types, ranging from near-free small servers to machines powerful enough to train large AI models. To skip repetitive setup (installing Node, PM2, configuring shell scripts), a pre-configured machine image (AMI) is reused rather than configuring each new instance from scratch.

The instance type chosen for the main server is **C8i.32xlarge**, with:

- 128 CPU cores
- 256 GB RAM
- 50 Gbit/s network throughput (≈6.25 GB/s)
- Cost: about $6/hour, or roughly $5,000/month

Compared to the Mac Studio baseline (12 cores, 32 GB RAM, 1.25 GB/s network), this single cloud instance has 8x the memory, 5x the network throughput, and roughly 10x the effective power overall — described as "launching 10 Mac Studios" in one machine.

Storage for the server instance is configured with about 500 GB and increased provisioned IOPS (30,000), at some added monthly cost, to reduce the chance of storage becoming a bottleneck. The instance's security group is set to "allow all" (opening all ports) purely as a convenience for this short-lived experiment — explicitly flagged as unacceptable practice for a real production system, justified only by the fact that the instance will be shut down after a few hours.

This machine is named the **power server**.

A second, identically-specced C8i.32xlarge instance is launched from a different AMI (one with only Autocannon installed) to serve purely as the **load generator**, named the **power tester**. Using a dedicated, similarly powerful machine to generate traffic avoids the load generator itself becoming the bottleneck, which was a risk when generating and receiving traffic on the same Mac Studio earlier.

### Database: Aurora/RDS

A managed Postgres database is also provisioned, via AWS Aurora/RDS, since some of the application's routes perform real reads/writes against Postgres. The instance class used is a very large one (described as roughly a **db.m5/db.r5.16xlarge**-class machine) with:

- 64 CPU cores
- 256 GB RAM
- Single availability zone (no multi-AZ replication needed for this test)
- Cost: roughly $5–6/hour

Storage is configured as GP3 with about 3,000 IOPS — acknowledged as comparatively low, but accepted for now since the database isn't the focus of this initial round of testing (with the intent to revisit and possibly try alternate configurations later).

### Network Architecture

The resulting architecture has three machines:

- **Power tester** (traffic generator) → connected over the network to →
- **Power server** (application server) → connected to →
- **Postgres database** (Aurora/RDS instance)

The tester and server communicate directly over their network interfaces; the database is reachable only from the power server. All three sit on the same private network so that traffic between them doesn't traverse the public internet, removing general internet speed/variability as a factor — the only network constraint that matters is the private network's own bandwidth between these machines.

### Initial Setup and First Cloud Test

After the instances finish initializing, SSH sessions are opened into both the power server and power tester (using a personal shell alias, `ss`, wrapping the SSH command with the instance's public DNS name). Separate terminal tabs are kept for each machine so CPU usage can be monitored live during tests.

On the power server, the same codebase from the local testing is already cloned, and PM2 is used to start the application in cluster mode via its ecosystem file — this time launching **128 instances** of the Node process, one per core, which takes a noticeably long time to spin up given the sheer count.

A sanity check is performed first: sending a single request to `/simple` on the power server (now reached via its public DNS rather than localhost) confirms the expected `{"message": "hi"}` response, with all 128 processes still idle at that point.

CPU monitoring is done using `mpstat 1` (showing live idle-CPU percentage) as well as a custom shell alias, `cpu-usage`, set up for convenience.

An initial large-scale Autocannon run is then launched from the power tester against the power server, with far more aggressive parameters than were used locally: 1,000 connections, 20-second duration, pipelining of 100, and 120 Autocannon worker threads. Once running:

- The power server's idle CPU dropped to 0% — its 128 cores were now fully saturated.
- The power tester, despite generating this massive load, still had roughly 50% idle CPU remaining — indicating that even this very powerful "tester" machine had headroom to spare (suggesting a somewhat smaller machine could have sufficed for generating traffic), while confirming that the constraint at this point was squarely on the server side, now fully using its available compute.

This sets up the transition point for the next phase of the lesson: with the server now fully utilizing 128 cores under heavy simulated load, the next steps will examine exactly how many requests per second this cloud configuration can sustain, and what needs to change to keep pushing toward the 1-million-per-second target.

# Finding the Real Bottlenecks: Network, Database, and the Path to Redis

## Revisiting the "Hello World" Result

The simple JSON "hi" route hit 6 million requests per second, but this came at a cost of $5,000/month for the server. The lesson explicitly notes that this number is almost meaningless on its own: the payload was trivial (a tiny hard-coded JSON response), so of course a powerful machine could serve it at that rate. The real test is what happens when actual application logic (writes, database operations) is introduced. The instructor sets up the general diagnostic principle here: since neither AWS nor the load-testing tool (autocannon) is the limiting factor, any shortfall on a more complex route must be explained by an actual resource bottleneck — CPU, memory, disk, or network.

## Testing the PATCH Route: Discovering the Network Bottleneck

### The surprising result
A PATCH request test was run with the same load profile as before (500 connections, 20s duration, pipelining 50, 12 workers). Two things stood out:
- The **testing machine** was 80% idle — it wasn't struggling to generate load.
- The **server (power machine)** was only 50% CPU utilized — also not maxed out.
- Yet throughput was only **100,000 requests/second** — far below the earlier 6 million.

Since neither CPU showed saturation, CPU wasn't the constraint. Something else had to be capping throughput.

### Diagnosing via data volume
The investigation approach: look at how much data moved during the test. In a 20-second window, 3 million requests transferred roughly 120 GB of data. Dividing 120 GB by 20 seconds gives about **6 GB/second** of throughput. Checking back against the earlier keynote/spec slide, the chosen EC2 instance's rated network bandwidth was exactly **6 GB/second** (50 Gbit/s). That match is the smoking gun: the **network interface**, not CPU, RAM, or disk, was the bottleneck for this route, because the PATCH payload was much larger (moving significant JSON per request) than the trivial "hi" response.

The instructor emphasizes that 6 GB/s (50 Gbit/s) is still an enormous number by everyday standards — a home connection of even 10 GB/s equivalent would be considered extreme — but at the scale of 1 million req/s with non-trivial payloads, even this becomes the limiting resource.

### Can we just get a faster network card?
Yes, in principle. Looking at AWS's instance selector for higher network bandwidth options:
- A 100 Gbit/s instance (roughly double bandwidth) was tried conceptually: it would only get to about 200,000 req/s — still nowhere near a million — despite costing around $12/hour and offering ~800 GB of RAM.
- Going further, AWS offers instances rated near 300 Gbit/s and above; one instance identified was rated near **3,000** (very high bandwidth, described as "close to a supercomputer") — powerful enough to comfortably clear 1 million req/s, but at a cost around **$30,000/month**.

The broader point: chasing the raw network ceiling to brute-force 1M req/s on a single machine becomes financially absurd very quickly.

## Just How Expensive Is "1 Million Requests per Second," Really?

To make the scale of 1M req/s tangible, the instructor walks through pricing from real API providers, using the fact that there are roughly **2 million seconds** in a month for the math.

- **OpenWeather API**: charges a very small fee per call after a free tier of 1,000 calls. Multiplying its per-request price by 1 million requests/second sustained for a month (2 million seconds) works out to about **$3.8 billion/month**. The instructor notes nobody would realistically hit a weather API that often — the point is purely to illustrate the scale of "1M/s sustained."
- A second, more realistically-scaled API charges about **90 cents per million requests**. Multiplied out over 2 million seconds/month, sustained 1M req/s would cost roughly **$3.9 million/month** — still enormous even at a "reasonable" per-request price.
- Other services like **Google Maps** and **Cloudflare Workers** were also checked. Cloudflare Workers, being serverless, is plausible for some company to actually hit at that scale — but even there, sustaining 1M req/s would cost close to **$1 million/month**. The instructor's conclusion: at that point, it becomes more cost-effective to run and manage your own servers than to pay per-request serverless pricing at this volume.

## Real-World Architecture: Why Companies Don't Use One Giant Server

Companies that genuinely do serve on the order of a million requests per second — the examples named are **Uber** and **Amazon** — do not rely on a single supercomputer-class machine to absorb the entire load. Instead, they run **many servers distributed geographically** with **load balancing** routing users to their nearest server. The instructor illustrates this conceptually:
- One server cluster for New York, Chicago, and Toronto.
- Another for California and Vancouver.
- Another for South America.
- More for Europe, Africa, India, etc.

If, say, 100 servers are deployed this way and each can handle 500,000 requests/second, the aggregate system can absorb far more than any single machine — and it can be scaled elastically by adding more servers in regions experiencing high demand (e.g., adding capacity for a surge of American traffic). This is presented as the standard, practical solution to the whole problem being explored in the video — the giant single-box approach is really just for demonstrating where the limits are.

## Fixing the PATCH Route by Shrinking the Payload

Back on the actual test setup, the instructor modifies the code: the array being generated in the PATCH handler is shrunk from **100 elements down to 3**, drastically cutting the size of data moved per request (down to roughly 1 KB, still described as a plausible real-world payload size). After restarting the stack and rerunning the same benchmark:
- CPU usage on the server dropped to near 0%.
- The tester was now half idle, meaning it could generate even more load if needed.
- Throughput jumped to **3 million requests/second** — comfortably past the 1 million milestone.

This confirms the diagnosis: with a small enough payload, the network is no longer the constraint, and the same route/hardware can blow past 1M req/s. The instructor flags that trying to sustain a much larger payload (e.g. 30 KB) at 1M req/s would require the exotic, extremely expensive network-optimized instances discussed earlier, and explicitly reserves that challenge for later in the video.

### Foreshadowing: the 30 KB / 1M req/s challenge
As a flash-forward aside, the instructor (speaking from after having done the work) reveals that they *did* eventually manage to hit 1 million requests/second even with a heavier ~30 KB payload — but only after a long struggle. Node.js could not do it even on more powerful machines; nor could Python, Java (Spring), or Go. The eventual solution was rewriting the route in **C++**, using the **Drogon** web framework (described as one of the fastest in the world) together with **RapidJSON** (one of the fastest JSON parsers available). This result is deferred to later in the video.

## The Database Write Route: Inserting into Postgres

### The route and setup
The next route generates a simple 500-character random code and inserts it into a Postgres table with columns for `id`, `created_at`, and the random `code`. This was verified manually first via Postman (POST to `/code`), confirming a row was created and returned.

A separate, similarly expensive database instance (~$5,000/month, many CPU cores and large memory) was provisioned to back this route. Before benchmarking, the database was reset to empty using an `npm run seed` command (which truncates/recreates the table); this same seed script can also be given an argument to pre-populate the table with records, used later for read benchmarks.

### First write benchmark: connection overload
An autocannon POST benchmark was run with 5,000 connections over 20 seconds. Result: the server and tester CPUs were both essentially idle (all the real work is happening in the database), but the run produced a large number of **errors** — trying to open 5,000 simultaneous connections overwhelmed the database, causing timeouts.

### Second attempt: lower connection count
Reducing the connection count to 300 fixed the errors and actually **increased** throughput to about **35,000 writes/second**, processing 700,000 requests with zero errors. Cross-checking `SELECT COUNT(*)` in the database (via DataGrip) confirmed the row count matched. Despite the fix, 35,000/s from a database this expensive is called "pathetic" relative to the 1M/s goal — and this is despite the code itself doing almost nothing (`INSERT INTO ...`, no computation), meaning the bottleneck is purely inherent to how fast Postgres can commit writes, regardless of the application language used.

### Understanding the connection math
The app layer (128 machines/workers, each opening up to 10 Postgres connections by default via the pg client's default pool size, as seen in `database/index.js`) results in roughly 1,000+ simultaneous connections to the database — described as already a very large number that would crash a smaller database instance. Running `SHOW max_connections` revealed the instance's limit was **5,000**, so the write test wasn't even hitting the connection ceiling — confirming the bottleneck lay elsewhere (disk I/O), not connection exhaustion.

### Scaling storage IOPS
The database's provisioned IOPS (inputs/outputs per second) was initially only 3,000 — far too low for a million writes/second. The instructor increased storage to 500 GB and raised throughput settings, bringing IOPS to 12,000 (roughly 4x). Cost rose by about $1,000/month. Re-running the write benchmark yielded about **66,000 writes/second** — better, but still far from 1 million, and the cost trajectory ($15,000+/month and climbing) makes it clear this path won't reach the goal affordably. The conclusion: hammering a relational database directly at 1M writes/sec is both technically very hard and financially unreasonable; the better real-world approach (introduced later) is to buffer writes and flush them to the database via **batch processing** over time, rather than writing synchronously per request.

## The Database Read Route: Four Versions, One Big Lesson in Algorithmic Complexity

To have a meaningful read benchmark, the database was seeded with **10 million records** (rationale: a system truly handling 1M req/s would realistically hold at least that many rows), taking about 30 minutes to insert.

### Version 1: `ORDER BY RANDOM()` — O(n) and catastrophic
The first read implementation selects `id, code` ordered by `RANDOM()` to pick one row. Testing this against 10 million rows caused the request to take **43 seconds** to return, and the database effectively crashed under load. The reasoning: `ORDER BY RANDOM()` forces Postgres to score and scan the *entire table* to produce a random ordering — an O(n) operation per single request. At 10 million rows, this is disastrous, and the instructor draws the explicit lesson that **not knowing your algorithmic complexity in a high-scale environment can be extremely costly**.

### Version 2: `SELECT COUNT(*)` first, then pick an ID — still O(n)
A second version first ran `SELECT COUNT(*)` to learn the table size, then generated a random ID within that range. This was faster than version 1 but still failed under the same load, because Postgres does not track row counts internally — `COUNT(*)` also requires a full table scan, making this approach essentially as bad as version 1 for a table this large.

### Version 3: `SELECT MAX(id)` then random ID in range — success
Version 3 instead selects `MAX(id)` (ordering by ID, effectively an index-backed lookup, not O(n) in practice) and generates a random ID between 1 and that max. This query ran in about 40 milliseconds. Benchmarking this version gave roughly **200,000 reads/second** — a huge improvement, still short of a million, but "very good" and indicating this route could plausibly hit 1M with roughly a 5x boost in either database power or connection scaling.

### Version 4: two separate lookups, cheating for speed
A fourth variant does two round-trips to the database — one to get the ID, one to fetch the row by that ID — described as a shortcut/"cheat" that relies on randomly generated IDs. Since an ID lookup is effectively an **index lookup** with near-instant time complexity, this version achieved about **400,000 reads/second** with zero errors, again with both server and tester CPUs sitting idle (database-bound, not compute-bound).

### Pushing the database further: IOPS and CPU scaling
The instructor then reconfigured the database with much higher storage (1 TB) and IOPS, pushing the database cost to about **$7,000/month**. AWS flagged severe warnings: CPU spiking to 100% and database connections exceeding 1,200 (expected, given 128 app instances × 10 connections each, within the 5,000 max). This confirmed **CPU**, not disk, was now the dominant read bottleneck.

After the storage upgrade finished (~1 hour), re-testing showed:
- Writes improved modestly to about **50,000/second**.
- Reads stayed roughly flat at about **400,000/second** — the earlier disk upgrade didn't move the read number because CPU, not disk I/O, was the actual constraint for reads.

### The cost of brute-forcing it further
Extrapolating: to reach 1M reads/second in a best-case scenario might require doubling the database (e.g., an additional read replica), pushing cost to roughly **$14,000/month**. Boosting CPU (~1.5x via a larger instance class) and maximizing provisioned IOPS (up to a quarter-million) pushes cost to about **$33,000/month** — and even that isn't a guaranteed win for both reads and writes simultaneously. AWS's managed **Aurora Postgres** (with built-in autoscaling) was also estimated, coming out to roughly **$20,000–$30,000/month** for handling reads and writes at this scale — comparable to Uber-level infrastructure spend.

**Conclusion on the database routes:** the instructor explicitly calls this a failure to reach 1M requests/second in a cost-effective way using a disk-backed relational database directly. The database is terminated at this cost level, setting up the motivation for the next section.

## Introducing Redis: Trading Disk for Memory

### Why memory helps
The key fact motivating the next approach: RAM read/write speed is roughly **10x faster** than disk, and in practice the access-time gap between RAM and disk (even a fast SSD, which is what Postgres ultimately reads/writes to) can be **thousands of times** in latency terms. This motivates using an **in-memory database** — **Redis** — as a front for high-frequency operations, sitting in front of (or alongside) the persistent SQL database.

### The `code-fast` route: write-through to a queue, sync later
A new route, `code-fast`, performs the same operation as the original POST-to-Postgres route, but instead writes to Redis. Rather than hitting Postgres directly, generated IDs/codes are pushed onto an in-memory **queue** (`sync-queue`). A separate script, `sync`, periodically drains this queue and writes the buffered records into Postgres — this can run on a schedule (e.g., overnight, or continuously as a background process) without blocking the hot path.

This mirrors a real-world pattern: for something like continuously streaming vehicle location updates (the example given is a ride-hailing company like Uber tracking driver locations), it would be absurd to write every single location ping straight into an SQL database at request time. Instead, buffer to memory (Redis or similar) and flush to durable storage asynchronously in batches.

The trade-off acknowledged: storing everything in Redis loses SQL's relational capabilities (joins, structured querying). The mitigation is that you don't need to move your *entire* dataset into Redis — only the specific hot subset of data or operations that receive extreme traffic. (This is previewed with the `weird.pro` URL-shortener project the instructor is building: if a specific type of short code, e.g. six-character codes, receives disproportionate traffic, only that subset needs to live in Redis with its own sync/migration logic — not the whole database.)

### Migrating the whole existing dataset into Redis
To test this at scale, a `migrate` script moves the entire existing Postgres dataset (11 million records, ~16 GB on disk, confirmed via a Postgres table-size query) into Redis in batches of 2,000 records. This uses Redis as a key-value store: each code is a key, values fetched with commands like `HGETALL`. The migration also sets up:
- A counter for the **last used ID**, to keep allocating sequential IDs.
- A Redis **set** called `codes-unique` to track which IDs have already been used, preventing duplicates when generating new sequential IDs.

The server hosting Redis had about a quarter-terabyte (200+ GB) of RAM available, comfortably fitting the full dataset (using about 20 GB once migrated, slightly more than the 16 GB Postgres size due to the extra tracking structures).

### Benchmarking Redis: writes and reads
- **Writes to Redis** (`code-fast`): benchmarked at about **100,000 requests/second**, roughly 3x better than the best Postgres write result (~35,000/s), and CPU was at 80% (better utilized than before, but still with headroom). This is explained by a fundamental limitation: **a single Redis instance is single-threaded** and effectively caps out around 100,000 requests/second regardless of how powerful the underlying machine is.
- **Reads from Redis** (`code-get`): after migrating the full 10 million+ records, reads benchmarked at about **300,000 requests/second** — comparable to (though not dramatically better than) the earlier best Postgres read numbers, but at a fraction of the infrastructural cost (no need for a $20-30k/month database).

The instructor frames this as the core value proposition of Redis at scale: even without clustering, it delivers Postgres-competitive throughput without Postgres-scale cost, and it's straightforward to combine with selective migration/sync so only "hot" data lives in memory.

## Scaling Past a Single Redis Instance: Clustering

Since a single Redis instance is capped around 100,000–200,000 requests/second (being single-threaded), reaching 1 million requires **Redis clustering** — running multiple Redis instances/shards together.

### Setting up a cluster locally
Using a bash script (`redis.sh`) with a `--setup` flag, the instructor spins up **30 Redis cluster instances** as separate processes on a local machine (visible as 30 separate processes in the activity monitor). Since each single-threaded instance still tops out around 100–200k ops/second, having 30 of them working together in aggregate provides enough combined capacity to plausibly reach the 1 million/second milestone.

### What changes in application code for cluster mode
Redis Cluster automatically shards data across nodes using internal hashing, but the client code must account for this:
- Cluster mode determines, via hashing a key, **which node** a given piece of data lives on — consistent keys always hash to the same node.
- The existing `sync` script (written for single-instance Redis) does **not** work unmodified against a cluster — the instructor notes this as a known gap to fix later, though described as an easy change.

### The `code-ultra-fast` route: dropping sequential IDs for UUIDs
For the cluster-targeted route, the instructor replaces the sequential-ID scheme with `crypto.randomUUID()`, generating random 122-bit IDs (conceptually similar to how MongoDB generates document IDs). This removes the need to:
- Maintain and increment a shared "last ID" counter (itself a serialized bottleneck across many concurrent writers).
- Perform an extra write to check/maintain the `codes-unique` set for collision avoidance.

Both of these were extra Redis operations required only because sequential IDs need central coordination; switching to random UUIDs removes that coordination overhead entirely, at the cost of needing to reason about collision probability instead.

### Collision probability via the birthday paradox
The concern: if IDs are generated randomly rather than sequentially, could two random UUIDs collide? This is modeled using the **birthday paradox** formula for collision probability:

$$P \approx 1 - e^{-\frac{n^2}{2N}}$$

where:
- $e$ is Euler's number,
- $N = 2^{122}$ is the total number of possible UUID values (122 bits of entropy),
- $n$ is the number of UUIDs generated.

Solving for the number of generations needed to reach at least a 50% probability of a collision, and assuming a sustained generation rate of 1 million UUIDs per second, the result is that it would take approximately **86,000 years** of continuous generation to reach even a 50% chance of a single collision. Given this, the extra bookkeeping (uniqueness sets, sequential counters) is deemed unnecessary — random UUIDs can be used safely, and for the final insert into Postgres, the primary key/ID can simply be left to Postgres's own auto-generation rather than being manually tracked at all.

With this simplification in place (random IDs, no uniqueness-check writes, cluster-sharded Redis), the section ends with the instructor about to demonstrate the `code-ultra-fast` route running against the properly clustered Redis setup on the powerful cloud machine, aiming to finally cross the 1 million writes/second threshold.

# Scaling to 1 Million Requests per Second

## Setting Up Redis Cluster Mode

The previous benchmarks (with a single Redis instance) capped out around 400,000 reads per second and roughly 150,000 writes per second. To push toward 1 million requests per second, the next step is switching from a single Redis instance to **Redis Cluster mode**, which spreads data across many Redis nodes instead of forcing everything through one.

The practical setup steps were:

- Shut down the existing single-instance Redis server (loaded with 10 million records) and wait for it to fully stop.
- Re-run the setup script with `--setup --prod` flags — `--prod` tells the script to use Redis 6, which is what's installed on this machine.
- Delete all existing PM2 process instances so the app can be restarted cleanly against the new Redis configuration.
- Edit the `ecosystem` config file (the PM2 configuration) to control whether the app connects to Redis in cluster mode or single-instance mode, via a `REDIS_CLUSTER` environment variable: `false` connects to a single Redis instance, `true` connects to the full cluster.

Running the app with `REDIS_CLUSTER=true` produces a log confirming "Redis cluster ready" with **30 total nodes: 15 masters and 15 replicas**.

## How Redis Cluster Distributes Data

To build intuition for what's happening, picture the full hardware setup: the "power" machine runs one main parent Node.js process on port 3000, which forks 127 additional Node.js child processes, all handling incoming traffic distributed by the OS across cores. Previously, when these processes needed data, they reached out over the network card to a separate database machine, and that machine had to pull the data from its physical storage disk — two hops, and one of them touches disk.

The redesign eliminates both of those bottlenecks: all nodes now only reach out to **RAM**, because Redis is an in-memory data store, and there isn't just one Redis instance — there's a whole cluster of them, all living in RAM alongside the app processes.

Within the Redis cluster:

- There are 15 **masters** and 15 **replicas**. Each master has exactly one replica, which is a live copy of its data. If a master goes down, its replica can be promoted, which is what makes the cluster resilient.
- Writes always go to a master.
- Reads can be served from either the master or its replica, spreading read load further.

**How lookups work:** when a Node.js process wants to fetch data for a given key (e.g., a code with a particular ID), it doesn't need to know which of the 15 masters holds it. It sends the key to Redis, and Redis **hashes the key's content** to compute a number that maps deterministically to one specific master node. Redis cluster already knows which node owns which hash-slot range, so it routes the request to the correct master, retrieves the data, and returns it to the Node.js process. This hashing scheme is what lets the cluster scale horizontally — each new master simply takes ownership of a slice of the hash space — without the application needing any cluster-awareness logic of its own.

## Running the Benchmark: Reaching 1 Million

With the cluster live, the app is restarted under PM2 (`pm2 start ecosystem`) to use all available CPU cores, and the benchmark tool is pointed at the fast "patch" (write) endpoint used in earlier tests.

Result: **idle CPU dropped to nearly 0%** across all cores — everything was being used, split between the Node.js application logic and Redis's own processing (Redis competes for CPU too, which is why per-process CPU sometimes showed around 50% rather than 100%, with Redis consuming the rest). The benchmark hit **1 million requests per second**, meaning 1 million writes per second were successfully persisted into Redis.

This satisfies the video's stated goal: handling a million writes per second while still having a real, queryable database backing the system. The actual permanent database (Postgres) sync would happen separately — for example overnight, reading all the IDs accumulated in Redis and batch-writing them to Postgres.

**Key takeaway on cost:** this level of throughput did not require anything close to the "millions of dollars" spending seen with commercial APIs like OpenWeatherMap earlier in the series. Scaling further, if data volume grew, would mean modest additions — a few more CPU cores, more RAM — and worst case another ~$5,000 machine, nowhere near enterprise API pricing.

Repeating the write benchmark multiple times kept pushing millions more records into Redis — after several runs, the cluster held roughly **60 million records** and had consumed about **100 GB of RAM**, approaching the limit of the machine's memory. This surfaces a real operational concern: if you're sustaining a million writes per second into memory, you must continuously offload/flush that data (e.g., batch it into Postgres or write it to disk) or you will run out of RAM — potentially needing to scale toward a terabyte of memory otherwise.

## The Cost of Getting This Wrong

The speaker emphasizes that operating at "1 million requests per second" scale is not trivial, and a single design mistake here is extremely costly — potentially tens of thousands of dollars. The earlier example from the series (the "version one" SQL code) is invoked as a cautionary tale: if you assume the fix for poor performance is to horizontally scale the database rather than first optimizing the code itself, you end up paying for infrastructure to paper over an inefficiency that a faster implementation would have avoided. This mistake is described as extremely common in production systems — teams reach for horizontal scaling before investigating whether the code itself is the bottleneck.

Running these large cloud instances was itself expensive in real time — about $20/hour just to keep the servers alive — underscoring why efficient code matters even during testing.

# Pushing Beyond Node.js: The "Beast" Machines and C++

## New, More Powerful Hardware

To go further while controlling cost, two new, more powerful servers were provisioned: a "beast tester" and a "beast server," both roughly **1.5× more powerful** than the earlier "power" machines (which were `c8i.32xlarge` instances, compared against a Mac Studio). The new instance type is `c8gn.48xlarge` — the "N" denotes network-optimized, which matters because at this scale network throughput becomes the constraint, not just CPU.

Specs of the beast machines:
- 192 CPU cores
- 384 GB RAM
- 600 GB/second network bandwidth

Cost: roughly **2× the earlier machines** — about $11/hour or $8,000/month per instance. With two beast machines running (one tester, one server), the combined estimated monthly cost was around **$17,000/month**. A smaller `24xlarge` variant was tried first but wasn't enough CPU to reach 1 million requests per second — the full `48xlarge` was required.

## First Attempt: Node.js on the Beast Machine

180 of the 192 cores were used for Node processes (deliberately leaving a few cores unused). The benchmark tool was run against the "patch" (write) route, but with pipelining reduced to 20 and duration extended to 60 seconds, since a large volume of data now had to travel over the network and needed time to "warm up."

**Result:** CPU usage hit its ceiling (only a few cores idle), but the network was *not* fully utilized — throughput reached about 20+ GB/second (roughly 160 Gbit/second). That's already far beyond what the earlier `c8i` machine could sustain (which capped around 50 GB/s), but still well short of the beast's 600 GB/s network ceiling. In other words: this time, **CPU was the bottleneck, not the network**.

Even attempting an even more powerful server (~300 cores) still failed to reach 1 million requests per second with Node.js. The diagnosed reason: all incoming traffic funnels into one parent Node process before being distributed to child processes, and this fan-out overhead itself becomes the limiting factor at extreme scale — more cores don't fix an architectural bottleneck in how work gets distributed.

## Express Performs Even Worse

Testing the same workload against an Express server (switching the benchmark's target port to 3001) showed Express barely reaching half a million requests per second — confirming Express's comparatively higher framework overhead makes it unsuitable at this scale. The `cp`/Fastify-style approach used earlier came much closer to a million but still couldn't fully get there on Node.js.

## Why C++ (Drogon) Was the Answer

The conclusion drawn: **interpreted/managed languages like Node.js (JavaScript), Python, and Java are not well-suited to CPU-bound workloads at this extreme scale**, because the request handler here does real CPU work — validation checks, string manipulation, and data generation — not just I/O waiting. When a workload is genuinely CPU-intensive rather than I/O-bound, switching to a compiled, low-overhead language like **C, C++, or Rust** yields substantial gains.

The chosen framework was **Drogon**, described as one of the fastest web frameworks in the world, with the same application logic rewritten in C++ (same conceptual structure: read the request, set headers, set the response body — this maps directly onto concepts already learned in the Node/Express version).

**First problem — JSON parsing:** Drogon's *default* JSON parser was actually about **4× slower than Node's V8** for this workload, making the initial C++ version slower than the Node version. The fix was swapping in **RapidJSON**, one of the fastest JSON parsers available (acknowledged as not the single fastest possible option — an even faster parser exists — but RapidJSON was sufficient to hit the 1 million target, so optimization stopped there).

**Build/run configuration used for the benchmark:**
- Threading is handled internally by the Drogon framework itself, so PM2 (used to fork multiple Node processes) is unnecessary here.
- Compression and logging were both **disabled** for the test — logging to keep max performance, and compression because the test payload (30 KB) has heavy internal repetition that compression would shrink down to about 1 KB, which would misrepresent the actual network load being simulated. (The speaker notes that in a real production deployment, compression should be enabled — it was only disabled here to keep the benchmark comparable to the uncompressed Node test.)
- Project built and launched with a custom bash script (`do run` command).

## Results with C++/Drogon

Running the benchmark against the C++ server (port changed to 555 for this test):

- Idle CPU stabilized around **30%** — i.e., only about 70% of CPU was actually needed to hit the target throughput, unlike the Node version which needed 100% of CPU. The speaker suspects the remaining idle capacity was actually being limited by the network card rather than CPU headroom, though this was not fully resolved.
- Checking process-level CPU usage via `top` showed heavy CPU utilization but **very low memory usage** — a notable contrast to the memory-hungry Redis test earlier.
- Over a 60-second run, **average throughput was about 1 million requests/second**, peaking as high as **1.2 million/second**, with roughly half the test duration sustained at or above 1 million (a brief dip to ~31,000/s appeared at the very start, attributed again to network warm-up).
- Total data moved: **38 GB/second**, i.e., roughly **300 Gbit/second**, totaling about **2 terabytes of data transferred in one minute** (application-layer figure; actual wire-level total including TCP overhead would be somewhat higher).

**Concrete comparison for scale:** the speaker's Mac Studio has a fast SSD reading at about 5 GB/second. The network throughput achieved here (38 GB/s) was roughly **8× faster than that SSD's read speed** — equivalent to copying a full 2-terabyte SSD's contents to another 2 TB SSD in about one minute.

**Node vs. C++ comparison:** C++/Drogon delivered about a **30% improvement in requests per second over Node**, while using *less* CPU (70% vs. Node's ~100%). This is presented as the underlying reason large-scale companies handling millions of requests per second generally avoid Python/Node for CPU-bound routes, reserving those languages for workloads that are heavily I/O-bound (e.g., database- or Redis-bound routes), where the language runtime's overhead matters far less because the bottleneck is the external system (SQL, Redis) rather than the application code itself. The speaker notes Redis itself is written in C, and that Redis/Postgres integration into the C++ server would be straightforward since communication happens over the network regardless of implementation language — meaning a polyglot architecture (Nginx routing some routes to C++, others to Node) is entirely practical, combining Node's development speed with C++'s raw performance where needed.

## Attempting to Use a Load Balancer to Close the Remaining Gap

Since the single beast server was still leaving ~30% CPU idle, the next idea was to put a **load balancer** in front of two beast servers to try to fully saturate that remaining capacity. This did **not** work as hoped — throughput did not meaningfully improve. Suspected causes: at ~300 Gbit/second scale, AWS itself may impose limits, and the Linux OS-level network stack on either the tester or server machine may need explicit tuning to handle such extreme traffic volumes.

# Scaling the Tester Itself: Many Small Machines Instead of One Big One

## Diagnosing the Real Bottleneck

After further reflection (described as literally losing sleep over the unused 30%), the speaker concluded the true limitation wasn't the beast server's capacity — it was that the **single tester machine** couldn't open enough concurrent connections to fully load the server. The fix: replace one large tester with **many smaller tester instances** running in parallel.

## Provisioning 60 Small Testers

Using a smaller instance type, `c8gn.2xlarge` (8 CPU cores, 16 GB RAM each), the plan was to launch many of these simultaneously from one AMI (Amazon Machine Image), placed in the same **placement group** so the servers sit physically close to each other (minimizing network latency between them).

Provisioning ran into AWS account limits:
- Launching 100 instances at once failed — the account's per-region limit was **800 CPU cores**, but that had been raised gradually from a default of 32; even so, 100 instances didn't fit within available headroom at that moment.
- Trying 80 also failed.
- **60 instances** ultimately succeeded.

Cost of just the 60 tester machines: about **$20,000/month**, or roughly $30/hour (on top of the beast server's own cost, bringing the combined rate to roughly $40/hour).

A bash script was used to fan out the AutoCannon benchmark command to all 60 tester machines simultaneously and collect their output.

## First Full-Scale Run and the Math Behind "120,000 Concurrent Connections"

An initial low-connection-count test across the 60 machines confirmed the approach worked, still reaching roughly a million requests per second collectively even with modest settings on the earlier attempt.

For the "final big test," parameters were: 800 connections per machine, duration extended to **1 hour**.

**The concurrency math:** with 60 tester machines, each opening 400 connections, and a pipelining factor of 5:
$$60 \times 400 \times 5 = 120{,}000$$
This 120,000 figure represents the number of requests the server is handling *at any given instant* — described as comparable to having 120,000 simultaneous live users, "absolutely mind-blowing" in scale. Separately, the total number of open TCP connections at any time across all testers is $60 \times 400 = 24{,}000$.

During this run, the beast server's idle CPU dropped to **0%**, and it was observed sustaining more than a million requests per second, with instantaneous concurrent-request counts reaching roughly a quarter million at points. A rough electricity estimate was mentioned: the power draw across this 1-hour test (accounting for CPU wattage and the terabytes of data moved) would be enough to run a Tesla for "thousands of kilometers."

## A Logging Failure, and the Retry Strategy

After the full 1-hour run completed, the terminal logs came back corrupted/unreadable — despite the server itself handling the load correctly with no errors. Troubleshooting under time pressure (given the ~$40–50/hour cost of keeping the fleet running) wasn't practical, so the run was abandoned rather than debugged live. Shorter re-runs (20 seconds, 30 minutes, 40 minutes) reproduced clean logs fine — only the 1-hour run specifically triggered the failure, suspected to be an AutoCannon/tester-side issue at that duration. This prompted a change in approach for the next attempt (continued the next day).

## Redesigned Approach: Structured Output via a Node Script, SSM, S3, and CloudWatch

Rather than invoking AutoCannon directly from the terminal, a **Node.js wrapper script** was built that:
- Accepts connection count, duration, and target host as CLI arguments (passed in a fixed order).
- Runs AutoCannon programmatically with that config.
- Writes the result object to a `results.txt` file.
- Appends metadata — specifically the **start time and finish time** of each individual test run — because earlier testing revealed that the 60 machines didn't always start their tests at precisely the same moment, which skewed results; recording exact timestamps makes it possible to verify (or account for) synchronization drift.

This tooling was packaged into a repo (`1M-RPS-tester`) and deployed to all 60 tester instances. A quick manual SSH test on a single instance confirmed the script worked end-to-end, producing a clean `results.txt`.

**Fleet-wide execution via AWS Systems Manager (SSM):** rather than SSH-ing into each of the 60 machines individually, a single SSM "Run Command" was dispatched to all of them at once. Key details of this command:
- It `cd`s into the tooling folder and runs the Node script with the required parameters.
- **`MaxConcurrency` was explicitly set to 100%.** By default, SSM only dispatches a command to 50 targets at a time, then waits before sending to the rest — which would stagger the 60 machines' start times exactly as seen in the earlier failed run. Setting max concurrency to 100% ensures the command (and thus the benchmark) truly starts on all 60 machines simultaneously — described as a lesson learned "the hard way."
- Output from each instance is redirected to **S3** (Amazon's cloud file storage) for collection.
- Logs are additionally streamed to **CloudWatch** for real-time monitoring.
- **IAM** (the identity/permissions service referenced earlier in the series as "the busiest service in the world") is what makes this all possible — the tester instances needed IAM permissions explicitly granted to allow them to write output to S3 and CloudWatch, and IAM is also what secures the SSM command channel itself.
- The command returns a **command ID**, needed later both to cancel an in-progress run and to locate that specific run's output folder in S3.

A first attempt was accidentally launched with only a 3-minute duration; it was cancelled via `aws ssm cancel-command` using the saved command ID, then relaunched with the corrected duration (1800 seconds = 30 minutes).

While the 30-minute run was in progress, live output from all 60 machines could be tailed centrally via:
```
aws logs tail /aws/ssm/benchmarks --follow
```
letting the speaker watch every instance's benchmark output streaming into one local terminal in real time — highlighted as "pretty cool" for observability at this scale.

## A Digression: AWS Support and Network Load Balancers

While waiting on this run, the speaker received a reply from AWS support about an earlier, unshown experiment: placing a **Network Load Balancer** (which operates at the TCP layer, not HTTP, and is very fast) in front of two beast servers on the same private network, expecting it to allow handling even more traffic than a single beast server alone.

The actual result was **degraded** performance — throughput dropped from roughly 1 million requests/second (single beast server) down to about **5 GB/second** through the load balancer, a steep regression. After reaching out to AWS support, the explanation given was that the load balancer's consumed capacity had hit **165**, which was its configured limit — AWS network load balancers scale to very high throughput, but only if that capacity is **reserved in advance**. Without pre-reserving capacity, the load balancer throttles well below its theoretical maximum.

AWS pointed to a capacity-planning tool where you specify desired throughput (e.g., 300 Gbit/second), number of connections (e.g., 100,000), and availability zones, and it computes how many **LCUs** (Load Balancer Capacity Units, for a Network Load Balancer specifically, as opposed to an Application Load Balancer) would need to be reserved via a support request to sustain that load. The speaker did not pursue actually reserving this capacity or repeating that test, given the high cost of running these experiments, but flagged the mechanism as valuable to know about. Notably, AWS support had even run an internal AI assistant to try to suggest fixes, offering about ten suggestions, none of which resolved the issue — attributed to this being such a rare, extreme scale (few companies operate at 1M+ requests/second) that AI systems likely lack enough training data on it. The human support response, by contrast, was described as fast and genuinely useful.

## Processing the Final Results

Once the 30-minute, 60-machine SSM run completed, results were retrieved and consolidated using shell/bash tooling:

- A follow-up SSM command (`cat results.txt`, dispatched to all 60 named tester instances, output again routed to S3) confirmed each machine's results file existed.
- The S3 output for that specific command ID (a folder named by the command ID, starting with "97" in this case) was located in the S3 console, containing one subfolder per instance with a `stdout` file inside.
- Rather than inspecting each of the 60 files manually, the entire S3 folder was synced locally:
```bash
aws s3 sync s3://<bucket>/<command-id>/ results
```
- All individual result files were then concatenated into a single combined file using `find` piped to `cat`:
```bash
find results -path "*stdout" -exec cat {} \; > 60-instances-30min-results.txt
```
(The speaker committed to publishing this raw combined results file on GitHub for others to analyze.)

**Sanity-checking completeness:** to confirm all 60 machines actually reported results (a few had gone missing in earlier attempts), the file was filtered for lines containing "read" and counted:
```bash
grep read 60-instances-30min-results.txt | wc -l
```
This returned exactly 60, confirming every instance's result was present.

**Checking for errors:** filtering for "errors" showed the server handled the entire 30-minute, 60-machine, 100,000-simultaneous-connection load with **zero application errors**, but did register about **40 timeouts** total across millions and millions of requests — considered a very small and acceptable number given the scale (100,000 connections open to the server at any instant).

**Aggregating total throughput and data moved:** using `awk`, the total requests and total data transferred were summed across all 60 result lines — extracting the appropriate columns (the request count and, from the fifth field, the data-transferred value in terabytes), printing running totals for "total requests" and "total data read" in terabytes.

```markdown
## Results of the Final Test

The test ran for 30 minutes total, and the numbers it produced were staggering: 2 billion requests were sent to the server, and over 60 terabytes of data moved across the network — all handled by the single "beast machine" in half an hour. Since the load was steady throughout, you can simply double both figures to estimate what a full hour of this traffic would look like.

Out of those 2 billion requests, only 40 ended in a timeout. That is an extremely small failure rate given the scale, and it demonstrates just how much throughput a single well-tuned machine running C++ with the Drogon framework can sustain.

This result is the payoff of the whole video: with the right combination of hardware, OS-level tuning, and a high-performance C++ web framework, a single machine can approach and sustain workloads on the order of a million requests per second, with only a negligible error rate.

## Closing Reflections on the Purpose of the Video

The goal of the video was never to hand viewers a step-by-step recipe for building a "handle a million requests per second" architecture. Every individual topic touched on along the way — networking internals, OS tuning, load testing, framework choice, infrastructure setup — is deep enough to deserve hours of dedicated content on its own, so no single video could properly teach all of it as a tutorial.

Instead, the explicit aim was to shift how viewers think about performance and systems engineering: to build intuition, encourage creativity, and offer new perspectives, rather than deliver a narrow "how-to." The reasoning given for this choice is that the era of how-to content is largely over, especially in software development, because AI can now generate how-to instructions on demand. Because of that shift, the direction of this creator's content has moved deliberately away from tutorials and toward material that sharpens thinking and problem-solving ability — a harder kind of content to produce well, but the one considered more valuable going forward.

The creator notes that making this video — including all the tests and the research behind them — was both a lot of fun and genuinely stressful, given the scale of experimentation involved.

## Cost of the Experimentation

The total spend for the month was around $2,000, broken down roughly as:

- **~$800** on databases
- **~$1,200** on EC2 compute

Importantly, this figure isn't solely attributable to the tests shown in the video — a significant portion covers broader research that fed into the video but wasn't all directly part of the on-screen experiments. In hindsight, a few hundred dollars could have been saved; some avoidable mistakes were made along the way that inflated the bill, though the creator notes it could have been considerably worse.

## What Comes Next: The URL Shortener Project

Viewers who want to get more hands-on involvement are pointed toward an open-source URL shortener application project. Two things are emphasized about how this project will be built:

- No "VIP coding" shortcuts.
- No AI-generated code or "AI slop" — the code will be written and understood properly.

The stated long-term challenge for that project is even more ambitious than the one just completed in this video: attempting to shorten **1 million links per second**. This is explicitly framed as harder than the million-requests-per-second test just performed, because the URL shortener involves real business logic rather than a minimal benchmark endpoint — multiple database tables, complex application logic, authentication, and encryption all add overhead and complexity that a raw request-handling benchmark doesn't have to deal with.

Because of that added complexity, achieving 1 million operations per second on the URL shortener is expected to cost even more than this video's tests did. The project is still months away from being ready for that kind of large-scale test, since the underlying framework — being built in C++ — still has a lot of features left to implement before a release is ready.

As part of this project's development, the plan is to hire attackers to continuously try to break into and hack the application. Since the team is also building the web framework itself from scratch, this adversarial testing is expected to create rich opportunities to learn about security and about how to design performant code, beyond what the current video covered.

The pitch for why this project offers unusually high learning value: it's aimed at production use by real, non-technical end users — not just a technical audience — with the goal of building something people who have no prior awareness of the creator would still choose to use over competing products. Building for real-world adoption rather than purely for educational purposes is presented as creating a fundamentally different, more demanding environment, and it's in that kind of environment that the creator argues the deepest engineering growth happens — more than any AI tool or traditional course could provide.

## Other Resource Mentioned

A paid Node.js course is also referenced as available for those interested, with an acknowledgment that supporting it would be appreciated.
```

---

Source: [Let’s Handle 1 Million Requests per Second, It’s Scarier Than You Think!](https://youtu.be/W4EwfEU8CGA?si=wK15t9A7NYiBW5aB) — Cododev
