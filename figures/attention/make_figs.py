"""Figures for 'Attention in Transformers - Queries Keys and Values'.
The attention heatmaps are computed by a real (hand-built, tiny) attention head, not drawn by hand.
Run:  python figures/attention/make_figs.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _style import *

OUT = out_dir(__file__)
rng = np.random.default_rng(0)

TOKENS = ["a", "fluffy", "blue", "creature", "roamed", "the", "verdant", "forest"]
TYPES = ["det", "adj", "adj", "noun", "verb", "det", "adj", "noun"]


def softmax(z, axis=-1):
    z = z - np.max(np.where(np.isfinite(z), z, -1e30), axis=axis, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=axis, keepdims=True)


def toy_head():
    """A single hand-built head: nouns look for adjectives shortly before them."""
    n = len(TOKENS)
    kinds = ["det", "adj", "noun", "verb"]
    onehot = np.array([[1.0 if t == k else 0.0 for k in kinds] for t in TYPES])
    # sinusoidal positional encoding: dot product of two positions depends on their distance
    freqs = np.array([0.35, 0.7, 1.1, 1.6])
    pos = np.arange(n)[:, None] * freqs[None, :]
    P = np.concatenate([np.cos(pos), np.sin(pos)], 1)  # (n, 8)
    E = np.concatenate([onehot, P], 1)                 # embeddings (n, 12)
    d_k = 9
    W_Q = np.zeros((d_k, E.shape[1])); W_K = np.zeros((d_k, E.shape[1]))
    W_Q[0, 2] = 6.0          # query dim 0 fires for nouns: "any adjectives before me?"
    W_K[0, 1] = 1.0          # key dim 0 fires for adjectives: "I am an adjective"
    W_Q[1:, 4:] = np.eye(8) * 1.3   # position part: prefer nearby tokens
    W_K[1:, 4:] = np.eye(8) * 1.3
    Q = E @ W_Q.T; K = E @ W_K.T
    scores = Q @ K.T / np.sqrt(d_k)
    mask = np.triu(np.ones((n, n), bool), 1)      # True where key is AFTER query
    masked = np.where(mask, -np.inf, scores)
    A = softmax(masked, -1)
    return E, Q, K, scores, masked, A


# ------------------------------------------------------------------ 01 context changes meaning
def fig_embedding_shift():
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6))
    ax = axes[0]
    ax.set_xlim(-1.4, 1.6); ax.set_ylim(-1.3, 1.5); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("'mole' starts with ONE generic vector…\nattention adds a context-dependent ΔE")
    base = np.array([0.45, 0.05])
    ax.annotate("", base, (0, 0), arrowprops=dict(arrowstyle="-|>", color=DARK, lw=2.5))
    ax.text(0.2, -0.3, "E(mole)\ngeneric lookup", fontsize=9, color=DARK)
    for vec, lab, col in [((-1.1, 1.0), "animal sense\n('American shrew mole')", GREEN),
                          ((1.3, 0.9), "chemistry sense\n('one mole of CO₂')", BLUE),
                          ((0.6, -1.1), "skin sense\n('biopsy of the mole')", RED)]:
        v = np.array(vec)
        ax.annotate("", v, (0, 0), arrowprops=dict(arrowstyle="-|>", color=col, lw=1.6, alpha=0.35, ls="--"))
        ax.annotate("", v, base, arrowprops=dict(arrowstyle="-|>", color=col, lw=2))
        ax.text(v[0] * 1.02, v[1] + (0.08 if v[1] > 0 else -0.28), lab, fontsize=9, color=col, ha="center")
        mid = (base + v) / 2
        ax.text(mid[0] + 0.05, mid[1] + 0.05, "+ΔE", color=col, fontsize=9, weight="bold")
    ax = axes[1]
    ax.set_xlim(-0.2, 2.1); ax.set_ylim(-0.3, 1.9); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("'tower' gets more specific as context arrives")
    pts = [((0, 0), (1.3, 0.3), "E(tower)\n'tall, large noun'", GRAY),
           ((1.3, 0.3), (1.7, 1.2), "+ 'Eiffel' → Paris, steel, France", BLUE),
           ((1.7, 1.2), (0.9, 1.65), "+ 'miniature' → small, souvenir", PURPLE)]
    for s, e, lab, col in pts:
        ax.annotate("", e, s, arrowprops=dict(arrowstyle="-|>", color=col, lw=2.4))
        ax.text(e[0] + 0.03, e[1] + 0.03, lab, color=col, fontsize=9)
    save(fig, OUT, "01_context_changes_meaning.png")


# ------------------------------------------------------------------ 02 Q K V pipeline
def fig_qkv_pipeline():
    fig, ax = canvas(13, 6.2, (0, 13), (0, 6.2))
    ax.text(6.5, 5.9, "One attention head — what happens to every token, in parallel", ha="center",
            fontsize=13, weight="bold")
    box(ax, 0.2, 2.4, 1.6, 1.4, "embeddings E\n(one vector\nper token)\n12,288-dim", fc="#eff6ff", ec=BLUE, fs=9)
    rows = [(4.6, "W_Q", "queries  q\n\"what am I\nlooking for?\"", AMBER),
            (3.1, "W_K", "keys  k\n\"what do I\ncontain?\"", TEAL),
            (1.1, "W_V", "values  v\n\"what I'd add\nif relevant\"", PURPLE)]
    for y, w, lab, col in rows:
        arrow(ax, 1.8, 3.1, 2.6, y + 0.4, color=GRAY)
        box(ax, 2.6, y, 1.0, 0.8, w, fc="white", ec=col, fs=10, weight="bold")
        arrow(ax, 3.6, y + 0.4, 4.2, y + 0.4, color=col)
        box(ax, 4.2, y - 0.1, 1.7, 1.0, lab, fc="white", ec=col, fs=8.5)
    box(ax, 6.6, 3.6, 1.8, 1.5, "dot product\nevery q with\nevery k\n÷ √d_k", fc="#fffbeb", ec=AMBER, fs=9)
    arrow(ax, 5.9, 5.0, 6.6, 4.6, color=AMBER); arrow(ax, 5.9, 3.5, 6.6, 4.1, color=TEAL)
    box(ax, 9.0, 3.6, 1.6, 1.5, "mask future\n(−∞)\nthen\nsoftmax", fc="#fef2f2", ec=RED, fs=9)
    arrow(ax, 8.4, 4.35, 9.0, 4.35, color=DARK)
    # tiny heatmap icon
    A = toy_head()[-1]
    axh = fig.add_axes([0.845, 0.56, 0.12, 0.25])
    axh.imshow(A, cmap="Blues", vmin=0, vmax=1); axh.set_xticks([]); axh.set_yticks([])
    axh.set_title("attention\npattern", fontsize=8)
    arrow(ax, 10.6, 4.35, 11.0, 4.35, color=DARK)
    box(ax, 6.6, 0.8, 3.0, 1.5, "weighted sum of values\nΔE_i = Σ_j A_ij · v_j\n(big weight → big contribution)",
        fc="#f5f3ff", ec=PURPLE, fs=9)
    arrow(ax, 5.9, 1.5, 6.6, 1.5, color=PURPLE)
    arrow(ax, 11.6, 3.3, 9.0, 2.3, color=BLUE, rad=0.15, text="weights A", fs=8)
    box(ax, 10.4, 0.8, 2.4, 1.5, "E_new = E + ΔE\ncontext-aware\nembedding", fc="#f0fdf4", ec=GREEN, fs=9.5,
        weight="bold")
    arrow(ax, 9.6, 1.55, 10.4, 1.55, color=GREEN)
    ax.text(0.2, 0.2, "Learned parameters: only W_Q, W_K, W_V (and the output matrix). Everything else is fixed arithmetic.",
            fontsize=9, color=GRAY)
    save(fig, OUT, "02_qkv_pipeline.png")


# ------------------------------------------------------------------ 03 attention pattern computed
def fig_attention_pattern():
    E, Q, K, scores, masked, A = toy_head()
    n = len(TOKENS)
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.2))
    labs = [f"{t}" for t in TOKENS]
    im = axes[0].imshow(scores, cmap="RdBu_r", vmin=-np.abs(scores).max(), vmax=np.abs(scores).max())
    axes[0].set_title("① raw scores  q_i · k_j / √d_k\n(any real number)")
    for i in range(n):
        for j in range(n):
            axes[0].text(j, i, f"{scores[i,j]:.1f}", ha="center", va="center", fontsize=7)
    m2 = np.where(np.isfinite(masked), masked, np.nan)
    cmap2 = plt.get_cmap("RdBu_r").copy(); cmap2.set_bad("#374151")
    axes[1].imshow(m2, cmap=cmap2, vmin=-np.abs(scores).max(), vmax=np.abs(scores).max())
    axes[1].set_title("② causal mask: future → −∞\n(dark cells: a word may not look ahead)")
    for i in range(n):
        for j in range(n):
            axes[1].text(j, i, "−∞" if j > i else f"{scores[i,j]:.1f}", ha="center", va="center", fontsize=7,
                         color="white" if j > i else DARK)
    axes[2].imshow(A, cmap="Blues", vmin=0, vmax=1)
    axes[2].set_title("③ softmax each row → attention pattern\n(each row sums to 1)")
    for i in range(n):
        for j in range(n):
            if j <= i:
                axes[2].text(j, i, f"{A[i,j]:.2f}", ha="center", va="center", fontsize=7,
                             color="white" if A[i, j] > 0.55 else DARK)
    for ax in axes:
        ax.set_xticks(range(n)); ax.set_xticklabels(labs, rotation=45, ha="right")
        ax.set_yticks(range(n)); ax.set_yticklabels(labs)
        ax.set_xlabel("key: the word being looked AT  (j)")
    axes[0].set_ylabel("query: the word being updated  (i)")
    for r, c in [(3, 1), (3, 2), (7, 6)]:
        axes[2].add_patch(Rectangle((c - 0.5, r - 0.5), 1, 1, fill=False, ec=AMBER, lw=2.5))
    fig.suptitle("A real (tiny, hand-built) attention head: nouns look back for their adjectives",
                 weight="bold", y=1.02)
    save(fig, OUT, "03_attention_pattern.png")


# ------------------------------------------------------------------ 04 why divide by sqrt(d_k)
def fig_scaling():
    dks = np.array([4, 16, 64, 128, 512, 2048])
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    ent_raw, ent_scaled, std_raw = [], [], []
    for d in dks:
        q = rng.normal(size=(2000, 1, d)); k = rng.normal(size=(2000, 16, d))
        s = (q * k).sum(-1)
        std_raw.append(s.std())
        for arr, lst in [(s, ent_raw), (s / np.sqrt(d), ent_scaled)]:
            p = softmax(arr, -1)
            lst.append(float(np.mean(-(p * np.log(p + 1e-12)).sum(-1))))
    ax = axes[0]
    ax.plot(dks, std_raw, "o-", color=RED, lw=2, label="spread of raw q·k")
    ax.plot(dks, np.sqrt(dks), "--", color=GRAY, label="√d_k (theory)")
    ax.plot(dks, np.ones_like(dks), "o-", color=GREEN, lw=2, label="spread after ÷ √d_k")
    ax.set_xscale("log", base=2); ax.set_xlabel("key/query dimension d_k"); ax.set_ylabel("standard deviation")
    ax.set_title("Dot products of random vectors grow like √d_k"); ax.legend(fontsize=8)
    ax = axes[1]
    ax.plot(dks, ent_raw, "o-", color=RED, lw=2, label="without scaling")
    ax.plot(dks, ent_scaled, "o-", color=GREEN, lw=2, label="with ÷ √d_k")
    ax.axhline(np.log(16), color=GRAY, ls=":", lw=1); ax.text(4.3, np.log(16) - 0.18, "uniform over 16 tokens", fontsize=8, color=GRAY)
    ax.set_xscale("log", base=2); ax.set_xlabel("key/query dimension d_k"); ax.set_ylabel("entropy of attention row (nats)")
    ax.set_title("Unscaled scores make softmax 'one-hot'\n→ near-zero gradients, training stalls"); ax.legend(fontsize=8)
    save(fig, OUT, "04_why_sqrt_dk.png")


# ------------------------------------------------------------------ 05 softmax & masking trick
def fig_softmax_mask():
    s = np.array([2.0, 1.0, 0.1, 3.0, -1.0])
    labels = ["a", "fluffy", "blue", "creature", "roamed"]
    fig, axes = plt.subplots(1, 3, figsize=(13, 3.6), sharey=False)
    axes[0].bar(labels, s, color=[GRAY, GRAY, GRAY, RED, RED]); axes[0].axhline(0, color=DARK, lw=0.8)
    axes[0].set_title("raw scores for the query 'fluffy'\n(red = tokens AFTER 'fluffy')")
    p_bad = softmax(s); p_bad[3:] = 0
    axes[1].bar(labels, p_bad, color=[GRAY, GRAY, GRAY, RED, RED])
    axes[1].set_title(f"✗ softmax, THEN zero the future\nrow sums to {p_bad.sum():.2f} — broken")
    m = s.copy(); m[3:] = -np.inf
    p_good = softmax(m)
    axes[2].bar(labels, p_good, color=[GREEN, GREEN, GREEN, RED, RED])
    axes[2].set_title(f"✓ set future to −∞, THEN softmax\nrow sums to {p_good.sum():.2f}")
    for ax in axes[1:]:
        ax.set_ylim(0, 1)
    for ax in axes:
        ax.tick_params(axis="x", rotation=30)
    save(fig, OUT, "05_masking_trick.png")


# ------------------------------------------------------------------ 06 quadratic cost
def fig_quadratic():
    L = np.logspace(3, 6.2, 60)
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))
    ax = axes[0]
    heads, layers, bytes_ = 96, 96, 2
    mem_naive = L ** 2 * heads * layers * bytes_ / 1e9
    ax.loglog(L, mem_naive, color=RED, lw=2.5, label="naive: store every n×n attention matrix\n(96 layers × 96 heads, fp16)")
    ax.loglog(L, L * 12288 * 2 * layers * bytes_ / 1e9, color=GREEN, lw=2.5,
              label="FlashAttention-style: never store n×n\n(memory grows only linearly)")
    ax.axhline(80, color=GRAY, ls="--"); ax.text(1100, 95, "one 80 GB GPU", fontsize=8, color=GRAY)
    for name, n in [("GPT-3\n2K", 2048), ("GPT-4 Turbo\n128K", 128000), ("Gemini 1.5\n1M", 1e6)]:
        ax.axvline(n, color=GRAY, ls=":", lw=1); ax.text(n, 3e7, name, fontsize=8, ha="center")
    ax.set_xlabel("context length n (tokens)"); ax.set_ylabel("memory (GB)")
    ax.set_title("Attention memory at GPT-3 scale"); ax.legend(fontsize=7.5, loc="lower right")
    ax.set_ylim(1, 3e8)
    ax = axes[1]
    d = 12288
    attn_mat = 2 * L * d        # per-token FLOPs from the n×n part (score + weighted sum), per layer
    dense = 24 * d ** 2         # per-token FLOPs of the weight matrices (QKVO + MLP), fwd per layer
    ax.semilogx(L, attn_mat / (attn_mat + dense) * 100, color=PURPLE, lw=2.5)
    ax.set_xlabel("context length n (tokens)"); ax.set_ylabel("% of compute per token")
    ax.set_title("Share of compute spent on the n×n attention part\n(GPT-3 width, rest = weight matrices & MLP)")
    ax.set_ylim(0, 100); ax.grid(alpha=0.3)
    for n in [2048, 128000, 1e6]:
        v = 2 * n * d / (2 * n * d + dense) * 100
        ax.scatter([n], [v], color=PURPLE, zorder=4); ax.text(n, v + 4, f"{v:.0f}%", ha="center", fontsize=9)
    save(fig, OUT, "06_quadratic_cost.png")


# ------------------------------------------------------------------ 07 GPT-3 parameter breakdown
def fig_params():
    d, layers, vocab, dk, heads = 12288, 96, 50257, 128, 96
    per_head = 4 * d * dk
    attn_block = heads * per_head
    attn = layers * attn_block
    mlp = layers * 8 * d * d
    emb = vocab * d
    total = attn + mlp + emb
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.2), gridspec_kw=dict(width_ratios=[1, 1.2]))
    ax = axes[0]
    ax.pie([mlp, attn, emb], labels=[f"MLP blocks\n{mlp/1e9:.0f} B", f"Attention\n{attn/1e9:.0f} B", f"Embeddings\n{emb/1e9:.1f} B"],
           colors=[BLUE, AMBER, GRAY], autopct=lambda p: f"{p:.0f}%" if p >= 1 else "", startangle=90, wedgeprops=dict(ec="white", lw=2),
           textprops=dict(fontsize=9))
    ax.set_title(f"GPT-3: {total/1e9:.0f} B parameters\n(attention is only about ⅓)")
    ax = axes[1]; ax.axis("off")
    rows = [("W_Q", "128 × 12,288", 128 * d), ("W_K", "128 × 12,288", 128 * d),
            ("W_V↓ (value-down)", "128 × 12,288", 128 * d), ("W_V↑ (value-up / output)", "12,288 × 128", 128 * d),
            ("one head", "4 matrices", per_head), ("one block (96 heads)", "", attn_block),
            ("96 layers", "", attn)]
    ax.text(0.0, 1.0, "Attention parameter count", fontsize=11, weight="bold", va="top", transform=ax.transAxes)
    for i, (a, b, c) in enumerate(rows):
        y = 0.86 - i * 0.12
        bold = "bold" if i >= 4 else "normal"
        ax.text(0.0, y, a, fontsize=10, weight=bold, transform=ax.transAxes); ax.text(0.5, y, b, fontsize=10, color=GRAY, transform=ax.transAxes)
        ax.text(1.0, y, f"{c:,.0f}", fontsize=10, ha="right", weight=bold, transform=ax.transAxes)
        if i == 3:
            ax.plot([0, 1], [y - 0.04, y - 0.04], color=LIGHT, transform=ax.transAxes)
    save(fig, OUT, "07_gpt3_param_breakdown.png")


# ------------------------------------------------------------------ 08 multi-head patterns
def fig_multihead():
    n = 10
    words = ["When", "Mary", "and", "John", "went", "to", "the", "store", ",", "John"]
    heads = {}
    prev = np.full((n, n), -np.inf)
    for i in range(n):
        prev[i, max(i - 1, 0)] = 5; prev[i, i] = 1
    heads["previous-token head\n(copies the word before)"] = prev
    sink = np.full((n, n), -np.inf)
    for i in range(n):
        sink[i, :i + 1] = 0; sink[i, 0] = 4
    heads["'attention sink'\n(parks on the first token)"] = sink
    ind = np.full((n, n), -np.inf)
    for i in range(n):
        ind[i, :i + 1] = 0
    ind[9, 4] = 5  # second "John" attends to token after first "John"
    heads["induction head\n(…John went → next time 'John', look at 'went')"] = ind
    local = np.full((n, n), -np.inf)
    for i in range(n):
        for j in range(i + 1):
            local[i, j] = -0.9 * (i - j)
    heads["local window\n(nearby words matter more)"] = local
    fig, axes = plt.subplots(1, 4, figsize=(16, 4.6))
    for ax, (title, s) in zip(axes, heads.items()):
        A = softmax(s, -1)
        ax.imshow(A, cmap="Purples", vmin=0, vmax=1)
        ax.set_title(title, fontsize=9.5)
        ax.set_xticks(range(n)); ax.set_xticklabels(words, rotation=60, fontsize=7.5)
        ax.set_yticks(range(n)); ax.set_yticklabels(words, fontsize=7.5)
    fig.suptitle("Multi-head attention: each head learns its own pattern (these 4 types are really found in trained LLMs)",
                 weight="bold", y=1.02)
    save(fig, OUT, "08_multihead_patterns.png")


# ------------------------------------------------------------------ 09 transformer block / residual stream
def fig_block():
    fig, ax = canvas(12, 5.2, (0, 12), (0, 5.2))
    ax.text(6, 5.0, "Where attention lives: the residual stream of a GPT-style transformer", ha="center",
            fontsize=12, weight="bold")
    ax.add_patch(Rectangle((0.5, 2.35), 11.0, 0.5, fc="#dbeafe", ec=BLUE, lw=1.2))
    ax.text(0.6, 2.6, "residual stream (one vector per token flows left → right)", fontsize=8.5, color=BLUE, va="center")
    box(ax, 0.2, 0.6, 1.5, 1.0, "tokens →\nembedding\n+ position", fc="#eff6ff", ec=BLUE, fs=8.5)
    arrow(ax, 0.95, 1.6, 0.95, 2.35, color=BLUE)
    x = 2.3
    for layer in range(2):
        box(ax, x, 3.3, 1.9, 1.1, "LayerNorm →\nmulti-head\nattention", fc="#fffbeb", ec=AMBER, fs=8.5)
        arrow(ax, x + 0.3, 2.85, x + 0.3, 3.3, color=AMBER)
        arrow(ax, x + 1.6, 3.3, x + 1.6, 2.85, color=AMBER, text="+ΔE", fs=8, toff=(0.3, -0.05))
        box(ax, x + 2.4, 0.9, 1.9, 1.1, "LayerNorm →\nMLP\n(per token)", fc="#eef2ff", ec=PURPLE, fs=8.5)
        arrow(ax, x + 2.7, 2.35, x + 2.7, 2.0, color=PURPLE)
        arrow(ax, x + 4.0, 2.0, x + 4.0, 2.35, color=PURPLE, text="+", fs=9, toff=(0.2, -0.1))
        ax.text(x + 2.1, 4.55, f"layer {layer + 1}" if layer == 0 else "layer 2 … 96", ha="center", fontsize=9, weight="bold")
        x += 4.6
    box(ax, 10.6, 3.3, 1.3, 1.1, "unembed →\nsoftmax →\nnext token", fc="#f0fdf4", ec=GREEN, fs=8.5)
    arrow(ax, 11.25, 2.85, 11.25, 3.3, color=GREEN)
    ax.text(6, 0.15, "Attention = tokens TALK to each other (move information between positions).   "
                     "MLP = each token THINKS on its own (looks up / transforms facts).",
            ha="center", fontsize=9, color=DARK)
    save(fig, OUT, "09_transformer_block.png")


# ------------------------------------------------------------------ 10 RNN vs attention
def fig_rnn_vs_attention():
    fig, axes = plt.subplots(1, 2, figsize=(15, 3.8))
    words = ["The", "murderer", "…", "…", "was"]
    for ax in axes:
        ax.set_xlim(-0.5, 5); ax.set_ylim(-0.6, 2.6); ax.axis("off")
    ax = axes[0]
    ax.set_title("RNN / LSTM (before 2017): read one word at a time\ninfo from word 1 must survive n hops · cannot parallelize")
    for i, w in enumerate(words):
        ax.add_patch(FancyBboxPatch((i - 0.35, 1.0), 0.7, 0.6, boxstyle="round,pad=0.02", fc="#fef2f2", ec=RED))
        ax.text(i, 1.3, f"h{i+1}", ha="center", va="center", fontsize=9)
        ax.text(i, 0.2, w, ha="center", fontsize=9)
        arrow(ax, i, 0.45, i, 1.0, color=GRAY)
        if i < 4:
            arrow(ax, i + 0.35, 1.3, i + 0.65, 1.3, color=RED)
        ax.text(i, 1.85, f"step {i+1}", ha="center", fontsize=8, color=RED)
    ax = axes[1]
    ax.set_title("Attention (transformer): every word looks at every earlier word directly\n1 hop between any two words · all positions computed at once on a GPU")
    for i, w in enumerate(words):
        ax.add_patch(FancyBboxPatch((i - 0.35, 1.0), 0.7, 0.6, boxstyle="round,pad=0.02", fc="#f0fdf4", ec=GREEN))
        ax.text(i, 1.3, f"h{i+1}", ha="center", va="center", fontsize=9)
        ax.text(i, 0.2, w, ha="center", fontsize=9)
        arrow(ax, i, 0.45, i, 1.0, color=GRAY)
        for j in range(i):
            ax.add_patch(FancyArrowPatch((j, 1.6), (i, 1.6), arrowstyle="-|>", mutation_scale=8, color=GREEN,
                                         lw=0.9, connectionstyle=f"arc3,rad=-{0.25 + 0.05*(i-j)}", alpha=0.7))
    ax.text(2, 2.45, "all at the same time", ha="center", fontsize=8, color=GREEN)
    save(fig, OUT, "10_rnn_vs_attention.png")


# ------------------------------------------------------------------ 11 self vs cross attention
def fig_self_cross():
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.6))
    for ax in axes:
        ax.set_xlim(0, 6); ax.set_ylim(0, 3.2); ax.axis("off")
    ax = axes[0]; ax.set_title("SELF-attention (GPT, BERT)\nQ, K, V all come from the same sequence")
    box(ax, 1.5, 0.3, 3, 0.7, "one sequence: 'the cat sat'", fc="#eff6ff", ec=BLUE, fs=9)
    for x, l in [(1.8, "Q"), (3.0, "K"), (4.2, "V")]:
        arrow(ax, x, 1.0, x, 1.9, color=BLUE)
        ax.text(x, 2.05, l, ha="center", fontsize=12, weight="bold", color=BLUE)
    ax.text(3, 2.7, "causal mask in decoders (GPT)\nno mask in encoders (BERT)", ha="center", fontsize=8.5, color=GRAY)
    ax = axes[1]; ax.set_title("CROSS-attention (translation, Whisper, image generators)\nQ from one stream, K & V from another")
    box(ax, 0.2, 0.3, 2.6, 0.7, "French being written\n'le chat …'", fc="#fff7ed", ec=AMBER, fs=9)
    box(ax, 3.2, 0.3, 2.6, 0.7, "English source / audio /\ntext prompt", fc="#f0fdf4", ec=GREEN, fs=9)
    arrow(ax, 1.5, 1.0, 1.5, 1.9, color=AMBER); ax.text(1.5, 2.05, "Q", ha="center", fontsize=12, weight="bold", color=AMBER)
    for x, l in [(4.0, "K"), (5.0, "V")]:
        arrow(ax, x, 1.0, x, 1.9, color=GREEN); ax.text(x, 2.05, l, ha="center", fontsize=12, weight="bold", color=GREEN)
    ax.text(3, 2.7, "no causal mask across streams", ha="center", fontsize=8.5, color=GRAY)
    save(fig, OUT, "11_self_vs_cross.png")


if __name__ == "__main__":
    fig_embedding_shift(); fig_qkv_pipeline(); fig_attention_pattern(); fig_scaling(); fig_softmax_mask()
    fig_quadratic(); fig_params(); fig_multihead(); fig_block(); fig_rnn_vs_attention(); fig_self_cross()
