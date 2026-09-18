"""Figures for 'BM25 - Keyword Search for AI Agents'.
Plots 06 and 07 come from actually running BM25 over a synthetic corpus (built below).
Run:  python figures/bm25/make_figs.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _style import *
import scipy.sparse as sp

OUT = out_dir(__file__)
rng = np.random.default_rng(42)


def idf(df, N):
    return np.log(1 + (N - df + 0.5) / (df + 0.5))


# ------------------------------------------------------------------ 01 agentic search loop
def fig_loop():
    fig, ax = canvas(12, 5.2, (0, 12), (0, 5.2))
    ax.text(6, 4.95, "Agentic search = search inside an agent loop", ha="center", fontsize=13, weight="bold")
    box(ax, 0.3, 2.2, 2.2, 1.3, "Task\n\"Which 1990s band's\ndrummer later…?\"", fc="#f9fafb", ec=GRAY, fs=8.5)
    box(ax, 3.3, 2.0, 2.4, 1.7, "① MODEL\nplans, writes queries,\nreads results,\nreformulates", fc="#eff6ff", ec=BLUE, fs=9, weight="bold")
    box(ax, 6.7, 3.3, 2.4, 1.2, "② HARNESS\ntool: search(query)\nor code / grep / files", fc="#fffbeb", ec=AMBER, fs=8.5, weight="bold")
    box(ax, 6.7, 0.8, 2.4, 1.3, "③ RETRIEVAL ENGINE\nBM25 / vectors / hybrid\nover 10⁵ – 10¹⁰ docs", fc="#f0fdf4", ec=GREEN, fs=8.5, weight="bold")
    box(ax, 9.9, 2.0, 1.9, 1.7, "Answer\n(only when evidence\nis found or context\nis full)", fc="#f9fafb", ec=GRAY, fs=8.5)
    arrow(ax, 2.5, 2.85, 3.3, 2.85)
    arrow(ax, 5.7, 3.3, 6.7, 3.9, color=BLUE, text="query", fs=8)
    arrow(ax, 7.9, 3.3, 7.9, 2.1, color=AMBER)
    arrow(ax, 6.7, 1.45, 5.7, 2.3, color=GREEN, text="top-k snippets", fs=8)
    arrow(ax, 5.7, 2.85, 9.9, 2.85, color=GRAY, ls="--", rad=0.0)
    ax.add_patch(FancyArrowPatch((4.2, 3.7), (4.8, 3.7), arrowstyle="-|>", mutation_scale=12, color=RED, lw=1.6,
                                 connectionstyle="arc3,rad=-1.8"))
    ax.text(4.5, 4.45, "repeat: reformulate", ha="center", fontsize=8.5, color=RED)
    ax.add_patch(Rectangle((3.3, 0.35), 2.4, 0.45, fc="#fee2e2", ec=RED))
    ax.text(4.5, 0.575, "context window ≈ 'a floppy disk'", ha="center", va="center", fontsize=8, color=RED)
    save(fig, OUT, "01_agentic_search_loop.png")


# ------------------------------------------------------------------ 02 TF saturation
def fig_tf():
    tf = np.arange(0, 21)
    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.plot(tf, tf / 4, "--", color=GRAY, lw=2, label="raw count (classic TF-IDF style): no limit")
    for k1, c in [(0.5, "#93c5fd"), (1.2, BLUE), (2.0, PURPLE), (5.0, RED)]:
        ax.plot(tf, tf * (k1 + 1) / (tf + k1), "o-", ms=3, color=c, lw=2, label=f"BM25, k1 = {k1}   (max = {k1+1:g})")
    ax.set_xlabel("how many times the query word appears in the document (tf)")
    ax.set_ylabel("term-frequency contribution")
    ax.set_title("k1 controls SATURATION: the 20th mention adds little\n(stops keyword-stuffed pages from winning)")
    ax.legend(fontsize=8); ax.set_ylim(0, 5.5); ax.grid(alpha=0.3)
    save(fig, OUT, "02_tf_saturation.png")


# ------------------------------------------------------------------ 03 IDF
def fig_idf():
    N = 100_000
    df = np.logspace(0, 5, 200)
    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.semilogx(df, idf(df, N), color=GREEN, lw=2.5)
    for word, d in [("'SKU-88213'", 2), ("'Bergum'", 40), ("'retrieval'", 3000), ("'search'", 25000), ("'the'", 99000)]:
        ax.scatter([d], [idf(d, N)], color=DARK, zorder=4)
        ax.annotate(f"{word}\nin {d:,} docs → {idf(d, N):.2f}", (d, idf(d, N)), (8, 6), textcoords="offset points", fontsize=8.5)
    ax.set_xlabel("number of documents containing the word (df), out of 100,000")
    ax.set_ylabel("IDF weight")
    ax.set_title("IDF: rare words are strong evidence, common words are noise")
    ax.grid(alpha=0.3); ax.set_ylim(-0.3, 12.5)
    save(fig, OUT, "03_idf.png")


# ------------------------------------------------------------------ 04 length normalization
def fig_length():
    ratio = np.linspace(0.1, 6, 200)  # doc length / average length
    tf, k1 = 3, 1.2
    fig, ax = plt.subplots(figsize=(7.5, 4))
    for b, c in [(0.0, GRAY), (0.4, GREEN), (0.75, BLUE), (1.0, RED)]:
        s = tf * (k1 + 1) / (tf + k1 * (1 - b + b * ratio))
        ax.plot(ratio, s, color=c, lw=2.3, label=f"b = {b}" + ("  (Lucene/Elasticsearch default)" if b == 0.75 else "") +
                ("  (Pyserini/Anserini default)" if b == 0.4 else "") + ("  (no length penalty)" if b == 0 else ""))
    ax.axvline(1, color=GRAY, ls=":"); ax.text(1.05, 0.4, "average length", fontsize=8, color=GRAY)
    ax.set_xlabel("document length ÷ average document length")
    ax.set_ylabel("score from a word appearing 3 times")
    ax.set_title("b controls LENGTH NORMALIZATION: 3 mentions in a huge doc\ncount less than 3 mentions in a short one")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    save(fig, OUT, "04_length_normalization.png")


# ------------------------------------------------------------------ 05 inverted index
def fig_index():
    fig, ax = canvas(12, 4.6, (0, 12), (0, 4.6))
    ax.text(6, 4.35, "The inverted index: how BM25 avoids scoring every document", ha="center", fontsize=12, weight="bold")
    docs = [("doc 1", "BM25 ranks documents"), ("doc 2", "agents search documents"), ("doc 3", "agents use BM25 search")]
    for i, (d, t) in enumerate(docs):
        box(ax, 0.2, 3.1 - i * 1.05, 3.2, 0.8, f"{d}: \"{t}\"", fc="#f9fafb", ec=GRAY, fs=9, ha="left")
    arrow(ax, 3.6, 2.1, 4.6, 2.1, text="index once", fs=8)
    posting = [("agents", "doc2 (tf 1) → doc3 (tf 1)"), ("bm25", "doc1 (tf 1) → doc3 (tf 1)"),
               ("documents", "doc1 (tf 1) → doc2 (tf 1)"), ("search", "doc2 (tf 1) → doc3 (tf 1)"),
               ("ranks", "doc1 (tf 1)"), ("use", "doc3 (tf 1)")]
    for i, (term, p) in enumerate(posting):
        y = 3.55 - i * 0.58
        box(ax, 4.7, y, 1.4, 0.45, term, fc="#eff6ff", ec=BLUE, fs=9, weight="bold")
        box(ax, 6.3, y, 2.8, 0.45, p, fc="white", ec=BLUE, fs=8.5)
    box(ax, 9.5, 1.3, 2.3, 2.2, "query 'bm25 agents'\n→ read only 2 lists\n→ score doc1, doc2, doc3\n→ skip the other\n    99.99% of the corpus\n(WAND / MaxScore)", fc="#f0fdf4", ec=GREEN, fs=8.5)
    save(fig, OUT, "05_inverted_index.png")


# ------------------------------------------------------------------ synthetic corpus for experiments
V = 20000
N_DOCS = 4000
N_Q = 300
DISTRACT = 12


def build_corpus():
    zipf = 1 / np.arange(1, V + 1) ** 1.05
    zipf /= zipf.sum()
    lengths = np.clip(rng.lognormal(5.6, 0.9, N_DOCS), 30, 8000).astype(int)
    rows, cols, vals = [], [], []
    docs_terms = []
    for d, L in enumerate(lengths):
        terms = rng.choice(V, size=L, p=zipf)
        docs_terms.append(terms)
    # queries: each has a target doc (biased toward long docs, like web pages in BrowseComp-Plus)
    probs = lengths / lengths.sum()
    targets = rng.choice(N_DOCS, size=N_Q, replace=False, p=probs)
    queries = []
    for qi, t in enumerate(targets):
        clues = rng.choice(np.arange(800, 6000), size=6, replace=False)        # specific-ish "entity" words
        docs_terms[t] = np.concatenate([docs_terms[t], clues])                 # evidence: each clue once, buried in a long doc
        short_docs = np.where(lengths < np.median(lengths))[0]
        for c in clues:                                                        # distractors: short pages repeating one clue
            for dd in rng.choice(short_docs, size=DISTRACT, replace=False):
                docs_terms[dd] = np.concatenate([docs_terms[dd], [c] * int(rng.integers(1, 4))])
        common = rng.choice(np.arange(0, 400), size=3, replace=False)          # vague words a query also contains
        queries.append((t, clues, common))
    for d, terms in enumerate(docs_terms):
        u, c = np.unique(terms, return_counts=True)
        rows += [d] * len(u); cols += list(u); vals += list(c)
    TF = sp.csc_matrix((vals, (rows, cols)), shape=(N_DOCS, V), dtype=float)
    dl = np.array([len(t) for t in docs_terms], float)
    return TF, dl, queries


def bm25_scores(TF, dl, qterms, k1, b):
    N = TF.shape[0]; avgdl = dl.mean()
    scores = np.zeros(N)
    for t in qterms:
        col = TF.getcol(t)
        idx = col.indices; f = col.data
        if len(idx) == 0:
            continue
        w = idf(len(idx), N)
        scores[idx] += w * f * (k1 + 1) / (f + k1 * (1 - b + b * dl[idx] / avgdl))
    return scores


def fig_tuning_and_agentic():
    TF, dl, queries = build_corpus()
    k1s = [0.4, 0.9, 1.2, 1.6, 2.2]
    bs = [0.0, 0.2, 0.4, 0.6, 0.75, 1.0]
    R = np.zeros((len(k1s), len(bs)))
    for i, k1 in enumerate(k1s):
        for j, b in enumerate(bs):
            hit = 0
            for t, clues, common in queries:
                q = list(clues[:2]) + list(common[:2])
                s = bm25_scores(TF, dl, q, k1, b)
                hit += t in np.argpartition(-s, 10)[:10]
            R[i, j] = hit / len(queries)
    fig, ax = plt.subplots(figsize=(7, 4.2))
    im = ax.imshow(R * 100, cmap="YlGn", aspect="auto")
    for i in range(len(k1s)):
        for j in range(len(bs)):
            ax.text(j, i, f"{R[i,j]*100:.0f}%", ha="center", va="center", fontsize=9,
                    weight="bold" if R[i, j] == R.max() else "normal")
    ax.set_xticks(range(len(bs))); ax.set_xticklabels([str(b) for b in bs])
    ax.set_yticks(range(len(k1s))); ax.set_yticklabels([str(k) for k in k1s])
    ax.set_xlabel("b (length normalization)"); ax.set_ylabel("k1 (tf saturation)")
    ax.set_title("'Which BM25 do you mean?' — same corpus, same queries\nrecall@10 changes a lot with the two knobs (simulation, long docs)")
    fig.colorbar(im, ax=ax, label="recall@10 (%)")
    save(fig, OUT, "06_parameter_grid.png")
    best = np.unravel_index(R.argmax(), R.shape)
    k1b, bb = k1s[best[0]], bs[best[1]]

    # agentic: the agent knows the 6 clues but each query only uses ONE of them (+ 2 vague words)
    max_q = 8
    single, multi_default, multi_tuned = [], np.zeros(max_q), np.zeros(max_q)
    for t, clues, common in queries:
        for params, acc in [((1.2, 0.75), multi_default), ((k1b, bb), multi_tuned)]:
            found = False
            order = rng.permutation(6)
            for step in range(max_q):
                q = [clues[order[step % 6]], common[step % 3], common[(step + 1) % 3]] + ([clues[order[(step + 1) % 6]]] if step >= 4 else [])
                s = bm25_scores(TF, dl, q, *params)
                if t in np.argpartition(-s, 10)[:10]:
                    found = True
                if found:
                    acc[step] += 1
    multi_default /= len(queries); multi_tuned /= len(queries)
    fig, ax = plt.subplots(figsize=(7.5, 4))
    steps = np.arange(1, max_q + 1)
    ax.plot(steps, multi_default * 100, "o-", color=BLUE, lw=2, label="BM25 default (k1=1.2, b=0.75)")
    ax.plot(steps, multi_tuned * 100, "o-", color=GREEN, lw=2, label=f"BM25 tuned (k1={k1b}, b={bb})")
    ax.set_xlabel("number of queries the agent has issued")
    ax.set_ylabel("% of questions where the evidence\nhas appeared in some top-10")
    ax.axvline(4.5, color=GRAY, ls=":")
    ax.text(4.6, 8, "from query 5 the agent\ncombines TWO clue words", fontsize=8.5, color=DARK)
    ax.set_title("An agent's search trajectory (simulation)\nvague 1-clue queries rarely work; more specific reformulations do")
    ax.set_ylim(0, 100); ax.grid(alpha=0.3); ax.legend(fontsize=9)
    save(fig, OUT, "07_agentic_reformulation.png")
    print("grid", R.round(2).tolist(), "best", k1b, bb)
    print("agentic default", multi_default.round(2).tolist())
    print("agentic tuned", multi_tuned.round(2).tolist())


# ------------------------------------------------------------------ 08 context budget
def fig_budget():
    fig, ax = plt.subplots(figsize=(8.5, 3.8))
    items = [("a 1.44 MB floppy disk\n(≈ usable context)", 3.5e5, AMBER),
             ("BrowseComp-Plus corpus\n(~100K web pages, assuming ~5K tokens each)", 5e8, BLUE),
             ("a 100M-document web index\n(same assumption)", 5e11, PURPLE),
             ("the indexed web\n(tens of billions of pages)", 1e14, RED)]
    ys = np.arange(len(items))[::-1]
    for y, (lab, v, c) in zip(ys, items):
        ax.barh(y, v, color=c)
        ax.text(v * 1.5, y, "~" + {3.5e5: "350 thousand", 5e8: "500 million", 5e11: "500 billion", 1e14: "100 trillion"}[v] + " tokens", va="center", fontsize=9)
    ax.set_yticks(ys); ax.set_yticklabels([i[0] for i in items], fontsize=8.5)
    ax.set_xscale("log"); ax.set_xlim(1e4, 1e16); ax.set_xlabel("tokens (log scale)")
    ax.set_title("Why retrieval never goes away: what fits vs what exists")
    save(fig, OUT, "08_context_budget.png")


# ------------------------------------------------------------------ 09 workspace as filesystem
def fig_workspace():
    fig, ax = canvas(12, 4.8, (0, 12), (0, 4.8))
    ax.text(6, 4.55, "Dynamic workspace: retrieval results become FILES the agent can grep", ha="center",
            fontsize=12, weight="bold")
    box(ax, 0.2, 1.7, 2.2, 1.4, "Web-scale index\nbillions of docs\n(BM25 top-k)", fc="#f0fdf4", ec=GREEN, fs=9)
    arrow(ax, 2.4, 2.4, 3.2, 2.4, color=GREEN, text="search()", fs=8)
    ax.add_patch(FancyBboxPatch((3.2, 0.5), 3.6, 3.6, boxstyle="round,pad=0.03", fc="#fffbeb", ec=AMBER, lw=1.5))
    ax.text(5.0, 3.85, "workspace/  (sandbox filesystem)", ha="center", fontsize=9, weight="bold", color=AMBER)
    files = ["q1_results/serp.md   ← titles + snippets", "q1_results/doc_0417.txt", "q1_results/doc_2231.txt",
             "q2_results/serp.md", "q2_results/doc_0090.txt", "notes.md   ← agent's own notes"]
    for i, f in enumerate(files):
        ax.text(3.4, 3.4 - i * 0.48, "📄 " + f if False else "• " + f, fontsize=8.5, family="monospace")
    arrow(ax, 6.8, 2.4, 7.6, 2.4, color=AMBER)
    steps = [("1. read serp.md", "cheap: titles + snippets only"),
             ("2. rg -n 'drummer' doc_0417.txt", "jump to the exact lines"),
             ("3. sed -n '120,160p' doc_0417.txt", "read just that section"),
             ("4. new search() with found names", "expand the workspace")]
    for i, (a, b_) in enumerate(steps):
        box(ax, 7.6, 3.4 - i * 0.85, 4.2, 0.7, f"{a}\n{b_}", fc="white", ec=BLUE, fs=8.3, ha="left")
    ax.text(6, 0.1, "Progressive disclosure: pay context tokens only for what is actually relevant.", ha="center",
            fontsize=9, color=GRAY)
    save(fig, OUT, "09_workspace_filesystem.png")


if __name__ == "__main__":
    fig_loop(); fig_tf(); fig_idf(); fig_length(); fig_index(); fig_budget(); fig_workspace()
    fig_tuning_and_agentic()
