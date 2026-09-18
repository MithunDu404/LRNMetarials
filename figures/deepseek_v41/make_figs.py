"""Figures for 'DeepSeek V4.1 Flash - Extreme KV Cache Compression'.

Every plot is either computed from the paper's published configuration
(Section 4.2.1) or plots numbers the paper reports.  Figures that use assumed
hardware constants say so on the figure itself.

    python figures/deepseek_v41/make_figs.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _style import *

OUT = out_dir(__file__)

# --- published configuration (tech report Section 4.2.1) --------------------
LAYERS, ENC, DEC, SWA_ONLY = 40, 20, 20, 2
WIN, TOP_K = 128, 512
CAND_POOL = 2048 * 8                     # 16,384 positions
KV_V41 = 890                             # bytes/token, global KV, in HBM
KV_V4F = KV_V41 * 4                      # "roughly 1/4 of V4-Flash"
KV_V1 = KV_V41 * 437                     # "approximately 437-fold vs V1"


def layer_map():
    """Per-layer mode assignment, rebuilt from Section 4.2.1."""
    L = [("SWA-only", 2)] * SWA_ONLY
    for _ in range(3):                               # encoder: 3 groups of 6
        L += [("Full", 2)] + [("Reuse", 2)] * 5
    for g in range(5):                               # decoder: 5 groups of 4
        L += [("Full" if g == 0 else "Reindex", 1)] + [("Reuse", 1)] * 3
    assert len(L) == LAYERS
    return L


MODE_COLOR = {"SWA-only": GRAY, "Full": RED, "Reindex": AMBER, "Reuse": GREEN}


# ---------------------------------------------------------------- figure 01
def fig_generations():
    fig, ax = plt.subplots(figsize=(8, 4.2))
    names = ["DeepSeek-V1\n(MHA)", "DeepSeek-V2/V3\n(MLA)", "DeepSeek-V4-Flash\n(CSA+HCA, FP8)",
             "DeepSeek-V4.1-Flash\n(CSA2, FP4)"]
    # V2/V3 MLA: 576 numbers/layer x 61 layers at FP8 -- computed from the V3 config
    mla = 576 * 61 * 1
    vals = [KV_V1, mla, KV_V4F, KV_V41]
    cols = [GRAY, BLUE, TEAL, RED]
    bars = ax.bar(range(4), vals, color=cols, width=0.6)
    ax.set_yscale("log")
    ax.set_ylabel("global KV cache (bytes per token)")
    ax.set_title("Seven years of shrinking the KV cache")
    ax.set_xticks(range(4)); ax.set_xticklabels(names, fontsize=8)
    ax.set_ylim(300, 1.2e6)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v * 1.25, f"{v:,.0f} B",
                ha="center", fontsize=9, weight="bold")
    ax.annotate("", xy=(2.95, KV_V41 * 2.2), xytext=(0.05, KV_V1 * 1.9),
                arrowprops=dict(arrowstyle="->", color=DARK, lw=1.4,
                                connectionstyle="arc3,rad=-0.18"))
    ax.text(1.5, 3.0e5, f"{KV_V1 / KV_V41:.0f}x smaller", fontsize=12, weight="bold",
            color=DARK, ha="center",
            bbox=dict(fc="white", ec="none", pad=2))
    fig.text(0.5, -0.09,
             "V1 and V4-Flash are back-computed from the ratios the paper states; V2/V3 is "
             "computed from the published MLA config (576 numbers x 61 layers, FP8).",
             ha="center", fontsize=8, color=GRAY)
    save(fig, OUT, "01_kv_cache_generations.png")


# ---------------------------------------------------------------- figure 02
def fig_memory_hierarchy():
    fig, ax = canvas(10, 5.8, (0, 10), (0, 5.9))
    ax.set_title("Where a conversation's memory actually lives", loc="left", weight="bold")
    tiers = [
        (3.75, "GPU compute", "#fee2e2", RED, "the processor", ""),
        (2.55, "HBM  (~192 GB)", "#fef3c7", AMBER, "fast, tiny, expensive", "global KV lives here"),
        (1.35, "Host DRAM  (TB)", "#dbeafe", BLUE, "10x slower", "Engram + short-lived SWA KV"),
        (0.15, "SSD  (100s of TB)", "#dcfce7", GREEN, "1000x slower", "persistent prefix cache"),
    ]
    for y, label, fc, ec, speed, holds in tiers:
        box(ax, 0.4, y, 4.4, 0.95, label, fc=fc, ec=ec, fs=10, weight="bold")
        ax.text(5.05, y + 0.62, speed, fontsize=9, color=ec, weight="bold", va="center")
        ax.text(5.05, y + 0.33, holds, fontsize=8.5, color=GRAY, va="center")
    for y in (3.55, 2.35, 1.15):
        arrow(ax, 2.6, y + 0.2, 2.6, y, color=DARK, lw=1.0)
        arrow(ax, 2.0, y, 2.0, y + 0.2, color=DARK, lw=1.0)
    ax.text(0.4, 5.8, "Every token generated must re-read the whole global cache.\n"
                      "If that cache does not fit in HBM, the GPU waits on the bus instead of computing.",
            fontsize=9.5, color=DARK, va="top")
    save(fig, OUT, "02_memory_hierarchy.png")


# ---------------------------------------------------------------- figure 03
def fig_layer_map():
    L = layer_map()
    fig, ax = plt.subplots(figsize=(11, 3.4))
    for i, (mode, ratio) in enumerate(L):
        ax.add_patch(Rectangle((i, 0), 0.86, 1, fc=MODE_COLOR[mode], ec="white", lw=1))
        if mode == "Full":
            ax.text(i + 0.43, 0.5, "F", ha="center", va="center", color="white",
                    fontsize=10, weight="bold")
        elif mode == "Reindex":
            ax.text(i + 0.43, 0.5, "R", ha="center", va="center", color="white",
                    fontsize=10, weight="bold")
    ax.plot([ENC, ENC], [-0.35, 1.5], color=DARK, lw=2, ls="--")
    ax.text(ENC / 2, 1.28, "CAUSAL ENCODER  (20 layers)", ha="center", fontsize=10,
            weight="bold", color=DARK)
    ax.text(ENC + DEC / 2, 1.28, "DECODER  (20 layers)", ha="center", fontsize=10,
            weight="bold", color=DARK)
    ax.text(ENC / 2, -0.30, "reads the prompt · rate 2 · 8B active",
            ha="center", fontsize=8.5, color=GRAY)
    ax.text(ENC + DEC / 2, -0.30,
            "writes the answer · rate 1 · 16B active · KV inherited",
            ha="center", fontsize=8.5, color=GRAY)
    counts = {}
    for m, _ in L:
        counts[m] = counts.get(m, 0) + 1
    handles = [plt.Rectangle((0, 0), 1, 1, fc=MODE_COLOR[m]) for m in
               ("SWA-only", "Full", "Reindex", "Reuse")]
    labels = [f"{m} ({counts[m]})" for m in ("SWA-only", "Full", "Reindex", "Reuse")]
    ax.legend(handles, labels, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.06),
              fontsize=9)
    ax.set_xlim(-0.4, LAYERS + 0.4); ax.set_ylim(-0.6, 1.6); ax.axis("off")
    ax.set_title("All 40 layers, coloured by what they actually compute "
                 "(rebuilt from the published config)", loc="left")
    fig.text(0.5, -0.11, f"Only the {counts['Full']} red layers build a KV cache of their own. "
                         f"The {counts['Reuse']} green layers compute neither KV nor an index — "
                         "they just read someone else's.",
             ha="center", fontsize=9.5, color=DARK)
    save(fig, OUT, "03_layer_map.png")


# ---------------------------------------------------------------- figure 04
def fig_csa2_modes():
    fig, axes = plt.subplots(1, 3, figsize=(11.5, 4.1))
    rows = ["main KV", "indexer K", "top-K indices", "query + SWA KV"]
    specs = {
        "Full Mode": ["compute", "compute", "compute", "compute"],
        "Reindex Mode": ["reuse", "reuse", "compute", "compute"],
        "Reuse Mode": ["reuse", "reuse", "reuse", "compute"],
    }
    counts = {"Full Mode": 4, "Reindex Mode": 4, "Reuse Mode": 30}
    for ax, (title, acts) in zip(axes, specs.items()):
        ax.set_xlim(0, 1); ax.set_ylim(-0.4, 4.3); ax.axis("off")
        n = counts[title]
        ax.set_title(f"{title}\n{n} of 38 CSA2 layers", fontsize=10.5)
        for j, (r, a) in enumerate(zip(rows, acts)):
            y = 3 - j
            fc, ec, tc = ("#fee2e2", RED, RED) if a == "compute" else ("#f3f4f6", GRAY, GRAY)
            box(ax, 0.04, y, 0.92, 0.72, "", fc=fc, ec=ec, lw=1.3)
            ax.text(0.1, y + 0.36, r, fontsize=9.5, va="center", color=DARK, weight="bold")
            ax.text(0.9, y + 0.36, a, fontsize=9, va="center", ha="right", color=tc,
                    style="italic")
        cost = acts.count("compute")
        ax.text(0.5, -0.3, f"computes {cost} of 4", ha="center", fontsize=9,
                color=DARK, weight="bold")
    fig.suptitle("CSA2's three modes: what each layer builds versus borrows", y=1.0,
                 fontsize=12, weight="bold")
    fig.text(0.5, -0.02, "Red = built in this layer.  Grey = taken from the nearest earlier "
                         "layer that built one.  Every layer still computes its own query and "
                         "its own sliding-window KV.", ha="center", fontsize=9, color=DARK)
    fig.tight_layout()
    save(fig, OUT, "04_csa2_modes.png")


# ---------------------------------------------------------------- figure 05
def fig_layer_dimension():
    """How much main-KV storage the layer dimension actually saves."""
    L = layer_map()
    csa2 = [x for x in L if x[0] != "SWA-only"]
    full = [x for x in csa2 if x[0] == "Full"]
    # relative "entries stored per token": rate 2 -> 0.5 entries/token, rate 1 -> 1
    naive = sum(1 / r for _, r in csa2)
    actual = sum(1 / r for _, r in full)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.1))

    ax1.bar([0, 1], [naive, actual], color=[GRAY, RED], width=0.55)
    ax1.set_xticks([0, 1])
    ax1.set_xticklabels([f"every CSA2 layer\nkeeps its own\n({len(csa2)} layers)",
                         f"CSA2 cross-layer reuse\n({len(full)} Full-mode layers)"], fontsize=9)
    ax1.set_ylabel("main-KV entries stored per token")
    ax1.set_title("The layer dimension")
    for x, v in zip([0, 1], [naive, actual]):
        ax1.text(x, v + 0.9, f"{v:.1f}", ha="center", fontsize=12, weight="bold")
    ax1.annotate(f"{naive / actual:.1f}x less to store", xy=(1, actual + 2.2),
                 xytext=(0.42, naive * 0.60), fontsize=10.5, weight="bold", color=DARK,
                 arrowprops=dict(arrowstyle="->", color=DARK, lw=1.3))
    ax1.set_ylim(0, naive * 1.25)

    ctx = [4_000, 32_000, 128_000, 1_000_000]
    x = np.arange(len(ctx))
    naive_gb = [naive / actual * KV_V41 * c / 1e9 for c in ctx]
    real_gb = [KV_V41 * c / 1e9 for c in ctx]
    ax2.bar(x - 0.2, naive_gb, 0.4, color=GRAY, label="without cross-layer reuse")
    ax2.bar(x + 0.2, real_gb, 0.4, color=RED, label="DeepSeek-V4.1-Flash (890 B/token)")
    ax2.axhline(192, color=AMBER, ls="--", lw=1.6)
    ax2.set_ylim(1e-3, 3e3)
    ax2.text(3.45, 260, "one 192 GB HBM module", fontsize=8.5, color=AMBER, weight="bold",
             ha="right")
    ax2.set_yscale("log"); ax2.set_xticks(x)
    ax2.set_xticklabels([f"{c // 1000}K" if c < 1e6 else "1M" for c in ctx])
    ax2.set_xlabel("context length (tokens)")
    ax2.set_ylabel("global KV cache for one conversation (GB)")
    ax2.set_title("What that means for one conversation")
    ax2.legend(fontsize=8.5, loc="upper left")
    fig.tight_layout()
    save(fig, OUT, "05_layer_dimension.png")


# ---------------------------------------------------------------- figure 06
def fig_hierarchical_indexer():
    index_layers = 8                      # 4 Full + 4 Reindex layers run an indexer
    n = np.logspace(np.log10(4_000), 6, 200)
    flat = index_layers * n
    hier = n + (index_layers - 1) * np.minimum(CAND_POOL, n)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.1))

    ax1.loglog(n, flat, color=GRAY, lw=2.4, label="every indexer scans the whole context")
    ax1.loglog(n, hier, color=RED, lw=2.4, label="Hierarchical Sparse Indexer")
    ax1.axvline(CAND_POOL, color=BLUE, ls=":", lw=1.4)
    ax1.text(CAND_POOL * 1.15, 6e4, f"candidate pool\n= {CAND_POOL:,} positions",
             fontsize=8.5, color=BLUE)
    ax1.set_xlabel("context length (tokens)")
    ax1.set_ylabel("positions scored per generated token")
    ax1.set_title("Indexing cost stops growing with context")
    ax1.legend(fontsize=8.5, loc="upper left")

    ratio = flat / hier
    ax2.semilogx(n, ratio, color=RED, lw=2.4)
    ax2.set_xlabel("context length (tokens)")
    ax2.set_ylabel("times less indexing work")
    ax2.set_title("The saving grows as the context does")
    for mark in (32_000, 128_000, 1_000_000):
        r = index_layers * mark / (mark + (index_layers - 1) * min(CAND_POOL, mark))
        ax2.plot([mark], [r], "o", color=DARK, ms=6)
        ax2.annotate(f"{r:.1f}x at {mark // 1000}K" if mark < 1e6 else f"{r:.1f}x at 1M",
                     xy=(mark, r), xytext=(mark * 0.28, r + 0.45), fontsize=9, color=DARK)
    ax2.set_ylim(0.8, 8.6)
    fig.text(0.5, -0.03, "The first Full-mode layer still scans the entire context — that is the "
                         "one term that never becomes constant, and it is why decode cost is "
                         "nearly, but not exactly, flat.", ha="center", fontsize=9, color=DARK)
    fig.tight_layout()
    save(fig, OUT, "06_hierarchical_indexer.png")


# ---------------------------------------------------------------- figure 07
def fig_prefill_split():
    n = np.logspace(2.7, 6, 200)
    plain = LAYERS * n
    ced = ENC * n + DEC * WIN
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.1))

    ax1.loglog(n, plain, color=GRAY, lw=2.4, label="all 40 layers read the prompt")
    ax1.loglog(n, ced, color=RED, lw=2.4,
               label="CED: 20 encoder layers + a 128-token decoder replay")
    ax1.set_xlabel("prompt length (tokens)")
    ax1.set_ylabel("prefill work (layer-tokens)")
    ax1.set_title("Reading the prompt costs half as much")
    ax1.legend(fontsize=8.5, loc="upper left")

    saving = 100 * (1 - ced / plain)
    ax2.semilogx(n, saving, color=RED, lw=2.4)
    ax2.axhline(50, color=GRAY, ls="--", lw=1.2)
    ax2.text(1e3, 51, "50% ceiling", fontsize=8.5, color=GRAY)
    ax2.set_xlabel("prompt length (tokens)")
    ax2.set_ylabel("prefill work saved (%)")
    ax2.set_ylim(0, 60)
    ax2.set_title("Approaching the ceiling almost immediately")
    ax2.annotate("even a 1,000-token prompt\nalready saves ~44%", xy=(1000, 43.6),
                 xytext=(2500, 22), fontsize=9, color=DARK,
                 arrowprops=dict(arrowstyle="->", color=DARK, lw=1.2))
    fig.text(0.5, -0.03, "Computed from the published architecture. Agentic workloads are "
                         "prefill-heavy — every tool result is a new prompt — so halving prefill "
                         "matters more than it would for chat.", ha="center", fontsize=9, color=DARK)
    fig.tight_layout()
    save(fig, OUT, "07_prefill_split.png")


# ---------------------------------------------------------------- figure 08
def fig_swa_replay():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

    ax1.bar([0, 1, 2], [LAYERS * WIN, DEC * WIN, WIN], color=[GRAY, TEAL, RED], width=0.55)
    ax1.set_xticks([0, 1, 2])
    ax1.set_xticklabels(["exact, all layers\n(L x win)", "exact, decoder only\n((L/2) x win)",
                         "bounded replay\n(win)"], fontsize=9)
    ax1.set_ylabel("tokens that must be re-run")
    ax1.set_title("Rebuilding the sliding-window state")
    for x, v in zip([0, 1, 2], [LAYERS * WIN, DEC * WIN, WIN]):
        ax1.text(x, v + 130, f"{v:,}", ha="center", fontsize=11, weight="bold")
    ax1.set_ylim(0, LAYERS * WIN * 1.22)
    ax1.annotate(f"{LAYERS * WIN // WIN}x less work,\nfor an approximate state",
                 xy=(2, WIN + 250), xytext=(1.1, 3400), fontsize=9.5, weight="bold",
                 color=DARK, arrowprops=dict(arrowstyle="->", color=DARK, lw=1.3))

    # order-of-magnitude comparison with clearly-stated assumptions
    SSD_LAT_US, SSD_BW, TFLOPS, HID, ACTIVE = 100.0, 7.0e9, 1000.0, 5120, 8e9
    swa_bytes = WIN * LAYERS * 2 * HID
    fetch = SSD_LAT_US + swa_bytes / SSD_BW * 1e6
    recompute = 2 * ACTIVE * WIN / (TFLOPS * 1e12) * 1e6
    ax2.barh([1, 0], [fetch / 1000, recompute / 1000], color=[GRAY, RED], height=0.45)
    ax2.set_yticks([0, 1])
    ax2.set_yticklabels(["recompute\n128 tokens on GPU", "fetch from SSD\nand back"], fontsize=9)
    ax2.set_xlabel("estimated time (milliseconds)")
    ax2.set_title("Why recomputing wins")
    for y, v in zip([0, 1], [recompute / 1000, fetch / 1000]):
        ax2.text(v + 0.2, y, f"{v:.1f} ms", va="center", fontsize=10, weight="bold")
    ax2.set_xlim(0, fetch / 1000 * 1.3)
    ax2.set_ylim(-0.5, 1.5)
    fig.tight_layout()
    fig.text(0.56, -0.10, "Right panel is a TOY MODEL with assumed hardware constants "
                          "(100 us SSD latency, 7 GB/s, 1000 TFLOP/s, 8B active params).\n"
                          "It shows the direction of the trade-off, not its exact size — and note "
                          "the answer is milliseconds, not the 'microseconds' the video claims.",
             ha="center", fontsize=8.5, color=GRAY)
    save(fig, OUT, "08_swa_bounded_replay.png")


# ---------------------------------------------------------------- figure 09
def fig_benchmarks():
    """Numbers as published in Table 3 of the technical report."""
    bench = ["DeepSWE v1.1", "Terminal-\nBench 2.1", "Automation-\nBench",
             "Agents' Last\nExam", "CyberGym", "GPQA\nDiamond", "Terminal-\nBench 4.0"]
    models = [
        ("DeepSeek-V4.1-Flash", RED, [74.2, 90.6, 54.8, 31.8, 88.1, 90.9, 31.2]),
        ("Claude Opus-5", PURPLE, [74.0, 89.1, 50.3, 28.6, np.nan, 93.4, 51.8]),
        ("GPT-5.6 Sol", TEAL, [73.0, 88.8, 45.8, 26.7, 84.5, 94.1, 39.9]),
        ("Kimi-K3", AMBER, [67.5, 88.3, 46.7, 27.6, 80.0, 92.9, 12.6]),
        ("DeepSeek-V4-Flash", GRAY, [54.4, 82.7, 37.7, 25.2, 76.7, 89.9, 7.0]),
    ]
    x = np.arange(len(bench))
    w = 0.16
    fig, ax = plt.subplots(figsize=(12, 4.6))
    for i, (name, c, vals) in enumerate(models):
        ax.bar(x + (i - 2) * w, vals, w, color=c, label=name)
    ax.set_xticks(x); ax.set_xticklabels(bench, fontsize=8.5)
    ax.set_ylabel("score (%)   ·   higher is better")
    ax.set_title("DeepSeek-V4.1-Flash against frontier models (as published, Table 3)")
    ax.legend(fontsize=8.5, ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.13))
    ax.set_ylim(0, 105)
    ax.axvspan(5.5, 6.5, color="#fef3c7", zorder=0)
    ax.text(6, 97, "the remaining gap", fontsize=8.5, ha="center", color=AMBER, weight="bold")
    ax.text(0, 97, "beats both closed frontier models", fontsize=8.5, color=RED, weight="bold")
    save(fig, OUT, "09_benchmarks.png")


# ---------------------------------------------------------------- figure 10
def fig_scaffolds():
    """Table 4: the same checkpoint run under eight different agent harnesses."""
    names = ["Claude Code", "Codex", "OpenCode", "Pi", "mini-SWE",
             "DSH\nMinimal", "DSH\nStandard", "DSH\nPTC"]
    swe = [69.8, 65.6, 65.5, 66.2, 74.2, 72.6, 70.5, 67.6]
    tb = [88.0, 84.1, 85.0, 86.1, 90.3, 90.6, 85.8, 85.8]
    x = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(11, 4.3))
    ax.bar(x - 0.2, swe, 0.4, color=RED, label="DeepSWE v1.1 (resolved %)")
    ax.bar(x + 0.2, tb, 0.4, color=BLUE, label="Terminal-Bench v2.1 (Pass@1 %)")
    for arr, col, off in ((swe, RED, -0.2), (tb, BLUE, 0.2)):
        ax.axhline(max(arr), color=col, ls=":", lw=1.1, alpha=0.6)
        ax.axhline(min(arr), color=col, ls=":", lw=1.1, alpha=0.6)
    ax.set_xticks(x); ax.set_xticklabels(names, fontsize=8.5)
    ax.set_ylim(55, 100)
    ax.set_ylabel("score (%)")
    ax.set_title("Same model, same tasks, eight harnesses — only the scaffold changes")
    ax.legend(fontsize=9, loc="upper right")
    ax.text(0.1, 57.2, f"DeepSWE spread: {min(swe):.1f} – {max(swe):.1f}  "
                       f"({max(swe) - min(swe):.1f} points)   ·   "
                       f"Terminal-Bench spread: {min(tb):.1f} – {max(tb):.1f}  "
                       f"({max(tb) - min(tb):.1f} points)",
            fontsize=9, color=DARK, weight="bold")
    save(fig, OUT, "10_agent_scaffolds.png")


# ---------------------------------------------------------------- figure 11
def fig_reasoning_effort():
    """Reported in Section 5.3.2: effort 25 -> 100, and the token cost."""
    effort = np.array([25, 100])
    fig, ax = plt.subplots(figsize=(8.4, 4.3))
    series = [("8 reasoning benchmarks (avg)", [67.1, 76.3], RED),
              ("DeepSWE v1.1", [66.0, 74.2], BLUE),
              ("Terminal-Bench 2.1", [82.4, 90.6], GREEN)]
    for name, vals, c in series:
        ax.plot(effort, vals, ":", color=c, lw=1.4)          # NOT a fitted curve
        ax.plot(effort, vals, "o", color=c, ms=9, label=name)
        ax.annotate(f"+{vals[1] - vals[0]:.1f}", xy=(100, vals[1]), xytext=(103, vals[1] - 0.6),
                    fontsize=9, color=c, weight="bold")
    ax.set_xlabel("reasoning effort setting")
    ax.set_ylabel("Pass@1 (%)")
    ax.set_xlim(15, 118); ax.set_ylim(62, 95)
    ax.set_title("Paying for accuracy with tokens (the two reported endpoints)")
    ax.legend(fontsize=9, loc="lower right")
    fig.text(0.5, -0.13,
             "Only the endpoints at effort 25 and 100 are quoted in the paper's text, so the dotted\n"
             "joins are NOT the real curve. Figure 9 of the paper shows it is concave: gains are\n"
             "front-loaded, and effort 60–80 recovers most of the accuracy for well under half the\n"
             "token budget. Going 25 -> 100 costs roughly 2.5x the output tokens.",
             ha="center", fontsize=8.5, color=GRAY)
    save(fig, OUT, "11_reasoning_effort.png")


# ---------------------------------------------------------------- figure 12
def fig_three_dimensions():
    fig, ax = canvas(10.5, 4.6, (0, 10.5), (0, 4.6))
    ax.set_title("The three multiplicative dimensions of KV compression "
                 "(the paper's own framing)", loc="left")
    dims = [
        (0.3, "1. ENTRY SIZE", "how many numbers per cached entry",
         "MHA -> GQA -> MLA's shared latent -> FP4 precision", BLUE),
        (0.3, "2. SEQUENCE", "how many entries per token",
         "compress every c tokens into one entry (CSA/CSA2, rate 2)", TEAL),
        (0.3, "3. LAYER", "how many layers keep a cache at all",
         "cross-layer reuse: 4 of 38 layers (CSA2 Full mode)", RED),
    ]
    y = 3.3
    for _, title, sub, how, col in dims:
        box(ax, 0.3, y, 2.5, 0.95, title, fc="white", ec=col, fs=10.5, tc=col, weight="bold")
        ax.text(3.0, y + 0.62, sub, fontsize=9.5, color=DARK, weight="bold", va="center")
        ax.text(3.0, y + 0.3, how, fontsize=8.8, color=GRAY, va="center")
        y -= 1.15
    ax.text(0.3, 0.55, "They multiply.  Halve each one and the cache is 8x smaller.",
            fontsize=11, weight="bold", color=DARK)
    ax.text(0.3, 0.2, "DeepSeek-V4.1-Flash is the first model to push on all three at once — "
                      "that is the paper's actual claim to novelty.",
            fontsize=9, color=GRAY)
    save(fig, OUT, "12_three_dimensions.png")


# ---------------------------------------------------------------- figure 13
def fig_ced_flow():
    fig, ax = canvas(11, 4.6, (0, 11), (0, 4.6))
    ax.set_title("Causal Encoder-Decoder: who does what, and when", loc="left")
    ax.add_patch(Rectangle((0.15, 2.75), 10.6, 1.5, fc="#f0f7ff", ec="none", zorder=0))
    ax.add_patch(Rectangle((0.15, 1.05), 10.6, 1.5, fc="#fff5f5", ec="none", zorder=0))
    box(ax, 0.3, 2.9, 3.0, 1.2, "CAUSAL ENCODER\nlayers 1–20", fc="#dbeafe", ec=BLUE,
        fs=10, weight="bold")
    box(ax, 0.3, 1.2, 3.0, 1.2, "DECODER\nlayers 21–40", fc="#fee2e2", ec=RED,
        fs=10, weight="bold")
    box(ax, 4.3, 2.9, 2.6, 1.2, "global KV cache\n890 B / token", fc="#fef3c7", ec=AMBER,
        fs=9.5, weight="bold")
    arrow(ax, 3.4, 3.5, 4.2, 3.5, color=BLUE, lw=2.0, text="builds it")
    arrow(ax, 5.6, 2.85, 5.6, 1.9, color=AMBER, lw=2.0, rad=0)
    arrow(ax, 5.5, 1.8, 3.45, 1.8, color=AMBER, lw=2.0, text="inherits it", fs=8.5)
    box(ax, 7.4, 2.9, 3.2, 1.2, "PREFILL\nreading the prompt\n8B params active",
        fc="white", ec=BLUE, fs=9)
    box(ax, 7.4, 1.2, 3.2, 1.2, "DECODE\nwriting the answer\n16B params active",
        fc="white", ec=RED, fs=9)
    ax.text(9.0, 4.33, "this row is what runs during…", fontsize=8.5, color=GRAY,
            ha="center", style="italic")
    ax.text(0.3, 0.75, "The decoder never reads the prompt. It is handed the encoder's finished "
                       "summary, and looks at the\nlast 128 tokens directly for local detail. "
                       "That is what halves the cost of reading.",
            fontsize=9.5, color=DARK, va="top")
    save(fig, OUT, "13_ced_flow.png")


if __name__ == "__main__":
    fig_generations()
    fig_memory_hierarchy()
    fig_layer_map()
    fig_csa2_modes()
    fig_layer_dimension()
    fig_hierarchical_indexer()
    fig_prefill_split()
    fig_swa_replay()
    fig_benchmarks()
    fig_scaffolds()
    fig_reasoning_effort()
    fig_three_dimensions()
    fig_ced_flow()
    print("all figures written to", OUT)
