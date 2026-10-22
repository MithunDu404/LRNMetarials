"""Demos for 'AI Engineering 1 - How LLMs Work' (target/ai/).
Toy BPE tokenizer, temperature and top-p sampling, cosine similarity, and one attention step by hand.
Standard library + numpy only, no API keys.  Run:  py -3.12 code/ai_tokens_and_sampling.py
"""
from collections import Counter
import numpy as np


# ---------------------------------------------------------------- 1. Byte-pair encoding (toy)
def bpe_train(words, num_merges):
    """words: {word: count}. Each word starts as characters plus an end marker '_'."""
    vocab = {tuple(w) + ("_",): c for w, c in words.items()}
    merges = []
    for _ in range(num_merges):
        pairs = Counter()
        for sym, c in vocab.items():
            for a, b in zip(sym, sym[1:]):
                pairs[(a, b)] += c
        if not pairs:
            break
        best = max(pairs, key=pairs.get)          # most frequent adjacent pair
        merges.append((best, pairs[best]))
        new = {}
        for sym, c in vocab.items():              # replace that pair everywhere
            out, i = [], 0
            while i < len(sym):
                if i < len(sym) - 1 and (sym[i], sym[i + 1]) == best:
                    out.append(sym[i] + sym[i + 1]); i += 2
                else:
                    out.append(sym[i]); i += 1
            new[tuple(out)] = c
        vocab = new
    return merges, vocab


def demo_bpe():
    words = {"low": 5, "lower": 2, "newest": 6, "widest": 3}
    merges, vocab = bpe_train(words, 6)
    for i, (pair, n) in enumerate(merges, 1):
        print(f"merge {i}: {pair[0]!r} + {pair[1]!r} -> {pair[0] + pair[1]!r}  (seen {n} times)")
    for sym in vocab:
        print("  ", " ".join(sym))


# ---------------------------------------------------------------- 2. Temperature and top-p
def softmax(z):
    z = np.asarray(z, float); e = np.exp(z - z.max()); return e / e.sum()


def top_p_set(probs, p):
    order = np.argsort(-probs); cum = np.cumsum(probs[order])
    keep = order[: int(np.searchsorted(cum, p) + 1)]
    return keep


def demo_sampling():
    toks = ["Paris", "Lyon", "the", "France", "banana"]
    logits = np.array([2.0, 1.0, 0.5, 0.0, -1.0])
    for T in (0.5, 1.0, 2.0):
        print(f"T={T}:", " ".join(f"{t}={p:.3f}" for t, p in zip(toks, softmax(logits / T))))
    p = softmax(logits)
    keep = top_p_set(p, 0.9)
    renorm = p[keep] / p[keep].sum()
    print("top-p 0.9 keeps:", [toks[i] for i in keep], "renormalised:", np.round(renorm, 3).tolist())


# ---------------------------------------------------------------- 3. Cosine similarity
def cosine(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return float(a @ b / (np.linalg.norm(a) * np.linalg.norm(b)))


def demo_cosine():
    cat, kitten, invoice = [0.9, 0.8, 0.1], [0.85, 0.9, 0.15], [0.1, 0.05, 0.95]
    print(f"cos(cat, kitten)  = {cosine(cat, kitten):.3f}")
    print(f"cos(cat, invoice) = {cosine(cat, invoice):.3f}")


# ---------------------------------------------------------------- 4. One attention step by hand
def demo_attention():
    Q = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    K = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])
    V = np.array([[10.0, 0.0], [0.0, 10.0], [5.0, 5.0]])
    d = Q.shape[1]
    S = Q @ K.T / np.sqrt(d)
    S[np.triu_indices(3, 1)] = -np.inf                # causal mask: no peeking ahead
    A = np.vstack([softmax(r) for r in S])
    print("scores (scaled, masked):\n", np.round(S, 3))
    print("weights:\n", np.round(A, 3))
    print("outputs:\n", np.round(A @ V, 3))


if __name__ == "__main__":
    for d in (demo_bpe, demo_sampling, demo_cosine, demo_attention):
        print(f"--- {d.__name__}"); d()
