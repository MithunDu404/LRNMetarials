"""Demo for 'AI Engineering 5 - Agents' (target/ai/).
A minimal agent loop: tool schemas, argument validation with errors fed back, a human-approval
gate on a risky tool, and step limits. The "model" is a scripted stand-in (no API key).
Run:  py -3.12 code/ai_agent_loop.py
"""
import json

# ---------------------------------------------------------------- tools
ORDERS = {"4411": {"customer": "c-17", "total": 59.0, "charges": [59.0, 59.0]}}

def get_order(order_id: str):
    o = ORDERS.get(order_id)
    return {"error": f"order {order_id} not found"} if o is None else {"order_id": order_id, "total": o["total"]}

def list_charges(order_id: str):
    return {"order_id": order_id, "charges": ORDERS[order_id]["charges"]}

def issue_refund(order_id: str, amount: float):
    return {"status": "refunded", "order_id": order_id, "amount": amount}

TOOLS = {  # name -> (function, required args with types, needs human approval)
    "get_order": (get_order, {"order_id": str}, False),
    "list_charges": (list_charges, {"order_id": str}, False),
    "issue_refund": (issue_refund, {"order_id": str, "amount": float}, True),
}

def validate(name, args):
    if name not in TOOLS:
        return f"Unknown tool '{name}'. Available: {sorted(TOOLS)}."
    for arg, typ in TOOLS[name][1].items():
        if arg not in args:
            return f"Tool '{name}' is missing required argument '{arg}'."
        if not isinstance(args[arg], typ):
            return f"Argument '{arg}' must be {typ.__name__}."
    return None

def human_approves(name, args):          # in a real app: a UI prompt or a review queue
    print(f"    [approval requested] {name}({args}) -> approved by agent operator")
    return True

# ---------------------------------------------------------------- scripted "model"
SCRIPT = iter([
    {"tool": "get_order", "args": {"id": "4411"}},                       # wrong argument name
    {"tool": "get_order", "args": {"order_id": "4411"}},
    {"tool": "list_charges", "args": {"order_id": "4411"}},
    {"tool": "issue_refund", "args": {"order_id": "4411", "amount": 59.0}},
    {"final": "Order 4411 was charged twice (2 x 59.00). I refunded the duplicate 59.00."},
])

def model(messages):
    return next(SCRIPT)

# ---------------------------------------------------------------- the loop
def run_agent(task, max_steps=8):
    messages = [{"role": "user", "content": task}]
    for step in range(1, max_steps + 1):
        action = model(messages)
        if "final" in action:
            print(f"step {step}: FINAL -> {action['final']}")
            return action["final"]
        name, args = action["tool"], action["args"]
        error = validate(name, args)
        if error:
            result = {"error": error}                       # errors go back to the model as observations
        elif TOOLS[name][2] and not human_approves(name, args):
            result = {"error": "Action rejected by a human reviewer."}
        else:
            result = TOOLS[name][0](**args)
        print(f"step {step}: {name}({json.dumps(args)}) -> {result}")
        messages += [{"role": "assistant", "content": json.dumps(action)},
                     {"role": "tool", "content": json.dumps(result)}]
    return "Stopped: step limit reached without finishing."

if __name__ == "__main__":
    run_agent("Customer says order 4411 was double-charged. Check and fix it.")
