"""Demo for 'AI Engineering 3 - Evals and Quality' (target/ai/).
A tiny eval harness: deterministic checks, a pass rate with a confidence interval,
and agreement between an LLM judge and human labels (Cohen's kappa, TPR/TNR, corrected pass rate).
Standard library only, no API keys.  Run:  py -3.12 code/ai_eval_harness.py
"""
import json, math, re

# ---------------------------------------------------------------- 1. Deterministic checks
CASES = [  # (input id, model output) for a "answer with a citation, as JSON" task
    ("q1", '{"answer": "Refunds take 5 days.", "source": "policy.md#refunds"}'),
    ("q2", '{"answer": "Yes, you can cancel anytime.", "source": "terms.md#cancel"}'),
    ("q3", 'Refunds usually take a week.'),                                           # not JSON
    ("q4", '{"answer": "Contact support.", "source": ""}'),                            # no citation
    ("q5", '{"answer": "As an AI language model, I cannot say.", "source": "faq.md"}'),  # banned phrase
    ("q6", '{"answer": "Plans renew monthly.", "source": "billing.md#renewal"}'),
]

def checks(output):
    try:
        d = json.loads(output)
    except json.JSONDecodeError:
        return {"valid_json": False}
    return {
        "valid_json": True,
        "has_citation": bool(re.fullmatch(r"[\w\-]+\.md(#[\w\-]+)?", d.get("source", ""))),
        "no_banned_phrase": "as an ai language model" not in d.get("answer", "").lower(),
        "short_enough": len(d.get("answer", "")) <= 200,
    }

def wilson(k, n, z=1.96):
    p = k / n; den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return c - h, c + h

def demo_checks():
    passed = 0
    for cid, out in CASES:
        r = checks(out); ok = all(r.values()) and len(r) == 4
        passed += ok
        failed = [k for k, v in r.items() if not v]
        print(f"{cid}: {'PASS' if ok else 'FAIL'} {failed if failed else ''}")
    lo, hi = wilson(passed, len(CASES))
    print(f"pass rate {passed}/{len(CASES)} = {passed/len(CASES):.0%}, 95% CI {lo:.0%}-{hi:.0%}  <- 6 cases tell you very little")
    lo, hi = wilson(80, 100)
    print(f"for comparison, 80/100: 95% CI {lo:.1%}-{hi:.1%}")

# ---------------------------------------------------------------- 2. Judge vs human agreement
def demo_judge_agreement():
    # 100 traces labelled by a human expert and by an LLM judge (1 = pass)
    both_pass, both_fail, judge_pass_human_fail, judge_fail_human_pass = 70, 15, 10, 5
    n = both_pass + both_fail + judge_pass_human_fail + judge_fail_human_pass
    po = (both_pass + both_fail) / n
    judge_pass = (both_pass + judge_pass_human_fail) / n
    human_pass = (both_pass + judge_fail_human_pass) / n
    pe = judge_pass * human_pass + (1 - judge_pass) * (1 - human_pass)
    kappa = (po - pe) / (1 - pe)
    tpr = both_pass / (both_pass + judge_fail_human_pass)        # judge says pass when human says pass
    tnr = both_fail / (both_fail + judge_pass_human_fail)        # judge says fail when human says fail
    print(f"raw agreement {po:.2f}, chance agreement {pe:.2f}, Cohen's kappa {kappa:.3f}")
    print(f"judge TPR {tpr:.3f}, TNR {tnr:.3f}")
    q = 0.80   # judge-measured pass rate on a new, unlabelled batch
    corrected = (q - (1 - tnr)) / (tpr + tnr - 1)
    print(f"judge reports {q:.0%} pass on a new batch -> corrected estimate {corrected:.1%}")

if __name__ == "__main__":
    for d in (demo_checks, demo_judge_agreement):
        print(f"--- {d.__name__}"); d()
