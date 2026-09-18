"""A minimal "harness v1": agent spec + tools + skills + sub-agents + context compilation + limits + compaction.

The "LLM" is a tiny scripted policy so this runs offline and deterministically.
Replace `fake_llm` with a real chat-completion call (returning the same JSON-ish dict) to make it real.
"""
import json, re

# ----------------------------------------------------------------------------- tools (JSON-schema style specs)
TOOLS = {
    "calculator": {"description": "Evaluate + - * / on numbers exactly.", "params": {"expr": "string"}},
    "read_file":  {"description": "Read a file from the sandbox.",        "params": {"path": "string"}},
    "spawn_subagent": {"description": "Run a sub-agent on a sub-task; returns only its final answer.",
                       "params": {"task": "string"}},
}
FILES = {"prices.txt": "apples 3\npears 5\n" + "noise line\n" * 400}      # a big file: context pressure
SKILLS = {"shopping_total": "1) read prices.txt  2) multiply each quantity by price  3) add with calculator"}

def run_tool(name, args, depth):
    if name == "calculator":
        if not re.fullmatch(r"[\d+\-*/(). ]+", args["expr"]):
            return "error: invalid expression"
        return str(eval(args["expr"]))                                  # safe: digits and operators only
    if name == "read_file":
        return FILES.get(args["path"], "error: no such file")
    if name == "spawn_subagent":
        return Agent(depth=depth + 1).run(args["task"])                 # sub-agent has its OWN context
    return "error: unknown tool"

# ----------------------------------------------------------------------------- scripted stand-in for an LLM
def fake_llm(context):
    """Decide the next action from the compiled context (a real LLM does this with next-token prediction)."""
    last = context[-1]["content"]
    task = context[1]["content"]
    if "prices" in task and not any("apples 3" in m["content"] for m in context):
        if "SUBAGENT" not in task:                                      # parent delegates the noisy file reading
            return {"tool": "spawn_subagent", "args": {"task": "SUBAGENT: extract prices from prices.txt"}}
        return {"tool": "read_file", "args": {"path": "prices.txt"}}
    if task.startswith("SUBAGENT"):
        found = re.findall(r"(apples|pears) (\d+)", " ".join(m["content"] for m in context))
        return {"final": ", ".join(f"{a} {b}" for a, b in found)}
    if not last.lstrip("-").isdigit():
        prices = dict(re.findall(r"(apples|pears) (\d+)", " ".join(m["content"] for m in context)))
        return {"tool": "calculator", "args": {"expr": f"4*{prices['apples']} + 2*{prices['pears']}"}}
    return {"final": f"Total cost is {last}"}

# ----------------------------------------------------------------------------- the harness loop
class Agent:
    def __init__(self, depth=0, max_turns=8, max_context_chars=4000):
        self.depth, self.max_turns, self.max_context_chars = depth, max_turns, max_context_chars
        self.tool_calls, self.compactions = 0, 0

    def compile_context(self, history):
        system = (f"You are a careful assistant (depth {self.depth}). Tools: {json.dumps(TOOLS)}. "
                  f"Skills: {json.dumps(SKILLS)}. Limits: {self.max_turns} turns.")
        return [{"role": "system", "content": system}] + history

    def compact(self, history):
        """Replace old, bulky tool outputs with a short summary (a real harness asks the LLM to summarize)."""
        self.compactions += 1
        return [history[0]] + [{"role": m["role"], "content": (m["content"][:120] + " …[compacted]")
                                if len(m["content"]) > 200 else m["content"]} for m in history[1:]]

    def run(self, task):
        history = [{"role": "user", "content": task}]
        for turn in range(self.max_turns):                               # STOP RULE: turn cap
            context = self.compile_context(history)
            if sum(len(m["content"]) for m in context) > self.max_context_chars:
                history = self.compact(history)
                context = self.compile_context(history)
            action = fake_llm(context)
            if "final" in action:
                indent = "  " * self.depth
                print(f"{indent}[depth {self.depth}] done in {turn + 1} turns, {self.tool_calls} tool calls, "
                      f"{self.compactions} compactions, context {sum(len(m['content']) for m in context)} chars")
                return action["final"]
            self.tool_calls += 1
            result = run_tool(action["tool"], action["args"], self.depth)
            history += [{"role": "assistant", "content": f"call {action['tool']}({action['args']})"},
                        {"role": "tool", "content": result}]                 # append tool result, loop again
        return "stopped: turn limit reached"

if __name__ == "__main__":
    answer = Agent().run("I buy 4 apples and 2 pears; use prices.txt. What is the total?")
    print("final answer:", answer)
