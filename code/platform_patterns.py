"""Three platform-engineering patterns from the Atlassian retrospective, runnable offline.

1. Async provisioning broker: accept fast (202), queue the work, worker does it, client polls.
2. Control plane: render proxy config from templates + context, VALIDATE before shipping it.
3. Token-bucket rate limiter: the algorithm behind most rate-limiting sidecars / gateways.
"""
import asyncio, json, string, time, uuid

# ---------------------------------------------------------------- 1. async broker (API -> queue -> worker -> DB)
DB = {}                                                  # stands in for DynamoDB

async def api_provision(queue, request):
    job_id = str(uuid.uuid4())[:8]
    DB[job_id] = {"state": "in_progress", "request": request}
    await queue.put(job_id)                              # stands in for SQS
    return 202, {"job_id": job_id, "poll": f"/v2/service_instances/{job_id}/last_operation"}

async def api_poll(job_id):
    return 200, {"state": DB[job_id]["state"]}

async def worker(queue):
    while True:
        job_id = await queue.get()
        await asyncio.sleep(0.3)                         # slow work: DNS records, CloudFront, ...
        DB[job_id]["state"] = "succeeded"
        DB[job_id]["result"] = {"hostname": f"{DB[job_id]['request']['service']}.example.net"}
        queue.task_done()

async def demo_broker():
    queue = asyncio.Queue()
    w = asyncio.create_task(worker(queue))
    t0 = time.perf_counter()
    status, body = await api_provision(queue, {"service": "billing", "plan": "public-https"})
    print(f"[broker] POST answered in {1000*(time.perf_counter()-t0):.1f} ms -> {status} {body['job_id']}")
    polls = 0
    while True:
        polls += 1
        _, s = await api_poll(body["job_id"])
        if s["state"] != "in_progress":
            break
        await asyncio.sleep(0.1)
    print(f"[broker] after {polls} polls: {s['state']} -> {DB[body['job_id']]['result']}")
    w.cancel()

# ---------------------------------------------------------------- 2. control plane: template + context + validation
ROUTE_TEMPLATE = string.Template(json.dumps({
    "name": "$service-route",
    "virtual_hosts": [{"name": "$service", "domains": ["$domain"],
                       "routes": [{"match": {"prefix": "$prefix"}, "route": {"cluster": "$cluster"}}]}]}))

KNOWN_CLUSTERS = {"billing-backend", "search-backend"}  # clusters that actually exist on the fleet

def render_route(context):
    config = json.loads(ROUTE_TEMPLATE.substitute(context))
    errors = []
    route = config["virtual_hosts"][0]["routes"][0]
    if route["route"]["cluster"] not in KNOWN_CLUSTERS:
        errors.append(f"cluster '{route['route']['cluster']}' does not exist (would black-hole traffic)")
    if not route["match"]["prefix"].startswith("/"):
        errors.append("prefix must start with '/'")
    if config["virtual_hosts"][0]["domains"][0] in {"*", ""}:
        errors.append("wildcard domain would steal traffic from every other service")
    return config, errors

def demo_control_plane():
    for ctx in [{"service": "billing", "domain": "billing.example.net", "prefix": "/", "cluster": "billing-backend"},
                {"service": "search", "domain": "*", "prefix": "api", "cluster": "serch-backend"}]:
        config, errors = render_route(ctx)
        verdict = "SHIP to proxies" if not errors else "REJECT: " + "; ".join(errors)
        print(f"[control plane] {ctx['service']:8s} -> {verdict}")

# ---------------------------------------------------------------- 3. token bucket rate limiter
class TokenBucket:
    def __init__(self, rate_per_s, burst):
        self.rate, self.capacity = rate_per_s, burst
        self.tokens, self.last = burst, 0.0

    def allow(self, now):
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)   # refill
        self.last = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True                                  # forward to backend
        return False                                     # respond 429 Too Many Requests + Retry-After

def demo_rate_limit():
    bucket = TokenBucket(rate_per_s=5, burst=10)
    # a burst of 30 requests in 1 second, then 1 request every 0.25 s
    times = [i / 30 for i in range(30)] + [1 + i * 0.25 for i in range(12)]
    allowed = [bucket.allow(t) for t in times]
    print(f"[rate limit] burst: {sum(allowed[:30])}/30 allowed, then steady: {sum(allowed[30:])}/12 allowed")

if __name__ == "__main__":
    asyncio.run(demo_broker())
    demo_control_plane()
    demo_rate_limit()
