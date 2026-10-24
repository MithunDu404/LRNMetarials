# System Design 1: Foundations, Building Blocks and Storage

> **Series:** **Part 1 (this file)** · [Part 2: Distributed Systems Theory](System%20Design%202%20-%20Distributed%20Systems%20Theory.md) · [Part 3: Building Real Systems in 2026](System%20Design%203%20-%20Building%20Real%20Systems%20in%202026.md) · [Part 4: Worked Case Studies](System%20Design%204%20-%20Worked%20Case%20Studies.md)
> **Self-contained:** the four parts in this folder need nothing else. Each part links only to the others, to its own `images/` and to its own `code/`.
> **Source:** built from research (textbooks, papers and official specs listed in [References](#12-references)). Every number in this guide was recomputed with Python; figures come from [make_figs.py](images/make_figs.py) and code from [system_design_theory.py](code/system_design_theory.py).
> **Facts re-checked:** 24 October 2026 (full audit: PostgreSQL 19 status, isolation and caching details, new diagrams).

**The big picture:** every large system is a set of trade-offs between speed, cost, correctness and survival. To make those trade-offs well, you need to know what the machine, the network and the storage engine are *physically* doing underneath. This part builds that ground floor.

Diagram colours: 🔵 input / primary · 🟣 processing · 🟢 result · 🟠 trade-off · 🔴 failure

---

## Contents

0. [How to use this guide](#0-how-to-use-this-guide)
1. [TL;DR](#1-tldr)
2. [How a system designer thinks](#2-how-a-system-designer-thinks)
3. [The hardware and OS facts that shape every design](#3-the-hardware-and-os-facts-that-shape-every-design)
4. [Networking for system designers](#4-networking-for-system-designers)
5. [The building blocks](#5-the-building-blocks)
6. [Storage engines: how a database really stores data](#6-storage-engines-how-a-database-really-stores-data)
7. [Data models and choosing a database](#7-data-models-and-choosing-a-database)
8. [Transactions and isolation](#8-transactions-and-isolation)
9. [Probabilistic and spatial data structures](#9-probabilistic-and-spatial-data-structures)
10. [Self-check and decision drills](#10-self-check-and-decision-drills)
11. [Glossary](#11-glossary)
12. [References](#12-references)

---

## 0. How to use this guide

| If you have… | Read |
|---|---|
| 10 minutes | §0.1, §1 (TL;DR) and the latency ladder figure in §2.4 |
| 1 hour | §2, §5 and §6: thinking method, building blocks, storage engines |
| A weekend | Everything, then the decision drills in §10, then move to Part 2 |

The four parts build on each other. Part 1 is *one machine and its neighbours*. Part 2 is *many machines that must agree*. Part 3 is *the real systems people build from all of that*. Part 4 is *eight complete designs*, worked from a blank page.

**How this guide trains judgement, not just knowledge.** Facts are cheap; deciding well is the skill. So every part has the same three habits built in:

1. **"The problem" first.** Every concept starts with what breaks without it. If you can't say what problem a tool solves, you can't judge when to use it.
2. **Decision guides.** Wherever there's a real choice (SQL vs NoSQL, cache pattern, consistency level, sync vs async), there's a guide saying *which questions decide it*.
3. **Decision drills** at the end of each part. Each one is a realistic situation with no single right answer. Commit to your answer *before* opening the reasoning. §2.5 explains the thinking toolkit they practise.

### 0.1 First, in completely plain words

Picture a restaurant. One cook can run a small restaurant fine. When the queue goes out of the door, you have choices. You can hire a faster cook, but there is a limit. You can hire more cooks, but now they need to share the fridge and agree on who cooks what. You can prepare popular dishes in advance, but then they might go stale. You can open a second branch across town, but now the two menus can drift apart.

**System design is that same problem with computers.** "Requests" are customers, "servers" are cooks, the "database" is the fridge, a "cache" is the pre-made dishes, and a "CDN" is the branch near the customer.

Three ideas run through everything:

1. **Physics sets the limits.** Reading from memory takes about 100 nanoseconds. A round trip across the Pacific takes about 200 milliseconds, two million times longer. No clever code beats the speed of light.
2. **Every fix creates a new problem.** A cache makes reads fast, but now data can be stale. Copies of the database survive crashes, but now the copies can disagree.
3. **There is no best design, only a design that fits.** A bank and a social feed need opposite trade-offs. Your job is to know the options and pick on purpose.

This part teaches the ground floor: how to reason about requirements and numbers, what the hardware and network really do, the standard building blocks, and how databases store and protect data.

---

## 1. TL;DR

1. **Start from requirements**, not technologies. Non-functional requirements (latency, availability, consistency, durability, cost) decide the architecture.
2. **Estimate before designing.** One day is 86,400 seconds, so 1 million requests per day is only about 12 per second on average. Always multiply by a peak factor.
3. **Know the latency ladder.** RAM ≈ 100 ns, SSD ≈ 20 µs, same-datacenter round trip ≈ 0.5 ms, cross-continent ≈ 80–200 ms. The steps aren't equal: RAM → SSD is about 200×, SSD → datacenter round trip about 25×, and datacenter → another continent about 160–400×. From RAM to an ocean crossing is about **two million times** slower.
4. **Sequential I/O beats random I/O**, by about 500× on spinning disks and still a lot on SSDs. Log-structured designs exist because of this.
5. **Round trips are the enemy of latency.** TCP + TLS 1.3 costs 2 round trips before the request even starts. QUIC (HTTP/3) cuts that to 1, or 0 on resumption.
6. **Caching** trades freshness for speed. A 90% hit ratio with a 1 ms cache and a 20 ms database gives an average of 3 ms and 10× less database load.
7. **B-trees** update pages in place, which makes reads fast and predictable. **LSM-trees** append and merge later, which makes writes fast. Neither wins everywhere.
8. **Isolation levels** are about which anomalies you allow. "Repeatable read" and "snapshot isolation" still allow *write skew*. Only serializable stops everything.
9. **Probabilistic structures** trade a small, known error for huge memory savings. A Bloom filter needs about 10 bits per key for 1% false positives. HyperLogLog counts billions of distinct items in 12 KB at about 0.8% error.

---

## 2. How a system designer thinks

### 2.1 Requirements come first

**The problem.** If you start by picking Kafka and Cassandra, you have answered a question nobody asked. Different requirements produce different architectures.

**How it works.** Split requirements into two kinds:

- **Functional requirements**: what the system does. "Users can post a photo." "Users see a feed of people they follow."
- **Non-functional requirements (NFRs)**: how well it must do it. These drive the design:

| NFR | The question it asks | Typical way to state it |
|---|---|---|
| **Scalability** | How much load, and how fast does it grow? | 50k reads/s at peak, growing 2× per year |
| **Latency** | How fast must one request be? | p99 < 200 ms for the feed |
| **Availability** | What fraction of time must it work? | 99.95% monthly |
| **Consistency** | Can a user see stale or out-of-order data? | "A user always sees their own post at once" |
| **Durability** | Can we ever lose acknowledged data? | Zero loss of payments; feed likes can be lossy |
| **Cost** | What can we spend? | < $0.01 per 1,000 requests |
| **Security & compliance** | Who may see what, and where may data live? | EU data stays in the EU |

Two habits separate strong designers:

1. **Use percentiles, not averages.** "p99 = 200 ms" means 99% of requests finish within 200 ms. Averages hide the slow requests, and slow requests are the ones users remember. (Part 3 §3 shows why tails get worse at scale.)
2. **Requirements can differ inside one system.** In a shopping site, the payment path needs strong consistency and zero data loss. The "recommended for you" path can be stale, lossy and approximate. Design each path for its own needs.

### 2.2 Trade-offs are the job

**The problem.** Every important decision gives something up. Engineers who don't name the cost end up paying it by surprise.

The classic trade-offs you will meet again and again:

| You gain… | …and pay with | Example |
|---|---|---|
| Lower latency | Staleness | Caches, read replicas, CDNs |
| Strong consistency | Latency and availability during failures | Consensus on every write (Part 2) |
| Write throughput | Read cost and background work | LSM-trees (§6.2) |
| Read speed | Write cost and storage | Indexes, denormalisation |
| Availability | Possible conflicts to merge | Multi-leader and leaderless replication (Part 2) |
| Simplicity | Scale ceiling | One big database vs sharding |
| Flexibility | Performance | Generic JSON documents vs typed columns |
| Cost savings | Headroom | Running servers hot (Part 3 §3: latency explodes near 100%) |

A good design document names each trade-off and says *why* this side was chosen for this requirement.

### 2.3 Back-of-the-envelope estimation

**The problem.** "Do we need one database or a hundred?" You must answer this before choosing anything, and you have minutes, not days.

**How it works.** Estimate four things: **traffic (QPS)**, **storage**, **bandwidth**, and **memory for caching**. Round hard. You want the right power of ten, not three significant figures.

The two facts that make it fast:

$$
\text{average QPS} = \frac{\text{requests per day}}{86{,}400}
$$

Read that out loud: *average queries per second is the daily request count divided by the number of seconds in a day (86,400).*

$$
\text{peak QPS} \approx \text{average QPS} \times \text{peak factor}
$$

*Peak traffic is the average times a peak factor.* The peak factor is usually 2–5 for consumer apps (evenings, events).

A handy shortcut: **1 million per day ≈ 12 per second** (1,000,000 / 86,400 = 11.57).

**Worked example: a Twitter-like service.** Assume 300 million daily active users. Each posts 2 times a day and reads 100 posts a day. Each post with its metadata is about 1 KB.

| Quantity | Calculation | Result |
|---|---|---|
| Write QPS (average) | 300M × 2 / 86,400 | **≈ 6,900/s** |
| Write QPS (peak, ×3) | 6,944 × 3 | ≈ 21,000/s |
| Read QPS (average) | 300M × 100 / 86,400 | **≈ 347,000/s** |
| Read QPS (peak, ×3) | 347,222 × 3 | ≈ 1,000,000/s |
| New storage per day | 600M posts × 1 KB | 600 GB/day |
| Storage over 5 years | 600 GB × 365 × 5 | ≈ **1.1 PB** (text only) |

Notice what the numbers already tell you, before any design:

- The **read:write ratio is 50:1**. Optimise reads: caching, precomputed feeds, replicas.
- **1 million reads per second** cannot come from one database. You need caching and partitioning.
- **1.1 PB** does not fit on one machine. Storage must be partitioned (sharded).

Media (photos, video) is usually 100× bigger than text and goes in object storage plus a CDN. Estimate it separately.

### 2.4 The latency ladder: numbers every engineer should know

**The problem.** You cannot judge a design without knowing what each step costs. "Call the database twice" is fine inside a datacenter (about 1 ms) and terrible across continents (about 400 ms).

![Fig 1 – Latency ladder (fig01_latency_ladder.png): approximate time for common operations on a log scale, from a 1 ns L1 cache hit to a 200 ms US–Australia round trip.](images/fig01_latency_ladder.png)

*Fig 1 (fig01_latency_ladder.png). Orders of magnitude, not benchmarks. Exact values change with hardware; the ratios are what matter.*

The rules to take away:

1. **RAM is about 200× faster than an NVMe SSD read (100 ns vs 20 µs), and an SSD read is about 25× faster than a datacenter round trip (20 µs vs 500 µs).** Keep hot data in RAM, and notice that *a local SSD beats a network call*. That's why reading a local replica or an embedded store can beat a remote cache.
2. **A network round trip inside a datacenter (~0.5 ms) costs as much as thousands of memory reads.** Batch your calls. Avoid chatty protocols.
3. **Cross-continent round trips (80–200 ms) are set by the speed of light in fibre** (about 200,000 km/s, two-thirds of the speed in a vacuum). The only fix is to move data closer to the user: CDNs, edge computing, regional replicas.
4. **Sequential reads are much faster than random ones** (see §3.2).

### 2.5 Making decisions: a toolkit for thinking like a system designer

**The problem.** Knowing what Kafka, Raft and B-trees are doesn't tell you *what to do* on Monday morning. Two engineers with the same knowledge make very different designs. The difference is how they decide. This section is the thinking method that every later "decision guide" and "decision drill" uses.

**The decision loop.** Run every significant decision through these seven steps. It takes minutes, and it catches most bad designs before they're built.

```mermaid
flowchart LR
    accTitle: The design decision loop
    accDescr: Clarify the real problem, quantify it, generate at least two options, test them against requirements, choose and name the trade-off, state what would change your mind, then check how reversible it is.
    A["1. Clarify<br/>the real problem"] --> B["2. Quantify<br/>numbers, not adjectives"]
    B --> C["3. Generate<br/>at least 2 options"]
    C --> D["4. Test against<br/>requirements + failures"]
    D --> E["5. Choose<br/>and name the cost"]
    E --> F["6. Say what would<br/>change your mind"]
    F --> G{"7. Reversible?"}
    G -->|"yes"| H(["Decide fast,<br/>measure, adjust"])
    G -->|"no"| I(["Slow down: prototype,<br/>review, write it down"])
    class A,B primary;
    class C,D,E,F intermediate;
    class H target;
    class I warning;
    classDef primary fill:#EFF6FF,stroke:#2563EB,stroke-width:1.5px,color:#0F172A;
    classDef intermediate fill:#FAF5FF,stroke:#7C3AED,stroke-width:1.5px,color:#0F172A;
    classDef target fill:#F0FDF4,stroke:#059669,stroke-width:2px,color:#0F172A;
    classDef warning fill:#FFFBEB,stroke:#D97706,stroke-width:1.5px,color:#92400E;
```

1. **Clarify the real problem.** "We need Kafka" is a solution, not a problem. Ask "what goes wrong today, for whom, and how often?" Often the real problem is smaller (one slow query) or different (the team can't deploy independently).
2. **Quantify.** Replace adjectives with numbers: "lots of traffic" becomes "4,000 writes/s at peak, growing 50% a year". Numbers kill bad options fast (§2.3). A design for 400 writes/s and one for 400,000 writes/s are different designs.
3. **Generate at least two options**, and include the boring one ("one PostgreSQL database with a read replica"). If you only have one option, you haven't made a decision; you've made an assumption.
4. **Test each option against the requirements *and* against failure.** For each, ask: what happens when a node dies, the network is slow, traffic doubles, or a request is retried twice?
5. **Choose, and name the cost out loud.** "We pick X; we accept Y." If you can't name what you're giving up, you don't understand the option yet.
6. **Say what would change your mind.** "If writes pass 20,000/s, or we need cross-region writes, we revisit this." That turns a frozen opinion into a monitored decision.
7. **Check reversibility.** Some decisions are **two-way doors**: cheap to undo (instance size, cache TTL, a library, a timeout). Decide those quickly and measure. Others are **one-way doors**: expensive or impossible to undo. Spend your care on those.

| Usually a **one-way door** (decide slowly) | Usually a **two-way door** (decide fast) |
|---|---|
| The data model and primary keys | Instance sizes and counts |
| The partition (shard) key | Cache TTLs, pool sizes, timeouts |
| Consistency guarantees promised to users or other teams | Which internal library or framework version |
| Public API shapes and event schemas others consume | Internal service boundaries behind one API |
| Choice of primary database for critical data | Adding a cache or a read replica |
| Data residency and deletion guarantees | Deployment strategy, alert thresholds |

**Questions that expose hidden requirements.** Before designing, ask these out loud. Each one has changed a real design:

- **Who** uses it, and **how many**? Read-heavy or write-heavy? What's the ratio?
- What happens to the user if it's **slow**? **Down**? **Wrong**? **Duplicated**? **Lost**? (The answers set latency, availability, consistency, idempotency and durability.)
- Which data **must** be strongly consistent, and which can be minutes stale?
- How fast does it **grow**? What does traffic look like on the worst day (a sale, a launch, a news event)?
- What are the **access patterns**: by key, by range, by text search, by relationship, by time?
- What does the **team** know how to run? What's the **budget**?
- Are there **legal** constraints: where data lives, how long it's kept, who may see it?

**Heuristics that hold up in practice:**

1. **Start with the simplest design that meets the numbers.** A single well-tuned PostgreSQL primary with replicas carries far more load than most products ever reach. Add distribution only when a number forces you to.
2. **Every new component is a new failure mode, a new thing to monitor, and a new thing to be on call for.** A cache, a queue or a new service has to pay for itself.
3. **Put strong consistency only where the business needs it** (money, inventory, identity, permissions) and make everything else fast and eventually consistent. Finding those few points is most of the design.
4. **Design for 10×, not 1,000×.** Systems usually get rewritten before 1,000× anyway, and the 1,000× design is slower and costlier today.
5. **Make operations idempotent and services stateless by default.** It's cheap at the start and very expensive to retrofit.
6. **Measure before optimising.** Profile, trace and load-test. Intuition about bottlenecks is wrong surprisingly often.
7. **Prefer boring, well-understood technology** for the core. Spend your "innovation budget" only where it's a competitive advantage.

**Second-order thinking: "and then what?"** Every fix has consequences, and good designers follow them one more step:

| First-order fix | Second-order consequence you must design for |
|---|---|
| Add a cache | Stale data, invalidation bugs, a stampede when it empties (§5.3) |
| Add retries | Retry storms that keep an overloaded service down (Part 3 §5.1, §5.3) |
| Split into microservices | Distributed transactions, network failures, harder debugging (Part 2 §8, Part 3 §10) |
| Add a read replica | Replication lag: users may not see their own writes (Part 2 §3.2) |
| Shard the database | Cross-shard queries and transactions; hot shards; rebalancing (Part 2 §4) |
| Go multi-region | Conflicting writes, or cross-region latency on every write (Part 2 §5.4, Part 3 §5.7) |
| Autoscale aggressively | A traffic spike scales up the database's client connections too (§6.6) |

**The premortem.** Before building, imagine it's six months later and the system has failed badly. Write down the three most likely reasons. Each reason is either a risk to design out now, or an alert to add. It's the cheapest reliability work there is.

**A worked decision: PostgreSQL or DynamoDB for an orders service?** A **weighted decision matrix** forces you to make your priorities explicit. Score each option 1–5 on each criterion, multiply by the criterion's weight, and add up.

| Criterion (weight) | PostgreSQL | DynamoDB |
|---|---|---|
| Multi-row transactions (×3) | 5 → 15 | 3 → 9 |
| Operational burden (×2) | 3 → 6 | 5 → 10 |
| Scale headroom (×2) | 3 → 6 | 5 → 10 |
| Query flexibility (×2) | 5 → 10 | 2 → 4 |
| Cost at our current scale (×1) | 4 → 4 | 3 → 3 |
| **Total** | **41** | **36** |

PostgreSQL wins. But do one more step: a **sensitivity check**. If scale headroom really matters more (weight 4 instead of 2), the totals become 47 vs 46, nearly a tie. **What you've learned is that the decision hinges on the growth forecast.** So the right next action isn't "pick Postgres"; it's "get a credible growth estimate". The matrix doesn't make the decision for you. It shows which assumption the decision depends on, and that's where to spend effort.

**Smells that a design hasn't been thought through:**

- A technology was chosen before the requirements were written down.
- No numbers anywhere: no QPS, no data size, no latency target.
- "It's highly available" with no answer to "what happens when *this* box dies?"
- Strong consistency everywhere "to be safe", or eventual consistency everywhere "for scale". Both mean nobody decided per path.
- No mention of retries, timeouts, idempotency or what happens on a duplicate message.
- No migration or rollback plan, and no answer to "how do we know it's working?"

> **"It depends" is only half an answer.** Always finish the sentence: "it depends *on the read/write ratio; above about 10:1 I'd add a cache*". Naming what it depends on is the skill being tested, in interviews and at work.

---

## 3. The hardware and OS facts that shape every design

### 3.1 The memory hierarchy and locality

**The problem.** CPUs are much faster than memory. A CPU can do hundreds of operations in the time one RAM access takes. Without caches, it would sit idle most of the time.

**How it works.** Hardware stacks small, fast memories in front of big, slow ones: registers → L1 cache (~1 ns) → L2 (~4 ns) → L3 (~10–40 ns) → RAM (~100 ns) → SSD → disk → network. Each level holds copies of data the level below holds.

Caches work because programs show **locality**:

- **Temporal locality**: data used now will likely be used again soon.
- **Spatial locality**: data next to what you used will likely be used soon. Memory moves in **cache lines** (usually 64 bytes), so reading one byte brings its 63 neighbours along for free.

**Why this matters for system design:** the same idea repeats at every scale. A CDN is a cache for a datacenter. Redis is a cache for a database. The OS page cache is a cache for the disk. Each one only pays off when the access pattern has locality, which real traffic usually does: a few items are very popular. That skew is why a cache holding 1% of items can serve half the requests (§5.3 works out the numbers).

### 3.2 Disks: random vs sequential

**The problem.** Storage speed depends heavily on the *pattern* of access, not just the device.

**How it works.**

- A **hard disk (HDD)** has a spinning platter and a moving arm. A random read must move the arm (seek) and wait for the platter to rotate: about 5–10 ms. That limits it to roughly **100 random operations per second (IOPS)**. Reading *sequentially*, the arm stays put and data streams at about 200 MB/s.
- An **SSD** has no moving parts. Random reads take about 20–100 µs, and NVMe drives reach hundreds of thousands of IOPS. But SSDs write in pages and erase in larger blocks. Many small random overwrites cause **write amplification** inside the drive and wear it out faster.

**Worked example.** Read 4 KB blocks at random from an HDD at 100 IOPS:

$$
100 \ \tfrac{\text{ops}}{\text{s}} \times 4 \ \text{KB} = 400 \ \text{KB/s}
$$

*One hundred operations per second, four kilobytes each, gives four hundred kilobytes per second.* The same disk reads sequentially at 200 MB/s, which is **500× faster** (200,000 KB/s ÷ 400 KB/s). An NVMe SSD at 100,000 IOPS × 4 KB gives 400 MB/s even for random reads. That is why SSDs changed database design, and why log-structured storage (§6.2) still helps: turning random writes into sequential ones pays off on every device.

### 3.3 The page cache, fsync and what "saved" really means

**The problem.** When your program calls `write()`, the data has usually *not* reached the disk. If the power fails, it can vanish. Databases that promise durability must handle this.

**How it works.**

1. `write()` copies data into the OS **page cache** (RAM) and returns at once. This is fast.
2. The OS flushes dirty pages to disk later, often seconds later.
3. `fsync()` forces the data to stable storage and waits. This is slow: about a millisecond or more on SSDs, more on HDDs.

So every durable database faces a trade-off: **fsync on every commit** (safe, slow) vs **group commit** (wait a few milliseconds, fsync many transactions together) vs **async flush** (fast, can lose the last moments of data in a crash). Settings like PostgreSQL's `synchronous_commit` or Kafka's `acks` and flush settings are exactly this dial.

> **Durability is a spectrum.** "Written to the page cache" < "fsynced to one disk" < "replicated to another machine" < "replicated to another datacenter". Each step survives a bigger disaster and costs more latency.

### 3.4 Concurrency: threads, event loops and locks

**The problem.** A server must handle many requests at once. Most of each request's time is spent *waiting* (for the database, the network, the disk), not computing.

**How it works.** There are two main models:

| Model | How it works | Strength | Weakness |
|---|---|---|---|
| **Thread per request** | Each request gets an OS thread that blocks while waiting | Simple code | Each thread costs memory (often ~1 MB of stack) and context switches cost CPU. Tens of thousands of threads hurt. |
| **Event loop (async I/O)** | One thread per core juggles thousands of connections using `epoll`/`kqueue`/`io_uring` and never blocks | Handles huge numbers of idle connections cheaply (Node.js, Nginx, Netty) | One slow computation blocks everyone on that loop |
| **Lightweight threads** | The runtime maps many cheap "green threads" onto few OS threads (Go goroutines, Java virtual threads) | Simple blocking-style code with event-loop efficiency | Runtime-specific behaviour |

When threads share data, they need **synchronisation**:

- A **mutex (lock)** lets one thread at a time into a critical section. Under heavy **contention**, threads queue on the lock and adding cores stops helping (this is the serial fraction in Amdahl's law, Part 3 §3).
- A **deadlock** happens when two threads each hold a lock the other needs. The standard prevention is to always take locks in the same global order.
- **Lock-free** structures use atomic CPU instructions such as compare-and-swap (CAS): "set X to new only if it still equals old". The same CAS idea reappears in distributed systems as conditional writes and optimistic concurrency (§8.5).

**The key insight:** the same problems (races, lost updates, deadlocks) come back at distributed scale in Part 2, but worse, because machines can also crash halfway and messages can be delayed.

---

## 4. Networking for system designers

### 4.1 The layers that matter

You need four layers in your head:

| Layer | Job | Examples |
|---|---|---|
| Application (L7) | Meaning of messages | HTTP, gRPC, DNS, WebSocket |
| Transport (L4) | Process-to-process delivery | TCP, UDP, QUIC (runs over UDP) |
| Network (L3) | Machine-to-machine routing | IP, BGP routing between networks |
| Link (L2) | Next hop on the wire | Ethernet, Wi-Fi |

"L4 load balancer" and "L7 load balancer" (§5.1) refer to these layers: what the balancer can see and act on.

### 4.2 TCP: reliable, ordered, and full of round trips

**The problem.** IP delivers packets on a best-effort basis. They can be lost, duplicated, reordered or delayed. Applications want a clean, ordered stream of bytes.

**How it works.**

1. **Three-way handshake.** Client sends SYN, server replies SYN-ACK, client sends ACK. That costs **one round trip (RTT)** before any data flows.
2. **Reliability.** Every byte has a sequence number. The receiver acknowledges what it got, and the sender retransmits what goes missing.
3. **Flow control.** The receiver advertises a window: "I have room for N more bytes." This stops a fast sender from drowning a slow receiver.
4. **Congestion control.** The sender also limits itself to protect the *network*. It starts slowly (**slow start**), roughly doubling its congestion window every RTT, and backs off when it sees loss. Modern algorithms include CUBIC (the Linux default) and BBR.

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    C->>S: SYN
    S->>C: SYN-ACK
    C->>S: ACK + first request bytes
    Note over C,S: 1 RTT spent before the request starts
    S->>C: Response (limited by congestion window)
```

**Worked example: why a "small" 1 MB response is slow on a new connection.** Modern TCP starts with an initial window of 10 segments × 1,460 bytes = 14.6 KB. The window doubles each RTT: 14.6, 29.2, 58.4, 116.8, 233.6, 467.2, 934.4 KB…

| RTT | Sent this RTT | Total sent |
|---|---|---|
| 1 | 14.6 KB | 14.6 KB |
| 2 | 29.2 KB | 43.8 KB |
| 3 | 58.4 KB | 102.2 KB |
| 4 | 116.8 KB | 219.0 KB |
| 5 | 233.6 KB | 452.6 KB |
| 6 | 467.2 KB | 919.8 KB |
| 7 | 934.4 KB | 1,854.2 KB ✓ |

So 1 MB needs **7 RTTs** of slow start. At 100 ms RTT, that is 700 ms, even on a gigabit link. This is why connection reuse (keep-alive, connection pools) and CDNs near users matter so much.

**Bandwidth-delay product.** To keep a pipe full, the amount of data "in flight" must equal bandwidth × RTT:

$$
\text{BDP} = \text{bandwidth} \times \text{RTT}
$$

*The bytes you must have in flight equal the link speed times the round-trip time.* For 1 Gbit/s and 100 ms: $10^9 \times 0.1 / 8 = 12.5$ MB. If the windows are smaller than that, the link sits idle part of the time.

**Head-of-line (HOL) blocking.** TCP delivers bytes strictly in order. If one packet is lost, every later byte waits for its retransmission, even bytes that belong to unrelated requests sharing the connection. Keep this in mind for HTTP/2 below.

### 4.3 UDP

UDP sends independent datagrams with no handshake, no ordering, no retransmission and no congestion control. It suits cases where a late packet is useless anyway (live video, games, VoIP), or where the application builds its own reliability on top. QUIC is the big example.

### 4.4 HTTP/1.1 → HTTP/2 → HTTP/3

**The problem.** A web page needs dozens of resources. Each round trip costs latency, so protocols evolved to waste fewer.

| Version | Key idea | Remaining problem |
|---|---|---|
| **HTTP/1.1** (1997) | Keep-alive: reuse a TCP connection for several requests, one after another | Only one request in flight per connection, so browsers open ~6 connections per host |
| **HTTP/2** (2015) | Multiplexing: many concurrent streams over one TCP connection, binary framing, header compression (HPACK) | One lost TCP packet stalls *all* streams (TCP head-of-line blocking) |
| **HTTP/3** (2022, RFC 9114) | Runs over **QUIC** (RFC 9000) on UDP. Each stream is independent, so loss on one doesn't stall the others. TLS 1.3 is built into the handshake. Connections survive network changes (Wi-Fi → mobile) via connection IDs. | UDP is sometimes blocked or throttled by middleboxes, so clients fall back to HTTP/2 |

![Fig 2 – Handshake round trips (fig02_handshake_rtts.png): time until the response arrives at 100 ms RTT for TCP+TLS 1.2 (400 ms), TCP+TLS 1.3 (300 ms), QUIC first visit (200 ms) and QUIC 0-RTT (100 ms).](images/fig02_handshake_rtts.png)

*Fig 2 (fig02_handshake_rtts.png). Counting round trips at RTT = 100 ms: handshake RTTs plus one for the request itself.*

Reading the figure: TCP (1 RTT) + TLS 1.2 (2 RTT) + request (1 RTT) = 4 RTT = 400 ms. TLS 1.3 cuts its handshake to 1 RTT, giving 300 ms. QUIC merges the transport and TLS handshakes into 1 RTT, giving 200 ms. On a repeat visit, **0-RTT** sends the request with the very first packet, giving 100 ms.

> **0-RTT has a catch.** Data in the first flight can be *replayed* by an attacker. Only use it for idempotent requests, such as a GET with no side effects. Idempotency comes back in Part 2 §7.

### 4.5 TLS 1.3 in one paragraph (and the post-quantum change)

TLS gives you three things: **confidentiality** (encryption), **integrity** (no tampering), and **authentication** (the server proves its identity with a certificate signed by a trusted authority). In TLS 1.3, client and server agree a fresh shared key with an ephemeral key exchange, which gives *forward secrecy*: stealing the server's long-term key later cannot decrypt past traffic. **mTLS** (mutual TLS) makes the client present a certificate too. It is the standard way services authenticate each other inside a zero-trust network (Part 3 §7).

**What changed by 2026:** the major browsers and CDNs now use a **hybrid post-quantum key exchange** (`X25519MLKEM768`) by default. It combines a classical elliptic-curve exchange with ML-KEM (the NIST post-quantum standard, FIPS 203), so the session stays safe if either one is broken. The motivation is "harvest now, decrypt later": attackers may record traffic today and decrypt it once quantum computers arrive. Certificates (signatures) are still mostly classical. That migration is harder and still under way.

### 4.6 DNS: the internet's phone book

**The problem.** Humans and configs use names (`api.example.com`). Machines route by IP address. Something must translate, fast, billions of times a day.

**How it works.**

```mermaid
sequenceDiagram
    participant B as Browser / OS cache
    participant R as Recursive resolver
    participant Root as Root server
    participant TLD as .com server
    participant Auth as example.com authoritative
    B->>R: api.example.com?
    R->>Root: api.example.com?
    Root->>R: ask the .com servers
    R->>TLD: api.example.com?
    TLD->>R: ask example.com's servers
    R->>Auth: api.example.com?
    Auth->>R: 203.0.113.10 (TTL 60 s)
    R->>B: 203.0.113.10
    Note over B,R: Cached at every level until the TTL expires
```

Ideas a designer uses:

- **TTL (time to live)** controls how long answers are cached. A low TTL (30–60 s) lets you fail over quickly but sends more queries. A high TTL is cheap but slow to change. Many clients ignore TTLs and cache longer, so never rely on DNS for instant failover.
- **GeoDNS / latency-based routing**: answer with the IP of the nearest region.
- **Anycast**: announce *the same IP* from many locations. The internet's routing protocol (BGP) delivers each user to the nearest one. CDNs and public resolvers (such as 1.1.1.1 and 8.8.8.8) work this way, which also spreads out DDoS traffic.

### 4.7 Cloud networking basics: VPCs, subnets and NAT

**The problem.** In the cloud, your servers live on a network you design yourself. Get it wrong and your database is reachable from the internet, or your app can't reach anything at all. Every cloud architecture diagram assumes you know these few pieces.

**How it works.**

- A **VPC (virtual private cloud)** is your own private network inside one cloud region, with an address range written in **CIDR** notation. `10.0.0.0/16` means "the first 16 bits are fixed", leaving $2^{32-16} = 65{,}536$ addresses.
- You split the VPC into **subnets**, each inside one availability zone. A `/24` subnet has $2^{8} = 256$ addresses (AWS reserves 5 in each, leaving 251 usable). Use one set of subnets per AZ so that losing an AZ doesn't take everything down.
- A **public subnet** has a route to an **internet gateway**, so things in it can have public IPs. A **private subnet** has no inbound route from the internet.
- **NAT (network address translation)** lets many private machines share one public IP for *outgoing* traffic (downloading updates, calling an external API). The NAT device remembers each outgoing connection and maps replies back. Nobody outside can *start* a connection to a private machine. A managed **NAT gateway** does this per AZ.
- **Security groups** are stateful firewalls attached to each instance ("allow port 5432 only from the app servers' group"). Return traffic is allowed automatically. **Network ACLs** are stateless rules on whole subnets, a coarser second layer.
- To reach other networks: **VPC peering** or a **transit gateway** (VPC to VPC), **private endpoints** (reach cloud services such as S3 without crossing the internet), and **VPN** or a dedicated line such as Direct Connect (reach your own datacenter).

**The standard layout:**

```mermaid
flowchart LR
    accTitle: Standard VPC layout
    accDescr: Internet traffic reaches a load balancer in public subnets; app servers and databases sit in private subnets; outbound traffic from private subnets leaves through a NAT gateway.
    NET(["Internet"]) --> IGW["Internet gateway"]
    subgraph vpc ["VPC 10.0.0.0/16, one set of subnets per AZ"]
        subgraph pub ["Public subnets"]
            LB["Load balancer"]
            NAT["NAT gateway"]
        end
        subgraph priv ["Private subnets"]
            APP["App servers"]
            DB[("Database")]
        end
    end
    IGW --> LB
    LB --> APP
    APP --> DB
    APP -->|"outbound only"| NAT
    NAT --> IGW
    class NET primary;
    class IGW,LB,NAT intermediate;
    class APP,DB target;
    classDef primary fill:#EFF6FF,stroke:#2563EB,stroke-width:1.5px,color:#0F172A;
    classDef intermediate fill:#FAF5FF,stroke:#7C3AED,stroke-width:1.5px,color:#0F172A;
    classDef target fill:#F0FDF4,stroke:#059669,stroke-width:2px,color:#0F172A;
```

Only the load balancer faces the internet. App servers and databases sit in private subnets, and the database's security group accepts connections only from the app servers. **Two cost surprises to watch:** NAT gateways charge per GB processed, and traffic between AZs is billed too. Chatty cross-AZ services and heavy outbound traffic through NAT show up on the bill (Part 3 §6.5).

---

## 5. The building blocks

These are the Lego bricks of every architecture. For each one we cover what it's for, how it works, and (most important) how it fails.

```mermaid
flowchart LR
    accTitle: Request path through standard building blocks
    accDescr: A user request passes DNS, CDN, load balancer, gateway, stateless services, then cache and database.
    U(["User"]) --> DNS["DNS<br/>name to nearest IP"]
    DNS --> CDN["CDN edge<br/>static + cacheable"]
    CDN --> LB["Load balancer<br/>L4 / L7"]
    LB --> GW["API gateway<br/>auth, rate limit, routing"]
    GW --> S1["Stateless service<br/>many copies"]
    S1 --> C[("Cache<br/>Redis / Memcached")]
    S1 --> DB[("Database<br/>primary + replicas")]
    S1 --> Q[["Queue / log<br/>async work"]]
    class U primary;
    class DNS,CDN,LB,GW,S1 intermediate;
    class C,DB,Q target;
    classDef primary fill:#EFF6FF,stroke:#2563EB,stroke-width:1.5px,color:#0F172A;
    classDef intermediate fill:#FAF5FF,stroke:#7C3AED,stroke-width:1.5px,color:#0F172A;
    classDef target fill:#F0FDF4,stroke:#059669,stroke-width:2px,color:#0F172A;
```

### 5.1 Load balancers

**The problem.** Many server copies are useless unless traffic is spread across them, and sent only to healthy ones.

**How it works.**

- An **L4 load balancer** sees only IP addresses and ports. It forwards TCP/UDP connections without reading them. It is very fast and protocol-agnostic, but it cannot route by URL or header.
- An **L7 load balancer** terminates the connection and reads HTTP. It can route `/api/*` and `/images/*` to different pools, retry, add headers, and terminate TLS. It costs more CPU, and it sees the plaintext.

**Algorithms:**

| Algorithm | Idea | Use when |
|---|---|---|
| Round robin / weighted | Take turns, possibly weighted by capacity | Requests cost about the same |
| Least connections / least outstanding requests | Send to the least busy server | Request costs vary |
| **Power of two choices** | Pick 2 servers at random, send to the less loaded one | Large fleets. Close to the best possible, with no global state. |
| Consistent hashing on a key | The same key always goes to the same server | You need cache affinity or sticky sessions (Part 2 §4.2) |

**Why the choice matters more than it looks.** Round robin is *blind*: it keeps sending a slow server its full share. Suppose one of four servers slows to half speed (a noisy neighbour, a long GC pause). Round robin still gives it 25% of the traffic, but it can only finish about 12.5%. Its queue grows without limit, and every request that lands there waits longer and longer. Part 3 §4.2 shows the maths: waiting time explodes as utilisation nears 100%. **Load-aware** algorithms (least outstanding requests, power of two choices) notice the queue and route around it.

Power of two choices is the surprising one. Picking the less-loaded of just *two* random servers is dramatically better than picking one at random. With $n$ servers and random placement, the busiest server's excess load grows like $\log n / \log \log n$; with two choices it grows only like $\log \log n$ (Mitzenmacher, 2001). It needs no global view of the fleet, so many independent load balancers can use it at once without coordinating. That's why it's common in large systems such as Envoy and Nginx's `random two` mode.

**Health checks** remove dead servers: *active* checks probe an endpoint every few seconds, and *passive* checks watch real traffic for errors. A load balancer must itself be redundant: an active-passive pair sharing a floating IP, or many instances behind anycast or DNS.

### 5.2 Reverse proxy, API gateway, service mesh

These overlap, so here's the distinction:

- **Reverse proxy** (Nginx, Envoy, HAProxy): sits in front of servers, terminates TLS, caches, compresses, and forwards.
- **API gateway**: a reverse proxy with API-specific *policy* at the edge: authentication, rate limiting, request validation, API keys and quotas, routing to many backend services, and sometimes response aggregation.
- **Service mesh** (Istio, Linkerd): the same features (mTLS, retries, timeouts, traffic shifting, telemetry) applied to *internal* service-to-service traffic. It is done with a proxy beside each service (sidecar) or a per-node proxy (the newer "ambient" or sidecar-less mode).

Rule of thumb: the gateway handles **north-south** traffic (clients into your system). The mesh handles **east-west** traffic (between your services).

### 5.3 Caching: the theory and the failure modes

**The problem.** The database is the slowest and hardest-to-scale part of most systems, and most reads ask for the same few items again and again.

**How it works.** Keep copies of hot data in a faster store. The core formula is expected latency:

$$
T_{\text{avg}} = h \cdot T_{\text{hit}} + (1 - h) \cdot T_{\text{miss}}
$$

*The average latency is the hit ratio times the hit time, plus the miss ratio times the miss time.* Here $h$ is the hit ratio (the fraction of requests found in the cache). The miss time includes the cache check *and* the database trip.

**Worked example.** Cache hit = 1 ms. Miss = 1 ms (check) + 20 ms (database) = 21 ms.

| Hit ratio $h$ | Average latency | Database load (fraction of reads) |
|---|---|---|
| 50% | 0.5 × 1 + 0.5 × 21 = **11 ms** | 50% |
| 90% | 0.9 × 1 + 0.1 × 21 = **3 ms** | 10% |
| 99% | 0.99 × 1 + 0.01 × 21 = **1.2 ms** | 1% |

Read the last column again: **going from 90% to 99% hits cuts database load by another 10×.** The last few percent of hit ratio are often worth more than they look.

**How big must the cache be? It depends on skew.** Real traffic is very uneven: a few items get most of the requests. A common model is the **Zipf distribution**: the item of popularity rank $r$ is requested with probability proportional to $1/r^{s}$. Here $s$ measures how skewed the traffic is ($s \approx 1$ is typical for web content).

An ideal cache holding the $k$ most popular of $N$ items then serves this fraction of requests:

$$
h(k) = \frac{\sum_{r=1}^{k} r^{-s}}{\sum_{r=1}^{N} r^{-s}}
$$

*The hit ratio is the popularity of the top k items divided by the popularity of all items.*

**Worked example.** A catalogue of 100,000 items with $s = 1$:

| Cache size | Ideal hit ratio | Real LRU (simulated) |
|---|---|---|
| 0.1% (100 items) | 43% | — |
| **1% (1,000 items)** | **62%** | **51%** |
| 10% (10,000 items) | 81% | — |

![Fig 13 – Zipf cache hit ratio (fig13_zipf_cache.png): hit ratio against cache size for Zipf skew 0.8, 1.0 and 1.2, against uniform traffic, with simulated LRU points.](images/fig13_zipf_cache.png)

*Fig 13 (fig13_zipf_cache.png). With typical skew, a cache holding 1% of the items serves about half of the requests even with plain LRU. With no skew (the dotted line), a 1% cache serves 1%. **Measure your skew before sizing a cache:** it decides whether a cache helps a lot or barely at all. LRU falls below the ideal because one-off requests push popular items out, which is the problem LFU-style policies address.*

**Patterns** (who loads and who writes):

| Pattern | Reads | Writes | Trade-off |
|---|---|---|---|
| **Cache-aside** (most common) | App checks the cache; on a miss it reads the DB and fills the cache | App writes the DB, then *deletes* the cache key | Simple. Brief staleness is possible. The first read after a delete is slow. |
| **Read-through** | Cache loads from the DB itself on a miss | — | App code is simpler; needs a cache that knows the DB |
| **Write-through** | — | Write goes to the cache *and* DB synchronously | Cache always fresh; writes are slower |
| **Write-back (write-behind)** | — | Write to the cache, flush to the DB later | Very fast writes; **data loss** if the cache dies before flushing |
| **Write-around** | — | Write straight to the DB, skipping the cache | Avoids filling the cache with data nobody reads |

> **Why "delete", not "update", on write?** If two writers update the cache in different orders from the DB, the cache ends up wrong *forever*. Deleting lets the next read fetch the truth. A small race remains (a slow reader can re-insert a stale value), which is why caches also use TTLs as a safety net.

**The race that remains, step by step.** It needs a cache miss and a write to overlap, which is rare but happens every day at scale:

```mermaid
sequenceDiagram
    participant R as Reader
    participant C as Cache
    participant DB as Database
    participant W as Writer
    R->>C: get(price) → miss
    R->>DB: read price → 10 (old)
    W->>DB: write price = 12
    W->>C: delete(price)
    Note over R: reader was slow (GC pause, network)
    R->>C: set(price = 10)
    Note over C: Stale value 10 now sits in the cache until its TTL expires
```

The reader read *before* the write and stored its result *after* the delete, so the delete "missed". Three defences, in increasing strength: (1) a **TTL** bounds how long the stale value lives (the cheap default); (2) a **delayed second delete** ("delete again 1 s after the write") catches most slow readers; (3) **leases or versioned sets**: the cache hands the reader a token on a miss, a delete invalidates the token, and a `set` carrying an invalidated token is refused. Facebook's memcache paper describes that last design, which also stops stampedes, because only the token holder loads the value. Pick the defence by how long a stale value may live: if "never", don't use cache-aside for that data.

**Eviction**: when the cache is full, something must go. **LRU** (least recently used) is the default and works well with temporal locality. **LFU** (least frequently used) protects long-term popular items from one-off scans. **TTL** expires entries by age, which bounds staleness.

**The failure modes** (these are what senior engineers ask about):

| Failure | What happens | Defence |
|---|---|---|
| **Cache stampede (thundering herd)** | A hot key expires; thousands of requests miss at once and all hit the DB | Request coalescing (one loader, the rest wait), locks, refreshing early with a random margin |
| **Cache penetration** | Requests for keys that *don't exist* always miss and hit the DB (often an attack) | Cache negative results briefly; put a Bloom filter (§9.1) in front |
| **Cache avalanche** | Many keys expire at the same moment, or the cache cluster restarts empty | Add random jitter to TTLs; warm the cache; keep the cache replicated |
| **Hot key** | One key (a celebrity's profile) overloads one cache node | Replicate the hot key to several nodes; add a small in-process cache in front |
| **Inconsistency** | The cache and the DB disagree | TTLs, delete-on-write, or invalidation driven by change data capture (Part 3 §3.5) |

**Decision guide: should you add a cache here?**

1. **Is the data read much more than it's written?** Roughly 10:1 or more. If it changes on almost every read, a cache mostly adds invalidation work.
2. **Is the traffic skewed?** Without skew (Fig 13), a cache must hold most of the data to help, and then it's just a second database.
3. **Can the reader tolerate staleness, and for how long?** That number becomes your TTL. "Never stale" usually means "don't cache this", or cache with write-through and accept slower writes.
4. **Is the database actually the bottleneck?** Check first. Sometimes an index (§6.5) or a better query (§6.6) removes the need for a cache entirely.
5. **What happens when the cache is empty** (a restart, a deploy, an avalanche)? If the database can't survive full traffic without the cache, the cache has become critical infrastructure. It then needs replication, warming and stampede protection, and its own on-call attention.

**Current note (2026):** Redis changed its licence in 2024, then returned to open source under AGPLv3 with Redis 8 in 2025. Meanwhile **Valkey**, a Linux Foundation fork of Redis 7.2, is widely offered by cloud providers. They're protocol-compatible for typical cache use, so the design advice here applies to both.

### 5.4 CDNs

**The problem.** The speed of light makes far-away users slow (Fig 1), and serving the same video bytes to millions of people from one origin is expensive.

**How it works.** A **content delivery network** is a global fleet of caching servers (points of presence, or PoPs) near users.

- **Pull CDN**: on a miss, the edge fetches from your origin and caches according to `Cache-Control` headers. Easy; the first user in each region pays the miss.
- **Push CDN**: you upload content ahead of time. Good for big, predictable files.
- **Cache key design** matters: decide which query parameters, headers and cookies make two requests "the same". Version static files by content hash (`app.3f9a1c.js`) so they can be cached "forever" and replaced instantly.
- **Edge compute** (Workers, Lambda@Edge, Wasm at the edge) runs small pieces of code at the PoP: auth checks, A/B routing, personalisation.
- An **origin shield** is a middle cache layer that collapses misses from many PoPs into one origin request.

### 5.5 Stateless services and where state goes

**The problem.** If server A holds a user's session in memory, every request from that user must go to A. Scaling, deploys and crashes all break it.

**How it works.** Make application servers **stateless**: any server can handle any request. Push the state out to a shared store (database, Redis), or into the request itself (a signed token such as a JWT). Then you can add, remove or replace servers freely, which is the foundation of autoscaling (Part 3 §5.8).

**Two ways to keep a logged-in user's session:**

| | **Server-side session** | **Self-contained token (JWT)** |
|---|---|---|
| What the client holds | A random session ID in a cookie | A signed token containing the user ID, roles and expiry |
| Each request | Look up the ID in a shared store (Redis, DB) | Verify the signature locally; no lookup |
| Logout / revoke | **Instant**: delete the session | **Hard**: the token stays valid until it expires, unless you add a deny-list (which is a lookup again) |
| Cost at scale | One fast store lookup per request | CPU for signature checks; no shared store on the hot path |
| Size | Tiny cookie | Hundreds of bytes to a few KB on every request |
| Best for | Web apps with a browser session; anything needing instant revocation | Service-to-service calls; APIs spanning many services; short-lived access tokens |

The common modern answer combines them: a **short-lived access token** (a JWT valid for about 5–15 minutes, verified locally by every service) plus a **long-lived refresh token** kept server-side and revocable. Revoking the refresh token cuts a user off within one access-token lifetime. The token's expiry *is* your revocation delay, so choose it deliberately. Store browser tokens in `HttpOnly`, `Secure`, `SameSite` cookies rather than in JavaScript-readable storage, which cross-site scripting can steal (Part 3 §7.8).

**The general principle:** *push state to the edges of the system and keep the middle stateless.* The state that remains (databases, queues, caches) is where all the hard problems of Part 2 live.

### 5.6 Scaling up vs scaling out

**The problem.** Load is growing. You can buy a bigger machine, or more machines. Each choice has a ceiling and a price.

| | **Vertical scaling (scale up)** | **Horizontal scaling (scale out)** |
|---|---|---|
| How | Bigger machine: more cores, RAM, faster disks | More machines behind a load balancer, or data split across nodes |
| Code changes | None | Services must be stateless; data must be partitioned or replicated |
| Ceiling | The largest machine you can buy or rent | Very high, if the work divides cleanly (Part 3 §4.4) |
| Failure | Still one machine: a single point of failure | Survives losing nodes, if designed to |
| Cost curve | Rises steeply at the top end | Roughly linear, plus coordination overhead |
| Complexity | Low | High for stateful parts (Part 2 is all about this) |

**How to decide.** *Stateless tiers* (web and app servers) should scale out from day one. It's cheap, and it also gives you redundancy. *Stateful tiers* (databases) should usually **scale up first**: modern servers with hundreds of cores and terabytes of RAM take a single database a very long way. Add read replicas for read load. Shard only when a number forces you to, because sharding is close to a one-way door (§2.5). The mistake to avoid is distributing data early "for scale" and paying the complexity cost for years before the scale arrives.

---

## 6. Storage engines: how a database really stores data

This is the part most engineers skip, and it explains most database behaviour. There are two dominant families: **log-structured (LSM-trees)** and **page-oriented (B-trees)**.

### 6.1 Start with the simplest database: a log

**The problem.** We want to store key-value pairs durably and find them again quickly.

**The naive approach.** Append every write to the end of a file: `key,value\n`. Writing is as fast as the disk allows, because it is purely sequential. But reading means scanning the whole file from the end: O(n). Useless at scale.

**The fix: an index.** Keep an in-memory hash map from each key to its byte offset in the file. Reads become one seek. This is exactly how Bitcask (Riak's engine) works. Two limits remain:

1. All keys must fit in RAM.
2. Range queries ("all keys between `user:100` and `user:200`") are impossible, because a hash map has no order.

The log also grows forever, so you periodically **compact** it: rewrite it keeping only the latest value for each key, then delete the old segments. Deletes are written as special **tombstone** records.

### 6.2 SSTables and LSM-trees

**The problem.** We want the write speed of a log *plus* sorted order (for range scans) *plus* keys that don't all fit in RAM.

**How it works.**

1. Writes go to an in-memory **sorted** structure called the **memtable** (a balanced tree or skip list), *and* are appended to a **write-ahead log (WAL)** on disk so a crash can't lose them.
2. When the memtable reaches a size limit (tens to hundreds of MB), it is written out as an immutable, sorted file: a **Sorted String Table (SSTable)**. This is one big sequential write.
3. A **read** checks the memtable, then SSTables from newest to oldest. Each SSTable has a sparse index (one key per block) and a **Bloom filter** (§9.1) that answers "definitely not here" without touching the disk.
4. In the background, **compaction** merges SSTables (like the merge step of merge sort), dropping overwritten values and tombstones.

```mermaid
flowchart LR
    accTitle: LSM-tree write and read path
    accDescr: Writes go to WAL and memtable, flush to SSTables, which compaction merges into deeper levels. Reads check memtable then SSTables using Bloom filters.
    W(["Write"]) --> WAL[("WAL<br/>append-only, for crashes")]
    W --> MT["Memtable<br/>sorted, in RAM"]
    MT -->|"flush when full"| L0[("L0 SSTables<br/>recent, may overlap")]
    L0 -->|"compaction<br/>merge-sort"| L1[("L1<br/>10x bigger")]
    L1 -->|"compaction"| L2[("L2<br/>10x bigger")]
    R(["Read"]) --> MT
    R -.->|"Bloom filter says maybe"| L0
    R -.-> L1
    R -.-> L2
    class W,R primary;
    class MT,WAL intermediate;
    class L0,L1,L2 target;
    classDef primary fill:#EFF6FF,stroke:#2563EB,stroke-width:1.5px,color:#0F172A;
    classDef intermediate fill:#FAF5FF,stroke:#7C3AED,stroke-width:1.5px,color:#0F172A;
    classDef target fill:#F0FDF4,stroke:#059669,stroke-width:2px,color:#0F172A;
```

**Two compaction strategies:**

- **Size-tiered** (Cassandra's classic default): merge SSTables of similar size. Cheap on writes, but a key can live in many files, and compaction temporarily needs a lot of spare disk.
- **Leveled** (RocksDB, LevelDB): each level is about $T$ times bigger than the previous one ($T$ is the size ratio, often 10), and files inside a level don't overlap. A read touches at most one file per level. The cost is more rewriting.

**How many levels?** With a size ratio $T = 10$, a first level of 256 MB and 1 TB of data:

$$
L \approx \log_{T} \frac{\text{data size}}{\text{level-1 size}} = \log_{10} \frac{10^{12}}{2.56 \times 10^{8}} \approx 3.6 \ \Rightarrow \ 4 \ \text{levels}
$$

*The number of levels is the base-T logarithm of how many times bigger the data is than the first level.* Each byte gets rewritten roughly up to $T$ times per level as it sinks. So with leveled compaction, the total rewriting (**write amplification**) is commonly in the tens.

LSM-trees power RocksDB, Cassandra, ScyllaDB, HBase, Bigtable, LevelDB, and the storage layers of CockroachDB, TiDB and many time-series databases.

### 6.3 B-trees

**The problem.** We want predictable, fast reads and in-place updates, and we can afford some write cost.

**How it works.** A B-tree breaks the database into fixed-size **pages** (often 4–16 KB). Each page holds sorted keys and pointers to child pages. A lookup starts at the root and follows one pointer per level down to a leaf. In a **B+ tree** (what databases actually use), all values live in the leaves, and leaves are linked for fast range scans.

```mermaid
flowchart TD
    accTitle: B+ tree lookup
    accDescr: A root page points to internal pages, which point to linked leaf pages holding the rows.
    root["Root page<br/>keys: 100 | 200"]
    i1["Internal<br/>keys: 30 | 60"]
    i2["Internal<br/>keys: 130 | 160"]
    i3["Internal<br/>keys: 230 | 260"]
    l1["Leaf 1–29"]
    l2["Leaf 30–59"]
    l3["Leaf 130–159"]
    root --> i1
    root --> i2
    root --> i3
    i1 --> l1
    i1 --> l2
    i2 --> l3
    l1 -.->|"next leaf"| l2
```

**Worked example: tree height.** A 16 KB page holding entries of about 32 bytes (key + child pointer) has a **fanout** $f \approx 16{,}384 / 32 = 512$. Take $f = 500$ for round numbers. For a billion rows:

$$
h = \lceil \log_{f} N \rceil = \lceil \log_{500} 10^{9} \rceil = \lceil 3.33 \rceil = 4
$$

*The height is the base-f logarithm of the row count, rounded up.* Three levels hold $500^3 = 125$ million keys, and four hold 62.5 billion. So **any of a billion rows is reachable in 4 page reads.** The top two or three levels are tiny and stay in RAM, so a lookup usually costs **one or two disk reads**. That predictability is why B-trees dominate OLTP databases (PostgreSQL, MySQL InnoDB, SQL Server, Oracle, SQLite).

**Writes and crashes.** Updating a page in place is dangerous: a crash mid-write can leave a half-written page, and a page split touches several pages. So B-tree databases first write every change to a **write-ahead log (WAL, also called a redo log)** and fsync it. After a crash, they replay the WAL. Concurrency inside the tree uses lightweight page locks called *latches*.

### 6.4 B-tree vs LSM: amplification is the real trade-off

Every storage engine pays in three currencies (sometimes called the **RUM conjecture**: you can optimise two of **R**ead, **U**pdate and **M**emory/space overhead, not all three):

- **Read amplification**: disk reads per logical read.
- **Write amplification**: bytes written to disk per byte the user wrote.
- **Space amplification**: disk used per byte of live data.

| | **B-tree** | **LSM-tree** |
|---|---|---|
| Write pattern | Random in-place page writes (plus the WAL) | Sequential appends and merges |
| Write throughput | Good | Usually higher, especially on HDDs and for heavy ingest |
| Read latency | Low and predictable (one path) | Can check several levels; Bloom filters help; range scans merge levels |
| Space | Some fragmentation (half-empty pages after splits) | Compresses well; temporary bloat before compaction |
| Write amplification | Whole page rewritten for a small change | Rewrites during compaction (often 10–30× when leveled) |
| Background work | Little | Compaction can steal disk bandwidth and cause latency spikes |
| Best for | Read-heavy OLTP, strong transactions | Write-heavy ingest: logs, metrics, messaging, time series |

There is no winner. Measure with *your* workload.

### 6.5 Indexes

**The problem.** Without an index, a query must scan every row. An index makes reads fast but costs extra writes and storage.

Key ideas:

- **Primary vs secondary index.** The primary index is on the primary key. A secondary index is on another column (such as `email`).
- **Clustered index**: the table rows are *stored inside* the index's leaves in key order (InnoDB's primary key). Other indexes then point to the primary key.
- **Covering index**: the index contains every column the query needs, so the table itself is never touched.
- **Composite index** on `(country, city, age)` follows the **leftmost prefix rule**: it helps queries filtering on `country`, or `country + city`, but not on `city` alone. Order the columns by how you query.
- **Every index slows writes.** Each insert must update every index on the table. Index for your actual query patterns, not "just in case".
- Specialised indexes: **inverted indexes** for full-text search (§7.7), **GiST/R-trees** for geometry, **HNSW** graphs for vector similarity (Part 3 §9).

### 6.6 Connection pooling and reading query plans

These two practical skills cause many real production problems, and interviewers like to ask about them.

**Connection pooling: the problem.** Opening a database connection is expensive: a TCP handshake, often TLS, authentication, and on the server side a new backend. PostgreSQL starts a whole **OS process per connection**, using several MB of memory each. If every request opens its own connection, you pay several round trips per request, and thousands of connections can exhaust the database's memory.

**How it works.** A **pool** keeps a fixed set of connections open and lends one to each request, which returns it when done. How many do you need? Little's Law (Part 3 §4.1) gives the number that are busy at once:

$$
\text{connections busy} = \text{query rate} \times \text{time per query}
$$

*On average, the number of connections in use equals queries per second times how long each query holds its connection.* **Example:** 2,000 queries/s × 5 ms = **10** busy connections. A pool of about 20 gives headroom for bursts.

Two traps:

1. **Bigger pools aren't faster.** The database has a fixed number of CPU cores and disks. Beyond a point, extra connections just compete for locks and CPU, and every query slows down. Size the pool from the formula, not "as big as possible".
2. **Many app instances multiply.** 50 app instances × a pool of 20 = 1,000 database connections, even if each one is mostly idle. That's why there are external poolers (**PgBouncer**, RDS Proxy). In *transaction mode* they hand a real server connection to a client only for the length of one transaction, so thousands of client connections share a few dozen server connections. Serverless functions, which can scale to thousands of instances in seconds, almost always need one.

**Query plans: the problem.** A query that ran in 2 ms in testing takes 4 seconds in production. Why? The database chose a bad way to run it, or it has no good way.

**How it works.** SQL says *what* you want, not *how* to get it. The **query planner** considers possible plans (which index to use, which join order and join method) and estimates the cost of each, using **statistics** about the data (row counts, distinct values, value distributions). `EXPLAIN` shows the chosen plan. `EXPLAIN ANALYZE` actually runs the query and shows real row counts and times next to the estimates.

| Plan node | What it does | When it's a warning sign |
|---|---|---|
| **Seq Scan** | Reads the whole table | On a big table with a selective `WHERE`: probably a missing index |
| **Index Scan** | Walks the index, then fetches matching rows | Fine for few rows. Slow if it fetches a large fraction of the table (random I/O). |
| **Index Only Scan** | Answers from the index alone (a covering index, §6.5) | Usually the best case |
| **Bitmap Heap Scan** | Collects matches from one or more indexes, then reads pages in order | Normal for medium-selectivity filters |
| **Nested Loop** | For each outer row, look up matching inner rows | Fine when the outer side is small. A disaster when the estimates were wrong and it's huge. |
| **Hash Join** | Builds a hash table from one side, probes it with the other | Normal for big joins; watch its memory |
| **Sort** | Sorts rows | "external merge" or "Disk" in the output means it spilled to disk: add an index matching the `ORDER BY`, or more memory |

**The three things to check first:**

1. **Estimated rows vs actual rows.** If the planner expected 10 rows and got 1,000,000, it chose a plan for the wrong situation. Usually the statistics are stale (run `ANALYZE`), or the columns are correlated in a way the planner can't see.
2. **A sequential scan where you expected an index.** The index may be missing, or the query may prevent its use: a function on the column (`WHERE lower(email) = …` needs an index on `lower(email)`), a type mismatch, or a leading wildcard (`LIKE '%foo'`).
3. **Where the time goes.** `EXPLAIN ANALYZE` reports time per node. Fix the most expensive node first.

**The N+1 query problem** is the most common slow pattern in application code, and it doesn't show in any single query plan. An ORM loads 100 posts with one query, then lazily loads each post's author with *another* query: 101 round trips. At 0.5 ms each inside a datacenter, that's about 50 ms of pure network waiting. One join, or one batched `WHERE author_id IN (…)` query, does it in 1–2 round trips. The same problem appears in GraphQL resolvers (Part 3 §2.1).

### 6.7 Choosing primary keys: a one-way door

**The problem.** The primary key looks like a detail, but it's very hard to change later. It affects index performance, sharding, security and whether two systems can generate IDs independently.

| Key type | How it works | Strengths | Weaknesses |
|---|---|---|---|
| **Auto-increment integer** | The database hands out 1, 2, 3… | Small (8 bytes), sequential, fast B-tree inserts | Needs one central counter, so it doesn't work across shards; it leaks business volume (order #1,000,042 tells competitors your sales); IDs are guessable |
| **UUIDv4** (random, 128-bit) | Generated anywhere, no coordination | Unique without coordination; unguessable | **Random inserts scatter across the whole B-tree**: every insert touches a random page, which bloats the cache and slows writes as the table grows. 16 bytes per key in every index. |
| **UUIDv7** (RFC 9562, 2024) | A 48-bit millisecond timestamp first, then random bits | Generated anywhere, *and* roughly time-ordered, so inserts append near the end of the B-tree like auto-increment | Reveals creation time; 16 bytes |
| **Snowflake-style 64-bit** | Timestamp + machine ID + per-machine sequence | Time-ordered, compact (8 bytes), very fast | Needs machine IDs assigned; depends on clocks not going backwards (Part 3 §11.2 shows the bit layout) |

**The reasoning.** B-trees love keys that arrive in order (§6.3): new rows go into the right-most page, which stays in memory. Random keys spread writes over every page. **Default choice in 2026:** UUIDv7 (or Snowflake-style IDs) for most new tables. PostgreSQL 18 added a built-in `uuidv7()` function. Use a separate random or opaque public identifier if you don't want to reveal creation time. One caution for sharded systems: a time-ordered key used as a **range** shard key sends all new writes to the newest shard (a hot spot, Part 2 §4.1). Hash the key for placement, or shard by something else (such as the tenant).

---

## 7. Data models and choosing a database

**The problem.** The shape of your data and your access patterns should pick the database. Popularity should not.

### 7.1 Relational (SQL)

Data lives in tables of rows and columns with a fixed **schema**. Relations are expressed with foreign keys and combined with **joins**. **Normalisation** stores each fact once, which avoids update anomalies but needs joins to reassemble data. Relational databases give you powerful ad-hoc queries (SQL), strong transactions (§8) and decades of tooling. **PostgreSQL** is the default choice for new systems in 2026 for good reason: with extensions it also covers JSON documents (`jsonb`), full-text search, geospatial data (PostGIS) and vectors (`pgvector`). (Versions: PostgreSQL 18, released in September 2025, added asynchronous I/O and native `uuidv7()`. **PostgreSQL 19** reached release candidate 1 on 15 October 2026, with general availability expected within weeks. Its headline features include SQL/PGQ property-graph queries in standard SQL, a `WAIT FOR LSN` command that makes read-your-writes on replicas easy (Part 2 §3.2), parallel autovacuum and a non-blocking `REPACK` command.)

### 7.2 Document

Each record is a self-contained JSON-like **document** (MongoDB, Couchbase, Firestore). A document maps naturally onto objects in code and gives **locality**: one read fetches the whole aggregate (a user with their addresses). Weaknesses: many-to-many relationships and joins are awkward, and duplicated (denormalised) data must be kept in sync by your code. Choose it when data is naturally tree-shaped and accessed as a whole.

### 7.3 Wide-column

Rows are identified by a **partition key**. Inside a partition, columns are sorted by a **clustering key** (Cassandra, ScyllaDB, HBase, Bigtable). Built on LSM-trees, they handle massive write volumes and scale horizontally. The trade-off is that **you design tables around queries**: one table per access pattern, no joins, limited secondary indexes. They are great for time-ordered data per entity (messages per chat, events per device).

### 7.4 Key-value

The simplest model: `get(key)`, `put(key, value)`. In-memory stores (Redis, Memcached) give microsecond latency for caches, sessions, counters, leaderboards and rate limiters. Durable distributed ones (DynamoDB, etcd, FoundationDB) give predictable latency at huge scale. DynamoDB-style systems are really key-value plus a sort key, close to wide-column.

### 7.5 Graph

Data is **nodes and edges**, both with properties (Neo4j, Amazon Neptune; query languages Cypher, Gremlin, and the ISO standard GQL). They suit queries that follow relationships many hops deep: "friends of friends who like X", fraud rings, knowledge graphs. A relational database needs one self-join per hop, which gets slow and awkward fast.

### 7.6 Time-series

Data is append-mostly measurements keyed by time (metrics, IoT sensors, prices): TimescaleDB, InfluxDB, Prometheus, ClickHouse. They use columnar compression (deltas between consecutive timestamps compress extremely well), time-based partitioning, cheap deletion of whole old partitions (retention), and **downsampling** (keep per-second data for a day, per-minute data for a year).

### 7.7 Search engines and the inverted index

**The problem.** "Find documents containing *distributed* and *consensus*" by scanning every document is hopeless at scale.

**How it works.** An **inverted index** maps each term to its **posting list**: the IDs (and positions) of the documents containing it, like the index at the back of a book. A query intersects posting lists, then **ranks** the matches. Text goes through **analysis** first: tokenising, lowercasing, stemming ("running" → "run").

**Ranking with BM25**, the standard keyword-relevance formula:

```math
\text{score}(D, Q) = \sum_{q \in Q} \text{IDF}(q) \cdot \frac{f(q, D) \cdot (k_1 + 1)}{f(q, D) + k_1 \left(1 - b + b \cdot \frac{\lvert D \rvert}{\text{avgdl}}\right)}
```

*For each query word, multiply how rare the word is across all documents (IDF) by a saturating count of how often it appears in this document, adjusted for document length; then add over the query words.*

The three ideas inside it:

1. **Rare words matter more.** IDF is large for words in few documents ("Raft") and near zero for common ones ("the").
2. **Repetition helps, but with diminishing returns.** $f(q, D)$ is how often the word appears in document $D$. The $k_1$ term (typically 1.2–2.0) makes the 10th occurrence add far less than the 2nd.
3. **Long documents are penalised a little.** $\lvert D \rvert$ is the document's length and avgdl the average length; $b$ (typically 0.75) controls how much. Otherwise long documents would win just by containing more words.

Elasticsearch and OpenSearch (both built on Lucene) are the standard engines. They are usually *secondary* stores fed from the main database, not the source of truth. In AI systems, BM25 is paired with vector search, because each finds what the other misses (Part 3 §9.4).

### 7.8 Vector databases

They store **embeddings**, vectors that capture meaning, and answer "find the nearest vectors" using approximate nearest neighbour (ANN) indexes such as HNSW. This is the retrieval half of AI systems, covered properly in [Part 3 §9](System%20Design%203%20-%20Building%20Real%20Systems%20in%202026.md). In practice: pgvector inside Postgres, vector search inside existing engines (Elasticsearch, Redis), or dedicated stores (Pinecone, Qdrant, Weaviate, Milvus).

### 7.9 Object, block and file storage

| Kind | Interface | Examples | Use for |
|---|---|---|---|
| **Block** | Raw fixed-size blocks; a filesystem or DB sits on top | AWS EBS, local NVMe | Database disks, VM disks |
| **File** | Hierarchical paths, POSIX operations | NFS, EFS | Shared files between servers |
| **Object** | `PUT`/`GET` whole objects by key over HTTP; flat namespace; effectively unlimited | Amazon S3, GCS, Azure Blob, MinIO | Images, video, backups, logs, data lakes (Part 3 §8) |

Object storage is cheap, extremely durable (S3 is designed for 11 nines of durability) and massively scalable, but each request has high latency (tens of ms) and objects are replaced whole, not edited in place. The standard pattern: **put the bytes in object storage, put the metadata in a database, put a CDN in front.**

### 7.10 Choosing: a decision table

| If your dominant need is… | Start with |
|---|---|
| General-purpose, transactions, ad-hoc queries | **PostgreSQL** (or MySQL) |
| Massive write throughput, known query patterns, multi-region | Wide-column (Cassandra/ScyllaDB) or DynamoDB |
| Microsecond reads, ephemeral data | Redis / Memcached |
| Tree-shaped records read and written as a whole | Document store (or Postgres `jsonb`) |
| Deep relationship traversal | Graph database |
| Full-text relevance search | Elasticsearch / OpenSearch |
| Metrics and events over time | Time-series DB / ClickHouse |
| Analytics over billions of rows | Columnar warehouse or lakehouse (Part 3 §8) |
| Global SQL with strong consistency | Distributed SQL (Spanner, CockroachDB, YugabyteDB; Part 2) |
| Semantic similarity | Vector index (pgvector first; dedicated if it outgrows it) |

Big systems use several (**polyglot persistence**). The hard part then becomes keeping them in sync, which is what change data capture solves (Part 3 §3.5).

### 7.11 SQL vs NoSQL: thinking the decision through

**The problem.** "SQL or NoSQL?" is one of the most common design questions, and one of the most commonly answered by habit. "NoSQL scales, SQL doesn't" was a reasonable rule of thumb in 2010. In 2026 it's mostly wrong, and believing it leads to expensive designs.

**First, what the labels really mean.** "NoSQL" isn't one thing. It's four different families (key-value, document, wide-column, graph) that share only "not a relational table". The real differences that matter are these:

| Dimension | Relational (SQL) | Typical NoSQL (key-value, document, wide-column) |
|---|---|---|
| **Data model** | Normalised tables + joins; any question can be asked later | Shaped around known access patterns; questions you didn't plan for are hard |
| **Schema** | Enforced by the database; migrations needed (Part 3 §6.3) | Flexible per record; *the schema still exists*, but in your code, enforced by nobody |
| **Transactions** | Multi-row, multi-table ACID by default | Often single-record or single-partition only; multi-item transactions are limited or slower |
| **Query flexibility** | Ad-hoc SQL, joins, aggregations | Lookups by key or by pre-designed index; scans are expensive |
| **Scaling writes** | One primary, scaled up first; sharding is manual or needs distributed SQL | Built-in partitioning; scales writes horizontally |
| **Consistency** | Strong on the primary | Often tunable; eventual by default in leaderless systems (Part 2 §3.4) |
| **Operations** | Mature tooling; vertical limits | Managed services can be nearly zero-ops (DynamoDB); self-run clusters (Cassandra) need expertise |

**Three myths worth unlearning:**

1. **"SQL doesn't scale."** A single PostgreSQL or MySQL primary on modern hardware handles thousands to tens of thousands of writes per second and far more reads with replicas. Very few products outgrow that. When they do, **distributed SQL** (Spanner, CockroachDB, YugabyteDB, TiDB) scales horizontally *and keeps SQL and transactions* (Part 2 §7, §11).
2. **"NoSQL is schemaless, so it's more flexible."** The schema moves from the database into your application code, where nothing enforces it. Old records in old shapes accumulate, and every reader must handle every historical shape. That's flexibility for the writer and a cost for every reader.
3. **"NoSQL is faster."** A key lookup is fast in any database with an index. NoSQL systems are *predictably* fast at the access patterns they were designed for, at very large scale. They're often slower, or unable to answer, for anything else.

**Decision flow:**

```mermaid
flowchart TD
    accTitle: SQL vs NoSQL decision flow
    accDescr: Questions about transactions, query flexibility, write scale, data shape and team skills lead to relational, distributed SQL, or a specific NoSQL family.
    S(["New data store needed"]) --> Q1{"Need multi-row<br/>transactions or joins?"}
    Q1 -->|"yes"| Q2{"Fits one primary<br/>for 2–3 years?"}
    Q2 -->|"yes"| PG(["Relational<br/>PostgreSQL / MySQL"])
    Q2 -->|"no"| DSQL(["Distributed SQL<br/>Spanner, CockroachDB, YugabyteDB"])
    Q1 -->|"no"| Q3{"Access patterns<br/>known and few?"}
    Q3 -->|"no, ad-hoc queries"| PG
    Q3 -->|"yes"| Q4{"What shape?"}
    Q4 -->|"lookups by key,<br/>huge scale"| KV(["Key-value / DynamoDB"])
    Q4 -->|"time-ordered rows<br/>per entity, heavy writes"| WC(["Wide-column<br/>Cassandra, ScyllaDB"])
    Q4 -->|"whole nested records"| DOC(["Document store<br/>or Postgres jsonb"])
    Q4 -->|"many-hop relationships"| GR(["Graph database"])
    class S primary;
    class Q1,Q2,Q3,Q4 intermediate;
    class PG,DSQL,KV,WC,DOC,GR target;
    classDef primary fill:#EFF6FF,stroke:#2563EB,stroke-width:1.5px,color:#0F172A;
    classDef intermediate fill:#FAF5FF,stroke:#7C3AED,stroke-width:1.5px,color:#0F172A;
    classDef target fill:#F0FDF4,stroke:#059669,stroke-width:2px,color:#0F172A;
```

**Worked decisions** (cover the answer and try each one first):

| Situation | Choice | The deciding reason |
|---|---|---|
| Orders, payments, inventory for an online shop | **PostgreSQL** | Multi-row transactions and invariants ("stock never negative") need ACID; load fits one primary for years |
| Chat messages for 500M users | **Wide-column** (partition by conversation, cluster by time) | Enormous append-heavy writes; the access pattern is fixed: "latest messages in conversation X" (a full chat design is in Part 3 §11.4) |
| User sessions and rate-limit counters | **Key-value in memory** (Redis/Valkey) | Microsecond lookups; losing some data is acceptable; TTLs built in |
| Product catalogue with varied attributes per category | **PostgreSQL with `jsonb`** for the variable attributes | You get flexible attributes *and* joins, transactions and SQL. A separate document database would add a second system for little gain. |
| Global bank ledger across three continents | **Distributed SQL** | Needs both transactions and multi-region survival; the latency cost of consensus is accepted (Part 2 §5.4) |
| Fraud detection over account–device–card links | **Graph** (or graph queries in SQL) | The question is "how are these connected, 4 hops out?", which is a graph traversal |

**The deciding questions, in order:** (1) Do I need transactions across multiple items? (2) Do I know all my query patterns in advance, and are they few? (3) Will writes outgrow one primary within the planning horizon? (4) What does my team already run well? If the first answer is yes, start relational. If the second answer is yes *and* the third is yes, a NoSQL family that matches the shape is a strong choice.

---

## 8. Transactions and isolation

### 8.1 What ACID actually means

**The problem.** Many things happen at once, and things fail halfway. Without guarantees, money disappears and inventory goes negative.

A **transaction** groups several reads and writes into one unit. ACID names four guarantees, and each word is more specific than it sounds:

- **Atomicity**: all or nothing. If anything fails, every write in the transaction is rolled back. (This is about *aborting*, not about concurrency.)
- **Consistency**: the application's invariants hold, such as "balances never go negative". This is mostly the *application's* job, helped by constraints. It is **not** the "C" in CAP (Part 2).
- **Isolation**: concurrent transactions don't interfere with each other. Ideally each behaves as if it ran alone. This is the hard one, covered below.
- **Durability**: once committed, data survives crashes (WAL + fsync, §3.3, and replication).

### 8.2 The anomalies: what can go wrong

The isolation levels below are defined by which of these they prevent. Learn the anomalies and the levels make sense.

| Anomaly | What happens | Example |
|---|---|---|
| **Dirty read** | You read another transaction's *uncommitted* write, which might be rolled back | You see a balance that never really existed |
| **Dirty write** | You overwrite another transaction's uncommitted write | Two half-finished updates get mixed |
| **Read skew (non-repeatable read)** | You read the same data twice and get different answers because someone committed in between | A backup or report sees money "in flight" between two accounts and adds up wrong |
| **Lost update** | Two transactions read-modify-write the same value; one update silently disappears | Two clicks on "like" both read 10 and both write 11 |
| **Write skew** | Two transactions read the *same* data, each decides it's safe, then they write *different* rows, and together they break an invariant | Two on-call doctors both see "2 on call", both go off call, and now nobody is on call |
| **Phantom** | A query's *set of matching rows* changes because another transaction inserted or deleted rows | Two bookings check "is this room free 2–3 pm?" and both insert a booking |

**The lost update, step by step:**

```mermaid
sequenceDiagram
    participant T1 as Transaction 1
    participant DB as likes = 10
    participant T2 as Transaction 2
    T1->>DB: read likes (10)
    T2->>DB: read likes (10)
    T1->>DB: write likes = 11
    T2->>DB: write likes = 11
    Note over DB: Final value 11, should be 12. One update was lost.
```

**Write skew is the subtle one.** Neither transaction overwrote the other's data, so row-level conflict checks miss it. The bug is in the *decision* each made from data that changed underneath it.

```mermaid
sequenceDiagram
    participant A as Dr Alice (T1)
    participant DB as on_call table<br/>Alice ✓, Bob ✓
    participant B as Dr Bob (T2)
    A->>DB: SELECT count(*) WHERE on_call → 2
    B->>DB: SELECT count(*) WHERE on_call → 2
    Note over A,B: Both snapshots say "2 on call, safe for me to leave"
    A->>DB: UPDATE Alice SET on_call = false
    B->>DB: UPDATE Bob SET on_call = false
    A->>DB: COMMIT ✓
    B->>DB: COMMIT ✓ (different row, so no write conflict)
    Note over DB: 0 doctors on call. The rule "at least 1" is broken.
```

Compare it with the lost update above. There, both transactions wrote the **same** row, so a database that checks write conflicts (snapshot isolation does) catches it. Here they write **different** rows, so only a check on what each transaction *read* (serializable isolation) or an explicit lock on the rows read (`SELECT … FOR UPDATE`) can catch it.

### 8.3 Isolation levels

| Level | Prevents | Still allows | Notes |
|---|---|---|---|
| Read uncommitted | Dirty writes | Everything else | Rarely used |
| **Read committed** | Dirty reads and writes | Read skew, lost updates, write skew, phantoms | **PostgreSQL's default**, and Oracle's and SQL Server's |
| **Snapshot isolation** (Postgres calls it *repeatable read*) | + read skew, + most lost updates | **Write skew**, some phantoms | Each transaction reads a consistent snapshot |
| Repeatable read (MySQL InnoDB default) | Read skew for plain reads | Write skew, lost updates in some patterns | Names differ between vendors, so check the docs |
| **Serializable** | Everything: the result equals *some* one-at-a-time order | Nothing | Costs throughput, and aborts that clients must retry |

> **Vendor names lie.** The SQL standard defined isolation levels by three anomalies before snapshot isolation existed. That's why "repeatable read" means different things in PostgreSQL and MySQL, and why Oracle's "serializable" has historically been snapshot isolation. Always test the anomaly you care about.

### 8.4 How databases implement isolation

1. **Two-phase locking (2PL)**: readers take shared locks and writers take exclusive locks, all held until commit (the "growing then shrinking" phases). It is truly serializable, but readers and writers block each other and deadlocks happen (the database detects them and aborts one transaction). To stop phantoms it also locks *ranges* of the index (predicate or next-key locks).
2. **MVCC (multi-version concurrency control)**: every write creates a new *version* of the row tagged with its transaction ID. Each transaction reads the versions that were committed when its snapshot was taken. **Readers never block writers, and writers never block readers.** Old versions are garbage-collected later (PostgreSQL's VACUUM). MVCC is how snapshot isolation is built.

   ```mermaid
   flowchart LR
       accTitle: MVCC version chain
       accDescr: One logical row has three versions created by transactions 100, 205 and 310. A snapshot taken at 250 sees the 205 version; a snapshot taken at 400 sees the 310 version.
       V1["balance = 50<br/>created by tx 100<br/>replaced by tx 205"] --> V2["balance = 80<br/>created by tx 205<br/>replaced by tx 310"] --> V3["balance = 30<br/>created by tx 310<br/>current"]
       S1(["Snapshot at tx 250<br/>(a long report)"]) -.->|"sees"| V2
       S2(["Snapshot at tx 400<br/>(a new query)"]) -.->|"sees"| V3
       GC["VACUUM removes V1<br/>once no snapshot<br/>older than 205 exists"] -.-> V1
       class V1 warning;
       class V2,V3 target;
       class S1,S2 primary;
       class GC intermediate;
       classDef primary fill:#EFF6FF,stroke:#2563EB,stroke-width:1.5px,color:#0F172A;
       classDef intermediate fill:#FAF5FF,stroke:#7C3AED,stroke-width:1.5px,color:#0F172A;
       classDef target fill:#F0FDF4,stroke:#059669,stroke-width:2px,color:#0F172A;
       classDef warning fill:#FFFBEB,stroke:#D97706,stroke-width:1.5px,color:#92400E;
   ```

   Each version records which transaction created it and which replaced it. A reader simply picks the newest version that was committed before its snapshot, with no locks. The cost shows up in the last box: **a long-running transaction pins old versions**, so they can't be cleaned up and tables bloat. That's why Drill 7 below warns against long reports on the primary.
3. **Serializable snapshot isolation (SSI)**: MVCC plus tracking of read-write dependencies between concurrent transactions. When a dangerous pattern (a potential cycle) appears, one transaction is aborted at commit time. It is serializable with no read locks. It is *optimistic*: cheap when conflicts are rare. PostgreSQL's `SERIALIZABLE` level uses it.

### 8.5 Fixing lost updates and write skew in practice

- **Atomic operations**: `UPDATE posts SET likes = likes + 1 WHERE id = 7`. The database does the read-modify-write as one step.
- **Explicit locks**: `SELECT … FOR UPDATE` locks the rows you read, so the others wait.
- **Compare-and-set (optimistic concurrency)**: keep a `version` column and write `UPDATE … SET balance = 50, version = 8 WHERE id = 1 AND version = 7`. If 0 rows changed, someone got there first: re-read and retry. This is the CAS idea from §3.4 again.
- **Materialise the conflict**: for write skew on rows that don't exist yet (room bookings), create rows to lock, such as one row per room per time slot.
- **Unique constraints**: let the database reject the second booking.
- Or simply use **serializable** and retry on abort.

The distributed version of all this (transactions across machines: 2PC, Sagas) is in [Part 2 §7](System%20Design%202%20-%20Distributed%20Systems%20Theory.md).

---

## 9. Probabilistic and spatial data structures

**The problem.** At scale, exact answers can cost too much memory. Exactly counting the distinct visitors among a billion 64-bit IDs needs about 8 GB. Often an answer within 1% is fine, and costs kilobytes.

### 9.1 Bloom filters: "definitely not" or "probably yes"

**The problem.** Before an expensive lookup (a disk read, a network call), you want to know cheaply whether the key could exist at all.

**How it works.**

1. Start with an array of $m$ bits, all 0, and pick $k$ independent hash functions.
2. **Add** an item: hash it $k$ ways and set those $k$ bits to 1.
3. **Query** an item: hash it $k$ ways. If *any* of those bits is 0, the item was **definitely never added**. If all are 1, it was **probably** added: the bits may have been set by other items, which is a false positive.

There are **no false negatives**, ever. You cannot delete items (a Counting Bloom filter or a Cuckoo filter adds that).

**The maths.** After inserting $n$ items, the false-positive probability is approximately:

$$
p \approx \left(1 - e^{-kn/m}\right)^{k}
$$

*The chance of a false positive is the chance that one bit is set, which is one minus e to the minus k n over m, raised to the power k, because all k bits must be set by accident.*

For a target $p$, the best choices are:

$$
m = -\frac{n \ln p}{(\ln 2)^2}, \qquad k = \frac{m}{n} \ln 2
$$

*The bits needed equal minus n times the natural log of p, divided by the square of ln 2. The best number of hash functions is bits per item times ln 2 (about 0.69).*

**Worked example.** One million keys at a 1% false-positive rate:

- Bits per key: $m/n = -\ln(0.01) / (\ln 2)^2 = 4.605 / 0.4805 = 9.59$ bits.
- Total memory: $9.59 \times 10^6$ bits ≈ **1.2 MB** (vs tens of MB to store the keys themselves).
- Hash functions: $k = 9.59 \times 0.693 = 6.6$, so use **7**.

![Fig 3 – Bloom filter false-positive rate (fig03_bloom_filter.png): false-positive rate against bits per key for k = 1, 3, 7 and the best k, with simulated points matching the theory.](images/fig03_bloom_filter.png)

*Fig 3 (fig03_bloom_filter.png). The green curve is the best achievable rate. Red dots are measured from a simulation with 5,000 keys, and they sit on the theory line. Each extra ~4.8 bits per key cuts the false-positive rate 10×.*

Code is useful here, because the whole structure fits in a few lines (from [system_design_theory.py](code/system_design_theory.py)):

```python
class BloomFilter:
    def __init__(self, n_items, fp_rate):
        self.m = math.ceil(-n_items * math.log(fp_rate) / math.log(2) ** 2)  # bits
        self.k = max(1, round(self.m / n_items * math.log(2)))                # hash functions
        self.bits = bytearray(self.m)

    def _positions(self, item):
        d = hashlib.sha256(item.encode()).digest()
        a, b = int.from_bytes(d[:8], "big"), int.from_bytes(d[8:16], "big")
        return [(a + i * b) % self.m for i in range(self.k)]   # double hashing

    def add(self, item):
        for p in self._positions(item):
            self.bits[p] = 1

    def might_contain(self, item):
        return all(self.bits[p] for p in self._positions(item))
```

Actual output for 100,000 keys at a 1% target:

```text
bits=958,506 (117 KiB), k=7
false negatives: 0   false positives: 0.98%
```

The "double hashing" line builds $k$ hash functions from two, as $h_1 + i \cdot h_2$. That's a standard trick that keeps the same error rate.

**Where Bloom filters live:** LSM-tree SSTables (skip files that can't hold the key, §6.2), cache-penetration defence (§5.3), CDNs (don't cache one-hit wonders), web crawlers (have I seen this URL?), and spell checkers.

### 9.2 HyperLogLog: counting distinct items in kilobytes

**The problem.** "How many unique visitors today?" An exact answer needs a set of every ID seen.

**The intuition.** Hash every item to a random-looking bit string. In random bits, a run of $r$ leading zeros happens with probability $2^{-r}$. If the longest run of leading zeros you've seen is 20, you've probably seen around $2^{20}$ (about a million) distinct items. Duplicates hash identically, so they don't change the answer. One such estimate is very noisy, so HyperLogLog splits items into $m$ buckets (registers) by their first few hash bits, keeps the maximum run per bucket, and combines the buckets with a harmonic mean plus bias corrections.

**The maths.** The relative standard error is:

$$
\text{error} \approx \frac{1.04}{\sqrt{m}}
$$

*The typical error is 1.04 divided by the square root of the number of registers.*

**Worked example.** With $m = 16{,}384$ registers: error $= 1.04 / 128 \approx 0.0081$, about 0.81%. Each register needs only 6 bits, so memory = 16,384 × 6 / 8 = **12 KB**, whatever the count, even billions. Compare 8 GB for an exact set of a billion IDs. This is exactly Redis's `PFADD`/`PFCOUNT`. HLLs also **merge**: the union of two HLLs is the register-wise maximum, so daily counts combine into weekly counts for free.

### 9.3 Count-Min Sketch: approximate frequencies

**The problem.** "Which search terms are trending?" or "Has this IP sent too many requests?" across billions of events.

**How it works.** Keep a 2-D array of counters with $d$ rows and $w$ columns, and one hash function per row. To add an item, increment one counter in each row. To estimate its count, take the **minimum** over its $d$ counters. Collisions only ever *add* to a counter, so the minimum is the least polluted estimate. It never underestimates.

With $w = \lceil e/\varepsilon \rceil$ and $d = \lceil \ln(1/\delta) \rceil$, the estimate exceeds the true count by at most $\varepsilon N$ (where $N$ is the total of all counts), with probability at least $1 - \delta$.

*Read it as: the width sets how big the error can be, and the depth sets how often you may exceed it.* For ε = 0.1% and δ = 1%: $w = 2{,}719$ and $d = 5$, so about 13,600 counters. Combine it with a small heap to track the **top-k heavy hitters**.

### 9.4 Geospatial indexing

**The problem.** "Find restaurants within 2 km" is a 2-D range query. Ordinary B-tree indexes sort along one dimension.

**How it works.** Map 2-D space onto 1-D keys (or a tree) that preserve nearness:

- **Geohash**: repeatedly split the world in half, alternating longitude and latitude, and record each choice as a bit. Encode the bits in base-32. Nearby points share prefixes, so "nearby" becomes a *prefix range query* on an ordinary index. A 6-character geohash is a cell of about 1.2 km × 0.6 km. At 7 characters it's about 153 m × 153 m. **Edge case:** two points can be 1 m apart across a cell boundary with completely different prefixes, so always search the target cell *and its 8 neighbours*.
- **Quadtree**: recursively split a square into four children until each holds at most K points. It adapts to density: dense cities get deep trees, oceans stay shallow. Typically kept in memory.
- **Google S2** (sphere → cube → Hilbert curve cells) and **Uber H3** (hexagons, whose neighbours are all equidistant) are the production-grade grids. They are used for ride matching, surge-pricing zones and delivery areas.
- **R-trees** (PostGIS, via GiST indexes) index rectangles and polygons, not only points.

---

## 10. Self-check and decision drills

<details>
<summary>1. A service gets 50 million requests a day with a peak factor of 4. What peak QPS do you design for?</summary>

50,000,000 / 86,400 ≈ 579/s on average. × 4 ≈ **2,300/s** at peak. (Shortcut: 1M/day ≈ 12/s, so 50M ≈ 580/s.)
</details>

<details>
<summary>2. Why does a new HTTPS connection fetching 1 MB take far longer than 1 MB ÷ bandwidth?</summary>

Handshakes (TCP 1 RTT + TLS 1.3 1 RTT) plus **TCP slow start**: starting from 14.6 KB and doubling each RTT takes about 7 RTTs to send 1 MB. Latency-bound, not bandwidth-bound. Fixes: connection reuse, CDNs near the user, HTTP/3.
</details>

<details>
<summary>3. Your cache hit ratio rises from 95% to 99%. By how much does database read load fall?</summary>

From 5% of reads to 1%: **5× less**. Small hit-ratio gains at the top end matter a lot.
</details>

<details>
<summary>4. Which engine would you pick for 500k writes/s of sensor data with mostly recent-range reads, and why?</summary>

An **LSM-based** store (wide-column or time-series): sequential writes, good compression, and cheap whole-partition retention. A B-tree would pay random page writes on every insert.
</details>

<details>
<summary>5. Two doctors go off call at the same moment under snapshot isolation, and nobody is left. Which anomaly is it, and give two fixes.</summary>

**Write skew.** Fixes: `SELECT … FOR UPDATE` on the rows checked; serializable isolation (SSI) and retry; or materialise the conflict as a row that both transactions must update.
</details>

<details>
<summary>6. A Bloom filter says "present". What do you know? And if it says "absent"?</summary>

"Present" = **probably** present (false positives possible). "Absent" = **definitely** absent (no false negatives).
</details>

<details>
<summary>7. Why must a geohash proximity search also look at neighbouring cells?</summary>

Points close together can sit on opposite sides of a cell boundary and share no prefix, so searching one cell misses them.
</details>

### Decision drills

These have no single right answer. Write your decision and *the reason* before opening each one, then compare your reasoning, not just your conclusion. Each one uses the loop from §2.5.

<details>
<summary><b>Drill 1.</b> A three-person startup expects 2,000 orders a day. The CTO wants Cassandra and Kafka "so we're ready for scale". What do you recommend?</summary>

**Quantify first:** 2,000 orders/day ÷ 86,400 ≈ 0.02 per second. Even 100× growth is 2 per second. **One PostgreSQL primary with a replica** handles that with enormous headroom, and orders need transactions (stock, payment state), which Cassandra makes hard.

**Name the cost of the alternative:** Cassandra and Kafka are two distributed systems a team of three must run, monitor and be on call for, with no requirement that needs them.

**Say what would change your mind:** "If we pass ~5,000 writes/s, or need multi-region writes, we revisit." Then add the cheap insurance now: UUIDv7 keys (§6.7), idempotent order creation, and a clean module boundary around orders, so a later move is possible.
</details>

<details>
<summary><b>Drill 2.</b> Product pages take 800 ms. A teammate says "add Redis". What do you do first?</summary>

**Measure where the 800 ms goes** before adding a component. Trace one request. Common findings: an N+1 query pattern (§6.6: 100 queries × 0.5 ms each, plus processing), a missing index (a Seq Scan in `EXPLAIN ANALYZE`), or a slow external call. Each has a cheaper fix than a cache.

If the database really is the cost, then use the cache decision guide (§5.3): Is it read-heavy? Is the traffic skewed? How stale may a product page be (that's your TTL)? What happens when the cache is empty? A cache that hides an N+1 bug still has the bug on every miss.
</details>

<details>
<summary><b>Drill 3.</b> Security requires that a compromised account is locked out within 1 minute. Your services use 1-hour JWT access tokens. What changes?</summary>

A JWT can't be revoked before it expires (§5.5), so today the worst case is **60 minutes**. Options:

1. **Shorten access tokens to ≤ 1 minute** with refresh tokens. Simple, but every client refreshes about once a minute, which adds load on the auth service.
2. **Keep 5–15 minute tokens and add a deny-list check** (a fast key-value lookup of revoked token or user IDs) on each request. Revocation is near-instant, at the cost of one lookup, which is close to what server-side sessions cost anyway.
3. **Server-side sessions** for the browser app, with tokens only between services.

The interesting judgement: the requirement has quietly turned a stateless design into a stateful one. Say that out loud, and choose where the state lives.
</details>

<details>
<summary><b>Drill 4.</b> You're creating the main tables of a multi-tenant SaaS product that will probably need sharding in two years. Which primary keys, and what will you shard by later?</summary>

**Keys:** UUIDv7 (or Snowflake IDs). They're generated anywhere without a central counter (which sharding would break), they're time-ordered so B-tree inserts stay fast (§6.7), and they're not guessable like auto-increment IDs.

**Future shard key:** `tenant_id`. Almost every query is "within one tenant", so a tenant's data stays together, and cross-shard queries become rare (Part 2 §4). Put `tenant_id` into every table and every index *now*, while it's cheap. Watch for one giant tenant becoming a hot shard; plan to move big tenants onto shards of their own.
</details>

<details>
<summary><b>Drill 5.</b> Users in Australia say the app is slow. Servers are in Virginia, and server-side processing time is 40 ms. Will adding more servers help?</summary>

**No.** The problem is physics, not capacity. A Sydney–Virginia round trip is about 200 ms (Fig 1), and a new HTTPS connection needs 2–3 round trips before the first response (§4.4). The 40 ms of processing is the small part.

Fixes, cheapest first: a **CDN** for static assets and cacheable responses; **connection reuse** and HTTP/3; then **regional read replicas or edge compute** for read-heavy pages; and only if writes must also be fast there, multi-region writes, with all of Part 2's consistency costs (Part 3 §5.7).
</details>

<details>
<summary><b>Drill 6.</b> A colleague wants to set every transaction to SERIALIZABLE "to be safe". Agree?</summary>

**Partly.** Serializable prevents every anomaly (§8.3), so it's the right default for code that checks an invariant across rows (bookings, on-call rotas, balances). But it costs throughput, and it **aborts** conflicting transactions, so *every* caller needs a retry loop. Code without one turns the aborts into user-facing errors.

A more precise policy: use **atomic updates** for simple counters (`likes = likes + 1`), **unique constraints** for uniqueness, **SERIALIZABLE (with retries)** for multi-row invariants, and the database default (read committed) for simple reads. That's deciding per path, not everywhere.
</details>

<details>
<summary><b>Drill 7.</b> The analytics team wants to run heavy hourly reports directly against the production PostgreSQL primary. What do you say?</summary>

Heavy scans compete with user transactions for CPU, I/O and the buffer cache. Long-running queries also hold back cleanup (VACUUM), so tables bloat. **Protect the primary.** Options: (1) a **dedicated read replica** for reporting, cheap and quick, with a lag of seconds; (2) **change data capture into a columnar warehouse** (Part 3 §3.5 and §8) when reports grow, since columnar storage is far faster for this work. Choose by how fresh the reports must be and how heavy they'll get.
</details>

---

## 11. Glossary

| Term | Meaning |
|---|---|
| **NFR** | Non-functional requirement: how well (latency, availability, durability, cost…) |
| **One-way / two-way door** | A decision that's expensive / cheap to reverse |
| **Premortem** | Imagining a future failure to find its likely causes now |
| **Zipf distribution** | Popularity where rank r gets traffic ∝ 1/rˢ; makes small caches effective |
| **UUIDv7** | Time-ordered 128-bit ID (RFC 9562); B-tree-friendly |
| **Power of two choices** | Pick two random servers, use the less loaded one |
| **QPS / RPS** | Queries / requests per second |
| **p99** | 99th percentile: 99% of requests are at least this fast |
| **RTT** | Round-trip time: there and back over the network |
| **IOPS** | Input/output operations per second a storage device can do |
| **fsync** | System call forcing buffered data onto stable storage |
| **Slow start** | TCP's ramp-up: the window doubles each RTT from a small start |
| **HOL blocking** | Head-of-line blocking: later data stuck behind a lost or slow earlier piece |
| **QUIC** | UDP-based transport with built-in TLS 1.3 and independent streams; carries HTTP/3 |
| **Anycast** | One IP announced from many places; routing picks the nearest |
| **L4 / L7 LB** | Load balancer acting on connections (L4) or on HTTP content (L7) |
| **Cache-aside** | App reads cache → on miss reads DB and fills cache; writes delete the key |
| **Stampede** | Many simultaneous misses on one key overwhelming the backend |
| **WAL** | Write-ahead log: durable record of changes, written before the data itself |
| **Memtable / SSTable** | LSM's in-memory sorted buffer / immutable sorted file on disk |
| **Compaction** | Background merging of SSTables that removes old versions and tombstones |
| **Fanout** | Child pointers per B-tree page; sets the tree height |
| **Write amplification** | Bytes physically written per byte the user wrote |
| **MVCC** | Multi-version concurrency control: readers see snapshots, writers add versions |
| **Snapshot isolation** | Each transaction reads one consistent snapshot; still allows write skew |
| **SSI** | Serializable snapshot isolation: MVCC plus conflict detection, abort on danger |
| **Write skew** | Two transactions decide on the same data, write different rows, break an invariant |
| **Bloom filter** | Bit array answering "definitely not / probably yes" |
| **HyperLogLog** | Sketch estimating distinct counts at ~1.04/√m error |
| **Count-Min Sketch** | Counter grid estimating frequencies, never underestimating |
| **Geohash** | Base-32 string for a lat/long cell; shared prefix ≈ nearby |
| **VPC / subnet** | Your private cloud network / a slice of it inside one AZ |
| **NAT** | Many private machines sharing one public IP for outbound traffic |
| **Security group** | Stateful firewall rules attached to instances |
| **Connection pool** | A set of open DB connections reused across requests |
| **Query plan** | The planner's chosen way to run a query; shown by `EXPLAIN` |
| **N+1 queries** | One query plus one more per result row; fixed with a join or batching |

---

## 12. References

- Martin Kleppmann and Chris Riccomini, *Designing Data-Intensive Applications*, 2nd edition, O'Reilly, 2026 ([author's page](https://martin.kleppmann.com/2026/03/24/designing-data-intensive-applications-2e.html)). Chapters on storage engines, encoding and transactions underpin §6–§8.
- Alex Petrov, *Database Internals*, O'Reilly, 2019 (B-trees, LSM-trees, compaction).
- Patrick O'Neil et al., "The Log-Structured Merge-Tree (LSM-Tree)", *Acta Informatica*, 1996.
- Hal Berenson et al., "A Critique of ANSI SQL Isolation Levels", SIGMOD 1995 (the anomaly definitions in §8).
- Michael Cahill, Uwe Röhm, Alan Fekete, "Serializable Isolation for Snapshot Databases", SIGMOD 2008 (SSI).
- Burton Bloom, "Space/Time Trade-offs in Hash Coding with Allowable Errors", *CACM*, 1970.
- Philippe Flajolet et al., "HyperLogLog: the analysis of a near-optimal cardinality estimation algorithm", 2007.
- Graham Cormode and S. Muthukrishnan, "An Improved Data Stream Summary: The Count-Min Sketch", 2005.
- RFC 9000 (QUIC), RFC 9114 (HTTP/3), RFC 8446 (TLS 1.3), RFC 6928 (TCP initial window of 10).
- On post-quantum TLS adoption (2026): [Post-quantum TLS: what's actually shipping in 2026](https://unveilscan.unveiltech.com/blog/post-quantum-tls.html); NIST FIPS 203 (ML-KEM).
- Latency figures after Jeff Dean's "Numbers Everyone Should Know" and Colin Scott's interactive update.
- Michael Mitzenmacher, "The Power of Two Choices in Randomized Load Balancing", *IEEE TPDS*, 2001.
- Lee Breslau et al., "Web Caching and Zipf-like Distributions: Evidence and Implications", INFOCOM 1999.
- Rajesh Nishtala et al., "Scaling Memcache at Facebook", NSDI 2013 (leases against stale sets and stampedes, §5.3).
- Stephen Robertson and Hugo Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond", 2009.
- RFC 9562 (UUIDs, including UUIDv7), 2024. RFC 7519 (JSON Web Token).
- Redis 8 relicensing under AGPLv3: [The Register, May 2025](https://www.theregister.com/2025/05/01/redis_returns_to_open_source/); PostgreSQL 19 beta notes: [postgresql.org](https://postgresql.org/about/news/postgresql-19-beta-1-released-3313/); PostgreSQL 19 RC 1 announced 15 October 2026 ([news archive](https://www.postgresql.org/about/newsarchive/)).

**Next:** [Part 2: Distributed Systems Theory](System%20Design%202%20-%20Distributed%20Systems%20Theory.md), where many machines must agree on what is true.
