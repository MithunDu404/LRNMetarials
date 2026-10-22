"""Demo for 'AI Engineering 2 - Prompting and Context Engineering' (target/ai/).
Validate a model's JSON against a schema and retry with the error message fed back.
The "model" is a scripted stand-in, so this runs offline with no API key.
Run:  py -3.12 code/ai_structured_output.py
"""
import json

SCHEMA = {
    "required": {"category": str, "priority": int, "summary": str},
    "enums": {"category": {"billing", "bug", "feature_request", "other"}},
    "ranges": {"priority": (1, 4)},
}


def validate(text):
    """Return (data, None) if valid, else (None, error message for the model)."""
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        return None, f"Output was not valid JSON ({e.msg} at char {e.pos}). Return only a JSON object."
    for field, typ in SCHEMA["required"].items():
        if field not in data:
            return None, f"Missing required field '{field}'."
        if not isinstance(data[field], typ):
            return None, f"Field '{field}' must be {typ.__name__}, got {type(data[field]).__name__}."
    for field, allowed in SCHEMA["enums"].items():
        if data[field] not in allowed:
            return None, f"Field '{field}' must be one of {sorted(allowed)}, got {data[field]!r}."
    for field, (lo, hi) in SCHEMA["ranges"].items():
        if not lo <= data[field] <= hi:
            return None, f"Field '{field}' must be between {lo} and {hi}."
    return data, None


SCRIPTED_REPLIES = iter([
    'Sure! Here is the JSON: {"category": "billing", "priority": 2}',          # chatty + invalid
    '{"category": "payments", "priority": 2, "summary": "Double charge"}',     # bad enum value
    '{"category": "billing", "priority": 2, "summary": "Customer was charged twice for one order"}',
])


def fake_model(messages):
    return next(SCRIPTED_REPLIES)


def classify(ticket, max_attempts=3):
    messages = [
        {"role": "system", "content": "Classify support tickets. Reply with only a JSON object."},
        {"role": "user", "content": f"<ticket>{ticket}</ticket>"},
    ]
    for attempt in range(1, max_attempts + 1):
        reply = fake_model(messages)
        data, error = validate(reply)
        print(f"attempt {attempt}: {'OK' if data else 'INVALID'} -> {error or data}")
        if data:
            return data
        messages += [{"role": "assistant", "content": reply},
                     {"role": "user", "content": f"Your reply was invalid: {error} Try again."}]
    raise ValueError("no valid output after retries")


if __name__ == "__main__":
    classify("I was charged twice for order #4411, please refund one.")
