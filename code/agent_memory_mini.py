"""A miniature Mem0-style long-term memory: ingestion with dedup + entity links, and hybrid retrieval.

Stand-ins so it runs with no downloads:
  * "embedding" = character-trigram TF vector + cosine similarity (a real model would use e.g. a sentence-transformer)
  * "LLM extractor" = the caller passes already-extracted memory sentences
  * "entity extractor" = capitalized words (a real system would use an NER model or an LLM)
"""
import hashlib, math, re
from collections import Counter, defaultdict
from datetime import date

def lemmatize(text):                         # crude lemmatizer: lowercase + strip plural 's'
    return [w[:-1] if len(w) > 3 and w.endswith("s") else w for w in re.findall(r"[a-z0-9]+", text.lower())]

def embed(text):
    t = f"  {text.lower()}  "
    return Counter(t[i:i + 3] for i in range(len(t) - 2))

def cosine(a, b):
    dot = sum(a[k] * b.get(k, 0) for k in a)
    return dot / (math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values())) + 1e-9)

def entities(text):
    return {w for w in re.findall(r"\b[A-Z][a-zA-Z]+\b", text) if w not in {"The", "User", "I", "My", "What", "Where", "Which", "Any"}}

class MemoryStore:
    def __init__(self):
        self.memories = []                   # main store: text + metadata + vector
        self.entity_links = defaultdict(set) # entity store: entity -> memory ids
        self.history = []                    # "SQLite": change log
        self.hashes = set()

    # ---------------------------------------------------------------- ingestion
    def add(self, text, owner="user", agent="assistant-1"):
        h = hashlib.md5(text.strip().lower().encode()).hexdigest()
        if h in self.hashes:                 # exact-hash dedup (weak: paraphrases slip through)
            self.history.append(("SKIP_DUPLICATE", text)); return None
        mid = len(self.memories)
        self.memories.append(dict(id=mid, text=text, owner=owner, agent=agent, created=str(date.today()),
                                  hash=h, lemmas=lemmatize(text), vec=embed(text)))
        for e in entities(text):
            self.entity_links[e.lower()].add(mid)
        self.hashes.add(h); self.history.append(("ADD", text))
        return mid

    # ---------------------------------------------------------------- retrieval
    def _bm25(self, q_lemmas, pool, k1=1.2, b=0.75):
        N = len(self.memories); avgdl = sum(len(m["lemmas"]) for m in self.memories) / N
        df = Counter(l for m in self.memories for l in set(m["lemmas"]))
        raw = {}
        for mid in pool:
            m, tf = self.memories[mid], Counter(self.memories[mid]["lemmas"])
            s = 0.0
            for t in set(q_lemmas):
                if tf[t]:
                    idf = math.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5))
                    s += idf * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * len(m["lemmas"]) / avgdl))
            raw[mid] = s
        top = max(raw.values()) or 1.0
        return {mid: s / top for mid, s in raw.items()}          # normalized to 0..1

    def _entity_boost(self, query, pool):
        boost = defaultdict(float)
        for e in entities(query):
            linked = self.entity_links.get(e.lower(), set())
            if not linked:
                continue
            specificity = 0.5 / math.sqrt(len(linked))          # fewer linked memories -> bigger boost
            for mid in linked & set(pool):                       # only memories already in the pool
                boost[mid] = max(boost[mid], specificity)
        return boost

    def search(self, query, top_k=3, threshold=0.0, explain=False):
        qv = embed(query)
        sims = sorted(((cosine(qv, m["vec"]), m["id"]) for m in self.memories), reverse=True)
        pool = [mid for _, mid in sims[:max(top_k * 4, 60)]]    # bigger candidate pool for reranking
        sem = {mid: s for s, mid in sims}
        kw = self._bm25(lemmatize(query), pool)
        ent = self._entity_boost(query, pool)
        rows = []
        for mid in pool:
            total = (sem[mid] + kw[mid] + ent[mid]) / 2.5          # sum of 3 signals, normalized to 0..1
            if total >= threshold:
                rows.append((round(total, 3), mid, round(sem[mid], 3), round(kw[mid], 3), round(ent[mid], 3)))
        rows.sort(reverse=True)
        out = rows[:top_k]
        return out if explain else [(t, self.memories[mid]["text"]) for t, mid, *_ in out]

if __name__ == "__main__":
    store = MemoryStore()
    for m in ["The user prefers vegan restaurants",
              "The user's favorite neighborhood in Paris is Marais",
              "The user is planning a trip to Paris in October",
              "The user works as a data engineer at Spotify",
              "The user is allergic to peanuts",
              "The user likes jazz bars",
              "The user prefers vegan restaurants",                  # exact duplicate -> skipped
              "User likes restaurants that are vegan"]:              # paraphrase -> NOT caught by hash dedup
        store.add(m)
    print("history:", [op for op, _ in store.history])
    for q in ["Where should I eat in Paris?", "Any food allergies I should know about?"]:
        print(f"\nquery: {q}")
        for total, mid, sem, kw, ent in store.search(q, top_k=3, explain=True):
            print(f"  total {total:.3f} = (sem {sem:.2f} + bm25 {kw:.2f} + entity {ent:.2f}) / 2.5   {store.memories[mid]['text']}")
