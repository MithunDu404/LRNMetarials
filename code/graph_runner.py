"""A tiny agent-graph runner: jobs, arrows (dependencies), shared state, parallelism,
an independent checker, stop rules (cap / budget / bar) and a human gate.

LLM calls are simulated with asyncio.sleep so it runs instantly and offline.
Swap `fake_llm` for a real API call to use it for real.
"""
import asyncio, random, time

random.seed(7)
COST_PER_CALL = 2                          # cents, pretend (integers avoid float rounding)


class Budget:
    def __init__(self, dollars):
        self.left = round(dollars * 100)           # store cents

    def charge(self, amount):
        if amount > self.left:
            raise RuntimeError("STOP RULE (budget): out of money")
        self.left -= amount


async def fake_llm(task, budget, seconds=1.0):
    budget.charge(COST_PER_CALL)
    await asyncio.sleep(seconds * random.uniform(0.8, 1.2) / 10)     # /10 so the demo is fast
    return f"<answer to: {task}>"


class Graph:
    def __init__(self):
        self.jobs, self.deps = {}, {}

    def job(self, name, fn, after=()):
        self.jobs[name], self.deps[name] = fn, set(after)

    async def run(self, state, parallel=True):
        done, running = set(), {}
        while len(done) < len(self.jobs):
            ready = [j for j in self.jobs if j not in done and j not in running and self.deps[j] <= done]
            if not parallel and running:
                ready = []
            for j in (ready if parallel else ready[:1]):
                running[j] = asyncio.create_task(self.jobs[j](state))
            finished, _ = await asyncio.wait(running.values(), return_when=asyncio.FIRST_COMPLETED)
            for j in [k for k, t in running.items() if t in finished]:
                running.pop(j).result()               # re-raise errors (e.g. budget stop)
                done.add(j)
        return state


def build_research_desk(budget, approve):
    g = Graph()
    angles = ["market size", "competitors", "rules & taxes", "pricing", "risks"]

    async def lead(state):
        state["angles"] = angles
        state["log"].append(await fake_llm("split question into 5 angles", budget))

    def worker(angle):
        async def run(state):
            state["findings"][angle] = await fake_llm(f"research ONLY: {angle}, cite sources", budget, seconds=3)
        return run

    async def skeptic(state):
        # independent checker with a STOP RULE: cap of 3 rounds OR quality bar reached
        quality, rounds = 0.55, 0
        while rounds < 3 and quality < 0.85:           # cap AND bar
            rounds += 1
            await fake_llm("attack every claim; flag thin or stale sources", budget)
            quality += random.uniform(0.1, 0.2)
        state["check"] = dict(rounds=rounds, quality=round(quality, 2))

    async def merge(state):
        state["brief"] = await fake_llm("merge surviving findings, source next to each claim", budget)

    async def human_gate(state):
        state["approved"] = approve(state)             # the run pauses here until a human says yes/no

    g.job("lead", lead)
    for a in angles:
        g.job(a, worker(a), after=["lead"])
    g.job("skeptic", skeptic, after=angles)
    g.job("merge", merge, after=["skeptic"])
    g.job("human_gate", human_gate, after=["merge"])
    return g


async def main():
    approve = lambda state: True                       # in real life: show the brief, wait for a click
    for parallel in (False, True):
        budget = Budget(dollars=2.00)
        state = {"log": [], "findings": {}}
        t0 = time.perf_counter()
        await build_research_desk(budget, approve).run(state, parallel=parallel)
        print(f"{'graph (parallel)' if parallel else 'straight line   '}: {time.perf_counter() - t0:.2f}s  "
              f"spent ${(200 - budget.left) / 100:.2f}  check={state['check']}  approved={state['approved']}")

    # stop rule demo: a loop with a tiny budget stops itself instead of running all night
    budget = Budget(dollars=0.10)
    try:
        for i in range(1000):
            await fake_llm("improve the draft again", budget, seconds=0.01)
    except RuntimeError as e:
        print(f"loop stopped after {i} paid calls (budget $0.10) -> {e}")


if __name__ == "__main__":
    asyncio.run(main())
