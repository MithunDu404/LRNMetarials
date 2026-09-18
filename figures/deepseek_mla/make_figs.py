"""Figures for 'Multi-head Latent Attention - Shrinking the KV Cache'.
Timings are measured with a real NumPy decoder loop; cache sizes use DeepSeek-V3/R1's published config.
Run:  python figures/deepseek_mla/make_figs.py
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _style import *

OUT = out_dir(__file__)
rng = np.random.default_rng(0)

# DeepSeek-V3 / R1 config (config.json): 61 layers, 128 heads, head dim 128,
# kv_lora_rank 512, qk_rope_head_dim 64
LAYERS, HEADS, HDIM, LATENT, ROPE = 61, 128, 128, 512, 64
BYTES = 2  # fp16/bf16


def kv_bytes_per_token(kind):
    if kind == "MHA":
        return 2 * HEADS * HDIM * LAYERS * BYTES
    if kind == "GQA (groups of 8)":
        return 2 * (HEADS // 8) * HDIM * LAYERS * BYTES
    if kind == "MQA":
        return 2 * 1 * HDIM * LAYERS * BYTES
    if kind == "MLA":
        return (LATENT + ROPE) * LAYERS * BYTES


KINDS = ["MHA", "GQA (groups of 8)", "MQA", "MLA"]
KCOL = {"MHA": RED, "GQA (groups of 8)": AMBER, "MQA": GRAY, "MLA": GREEN}


# ------------------------------------------------------------------ 01 KV cache idea
def fig_kv_idea():
    toks = ["the", "American", "flag", "is", "red", "white", "and", "blue"]
    n = len(toks)
    fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), gridspec_kw=dict(width_ratios=[1, 1.15]))
    ax = axes[0]
    M = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            M[i, j] = 0 if j > i else (1 if i < n - 1 else 2)
    cmap = matplotlib.colors.ListedColormap(["#f3f4f6", "#bfdbfe", "#fca5a5"])
    ax.imshow(M, cmap=cmap, vmin=0, vmax=2)
    for i in range(n):
        for j in range(n):
            ax.text(j, i, "mask" if j > i else ("new" if i == n - 1 else "same"), ha="center", va="center",
                    fontsize=7, color=GRAY if j > i else DARK)
    ax.set_xticks(range(n)); ax.set_xticklabels(toks, rotation=45, ha="right")
    ax.set_yticks(range(n)); ax.set_yticklabels(toks)
    ax.set_xlabel("keys"); ax.set_ylabel("queries")
    ax.set_title("After adding the token 'blue':\nonly the BOTTOM ROW of the pattern is new")
    ax = axes[1]
    ax.set_xlim(0, 10); ax.set_ylim(0, 8); ax.axis("off")
    ax.set_title("So for each new token we only need…")
    box(ax, 0.3, 6.1, 2.2, 1.0, "new query q₈\n(1 row)", fc="#fee2e2", ec=RED, fs=10)
    for r in range(8):
        c = "#fee2e2" if r == 7 else "#dbeafe"
        ax.add_patch(Rectangle((4.0, 6.9 - r * 0.42), 1.6, 0.36, fc=c, ec=BLUE if r < 7 else RED, lw=1))
        ax.add_patch(Rectangle((6.4, 6.9 - r * 0.42), 1.6, 0.36, fc=c, ec=BLUE if r < 7 else RED, lw=1))
    ax.text(4.8, 7.45, "keys K", ha="center", weight="bold"); ax.text(7.2, 7.45, "values V", ha="center", weight="bold")
    ax.text(9.2, 5.5, "rows 1–7:\nread from\nthe KV CACHE", ha="center", fontsize=9, color=BLUE)
    ax.text(9.2, 3.8, "row 8:\ncompute now,\nappend to cache", ha="center", fontsize=9, color=RED)
    arrow(ax, 2.5, 6.6, 3.9, 6.6, color=RED)
    box(ax, 0.3, 1.0, 9.4, 1.6,
        "Queries are never cached (only the newest is needed).\n"
        "Cache size = 2 × tokens × layers × heads × head_dim × bytes\n"
        "DeepSeek-R1 with plain multi-head attention: ≈ 4 MB for EVERY token of context",
        fc="#fffbeb", ec=AMBER, fs=8.3)
    save(fig, OUT, "01_kv_cache_idea.png")


# ------------------------------------------------------------------ 02 measured speedup of KV caching
def fig_kv_speed():
    d, h = 256, 8
    dk = d // h
    W = [rng.normal(0, 1 / np.sqrt(d), (d, d)) for _ in range(4)]

    def attn_full(X):
        n = X.shape[0]
        Q = (X @ W[0].T).reshape(n, h, dk).transpose(1, 0, 2)
        K = (X @ W[1].T).reshape(n, h, dk).transpose(1, 0, 2)
        V = (X @ W[2].T).reshape(n, h, dk).transpose(1, 0, 2)
        s = Q @ K.transpose(0, 2, 1) / np.sqrt(dk)
        s = np.where(np.triu(np.ones((n, n), bool), 1), -1e9, s)
        s = np.exp(s - s.max(-1, keepdims=True)); s /= s.sum(-1, keepdims=True)
        return ((s @ V).transpose(1, 0, 2).reshape(n, d)) @ W[3].T

    def gen_nocache(T):
        X = rng.normal(size=(1, d))
        for _ in range(T):
            out = attn_full(X)
            X = np.vstack([X, np.tanh(out[-1:])])
        return X

    def gen_cache(T):
        x = rng.normal(size=(1, d)); Kc = np.zeros((h, 0, dk)); Vc = np.zeros((h, 0, dk))
        for _ in range(T):
            q = (x @ W[0].T).reshape(h, 1, dk)
            Kc = np.concatenate([Kc, (x @ W[1].T).reshape(h, 1, dk)], 1)
            Vc = np.concatenate([Vc, (x @ W[2].T).reshape(h, 1, dk)], 1)
            s = q @ Kc.transpose(0, 2, 1) / np.sqrt(dk)
            s = np.exp(s - s.max(-1, keepdims=True)); s /= s.sum(-1, keepdims=True)
            x = np.tanh(((s @ Vc).reshape(1, d)) @ W[3].T)
        return x

    Ts = [50, 100, 200, 400, 800]
    t_nc, t_c = [], []
    for T in Ts:
        t0 = time.perf_counter(); gen_nocache(T); t_nc.append(time.perf_counter() - t0)
        t0 = time.perf_counter(); gen_cache(T); t_c.append(time.perf_counter() - t0)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    ax = axes[0]
    ax.plot(Ts, t_nc, "o-", color=RED, lw=2, label="recompute everything each step")
    ax.plot(Ts, t_c, "o-", color=GREEN, lw=2, label="KV cache")
    for T, a, b in zip(Ts, t_nc, t_c):
        ax.text(T, a * 1.4, f"{a/b:.0f}× faster", ha="center", fontsize=8, color=RED)
    ax.set_yscale("log"); ax.set_xlabel("tokens generated"); ax.set_ylabel("seconds (measured, NumPy, log)")
    ax.set_title("Measured: generating text with one attention layer"); ax.legend(fontsize=8)
    ax = axes[1]
    n = np.arange(1, 4001)
    ax.plot(n, n ** 2, color=RED, lw=2, label="no cache: step t does t×t dot products")
    ax.plot(n, n, color=GREEN, lw=2, label="KV cache: step t does t dot products")
    ax.set_yscale("log"); ax.set_xlabel("position t of the token being generated")
    ax.set_ylabel("attention dot products for this step")
    ax.set_title("Cost of generating ONE token\nquadratic → linear in context length"); ax.legend(fontsize=8)
    save(fig, OUT, "02_kv_cache_speed.png")


# ------------------------------------------------------------------ 03 cache sizes
def fig_cache_sizes():
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.4))
    ax = axes[0]
    vals = [kv_bytes_per_token(k) for k in KINDS]
    bars = ax.barh(KINDS[::-1], [v / 1e3 for v in vals[::-1]], color=[KCOL[k] for k in KINDS[::-1]])
    ax.set_xscale("log"); ax.set_xlabel("KV cache per token (kilobytes, log scale)")
    for b, v, k in zip(bars, vals[::-1], KINDS[::-1]):
        lab = f"{v/1e6:.2f} MB" if v > 1e6 else f"{v/1e3:.0f} KB"
        ax.text(v / 1e3 * 1.15, b.get_y() + b.get_height() / 2, f"{lab}  ({vals[0]/v:.0f}× smaller)" if k != "MHA" else lab,
                va="center", fontsize=9)
    ax.set_xlim(10, 3e4)
    ax.set_title("DeepSeek-R1 architecture (61 layers, 128 heads, fp16)")
    ax = axes[1]
    ctx = np.logspace(3, 6, 100)
    for k in KINDS:
        ax.loglog(ctx, ctx * kv_bytes_per_token(k) / 1e9, color=KCOL[k], lw=2.4, label=k)
    for gb, lab in [(80, "1× H100 (80 GB)"), (1128, "8× H200 node (1.1 TB)")]:
        ax.axhline(gb, color=GRAY, ls="--", lw=1); ax.text(1100, gb * 1.2, lab, fontsize=8, color=GRAY)
    ax.axvline(128000, color=GRAY, ls=":"); ax.text(128000, 0.05, "128K\ncontext", fontsize=8, ha="center")
    ax.set_xlabel("context length (tokens)"); ax.set_ylabel("KV cache for ONE conversation (GB)")
    ax.set_title("Cache for a single user as context grows"); ax.legend(fontsize=8, loc="lower right")
    ax.set_ylim(0.03, 1e4)
    save(fig, OUT, "03_cache_sizes.png")


# ------------------------------------------------------------------ 04 architectures
def fig_architectures():
    fig, axes = plt.subplots(1, 4, figsize=(16, 5))
    titles = ["Multi-Head (MHA)\n2017 · GPT-3", "Multi-Query (MQA)\n2019 · PaLM, Falcon",
              "Grouped-Query (GQA)\n2023 · Llama 2/3, Mistral", "Multi-head Latent (MLA)\n2024 · DeepSeek V2/V3/R1"]
    for ax, t in zip(axes, titles):
        ax.set_xlim(0, 8); ax.set_ylim(0, 8); ax.axis("off"); ax.set_title(t, fontsize=10.5)
    xs = [1.0, 2.6, 4.2, 5.8]

    def qrow(ax):
        for x in xs:
            box(ax, x - 0.5, 6.2, 1.0, 0.7, "Q", fc="#fef3c7", ec=AMBER, fs=9)

    def cached(ax, x, y, w, h, text):
        box(ax, x, y, w, h, text, fc="#dcfce7", ec=GREEN, fs=8.5, lw=2.2)

    # MHA
    ax = axes[0]; qrow(ax)
    for x in xs:
        cached(ax, x - 0.55, 3.8, 1.1, 1.2, "K\nV")
        arrow(ax, x, 5.0, x, 6.2, color=GRAY)
    ax.text(4, 2.9, "every head has its own K, V", ha="center", fontsize=8.5)
    # MQA
    ax = axes[1]; qrow(ax)
    cached(ax, 2.2, 3.8, 2.2, 1.2, "one shared\nK, V")
    for x in xs:
        arrow(ax, 3.3, 5.0, x, 6.2, color=GRAY)
    ax.text(4, 2.9, "all heads share ONE K, V", ha="center", fontsize=8.5)
    # GQA
    ax = axes[2]; qrow(ax)
    for gx, pair in [(1.8, xs[:2]), (5.0, xs[2:])]:
        cached(ax, gx - 0.6, 3.8, 1.2, 1.2, "K\nV")
        for x in pair:
            arrow(ax, gx, 5.0, x, 6.2, color=GRAY)
    ax.text(4, 2.9, "heads share K, V within groups", ha="center", fontsize=8.5)
    # MLA
    ax = axes[3]; qrow(ax)
    for x in xs:
        box(ax, x - 0.5, 4.4, 1.0, 0.9, "W_UK\nW_UV", fc="white", ec=PURPLE, fs=7.5)
        arrow(ax, x, 5.3, x, 6.2, color=GRAY)
        arrow(ax, 4.0, 3.5, x, 4.4, color=PURPLE)
    cached(ax, 1.6, 2.6, 4.8, 0.9, "small shared latent c")
    ax.text(4, 1.9, "each head DECODES its own K, V\nfrom one compressed latent", ha="center", fontsize=8.5)
    for ax in axes:
        box(ax, 1.5, 0.3, 5.0, 0.8, "input x (the token)", fc="#eff6ff", ec=BLUE, fs=9)
    for ax in axes[:3]:
        arrow(ax, 4, 1.1, 4, 3.8 if ax is not axes[1] else 3.8, color=BLUE)
    arrow(axes[3], 4, 1.1, 4, 2.6, color=BLUE)
    fig.text(0.5, 0.0, "green = what must be stored in the KV cache for every past token", ha="center", fontsize=10,
             color=GREEN, weight="bold")
    save(fig, OUT, "04_attention_variants.png")


# ------------------------------------------------------------------ 05 low-rank structure across heads (simulation)
def fig_low_rank():
    n_tok, heads, hd, true_rank = 400, 32, 64, 48
    latent = rng.normal(size=(n_tok, true_rank))
    heads_mix = rng.normal(size=(heads * hd, true_rank)) / np.sqrt(true_rank)
    K = latent @ heads_mix.T + 0.15 * rng.normal(size=(n_tok, heads * hd))   # all heads' keys, concatenated
    U, S, Vt = np.linalg.svd(K, full_matrices=False)
    ranks = np.arange(1, 200)
    err = [np.linalg.norm(K - (U[:, :r] * S[:r]) @ Vt[:r]) / np.linalg.norm(K) for r in ranks]
    fig, axes = plt.subplots(1, 2, figsize=(14, 4))
    ax = axes[0]
    ax.semilogy(S[:200], color=BLUE, lw=2)
    ax.axvline(true_rank, color=GREEN, ls="--"); ax.text(true_rank + 4, S[0] / 3, f"shared structure\n(rank {true_rank})", color=GREEN, fontsize=9)
    ax.set_xlabel("component index"); ax.set_ylabel("singular value (log)")
    ax.set_title(f"Keys of {heads} heads × {hd} dims = {heads*hd} numbers per token…\nbut most variation lives in a few directions")
    ax = axes[1]
    ax.plot(ranks, np.array(err) * 100, color=PURPLE, lw=2)
    ax.axvline(true_rank, color=GREEN, ls="--")
    ax.set_xlabel("latent size kept (numbers cached per token)"); ax.set_ylabel("reconstruction error (%)")
    ax.set_title(f"Caching a {true_rank}-number latent recovers the {heads*hd}-number keys\nwith small error ({heads*hd/true_rank:.0f}× less memory)")
    ax.grid(alpha=0.3)
    save(fig, OUT, "05_low_rank_intuition.png")


# ------------------------------------------------------------------ 06 users per node
def fig_users():
    node_gb, weights_gb, ctx = 1128, 700, 32000
    free = (node_gb - weights_gb) * 1e9
    fig, ax = plt.subplots(figsize=(8, 3.8))
    users = [free / (kv_bytes_per_token(k) * ctx) for k in KINDS]
    bars = ax.bar(KINDS, users, color=[KCOL[k] for k in KINDS])
    for b, u in zip(bars, users):
        ax.text(b.get_x() + b.get_width() / 2, u * 1.1, f"{u:,.0f}", ha="center", fontsize=10, weight="bold")
    ax.set_yscale("log"); ax.set_ylabel("simultaneous 32K-token chats")
    ax.set_title("Why cache size = money: conversations that fit on one 8×H200 server\n"
                 "(1,128 GB total, ~700 GB for DeepSeek-R1 weights in FP8, rest for KV cache)")
    ax.set_ylim(1, 1e4)
    save(fig, OUT, "06_users_per_server.png")


# ------------------------------------------------------------------ 07 absorbing weights & RoPE
def fig_absorb():
    fig, ax = canvas(13, 5.4, (0, 13), (0, 5.4))
    ax.text(6.5, 5.1, "The 'absorb the up-projection' trick — and why RoPE breaks it", ha="center", fontsize=12, weight="bold")
    box(ax, 0.3, 3.0, 6.0, 1.7,
        "Attention score for one head:\n"
        "q · k   =   q · (W_UK c)   =   (W_UKᵀ q) · c\n\n"
        "→ fold W_UKᵀ into the query projection;\n   compare directly with the cached latent c",
        fc="#f0fdf4", ec=GREEN, fs=9.5)
    box(ax, 0.3, 0.6, 6.0, 1.9,
        "Values:  Σ_j A_ij (W_UV c_j)  =  W_UV ( Σ_j A_ij c_j )\n\n"
        "→ take the weighted sum of LATENTS first,\n   then apply W_UV once (fold into output W_O)",
        fc="#f0fdf4", ec=GREEN, fs=9.5)
    box(ax, 6.8, 2.6, 5.9, 2.1,
        "Problem: RoPE (rotary position encoding)\n"
        "rotates q and k by their positions:\n"
        "(R_i q) · (R_j W_UK c) — the rotation R_j sits\n"
        "BETWEEN W_UK and c, so W_UK can't be moved\n"
        "into the query (it would change with every position).",
        fc="#fef2f2", ec=RED, fs=9.5)
    box(ax, 6.8, 0.6, 5.9, 1.6,
        "DeepSeek's fix — 'decoupled RoPE':\n"
        "split each key into a content part (from the latent, no RoPE)\n"
        "+ a small 64-dim RoPE part shared by all heads.\n"
        "Cache = 512 latent + 64 RoPE = 576 numbers per layer.",
        fc="#eff6ff", ec=BLUE, fs=9.5)
    save(fig, OUT, "07_absorb_and_rope.png")


if __name__ == "__main__":
    fig_kv_idea(); fig_kv_speed(); fig_cache_sizes(); fig_architectures(); fig_low_rank(); fig_users(); fig_absorb()
    for k in KINDS:
        print(k, kv_bytes_per_token(k), "bytes/token")
