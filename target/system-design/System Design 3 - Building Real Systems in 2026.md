# System Design 3: Building Real Systems in 2026

> **Series:** [Part 1: Foundations, Building Blocks and Storage](System%20Design%201%20-%20Foundations%20Building%20Blocks%20and%20Storage.md) · [Part 2: Distributed Systems Theory](System%20Design%202%20-%20Distributed%20Systems%20Theory.md) · **Part 3 (this file)** · [Part 4: Worked Case Studies](System%20Design%204%20-%20Worked%20Case%20Studies.md)
> **Self-contained:** the four parts in this folder need nothing else. Part 1 §2.5 explains the decision method used throughout.
> **Source:** built from research: papers, official specs and engineering write-ups listed in [References](#13-references). Every number recomputed with Python; figures from [make_figs.py](images/make_figs.py); code from [system_design_theory.py](code/system_design_theory.py).
> **Facts re-checked:** 22 October 2026. Things that moved recently:
> - OAuth 2.1 is **still an IETF draft** (revision -16, September 2026).
> - The **OWASP Top 10:2025** added *Software Supply Chain Failures* and *Mishandling of Exceptional Conditions*.
> - Hybrid post-quantum key exchange is now the browser default.
> - Kafka runs without ZooKeeper since 4.0, and **Kafka 4.2 (February 2026) made share groups ("queues for Kafka") production-ready**.
> - **MCP** moved to the Linux Foundation's Agentic AI Foundation (December 2025), and **A2A** became the common agent-to-agent protocol.
> - OpenTelemetry **profiles** reached public alpha (March 2026).
> - **Iceberg v3** (deletion vectors, row lineage) reached general availability in major warehouses.
> - Disaggregated LLM serving is now in production use.

**The big picture:** Parts 1 and 2 gave you the bricks and the physics. This part is how real systems are put together and kept alive: how services talk, how work flows asynchronously, why latency explodes under load, how to survive failure, how infrastructure and security are built, how data and AI systems work, and a repeatable method for designing anything.

Diagram colours: 🔵 input / primary · 🟣 processing · 🟢 result · 🟠 trade-off · 🔴 failure

---

## Contents

0. [How to use this guide](#0-how-to-use-this-guide)
1. [TL;DR](#1-tldr)
2. [APIs and communication](#2-apis-and-communication)
3. [Messaging, streaming and async workflows](#3-messaging-streaming-and-async-workflows)
4. [Performance theory: queues, tails and scaling laws](#4-performance-theory-queues-tails-and-scaling-laws)
5. [Reliability engineering](#5-reliability-engineering)
6. [Cloud-native infrastructure and observability](#6-cloud-native-infrastructure-and-observability)
7. [Security architecture](#7-security-architecture)
8. [Data and analytics systems](#8-data-and-analytics-systems)
9. [AI and LLM systems](#9-ai-and-llm-systems)
10. [Architecture patterns](#10-architecture-patterns)
11. [The design method, applied to three systems](#11-the-design-method-applied-to-three-systems)
12. [Self-check, decision drills and glossary](#12-self-check-decision-drills-and-glossary)
13. [References](#13-references)

---

## 0. How to use this guide

| If you have… | Read |
|---|---|
| 10 minutes | §0.1, §1, and Fig 8 (queue latency) in §4 |
| 1 hour | §3, §4, §5: async systems, performance and reliability, the core of production engineering |
| A weekend | Everything, then work through §11's three designs on paper *before* reading the answers |

### 0.1 First, in completely plain words

Back to the restaurant from Part 1. By now you have many cooks, shared fridges and branches across town. This part covers running the place day to day:

- **How orders travel** (APIs): the order ticket format, so every cook reads it the same way.
- **Not making customers wait for everything** (queues): take the order, give them a ticket number, and cook in the background.
- **Why the kitchen falls apart at 95% busy** (queueing theory): when cooks are almost always busy, the line grows *explosively*, not gradually.
- **Surviving bad nights** (reliability): don't let one broken oven take down the kitchen, and don't let everyone re-order at the same moment.
- **The building, the alarms and the locks** (infrastructure, observability, security).
- **The accounts office** (analytics) and **the new robot chef** (AI systems), which has its own very particular physics.

And finally, **a method**: the steps a senior engineer follows to design any system from a blank page.

---

## 1. TL;DR

1. **APIs**: REST for public resources, gRPC for internal service calls, GraphQL for flexible client-shaped reads. Use cursor pagination and idempotency keys, and evolve schemas only additively.
2. **Queues** decouple producers from consumers in time and rate. **Logs** (Kafka) also keep history, so consumers can replay. Order exists only *within a partition*.
3. **Little's Law:** concurrent requests = arrival rate × time in system. 10,000 req/s × 50 ms = 500 in flight.
4. **Queueing:** at a 10 ms service time, mean latency is 20 ms at 50% utilisation, 100 ms at 90% and 1,000 ms at 99%. **Never run near 100%.**
5. **Tail at scale:** if each backend is slow 1% of the time, a request fanning out to 100 backends is slow **63%** of the time.
6. **Reliability toolkit:** timeouts → retries with exponential backoff **and jitter** → retry budgets → circuit breakers → bulkheads → load shedding. Watch for *metastable* failures, where retries keep a system down after the trigger is gone.
7. **Availability math:** three 99.9% services in series give 99.7%. Two 99% replicas in parallel give 99.99%. A 99.9% SLO allows 43.2 minutes of downtime per 30 days: that's your **error budget**.
8. **Cloud-native** = declarative desired state + controllers that reconcile reality toward it (Kubernetes). Deploy gradually (canaries) and measure with OpenTelemetry.
9. **Security**: zero trust (authenticate every request, mTLS between services), OAuth 2.1/OIDC, passkeys, relationship-based authorisation, envelope encryption, signed supply chains, post-quantum TLS.
10. **Analytics** uses columnar storage. Lakehouses (Iceberg tables on object storage) are now the default data platform.
11. **LLM serving is memory-bound.** A 70B-class model needs 320 KiB of KV cache *per token*, so memory, not compute, limits how many users share a GPU. RAG = retrieve (hybrid search + rerank) → generate.
12. **Method:** requirements → estimates → API → data model → high-level design → deep dives → failure modes → evolution.

---

## 2. APIs and communication

### 2.1 Choosing an API style

**The problem.** Services and clients must agree on how to ask for things. The style decides coupling, performance and how easy change is.

| Style | Model | Strengths | Weaknesses | Typical use |
|---|---|---|---|---|
| **REST** over HTTP + JSON | Resources (`/orders/42`) + HTTP verbs | Universal, cacheable (GET), human-readable, great tooling | Over- and under-fetching; many round trips for nested data | Public APIs, CRUD |
| **gRPC** (HTTP/2 + Protobuf) | Typed remote procedure calls from a `.proto` contract | Fast binary encoding, generated clients, streaming in both directions, deadlines built in | Not natively callable from browsers (needs gRPC-Web or a proxy); harder to debug by eye | Internal service-to-service calls |
| **GraphQL** | Client sends a query shaped like the response it wants | One round trip, no over-fetching, strongly typed schema | Caching is harder (POST to one endpoint); expensive queries must be limited (depth/cost limits); N+1 resolver problem (fixed with batching such as DataLoader) | Rich front-ends aggregating many backends |
| **WebSocket / SSE** | Long-lived connection; server pushes | Real-time updates | Stateful connections complicate scaling and load balancing | Chat, live dashboards, notifications |
| **Webhooks** | You call *their* URL when an event happens | Push between companies | Delivery must be retried, signed and idempotent | Payment events, integrations |

**How to choose.** Use the style that matches *who calls you and how*. Public APIs that third parties integrate with: **REST**, because everyone can call it and caches understand it. Internal calls between your own services, where latency and typed contracts matter: **gRPC**. One front-end that stitches data from many backends: **GraphQL**, usually as a gateway layer in front of REST or gRPC services. Server push: **SSE** for one-way streams (notifications, LLM tokens), **WebSocket** for two-way traffic (chat, collaboration). Mixing styles across layers is normal.

**REST essentials**, the conventions every REST API should follow:

| Method | Meaning | Safe (no side effects)? | Idempotent (repeating it = doing it once)? |
|---|---|---|---|
| `GET` | Read a resource | Yes | Yes |
| `PUT` | Replace a resource with this full version | No | **Yes**: sending it twice leaves the same state |
| `DELETE` | Remove a resource | No | **Yes**: the second call finds it already gone |
| `POST` | Create a resource or run an action | No | **No**: needs an idempotency key (§2.3) |
| `PATCH` | Partially update | No | Not necessarily |

Why it matters: **safe and idempotent methods can be retried automatically** by clients, proxies and load balancers. A `POST` cannot, unless you make it idempotent yourself.

- **Resources are nouns**: `/orders/42/items`, not `/getOrderItems?id=42`. Actions that don't fit the resource model become sub-resources (`POST /orders/42/cancellation`).
- **Status codes carry meaning**: `200/201/204` success; `400` bad input; `401` not authenticated; `403` authenticated but not allowed; `404` not found; `409` conflict (such as a version mismatch); `422` well-formed but invalid; `429` rate-limited; `5xx` the server's fault, which may be retryable. Never return `200` with an error inside the body.
- **One error format everywhere**: RFC 9457 "Problem Details" (`type`, `title`, `status`, `detail`, plus your own fields) is the standard shape. Clients can then handle errors generically.
- **Versioning**: evolve by adding (§2.2). Introduce `/v2` only for genuinely breaking changes, run versions side by side, and announce retirement with the `Deprecation` and `Sunset` headers.
- **Concurrency control**: return an `ETag` (a version) with each resource. Clients send `If-Match: <etag>` on updates, and the server rejects stale ones with `412`. This is optimistic concurrency (compare-and-set, Part 1 §8.5) over HTTP.

### 2.2 Contracts and schema evolution

**The problem.** Producers and consumers deploy at different times. During a rolling deploy, old and new code run side by side, and stored data written years ago must still be readable.

**How it works.** Two directions of compatibility:

- **Backward compatible**: *new* code can read data written by *old* code.
- **Forward compatible**: *old* code can read data written by *new* code (it must ignore what it doesn't know).

Protobuf, Avro and Thrift make both possible with rules:

1. Fields are identified by **number** (Protobuf/Thrift) or by schema resolution (Avro), not by position.
2. **Only add optional fields.** Old readers skip unknown field numbers; new readers use defaults when a field is missing.
3. **Never reuse or change a field number's type.** Mark removed fields as `reserved`.
4. For JSON APIs: add fields freely, never rename or remove without a deprecation window, and version (`/v2/`) only on genuinely breaking changes.

A **schema registry** (common with Kafka) enforces these rules on every producer at publish time.

### 2.3 Pagination, idempotency and other API essentials

- **Offset pagination** (`?offset=1000000&limit=20`) makes the database walk past a million rows every time, and pages shift when rows are inserted. **Cursor pagination** (`?after=<last_id>`, implemented as `WHERE id > :last_id ORDER BY id LIMIT 20`) is O(page size) with an index, and stable under inserts. Use cursors for anything large.
- **Idempotency keys** on every non-idempotent operation (POST payments, orders) make client retries safe (Part 2 §8.5).
- **Timeouts and deadlines**: gRPC propagates a deadline so downstream services stop working on a request the caller has already given up on.
- **Rate limits** with clear `429` responses and `Retry-After` headers. The algorithms (fixed and sliding windows, token and leaky buckets) and a full distributed design are in [Part 4 §2](System%20Design%204%20-%20Worked%20Case%20Studies.md).
- **Service discovery**: callers find healthy instances through DNS, a registry (Consul, etcd) or the platform itself (Kubernetes Services).

---

## 3. Messaging, streaming and async workflows

### 3.1 Why go asynchronous

**The problem.** In a synchronous chain (A calls B calls C), the user waits for the *sum* of the latencies. The chain is only as available as the *product* of the availabilities (§5.4), and a spike at A hits C directly.

**The fix.** Put a **message broker** between them. The producer writes a message and moves on; consumers process it when they can. You gain:

1. **Temporal decoupling**: the consumer can be down for a while; messages wait.
2. **Load levelling**: a burst fills the queue instead of crushing the consumer.
3. **Fan-out**: many independent consumers can react to one event.

The costs: eventual consistency (the work isn't done when the user gets "OK"), harder debugging, and the delivery-semantics problems from Part 2 §8.5.

**Decision guide: synchronous call or asynchronous message?**

| Question | Points to **synchronous** (request/response) | Points to **asynchronous** (queue/event) |
|---|---|---|
| Does the user need the result to continue? | Yes: "is this card valid?", "show my balance" | No: "send the receipt email", "update the search index" |
| Must the work finish within the request's time budget? | Yes, and it's fast | It's slow (video transcoding, reports) or bursty |
| What if the downstream is briefly down? | The user can see an error and retry | The work must not be lost; it should wait and happen later |
| How many parties care? | One caller | Many consumers (analytics, notifications, search…) |
| Is strict ordering across steps needed? | Easy in one call chain | Possible per key/partition only |

**A common good shape:** do the *minimum* synchronously (validate, write the core record, return an ID), then publish an event and let everything else happen asynchronously. Tell the user honestly what's pending ("Your report is being prepared").

### 3.2 Queues vs logs

| | **Message queue** (RabbitMQ, SQS, ActiveMQ) | **Log** (Kafka, Redpanda, Pulsar, Kinesis) |
|---|---|---|
| Model | Messages are delivered to a consumer and **deleted** once acknowledged | Messages are **appended** to a durable, ordered log and **kept** for a retention period |
| Consumers | Compete for messages (work distribution) | Each consumer group tracks its own **offset**; many groups read independently |
| Replay | No (once consumed, gone) | **Yes**: rewind the offset and reprocess history |
| Ordering | Usually none across competing consumers | Strict **within a partition** |
| Best for | Task queues, jobs, per-message routing | Event streams, CDC, event sourcing, analytics pipelines |

### 3.3 Kafka internals worth knowing

**How it works.**

- A **topic** is split into **partitions**, each an append-only log replicated across brokers. Every message has an **offset** in its partition.
- Producers choose the partition by **key** (`hash(key) mod partitions`), so all events for one key (one order, one user) stay **in order** in one partition.
- A **consumer group** shares partitions among its members. Each partition goes to exactly one member, so **the partition count caps a group's parallelism**: 12 partitions means at most 12 useful consumers in that group.
- **Replication**: each partition has a leader and followers. The **in-sync replicas (ISR)** are the followers that are caught up. With `acks=all` and `min.insync.replicas=2` (replication factor 3), a write is acknowledged only once at least 2 replicas have it. That survives a broker loss without losing data.
- **Retention** by time or size; **log compaction** keeps only the latest value per key, which turns a topic into a durable table of the current state.
- **Metadata** is managed by an internal Raft quorum (**KRaft**); ZooKeeper support was removed in Kafka 4.0 (2025).
- **Rebalancing.** When a consumer joins, leaves or crashes, the group reassigns partitions. A consumer that's too slow to poll (it exceeds `max.poll.interval.ms`) is presumed dead and its partitions are taken away. That causes **duplicate processing**, because its uncommitted offsets get re-read by the new owner. Modern clients use incremental, cooperative rebalancing so only the moved partitions pause. Design consumers to be idempotent anyway.
- **Consumer lag** (the latest offset minus the committed offset, per partition) is *the* health metric of a streaming system. Lag that keeps growing means consumers can't keep up; see backpressure (§3.4).
- **Offsets and "exactly once".** A consumer that processes a message and then crashes *before committing its offset* will see that message again. Commit after processing and make processing idempotent (at-least-once + idempotency), or use Kafka transactions for read-process-write pipelines that stay inside Kafka.
- **Share groups ("queues for Kafka")**, production-ready since Kafka 4.2 (February 2026): consumers in a share group **share** a partition, each message is acknowledged individually, and there's a delivery count per message. That gives queue-style work distribution (more consumers than partitions, per-message retry) on a Kafka topic, at the cost of per-key ordering. Some client libraries still lagged behind the brokers in 2026. Use classic consumer groups when order matters; share groups for independent tasks.

**Worked example: sizing partitions.** You need to ingest 1 GB/s, and one consumer instance processes about 10 MB/s. Partitions needed ≥ 1,000 MB/s ÷ 10 MB/s = **100**. Add headroom (say 150–200), because adding partitions later changes which partition each key maps to, and that breaks per-key ordering during the change.

### 3.4 Backpressure

**The problem.** If producers are permanently faster than consumers, queues grow without limit: memory runs out, or latency becomes hours.

**The options, in order of preference:** (1) **scale consumers** if the work can be parallelised; (2) **apply backpressure**: slow the producer down with bounded queues, TCP-style flow control, or reactive streams' demand signalling; (3) **shed load** by dropping or rejecting low-priority work (§5.3). A queue is a shock absorber for *bursts*. It can't fix a *sustained* rate mismatch. Little's Law (§4.1) tells you how deep the queue gets.

### 3.5 Event-driven patterns: event sourcing, CQRS, CDC

- **Event sourcing**: store the **sequence of events** ("Deposited 50", "Withdrew 20") as the source of truth, not the current state. Current state = fold over the events. You get a complete audit trail, time travel ("what was the balance last Tuesday?") and new views built by replaying. The costs: versioning event schemas forever, snapshots to avoid replaying millions of events, and "deleting" data for privacy (often solved with crypto-shredding: encrypt per user and delete the key).
- **CQRS (Command Query Responsibility Segregation)**: separate the **write model** (validates commands, emits events) from one or more **read models** (denormalised views optimised for each query: a search index, a cache, a reporting table). Read models are updated asynchronously, so they are eventually consistent. It's often paired with event sourcing, but doesn't require it.
- **Change Data Capture (CDC)**: read the database's own replication log (the PostgreSQL WAL, the MySQL binlog) and publish every row change as an event (Debezium is the standard tool). This is how you keep caches, search indexes and warehouses in sync with the database **without dual writes** (Part 2 §8.4). The database stays the source of truth.

```mermaid
flowchart LR
    accTitle: CQRS with change data capture
    accDescr: Commands write to the primary database; CDC streams changes through Kafka into read models such as search, cache and warehouse.
    CMD(["Commands<br/>(writes)"]) --> DB[("Primary DB<br/>source of truth")]
    DB -->|"WAL / binlog"| CDC["CDC connector<br/>(Debezium)"]
    CDC --> K[["Kafka topics<br/>one per table"]]
    K --> S[("Search index")]
    K --> C[("Cache")]
    K --> W[("Warehouse /<br/>lakehouse")]
    Q(["Queries<br/>(reads)"]) --> S
    Q --> C
    class CMD,Q primary;
    class CDC,K intermediate;
    class DB,S,C,W target;
    classDef primary fill:#EFF6FF,stroke:#2563EB,stroke-width:1.5px,color:#0F172A;
    classDef intermediate fill:#FAF5FF,stroke:#7C3AED,stroke-width:1.5px,color:#0F172A;
    classDef target fill:#F0FDF4,stroke:#059669,stroke-width:2px,color:#0F172A;
```

### 3.6 Stream processing: time, windows and watermarks

**The problem.** "Count clicks per minute" sounds easy, until events arrive late and out of order (a phone was offline for 10 minutes).

**How it works.**

- **Event time** (when it happened) vs **processing time** (when the system saw it). Correct analytics uses event time.
- **Windows** group the infinite stream: **tumbling** (fixed and non-overlapping: 12:00–12:01, 12:01–12:02), **sliding/hopping** (overlapping: a 5-minute window every minute), **session** (bursts of activity separated by a gap of inactivity).
- A **watermark** is the processor's claim: "I believe I've now seen all events with event time ≤ T." When the watermark passes the end of a window, the window's result is emitted. Events that arrive later still are **late data**: drop them, send them to a side output, or update the result (allowed lateness).
- **The trade-off**: an aggressive watermark gives fast but sometimes incomplete results. A conservative one gives complete but slow results.
- **Stateful processing** (running counts, joins) needs fault-tolerant state. Flink takes periodic consistent **checkpoints** across all operators (a variant of the Chandy-Lamport snapshot algorithm), and on failure restores state and replays the log from the matching offsets. That's exactly-once *state*, combined with transactional sinks for exactly-once *output*.

Engines: Apache Flink (the reference), Kafka Streams (a library inside your service), Spark Structured Streaming, and managed equivalents.

### 3.7 Durable execution and workflow orchestration

**The problem.** Business processes span minutes to months (order → payment → shipping → a 30-day return window). Writing them as code over queues and cron jobs, with manual state tracking, retries and compensations, is where bugs live.

**How it works.** **Durable execution** engines (Temporal, Restate, AWS Step Functions, Azure Durable Functions) let you write the workflow as ordinary code. The engine **records every step's result in an event history**. If the worker crashes, another worker *replays* the history to rebuild the exact state, and continues from the next step. Timers ("wait 30 days") and retries are built in. Your workflow code must be **deterministic** (no direct randomness or clock reads, which go through the engine's APIs instead), because replay must produce the same decisions. This is the natural home for sagas (Part 2 §8.3), and increasingly for long-running AI agents (§9.5).

### 3.8 Poison messages and dead-letter queues

**The problem.** Some messages will *never* succeed: malformed data, a bug triggered by one particular input, a reference to a deleted record. With automatic retries, such a **poison message** either loops forever, burning capacity, or (in an ordered log like Kafka) **blocks its whole partition**, so every message behind it waits.

**How it works.**

1. **Classify errors.** *Transient* errors (timeouts, 503, a lock conflict) deserve retries with backoff. *Permanent* errors (a validation failure, a 400 from the downstream) will fail every time, so stop retrying immediately.
2. After N failed attempts, or on a permanent error, move the message to a **dead-letter queue (DLQ)** with its error details, the number of attempts and a timestamp. The main queue keeps flowing.
3. **Treat the DLQ as an alarm.** Alert when its depth grows. Build tooling to inspect messages, fix the cause, and **re-drive** them back into the main queue. A DLQ nobody watches is just a slower way to lose data.

Queues such as SQS and RabbitMQ have DLQs built in (SQS moves a message after `maxReceiveCount` failed receives). Kafka has none. The usual pattern is a chain of **retry topics** with increasing delays (`orders.retry.1m` → `orders.retry.1h`), then a final `orders.dlq` topic.

> **The ordering catch.** Moving one message aside breaks per-key order: later events for the same order are processed before the failed one. If order matters (account balance updates), park the *whole key*: stop processing that key until its stuck message is resolved, and keep processing other keys.

### 3.9 Job scheduling: task queues, delayed jobs and distributed cron

**The problem.** Much of a backend's work isn't a user request: sending emails, generating reports, nightly cleanups, retrying a payment in an hour. "Design a job scheduler" is a common interview question because it combines queues, leases, idempotency and time.

**Task queues** (Celery, Sidekiq, BullMQ, SQS + workers): producers enqueue jobs, and a pool of workers pulls and runs them.

- **Visibility timeout / lease.** When a worker takes a job, the job becomes invisible to others for a set time. If the worker finishes, it deletes the job. If it crashes, the timeout expires and the job reappears for another worker. So delivery is **at-least-once**, and **jobs must be idempotent** (Part 2 §8.5). Set the timeout above the job's p99 duration, and have long jobs send heartbeats to extend their lease.
- Per-job **timeouts, retries with backoff, a DLQ** (§3.8), **priorities** (separate queues), and **per-tenant fairness**, so one customer's 1M jobs don't starve everyone else.

```mermaid
stateDiagram-v2
    [*] --> Scheduled: run_at in the future
    Scheduled --> Ready: run_at reached
    [*] --> Ready: enqueue now
    Ready --> Running: worker takes lease
    Running --> Succeeded: done, job deleted
    Running --> Ready: lease expired (worker crashed)
    Running --> Retrying: transient error
    Retrying --> Ready: after backoff
    Running --> Dead: permanent error or too many attempts
    Retrying --> Dead: attempts exhausted
```

**Delayed jobs** ("send a reminder in 24 hours"): store jobs with a `run_at` time in a structure ordered by time, such as a Redis sorted set or a database table indexed on `run_at`. Pollers claim due jobs. In PostgreSQL, this query lets many workers claim *different* jobs without blocking each other:

```sql
SELECT id FROM jobs
WHERE status = 'scheduled' AND run_at <= now()
ORDER BY run_at
LIMIT 100
FOR UPDATE SKIP LOCKED;
```

`SKIP LOCKED` makes each worker skip rows another worker has already locked, which turns an ordinary table into a safe, concurrent job queue.

**Distributed cron** (run "every day at 02:00" exactly once across a fleet):

- Cron on *every* server runs the job N times. Cron on *one* server is a single point of failure.
- **Option 1: a leader runs the scheduler.** Elect a leader with a lease in etcd or ZooKeeper (Part 2 §7.5), and protect its side effects with fencing tokens (Part 2 §7.6), because a paused old leader may wake up and run the job again.
- **Option 2: claim each run in the database.** For every scheduled run, insert `(job_id, scheduled_time)` under a **unique constraint**. Whichever scheduler inserts first owns that run. The others get a constraint violation and skip it. Exactly one claim per run, with no leader needed.
- Decide what happens to **missed runs** (the scheduler was down at 02:00: catch up, or skip?), and handle **time zones and daylight-saving changes** (02:30 may happen twice, or not at all, on change days).
- For multi-step or long-running jobs, a durable workflow engine (§3.7) handles retries, timers and state for you.

---

## 4. Performance theory: queues, tails and scaling laws

### 4.1 Little's Law

**The problem.** How many requests are "inside" the system at once? That sets the thread pools, connection pools and memory you need.

$$
L = \lambda W
$$

*The average number of items in a system equals the average arrival rate times the average time each item spends inside.* It holds for any stable system, whatever the distributions.

**Worked example.** 10,000 requests/s, each spending 50 ms in the service: $L = 10{,}000 \times 0.05 = 500$ concurrent requests. If a downstream slowdown raises $W$ to 500 ms, concurrency jumps to **5,000**. Pools sized for 500 run out and requests start queueing or failing. **A latency problem quickly becomes a capacity problem.** At extreme scale the same law sets hard limits: 1,000,000 requests/s at 20 ms each means 20,000 requests in flight at every instant, and every one of them holds memory, a connection and often a thread. That's why high-throughput servers use event loops (Part 1 §3.4) rather than a thread per request.

### 4.2 Why latency explodes near full utilisation

**The problem.** Teams want servers "efficiently" busy at 90–95%. Queueing theory says that's exactly where latency becomes unbearable.

**How it works.** Model a server as an **M/M/1 queue**: random (Poisson) arrivals at rate $\lambda$, random (exponential) service times with mean $S$, and one server. Utilisation is $\rho = \lambda S$. Mean time in the system:

$$
W = \frac{S}{1 - \rho}
$$

*Mean response time is the service time divided by one minus the utilisation.* As utilisation $\rho$ approaches 1, the denominator approaches 0 and the wait goes to infinity.

**Worked example.** Service time $S = 10$ ms:

| Utilisation ρ | Mean latency $W$ | vs. idle |
|---|---|---|
| 50% | 10 / 0.5 = **20 ms** | 2× |
| 80% | 10 / 0.2 = **50 ms** | 5× |
| 90% | 10 / 0.1 = **100 ms** | 10× |
| 95% | 10 / 0.05 = **200 ms** | 20× |
| 99% | 10 / 0.01 = **1,000 ms** | 100× |

Going from 90% to 99% busy (only 10% more throughput) makes latency **10× worse**. In this model the response time is exponentially distributed, so the 99th percentile is $W \ln 100 \approx 4.6 W$: at 90% utilisation, p99 ≈ 460 ms.

![Fig 8 – Queue latency vs utilisation (fig08_queue_latency.png): mean and 99th-percentile latency of an M/M/1 queue with 10 ms service time, rising sharply above 80% utilisation.](images/fig08_queue_latency.png)

*Fig 8 (fig08_queue_latency.png). Real systems aren't exactly M/M/1, but the hockey-stick shape is universal. Variability (in arrivals or in service time) is what creates the queue. Lower variability (batching, uniform work) moves the knee to the right.*

**Design rules that follow:** target 50–70% utilisation for latency-sensitive services; autoscale on utilisation or queue depth *before* the knee; and remember that a "small" traffic increase near the knee causes a huge latency increase.

### 4.3 The tail at scale

**The problem.** Your backend's p99 is 100 ms. The user-facing request calls 100 backends in parallel and waits for all of them. What's the user's latency?

**How it works.** If each backend is independently slow with probability $q$, the chance that a request touching $n$ backends hits at least one slow one is:

$$
P(\text{slow}) = 1 - (1 - q)^{n}
$$

*The chance of at least one slow backend is one minus the chance that all n are fast.*

**Worked example.** $q = 0.01$, i.e. 1% (each backend's p99): fan-out 1 gives 1%; fan-out 10 gives $1 - 0.99^{10} \approx 0.096$, i.e. 9.6%; fan-out 100 gives $1 - 0.99^{100} \approx 0.634$, i.e. **63.4%**. The backend's rare 1-in-100 slowness becomes the user's *typical* experience.

![Fig 10 – Tail at scale (fig10_tail_fanout.png): probability a user request is slow against fan-out, for backends slow 1%, 0.1% and 0.01% of the time.](images/fig10_tail_fanout.png)

*Fig 10 (fig10_tail_fanout.png). This is why large systems obsess over p99 and p99.9 of their **backends**, not their averages.*

**Defences** (Dean and Barroso, "The Tail at Scale", 2013):

- **Hedged requests**: send the request to one replica; if there's no reply by the p95 latency, send a second copy to another replica and take whichever answers first. It costs about 5% extra load and cuts the tail dramatically.
- **Tied requests**: send to two replicas at once, and the one that starts work tells the other to cancel.
- **Fewer fan-out hops**, partial results ("good enough" search answers), and isolating background work (compaction, GC) from serving.

### 4.4 Amdahl's law and the Universal Scalability Law

**The problem.** Why does doubling the servers rarely double the throughput, and why does it sometimes *reduce* it?

**Amdahl's law.** If a fraction $p$ of the work parallelises perfectly and $1 - p$ is serial:

$$
S(N) = \frac{1}{(1 - p) + p/N}
$$

*Speed-up on N workers is one over the serial part plus the parallel part divided by N.* As $N \to \infty$, $S \to 1/(1-p)$. With 5% serial work ($p = 0.95$): 16 workers give $1/(0.05 + 0.95/16) = 9.1\times$, and **no number of workers ever exceeds 20×**.

**The Universal Scalability Law** (Neil Gunther) adds **coherence cost**: workers must also coordinate *with each other* (cache invalidation, locks, consensus, cross-shard queries), and that cost grows with pairs of workers:

$$
C(N) = \frac{N}{1 + \sigma (N - 1) + \kappa N (N - 1)}
$$

*Capacity on N nodes is N divided by one, plus a contention term σ times (N − 1), plus a coherence term κ times N times (N − 1).* $\sigma$ is the contention (serial) fraction and $\kappa$ is the cost of each pair of nodes keeping each other in sync. Because the κ term grows like $N^2$, capacity **peaks** and then **falls**, at:

$$
N^{\ast} = \sqrt{\frac{1 - \sigma}{\kappa}}
$$

**Worked example.** $\sigma = 0.05$, $\kappa = 0.001$: $N^{\ast} = \sqrt{0.95 / 0.001} = \sqrt{950} \approx 31$ nodes, giving 9.0× capacity. At 100 nodes, capacity *drops* to 6.3×. Adding machines made it slower.

![Fig 9 – Scalability laws (fig09_scalability_laws.png): linear ideal, Amdahl with 5% serial work capped at 20×, and the USL curve peaking near 31 nodes then declining.](images/fig09_scalability_laws.png)

*Fig 9 (fig09_scalability_laws.png). You can fit σ and κ to your own load-test measurements to predict where your system stops scaling. **The design lesson:** shared-nothing architectures (independent partitions, no cross-node coordination on the hot path) drive κ toward 0. That's why partitioning (Part 2 §4) scales and global locks don't.*

---

## 5. Reliability engineering

### 5.1 Timeouts, retries and jitter

**The problem.** Calls fail transiently (a dropped packet, a restarting pod). Retrying fixes most transient failures. But naive retries turn a small problem into an outage.

**How it works, layer by layer:**

1. **Always set timeouts.** A call without a timeout can hang forever, holding a thread, a connection and memory (Little's Law again). Base the timeout on the downstream's measured p99.9, and **propagate deadlines** so inner calls give up when the outer request has.
2. **Retry only what is safe**: idempotent operations, or those protected by idempotency keys. Retry only retryable errors (timeouts, 503) and never client errors (400).
3. **Exponential backoff**: wait $\text{base} \times 2^{\text{attempt}}$ (capped) between tries, giving the dependency room to recover.
4. **Jitter**: randomise the wait. Without it, every client that failed at the same instant retries at the same instant. That's a synchronised wave that hits the recovering service again and again.

![Fig 11 – Retry jitter (fig11_retry_jitter.png): with no jitter, 1,000 clients' retries arrive in four 1,000-request spikes; with full jitter they spread out over time.](images/fig11_retry_jitter.png)

*Fig 11 (fig11_retry_jitter.png). Toy simulation: 1,000 clients fail at t = 0 and retry 4 times with backoff 100·2ᵃ ms. Left: every retry lands in four spikes of 1,000 requests. Right: "full jitter" (sleep a uniform random time between 0 and the backoff) spreads them out, so the peak is under 300 per 20 ms.*

Full jitter is one line (from [system_design_theory.py](code/system_design_theory.py)):

```python
def backoff_full_jitter(attempt, base=0.1, cap=10.0, rng=random):
    """Seconds to sleep before retry number `attempt` (0-based)."""
    return rng.uniform(0, min(cap, base * 2 ** attempt))
```

```text
sleeps (s): [0.024, 0.109, 0.148, 0.483, 1.001, 0.21]
```

Notice the last sleep (0.21 s) is *shorter* than the one before. That's intended: each sleep is random in $[0, \text{base} \cdot 2^{a}]$, so clients de-synchronise.

5. **Retry budgets.** Retries multiply load *across layers*. If each of 3 layers retries 3 times, one user request can become $3^3 = 27$ requests at the bottom, exactly when the bottom is struggling. Cap retries as a fraction of traffic (for example "retries ≤ 10% of requests" per client), and retry at **one** layer only, usually the one closest to the user.

### 5.2 Circuit breakers and bulkheads

**Circuit breaker.** When a dependency is failing, stop calling it for a while. You fail fast instead of piling up waiting threads, and you give it room to recover.

```mermaid
stateDiagram-v2
    [*] --> Closed
    Closed --> Open: failure rate over threshold
    Open --> HalfOpen: cool-down timer expires
    HalfOpen --> Closed: trial requests succeed
    HalfOpen --> Open: a trial request fails
```

- **Closed**: calls flow normally; failures are counted over a sliding window.
- **Open**: calls fail immediately (return a fallback: cached data, a default, or a clear error).
- **Half-open**: let a few trial calls through. Success closes the breaker; failure re-opens it.

**Bulkheads** (named after a ship's watertight compartments): give each dependency its **own** bounded resource pool (threads, connections, queue). If the recommendations service hangs, it can exhaust only *its* 20 threads, not the 200 that checkout also needs.

### 5.3 Load shedding and metastable failures

**Load shedding.** When demand exceeds capacity, **reject some requests deliberately and early**, instead of slowing down for everyone. A fast `503` (or `429`) costs microseconds. A request that queues, times out after 10 s and is retried costs far more. Techniques: priority-aware admission (keep checkout, shed analytics), concurrency limits that adapt to latency (Netflix's adaptive concurrency limits, inspired by TCP congestion control), and dropping requests that have already waited longer than their deadline.

**Metastable failures** (Bronson et al., HotOS 2021) are the scariest pattern in large systems. A temporary trigger (a traffic spike, a brief slowdown, a cache flush) pushes the system into a bad state that **sustains itself after the trigger is gone**:

1. Something slows the service briefly.
2. Requests time out, and clients retry, which adds load.
3. More load means more timeouts, which means more retries.
4. The trigger has passed, but the system stays overloaded. Its own retry traffic keeps it down.

Other self-sustaining loops: a cache that empties under load (every miss hits the DB, which is too slow to refill the cache), and GC thrashing from queued requests. **Defences:** retry budgets and jitter, load shedding, circuit breakers, slow ramp-up after recovery, and (critically) the ability to *drop* load to break the loop.

### 5.4 Availability math and the nines

**Serial dependencies** (A needs B needs C) multiply:

$$
A_{\text{serial}} = \prod_{i} A_i
$$

*The availability of a chain is the product of each link's availability.* Three services at 99.9%: $0.999^3 \approx 0.9970$, i.e. 99.70%. **Every synchronous dependency reduces your availability.**

**Parallel redundancy** (any one of several replicas is enough):

$$
A_{\text{parallel}} = 1 - \prod_{i} (1 - A_i)
$$

*A redundant group fails only if every member fails at once.* Two independent 99% replicas: $1 - 0.01^2 = 0.9999$, i.e. 99.99%. Two "nines" of components gave four nines of service, *if* failures are independent. That's why replicas go in different availability zones.

| Availability | Downtime per year | Per 30 days |
|---|---|---|
| 99% ("two nines") | 3.65 days (5,256 min) | 7.2 hours (432 min) |
| 99.9% | 8.76 hours (525.6 min) | **43.2 min** |
| 99.99% | 52.6 min | 4.3 min |
| 99.999% | 5.3 min | 26 seconds |

Each extra nine costs roughly an order of magnitude more engineering. At 99.99%, a human can't even respond to an alert in time, so recovery must be **automatic**.

### 5.5 SLIs, SLOs, SLAs and error budgets

- **SLI (service level indicator)**: a measured ratio of good events. "Fraction of requests served successfully in under 300 ms."
- **SLO (objective)**: the target for the SLI over a window. "99.9% over 30 days." An *internal* goal.
- **SLA (agreement)**: a *contract* with customers, with penalties. Always looser than the SLO, so you have warning before you owe money.
- **Error budget** = $1 - \text{SLO}$. For 99.9% over 30 days, that's $0.001 \times 43{,}200$ min = **43.2 minutes** of allowed badness. While budget remains, ship features and take risks. When it's spent, freeze risky launches and fix reliability. It turns "reliability vs speed" from an argument into a number.
- **Burn-rate alerting**: alert when the budget is being consumed fast (for example, at a rate that would spend a month's budget in two days), rather than on every blip. This is the standard practice from Google's SRE workbook.

> **100% is the wrong target.** Users can't tell 99.99% from 100% (their own Wi-Fi is less reliable), and chasing it stops all change. Pick the SLO users actually need.

### 5.6 Disaster recovery, cells and chaos

**Two numbers define a DR plan:**

- **RPO (recovery point objective)**: how much data you can afford to lose, measured in time ("the last 5 minutes"). It's set by backup frequency and replication mode.
- **RTO (recovery time objective)**: how long you can be down.

| Strategy | RPO / RTO | Cost |
|---|---|---|
| Backup and restore | Hours / hours–days | Low |
| Pilot light (data replicated, minimal compute idle) | Minutes / tens of minutes | Medium |
| Warm standby (a scaled-down full copy running) | Seconds–minutes / minutes | High |
| Multi-site active-active | ≈ 0 / ≈ 0 | Highest, plus all of Part 2's consistency problems |

Back-up rules: the **3-2-1 rule** (3 copies, 2 media types, 1 off-site), *immutable* backups (ransomware deletes mutable ones), and **regular restore tests**. A backup you've never restored is a hope, not a backup.

**Cell-based architecture** (used heavily at AWS): instead of one giant deployment, run many identical, independent **cells**, each serving a subset of customers with its own full stack. A bad deploy or poison request takes down one cell, not everyone, which limits the **blast radius**. A thin routing layer maps customers to cells. **Shuffle sharding** goes further: give each customer a random *combination* of a few workers, so two customers rarely share all their workers, and one noisy or malicious customer can't take down the others.

**Chaos engineering** (Netflix's Chaos Monkey, now a discipline): deliberately inject failures in controlled experiments (kill instances, add latency, partition networks, fail an AZ) to verify that the resilience mechanisms above actually work. Start with a hypothesis ("checkout's SLO holds if one cache node dies"), limit the blast radius, then automate it.

### 5.7 Multi-region architecture: the patterns and how to choose

**The problem.** One region can fail completely (it has happened to every major cloud), and users far away are slow (Part 1 §2.4). Going multi-region solves both, but it's the single biggest jump in complexity in this whole guide, because it brings every problem from Part 2 into play at 80–200 ms round trips.

**First, be clear which problem you're solving:**

- **Latency for distant users** → mostly a *read* problem. CDNs, edge caches and regional read replicas fix most of it *without* multi-region writes.
- **Surviving a region outage** → a *DR* problem. Its cost depends on your RPO and RTO (§5.6).
- **Data residency** → a *legal* problem (§7.7). Partition users by region; it doesn't require writes anywhere else.

**The patterns, from simple to hard:**

| Pattern | How it works | RPO / RTO on region loss | Write latency | Main difficulty |
|---|---|---|---|---|
| **Single region + backups elsewhere** | Everything in one region; backups copied to another | Hours / hours | Local | Long recovery |
| **Active-passive (warm standby)** | All writes in region A; async replication to B; fail over on disaster | Seconds of data (the replication lag) / minutes | Local in A, far for others | Failover must be practised; the lag is lost |
| **Read-local, write-home** | Every region serves reads from local replicas; writes go to the primary region | As active-passive | One cross-region trip for writers far from home | Read-your-writes after a write (Part 2 §3.2) |
| **Partitioned by user (home region)** | Each user's data lives in their home region; that region is the only writer for it | Only that region's users are affected | Local for each user's own data | Cross-region data (a user messages someone in another region); moving users between regions |
| **Active-active, conflict-tolerant** | Every region accepts writes to the same data; replicate async and merge | ≈ 0 / ≈ 0 | Local | **Conflicts**: needs CRDTs or careful merge rules (Part 2 §3.3, §9) |
| **Active-active, globally consistent** | Consensus spans regions (Spanner, CockroachDB, YugabyteDB) | 0 / seconds | A cross-region quorum on *every* write (Part 2 §5.4) | Latency and cost |

**Worked example: what async replication actually risks.** Region A takes 5,000 writes/s, and replication lag to region B averages 200 ms. If A disappears, B is missing about $5{,}000 \times 0.2 = 1{,}000$ writes. Is that acceptable? For likes, yes. For payments, no. So those need synchronous replication to a second zone or region, or consensus. **The RPO comes straight out of the lag × write rate.**

**Decision guide.**

1. Most products: **one primary region with multiple AZs, plus a CDN, plus a tested DR plan** (active-passive). It covers the large majority of needs.
2. Need low latency *and* data residency: **partition users by home region**. It's the most scalable pattern, because regions rarely coordinate.
3. Must survive a region loss with no data loss and no manual failover, on data with invariants: **globally consistent distributed SQL**, accepting slower writes.
4. Data with no invariants that must be writable everywhere (presence, carts, collaborative documents): **active-active with CRDTs**.

**Hidden costs to name in any multi-region design:** cross-region data transfer fees, running double the capacity, failover that nobody has rehearsed (test it regularly, like backups), global services that quietly live in one region (DNS, auth, config, CI), and the operational load of everything happening twice.

### 5.8 Capacity planning and autoscaling

**The problem.** Too little capacity means outages at the peak. Too much wastes money. And capacity must cover not just normal peaks, but **the peak with something broken**.

**Headroom for failure (N+1 and zone loss).** If you need 10 servers at peak, run at least 11 (**N+1**) so one can fail or be deployed without overload. The same logic at zone level: with traffic spread evenly over $n$ availability zones, losing one zone moves its share onto the survivors. To stay under 100% after losing one zone, normal utilisation must be at most:

$$
U_{\max} = \frac{n - 1}{n}
$$

*The highest safe normal utilisation is the number of surviving zones divided by the number of zones.*

| Zones | Max normal utilisation to survive losing one |
|---|---|
| 2 | 50% |
| 3 | 66.7% |
| 4 | 75% |

That's the ceiling *before* latency is considered. Queueing theory (§4.2) says latency already climbs steeply above about 70–80%. So a 3-zone service typically targets around 50–60% at peak.

**Autoscaling: reactive vs predictive.**

- **Reactive** autoscaling adds capacity when a metric (CPU, requests per instance, queue depth) crosses a threshold. The catch is **lag**: detecting the rise, booting instances, warming caches and runtimes can take minutes. If traffic grows 10% per minute and scale-up takes 5 minutes, demand is $1.1^5 \approx 1.61$ times higher, **61% more**, before the new capacity arrives. Headroom must cover that gap.
- **Predictive / scheduled** scaling adds capacity *before* known patterns (the daily evening peak, a planned launch, a sale). Most real traffic is very regular, so this removes most of the lag risk.
- **Scale on the right signal.** CPU is a poor signal for I/O-bound services. Requests in flight per instance (Little's Law, §4.1) or queue depth usually track load better.
- **Scale-down slowly, scale-up quickly.** That avoids "flapping" (scaling up and down repeatedly).
- **Remember the dependencies.** Doubling the app servers also doubles the database connections (Part 1 §6.6) and the calls to every downstream service. Autoscaling one tier can overload the next.

**Load testing** turns capacity guesses into numbers. Test at the expected peak, at about 2–3× peak, and to breaking point, so you know *where* and *how* the system fails, not just that it fails. §6.7 covers testing more broadly.

---

## 6. Cloud-native infrastructure and observability

### 6.1 Containers and Kubernetes

**The problem.** "It works on my machine." Apps need consistent packaging, and fleets need something to place, restart, scale and connect thousands of processes.

**Containers** package an app with its dependencies into an image. At runtime they're ordinary processes isolated by Linux **namespaces** (separate views of processes, network, filesystem) and limited by **cgroups** (CPU and memory caps). They're lighter than VMs because they share the host kernel, which also makes their isolation weaker. Sandboxes such as gVisor and Firecracker microVMs (used by serverless platforms) add stronger isolation for untrusted code.

**Kubernetes** is built on one idea: **declarative desired state + reconciliation loops.**

1. You declare what you want ("3 replicas of image v2, each with 1 CPU") as API objects, stored in etcd (consensus, Part 2 §7).
2. **Controllers** continuously compare desired state with actual state, and act to close the gap: start a pod, reschedule from a dead node, roll out a new version.
3. The **scheduler** places pods onto nodes based on resource requests, affinity rules and constraints.

Core objects: **Pod** (one or more co-located containers), **Deployment** (rolling updates of stateless pods), **StatefulSet** (stable identity and storage for databases), **Service** (a stable virtual IP and DNS name with load balancing over pods), **Ingress / Gateway API** (L7 entry), **HorizontalPodAutoscaler** (scale on metrics). **Operators** extend the same loop to complex software: a Postgres operator knows how to fail over, back up and upgrade a database.

### 6.2 Serverless

**Functions-as-a-Service** (Lambda, Cloud Run, Cloud Functions) run your code per request or event and scale to zero. You don't manage servers.

- **Gains**: no capacity planning, pay per use, automatic scaling.
- **Costs**: **cold starts** (starting a new instance adds latency, from milliseconds for lightweight runtimes to seconds for heavy ones), execution time limits, statelessness, vendor lock-in, and *higher unit cost at steady high load*. A continuously busy service is usually cheaper on reserved containers. Serverless wins for spiky, event-driven or low-traffic work.

### 6.3 Infrastructure as code, GitOps and deployment strategies

- **Infrastructure as Code** (Terraform/OpenTofu, Pulumi, CloudFormation): infrastructure defined in versioned files, reviewed like code and applied repeatably. Drift detection shows when reality differs from the code.
- **GitOps** (Argo CD, Flux): Git holds the desired state of the cluster; an agent continuously reconciles the cluster to match it. Rollback = `git revert`.

**Deployment strategies** (most outages are caused by changes, so *how* you change matters):

| Strategy | How | Rollback | Risk |
|---|---|---|---|
| **Rolling** | Replace instances a few at a time | Roll forward or back gradually | Old and new versions run together, so they must be compatible (§2.2) |
| **Blue-green** | Stand up a full new environment, switch traffic at once | Instant (switch back) | Double the capacity during the switch; the database schema must suit both |
| **Canary** | Send 1% → 5% → 25% → 100% to the new version, with automated checks on SLIs at each step | Stop and shift back | **Best practice.** Small blast radius, real-traffic validation |
| **Feature flags** | Ship code dark; turn features on per user or percentage at runtime | Flip the flag | Decouples *deploy* from *release*; flags need cleaning up |

**Schema changes** follow **expand → migrate → contract**: add the new column (compatible with old code), deploy code that writes both and reads the new one, backfill, then remove the old column in a *later* release. Never make a breaking schema change in the same step as the code change.

**Migrating to a new data store with zero downtime** (for example, from a single PostgreSQL to a sharded store, or from one service's database to another). This is one of the riskiest operations in enterprise work, and it follows a standard sequence:

1. **Backfill** the new store with a copy of the existing data. Size it first: 1 billion rows at 5,000 rows/s takes about **2.3 days**; at 50,000 rows/s, about **5.6 hours**. Throttle it so production traffic isn't hurt.
2. **Keep the new store in sync** with ongoing writes. Prefer **change data capture** (§3.5) from the old database over application dual-writes, which can diverge whenever one of the two writes fails (Part 2 §8.4).
3. **Shadow reads**: read from both stores, serve the old result, and log any differences. Fix the differences until they're zero.
4. **Cut over reads** gradually (1% → 100%) behind a feature flag, watching errors and latency.
5. **Cut over writes**, often reversing the sync direction so the *old* store stays current as a rollback path.
6. **Decommission** the old store only after a safe period.

Every step is reversible until the last. That's the point: a one-way door (Part 1 §2.5) broken into a series of two-way doors.

### 6.4 eBPF, WebAssembly and platform engineering

- **eBPF** runs small, verified programs *inside the Linux kernel* safely, attached to network events, system calls or functions. It powers high-performance networking and load balancing (Cilium, Meta's Katran), deep observability without code changes (continuous profiling, per-request network tracing), and runtime security (Falco, Tetragon). It's now the foundation of cloud-native networking.
- **WebAssembly (Wasm) on the server**: a portable, sandboxed bytecode that starts in microseconds, with capability-based security through WASI. It's used for plugins (Envoy filters, database UDFs), edge functions, and multi-tenant code isolation that's lighter than containers.
- **Platform engineering**: a dedicated team builds an **internal developer platform**, the paved road of templates, CI/CD, infrastructure and observability defaults, so product teams ship without each rebuilding the stack. The platform is run **as a product**: internal developers are its customers, adoption is earned rather than mandated, and its success is measured by how fast and safely teams ship. A useful split it often makes is **control plane vs data plane**: the control plane (provisioning, configuration, deployment) can be slow and asynchronous, while the data plane (serving requests) must stay up even when the control plane is down.

### 6.5 Cost (FinOps) and carbon as design constraints

In 2026, cost is a first-class non-functional requirement, not an afterthought:

- **Know your unit economics**: cost per request, per user, per GB stored. Track it like latency.
- **The usual big lines**: compute you leave idle, **data egress** (moving data out of a cloud or across regions is often far more expensive than storing it), over-provisioned databases, and log volume.
- **Levers**: right-sizing, autoscaling, spot/preemptible instances for fault-tolerant batch work (often much cheaper), committed-use discounts for the steady baseline, storage tiering (hot → infrequent access → archive), caching to cut egress, and ARM instances.
- **Carbon-aware design**: shift flexible batch work to times and regions with cleaner electricity. Efficiency usually cuts carbon and cost together.

### 6.6 Observability

**The problem.** In a distributed system, "why is checkout slow?" can involve 30 services. You must be able to ask *new* questions of production without shipping new code.

**The signals:**

| Signal | What it is | Best for | Watch out for |
|---|---|---|---|
| **Metrics** | Numeric time series (counters, gauges, histograms) | Dashboards, SLOs, alerts; cheap at any traffic level | **Cardinality**: a label like `user_id` creates millions of series and blows up cost |
| **Logs** | Timestamped event records (structured JSON, ideally) | Detail on specific events, debugging | Volume and cost; sample or tier them |
| **Traces** | The path of one request across services: a tree of **spans** with timings | Finding *where* latency or errors come from | Needs context propagation everywhere; sampling decisions |
| **Profiles** | Where CPU and memory go, continuously | Finding hot code paths in production | Overhead (eBPF-based profilers keep it low) |

**OpenTelemetry (OTel)** is the vendor-neutral standard for producing and shipping all of these: SDKs, auto-instrumentation and the OTel Collector. Traces, metrics and logs are stable. **Profiles** became the fourth signal in public alpha in March 2026, so treat them as early-stage. **Trace context** travels between services in the W3C `traceparent` header, so spans from every service join into one trace.

**Sampling**: **head sampling** decides at the start of a request (cheap, but may drop the interesting traces). **Tail sampling** decides after the request finishes, so it can keep all errors and slow traces (more useful, but it must buffer whole traces).

**What to measure** (two classic checklists):

- **RED** for request-driven services: **R**ate, **E**rrors, **D**uration (latency distribution).
- **USE** for resources (CPU, disk, network, pools): **U**tilisation, **S**aturation (queue length), **E**rrors.
- Google SRE's **four golden signals**: latency, traffic, errors, saturation.

**Alerting philosophy:** page a human only for **symptoms that hurt users** (SLO burn rate), not for causes ("CPU 80%"). Cause-based signals go on dashboards for diagnosis. After incidents, write **blameless postmortems** that focus on how the system allowed the failure, not who triggered it.

**Incident response in one paragraph.** When something breaks: (1) **mitigate first, diagnose later**: roll back the last change, fail over, or shed load, because restoring service beats understanding it; (2) one **incident commander** coordinates while others investigate, so effort doesn't scatter; (3) communicate status on a regular rhythm; (4) afterwards, the postmortem lists contributing causes and *specific* follow-up actions with owners. The best predictor of a fast recovery is a **recent change you can undo**, which is why canaries and feature flags (§6.3) are reliability tools.

### 6.7 Testing and verifying distributed systems

**The problem.** Unit tests check that one function is correct. Most production failures in distributed systems come from *interactions*: two services disagreeing about a contract, a retry storm under load, a timeout that's too long, a failover nobody tried.

| Test type | What it catches | Notes |
|---|---|---|
| **Unit tests** | Logic errors inside one component | Fast; the base of everything |
| **Contract tests** (consumer-driven, such as Pact) | A provider changing an API or event schema that a consumer depends on | Each consumer publishes the expectations it relies on; the provider's build fails if it breaks them. Cheaper and more reliable than full end-to-end tests between teams. |
| **Integration tests** | Wrong assumptions about a real database, queue or cache | Run against real dependencies (often in containers) |
| **End-to-end tests** | Broken critical user journeys | Keep them few: slow and flaky in large numbers |
| **Load and soak tests** | Capacity limits, memory leaks, latency knees (§4.2) | At peak, 2–3× peak, and for hours (soak) |
| **Failure injection / chaos** | Missing timeouts, broken failover, retry storms | Kill nodes, add latency, drop packets (§5.6) |
| **Deterministic simulation** | Rare interleavings in consensus or replication code | Run the whole system in one controllable simulated world (FoundationDB's approach, now used by others) |
| **Production verification** | Everything the above missed | Canaries with automatic SLO checks, synthetic probes, shadow traffic (§6.3) |

**The principle:** you can't test every interaction before release. So test the **contracts** between teams thoroughly, test **failure behaviour** deliberately, and make releases **small and reversible**, so production itself can safely serve as the final test.

---

## 7. Security architecture

This section is about security architecture, from network trust down to the web-application attacks every service must defend against (§7.8).

### 7.1 Zero trust

**The problem.** The old model ("hard shell, soft centre": a firewall outside, everything trusted inside) fails as soon as one internal machine is compromised. The attacker then moves laterally with no resistance.

**How it works** (Google's BeyondCorp; NIST SP 800-207): **never trust the network location; verify every request.**

1. **Strong identity for every user and every workload.** Services get cryptographic identities (SPIFFE/SPIRE IDs, or certificates issued by the service mesh).
2. **mTLS between all services**: encrypted and mutually authenticated.
3. **Authorise each request** using identity, device health and context, against least-privilege policies.
4. **Assume breach**: segment the network, keep credentials short-lived, and log everything for detection.

### 7.2 Authentication: OAuth 2.1, OIDC and passkeys

- **OAuth 2.0** is *delegated authorisation*: letting an app access an API on a user's behalf with **access tokens**. **OpenID Connect (OIDC)** adds *authentication* on top: an **ID token** saying who the user is. They're the basis of "Sign in with…" and of enterprise SSO.
- **OAuth 2.1** consolidates a decade of security lessons. It requires **PKCE** on the authorization-code flow for *all* clients, removes the implicit flow and the password grant, and requires exact redirect-URI matching. **Status:** as of September 2026 it is still an IETF Internet-Draft (revision -16), not yet an RFC, but its rules are already what modern identity providers implement. Design to OAuth 2.1 today.
**The authorization-code flow with PKCE** (how "Sign in with…" works for a web or mobile app):

```mermaid
sequenceDiagram
    participant U as User's browser / app
    participant C as Your app (client)
    participant A as Authorization server
    participant R as API (resource server)
    C->>C: create random code_verifier, hash it into code_challenge
    C->>U: redirect to A with code_challenge
    U->>A: log in (passkey / password + MFA), consent
    A->>U: redirect back with a one-time code
    U->>C: code
    C->>A: exchange code + original code_verifier
    A->>A: check hash(code_verifier) matches code_challenge
    A->>C: access token (short) + refresh token + ID token (OIDC)
    C->>R: API call with the access token
```

Why PKCE matters: the one-time code passes through the browser and can be intercepted (by a malicious app or a leaked redirect). It's useless without the secret `code_verifier`, which never left your app. Only its hash travelled in the first step.

- **Tokens**: keep access tokens short-lived (minutes) and refresh them with **rotating refresh tokens**. Bind tokens to the client where possible (sender-constrained tokens such as DPoP or mTLS) so a stolen token is useless elsewhere.
- **Passkeys (WebAuthn/FIDO2)**: public-key credentials stored on the user's device or synced through their platform's password manager. The private key never leaves the device, and each credential is bound to the site's domain, so **passkeys are phishing-resistant** in a way passwords and SMS codes are not. They're now supported across all major platforms and are the recommended default for consumer sign-in.

### 7.3 Authorization models at scale

| Model | Rule shape | Fits |
|---|---|---|
| **RBAC** (role-based) | User → role → permissions ("editors can edit") | Internal tools, coarse permissions |
| **ABAC** (attribute-based) | Policy over attributes of user, resource, environment ("doctors in ward 3 may read ward-3 records during their shift") | Rich, contextual rules; engines such as OPA/Rego and Cedar |
| **ReBAC** (relationship-based) | Permission follows relationships in a graph ("can view if member of a group that owns the folder that contains the doc") | Sharing models like Google Drive, GitHub orgs |

**Google Zanzibar** (2019) is the reference ReBAC system. It stores relationship tuples (`doc:readme#viewer@group:eng#member`) and answers permission checks across Google's products at millions of checks per second, with low latency. It uses **zookies** (consistency tokens) to avoid the "new enemy" problem: checking a permission against data that's older than a recent revocation. Open-source descendants: **SpiceDB**, **OpenFGA**. Design principle: **centralise authorisation decisions in one service with one model**, rather than scattering `if user.is_admin` checks across services.

### 7.4 Secrets, encryption and keys

- **Secrets management** (Vault, cloud secret managers): no secrets in code or images. Inject them at runtime, rotate them automatically, and prefer **dynamic, short-lived credentials** (a database password valid for one hour) over long-lived ones.
- **Encryption in transit** (TLS/mTLS everywhere) and **at rest**.
- **Envelope encryption** is how at-rest encryption scales: each object is encrypted with its own random **data key (DEK)**. The DEK is encrypted by a **key-encryption key (KEK)** that never leaves the **KMS/HSM**. The object is stored with its *encrypted* DEK. To read it, ask the KMS to decrypt the DEK (one small, audited, rate-limited call), then decrypt the data locally. Rotating the KEK means re-wrapping small DEKs, not re-encrypting petabytes. Deleting one user's key makes their data unrecoverable (**crypto-shredding**, useful for GDPR erasure).

### 7.5 Supply chain security

**The problem.** Modern apps are mostly *other people's code*: hundreds of dependencies, base images and CI actions. Attacks now target that chain (the SolarWinds build compromise in 2020; the xz-utils backdoor discovered in 2024).

**Defences:**

- **SBOM** (software bill of materials, in SPDX or CycloneDX format): an inventory of every component in each artifact, so you can answer "are we affected by this CVE?" in minutes.
- **SLSA** (Supply-chain Levels for Software Artifacts): a framework of build-integrity levels. Builds run on hardened, isolated builders and produce signed **provenance** (what source, which builder, what steps).
- **Sigstore** (cosign, Fulcio, Rekor): keyless signing of artifacts tied to an identity, recorded in a public transparency log. Deployments verify signatures before running anything.
- Pin dependencies by hash, review upgrades, scan continuously, and give CI tokens least privilege.

### 7.6 Post-quantum readiness and multi-tenancy

- **Post-quantum cryptography**: as Part 1 §4.5 described, the browser default is now hybrid `X25519MLKEM768` key exchange. The next steps for system designers: inventory where your systems use public-key crypto, make sure your TLS stack (for example OpenSSL 3.5+) negotiates the hybrid groups, and plan the slower migration to post-quantum **signatures** (ML-DSA, FIPS 204) for certificates, code signing and tokens. The goal is **crypto-agility**: being able to swap algorithms without redesigning.
- **Multi-tenancy isolation** (one platform, many customers): choose per tier, from shared tables with a `tenant_id` on every row (cheapest; enforce it with row-level security) to a schema per tenant to a database or cell per tenant (strongest isolation; noisy neighbours can't hurt others; most expensive). Tenant context must flow through every layer: caches, queues, logs, search indexes.

### 7.7 Privacy and compliance by design

**The problem.** Privacy laws (the EU's GDPR, California's CCPA/CPRA and many similar laws) put legal requirements on how personal data is stored, moved and deleted. Bolting these onto a finished system is extremely expensive: "delete this user" across 40 services, their caches, logs, backups and analytics copies is a project in itself. They have to be design inputs.

**How it works: the design consequences.**

1. **Know your data.** Classify fields (public / internal / confidential / restricted) and mark **PII** (personally identifiable information: names, emails, IPs, device IDs, location). Keep a **data map**: which systems hold which personal data, and why. You can't delete or export what you can't find.
2. **Minimise.** Don't collect what you don't need, and set **retention periods** with automatic deletion (TTLs, partition drops). Data you never stored can't leak or be subpoenaed.
3. **Right of access and portability.** A user can ask for all their data. Design a per-user export path across services, usually an internal API that each service implements, keyed by user ID.
4. **Right to erasure.** Deletion must reach the primary databases, caches, search indexes, event logs, analytics, ML training data, logs and backups. Techniques: deletion events that every service consumes (and confirms), short retention on logs, and **crypto-shredding** (§7.4: encrypt each user's data with a per-user key, and delete the key to make every copy unreadable, including the copies inside backups).
5. **Data residency.** Some data must stay in a jurisdiction (EU data in the EU). Partition users by region with region-local storage, which fits cell-based architecture (§5.6). Watch the side channels that quietly copy data abroad: logs, analytics, support tools, third-party SDKs and external LLM APIs.
6. **Pseudonymisation vs anonymisation.** Replacing names with IDs (pseudonymisation) is reversible with the mapping, so it's still personal data under GDPR. True anonymisation is hard: Latanya Sweeney showed that ZIP code + birth date + gender alone uniquely identifies about 87% of Americans. Aggregate, add noise (differential privacy), or treat the data as personal.
7. **Keep PII out of logs and prompts.** Redact at the logging library and at the LLM gateway (§9.6). Logs are the most common accidental PII store.

**Audit logs** record who did what, to which record, when and from where. Especially: access to sensitive data, permission changes and admin actions. Make them **append-only**, stored separately from the system they audit, and **tamper-evident**: each entry includes a hash of the previous entry, so editing or deleting any entry breaks the chain from that point on (the same idea as a Merkle tree, Part 2 §10.4).

**Other regimes you'll meet:** PCI DSS (card data; keep your scope small by letting a payment provider handle cards, Part 4 §4), HIPAA (US health data), SOC 2 (a security-controls audit that B2B customers ask for), and the EU AI Act, whose obligations for AI systems are phasing in. The design moves are the same each time: know where the data is, minimise it, control and log access, and be able to delete it.

### 7.8 Web application security essentials

**The problem.** Most real breaches don't defeat cryptography. They exploit an ordinary bug: a missing permission check, a query built from user input, a misconfigured bucket. The **OWASP Top 10** is the industry's ranked list of these risks. The **2025 edition** is:

| Rank | Category (OWASP Top 10:2025) | The design defence |
|---|---|---|
| A01 | **Broken Access Control** (now also includes SSRF) | Check authorisation on *every* request, for *the specific object*, on the server |
| A02 | Security Misconfiguration | Secure defaults, infrastructure as code, automated config scanning |
| A03 | **Software Supply Chain Failures** (new) | SBOMs, signed builds, pinned dependencies (§7.5) |
| A04 | Cryptographic Failures | TLS everywhere, managed keys (§7.4), no home-made crypto |
| A05 | Injection | Parameterised queries, never string-built commands |
| A06 | Insecure Design | Threat modelling at design time, which is this guide's whole point |
| A07 | Authentication Failures | Passkeys/MFA, rate-limited logins, safe session handling (§7.2) |
| A08 | Software or Data Integrity Failures | Verify signatures on updates and artifacts; don't deserialise untrusted data |
| A09 | Security Logging & Alerting Failures | Audit logs (§7.7), alerts on suspicious patterns |
| A10 | **Mishandling of Exceptional Conditions** (new) | Fail *closed* on errors in security checks; don't leak internals in error messages |

**The attacks every system designer must be able to explain:**

- **Broken object-level authorisation** (often called IDOR). `GET /invoices/1043` returns invoice 1043 to *any* logged-in user, because the code checked "is logged in" but not "owns invoice 1043". It's the most common serious API bug. **Defence:** every data access checks ownership or permission for that specific object, ideally through one central authorisation service (§7.3). Unguessable IDs (Part 1 §6.7) are a second layer, not a fix.
- **Injection.** User input concatenated into SQL (or a shell command, or an LLM prompt, §9.5) becomes code. `'; DROP TABLE users; --` is the classic. **Defence:** parameterised queries or prepared statements, so input is always treated as data.
- **Cross-site scripting (XSS).** Attacker-supplied text is shown on a page *as HTML*, so their script runs in other users' browsers and can steal tokens or act as them. **Defence:** context-aware output encoding (modern frameworks do it by default; avoid raw-HTML escape hatches), a Content Security Policy header, and keeping session tokens in `HttpOnly` cookies that scripts can't read.
- **Cross-site request forgery (CSRF).** A malicious site makes the *user's own browser* send a request to your site, and the browser attaches the user's cookies automatically. **Defence:** `SameSite=Lax` or `Strict` cookies (the modern baseline), plus anti-CSRF tokens on state-changing forms.
- **CORS is not a CSRF defence.** CORS controls which *other origins' JavaScript may read your responses*. It loosens the browser's same-origin policy; it doesn't stop requests being sent. Configure it narrowly (exact allowed origins, never `*` with credentials).
- **Server-side request forgery (SSRF).** Your server fetches a URL the user supplied ("import from URL", webhooks, link previews), and the attacker points it at internal addresses, especially the **cloud metadata endpoint**, which can hand out credentials. **Defence:** allow-lists of destinations, blocking private and link-local address ranges, a separate egress proxy, and the hardened metadata service (AWS IMDSv2 requires a session token).
- **DDoS.** *Volumetric* floods (huge traffic) are absorbed by anycast CDNs and cloud scrubbing networks (Part 1 §4.6). *Application-layer* floods (expensive requests that look legitimate) need rate limiting (Part 4 §2), a **WAF** (web application firewall rules at the edge), caching, and load shedding (§5.3).

---

## 8. Data and analytics systems

### 8.1 OLTP vs OLAP

| | **OLTP** (transactions) | **OLAP** (analytics) |
|---|---|---|
| Queries | Many small reads and writes by key | Few huge scans and aggregations |
| Data per query | A few rows | Millions to billions of rows, few columns |
| Users | End users through the app | Analysts, dashboards, ML pipelines |
| Storage layout | **Row-oriented** + B-tree indexes (Part 1 §6) | **Column-oriented** + compression |
| Examples | PostgreSQL, MySQL, DynamoDB | Snowflake, BigQuery, Redshift, ClickHouse, DuckDB |

### 8.2 Why columnar storage wins for analytics

**The problem.** `SELECT country, SUM(revenue) FROM sales GROUP BY country` over a 100-column table. A row store reads every column of every row from disk.

**How it works.** A **column store** keeps each column's values together. The query reads **only the 3 columns it needs**: 3/100 = **3% of the I/O**. Values in one column are similar, so they compress extremely well (run-length encoding, dictionary encoding, bit-packing), often 5–10×. And **vectorised execution** processes batches of a column with SIMD CPU instructions. Combined, analytic scans can be orders of magnitude faster. The open file formats are **Parquet** and **ORC**.

### 8.3 Warehouse, lake, lakehouse

- **Data warehouse**: structured, cleaned, schema-on-write data in a managed columnar engine. Fast and governed, but storage and compute are coupled to the vendor.
- **Data lake**: raw files of any kind (Parquet, JSON, images) dumped on cheap object storage. Flexible and cheap, but it became a "data swamp": no transactions, no schema enforcement, unclear "current" state.
- **Lakehouse**: open **table formats** (Apache **Iceberg**, Delta Lake, Apache Hudi) add a **metadata layer** on top of Parquet files in object storage. That layer gives you ACID transactions (via atomic swaps of metadata pointers), schema evolution, **time travel** (query a past snapshot), and partition pruning. Many engines (Spark, Trino, Flink, Snowflake, DuckDB…) can then read and write *the same tables*. In 2026, Iceberg has become the de-facto interoperable table format, supported by all the major warehouses and clouds. Its **v3 spec** (generally available in major warehouses during 2026) adds *deletion vectors*, compact bitmaps of deleted rows that make updates and deletes much cheaper, and *row lineage*, row IDs that make change data capture from the lake easier. Engine support for v3 was still uneven in 2026, and upgrading a table is one-way, so check every engine that reads it before you upgrade.

### 8.4 Batch and stream processing architectures

- **Batch**: MapReduce (Google, 2004) introduced **map → shuffle → reduce** over a distributed filesystem, with fault tolerance by re-running failed tasks. **Spark** generalised it: in-memory datasets, a DAG of transformations, SQL. Batch is simple to reason about and can be recomputed from scratch.
- **Lambda architecture**: run a **batch layer** (accurate, slow) and a **speed layer** (approximate, real-time) side by side, and merge them at query time. It works, but you maintain *two* codebases for the same logic.
- **Kappa architecture** (Jay Kreps, 2014): **everything is a stream**. Keep the log (Kafka) long enough, process with a stream processor, and "reprocess" by replaying the log through a new version of the job. One codebase. It became the default as stream processors matured (§3.6).
- **Real-time OLAP** (ClickHouse, Apache Druid, Apache Pinot) ingests streams and answers analytical queries in sub-seconds, for user-facing analytics ("your post's views in the last hour").

### 8.5 Data mesh and data contracts

- **Data mesh** (Zhamak Dehghani): an *organisational* pattern. Domain teams own their data as **products** (documented, quality-checked, discoverable), on a shared self-serve platform with federated governance. It addresses the bottleneck of one central data team owning every pipeline.
- **Data contracts**: explicit, versioned agreements between data producers and consumers (schema, meaning, freshness and quality guarantees), enforced in CI and at ingestion. They're the data-world version of API contracts (§2.2). They stop an upstream column rename from silently breaking 40 dashboards.

---

## 9. AI and LLM systems

AI features are now ordinary parts of system design, with their own physics. The model is one component. The system around it (retrieval, serving, caching, evaluation, guardrails) decides quality, latency and cost.

### 9.1 Classic ML systems in one page

- **Training vs serving.** Offline pipelines train models on historical data; online services serve predictions with low latency.
- **Feature stores** keep features consistent between the two: an **offline store** (historical, for training) and an **online store** (low-latency key-value, for serving), computed from the same definitions. The problem they prevent is **training/serving skew**: a model trained on features computed one way and served with features computed another way silently degrades.
- **Recommendation systems** run as a **funnel**: *candidate generation* (cheap retrieval of thousands of items from millions, often via embeddings and ANN search) → *ranking* (an expensive model scores hundreds) → *re-ranking* (business rules, diversity, freshness) → a dozen shown to the user.
- **Monitoring**: data drift and concept drift, delayed ground truth, and A/B tests on business metrics (not just offline accuracy).

### 9.2 LLM inference: prefill, decode and the memory wall

**The problem.** An LLM generates text one token at a time, and every token needs the entire model's weights to be read from GPU memory. Serving many users fast and cheaply is a hardware-physics problem.

**How it works.** A request has two phases:

1. **Prefill**: process the whole prompt in parallel. This is **compute-bound** (big matrix multiplications) and sets **time to first token (TTFT)**.
2. **Decode**: generate output tokens one by one. Each step reads all the weights *and* the attention state of all previous tokens, to produce one token per sequence. This is **memory-bandwidth-bound**. It sets **time per output token (TPOT)**.

**Worked example: the decode speed limit.** Assume a 70B-parameter model in FP16 (2 bytes per parameter) = **140 GB of weights**, split across 2 GPUs with about 3.35 TB/s of memory bandwidth each (6.7 TB/s total, H100-class). Each decode step must stream all 140 GB, so for a single sequence:

$$
\text{tokens/s} \leq \frac{\text{memory bandwidth}}{\text{bytes of weights}} = \frac{6.7 \times 10^{12}}{1.4 \times 10^{11}} \approx 48
$$

*A single sequence can generate at most bandwidth divided by model size tokens per second.* The GPUs' arithmetic units sit mostly idle. **The fix is batching**: one pass over the weights can serve *many* sequences at once, so throughput grows almost linearly with batch size, until something else runs out. That something is the **KV cache**.

### 9.3 The KV cache: why memory limits batch size

**The problem.** To avoid recomputing attention over all previous tokens at every step, the model caches each token's **keys and values** for every layer. That cache grows with every token of every concurrent request.

$$
\text{KV bytes per token} = 2 \times n_{\text{layers}} \times n_{\text{kv heads}} \times d_{\text{head}} \times \text{bytes per value}
$$

*Per token you store a key and a value (the 2), for every layer, for every key-value head, each of the head's dimension, at the chosen precision.*

**Worked example** (an assumed 70B-class shape: 80 layers, head dimension 128, FP16, with grouped-query attention using 8 KV heads):

- Per token: $2 \times 80 \times 8 \times 128 \times 2 = 327{,}680$ bytes = **320 KiB**.
- One request with an 8K-token context: 320 KiB × 8,192 = **2.5 GiB**. At 128K context: **40 GiB**.
- On 2 × 80 GB GPUs, after 140 GB of weights about 20 GB is left: **only about 7 concurrent 8K-token requests** fit.
- Without grouped-query attention (64 KV heads, classic multi-head), it would be 2,560 KiB per token, 8× worse.

![Fig 12 – KV cache memory (fig12_kv_cache.png): KV cache size per request against context length, for 64 and 8 KV heads, against the roughly 20 GB left after FP16 weights on two 80 GB GPUs.](images/fig12_kv_cache.png)

*Fig 12 (fig12_kv_cache.png). Assumed model shape, back-of-envelope. The point: long contexts and many users compete for the same GPU memory. Architectures that shrink the KV cache translate directly into more users per GPU: **grouped-query attention** (several query heads share one key-value head, so fewer KV heads are stored) and **multi-head latent attention** (introduced by DeepSeek: it caches one small compressed vector per token and rebuilds keys and values from it when needed).*

**The serving techniques that follow from this physics:**

| Technique | Problem solved | Idea |
|---|---|---|
| **Continuous batching** (Orca, 2022) | Static batches wait for their longest sequence | Add and remove sequences from the batch at *every* decode step |
| **PagedAttention** (vLLM, 2023) | KV memory fragmentation wasted much of the cache | Store the KV cache in fixed-size blocks like OS virtual-memory pages; allocate on demand; share blocks between requests |
| **Prefix caching** | The same long system prompt is recomputed for every request | Reuse KV blocks for shared prefixes (also sold as "prompt caching" by API providers) |
| **Quantisation** (FP8, INT4) | Weights and KV take too much memory and bandwidth | Fewer bytes per value: more speed and more capacity, with a small quality cost to measure |
| **Speculative decoding** | One token per expensive step | A small draft model proposes several tokens; the big model verifies them in one pass |
| **Disaggregated prefill/decode** | Compute-bound and memory-bound phases interfere | Run prefill and decode on separate GPU pools and transfer the KV cache between them. In production by 2026 (NVIDIA Dynamo, Mooncake, DeepSeek); it trades simplicity for more predictable latency |
| **Model routing** | Using the largest model for everything is slow and costly | Send easy requests to small, cheap models and hard ones to big models |

Serving engines: vLLM, SGLang, TensorRT-LLM, and the managed APIs. The metrics to set SLOs on are **TTFT**, **TPOT** (or tokens/s per user), throughput (tokens/s per GPU), and **cost per million tokens**.

### 9.4 Retrieval-augmented generation (RAG) and vector search

**The problem.** Models don't know your private or recent data, and they make things up when they're unsure. You want answers grounded in *your* documents, with citations.

**How it works.**

```mermaid
flowchart LR
    accTitle: RAG pipeline
    accDescr: Offline, documents are chunked, embedded and indexed. Online, the query goes to hybrid retrieval, reranking, prompt assembly, the LLM, and a cited answer.
    subgraph off ["Offline indexing"]
        D["Documents"] --> CH["Chunk<br/>(~200–1000 tokens)"] --> EM["Embed each chunk"] --> IDX[("Vector index (HNSW)<br/>+ keyword index (BM25)")]
    end
    subgraph on ["Online query"]
        Q(["User question"]) --> HY["Hybrid retrieval<br/>vector + BM25, fused"] --> RR["Rerank top 50<br/>cross-encoder"] --> PR["Prompt with top 5–10<br/>chunks + instructions"] --> LLM["LLM"] --> A(["Answer with citations"])
    end
    off --> on
    class D,Q primary;
    class CH,EM,HY,RR,PR,LLM intermediate;
    class IDX,A target;
    classDef primary fill:#EFF6FF,stroke:#2563EB,stroke-width:1.5px,color:#0F172A;
    classDef intermediate fill:#FAF5FF,stroke:#7C3AED,stroke-width:1.5px,color:#0F172A;
    classDef target fill:#F0FDF4,stroke:#059669,stroke-width:2px,color:#0F172A;
```

1. **Chunking**: split documents into passages that fit the embedding model and carry one idea each. Use overlap or structure-aware splits (headings, paragraphs), and keep metadata (source, date, permissions).
2. **Embedding**: map each chunk to a vector (hundreds to a few thousand dimensions) where similar meanings are close together.
3. **Hybrid retrieval**: vectors find *semantic* matches but miss exact terms (product codes, names). Keyword search (**BM25**, explained in Part 1 §7.7) catches those. Run both and fuse the rankings, commonly with **reciprocal rank fusion**: score $= \sum 1/(k + \text{rank})$ across the lists.
4. **Reranking**: a cross-encoder scores (question, chunk) pairs jointly. That's much more accurate than vector similarity, but too slow for millions of chunks, so it's applied only to the top few dozen.
5. **Generation** with instructions to answer only from the context and to cite sources.
6. **Enforce permissions at retrieval time** (filter by the user's access rights). Otherwise RAG becomes a data-leak engine.

**Vector indexes (approximate nearest neighbour):**

- **HNSW** (hierarchical navigable small world graphs): a layered graph you search greedily from coarse to fine. Search cost is roughly logarithmic, recall is high, and it's the default almost everywhere. The cost is memory (the graph plus full vectors in RAM).
- **IVF** (inverted file): cluster the vectors (k-means) and search only the closest few clusters.
- **Product quantisation (PQ)**: compress each vector into a few bytes by quantising sub-vectors.

**Worked example: memory.** 10 million chunks × 1,024 dimensions × 4 bytes (FP32) = **40.96 GB** of raw vectors, before the index. With PQ at 64 bytes per vector: 10M × 64 = **640 MB**, a 64× reduction, at some loss of recall (usually recovered by re-scoring the top candidates with full vectors). Trade-off triangle: **recall vs latency vs memory**.

### 9.5 Agents, tools and MCP

**The problem.** Many tasks need multiple steps, actions and external data: "find the failing test, fix it, open a PR". A single prompt-response can't do that.

**How it works.** An **agent** is an LLM in a loop: decide → call a **tool** (search, code execution, an API) → observe the result → decide again, until done. The system around the loop (the **harness**) matters as much as the model. The harness decides:

- **What goes into the context** each step: instructions, relevant files, tool results, summaries of earlier steps. The context window is limited and expensive, so choosing what to include is the core engineering problem.
- **Which tools exist and how they're described**: few, clear, well-named tools beat many overlapping ones.
- **How work is structured**: a free loop, or an explicit graph of steps (plan → split into parallel sub-tasks → check → merge) where the order is known in advance. Explicit graphs are easier to test, parallelise and debug. Free loops handle open-ended tasks. Many systems combine both.
- **How results are verified**: tests, linters, a second model checking the first, and **human approval gates** before irreversible actions.

System-design concerns specific to agents:

- **Tool protocols**: the **Model Context Protocol (MCP)** standardises how agents discover and call tools and data sources. Anthropic introduced it in 2024 and donated it in December 2025 to the **Agentic AI Foundation** under the Linux Foundation; it's supported across the major AI clients and platforms. It's a client-server protocol, so one MCP server (for your database, ticketing system or docs) works with many agent clients. Design tools like APIs: clear schemas, idempotent where possible, least-privilege credentials.
- **Agent-to-agent protocols**: **A2A** (Agent2Agent), launched by Google in 2025 and governed by the Linux Foundation since June 2025, covers a different layer: *agents calling other agents* (discovery through "agent cards", task hand-off, streaming status), possibly across companies. Rule of thumb: **MCP connects an agent to tools and data; A2A connects agents to each other.**
- **Durability**: agent runs can take minutes to hours. Run them on durable execution (§3.7) so a crash resumes instead of restarting, with checkpoints and human approval steps for risky actions.
- **Memory**: short-term (the context window, compacted or summarised as it fills) and long-term (facts extracted from conversations, stored in a database or vector store, and retrieved when relevant, with the same hybrid retrieval as RAG, §9.4). Long-term memory needs the same care as any user data: deletion, privacy (§7.7), and handling of facts that become outdated.
- **Security**: **prompt injection** is the defining threat. Text inside a retrieved web page, email or file can contain instructions the model may follow. Defences are architectural: treat all tool output as untrusted data, give agents least-privilege and scoped credentials, require confirmation for irreversible actions, isolate code execution in sandboxes, and filter outputs that could exfiltrate data (such as URLs with embedded secrets).
- **Cost and loop control**: budget limits on steps, tokens and wall time; detection of loops that repeat the same failing action.

### 9.6 The LLM platform layer: gateways, caching, evals and guardrails

- **LLM gateway**: one internal entry point to all model providers. It handles authentication, per-team quotas and budgets, routing and **fallback** between models and providers, retries with backoff, logging, and PII redaction. It's an API gateway (Part 1 §5.2) specialised for tokens.
- **Caching**: *exact* response caching for repeated prompts; provider **prompt/prefix caching** for long shared prefixes (cheaper and faster TTFT); **semantic caching** (return a cached answer when a new question's embedding is close to a past one). Semantic caching is risky, because "close" questions can need different answers, so use it only for narrow, low-risk domains with conservative thresholds.
- **Evaluations (evals)**: you can't unit-test free text with `assertEquals`. Build eval sets of real tasks with graded expectations: exact checks where possible, rubric-based **LLM-as-judge** where not (calibrated against human labels). Run them in CI on every prompt or model change, like a regression suite, and monitor production samples continuously. **Evals are the test suite of AI systems.**
- **Guardrails**: input and output classifiers (safety, PII, off-topic), structured-output validation (JSON schema), groundedness checks for RAG, and rate limits against abuse.
- **Observability**: trace every step (prompt, retrieved chunks, tool calls, tokens, latency, cost) with OpenTelemetry's generative-AI conventions or dedicated LLM tracing tools. Without traces, agent failures are impossible to debug.

### 9.7 Decision guide: how to add AI to a system

**First question: should this be an LLM at all?** LLMs are slow (hundreds of ms to seconds), costly per call, and non-deterministic. If the task has a precise rule ("is this a valid email?", "sum the invoice"), use ordinary code. LLMs earn their place on fuzzy language tasks: understanding, summarising, extracting from messy text, drafting, answering questions over documents, and multi-step tool use.

**Second question: how does the model get the knowledge or behaviour it needs?**

| Approach | Use when | Strengths | Weaknesses |
|---|---|---|---|
| **Prompting** (instructions + examples) | The model already knows how; it just needs direction | Instant to change; no training | Limited by context; behaviour can drift with model updates (catch it with evals) |
| **Long context** (put the documents in the prompt) | The relevant material is small (tens to a few hundred pages) and changes often | Simple; no retrieval pipeline | Cost and latency grow with every token on every call (§9.3); prompt caching helps |
| **RAG** (§9.4) | Large or fast-changing knowledge; citations needed; per-user permissions | Fresh, traceable, scales to millions of documents | Retrieval quality is the ceiling; more moving parts |
| **Fine-tuning** | A consistent *style, format or skill* is needed, or a small model must do a narrow task well and cheaply | Shorter prompts, cheaper inference, consistent output | Needs good training data; knowledge goes stale; must retrain to update |
| **Agents** (§9.5) | Multi-step tasks needing actions and observation | Handles open-ended work | Hardest to make reliable, secure and affordable |

**The usual progression:** start with prompting plus a strong eval set (§9.6). Add RAG when knowledge is the gap. Fine-tune when cost or consistency at volume is the gap. Reach for agents only when the task truly needs multiple steps with actions. Common mistakes are fine-tuning to add *facts* (use RAG instead; fine-tuned facts go stale and can't be cited) and building an agent where a fixed pipeline would be more reliable.

**Third question: what happens when the model is wrong?** Design for it. Show sources so users can check, keep a human in the loop for consequential actions, constrain outputs with schemas, and measure error rates with evals before and after every change. A model being wrong some of the time is a given; a system that hides it is a design failure.

---

## 10. Architecture patterns

### 10.1 Monolith, modular monolith, microservices

| | **Monolith** | **Modular monolith** | **Microservices** |
|---|---|---|---|
| Deploy unit | One | One, with strictly enforced internal module boundaries | Many independently deployable services |
| Calls between parts | In-process function calls | In-process, through module interfaces | Network calls (latency, partial failure, Part 2) |
| Data | One shared database | One database, schemas owned per module | **Database per service** |
| Strength | Simple to build, test, debug and deploy | Simplicity *plus* clear boundaries, ready to split later | Independent scaling, deploys and team autonomy |
| Weakness | Boundaries erode; one team's change can break everyone | Discipline needed to keep boundaries | Distributed-systems complexity; needs strong platform and observability |
| Fits | Small teams, new products | **Most companies' best default** | Many teams, a mature platform, parts with very different scaling needs |

**The key insight:** microservices solve an **organisational** scaling problem (many teams stepping on each other) at the price of a **technical** one (distributed systems). Several well-known companies have publicly moved parts of their systems *back* toward monoliths when the price outweighed the benefit. Start modular; split out a service when a boundary is stable *and* there's a concrete reason (scaling profile, team ownership, release cadence).

### 10.2 Domain-driven design and boundaries

- **Bounded context**: a part of the business with its own consistent model and language. "Customer" means something different in Billing (a payment method, invoices) and in Support (tickets, satisfaction). Don't force one shared model on both. **Service boundaries should follow bounded contexts.**
- **Aggregate**: a cluster of objects that must be consistent together (an order and its line items), changed only through its root, inside one transaction. Cross-aggregate consistency is eventual (events, sagas). This maps naturally onto partitions and transaction boundaries.
- **Hexagonal architecture (ports and adapters)**: business logic sits at the centre with no dependency on frameworks or databases. Adapters plug into ports: REST controllers in, database repositories out. It makes the core testable and the infrastructure swappable.

### 10.3 Migration and integration patterns

- **Strangler fig**: replace a legacy system gradually. Put a routing layer in front, move one capability at a time to the new system, and route its traffic there, until the old system is "strangled" and can be removed. It avoids the risky big-bang rewrite.
- **Anti-corruption layer**: a translation layer between your clean model and a legacy or external system's messy one, so their concepts don't leak into yours.
- **Backend for frontend (BFF)**: a thin backend per client type (web, iOS, TV) that aggregates and shapes data for exactly that client.
- **Sidecar / ambassador**: deploy cross-cutting helpers (proxy, telemetry agent, secrets fetcher) as a separate process beside each service, as the service mesh does.

### 10.4 Conway's Law

> "Organizations which design systems are constrained to produce designs which are copies of the communication structures of these organizations." (Melvin Conway, 1968)

Your architecture will mirror your org chart, whether you plan it or not. The **inverse Conway manoeuvre** uses this deliberately: shape the teams (*Team Topologies*' stream-aligned teams, platform teams, enabling teams) to match the architecture you want. A design that cuts across team boundaries will be hard to build and harder to own.

---

## 11. The design method, applied to three systems

### 11.1 A repeatable framework

```mermaid
flowchart LR
    accTitle: System design method
    accDescr: Eight steps from requirements through estimates, API, data model, high-level design, deep dives, failure modes and evolution.
    R["1. Requirements<br/>functional + NFRs"] --> E["2. Estimates<br/>QPS, storage, bandwidth"]
    E --> A["3. API<br/>key operations"]
    A --> D["4. Data model<br/>entities, access patterns"]
    D --> H["5. High-level design<br/>boxes and arrows"]
    H --> DD["6. Deep dives<br/>the 2–3 hardest parts"]
    DD --> F["7. Failure modes<br/>what breaks, blast radius"]
    F --> EV["8. Evolution<br/>10x growth, trade-offs named"]
    class R,E primary;
    class A,D,H,DD intermediate;
    class F warning;
    class EV target;
    classDef primary fill:#EFF6FF,stroke:#2563EB,stroke-width:1.5px,color:#0F172A;
    classDef intermediate fill:#FAF5FF,stroke:#7C3AED,stroke-width:1.5px,color:#0F172A;
    classDef warning fill:#FFFBEB,stroke:#D97706,stroke-width:1.5px,color:#92400E;
    classDef target fill:#F0FDF4,stroke:#059669,stroke-width:2px,color:#0F172A;
```

1. **Requirements**: ask before drawing. Who uses it, what are the core operations, what scale, what latency, what consistency, what can be lost?
2. **Estimates** (Part 1 §2.3): enough to know which parts need scaling.
3. **API**: the handful of key operations and their shapes.
4. **Data model**: entities, relationships and *access patterns*, which decide the database (Part 1 §7).
5. **High-level design**: the simplest architecture that meets the requirements.
6. **Deep dives**: the hardest 2–3 parts (the hot path, the consistency-critical part, the biggest scale).
7. **Failure modes**: for each component, what happens when it dies, slows down or partitions?
8. **Evolution**: what breaks at 10×, and which trade-offs you made on purpose.

### 11.2 Worked design 1: URL shortener

**Requirements.** Create a short link for a long URL; redirect from it quickly; links last years. NFRs: redirect p99 < 50 ms; very high availability for reads; 100M new links per day; reads 100× writes.

**Estimates.**

| Quantity | Calculation | Result |
|---|---|---|
| Writes | 100M / 86,400 | **≈ 1,160/s** |
| Reads | 100 × writes | **≈ 116,000/s** |
| Storage, 10 years | 500 bytes × 100M × 365 × 10 | **≈ 183 TB** |
| Codes needed in 10 years | 100M × 3,650 | 365 billion |
| 7-character base-62 codes | $62^7$ | **3.52 trillion** ✓ (enough; 6 chars = 56.8 billion is not) |

**API.** `POST /links {long_url}` → `{code}`; `GET /{code}` → redirect.

**The deep dive: generating unique codes.**

| Option | How | Trade-off |
|---|---|---|
| Hash the URL (e.g. first 7 base-62 chars of a SHA-256) | Deterministic | Collisions must be detected and retried; the same URL always gets the same code (sometimes wanted, sometimes not) |
| Global counter → base-62 | Unique by construction | A single counter is a bottleneck and a single point of failure; codes are guessable (enumerable) |
| **Counter ranges** | Each app server leases a block of 1M IDs from a coordination store (etcd or a DB row), then hands them out locally | No per-request coordination; a crash only wastes the unused part of a block |
| **Snowflake-style IDs** | 64 bits = 41-bit millisecond timestamp + 10-bit machine ID + 12-bit sequence | No coordination at all; 4,096 IDs per ms per machine; time-ordered; 41 bits of ms lasts about 69.7 years. Codes are longer (up to 11 base-62 chars) |

**Design.** Stateless app servers behind a load balancer; a key-value store or a sharded database keyed by `code` (a pure key lookup, hash-partitioned); a cache in front (popular links are extremely skewed, so the hit ratio is high); a CDN or edge layer for the hottest redirects. Use a **302** (temporary) redirect if you need click analytics, because browsers cache 301s and skip your server. Analytics are written **asynchronously** (log → Kafka → analytics store), never on the redirect's critical path.

**Failure modes.** The cache cluster dies → the DB must survive the read load, or the edge keeps serving stale entries. The ID lease store is down → servers continue on already-leased blocks. Abuse → rate-limit creation and scan target URLs for malware.

### 11.3 Worked design 2: news feed

**Requirements.** Users follow others; their home feed shows recent posts from people they follow, ranked. NFRs: feed load p99 < 200 ms; posting can take a little longer; a feed can be a few seconds stale. Using Part 1 §2.3's numbers: about 7k posts/s and about 350k feed reads/s on average.

**The deep dive: fan-out.**

- **Fan-out on write (push)**: when a user posts, insert the post ID into every follower's precomputed feed (in a cache or wide-column store). Reads are trivial: fetch your feed list. **Problem: celebrities.** A user with 100M followers produces 100M writes per post. At 1M feed inserts/s, that single post takes **100 seconds** to propagate and eats the whole write capacity.
- **Fan-out on read (pull)**: at read time, fetch recent posts from everyone you follow and merge them. Writes are trivial, but reads are expensive (a scatter/gather over hundreds of followees, with the tail-latency problem from §4.3).
- **Hybrid (what large platforms do)**: push for ordinary users; **pull for celebrities**. At read time, merge your precomputed feed with fresh posts from the few celebrities you follow. The threshold (for example, over 100k followers) is a tunable trade-off.

**Design.** A post service writes posts to a sharded store (by `post_id`) and emits `PostCreated` events to Kafka. Fan-out workers consume the events and update follower feed lists (keep only the latest ~1,000 IDs per user, in Redis or a wide-column store). The feed service reads the feed list, merges celebrity posts, **hydrates** IDs into full posts (cached heavily), then **ranks** them with an ML model (the candidate → rank funnel from §9.1). Media goes in object storage behind a CDN.

**Failure modes.** A lagging fan-out → feeds are a bit stale, which is acceptable by the NFRs. Hot posts → cache and replicate their hydration. A new user with no feed cache → build it on the fly by pulling.

### 11.4 Worked design 3: chat system

**Requirements.** One-to-one and group messaging; online delivery in under a second; offline users get messages later (and push notifications); messages ordered within each conversation; message history; presence (online/offline). Scale: 100M concurrent connections at peak.

**Connections.** Clients hold a persistent **WebSocket** to a **gateway** tier. If each gateway server holds about 500k idle connections (it's an event-loop server, Part 1 §3.4; memory per connection is the limit), you need $100{,}000{,}000 / 500{,}000 = $ **200 gateway servers**, plus headroom for failover and reconnect storms. A **session registry** (a fast key-value store with TTLs) maps `user_id → gateway` so messages can be routed to the right server.

**Message flow.**

```mermaid
sequenceDiagram
    participant A as Alice (gateway 7)
    participant CS as Chat service
    participant DB as Message store
    participant SR as Session registry
    participant B as Bob (gateway 42)
    A->>CS: send(conv 9, "hi", client_msg_id)
    CS->>DB: append with next seq in conv 9 (idempotent on client_msg_id)
    CS->>A: ack (seq 1051)
    CS->>SR: where is Bob?
    SR->>CS: gateway 42
    CS->>B: deliver(conv 9, seq 1051)
    B->>CS: delivered receipt
    Note over CS: Bob offline? Store, send a push notification, sync on reconnect
```

**The deep dives.**

1. **Ordering.** Assign a **per-conversation sequence number** at the chat service: the conversation is the unit of ordering, so all of a conversation's writes go through one partition owner. There's no global order, and none is needed (Part 2 §6: order only what users can see).
2. **Storage.** A wide-column store partitioned by `conversation_id` and clustered by `seq`: writes are appends, and "load the last 50 messages" is one partition range scan (Part 2 §4.1's compound key).
3. **Exactly-once effect.** Clients retry sends over flaky mobile networks, so a client-generated `client_msg_id` makes the append idempotent (Part 2 §8.5). Clients sync by asking "everything after seq N" on reconnect, which also repairs any missed pushes.
4. **Groups.** Small groups: fan out to each member's gateway. Very large channels: members pull or subscribe, like the celebrity case in the news feed.
5. **Presence.** Heartbeats over the WebSocket update a TTL key. Changes are fanned out only to contacts who are online and looking, and batched, because presence is chatty and doesn't need to be exact.
6. **Security.** End-to-end encryption (the Signal protocol, or MLS, RFC 9420, for large groups) means the server stores ciphertext it can't read. That rules out server-side search and moderation of message content, which is a product trade-off to decide explicitly.

**Failure modes.** A gateway dies → its clients reconnect to others with jittered backoff (§5.1; otherwise, a reconnect storm). Then they sync from their last seq. A chat-service partition owner fails → leadership moves (consensus-backed) and clients retry idempotently.

### 11.5 Systems to practise next

[Part 4](System%20Design%204%20-%20Worked%20Case%20Studies.md) works through eight more designs in full: rate limiter, key-value store, payments, ticket booking, video streaming, notifications, ride matching and an LLM chat service. For the rest, work each one through all eight steps, on paper, before looking anything up:

| Category | Systems | The key concept each one tests |
|---|---|---|
| Core | Rate limiter · distributed key-value store · unique ID generator | Algorithms + quorums (Part 2 §3) · consistent hashing · clock-free uniqueness |
| Social | Notification system · comments with replies · "people you may know" | Fan-out, idempotency · causal ordering · graph queries |
| Media | Video platform (upload → transcode → adaptive streaming) · photo sharing | Async pipelines, object storage, CDN economics |
| Location | Ride matching · proximity search · delivery ETA | Geospatial indexes (Part 1 §9.4), real-time state |
| Commerce | Payment system with a double-entry ledger · flash-sale ticketing · stock exchange order book | Strong consistency, idempotency, sagas · contention · ordering and latency |
| Infra | Web crawler · metrics/monitoring system · distributed job scheduler · search autocomplete | Politeness and dedup (Bloom filters) · time series · leases and fencing · tries and caching |
| Collaboration | Collaborative document editor · file sync (Dropbox) | CRDTs/OT (Part 2 §9) · chunking, dedup and conflict handling |
| AI | Chat assistant at scale · enterprise RAG · LLM gateway · coding-agent platform | KV-cache capacity (§9.3) · retrieval with permissions · routing and budgets · durable sandboxed agents |

### 11.6 Writing it down: design docs and ADRs

**The problem.** At work, a design that lives only in someone's head (or on a whiteboard photo) can't be reviewed before it's built, and nobody remembers later *why* it was built that way. Senior engineers are judged as much on how clearly they write designs as on the designs themselves.

**A design doc** (also called an RFC or tech spec) is written and reviewed *before* building. A useful structure:

1. **Context and problem**: what's wrong or missing, and why now.
2. **Goals and non-goals**: non-goals stop scope creep ("we will not support multi-region in v1").
3. **Requirements**: functional and non-functional, with numbers (§11.1 steps 1–2).
4. **Proposed design**: diagrams, APIs, data model, the key flows.
5. **Alternatives considered**: each with *why it was rejected*. This is the section that shows real thinking.
6. **Trade-offs and risks**: what you're giving up, and what could go wrong.
7. **Rollout and migration**: phases, feature flags, backfills, rollback plan (§6.3).
8. **Operations**: SLOs, dashboards, alerts, on-call impact.
9. **Security, privacy and cost** (§7, §7.7, §6.5).
10. **Open questions**.

Keep it as short as the decision allows. A two-page doc that gets read beats a 30-page one that doesn't.

**An ADR (architecture decision record)**, a format proposed by Michael Nygard in 2011, records *one* decision in a short file kept in the repository next to the code:

```markdown
# ADR 0007: Use PostgreSQL for the orders service

Status: Accepted (2026-10-21). Supersedes ADR 0003.

## Context
Orders need multi-row transactions and ad-hoc reporting queries.
Peak load is about 2,000 writes/s, well within one primary with replicas.

## Decision
Use PostgreSQL 18 with one primary and two replicas. No sharding until
write load passes about 20,000/s.

## Consequences
+ Serializable transactions, mature tooling, the team already knows it.
- Vertical write ceiling; sharding later will be a project of its own.
- We must run connection pooling (PgBouncer) for the serverless workers.
```

ADRs are **never edited after acceptance**. A changed decision gets a *new* ADR that supersedes the old one. Over time, the folder becomes the project's memory: a new engineer can read why things are the way they are, instead of undoing a decision whose reason they never knew.

**The interview connection:** say your design the same way. State the alternatives, pick one, and give the trade-off out loud ("I'll use fan-out on write *because* reads outnumber writes 50:1, *accepting* the celebrity problem, which I'll handle with…"). That's what interviewers mean by "trade-off reasoning".

---

## 12. Self-check, decision drills and glossary

<details>
<summary>1. A service handles 2,000 req/s at 80 ms average latency. How many requests are in flight? What if latency degrades to 800 ms?</summary>

Little's Law: $2{,}000 \times 0.08 = 160$. At 800 ms: **1,600**, a 10× jump in concurrency that can exhaust pools and memory.
</details>

<details>
<summary>2. Your servers run at 90% utilisation with 10 ms service time. Product wants 5% more traffic on the same fleet. What happens to mean latency (M/M/1)?</summary>

90% → 94.5%: $10/0.1 = 100$ ms → $10/0.055 \approx 182$ ms. **5% more traffic, ~80% more latency.** Add capacity instead.
</details>

<details>
<summary>3. Why do retries need jitter, and why should only one layer retry?</summary>

Without jitter, clients that failed together retry together: synchronised waves. Retrying at several layers multiplies load ($3^3 = 27$× for 3 layers × 3 tries) exactly when the backend is weakest.
</details>

<details>
<summary>4. Your service synchronously calls 4 dependencies, each 99.95% available. What's your best-case availability?</summary>

$0.9995^4 \approx 0.9980$, so 99.80% (assuming your own code never fails). That's about 86 minutes of downtime per 30 days, against 22 minutes for a single 99.95% component.
</details>

<details>
<summary>5. Why can't you fix a slow LLM decode by buying GPUs with more compute (FLOPS)?</summary>

Decode is **memory-bandwidth-bound**: each token step streams all the weights. More bandwidth, batching (limited by KV-cache memory), quantisation and speculative decoding help. More FLOPs mostly help prefill.
</details>

<details>
<summary>6. In RAG, why combine BM25 with vector search, and where must permissions be enforced?</summary>

Vectors miss exact tokens (IDs, names); BM25 catches them. Permissions must be enforced **at retrieval**, so that unauthorised chunks never enter the prompt.
</details>

<details>
<summary>7. News feed: why not fan out on write for everyone?</summary>

Celebrities: one post becomes millions of writes (100M followers at 1M writes/s = 100 s). Use the hybrid: push for normal users, pull for celebrities.
</details>

**Decision drills.** Commit to an answer and a reason before opening each one (method: Part 1 §2.5).

<details>
<summary><b>Drill 1.</b> Checkout synchronously calls six services in sequence: inventory, pricing, tax, fraud, payment and email. p99 is 2.5 s and checkout fails more often than any one service does. What do you change?</summary>

Two separate problems. **Availability multiplies** in a chain (§5.4): six 99.9% services give about 99.4%. **Latency adds** in a sequence. Fixes:

1. **Move non-essential work off the critical path**: email (and analytics) become events after the order commits (§3.1). They no longer affect checkout at all.
2. **Run independent calls in parallel**: pricing, tax and fraud don't depend on each other. Latency becomes the *slowest* of them, not the sum.
3. **Timeouts and fallbacks** for the soft dependencies: if fraud scoring times out, accept low-value orders and flag them for review, rather than failing.
4. Keep inventory reservation and payment synchronous; they're the truly essential steps (Part 4 §4–§5).
</details>

<details>
<summary><b>Drill 2.</b> On a sale day, traffic jumps 5× within 10 minutes. Autoscaling takes 6 minutes to add capacity. The site falls over. What should the design have been?</summary>

Reactive autoscaling can't absorb a spike faster than its own lag (§5.8). Layers of defence:

1. **Predictive scaling**: the sale was scheduled, so pre-scale before it starts.
2. **Load shedding with priorities** (§5.3): protect checkout; shed recommendations and other non-essential calls first.
3. **Graceful degradation**: switch off expensive features (personalisation, live stock counts), and serve more from caches with longer TTLs.
4. **A waiting room** (Part 4 §5) if demand exceeds what any amount of scaling can serve.
5. **Check the dependencies**: the database can't autoscale the way app servers do. Did more app servers just multiply its connections?
</details>

<details>
<summary><b>Drill 3.</b> A B2B SaaS team wants active-active multi-region "for availability". Their customers are mainly in the EU, and their SLO is 99.95%. Do you agree?</summary>

**Clarify the problem first** (§5.7). 99.95% allows about 22 minutes of downtime a month. That's achievable with **one region across multiple AZs**, good deploy practices, and a **tested DR plan** to a second region (active-passive). Active-active brings conflict handling or cross-region consensus, double the cost, and much more operational complexity, for availability they probably don't need.

What their EU customers may truly need is **data residency**: an EU home region. If they later add US customers, partition by home region instead of making every region write everything. Say what would change your mind: a contractual SLO of 99.99%+, or regulators requiring no single-region dependency.
</details>

<details>
<summary><b>Drill 4.</b> Ten minutes after a deploy, the error rate is 2% and rising, and nobody knows why. What do you do first?</summary>

**Roll back.** Mitigate first, diagnose later (§6.6). The most likely cause of a new problem is the most recent change, and undoing it is usually fast and safe. Investigate on the rolled-back system, or with the bad version in a canary.

Then the design lesson: a **canary with automatic SLO checks** (§6.3) should have stopped this at 1% of traffic, before it reached everyone. If rollback is hard (say, a schema change that went with the deploy), that's the real finding for the postmortem: the change should have used expand → migrate → contract.
</details>

<details>
<summary><b>Drill 5.</b> A Kafka consumer keeps crashing on one malformed event. Lag on that partition grows by the hour, and orders behind it are delayed. Fix it now, and fix it for good.</summary>

**Now:** move the bad message aside (to a dead-letter topic), or skip it with a recorded offset, so the partition flows again (§3.8). If per-key ordering matters, park only that key's later events.

**For good:** separate *permanent* errors (malformed data, which goes to the DLQ immediately) from *transient* ones (retry with backoff). Add schema validation at the producer (a schema registry, §2.2) so malformed events can't be published. Alert on DLQ growth and consumer lag. And make the consumer **catch failures per message** instead of crashing the whole process.
</details>

<details>
<summary><b>Drill 6.</b> HR wants an assistant that answers employee questions from 2,000 policy documents. They're updated weekly, and some are restricted to managers. Which approach?</summary>

**RAG** (§9.4, §9.7). The knowledge is too large and changes too often for fine-tuning, and answers need citations. Key design points:

1. **Permission filtering at retrieval time**, so a non-manager's question never retrieves manager-only chunks. This is the most important requirement.
2. Hybrid search (BM25 + vectors), because policy questions often use exact terms ("parental leave", form numbers).
3. Re-index on each weekly update (CDC or a scheduled job), keeping document versions and dates.
4. An **eval set** of real questions with expected answers, run on every change.
5. "I don't know, contact HR" when retrieval finds nothing relevant, rather than letting the model guess.
</details>

<details>
<summary><b>Drill 7.</b> A security review finds that <code>GET /api/files/{id}</code> returns any file to any logged-in user who knows its ID. How do you fix it, and how do you make sure the bug class is gone?</summary>

It's broken object-level authorisation, OWASP A01 (§7.8). **Fix:** check, on the server, that the requesting user may access *that* file, on every request.

**Make the class go away**, because this bug is rarely alone: route all data access through one **authorisation layer or service** with one permission model (§7.3), so a new endpoint can't forget the check. Add automated tests that call every endpoint as the wrong user. Use unguessable IDs (UUIDv7 or random) as extra defence, not as the fix. Review the audit logs (§7.7) to learn whether the hole was exploited.
</details>

**Glossary**

| Term | Meaning |
|---|---|
| **gRPC** | Typed RPC over HTTP/2 with Protobuf |
| **Backward / forward compatible** | New code reads old data / old code reads new data |
| **Cursor pagination** | Paging by "after this key" instead of offsets |
| **Consumer group** | Kafka consumers sharing a topic's partitions |
| **ISR** | In-sync replicas of a Kafka partition |
| **Backpressure** | Slowing producers to match consumers |
| **Event sourcing / CQRS** | Events as source of truth / separate write and read models |
| **CDC** | Change data capture: streaming a DB's own change log |
| **Watermark** | A stream processor's estimate that event time T is complete |
| **Durable execution** | Workflows whose state is persisted per step and replayed after crashes |
| **Little's Law** | $L = \lambda W$ |
| **Utilisation (ρ)** | Fraction of time a server is busy |
| **Hedged request** | Duplicate request sent after a delay to cut tail latency |
| **USL** | Universal Scalability Law: contention + coherence costs |
| **Full jitter** | Random backoff uniformly in [0, cap] |
| **Retry budget** | Limit on retries as a share of traffic |
| **Circuit breaker** | Stops calls to a failing dependency, then probes |
| **Bulkhead** | Separate resource pools per dependency |
| **Load shedding** | Rejecting excess work early |
| **Metastable failure** | Overload sustained by its own retries after the trigger is gone |
| **SLI / SLO / SLA** | Measured indicator / internal target / external contract |
| **Error budget** | 1 − SLO: allowed unreliability |
| **RPO / RTO** | Tolerable data loss / downtime |
| **Cell / shuffle sharding** | Independent stack copies / random worker combinations per customer |
| **Reconciliation loop** | Controller driving actual state toward desired state |
| **Canary** | Gradual rollout to a small share of traffic, with checks |
| **Expand–contract** | Safe, multi-step schema migration |
| **eBPF** | Verified programs running inside the Linux kernel |
| **OpenTelemetry** | Vendor-neutral standard for traces, metrics and logs |
| **RED / USE** | Rate-Errors-Duration / Utilisation-Saturation-Errors |
| **Zero trust** | Verify every request; no implicit network trust |
| **PKCE** | OAuth proof key that stops authorisation-code interception |
| **Passkey** | Phishing-resistant public-key credential (WebAuthn) |
| **ReBAC / Zanzibar** | Relationship-based authorisation / Google's system for it |
| **Envelope encryption** | Data keys wrapped by a master key in a KMS |
| **SBOM / SLSA / Sigstore** | Component inventory / build-integrity levels / artifact signing |
| **Columnar storage** | Storing each column contiguously for fast scans |
| **Lakehouse / Iceberg** | Warehouse features on object storage / the open table format |
| **Kappa architecture** | Everything as a replayable stream |
| **Prefill / decode** | Processing the prompt / generating tokens one at a time |
| **TTFT / TPOT** | Time to first token / time per output token |
| **KV cache** | Stored attention keys and values for previous tokens |
| **Continuous batching / PagedAttention** | Per-step batch membership / paged KV memory |
| **RAG** | Retrieval-augmented generation |
| **HNSW / PQ** | Graph-based ANN index / vector compression |
| **MCP** | Model Context Protocol: standard for agent tools and data sources |
| **Prompt injection** | Malicious instructions hidden in data an LLM reads |
| **Evals** | Graded test sets for AI behaviour |
| **Bounded context** | A domain area with its own consistent model |
| **Strangler fig** | Incremental replacement of a legacy system |
| **Conway's Law** | Systems mirror the communication structure of their organisations |
| **Poison message / DLQ** | A message that always fails / the queue it's moved to after N attempts |
| **Visibility timeout** | How long a taken job stays hidden before reappearing for another worker |
| **SKIP LOCKED** | SQL clause letting concurrent workers claim different rows without blocking |
| **PII** | Personally identifiable information |
| **Crypto-shredding** | Deleting a per-user key to make all copies of their data unreadable |
| **Data residency** | Keeping data stored and processed inside a required jurisdiction |
| **ADR** | Architecture decision record: one short, immutable file per decision |
| **RFC 9457 Problem Details** | Standard JSON shape for API errors |
| **ETag / If-Match** | Resource version and conditional update over HTTP (optimistic concurrency) |
| **Share group** | Kafka 4.2+ queue-style consumption: per-message acknowledgement, no per-key order |
| **Consumer lag** | How far a consumer is behind the newest message |
| **Home region** | The one region that owns (writes) a given user's data |
| **N+1 capacity** | One spare unit beyond what peak needs, to survive a failure |
| **Contract test** | Test that a provider still meets the expectations its consumers rely on |
| **IDOR / BOLA** | Broken object-level authorisation: accessing others' objects by ID |
| **SSRF** | Tricking a server into fetching an attacker-chosen (often internal) URL |
| **PKCE** | OAuth proof key binding the code exchange to the client that started it |
| **A2A** | Agent2Agent protocol for agents calling other agents |

---

## 13. References

- Jeffrey Dean and Luiz André Barroso, "The Tail at Scale", *CACM*, 2013.
- Neil Gunther, *Guerrilla Capacity Planning* (Universal Scalability Law), 2007. Gene Amdahl, 1967.
- John D. C. Little, "A Proof for the Queuing Formula L = λW", 1961.
- Nathan Bronson et al., "Metastable Failures in Distributed Systems", HotOS 2021.
- Marc Brooker, "Exponential Backoff and Jitter", AWS Architecture Blog, 2015; the AWS Builders' Library on timeouts, retries, and cell-based architecture / shuffle sharding.
- Betsy Beyer et al., *Site Reliability Engineering* and *The Site Reliability Workbook*, Google/O'Reilly (SLOs, error budgets, burn-rate alerts; free online).
- Jay Kreps, "Questioning the Lambda Architecture", 2014; Tyler Akidau et al., "The Dataflow Model", VLDB 2015 (windows and watermarks).
- Jeffrey Dean and Sanjay Ghemawat, "MapReduce", OSDI 2004. Matei Zaharia et al., "Resilient Distributed Datasets" (Spark), NSDI 2012.
- Ruoming Pang et al., "Zanzibar: Google's Consistent, Global Authorization System", USENIX ATC 2019.
- NIST SP 800-207 *Zero Trust Architecture*, 2020; NIST FIPS 203 (ML-KEM) and FIPS 204 (ML-DSA), 2024.
- IETF, [draft-ietf-oauth-v2-1](https://datatracker.ietf.org/doc/draft-ietf-oauth-v2-1/) (OAuth 2.1, still a draft as of revision -16, September 2026).
- [Post-quantum TLS: what's actually shipping in 2026](https://unveilscan.unveiltech.com/blog/post-quantum-tls.html).
- Gyeong-In Yu et al., "Orca: A Distributed Serving System for Transformer-Based Generative Models", OSDI 2022 (continuous batching).
- Woosuk Kwon et al., "Efficient Memory Management for Large Language Model Serving with PagedAttention" (vLLM), SOSP 2023.
- Yu. A. Malkov and D. A. Yashunin, "Efficient and robust approximate nearest neighbor search using HNSW graphs", 2016/2018. Hervé Jégou et al., "Product Quantization for Nearest Neighbor Search", 2011.
- Patrick Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", NeurIPS 2020.
- Model Context Protocol specification ([modelcontextprotocol.io](https://modelcontextprotocol.io)); [Anthropic: donating MCP and establishing the Agentic AI Foundation](https://anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation), December 2025.
- [Linux Foundation: A2A protocol at one year](https://linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year), April 2026.
- [OWASP Top 10:2025](https://owasp.org/Top10/2025/0x00_2025-Introduction/). RFC 9457 (Problem Details for HTTP APIs), RFC 7636 (PKCE).
- Apache Kafka 4.2 release (share groups production-ready): [Confluent: Apache Kafka 4.2 release](https://www.confluent.io/blog/apache-kafka-4-2-release/).
- [OpenTelemetry Profiles enters public alpha](https://opentelemetry.io/blog/2026/profiles-alpha), March 2026.
- Iceberg v3 general availability: [Snowflake release note, May 2026](https://docs.snowflake.com/en/release-notes/2026/other/2026-05-07-iceberg-v3-ga).
- NVIDIA Dynamo documentation on [disaggregated serving](https://docs.nvidia.com/dynamo/v1.0.0/design-docs/disaggregated-serving).
- Pact consumer-driven contract testing; FoundationDB's deterministic simulation testing (Will Wilson, "Testing Distributed Systems w/ Deterministic Simulation", Strange Loop 2014).
- Eric Evans, *Domain-Driven Design*, 2003. Matthew Skelton and Manuel Pais, *Team Topologies*, 2019. Melvin Conway, "How Do Committees Invent?", 1968.
- Alex Xu, *System Design Interview*, volumes 1 and 2 (for more worked designs in the §11 format).
- Martin Kleppmann and Chris Riccomini, *Designing Data-Intensive Applications*, 2nd ed., O'Reilly, 2026.

**Next:** [Part 4: Worked Case Studies](System%20Design%204%20-%20Worked%20Case%20Studies.md), eight more systems designed end to end.

**Back to:** [Part 1](System%20Design%201%20-%20Foundations%20Building%20Blocks%20and%20Storage.md) · [Part 2](System%20Design%202%20-%20Distributed%20Systems%20Theory.md)
