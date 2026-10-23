# Python for Backend Engineering — Interactive Quiz Log

> **Source Material:** [[py-backend|notes/py-backend.md]]  
> **Session Mode:** Continuous Mastery Evaluation  
> **Status:** Active Session  

---

> [!question] Question 1: The Global Interpreter Lock (GIL) & Workload Types
> In CPython, how does the Global Interpreter Lock (GIL) fundamentally dictate the behavior of multi-threaded (`threading.Thread`) execution across different workload types?
> 
> 1. Spawning multiple OS threads scales CPU-bound computation linearly across all available physical CPU cores.
> 2. The GIL prevents Python threads from making operating system socket calls or reading files from disk.
> 3. CPU-bound multi-threading suffers from GIL lock contention overhead, whereas I/O-bound threads release the GIL while waiting on external sockets.
> 4. The GIL only exists within asynchronous frameworks like FastAPI and does not affect synchronous scripts.
> 5. I don't know

> [!success] Question 1 — Correct ✓
> **Your Answer:** 3. CPU-bound multi-threading suffers from GIL lock contention overhead, whereas I/O-bound threads release the GIL while waiting on external sockets.  
> **Correct Answer:** 3. CPU-bound multi-threading suffers from GIL lock contention overhead, whereas I/O-bound threads release the GIL while waiting on external sockets.  
> 
> **Explanation:** In CPython, the GIL allows only one native thread to execute Python bytecode at any instant. For I/O-bound tasks, CPython releases the GIL while waiting on system-level network or disk I/O, allowing other threads to run. For CPU-bound tasks, threads constantly fight for lock acquisition, adding context-switching overhead that makes multi-threading slower than single-threaded execution.

---

> [!question] Question 2: Path Operation Declaration (`async def` vs plain `def`)
> In FastAPI, how does declaring a path operation as `async def` versus standard `def` change how the framework executes synchronous blocking operations?
> 
> 1. Both `async def` and plain `def` execute directly on the main event loop thread without thread pool offloading.
> 2. An `async def` function runs on the single-threaded event loop and blocks all concurrent traffic if it contains synchronous I/O, whereas plain `def` is automatically offloaded to an external worker thread pool.
> 3. Plain `def` functions trigger an immediate runtime `TypeError` because ASGI routers only accept coroutines.
> 4. An `async def` function automatically converts all synchronous blocking network calls into non-blocking asynchronous coroutines.
> 5. I don't know

> [!failure] Question 2 — Incorrect ✗
> **Your Answer:** 4. An `async def` function automatically converts all synchronous blocking network calls into non-blocking asynchronous coroutines.  
> **Correct Answer:** 2. An `async def` function runs on the single-threaded event loop and blocks all concurrent traffic if it contains synchronous I/O, whereas plain `def` is automatically offloaded to an external worker thread pool.  
> 
> **Diagnostic Explanation:** Python's `async def` keyword does not monkey-patch or convert synchronous blocking libraries into async coroutines. If you call synchronous I/O (`requests.get()`, `time.sleep()`, or synchronous DB drivers) inside an `async def` endpoint, it runs directly on the single-threaded event loop without yielding control (`await`), stalling the entire server for all concurrent clients. In contrast, when FastAPI encounters a standard `def` endpoint, it automatically offloads its execution to an external worker thread pool (`anyio.to_thread`), protecting the event loop.

---

> [!question] Question 3: Multi-Worker Process Topology (Gunicorn + Uvicorn)
> In a production deployment running `gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app`, how does process isolation operate across the workers?
> 
> 1. Gunicorn converts all incoming async coroutines into synchronous OS threads to ensure ACID compliance across workers.
> 2. All workers share a single global event loop instance across all physical CPU cores.
> 3. If one Uvicorn worker process encounters a blocking call, Gunicorn automatically terminates and recreates all other worker processes.
> 4. Each worker running `UvicornWorker` is an independent OS process with its own dedicated GIL and event loop, so a stall in one worker does not freeze other workers.
> 5. I don't know

> [!success] Question 3 — Correct ✓
> **Your Answer:** 4. Each worker running `UvicornWorker` is an independent OS process with its own dedicated GIL and event loop, so a stall in one worker does not freeze other workers.  
> **Correct Answer:** 4. Each worker running `UvicornWorker` is an independent OS process with its own dedicated GIL and event loop, so a stall in one worker does not freeze other workers.  
> 
> **Explanation:** Gunicorn acts as a pre-fork master process manager that spawns independent OS worker processes across CPU cores. Each Uvicorn worker process has its own separate memory space, its own GIL, and its own event loop (`uvloop`). Therefore, if one worker's event loop stalls or crashes, other workers continue processing client requests unaffected.

---

> [!question] Question 4: Pydantic v2 Parsing & Validation Behavior
> A client sends an HTTP POST request with the JSON payload `{"age": "28", "email": "alice_at_example.com"}` to a FastAPI endpoint whose body schema defines `age: int` and `email: EmailStr`. How does Pydantic v2 handle this payload?
> 
> 1. It coerces the string `"28"` into the integer `28`, but rejects the payload with an HTTP 422 Unprocessable Entity error due to invalid email formatting.
> 2. It raises an HTTP 400 Bad Request error immediately upon encountering `"28"` because string-to-int coercion is disallowed in Pydantic v2.
> 3. It accepts the payload completely, storing `"28"` as a string in the database and ignoring the missing `@` character in the email.
> 4. It converts the payload into an untyped dictionary and logs a warning to stderr without aborting the request.
> 5. I don't know

> [!failure] Question 4 — Incorrect ✗
> **Your Answer:** 2. It raises an HTTP 400 Bad Request error immediately upon encountering "28" because string-to-int coercion is disallowed in Pydantic v2.  
> **Correct Answer:** 1. It coerces the string "28" into the integer 28, but rejects the payload with an HTTP 422 Unprocessable Entity error due to invalid email formatting.  
> 
> **Diagnostic Explanation:** Pydantic is fundamentally a data parsing and coercion engine, not just a strict validator. By default, Pydantic v2 seamlessly coerces compatible types (such as parsing the numeric string `"28"` into the integer `28`). Furthermore, when validation actually fails (such as an invalid email string missing `@` for `EmailStr`), FastAPI automatically intercepts the `ValidationError` and responds with an **HTTP 422 Unprocessable Entity** status code containing detailed field locations (`loc`), rather than an HTTP 400.

---

> [!question] Question 5: Resource Lifecycle & Cleanup with `yield` Dependencies
> In FastAPI, an endpoint acquires a database session using a `yield` dependency:
> ```python
> async def get_db():
>     session = await AsyncSessionLocal()
>     try:
>         yield session
>     finally:
>         await session.close()
> ```
> If the endpoint or another dependency raises an `HTTPException(404)` during execution, what happens to the database session?
> 
> 1. The ASGI worker immediately drops the socket and leaks the session because `finally:` blocks only run on HTTP 200 responses.
> 2. The exception is swallowed silently and replaced with an HTTP 204 No Content response.
> 3. Execution unwinds back to the dependency, executing the `finally:` block to safely close and return the connection to the pool.
> 4. FastAPI automatically reroutes the failed request to a fallback synchronous thread pool to re-execute the handler.
> 5. I don't know

> [!success] Question 5 — Correct ✓
> **Your Answer:** 3. Execution unwinds back to the dependency, executing the finally: block to safely close and return the connection to the pool.  
> **Correct Answer:** 3. Execution unwinds back to the dependency, executing the finally: block to safely close and return the connection to the pool.  
> 
> **Explanation:** FastAPI implements `yield` dependencies using Python asynchronous context managers under the hood. When an exception (such as `HTTPException` or an unhandled server error) is raised inside a route or downstream dependency, execution immediately jumps into the `finally:` block after the `yield`, ensuring that database connections, transaction rollbacks, or open network sockets are reliably released back to the pool.

---

> [!question] Question 6: The Async N+1 Trap & `MissingGreenlet` in SQLAlchemy 2.0
> You execute `stmt = select(User).where(User.id == 1)` in an async FastAPI route using SQLAlchemy 2.0 with `asyncpg`. When you subsequently access `user.orders` (a one-to-many relationship) without having specified eager loading in the query, what happens?
> 
> 1. SQLAlchemy automatically pauses the coroutine and resumes it once an implicit background greenlet worker fetches the data.
> 2. It raises a `MissingGreenlet` runtime exception because lazy loading requires a synchronous database read without an `await`, which violates the non-blocking async contract.
> 3. PostgreSQL rejects the query with a transaction deadlock because async connection pools disallow relationship joins.
> 4. The attribute returns an unresolved coroutine object that must be manually passed to `asyncio.run()`.
> 5. I don't know

> [!success] Question 6 — Correct ✓
> **Your Answer:** 2. It raises a MissingGreenlet runtime exception because lazy loading requires a synchronous database read without an await, which violates the non-blocking async contract.  
> **Correct Answer:** 2. It raises a MissingGreenlet runtime exception because lazy loading requires a synchronous database read without an await, which violates the non-blocking async contract.  
> 
> **Explanation:** In Python, standard attribute access (`user.orders`) is strictly synchronous syntax—there is no place to insert an `await`. Synchronous SQLAlchemy would silently emit a blocking SQL query across the socket. In async SQLAlchemy, this transparent blocking I/O is prohibited to prevent stalling the ASGI event loop, immediately triggering a `MissingGreenlet` exception unless eager loading was requested during query definition.

---

> [!question] Question 7: Eager Loading Strategies (`selectinload` vs `joinedload`)
> When querying entities with one-to-many relationships in SQLAlchemy 2.0 (such as fetching 100 `User` records along with each user's `orders`), why is `selectinload` generally preferred over `joinedload` for collections?
> 
> 1. `joinedload` requires defining raw SQL triggers on the PostgreSQL server, while `selectinload` executes entirely in client JavaScript.
> 2. `selectinload` is only compatible with SQLite and raises an exception when executed against PostgreSQL.
> 3. `joinedload` batches child primary keys into a Redis hash, while `selectinload` writes temporary files to disk.
> 4. `joinedload` performs a SQL Cartesian join that duplicates parent row data across all matching child rows, whereas `selectinload` issues a clean second query using `WHERE user_id IN (...)` without multiplying parent data.
> 5. I don't know

> [!success] Question 7 — Correct ✓
> **Your Answer:** 4. `joinedload` performs a SQL Cartesian join that duplicates parent row data across all matching child rows, whereas `selectinload` issues a clean second query using `WHERE user_id IN (...)` without multiplying parent data.  
> **Correct Answer:** 4. `joinedload` performs a SQL Cartesian join that duplicates parent row data across all matching child rows, whereas `selectinload` issues a clean second query using `WHERE user_id IN (...)` without multiplying parent data.  
> 
> **Explanation:** For 1-to-many collections, a SQL `LEFT OUTER JOIN` duplicates all parent columns for every matching child row, causing massive network bandwidth overhead and complex client-side deduplication. In contrast, `selectinload` runs two highly optimized queries: first fetching the parent records, then fetching all related children in a single query using `WHERE parent_id IN (...)`, assembling the objects cleanly in memory.

---

> [!question] Question 8: Password Hashing Mechanics (SHA-256 vs Argon2 / Bcrypt)
> Why is storing user passwords using SHA-256 or MD5 considered a severe security vulnerability compared to using adaptive hashing algorithms like Argon2 or bcrypt?
> 
> 1. SHA-256 hashes exceed the maximum column length supported by PostgreSQL text fields.
> 2. Modern web browsers automatically reject cookies or tokens containing SHA-256 hexadecimal digests.
> 3. Fast algorithms like SHA-256 allow modern GPUs to compute billions of guesses per second, whereas Argon2 and bcrypt incorporate adaptive work factors and automatic salting to make brute-force cracking computationally prohibitive.
> 4. SHA-256 is an asymmetric encryption cipher that requires storing the private decryption key directly in the database.
> 5. I don't know

> [!success] Question 8 — Correct ✓
> **Your Answer:** 3. Fast algorithms like SHA-256 allow modern GPUs to compute billions of guesses per second, whereas Argon2 and bcrypt incorporate adaptive work factors and automatic salting to make brute-force cracking computationally prohibitive.  
> **Correct Answer:** 3. Fast algorithms like SHA-256 allow modern GPUs to compute billions of guesses per second, whereas Argon2 and bcrypt incorporate adaptive work factors and automatic salting to make brute-force cracking computationally prohibitive.  
> 
> **Explanation:** General-purpose cryptographic hash functions like SHA-256 or MD5 were engineered for raw speed and data integrity, not password storage. Modern GPUs can calculate billions of SHA-256 hashes per second, making rainbow table and brute-force dictionary attacks trivial. In contrast, password hashing algorithms like bcrypt and Argon2id are intentionally slow and memory-hard, with configurable cost factors and automatic per-password salts that render mass offline attacks computationally unfeasible.

---

> [!question] Question 9: Stateless JWTs vs In-Memory Session Storage
> A team proposes replacing stateless JSON Web Tokens (JWT) with an in-memory dictionary (`sessions[session_id] = user_data`) inside a FastAPI application deployed with `gunicorn -w 4 -k uvicorn.workers.UvicornWorker`. What fundamental architectural problem will occur?
> 
> 1. Python dictionaries automatically serialize to disk on every write, causing severe disk I/O latency.
> 2. Because process memory is strictly private to each OS worker, a user authenticated on Worker 1 will appear unauthenticated whenever subsequent requests hit Worker 2, 3, or 4.
> 3. PostgreSQL transactions will automatically abort whenever server memory dictionaries exceed 64 megabytes.
> 4. The ASGI specification requires all in-memory session dictionaries to be encrypted with an RSA 4096-bit key.
> 5. I don't know

> [!success] Question 9 — Correct ✓
> **Your Answer:** 2. Because process memory is strictly private to each OS worker, a user authenticated on Worker 1 will appear unauthenticated whenever subsequent requests hit Worker 2, 3, or 4.  
> **Correct Answer:** 2. Because process memory is strictly private to each OS worker, a user authenticated on Worker 1 will appear unauthenticated whenever subsequent requests hit Worker 2, 3, or 4.  
> 
> **Explanation:** Operating system processes have completely isolated virtual memory spaces. In a multi-worker or multi-container environment, state stored in a Python in-memory dictionary is inaccessible to other workers. Stateless JSON Web Tokens (JWTs) solve this by cryptographically signing user claims into a self-contained string, allowing any worker process holding the shared secret key to verify authenticity without needing shared in-memory session state or sticky routing.

---

> [!question] Question 10: Task Offloading Architecture (`BackgroundTasks` vs Celery)
> An application needs to perform two distinct asynchronous operations:
> 1. Sending a quick transactional email via an external REST API (takes ~50ms).
> 2. Generating a complex multi-page PDF report that consumes 100% CPU for 8 seconds.
> 
> What is the recommended architectural allocation between FastAPI's `BackgroundTasks` and a Celery + Redis worker tier?
> 
> 1. Both operations must run inside `BackgroundTasks` because Celery only supports synchronous Flask applications.
> 2. The CPU-intensive PDF report should run in `BackgroundTasks` while the email must run in Celery due to SMTP network restrictions.
> 3. The lightweight email can run in `BackgroundTasks` directly after response delivery, whereas the CPU-intensive PDF generation should be dispatched to dedicated Celery workers via Redis.
> 4. Neither should run asynchronously; both operations should execute directly in the primary request handler before returning an HTTP 200 response.
> 5. I don't know

> [!success] Question 10 — Correct ✓
> **Your Answer:** 3. The lightweight email can run in BackgroundTasks directly after response delivery, whereas the CPU-intensive PDF generation should be dispatched to dedicated Celery workers via Redis.  
> **Correct Answer:** 3. The lightweight email can run in BackgroundTasks directly after response delivery, whereas the CPU-intensive PDF generation should be dispatched to dedicated Celery workers via Redis.  
> 
> **Explanation:** FastAPI's `BackgroundTasks` executes in-process on the same server worker immediately after delivering the HTTP response. For quick, non-critical I/O jobs (such as sending an email or writing an audit record), it incurs zero infrastructure overhead. However, executing CPU-heavy tasks like PDF rendering in `BackgroundTasks` monopolizes the web server process, causing latency spikes for all concurrent API requests. Heavy or critical jobs should be queued via Redis to dedicated Celery workers that scale independently and offer persistent task retries.

---

> [!question] Question 11: Redis Cache-Aside & Time-To-Live (TTL)
> When implementing the Cache-Aside pattern with Redis (`redis.set(cache_key, json_data, ex=300)`), why is configuring an explicit Time-To-Live (`ex=300`) considered mandatory in production?
> 
> 1. It prevents stale data from permanently accumulating in Redis memory and provides an automatic recovery bound against missed cache invalidation events.
> 2. It triggers Redis to automatically encrypt stored values with AES-256 after the time window expires.
> 3. It commands PostgreSQL to archive matching table rows into compressed cold storage.
> 4. It forces connected client web browsers to purge their local HTTP cookies every 300 seconds.
> 5. I don't know

> [!success] Question 11 — Correct ✓
> **Your Answer:** 1. It prevents stale data from permanently accumulating in Redis memory and provides an automatic recovery bound against missed cache invalidation events.  
> **Correct Answer:** 1. It prevents stale data from permanently accumulating in Redis memory and provides an automatic recovery bound against missed cache invalidation events.  
> 
> **Explanation:** Redis is an in-memory database with finite RAM. Setting a TTL guarantees that keys expire and memory is reclaimed even if an explicit invalidation trigger (e.g. after a DB update) fails or is omitted. Furthermore, TTL acts as a circuit-breaker against the "cache stampede" / permanently stale cache problem by guaranteeing that the data will eventually be re-queried from the primary source of truth (PostgreSQL).

---

> [!question] Question 12: Kubernetes Probes (Liveness vs Readiness)
> Why is it considered an architectural anti-pattern to query the database and Redis inside a Kubernetes Liveness Probe (`/healthz`), rather than confining external dependency checks strictly to the Readiness Probe (`/ready`)?
> 
> 1. Kubernetes strictly disallows HTTP GET requests for liveness probes and permits only raw TCP socket pings.
> 2. PostgreSQL permanently locks active tables if its connection pool receives automated health pings.
> 3. Database drivers cannot be executed within asynchronous FastAPI route handlers.
> 4. If a temporary database blip occurs, failing liveness probes cause Kubernetes to terminate and restart healthy application containers in a cascading reboot loop, whereas failing readiness probes only divert traffic away until connectivity recovers.
> 5. I don't know

> [!success] Question 12 — Correct ✓
> **Your Answer:** 4. If a temporary database blip occurs, failing liveness probes cause Kubernetes to terminate and restart healthy application containers in a cascading reboot loop, whereas failing readiness probes only divert traffic away until connectivity recovers.  
> **Correct Answer:** 4. If a temporary database blip occurs, failing liveness probes cause Kubernetes to terminate and restart healthy application containers in a cascading reboot loop, whereas failing readiness probes only divert traffic away until connectivity recovers.  
> 
> **Explanation:** Liveness probes (`/healthz`) verify that the Python process is alive and not stuck in a deadlock; if it fails, the orchestrator immediately kills and restarts the container. Readiness probes (`/ready`) verify that all backing downstream dependencies (PostgreSQL, Redis) are healthy and ready to serve traffic. If a database restarts or suffers temporary packet loss, a failing readiness probe simply tells the ingress load balancer to stop sending traffic to the pod until it recovers, preventing cascading container reboot storms.

---

> [!question] Question 13: Observability & Correlation IDs (`X-Request-ID`)
> In a high-throughput FastAPI application running across multiple worker processes with thousands of concurrent asynchronous requests, what primary problem does generating and logging a unique `X-Request-ID` (Correlation ID) solve?
> 
> 1. It enables Gzip stream compression on all outbound JSON payloads to conserve network bandwidth.
> 2. It allows developers to isolate and trace a single request's complete execution lifecycle across asynchronous, interleaved multi-worker log streams.
> 3. It assigns a dedicated physical hardware thread to each request, bypassing the CPython Global Interpreter Lock.
> 4. It commands client web browsers to cache the API response locally for 24 hours.
> 5. I don't know

> [!success] Question 13 — Correct ✓
> **Your Answer:** 2. It allows developers to isolate and trace a single request's complete execution lifecycle across asynchronous, interleaved multi-worker log streams.  
> **Correct Answer:** 2. It allows developers to isolate and trace a single request's complete execution lifecycle across asynchronous, interleaved multi-worker log streams.  
> 
> **Explanation:** Because an ASGI event loop processes hundreds of concurrent requests simultaneously across multiple worker processes, standard log outputs arrive interleaved and jumbled. Attaching an `X-Request-ID` (Correlation ID) to every incoming request via middleware and propagating it through all log messages allows engineering teams to filter log aggregators (e.g., Datadog, Elasticsearch) by a single UUID and inspect the full end-to-end execution path of any failing or slow request.

---

> [!question] Question 14: Production Containerization & Multi-Stage Docker Builds
> In production Python backend engineering, a Dockerfile splits into a `builder` stage (which installs `build-essential` and compiles C extensions like `asyncpg`) and a `runner` stage (which copies `/opt/venv` into a slim image and executes as `USER appuser`). Why is this separation considered a mandatory security and operational standard?
> 
> 1. Python bytecode cannot execute on Linux unless compiled into a standalone native binary in an Alpine container.
> 2. The Gunicorn master process refuses to bind to port 8000 if executed with administrative root permissions.
> 3. It minimizes production container size and drastically reduces vulnerability exposure by removing build-time C compilers, headers, and root execution rights from the production runtime image.
> 4. Multi-stage builds are required by the Docker daemon to enable asynchronous socket binding on port 8000.
> 5. I don't know

> [!success] Question 14 — Correct ✓
> **Your Answer:** 3. It minimizes production container size and drastically reduces vulnerability exposure by removing build-time C compilers, headers, and root execution rights from the production runtime image.  
> **Correct Answer:** 3. It minimizes production container size and drastically reduces vulnerability exposure by removing build-time C compilers, headers, and root execution rights from the production runtime image.  
> 
> **Explanation:** Compiling Python C-extensions (like `asyncpg` or cryptography packages) requires heavy toolchains (`gcc`, `g++`, `libpq-dev`). Leaving these compilers in production containers bloats images to over 1GB and provides attackers with instant local privilege-escalation and compilation tools if remote code execution occurs. Multi-stage builds compile packages in a temporary `builder` stage, copying only clean runtime artifacts into a minimal runner image that executes as an unprivileged, non-root user.

---

> [!question] Question 15: Handling Synchronous Legacy Libraries in FastAPI
> An engineering team must integrate a legacy third-party payment SDK (`payment_sdk.process_charge()`) that performs synchronous blocking network I/O. How should the FastAPI path operation function be defined to prevent stalling the ASGI event loop for all concurrent users?
> 
> 1. Declare the endpoint as standard `def process_payment(...)` so FastAPI automatically offloads its execution to an external worker thread pool.
> 2. Declare the endpoint as `async def process_payment(...)` without changes, relying on the event loop to automatically spawn threads for synchronous functions.
> 3. Wrap the synchronous SDK call in an infinite `while True:` loop inside an `async def` coroutine.
> 4. Synchronous libraries cannot be executed within FastAPI under any circumstances and must be rewritten in C.
> 5. I don't know

> [!success] Question 15 — Correct ✓ (Corrected Selection)
> **Your Answer:** 1. Declare the endpoint as standard def process_payment(...) so FastAPI automatically offloads its execution to an external worker thread pool. *(User immediate correction)*  
> **Correct Answer:** 1. Declare the endpoint as standard def process_payment(...) so FastAPI automatically offloads its execution to an external worker thread pool.  
> 
> **Explanation:** This is FastAPI's pragmatic superpower. When you declare an endpoint with standard `def` (instead of `async def`), FastAPI recognizes that the code may perform synchronous blocking I/O (like legacy SDKs, `open()`, or `requests.get()`) and automatically offloads the entire function execution to an external worker thread pool (`anyio.to_thread.run_sync`). This keeps the single-threaded event loop completely unblocked and free to process concurrent requests.

---

> [!question] Question 16: Security & Data Filtering via `response_model`
> A database table model `User` contains sensitive attributes: `id`, `email`, `hashed_password`, `two_factor_secret`, and `is_active`. An endpoint is declared as follows:
> ```python
> class UserPublic(BaseModel):
>     id: int
>     email: EmailStr
>     is_active: bool
> 
> @app.get("/users/{user_id}", response_model=UserPublic)
> async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
>     user = await db.get(User, user_id)
>     return user  # returns full ORM object
> ```
> What does the client receive in the HTTP response?
> 
> 1. An HTTP 500 Internal Server Error because the ORM object contains attributes not defined in `UserPublic`.
> 2. A JSON response containing all database fields including `hashed_password` and `two_factor_secret`.
> 3. An HTTP 422 Unprocessable Entity error indicating an output schema mismatch.
> 4. A JSON response containing strictly `id`, `email`, and `is_active`, because FastAPI uses `response_model` to filter out any undeclared fields.
> 5. I don't know

> [!success] Question 16 — Correct ✓
> **Your Answer:** 4. A JSON response containing strictly id, email, and is_active, because FastAPI uses response_model to filter out any undeclared fields.  
> **Correct Answer:** 4. A JSON response containing strictly id, email, and is_active, because FastAPI uses response_model to filter out any undeclared fields.  
> 
> **Explanation:** FastAPI's `response_model` acts as an outbound firewall. Even when you return an ORM instance or dictionary containing sensitive database columns (`hashed_password`, `two_factor_secret`, internal foreign keys), FastAPI serializes the return value strictly against the fields declared in `UserPublic`. Any attribute not explicitly specified in the `response_model` is stripped before generating the HTTP JSON response, guaranteeing zero accidental data leakage.

---

> [!question] Question 17: Database Connection Pooling & `pool_pre_ping`
> When configuring an asynchronous database engine in SQLAlchemy 2.0 (`create_async_engine("postgresql+asyncpg://...", pool_pre_ping=True)`), what specific operational issue does `pool_pre_ping=True` prevent?
> 
> 1. It automatically scales database CPU cores whenever incoming query traffic surges.
> 2. It compiles raw SQL queries into WebAssembly binaries prior to socket transmission.
> 3. It executes a lightweight check query upon connection checkout to detect and replace stale or dropped connections closed by database idle timeouts or firewall resets.
> 4. It eliminates the need for database passwords by authenticating pooled sockets using IP address whitelisting.
> 5. I don't know

> [!question] Question 17 — Skipped (I don't know)
> **Your Answer:** 5. I don't know  
> **Correct Answer:** 3. It executes a lightweight check query upon connection checkout to detect and replace stale or dropped connections closed by database idle timeouts or firewall resets.  
> 
> **Diagnostic Explanation:** In cloud environments (e.g., AWS RDS, Supabase, Azure), load balancers, firewalls, and database servers enforce idle connection timeouts, silently dropping idle TCP sockets after a few minutes. Without `pool_pre_ping=True`, the connection pool would hand a dead socket to an incoming request, causing unexpected `OperationalError: connection closed` or `ConnectionResetError` crashes. With `pool_pre_ping=True`, SQLAlchemy executes a rapid probe (`SELECT 1`) when checking out a connection from the pool; if the probe fails, it transparently recycles the connection and establishes a fresh one without disrupting the user request.

---

> [!question] Question 18: Database Schema Migrations with Alembic
> Why do production engineering teams manage database schemas using Alembic migrations rather than running manual `ALTER TABLE` commands or calling `Base.metadata.create_all()` on server startup?
> 
> 1. Manual `ALTER TABLE` commands cause PostgreSQL to permanently drop table indexes.
> 2. Alembic provides version-controlled, auditable migration scripts that can be tested in staging, run predictably in automated CI/CD pipelines, and rolled back if a deployment fails.
> 3. Modern asynchronous database drivers like `asyncpg` refuse to connect to tables not created through Alembic metadata.
> 4. Alembic converts relational SQL schemas into NoSQL JSON documents on the fly to accelerate read throughput.
> 5. I don't know
