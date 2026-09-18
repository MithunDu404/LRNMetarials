# System Design Foundations: From a Single Server to a Scalable Architecture

## Why System Design Matters

AI now writes most code implementation, and software engineering is shifting toward agentic development. Because of this, companies are placing less weight on whether a candidate can produce code and more weight on whether the candidate understands systems and trade-offs at a high level — how components talk to each other, how to design them from scratch, and how to justify architectural decisions at scale. This is why system design rounds have become a standard part of technical interviews. It also matters outside of interviews: even engineers who are not the ones making architectural decisions still need to understand how the systems they work on function, how the pieces fit together, and what trade-offs were made in building them.

The material is organized into five parts: foundations (core concepts), API design (contracts, versioning, communication patterns), databases (storage patterns, consistency, database types), scaling (performance, caching, reliability, points of failure), and interview preparation.

## Starting Small: The Single-Server Setup

Every complex system starts from something simple, so the approach here is to begin with a system that supports a single user and grow it step by step. This lets each core component be understood in isolation before additional complexity is layered on.

In the simplest possible setup, everything — the web application, the database, the cache, and any other components — runs on one single server.

### How a Request Flows Through a Single-Server System

1. A user, via a web browser or a mobile app, wants to reach the application at a domain like `app.demo.com`. The user does not know the server's actual IP address — only the domain name.
2. The browser or app contacts a **DNS (Domain Name System)** provider, whose job is to map domain names to IP addresses.
3. The DNS provider looks up `app.demo.com`, finds it maps to the server's IP address, and returns that IP address to the client.
4. Now that the client knows where to send traffic, it sends an **HTTP request** to that IP address asking for specific data.
5. The server processes the request and sends back the requested data — an HTML page for a browser, or a JSON response for a mobile app, depending on the type of client and request.

### Web Traffic vs. Mobile Traffic

Traffic into the server generally comes from two sources, and each is handled somewhat differently:

- **Web applications**: the server handles business logic, data storage, and presentation (HTML, CSS, JavaScript) directly.
- **Mobile applications**: communication happens over HTTP via API calls, and the server typically responds with JSON because it is lightweight and easy for mobile clients to parse.

Example API request from a mobile client:

```
GET /product/{id}
```

Example JSON response:

```json
{
  "id": "123",
  "name": "Product Name",
  "description": "...",
  "price": 19.99
}
```

The client (web or mobile) then uses this JSON to render the product on screen.

This single-server setup is fine for a small user base but will struggle under heavier traffic — the rest of the lesson is about identifying where a single server breaks down and how to scale each part of the system.

**Key takeaways:** start with the simplest possible architecture to understand the essential components; understand how a request actually flows through the system (DNS resolution → IP → HTTP request → response); and recognize that web and mobile clients interact with the server somewhat differently.

## Separating the Web Tier and the Data Tier

As the user base grows, a single server is no longer sufficient. The first structural change is to split the system into a **web tier** (handles web and mobile traffic) and a **data tier** (manages the database). Splitting these lets each be scaled independently according to its own load.

This raises the question: given a choice of database technologies, how do you pick the right one for a given application?

## Choosing a Database: Relational vs. Non-Relational

There are two broad categories of databases to choose between.

### Relational Databases (RDBMS)

Relational databases store data in **tables** — structurally similar to spreadsheets — and are queried using **SQL (Structured Query Language)**. Examples: PostgreSQL, MySQL, Oracle Database, SQLite.

- **Tables** are the fundamental building block; each table has **columns** (fields/attributes) and **rows** (individual records).
  - Example: a `customers` table might have columns `ID`, `name`, `age`, `email`, with a row like `123, John, 40, ...`.

**Advantages of relational databases:**

- **Complex join operations across multiple tables.** For example, given a `customers` table and a `products` table, you can create an `orders` table that references customer IDs and product IDs, effectively linking customers to the products they ordered. Combining data from two or more tables like this is called a **join**.
- **Robust data consistency and integrity, especially for transactions.** A **transaction** is a sequence of one or more SQL operations executed as a single atomic unit — the classic example is a bank transfer. Transactions follow the **ACID** properties:
  - **Atomicity**: the entire transaction is treated as one unit — it either completely succeeds or completely fails.
  - **Consistency**: a transaction moves the database from one valid state to another valid state.
  - **Isolation**: concurrent transactions don't interfere with each other's intermediate results.
  - **Durability**: once a transaction commits, the data survives even a system or database server failure.

### Non-Relational Databases (NoSQL)

Non-relational databases come in several distinct forms, each suited to different data shapes and access patterns:

- **Document stores** — e.g., **MongoDB**. Data is stored as JSON-like documents, which allows complex, nested data structures to live inside a single record.
- **Wide-column stores** — e.g., **Cassandra**, **Cosmos DB**. Data is organized into tables, rows, and *dynamic* columns. These handle massive scale well and are particularly strong for high write throughput.
- **Graph databases** — e.g., **Neo4j**. These focus on storing entities and the relationships between them as a graph. Example: Amazon uses the **Neptune** graph database to generate product recommendations based on a user's previous orders.
- **Key-value stores** — e.g., **Redis**, **Memcached**. Data is stored as key-value pairs. Because they are primarily held in RAM, reads and writes are extremely fast compared to disk-backed databases. Their main strengths are simplicity and speed.

**Why NoSQL can be advantageous:** Revisiting the customers/products/orders example — in MongoDB, all of that related data (user, orders, products) could be stored together in a single document rather than split across separate joined tables. This lets NoSQL databases handle highly dynamic, large datasets without imposing the rigid structure that relational databases require, and they are generally optimized for low latency and scalability.

### When to Use Which

| Use SQL when… | Use NoSQL when… |
|---|---|
| Data is well-structured with clear relationships (e.g., an e-commerce app tracking customers and orders) | The app needs super low latency for quick responses |
| Strong consistency and transactional integrity are required (e.g., a financial or banking system) | Data is unstructured/semi-structured (e.g., JSON objects) and relationships aren't critical |
| | The app needs flexible, scalable storage for massive data volumes (e.g., a recommendation engine storing user activity in key-value format) |

## Scaling Strategies: Vertical vs. Horizontal

### Vertical Scaling (Scale Up)

Vertical scaling means adding more resources — RAM, CPU, etc. — to the *existing* server. It's simple and adequate for low-to-moderate traffic, but has two structural limitations:

- **Resource limits**: there is a hard ceiling on how much a single machine can be upgraded.
- **Lack of redundancy**: if that one server goes down, the entire application goes down with it, since there's nothing else serving traffic.

### Horizontal Scaling (Scale Out)

Horizontal scaling means adding *more servers* to share the load — for example, replicating a single server into three identical servers and splitting traffic across them. This is generally preferred for large-scale applications because it provides:

- **Higher fault tolerance**: if one server fails, the remaining servers keep serving users while the failed one recovers.
- **Better scalability**: additional servers can be added as demand grows.

### The Need for a Load Balancer

With only one server, all client requests naturally go to that one place. Once there are multiple servers, something has to decide *which* server a given request goes to. That component is the **load balancer**, sitting between clients and the pool of servers.

The load balancer:
- Distributes incoming traffic to whichever server currently has the least load.
- Handles fault tolerance: if a server goes down, the load balancer stops routing traffic to it and redirects everything to the remaining healthy servers until the failed one recovers.
- Supports scalability: new servers can be added to the pool, and the load balancer will incorporate them into its distribution.

At this point the load balancer is treated as a black box — the next section opens it up to examine how its distribution logic actually works.

## Load Balancing Strategies and Algorithms

There are seven commonly used load balancing strategies:

### 1. Round Robin

The simplest algorithm: each server in the pool receives requests in sequential, rotating order — first request to server 1, second to server 2, third to server 3, then back to server 1, and so on. This works well when all servers in the pool have similar specifications/capacity.

### 2. Least Connections

Routes each new request to whichever server currently has the fewest active connections. Example: if server 1 has 10 active connections, server 2 has 9, and server 3 has 30, a new request goes to server 2 (now bringing it to 10). This is particularly useful when session lengths vary significantly (some sessions last 10 minutes, others last 1 minute) — the load balancer accounts for actual current load rather than assuming every connection is equally "expensive."

### 3. Least Response Time

Combines responsiveness with connection count. Example: server 1 is highly responsive, server 2 is low responsiveness, server 3 is medium. The load balancer prioritizes sending traffic to the fastest server, but also tracks active connections — once the fast server 1 reaches, say, 40 active connections, the balancer starts diverting some traffic (e.g., 20 requests) to the medium-responsiveness server 3, and eventually some to server 2, before cycling back. This is effective when the goal is fastest possible response time and servers have genuinely different capabilities.

### 4. IP Hash

Determines the target server by hashing the client's IP address. This guarantees a given client is consistently routed to the *same* server on every request — useful when servers hold client-specific state or information locally.

### 5. Weighted Algorithms

Variants of the above (e.g., weighted round robin, weighted least connections) where each server is assigned a **weight** based on its capacity/performance (e.g., amount of RAM: 16GB, 32GB, 64GB). More traffic is routed to higher-weighted (more capable) servers, and proportionally less to weaker ones.

### 6. Geographical (Location-Based) Algorithms

Routes requests to the server geographically closest to the user. Example: an application mostly used by US users but with some European traffic might have servers in US-East, US-West, and Europe. A request from a European user's IP address gets routed to the Europe-based server; a US request gets routed to US-East or US-West depending on location. This reduces latency and is useful for globally distributed services.

### 7. Consistent Hashing

Uses a hash function to distribute data/requests across nodes, conceptually visualized as a **hash ring** (a circle) with the servers placed at points along it. When a request arrives, the hash function maps the client's IP address to a point on this ring, and the request is routed to whichever server is closest to that point on the ring. This is more complex to implement than the other strategies but, like IP hashing, guarantees the same client is consistently routed to the same server.

### Health Checks

A load balancer needs to know when a server has actually gone down before it can stop routing to it. This is done via **health checks** — the load balancer continuously sends health-check requests to every server in the pool and tracks which are online vs. offline. If a server fails its health check, the load balancer marks it unavailable and stops sending it traffic; once the server responds successfully to health checks again, it's brought back into rotation.

### Load Balancer Implementations

- **Software load balancers**: e.g., **Nginx** (also functions as a web server, but includes load-balancing features you configure, including servers, algorithm, and health checks) and **HAProxy** (open-source, self-configured).
- **Hardware load balancers**: e.g., **F5** (known for high performance and a broad feature set) and **Citrix**.
- **Cloud-based load balancers**: e.g., **AWS Elastic Load Balancing**, **Azure Load Balancer**, **Google Cloud Load Balancing**. These are the easiest option if your infrastructure already lives in that cloud provider, since they come with built-in security, automatic scaling (adding servers to the pool as demand grows), and monitoring (equivalent to health checks) without manual setup.

## Single Point of Failure (SPOF)

A **single point of failure** is any one component in a system whose failure brings down the entire system. For example, in a setup where clients hit a load balancer, which distributes to multiple API servers, all of which rely on one shared database — that database is a single point of failure. If it goes down, every API server loses the ability to function, and clients get no responses at all, even though the API servers and load balancer themselves are still "up."

Single points of failure are problematic for three reasons:

- **Reliability**: one failure (e.g., the database) can take down the whole system, translating directly into business loss — users may be unable to access the platform or complete actions like checkout.
- **Scalability**: systems built around single points of failure often struggle to scale, because every new component added increases the risk of hitting that one fragile dependency.
- **Security**: a single point of failure (e.g., a lone load balancer) is also an attack surface — an attacker can target it directly (e.g., by overwhelming it with traffic) and take down the whole system.

Database-specific strategies for avoiding SPOF are deferred to the databases section, but strategies for avoiding the *load balancer* becoming a single point of failure include:

1. **Redundancy**: run more than one load balancer. If one goes down, traffic is redirected to the remaining one(s); once the failed load balancer recovers, traffic (e.g., 50%) is redirected back to it.
2. **Health checks and monitoring for the load balancers themselves**: just as load balancers monitor server health, their own health should be continuously monitored so traffic is never sent to a load balancer that is down.
3. **Self-healing systems**: continuously monitor load balancer health, and if one is detected as down, automatically replace it with a new instance so clients experience no interruption.

---

# API Design

## What Is an API?

**API (Application Programming Interface)** defines how software components interact. Conceptually, on one side is a client (mobile app or browser), and on the other is a server responding to requests. The API is the **contract** between them: what requests can be made (which endpoints, which methods), and what responses to expect.

Two key properties of APIs:

- **Abstraction**: an API hides implementation details while exposing functionality. A client can request "save this user's data" without knowing anything about how that's implemented behind the endpoint.
- **Service boundaries**: APIs define clear interfaces between systems and components, which allows splitting responsibilities across multiple servers (e.g., one server owning users, another owning posts) and lets systems built differently underneath still communicate — whether client-to-server or server-to-server.

## The Three Major API Styles

### REST (Representational State Transfer)

The most common style. REST APIs are **resource-based** and use HTTP methods as their protocol.

- **Stateless**: each request carries all the information needed to process it; no request depends on a prior one.
- Uses standard HTTP methods: **GET** (fetch), **POST** (create), **PUT/PATCH** (update), **DELETE** (remove).
- Most commonly used in web and mobile applications.

### GraphQL

The second most common style — a query language letting clients request exactly the data they need.

- A **single endpoint** serves all operations; the client specifies what it wants in the request payload.
- Operations are called **query** (read, equivalent to REST's GET), **mutation** (write, equivalent to REST's POST/PUT/PATCH), and **subscription** (real-time communication).
- Key advantage: **minimal round trips**. Where REST might require several separate requests to gather related data, GraphQL can gather it all in one request.
- Recommended for **complex UIs** where different views need different, often deeply nested, combinations of data.

### gRPC

The least common of the three, but important for internal/service-to-service communication.

- A high-performance RPC (remote procedure call) framework using **protocol buffers**.
- Methods are defined as RPCs in `.proto` files.
- Supports streaming and bidirectional communication.
- Especially well suited to **microservices** and internal system communication, being more efficient than REST or GraphQL for server-to-server traffic.

### REST vs. GraphQL, Side by Side

**REST:**
- Resource-based endpoints, e.g. `/users/123`, `/users/123/followers`, `/users/123/posts` — the URL names the resource.
- Getting related data (e.g., a user plus their posts plus their followers) often requires **multiple requests** (three, in this example).
- Operations are expressed via HTTP methods (GET, POST, etc.).
- Response structure is **fixed** for a given endpoint — the data may change, but the shape stays consistent.
- Uses **explicit versioning** in the URL, e.g. `/v1/...`, later becoming `/v2/...` after a breaking change.
- Can leverage standard **HTTP caching** via headers.

**GraphQL:**
- A **single endpoint** (e.g. `/graphql`) handles all operations.
- One request can retrieve precisely the needed data using the query language, e.g.:

```graphql
query {
  user(id: 123) {
    name
    posts {
      title
      content
    }
    followers {
      name
    }
  }
}
```

- The **client specifies the response structure** in the query itself.
- Schema typically **evolves without formal versioning** (though a pattern of versioning individual fields, e.g. `followersV2`, does exist as an alternative to a full new API version) — fields can often just be modified directly if no other clients depend on the old shape.
- Uses **application-level caching** rather than HTTP caching.

## Four Design Principles for Great APIs

The guiding idea: the best API is one developers can use correctly without reading the documentation.

1. **Consistency** — consistent naming, casing, and patterns throughout. Mixing `camelCase` in one endpoint and `snake_case` (e.g., `user_details`) in another breaks this.
2. **Simplicity** — focus on core use cases with intuitive design; minimize complexity so the API can be understood quickly, ideally without documentation. An endpoint like `/users/123` should do what it obviously implies (fetch that user's details) — if calling it also silently updates followers or triggers unrelated side effects, that violates this principle.
3. **Security** — authentication and authorization between users, input validation, and rate limiting are the baseline requirements.
4. **Performance** — design for efficiency: appropriate caching strategies, pagination (with limit/offset) for large datasets rather than returning everything at once, minimized payload sizes, and reducing round trips where reasonable (e.g., including small pieces of data alongside a response if you already know the client will need them, rather than forcing a second request).

## How Protocol Choice Shapes API Design

The chosen application protocol fundamentally constrains and enables specific API design options:

- **HTTP** naturally enables RESTful design — its status codes map cleanly onto CRUD-style operations.
- **WebSocket** enables real-time, bidirectional communication — well suited to chat applications or video streaming.
- **GraphQL** APIs also run over **HTTP** (not WebSocket or gRPC).
- **gRPC** is commonly used between microservices to achieve higher performance than HTTP-based communication.

Protocol choice affects API structure, performance, and capabilities, so it should be chosen to match the strengths/limitations relevant to the specific type of API being built.

## The API Design Process

### Understanding Requirements

- Identify core use cases and user stories.
- Define scope and boundaries — a large API is typically not built all at once, so decide what's in scope now versus deferred.
- Determine performance requirements and where bottlenecks are likely to occur.
- Address security constraints from the start: authentication, authorization, rate limiting, and anything else specific to the API.

### Design Approaches

- **Top-down**: start from high-level requirements and workflows, then define endpoints/operations. Common in interview settings, where requirements are given up front.
- **Bottom-up**: start from existing data models and capabilities and design the API around them. More common inside an existing company/codebase that already has established data models.
- **Contract-first**: define the API contract (request/response shapes) before implementation. Similar in spirit to top-down and also common in interviews.

### API Lifecycle

1. **Design phase** — design the API and discuss requirements and expected outcomes.
2. **Development phase** — build and locally test.
3. **Deployment and monitoring** — further testing on staging/production.
4. **Maintenance phase** — ongoing upkeep; this is easier when the API was designed with simplicity in mind.
5. **Deprecation and retirement** — older versions (e.g., a v1 API being superseded by v2) eventually get deprecated and retired.

The overall point: building an API is not just the coding/development step — design, maintainability, and eventual retirement are all part of the process.

---

# API Protocols

Choosing the wrong protocol for an API can create performance bottlenecks and functional limitations, so understanding the protocol options is necessary before they can be matched to an API's latency, throughput, and interaction-pattern requirements.

## Protocols in the Network Stack

Application-layer protocols sit at the top of the network stack, built on top of transport-layer protocols like **TCP** and **UDP**. At the application layer, protocols define message formats/structures, request-response patterns, and connection management/error handling. Below the application layer are the network, data link, and physical layers, but for API design purposes, the protocols of direct concern are **HTTP, HTTPS, WebSockets**, and similar application-layer protocols.

## HTTP (Hypertext Transfer Protocol)

HTTP is the foundation of web APIs. A typical HTTP interaction:

**Request** — the client specifies:
- **Method** (GET, POST, etc.)
- **Resource URL** (e.g., `/api/products/{id}`)
- **HTTP version**
- **Host** (the domain being accessed)
- **Authentication** (bearer token, basic auth, OAuth, etc.), typically required before accessing protected resources

**Response** — the server returns:
- **HTTP version** (matching the request)
- **Status code** (e.g., 200 for success, 400 for a client error, 500 for a server error)
- **Content type** (commonly `application/json`, but could be a static web page or other format)
- Additional headers, such as **cache-control**, for controlling caching behavior

### HTTP Methods

- **GET** — retrieve data
- **POST** — create data on the server
- **PUT / PATCH** — update data (fully or partially)
- **DELETE** — remove data from the server

### HTTP Status Codes

Status codes are grouped into series by what they signal. The 200 series indicates success (e.g., the request was processed successfully).

# HTTP Status Codes and Headers (continued)

Beyond the 200-series success codes, HTTP status codes are grouped by what kind of outcome they represent:

- **300 series** — redirection. The resource has moved and the client is pointed to a new location.
- **400 series** — client error. The request itself was malformed or invalid — the fault lies with whoever sent the request.
- **500 series** — server error. Something went wrong on the server's side while handling an otherwise valid request.

Common HTTP headers include:
- **Content-Type** — usually set by the server to describe the format of the body, though a client can also set it when sending data.
- **Authorization** — used by the client to authenticate itself to the server.
- **Accept** — tells the server what response formats the client can handle.
- **Cache-Control** — governs caching behavior.
- **User-Agent** — identifies the client software making the request.

There are more headers than this, but these are the ones you'll see constantly.

## HTTPS

HTTPS is the same HTTP protocol, but wrapped in TLS/SSL encryption. This adds a security layer so that data is protected while it's in transit between client and server.

Benefits of HTTPS:
- Data is encrypted in transit.
- It provides data integrity (the data can't be silently tampered with).
- It authenticates the server before it releases any data.
- It carries SEO benefits (search engines favor HTTPS sites).

Because plain HTTP carries real risk (data can be intercepted or modified in transit), the standard practice is to always serve production traffic over HTTPS.

## WebSockets

HTTP is well-suited to request-response interactions, but it has real limitations when you need continuous, real-time updates.

**Motivating example — a chat app.** Picture a client (the user's chat window) and a server (which holds messages between two users). When a user sends a message, the client makes a request to the server, and the server responds — perhaps with any new messages from the other user. But to find out about *new* incoming messages, the client has no choice but to keep asking again: "any new messages?" Often the answer is no, and the response comes back empty. This is called polling.

The problem with polling is threefold:
- **Increased latency** — a new message from the other user only becomes visible the next time the client happens to poll, not the instant it arrives.
- **Wasted bandwidth** — many of those requests return empty responses.
- **Wasted server resources** — the server has to process and respond to requests that accomplish nothing.

**How WebSockets fix this.** A WebSocket connection begins with a handshake (built on top of the first HTTP request). Once that handshake completes, the connection becomes genuinely two-way: the server is no longer limited to only responding when asked — it can *push* data to the client the instant new data exists. The client can still send its own requests when it needs something specific, but the key change is that the server is now an active participant that can initiate communication.

The result is real-time data delivery with minimal latency (the server pushes the moment something changes, instead of waiting for the client's next poll), and reduced bandwidth usage, since the constant cycle of "check every 5 or 10 seconds, usually for nothing" is eliminated. The only network round trip that's mandatory is the initial handshake — after that, communication happens exactly when there's something worth communicating.

## AMQP (Advanced Message Queuing Protocol)

AMQP is an enterprise messaging protocol built for message queuing with guaranteed delivery. It involves two roles:

- **Producer** — something that generates messages, e.g. a web service or a payment system.
- **Consumer** — something that processes those messages, e.g. a payment processor or a notification system.

The producer publishes messages to a **message broker**, which is where AMQP's queues live. For example, an "order processing" queue: whenever a new order is placed, the producer publishes a message onto that queue. The consumer then pulls messages from the queue whenever it has spare capacity — if it's busy handling something else, the message simply waits in the queue rather than being lost or forcing the producer to wait.

This decoupling is the whole point: the producer doesn't need the consumer to be immediately available, and the consumer processes work at its own pace rather than being overwhelmed by a burst of incoming requests.

AMQP supports different **exchange types** for how messages get routed to queues: direct (one-to-one), fan-out (broadcast to many), and topic-based (routed by pattern-matching). These are explored in more depth later, in the message-queuing section of the course.

## gRPC

gRPC is a high-performance RPC (remote procedure call) framework built by Google, using **protocol buffers** for message encoding and **HTTP/2** for transport.

Because it depends on HTTP/2, the client must support HTTP/2 — and since most browsers don't fully support this, gRPC is mainly used for **server-to-server** communication rather than browser-to-server. It's a natural fit for microservices talking to each other. Its reliance on HTTP/2 also gives it built-in streaming capability.

## Choosing an Application Protocol

Given HTTP, WebSockets, AMQP, and gRPC, the choice among them comes down to several factors:

- **Interaction pattern** — plain request-response defaults to HTTP; real-time, bidirectional needs (like chat) call for WebSockets.
- **Performance requirements** — when multiple internal services/microservices talk to each other and gRPC is viable, it can boost speed and efficiency.
- **Client compatibility** — e.g. most browsers can't fully leverage HTTP/2, which is part of why gRPC isn't typical for browser-facing APIs.
- **Payload size and encoding** needs.
- **Security needs** — authentication and encryption requirements.
- **Developer experience** — tooling and documentation quality matter because you'll be living with this API day to day.

**Summary of application-layer protocols:** HTTP/HTTPS for standard request-response, WebSockets for real-time bidirectional communication, AMQP for asynchronous, queued communication between producers and consumers, and gRPC (Google Remote Procedure Call) for high-performance service-to-service calls over HTTP/2.

# Transport Layer: TCP vs UDP

The application layer protocols above all still need something underneath them to actually move packets across the network — that's the transport layer, which contains **TCP** and **UDP**. Both move data between machines, but with very different guarantees.

## TCP (Transmission Control Protocol)

Think of TCP as sending a package with tracking, a receipt, and a required signature. If a large piece of data is broken into chunks — say three separate packets — TCP guarantees all three eventually arrive, in the correct order:

- If a packet is lost, TCP retransmits it.
- If packets arrive out of order (e.g. the client receives packet 1, then 3, then 2), TCP reorders them before delivering them to the application (1, 2, 3).
- TCP is **connection-based**: before any data flows, a **three-way handshake** establishes the connection.

The three-way handshake works like this:
1. Client sends a connection request (SYN) to the server.
2. Server responds, acknowledging and syncing (SYN-ACK).
3. Client acknowledges the server (ACK).

Once this exchange completes, the connection is established and data can flow both ways.

All of this — retransmission, reordering, handshake — adds overhead, but buys reliability and accuracy. That's why APIs handling payments, authentication, or other sensitive user data always use TCP: correctness matters more than raw speed.

## UDP (User Datagram Protocol)

UDP is fast and lightweight, but it gives up delivery guarantees. If four packets are sent and one is lost along the way, UDP does not retransmit it or otherwise ensure it arrives — that packet is simply gone. There's no handshake, no connection setup, no tracking.

This tradeoff is exactly why UDP suits real-time media. **Video calls** are the go-to example: if one small chunk of audio/video data is dropped mid-call, there's no value in going back to retrieve it — by the time it could be resent, the conversation has already moved on. So UDP just proceeds to the next packet rather than paying the cost of guaranteeing delivery of a packet whose moment has already passed. This makes UDP the standard choice for video calls, online games, and live streaming.

## TCP vs UDP: Decision Criteria

- **TCP** = safe and reliable, but slower — appropriate for banking, email, payments, and anything where losing or corrupting data is unacceptable.
- **UDP** = fast and lightweight, with acceptable data loss — appropriate for video streaming, gaming, and other real-time media where losing a little data is a fine trade for speed.

Together, the application layer (HTTP, WebSockets, AMQP, gRPC) and the transport layer (TCP, UDP) are the two layers most relevant to building APIs.

# RESTful APIs

REST APIs let different components of a system communicate over standard HTTP methods, and they're the dominant style for building and consuming APIs today. Designing them well means understanding architectural principles, resource modeling, URL design, status codes/error handling, filtering/sorting/pagination, and established best practices.

## Resource Modeling

The core idea of REST is to model your business domain as **resources**, expressed as **nouns**, not verbs. If your business domain has products, orders, and reviews, these become the URL resources `/products`, `/orders`, `/reviews`.

- `GET /api/products` returns the **collection** of products.
- `GET /api/products/{id}` returns a **single** product.

Note what's *not* done: you never see something like `/getProducts` — that would encode the action as a verb in the URL, which breaks REST convention. Instead, the verb is expressed through the HTTP method (GET, POST, etc.), and the URL only ever names the resource.

**Nested resources** should also be clearly and predictably structured. For example, `GET /products/{id}/reviews` is expected to return the reviews belonging to that specific product.

## Filtering, Sorting, and Pagination

Real-world APIs almost never want to return an entire dataset in one response. Three mechanisms address this, all implemented via **query parameters** (the part of the URL after `?`):

**Filtering** — e.g. `/products?category=electronics&inStock=true` filters the collection down to items matching the category and in-stock criteria before it's ever sent over the wire. This avoids wasting bandwidth and avoids handing the frontend a bloated response it would have to filter itself.

**Sorting** — e.g. `?sort=price_asc` or `?sort=reviews_desc`. The reasoning here matters: if a backend held, say, 1,000 products and simply returned all of them unsorted, the frontend would have to fetch the entire 1,000-item set just to sort by price. That's inefficient. So sorting is pushed down into the backend — the frontend just asks for the order it wants, and the backend (closer to the data) does the sorting before the response goes out.

**Pagination** — e.g. `?page=2&limit=10`. The `limit` parameter matters just as much as `page`: without it, a request for "page 2 onward" could still return an enormous number of remaining items. `limit` caps the response to whatever the frontend is actually going to display, and the client pages forward (`page=3`, etc.) as the user navigates.

Pagination has a few common variants:
- **Page + limit** (as above).
- **Offset + limit** — instead of a page number, `offset` specifies exactly which item index to start counting from within the full dataset, and `limit` still caps how many items come back from that point.
- **Cursor-based** — instead of a page number or offset, a `cursor` value (a hash representing a position in the dataset) is passed to fetch the next batch.

The benefits of supporting filtering, sorting, and pagination together: it saves server bandwidth, improves performance on both server and client, and gives the frontend flexibility to request exactly the data it needs rather than over-fetching.

## HTTP Methods for CRUD

REST APIs map CRUD operations onto standard HTTP methods:

- **GET** — read/retrieve a resource (e.g. `GET /api/v1/products`). GET requests are both **safe** and **idempotent** — calling `/products` repeatedly should return the same result each time (barring actual changes to the underlying data, like new products being added).
- **POST** — create a resource (e.g. `POST /api/v1/products` creates a new product). POST changes server state and is **not idempotent** — each call to create a resource produces a new, distinct item with its own new ID.
- **PUT** — update a resource by **replacing it entirely**. `PUT /products/123` takes the whole incoming object and overwrites the existing resource with ID 123 wholesale.
- **PATCH** — update a resource **partially**. `PATCH /products/123` with just a title field only changes the title, leaving every other property of that resource untouched.
- **DELETE** — remove a resource. `DELETE /products/123` deletes that resource; no request body is needed since you're identifying it purely by URL.

## Status Codes and Error Handling

Each of the operations above should return a status code appropriate to what actually happened:

- **200 series (success):** 200 = OK (e.g. a successful GET), 201 = resource created (used specifically for a successful POST — not 200, because 201 communicates *creation* specifically), 204 = no content.
- **300 series (redirection):** used when a requested URL has moved elsewhere, and the response redirects the client to the new location.
- **400 series (client error):** 400 = generic bad request (e.g. invalid parameters or malformed JSON), 401 = unauthorized (the requester isn't authenticated), 404 = not found (e.g. requesting a specific product ID that doesn't exist in the database — even though the request itself was well-formed).
- **500 series (server error):** used when something goes wrong on the server that isn't attributable to a client mistake — an unexpected server-side failure, returned with a generic server error message.

## Best Practices

- Use **plural nouns** for resource collections consistently (`/products`, not `/product`).
- Use the **correct HTTP method** paired with the correct URL for each CRUD operation — e.g. deleting a user should be `DELETE /users/{id}`, never something like a POST to `/delete`.
- Support **filtering, sorting, and pagination** together, not just pagination alone — offering page/limit/sort together gives the client real control, whereas offering only a page number without a limit or sort option is much more restrictive.
- Use **versioning** in the URL (e.g. `/api/v1/...`, `/api/v2/...`). This matters because it lets you evolve or even break changes in a new version without disrupting clients still relying on the old version — they can keep using `v1` uninterrupted while `v2` (or `v3`) is developed and potentially introduces breaking changes.

# GraphQL

## Why GraphQL Exists

Traditional REST APIs tend to either over-fetch or under-fetch data, often forcing the client to make several separate requests to assemble everything a single view needs. GraphQL was created at Facebook specifically to address this: clients kept needing multiple API calls and still not getting exactly the data they needed.

**Motivating example.** Imagine Facebook-style separate APIs for users, posts, comments, and likes. Assembling a single page might require hitting all of these APIs separately, and even then, each individual response might carry more or less data than the view actually needs. Every one of those round trips adds to the page's overall load latency — nothing is fully rendered until every request finishes.

GraphQL's alternative: a **single endpoint**, still built on HTTP, where the client specifies the *exact shape* of the response it wants. For example, a query can ask for a user by ID with just their `name`, their `posts` with just each post's `title` (skip the images), and nested `comments` with only the specific fields needed — all resolved through one request, with no more and no less data than requested. This eliminates both over-fetching and the need for multiple round trips.

## Schema Design and Type System

The GraphQL schema is the **contract** between client and server. It's built from:

- **Types** — e.g. a `User` type with fields like `id`, `name`, and `posts`. If a field isn't a primitive (like `posts`), it references another defined type (e.g. an array of `Post`), and that type is defined separately in the schema.
- **Queries** — the read side, equivalent to GET in REST. A query defines a name, its parameters, and its return type — e.g. a `user` query that takes an ID and returns the `User` type.
- **Mutations** — the write side, equivalent to POST/PUT/PATCH/DELETE in REST. Any operation that changes data in the database is expressed as a mutation — e.g. a `createUser` mutation that takes a `name` (and, in a real system, more fields) and returns the `User` type.

A well-designed schema should mirror the actual domain model and be intuitive and flexible to use.

## Queries and Mutations in Practice

A **query** lets the client request exactly the fields it needs from a defined query method — e.g. calling the `user` query and specifying only `name`, `posts`, and within each post only `title`. The server returns precisely that shape, nothing more.

A **mutation** works similarly but for writes — e.g. calling a `createPost` mutation with a `title` and `body`, while also specifying which fields of the newly created post (e.g. `id` and `title`) should come back in the response.

## Error Handling in GraphQL

GraphQL error handling differs meaningfully from REST: **every GraphQL response returns HTTP 200 OK**, regardless of whether an error occurred inside it. Errors are instead communicated through a dedicated `errors` field in the response body, and GraphQL supports **partial responses** — some data can come back successfully while other parts fail.

For example, a response might have `user: null` alongside an `errors` array containing an entry with a status code (e.g. 404), a message ("not found"), and a `path` indicating which part of the schema/query failed. Because the outer HTTP status is always 200, this `errors` array is where the actual error status must be encoded and inspected.

## Best Practices for GraphQL

- Keep schemas **small and modular**.
- **Avoid deeply nested queries** — a `user` → `posts` → `comments` chain could, in principle, nest indefinitely. To guard against this, set a **query depth limit** (e.g. capping nesting at six or seven levels).
- Use **meaningful naming** for types and fields, since both client and server share the exact same schema — naming clarity benefits both sides equally.
- Use dedicated **input types** for mutations (rather than reusing output types) when accepting mutation arguments.

# Authentication

## What Authentication Answers

Before a system can decide what a requester is *allowed* to do (authorization), it first has to establish *who* the requester is — a human via browser or mobile app, or a third-party service. That identity-verification step is authentication.

A common source of confusion the lesson calls out explicitly: many of these terms get conflated even though they operate at different levels:
- **JWT** is often treated as an authentication *method*, but it's actually just a **token format**.
- **Bearer authentication** is often confused with JWT specifically, but bearer is a general *pattern* ("whoever holds this token gets access"), and JWT is just the most common type of bearer token.
- **OAuth 2** is often called an authentication method, but it's actually an **authorization framework** — it answers "what can this app do on my behalf," not "who is this user."
- **Single sign-on (SSO)** is often treated as an authentication method, but it's really a **user-experience pattern**.

**Where authentication sits architecturally:** before a client (user or service) can reach the API gateway, service layer, or data storage, it sends a login request. The system verifies the claimed identity — if valid, access is granted to the gateway and downstream services; if not, the system responds with **401 Unauthorized**. Authentication is strictly the "who are you" step, prior to and separate from authorization ("what can you do").

## Basic Authentication Methods

**Basic authentication.** The simplest form: a client requests a protected resource (e.g. `GET /api/users`) without credentials and gets back 401 Unauthorized. The client retries, this time including an `Authorization` header containing the **Base64-encoded** `username:password`. The server decodes and verifies these credentials — 200 OK with data if valid, 401 again if not.

The problem: Base64 is trivially reversible, not actual encryption. This makes basic auth insecure unless wrapped in HTTPS, and even then it's rarely used in production outside of internal tooling, precisely because credentials are transmitted (in a barely-obscured form) with every single request.

**Digest authentication.** A modest improvement over basic auth: instead of sending the plain (Base64) username/password, the client sends an **MD5 hash** of the credentials. The flow is otherwise identical — initial 401, retry with the hashed credentials, success or 401 depending on validity. It's better than plain Base64, but still considered outdated and rarely used today given better modern alternatives.

*(Note: in tools like Postman, all of these — basic, digest, API key, bearer, etc. — get grouped under one "Authorization type" dropdown, which is part of why developers conflate authentication methods with authorization frameworks; Postman's UI treats them as one undifferentiated category for convenience.)*

**API key authentication.** Each client is issued a unique key, which it sends with every request via either the `Authorization` header or an `X-API-Key` header. On the server, keys are typically stored (as a hash, alongside associated **scopes**) in a database. When a request arrives, the server looks up the key: if the header is missing entirely, the server returns 400 Bad Request (the key is a required part of a well-formed request); if the key is present but invalid, 401 Unauthorized; if valid, the request proceeds and data is returned.

Two important caveats about API keys:
- If a key **leaks**, anyone holding it can act as that client — and there's no built-in expiration unless the system implements one itself.
- Despite superficial similarity to JWTs, an API key is just a **random string with no embedded information** — the server has no way to know who owns it or what it's allowed to do without a database lookup. JWTs, by contrast, can carry that information directly within the token itself.

**Session-based authentication.** The traditional web approach: a user logs in with credentials, and the server creates a **session**, storing it somewhere — options include:
- **In-memory** (a simple variable) — the drawback is that a server restart or crash wipes it out.
- **Redis** — the most common production choice, because it's fast and supports built-in key expiration.
- **A dedicated database** (SQL-based).
- **The filesystem** — rare, and not scalable.

Flow: the first login request returns a session ID, which is set as a cookie on the client. Subsequent requests include that cookie; the server looks the session up in session storage — if found and valid, the user's data comes back with an authorized response; if not found, 401 Unauthorized.

The key limitation: session-based auth is **stateful** — the server must maintain session storage somewhere. This works fine for traditional web apps but doesn't scale as cleanly for APIs or distributed systems, since every request requires a lookup against shared state.

## Token-Based Authentication

**Bearer authentication and JWT.** Modern systems generally move to tokens instead of sessions: the client sends a token with each request via the `Authorization` header, formatted as `Bearer <token>`. "Bearer token" is just a *pattern* — whoever holds the token gets access — not a specific method. The most common bearer token format is the **JWT (JSON Web Token)**: a signed JSON object containing claims such as user ID or email, an expiration time, and any other claims needed (roles, permissions, etc.).

**Why JWT matters — the shift from stateful to stateless.** Before JWTs, a token was just an opaque string with no information encoded in it; validating it required looking it up in a database (or cache) on every single request — inherently stateful. JWTs changed this by letting the server **encode and cryptographically sign claims directly into the token**. This makes short-lived JWTs **self-contained and stateless** — validation is just checking the signature locally, with no database hit required. This reduces database load and simplifies the server's authentication logic.

Flow: client sends credentials once; if valid, the server issues a JWT. From then on, the client attaches that JWT as a bearer token on every request; the server verifies the signature locally (no DB lookup) and either serves the request or returns unauthorized if the signature/claims are invalid.

**Access tokens and refresh tokens.** Modern systems typically issue two tokens together at login:
- **Access token** — short-lived (roughly 15 minutes to 1 hour), used to authenticate actual API calls.
- **Refresh token** — long-lived (days to weeks), used solely to obtain a new access token once the old one expires.

The reasoning for splitting these: a short-lived access token limits the damage window if it's ever compromised, while the long-lived refresh token lets the user stay logged in without repeatedly re-entering credentials.

Important security detail: refresh tokens should **never be stored in local storage** — they should be stored in **HTTP-only cookies**, specifically to prevent them from being accessible to (and stolen by) client-side scripts, i.e. to mitigate XSS-style attacks.

Flow in practice: the client uses the access token for ordinary requests. When it expires, the server returns 401 Unauthorized; the client then presents its stored refresh token to the auth server to obtain a fresh access token, and resumes making requests with the new one — without the user ever having to log in again.

## OAuth 2 and OpenID Connect

**OAuth 2** is frequently misunderstood as an authentication method, but it is an **authorization framework** — it answers "what is this application allowed to access on the user's behalf," not "who is this user."

**Motivating example — granting Google Drive access to a third-party app.**
1. The user chooses to connect their Google Drive to an external application.
2. The app redirects the user to a Google OAuth **consent screen**, which lists exactly what permission is being requested (e.g. "read your Drive files").
3. If the user approves, Google returns an **authorization code** to the application.
4. The application exchanges that code for an **access token**.
5. The confusing part: receiving this access token can *feel* like authentication, but it isn't — the access token only proves the app is permitted to access certain resources (Drive files); it does **not** tell the application who the user is.
6. From here, the app can use that access token to actually call the Google Drive API and retrieve files on the user's behalf.

**OpenID Connect (OIDC)** builds authentication *on top of* OAuth 2, closing exactly the gap described above. Flow for "Sign in with Google":
1. Clicking "Sign in with Google" redirects to an authorization endpoint showing a login/consent screen.
2. The user enters credentials and consents; the provider returns an authorization code.
3. The application exchanges that code for **two tokens**: an access token (for OAuth 2 authorization, as before) and an **ID token**.
4. The ID token is itself a **JWT** — and this is the piece that actually carries the user's identity (email, username, user ID, etc.).
5. The application verifies the ID token's signature, extracts the user's identity from it, and sends it to its own backend for verification.
6. With identity now established, the application can create its own session and issue its own access token for that authenticated user.

This combination — OAuth 2 for authorization plus OpenID Connect for authentication — is described as the modern, secure, and scalable standard for this kind of third-party sign-in flow.

# Single Sign-On and Identity Protocols

## What Single Sign-On Actually Is

Single sign-on (SSO) is a **user experience**, not an authentication method in itself. The distinction matters: SSO describes the *convenience* of logging in once and gaining access to multiple, otherwise separate services. It does not by itself define *how* the user's identity is verified — that job is handled by identity protocols working underneath SSO.

The classic example is Google. If you sign in once to Google as your identity provider, you can then move between Gmail, Google Drive, YouTube, and Google Calendar without re-entering your credentials at each one.

### How SSO Works Mechanically

1. You authenticate once with the identity provider (e.g. Google). This creates a **global session**, which is stored in session storage on the provider's side.
2. You receive a **single sign-on cookie** on your client. This cookie is what lets you prove, on subsequent requests, that you already have a valid global session.
3. The first time you try to access a resource — say, Gmail — your session is verified against the session storage, and access is granted.
4. When you then try to access a *different* resource — say, Google Drive — you don't have to log in again. The existing cookie plus the stored session are checked again; since it's still valid, access is granted immediately.
5. The same verify-and-grant flow repeats for YouTube, Google Calendar, and any other connected service.

So the "single login, many services" feel of SSO is powered by a shared session plus a cookie, checked afresh (but silently) at each new service.

### The Identity Protocols Underneath SSO

SSO needs a standardized way to actually validate and communicate identity between the identity provider and the services relying on it. Two protocols dominate here: **SAML** and **OpenID Connect**.

**SAML (Security Assertion Markup Language)**
- Flow: you try to access an app, get redirected to a login page, authenticate there, and receive back a **SAML assertion in XML format**. That assertion confirms your identity to the third-party application, which then grants access.
- It's XML-based, which makes it a bit heavier/older compared to newer alternatives.
- It's the common choice in **enterprise and legacy systems** — the speaker names **Salesforce** and corporate dashboards as typical examples.
- SAML is still widely used and considered secure, but it's the older of the two approaches.

**OpenID Connect**
- Flow: you try to access an app (the speaker uses **Gmail** as the example), get redirected to log in, provide credentials, and once authenticated you receive back an **ID token in JSON Web Token (JWT) format**. This token is what confirms your identity to Gmail.
- This is what Google itself uses under the hood.
- It's described as the more modern approach, though both SAML and OpenID Connect are considered secure and relevant today — the choice tends to depend on the ecosystem (enterprise/legacy vs. modern web apps).

Authentication (confirming who someone is) is only the first gate. Once that's settled, the system still needs to decide what that person is allowed to do — which is authorization.

# Authorization

## Authentication vs. Authorization

Authentication answers "who is this user, and are they allowed into the system at all?" — it's resolved at login, when the system approves or denies the login request. Authorization is the step that comes *after* a successful login: it determines **what resources or actions this specific user is permitted to touch**, and conversely what's denied to them. This is the mechanism that gives systems fine-grained security and privacy control, rather than an all-or-nothing gate.

Three authorization models are covered:
- Role-based access control (RBAC)
- Attribute-based access control (ABAC)
- Access control lists (ACL)

Alongside these, OAuth 2 and JWTs are the practical mechanisms used to *enforce* whichever authorization model a system chooses.

## Motivating Example: GitHub Repository Access

GitHub repositories illustrate why authorization needs to be more granular than authentication:
- **User A** might have **write access only** — they can push code to the repo.
- **User B** might have **read access only** — they can read the repo's contents but cannot push code or open pull requests.
- An **admin** user has full control — they can manage all repository settings and even delete the repository entirely.

All three users passed authentication in exactly the same way (they logged in successfully), yet they can do very different things once inside. That gap is what authorization models are built to manage.

## Role-Based Access Control (RBAC)

RBAC assigns each user to a **role**, and each role carries a predefined bundle of permissions. This is described as the most common of the three approaches. Using the GitHub-style tiering as illustration:

- **Admin**: full access — create, read, update, delete resources, and manage other users/roles.
- **Editor**: can create, read, and update content, but **cannot delete** resources and **cannot manage other users**.
- **Viewer**: read-only — can view resources and content but cannot create or update anything.

RBAC shows up constantly in everyday tools: GitHub, Stripe dashboards, CMS tools, and team-management tools are all named as real examples.

## Attribute-Based Access Control (ABAC)

ABAC goes beyond fixed roles. Instead of asking "what role does this user have?", it evaluates **attributes** of the user, attributes of the resource, and **environmental conditions**, combining them into policies.

Example policy walked through: allow access only if the user's `department` attribute equals `HR` **and** the resource's attribute equals `internal`. Only when both conditions hold is access granted — and even then, the policy can specify exactly what kind of access (read vs. write).

The kinds of attributes that can feed into these policies:
- **User attributes**: department, age, or other profile fields.
- **Resource attributes**: confidentiality level, owner, classification.
- **Environmental attributes**: time of day, location, device type.

Because ABAC combines many independent conditions rather than checking a single role, it is more flexible than RBAC — but that flexibility comes at a cost: it requires careful, deliberate policy management, and it's generally more complex and more prone to conflicting rules than RBAC. Note also that ABAC isn't necessarily a replacement for RBAC; the speaker points out it can be **combined** with role-based checks rather than used purely on its own.

## Access Control Lists (ACL)

Rather than granting access via roles or attribute policies, ACL attaches a **permissions list directly to a specific resource** — for example, a single document or JSON file. That list names which users may access the resource and exactly what they're allowed to do with it.

Example walked through: for one document, user Alyssa has read-only access, user Bob has both read and write access, and some other user has no access at all. Two things are being tracked simultaneously here: *which* users can touch the resource, and *what* each of those users is permitted to do with it.

ACLs are described as highly specific and user-centric. That specificity is also their weakness: they are hard to scale cleanly across systems with millions of users or objects unless managed carefully, because permissions are tracked per resource/per user rather than via a compact role or policy.

**Google Drive** is given as the canonical real-world example: when you share a Google Doc, you might give one colleague read-only access, and another colleague edit-and-comment access. That per-document, per-person permission list is exactly what ACL is. Despite the scaling concerns, Google Drive demonstrates that ACL *can* work at large scale (documents, spreadsheets, etc.) when implemented carefully.

## Enforcing Authorization: OAuth 2 and JWT

Having a model (RBAC/ABAC/ACL) describes *what the rules are*. Systems still need a mechanism to *carry and enforce* those rules on every request — that's the role of OAuth 2 and token-based schemes like JWT.

### OAuth 2 — Delegated Authorization

OAuth 2 is used when one service needs to access another service's resources **on behalf of a user**, without that user handing over their actual credentials.

Worked example: deploying an app to **Vercel**, where Vercel needs some level of control over your **GitHub** repository.
- The insecure alternative would be giving Vercel your GitHub username and password directly — this is bad because you'd be handing over full, unbounded control, with no way to limit what Vercel can actually do with those credentials.
- Instead, under OAuth 2: you (the user) initiate a request from the third-party app (Vercel) to access your GitHub repositories. You explicitly specify which repositories it can touch and which operations are permitted (create/read/update, but say, not delete). GitHub then issues an **access token** encoding exactly those approved permissions — not your password.
- OAuth 2's job, formally, is to define the **flow** for securely issuing and validating these tokens, so that delegated access can happen without ever exposing the user's actual login credentials.

### Token-Based Authorization (JWT / Bearer Tokens)

Once a user is authenticated, most systems attach a **token** — typically a JWT, sometimes called a bearer token — to represent their identity and permissions on every subsequent request. A JWT commonly carries:
- User ID
- Roles (e.g. admin, editor)
- Scopes (what specifically this token is allowed to access)
- Expiration time
- Issuer

Every request from the user carries this token to the backend, and the server checks the token's validity and then applies whatever permission logic follows from it.

**Key distinction to keep straight**: the token is just a *carrier* of identity and claims — a mechanism. The authorization model (RBAC, ABAC, etc.) is what actually *defines* what a given identity/claim set is allowed to do. Tokens transport the information; models interpret it.

## Recap of Authorization

Authorization is not the same act as authentication — authentication decides whether you get in at all, while authorization governs what you can do once you're in. The three core models — role-based, attribute-based, and access-control-list — each have distinct tradeoffs, and real systems frequently combine more than one of them (e.g., RBAC for coarse roles plus ABAC-style conditions, or RBAC plus ACL on top of shared resources) to balance flexibility against complexity. OAuth 2 and JWT are the practical plumbing that carries and enforces whatever model a given system has chosen.

# Seven Techniques for Protecting APIs

APIs act as the entry points into a system — described as "doors" — and if left unprotected, they let attackers freely access and manipulate user data and the system as a whole. Seven techniques are covered.

## 1. Rate Limiting

Rate limiting controls how many requests a given client can make within a set time window. Example: user A is allowed 100 requests over some period; the 101st request within that window is blocked, and the client must wait before the next request is allowed through.

Without rate limiting, attackers can overwhelm a system by firing thousands of requests per minute — either taking the system down outright or using the volume to brute-force data (e.g. guessing passwords or tokens by sheer repetition).

Rate limits can be applied at different granularities:
- **Per endpoint**: e.g. a `/comments` endpoint (used both to create and fetch comments) might get a stricter per-minute cap than other endpoints, since it's a common target.
- **Per user or per IP address**: each distinct IP (A, B, C for legitimate users, D for an attacker) gets its own counter. Once IP D crosses its limit (say, its 101st request), only *that* IP is blocked — legitimate users A, B, and C are unaffected.
- **Overall/global rate limiting**: this exists specifically to guard against DDoS attacks. Per-IP limiting alone isn't enough against a coordinated attack, because an attacker can spin up many bots, each individually staying under the per-IP cap (e.g. each bot sends 100 requests, staying just within its own allowed limit), while collectively they still flood the server. A global limit — some larger threshold across *all* incoming traffic regardless of source — triggers a temporary block of all requests once total traffic crosses it, buying time to investigate the root cause. (The specific numbers used, like 100 or 1,000, are just illustrative — real-world thresholds are typically much higher.)

## 2. CORS (Cross-Origin Resource Sharing)

CORS controls which domains are allowed to call your API from a browser context. Without proper CORS configuration, a malicious website could trick a user's browser into making unauthorized requests against your API using that user's browser session.

Example: if your API is meant to serve only `app.yourdomain.com`, then requests originating from that domain should be allowed, while a request coming from `app.anotherdomain.com` should be rejected outright — it should not be allowed to authenticate or pull data through your API.

## 3. SQL and NoSQL Injection Protection

Injection attacks occur when user-supplied input is inserted directly into a database query without proper handling. An attacker can craft input that alters the query's logic — for instance, injecting a fragment that **bypasses the intended checks entirely** — and use this to read, modify, or delete data, potentially affecting all user data and every table in the database.

The fix: always use **parameterized queries** or rely on **ORM safeguards**, which ensure user input is treated strictly as data and never interpreted as part of the query's executable structure.

## 4. Firewalls (and VPNs)

A firewall sits between incoming traffic and your API, filtering out malicious requests while letting legitimate traffic through. The example given is **AWS's Web Application Firewall (WAF)**, which can detect and block requests matching known attack patterns — such as suspicious SQL keywords embedded in input, or unusual/unexpected HTTP methods — while allowing normal requests to pass through untouched.

Related to this: some APIs shouldn't be reachable from the public internet at all, and should only be accessible from within a specific private network. This is where **VPNs (Virtual Private Networks)** come in. An API placed behind a VPN will reject requests from any client not connected to that same private network — a request from an ordinary internet user is blocked, while a request from someone connected to the VPN passes through and reaches the API normally. The stated use case: an internal admin dashboard, where the API backing that dashboard should only be reachable by employees connected to the company's VPN.

## 5. CSRF (Cross-Site Request Forgery) Protection

CSRF attacks trick a browser that's already logged into a service into unknowingly issuing unwanted requests to that service's API.

Worked example: imagine you're logged into your bank's system, and that system relies solely on session cookies for authentication. If the bank doesn't defend against CSRF, a malicious site could exploit your still-valid session cookie to silently submit a hidden "transfer money" request — riding on your authenticated session without your knowledge or consent.

The defense: use **CSRF tokens in combination with session cookies**. The banking system checks not just that a valid session cookie is present, but that a matching CSRF token also accompanies the request. A request lacking the correct CSRF token gets blocked even if it carries a valid session cookie, while genuine requests — which include both the cookie and the correct token — are allowed through.

## 6. XSS (Cross-Site Scripting) Protection

XSS lets an attacker inject scripts into web pages that get served to *other* users.

Worked example, step by step:
1. A comment section accepts user submissions, which get sent to the API and stored in a database. A normal comment like "nice picture" flows through fine — submitted, stored, no issue.
2. Now suppose an attacker submits a comment that instead contains a **script**. That script could be designed to do things like steal another user's cookies, or attempt to inject something further into the database.
3. If the API doesn't sanitize or validate this input, the malicious script gets written into the database just like any normal comment would.
4. Later, when *other* users load that comment section, the stored script comes back down as part of the page content — and because it wasn't neutralized, the browser executes it as real JavaScript, running the attacker's malicious code inside those other users' browsers.

This is exactly why comment content and any other user-generated input that gets rendered back to other users must be sanitized or escaped before storage and/or before rendering — otherwise the API becomes a delivery mechanism for injected scripts.

---

Source: [System Design Explained: APIs, Databases, Caching, CDNs, Load Balancing & Production Infra](https://youtu.be/oYxTTirKY8M?si=-LRByScCPEBB1Y4T) — Hayk Simonyan
