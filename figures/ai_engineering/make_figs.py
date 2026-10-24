"""Figures for the 'AI Engineering' guide series (target/ai/).
Every figure is computed from a formula or a simulation; assumed numbers are labelled on the figure.
Run:  py -3.12 figures/ai_engineering/make_figs.py
"""
import sys, os
from math import log
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _style import *

OUT = out_dir(__file__)
rng = np.random.default_rng(11)


def note(ax, text, loc=(0.02, 0.97)):
    ax.text(*loc, text, transform=ax.transAxes, fontsize=8, color=GRAY, va="top",
            bbox=dict(fc="white", ec=LIGHT, pad=3))


def stacked(ax, parts, unit=""):
    """Stacked horizontal bar with labels alternating above and below, so small segments don't collide."""
    left = 0
    for i, (name, n, c) in enumerate(parts):
        ax.barh([0], [n], left=left, color=c, edgecolor="white", height=0.6)
        up = i % 2 == 0
        ax.text(left + n / 2, 0.36 if up else -0.36, f"{name}\n{n:,}{unit}", ha="center",
                va="bottom" if up else "top", fontsize=7.5)
        left += n
    ax.set_ylim(-1.0, 1.0); ax.set_yticks([])
    return left


def softmax(z):
    z = np.asarray(z, float); e = np.exp(z - z.max()); return e / e.sum()


# ------------------------------------------------------------ Guide 1
def f01_temperature():
    toks = ["Paris", "Lyon", "the", "France", "banana"]
    logits = np.array([2.0, 1.0, 0.5, 0.0, -1.0])
    fig, ax = plt.subplots(figsize=(8, 4))
    w = 0.25
    for i, (T, c) in enumerate([(0.5, BLUE), (1.0, PURPLE), (2.0, AMBER)]):
        p = softmax(logits / T)
        b = ax.bar(np.arange(5) + (i - 1) * w, p, w, color=c, label=f"T = {T}")
        for x, v in zip(np.arange(5) + (i - 1) * w, p):
            ax.text(x, v + 0.01, f"{v:.2f}", ha="center", fontsize=7)
    ax.set_xticks(range(5)); ax.set_xticklabels(toks)
    ax.set_ylabel("Probability of next token"); ax.set_ylim(0, 0.95); ax.grid(axis="y", alpha=0.3)
    ax.legend(fontsize=8)
    ax.set_title("Temperature reshapes the same logits: low T sharpens, high T flattens")
    note(ax, "Toy logits [2.0, 1.0, 0.5, 0.0, −1.0]\nfor \"The capital of France is …\"", (0.62, 0.80))
    save(fig, OUT, "f01_temperature.png")


def f02_attention():
    toks = ["The", "cat", "sat", "on", "the", "mat"]
    n, d = len(toks), 8
    r = np.random.default_rng(3)
    X = 0.45 * r.normal(size=(n, d)); Wq, Wk = r.normal(size=(d, d)), r.normal(size=(d, d))
    S = (X @ Wq) @ (X @ Wk).T / np.sqrt(d)
    S[np.triu_indices(n, 1)] = -np.inf
    A = np.vstack([softmax(row) for row in S])
    fig, ax = plt.subplots(figsize=(5.6, 4.8))
    im = ax.imshow(A, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(range(n)); ax.set_xticklabels(toks); ax.set_yticks(range(n)); ax.set_yticklabels(toks)
    ax.set_xlabel("Key: token being looked at"); ax.set_ylabel("Query: token doing the looking")
    for i in range(n):
        for j in range(n):
            if j <= i:
                ax.text(j, i, f"{A[i, j]:.2f}", ha="center", va="center", fontsize=8,
                        color="white" if A[i, j] > 0.55 else DARK)
            else:
                ax.text(j, i, "masked", ha="center", va="center", fontsize=6, color=GRAY)
    ax.set_title("Causal self-attention weights (each row sums to 1)")
    fig.colorbar(im, ax=ax, fraction=0.046)
    fig.text(0.5, -0.02, "Random toy weights (d = 8): shows the mechanics, not learned meaning.", ha="center", fontsize=8, color=GRAY)
    save(fig, OUT, "f02_attention_heatmap.png")


# ------------------------------------------------------------ Guide 2
def f03_context_budget():
    parts = [("System prompt", 2000, BLUE), ("Tool definitions", 6000, PURPLE), ("Retrieved documents", 12000, TEAL),
             ("Conversation history", 25000, AMBER), ("User message", 500, GREEN), ("Reserved for output", 8000, GRAY)]
    fig, ax = plt.subplots(figsize=(9, 3.2))
    left = stacked(ax, parts)
    ax.set_xlim(0, left)
    ax.set_xlabel(f"Tokens in one request (total {left:,}). Example budget, assumed numbers.")
    ax.set_title("Where the context window goes in a typical agent request")
    save(fig, OUT, "f03_context_budget.png")


# ------------------------------------------------------------ Guide 3
def f04_eval_ci():
    n = np.arange(20, 2001)
    fig, ax = plt.subplots(figsize=(7.5, 4))
    for p, c in [(0.5, RED), (0.8, BLUE), (0.95, GREEN)]:
        ax.plot(n, 100 * 1.96 * np.sqrt(p * (1 - p) / n), color=c, lw=2, label=f"true pass rate {p:.0%}")
    for nn in [50, 100, 400]:
        h = 100 * 1.96 * np.sqrt(0.8 * 0.2 / nn)
        ax.scatter([nn], [h], color=BLUE, zorder=5)
    note(ax, "At an 80% pass rate:\nn = 50  → ±11.1 pts\nn = 100 → ±7.8 pts\nn = 400 → ±3.9 pts", (0.42, 0.95))
    ax.set_xscale("log"); ax.set_xlabel("Examples in the eval set (log scale)")
    ax.set_ylabel("95% margin of error (± percentage points)"); ax.grid(alpha=0.3); ax.legend(fontsize=8)
    ax.set_title("How many eval examples do you need? Error shrinks like 1/√n")
    save(fig, OUT, "f04_eval_margin_of_error.png")


def f05_ab_sample():
    z = 1.959964 + 0.841621
    p1 = 0.70; mde = np.linspace(0.01, 0.10, 100); p2 = p1 + mde
    n = z ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / mde ** 2
    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.plot(mde * 100, n, color=PURPLE, lw=2)
    for m in [0.02, 0.05, 0.10]:
        nn = z ** 2 * (p1 * (1 - p1) + (p1 + m) * (1 - p1 - m)) / m ** 2
        ax.scatter([m * 100], [nn], color=PURPLE, zorder=5); ax.text(m * 100 + 0.15, nn * 1.15, f"+{m*100:.0f} pts: {nn:,.0f} per arm", fontsize=8)
    ax.set_yscale("log"); ax.set_xlabel("Smallest improvement you want to detect (percentage points)")
    ax.set_ylabel("Users needed per arm (log scale)"); ax.grid(alpha=0.3)
    ax.set_title("A/B test size: halving the effect needs ~4× the users")
    note(ax, "Baseline success 70%, two-sided α = 0.05, power 80%.", (0.45, 0.97))
    save(fig, OUT, "f05_ab_sample_size.png")


# ------------------------------------------------------------ Guide 4
def kmeans(X, k, iters=12, seed=0):
    r = np.random.default_rng(seed); C = X[r.choice(len(X), k, replace=False)].copy()
    for _ in range(iters):
        a = np.argmin(((X[:, None, :] - C[None]) ** 2).sum(-1), axis=1)
        for j in range(k):
            m = X[a == j]
            if len(m): C[j] = m.mean(0)
    a = np.argmin(((X[:, None, :] - C[None]) ** 2).sum(-1), axis=1)
    return C, a


def f06_ivf():
    N, d, G = 20000, 32, 40
    centers = rng.normal(size=(G, d)) * 0.6
    X = centers[rng.integers(0, G, N)] + rng.normal(size=(N, d))
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    Q = centers[rng.integers(0, G, 200)] + rng.normal(size=(200, d)); Q /= np.linalg.norm(Q, axis=1, keepdims=True)
    k = 100
    C, assign = kmeans(X, k)
    lists = [np.flatnonzero(assign == j) for j in range(k)]
    exact = np.argsort(-(Q @ X.T), axis=1)[:, :10]
    probes = [1, 2, 4, 8, 16, 32, 100]; rec, frac = [], []
    for npb in probes:
        hits, scanned = 0, 0
        for qi, q in enumerate(Q):
            near = np.argsort(-(C @ q))[:npb]
            cand = np.concatenate([lists[j] for j in near]); scanned += len(cand)
            top = cand[np.argsort(-(X[cand] @ q))[:10]]
            hits += len(set(top) & set(exact[qi]))
        rec.append(hits / (10 * len(Q))); frac.append(scanned / (len(Q) * N))
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.plot(np.array(frac) * 100, rec, "o-", color=TEAL, lw=2)
    for f, r_, p in zip(frac, rec, probes):
        ax.text(f * 100 * 1.12, r_ - 0.035, f"nprobe={p}", fontsize=7.5)
    ax.set_xscale("log"); ax.set_xlabel("Share of the database scanned per query (%, log scale)")
    ax.set_ylabel("Recall@10 vs exact search"); ax.set_ylim(0, 1.05); ax.grid(alpha=0.3)
    ax.set_title("Approximate search: scan a small slice, keep most of the recall")
    note(ax, "Simulation: IVF index, 20,000 clustered vectors (d=32),\n100 k-means lists, 200 queries.", (0.38, 0.30))
    save(fig, OUT, "f06_ann_recall_vs_work.png")
    return list(zip(probes, frac, rec))


# ------------------------------------------------------------ Guide 5
def f07_compounding():
    n = np.arange(1, 51)
    fig, ax = plt.subplots(figsize=(7.5, 4))
    for p, c in [(0.90, RED), (0.95, AMBER), (0.99, BLUE), (0.999, GREEN)]:
        ax.plot(n, p ** n, color=c, lw=2, label=f"each step right {p:.1%} of the time")
    ax.scatter([20], [0.95 ** 20], color=AMBER, zorder=5)
    ax.text(21, 0.95 ** 20 + 0.03, f"20 steps at 95%: {0.95**20:.0%} success", fontsize=8, color=AMBER)
    ax.set_xlabel("Steps in the task"); ax.set_ylabel("P(whole task succeeds)"); ax.set_ylim(0, 1.02)
    ax.grid(alpha=0.3); ax.legend(fontsize=8, loc="lower left")
    ax.set_title("Errors compound: why long agent runs need checks and recovery")
    fig.text(0.5, -0.03, "Assumes independent steps with no error recovery.", ha="center", fontsize=8, color=GRAY)
    save(fig, OUT, "f07_agent_compounding_errors.png")


# ------------------------------------------------------------ Guide 6
def f08_caching():
    T = 20; prefix, per_turn, user = 10000, 1000, 500
    I = np.array([prefix + per_turn * (t - 1) + user for t in range(1, T + 1)])
    no = I * 1.0
    yes = [I[0] * 1.25] + [I[t - 1] * 0.10 + (I[t] - I[t - 1]) * 1.25 for t in range(1, T)]
    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.plot(range(1, T + 1), np.cumsum(no) / 1e3, "o-", color=RED, label="no caching")
    ax.plot(range(1, T + 1), np.cumsum(yes) / 1e3, "o-", color=GREEN, label="prompt caching")
    s = 1 - np.sum(yes) / np.sum(no)
    ax.text(T, np.cumsum(yes)[-1] / 1e3 + 15, f"{s:.0%} cheaper\nover {T} turns", ha="right", fontsize=8, color=GREEN)
    ax.set_xlabel("Conversation turn"); ax.set_ylabel("Cumulative input cost\n(thousand token-units)")
    ax.grid(alpha=0.3); ax.legend(fontsize=8, loc="upper left")
    ax.set_title("Prompt caching: re-sent history becomes cheap")
    fig.text(0.5, -0.04, "Assumed: 10k-token prefix, +1k tokens per turn. Prices relative to base input: cache write 1.25×, cache read 0.1×.", ha="center", fontsize=8, color=GRAY)
    save(fig, OUT, "f08_prompt_caching_cost.png")
    return s


def f09_voice_budget():
    parts = [("End-of-speech detection", 200, GRAY), ("Speech-to-text", 100, BLUE), ("LLM time to first token", 300, PURPLE),
             ("Text-to-speech first audio", 100, TEAL), ("Network", 80, AMBER)]
    fig, ax = plt.subplots(figsize=(9, 3.2))
    left = stacked(ax, parts, " ms")
    ax.axvline(800, color=RED, ls="--"); ax.text(808, 0.75, "≈800 ms: replies\nstart to feel slow", fontsize=8, color=RED, va="top")
    ax.set_xlim(0, 1000)
    ax.set_xlabel(f"ms from the user stopping speaking to hearing a reply (total {left} ms). Example budget, assumed numbers.")
    ax.set_title("A voice agent's latency budget (cascaded pipeline)")
    save(fig, OUT, "f09_voice_latency_budget.png")


# ------------------------------------------------------------ Guide 8
def f10_roofline():
    peak, bw = 989e12, 3.35e12
    ai = np.logspace(-1, 4, 300)
    perf = np.minimum(peak, ai * bw)
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.plot(ai, perf / 1e12, color=BLUE, lw=2.5)
    ridge = peak / bw
    ax.axvline(ridge, color=GRAY, ls=":"); ax.text(ridge * 1.1, 30, f"ridge ≈ {ridge:.0f} FLOP/byte", fontsize=8, color=GRAY)
    for x, lab, c in [(1, "decode, batch 1\n(≈1 FLOP/byte)", RED), (64, "decode, batch 64", AMBER), (2000, "prefill\n(long prompt)", GREEN)]:
        y = min(peak, x * bw) / 1e12
        ax.scatter([x], [y], color=c, zorder=5, s=40); ax.text(x * 1.2, y * 0.35, lab, fontsize=8, color=c)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("Arithmetic intensity (FLOPs per byte read from memory)"); ax.set_ylabel("Attainable TFLOP/s")
    ax.grid(alpha=0.3, which="both")
    ax.set_title("Roofline (H100 SXM, dense BF16): decode is memory-bound")
    note(ax, "Peak 989 TFLOP/s, 3.35 TB/s HBM.\nFP16 weights: decode intensity ≈ batch size.", (0.02, 0.97))
    save(fig, OUT, "f10_roofline.png")


def f11_batch_throughput():
    P, bw, peak = 8e9, 3.35e12, 989e12
    W = 2 * P; kv_seq = 131072 * 4096
    B = np.arange(1, 141)
    t_simple = np.maximum(W / bw, 2 * P * B / peak)
    t_kv = np.maximum((W + B * kv_seq) / bw, 2 * P * B / peak)
    bmax = int((80e9 - W) // kv_seq)
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.plot(B, B / t_simple / 1e3, color=GRAY, ls="--", label="weights only (ideal)")
    ax.plot(B, B / t_kv / 1e3, color=BLUE, lw=2, label="weights + KV cache reads (4K context)")
    ax.axvline(bmax, color=RED, ls=":"); ax.text(bmax - 3, 15, f"80 GB full\nat batch ≈ {bmax}", fontsize=8, color=RED, ha="right")
    ax.set_xlabel("Concurrent sequences (batch size)"); ax.set_ylabel("Output tokens/s (thousands)")
    ax.grid(alpha=0.3); ax.legend(fontsize=8, loc="upper left")
    ax.set_title("Batching helps, but KV-cache reads cap decode throughput")
    note(ax, "Back-of-envelope: 8B model, FP16, one H100.\nKV 128 KiB/token. Ignores kernel overheads.", (0.50, 0.30))
    save(fig, OUT, "f11_batch_throughput.png")
    return bmax


def f12_spec_decoding():
    a = np.linspace(0.3, 0.95, 200)
    fig, ax = plt.subplots(figsize=(7.5, 4))
    for k, c in [(2, BLUE), (4, PURPLE), (8, AMBER)]:
        ex = (1 - a ** (k + 1)) / (1 - a)
        ax.plot(a, ex / (1 + 0.05 * k), color=c, lw=2, label=f"draft {k} tokens per step")
    ax.axhline(1, color=GRAY, ls=":")
    ax.set_xlabel("Acceptance rate α (chance each drafted token is accepted)"); ax.set_ylabel("Speed-up vs normal decoding")
    ax.grid(alpha=0.3); ax.legend(fontsize=8, loc="upper left")
    ax.set_title("Speculative decoding pays off only when drafts are usually right")
    fig.text(0.5, -0.03, "Speed-up = (1 − α^(k+1)) / (1 − α) ÷ (1 + k·c), with draft cost c = 0.05 of a target step.", ha="center", fontsize=8, color=GRAY)
    save(fig, OUT, "f12_speculative_decoding.png")


# ------------------------------------------------------------ Guide 9
def f13_lora():
    r = np.array([1, 2, 4, 8, 16, 32, 64, 128, 256])
    d = k = 4096
    fig, ax = plt.subplots(figsize=(7.5, 4))
    ax.plot(r, r * (d + k) / (d * k) * 100, "o-", color=PURPLE, lw=2)
    for rr in [8, 64]:
        v = rr * (d + k) / (d * k) * 100
        ax.text(rr * 1.15, v * 0.75, f"r={rr}: {rr*(d+k):,} params ({v:.2f}%)", fontsize=8)
    ax.set_xscale("log", base=2); ax.set_yscale("log")
    ax.set_xlabel("LoRA rank r"); ax.set_ylabel("Trainable params vs full matrix (%)"); ax.grid(alpha=0.3, which="both")
    ax.set_title("LoRA on one 4096×4096 weight matrix (16.8M params)")
    save(fig, OUT, "f13_lora_params.png")


def f14_dpo():
    m = np.linspace(-20, 20, 400)
    fig, ax = plt.subplots(figsize=(7.5, 4))
    for beta, c in [(0.05, AMBER), (0.1, BLUE), (0.5, RED)]:
        ax.plot(m, np.log1p(np.exp(-beta * m)), color=c, lw=2, label=f"β = {beta}")
    ax.axvline(0, color=GRAY, ls=":"); ax.text(1.5, 2.2, "margin 0 → loss ln 2 ≈ 0.693", fontsize=8, color=GRAY)
    ax.set_xlabel("Margin: how much more the model (vs reference) prefers the chosen answer\n(difference of log-probability ratios)")
    ax.set_ylabel("DPO loss"); ax.set_ylim(0, 6); ax.grid(alpha=0.3); ax.legend(fontsize=8)
    ax.set_title("DPO loss: pushes the chosen answer up relative to the rejected one")
    save(fig, OUT, "f14_dpo_loss.png")


def f15_kv_cache():
    ctx = np.array([1, 4, 8, 16, 32, 64, 128]) * 1024
    per_gqa = 2 * 80 * 8 * 128 * 2; per_mha = 2 * 80 * 64 * 128 * 2
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.plot(ctx / 1024, ctx * per_mha / 2 ** 30, "o-", color=RED, label="64 KV heads (classic multi-head)")
    ax.plot(ctx / 1024, ctx * per_gqa / 2 ** 30, "o-", color=BLUE, label="8 KV heads (grouped-query)")
    ax.axhline(20, color=AMBER, ls="--")
    ax.text(127, 8, "≈20 GB left for KV cache on 2×80 GB GPUs after FP16 weights", fontsize=8, color=AMBER, ha="right", va="top")
    ax.set_yscale("log"); ax.set_xlabel("Context length per request (thousand tokens)")
    ax.set_ylabel("KV cache for ONE request (GiB)"); ax.grid(alpha=0.3); ax.legend(fontsize=8, loc="lower right")
    ax.set_title("KV-cache memory per request vs context length (log scale)")
    fig.text(0.5, -0.04, "Assumed 70B-class shape: 80 layers, head dim 128, FP16.  Bytes per token = 2 × layers × KV heads × head dim × 2.", ha="center", fontsize=8, color=GRAY)
    save(fig, OUT, "f15_kv_cache.png")


# ------------------------------------------------------------ added in the October 2026 audit
def f16_hnsw():
    """HNSW: a real greedy search over a small 3-layer graph built from random 2-D points."""
    r = np.random.default_rng(5)
    P = r.uniform(0, 10, size=(40, 2))
    lvl = np.zeros(40, int); lvl[:10] = 1; lvl[:3] = 2          # nested layers: 40 -> 10 -> 3 nodes
    q = np.array([8.3, 2.1])
    def nbrs(ids, m):
        E = {}
        for i in ids:
            d = np.linalg.norm(P[ids] - P[i], axis=1)
            E[i] = [ids[j] for j in np.argsort(d)[1:m + 1]]
        for i in list(E):                                       # make links two-way
            for j in E[i]:
                if i not in E[j]: E[j].append(i)
        return E
    layers = [(2, 2), (1, 3), (0, 4)]
    cur = 0; fig, axes = plt.subplots(1, 3, figsize=(12, 4.2))
    total_visits = 0
    for ax, (L, m) in zip(axes, layers):
        ids = list(np.flatnonzero(lvl >= L)); E = nbrs(ids, m)
        for i in ids:
            for j in E[i]:
                ax.plot(*zip(P[i], P[j]), color=LIGHT, lw=1, zorder=1)
        ax.scatter(P[ids, 0], P[ids, 1], s=28, color=GRAY, zorder=2)
        path = [cur]
        while True:                                             # greedy: move to the neighbour closest to q
            best = min(E[cur], key=lambda j: np.linalg.norm(P[j] - q))
            if np.linalg.norm(P[best] - q) >= np.linalg.norm(P[cur] - q): break
            cur = best; path.append(cur)
        total_visits += len(path)
        ax.plot(P[path, 0], P[path, 1], "-o", color=BLUE, lw=2, ms=6, zorder=3)
        ax.scatter(*P[path[0]], s=90, color=AMBER, zorder=4, label="entry point")
        ax.scatter(*q, marker="*", s=220, color=RED, zorder=5, label="query")
        ax.set_title(f"Layer {L}: {len(ids)} nodes" + ("  (sparse 'highway')" if L == 2 else "  (all vectors)" if L == 0 else ""), fontsize=10)
        ax.set_xlim(-0.3, 10.3); ax.set_ylim(-0.3, 10.3); ax.set_xticks([]); ax.set_yticks([])
        ax.set_aspect("equal")
    axes[0].legend(fontsize=8, loc="upper left")
    exact = int(np.argmin(np.linalg.norm(P - q, axis=1)))
    fig.suptitle("HNSW search: greedy hops on a sparse top layer, then drop down and refine", fontweight="bold")
    fig.text(0.5, -0.02, f"Toy graph: 40 random 2-D points. The blue path visits {total_visits} nodes in total and ends at the true nearest neighbour: {cur == exact}. "
             "Real indexes keep a candidate list (ef_search) instead of one path, which protects recall.", ha="center", fontsize=8, color=GRAY)
    save(fig, OUT, "f16_hnsw_layers.png")
    return total_visits, cur == exact


def f17_paged_kv():
    """Contiguous KV reservation vs paged blocks with a shared prefix (block = 4 tokens, toy sizes)."""
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(10, 5.6), gridspec_kw={"height_ratios": [1, 1.35]})
    for ax in (a1, a2): ax.set_xlim(0, 24); ax.axis("off")
    # --- top: old contiguous reservation, sized for max length (8 blocks) each
    a1.set_ylim(0, 3); a1.set_title("Before: each request reserves memory for its maximum length", loc="left", fontsize=10)
    used = {"A": 5, "B": 3}
    for row, (name, u) in enumerate(used.items()):
        y = 1.7 - row * 1.1
        a1.text(0.2, y + 0.35, f"Request {name}", fontsize=9, va="center")
        for k in range(8):
            c = (BLUE if name == "A" else PURPLE) if k < u else "white"
            a1.add_patch(Rectangle((3 + k * 1.2, y), 1.1, 0.7, fc=c, ec=GRAY, hatch=None if k < u else "///"))
        a1.text(13, y + 0.35, f"{u} of 8 blocks used, {8 - u} reserved but empty", fontsize=8.5, va="center", color=GRAY)
    # --- bottom: paged
    a2.set_ylim(0, 4.6); a2.set_title("PagedAttention: small blocks allocated on demand; a shared prompt prefix is stored once", loc="left", fontsize=10)
    seqs = {"A": ["P0", "P1", "A2", "A3", "A4"], "B": ["P0", "P1", "B2"]}
    phys = ["A3", "P1", "free", "B2", "A2", "free", "P0", "A4", "free", "free"]
    col = lambda t: GREEN if t.startswith("P") else BLUE if t.startswith("A") else PURPLE if t.startswith("B") else "white"
    pos = {}
    for k, t in enumerate(phys):
        x = 12.2 + (k % 5) * 2.2; y = 2.6 - (k // 5) * 1.5
        a2.add_patch(Rectangle((x, y), 1.9, 0.9, fc=col(t), ec=GRAY, alpha=0.9 if t != "free" else 1))
        a2.text(x + 0.95, y + 0.45, t if t != "free" else "free", ha="center", va="center", fontsize=8,
                color="white" if t != "free" else GRAY)
        if t != "free": pos[t] = (x + 0.95, y + 0.45)
    a2.text(16.6, 4.0, "Physical GPU memory (any order)", ha="center", fontsize=9)
    for row, (name, blocks) in enumerate(seqs.items()):
        y = 3.0 - row * 1.8
        a2.text(0.2, y + 0.45, f"Request {name}\nblock table", fontsize=8.5, va="center")
        for k, t in enumerate(blocks):
            x = 2.6 + k * 1.75
            a2.add_patch(Rectangle((x, y), 1.55, 0.9, fc=col(t), ec=GRAY))
            a2.text(x + 0.78, y + 0.45, t, ha="center", va="center", fontsize=8, color="white")
        last = blocks[-1]; xl = 2.6 + (len(blocks) - 1) * 1.75
        arrow(a2, xl + 1.55, y + 0.45, pos[last][0] - 0.95, pos[last][1], color=GRAY, lw=1, rad=-0.15)
    a2.text(0.2, 0.15, "Green P0, P1 = the shared system prompt: computed once, used by both requests (prefix caching).  "
            "Waste is at most one part-filled block per request.", fontsize=8, color=GRAY)
    save(fig, OUT, "f17_paged_kv_blocks.png")


if __name__ == "__main__":
    if len(sys.argv) > 1:                       # run only the named figures, e.g. f16_hnsw
        for name in sys.argv[1:]: print(name, globals()[name]())
        sys.exit()
    f15_kv_cache()
    f01_temperature(); f02_attention(); f03_context_budget(); f04_eval_ci(); f05_ab_sample()
    print("IVF", f06_ivf())
    f07_compounding(); print("cache saving", f08_caching()); f09_voice_budget()
    f10_roofline(); print("bmax", f11_batch_throughput()); f12_spec_decoding(); f13_lora(); f14_dpo()
