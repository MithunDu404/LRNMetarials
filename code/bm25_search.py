"""BM25 from scratch: tokenizer, inverted index, scoring, and reciprocal-rank fusion (hybrid search)."""
import math, re
from collections import Counter, defaultdict

def tokenize(text):
    return re.findall(r"[a-z0-9][a-z0-9\-_.]*[a-z0-9]|[a-z0-9]", text.lower())

class BM25:
    def __init__(self, docs, k1=1.2, b=0.75):
        self.k1, self.b = k1, b
        self.doc_len, self.index = [], defaultdict(dict)      # term -> {doc_id: tf}
        for doc_id, text in enumerate(docs):
            counts = Counter(tokenize(text))
            self.doc_len.append(sum(counts.values()))
            for term, tf in counts.items():
                self.index[term][doc_id] = tf
        self.N = len(docs)
        self.avgdl = sum(self.doc_len) / self.N

    def idf(self, term):
        df = len(self.index.get(term, {}))
        return math.log(1 + (self.N - df + 0.5) / (df + 0.5))

    def search(self, query, k=3, explain=False):
        scores, why = defaultdict(float), defaultdict(list)
        for term in tokenize(query):
            postings = self.index.get(term)
            if not postings:
                continue                                      # only docs containing a query term are touched
            idf = self.idf(term)
            for doc_id, tf in postings.items():
                norm = 1 - self.b + self.b * self.doc_len[doc_id] / self.avgdl
                s = idf * tf * (self.k1 + 1) / (tf + self.k1 * norm)
                scores[doc_id] += s
                why[doc_id].append(f"{term}(tf={tf}, idf={idf:.2f}) +{s:.2f}")
        ranked = sorted(scores.items(), key=lambda x: -x[1])[:k]
        return [(d, round(s, 3), why[d]) if explain else (d, round(s, 3)) for d, s in ranked]

def reciprocal_rank_fusion(rankings, k=60):
    """Combine several ranked lists of doc ids (e.g. BM25 + embeddings). Higher = better."""
    fused = defaultdict(float)
    for ranking in rankings:
        for rank, doc_id in enumerate(ranking, start=1):
            fused[doc_id] += 1 / (k + rank)
    return sorted(fused, key=lambda d: -fused[d])

if __name__ == "__main__":
    docs = [
        "Error E-4012 occurs when the payment gateway times out. Retry after 30 seconds.",
        "Payment problems: our gateway sometimes fails. Contact support for payment help.",
        "Release notes: fixed error E-4011 in the login page.",
        "The payment gateway integration guide covers retries, timeouts and webhooks in detail. " * 5,
    ]
    engine = BM25(docs)
    for q in ["E-4012", "payment gateway timeout", "payment gateway times out"]:   # 3rd = agent reformulation
        print(f"\nquery: {q!r}")
        for doc_id, score, why in engine.search(q, explain=True):
            print(f"  doc {doc_id}  score {score:6.3f}   " + "; ".join(why))

    bm25_ranking = [d for d, _ in engine.search("payment gateway timeout", k=4)]
    embedding_ranking = [1, 3, 0, 2]          # pretend output of a vector search
    print("\nhybrid (RRF):", reciprocal_rank_fusion([bm25_ranking, embedding_ranking]))
