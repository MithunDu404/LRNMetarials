"""Demo for 'AI Engineering 4 - Retrieval and RAG' (target/ai/).
BM25 keyword search, a toy "embedding" search, reciprocal rank fusion, and retrieval metrics.
The embedding is a hand-made concept vector (a stand-in for a real embedding model), so this
runs offline.  Run:  py -3.12 code/ai_hybrid_retrieval.py
"""
import math, re
from collections import Counter

DOCS = {
    "d1": "Refund policy: you can get your money back within 30 days of purchase.",
    "d2": "Error code E1043 means the payment card was declined by the bank.",
    "d3": "To reset your password, open Settings and choose Security.",
    "d4": "Shipping takes 3 to 5 business days within the EU.",
    "d5": "Reimbursement requests for damaged items are handled by the returns team.",
    "d6": "Card payments may fail if the billing address does not match.",
    "d7": "Our office is closed on public holidays.",
    "d8": "Error E2001: an upload error occurs when the file exceeds 50 MB.",
}
QUERIES = {  # query -> relevant docs (graded: 2 = answers it, 1 = related)
    "how do I get a refund for broken goods": {"d1": 2, "d5": 2},
    "what does E1043 mean": {"d2": 2},
    "my card payment keeps failing": {"d2": 1, "d6": 2},
}

STOP = {"a", "an", "and", "are", "by", "can", "do", "does", "for", "get", "how", "i", "if", "is", "it", "keeps",
        "mean", "my", "not", "of", "on", "our", "the", "to", "what", "when", "within", "you", "your"}

def tok(text):
    return [w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in STOP]

# ---------------------------------------------------------------- BM25
class BM25:
    def __init__(self, docs, k1=1.2, b=0.75):
        self.ids = list(docs); self.toks = {i: tok(t) for i, t in docs.items()}
        self.k1, self.b = k1, b
        self.avg = sum(len(t) for t in self.toks.values()) / len(docs)
        df = Counter(w for t in self.toks.values() for w in set(t))
        n = len(docs)
        self.idf = {w: math.log(1 + (n - c + 0.5) / (c + 0.5)) for w, c in df.items()}

    def scores(self, query):
        out = {}
        for i, t in self.toks.items():
            tf = Counter(t); s = 0.0
            for w in tok(query):
                if w in tf:
                    f = tf[w]
                    s += self.idf[w] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * len(t) / self.avg))
            out[i] = s
        return out

# ---------------------------------------------------------------- toy dense "embedding"
CONCEPTS = {
    "refund": {"refund", "money", "back", "reimbursement", "reimburse", "returns"},
    "payment": {"payment", "payments", "card", "declined", "billing", "pay"},
    "error": {"error", "code", "e1043", "e2001", "fail", "fails", "failing", "occurs"},
    "damage": {"damaged", "broken", "faulty"},
    "account": {"password", "reset", "settings", "security"},
    "shipping": {"shipping", "days", "delivery"},
    "office": {"office", "holidays", "closed"},
    "upload": {"upload", "mb", "exceeds"},
}
def embed(text):
    t = tok(text)
    v = [sum(w in words for w in t) for words in CONCEPTS.values()]
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]

def dense_scores(query):
    q = embed(query)
    return {i: sum(a * b for a, b in zip(q, embed(t))) for i, t in DOCS.items()}

# ---------------------------------------------------------------- fusion + metrics
def ranking(scores):
    return [i for i, s in sorted(scores.items(), key=lambda kv: -kv[1]) if s > 0]

def rrf(rankings, k=60):
    fused = Counter()
    for r in rankings:
        for pos, i in enumerate(r, 1):
            fused[i] += 1 / (k + pos)
    return [i for i, _ in fused.most_common()]

def recall_at(r, rel, k): return len(set(r[:k]) & set(rel)) / len(rel)
def mrr(r, rel): return next((1 / p for p, i in enumerate(r, 1) if i in rel), 0.0)
def ndcg_at(r, rel, k):
    dcg = sum((2 ** rel.get(i, 0) - 1) / math.log2(p + 1) for p, i in enumerate(r[:k], 1))
    ideal = sorted(rel.values(), reverse=True)[:k]
    idcg = sum((2 ** g - 1) / math.log2(p + 1) for p, g in enumerate(ideal, 1))
    return dcg / idcg

if __name__ == "__main__":
    bm = BM25(DOCS); totals = {m: [0, 0, 0] for m in ("BM25", "vector", "hybrid")}
    for q, rel in QUERIES.items():
        rb, rv = ranking(bm.scores(q)), ranking(dense_scores(q))
        rh = rrf([rb, rv])
        print(f"\nQ: {q!r}   relevant: {sorted(rel)}")
        for name, r in (("BM25", rb), ("vector", rv), ("hybrid", rh)):
            m = (recall_at(r, rel, 2), mrr(r, rel), ndcg_at(r, rel, 3))
            for j in range(3): totals[name][j] += m[j] / len(QUERIES)
            print(f"  {name:6s} top-3 {r[:3]}  recall@2={m[0]:.2f}  MRR={m[1]:.2f}  nDCG@3={m[2]:.2f}")
    print("\nAverage over the 3 queries:")
    for name, (rc, mr, nd) in totals.items():
        print(f"  {name:6s} recall@2={rc:.2f}  MRR={mr:.2f}  nDCG@3={nd:.2f}")
