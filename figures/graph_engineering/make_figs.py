"""Figures for 'Graph Engineering - Agent Workflows as DAGs'.
02 and 04 are computed (critical-path scheduling, Monte-Carlo latency). 05 and 06 are simple
explicit toy models (assumptions in the titles). 09 uses numbers published by Anthropic.
Run:  python figures/graph_engineering/make_figs.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _style import *

OUT = out_dir(__file__)
rng = np.random.default_rng(11)


def node(ax, x, y, text, fc="white", ec=DARK, w=1.7, h=0.7, fs=9, weight="normal"):
    box(ax, x - w / 2, y - h / 2, w, h, text, fc=fc, ec=ec, fs=fs, weight=weight)


# ------------------------------------------------------------------ 01 vocabulary
def fig_vocab():
    fig, ax = canvas(12, 4.2, (0, 12), (0, 4.2))
    ax.text(6, 3.95, "The whole vocabulary: JOBS (boxes) · ARROWS (= wait for) · STATE (the clipboard)", ha="center",
            fontsize=12, weight="bold")
    node(ax, 1.3, 2.3, "research\ncompetitor A", fc="#eff6ff", ec=BLUE)
    node(ax, 1.3, 1.0, "research\ncompetitor B", fc="#eff6ff", ec=BLUE)
    node(ax, 4.6, 1.65, "write\ncomparison", fc="#eff6ff", ec=BLUE)
    node(ax, 7.6, 1.65, "fact-check\n(separate agent)", fc="#fffbeb", ec=AMBER)
    arrow(ax, 2.15, 2.2, 3.75, 1.8, color=DARK, text="wait", fs=8)
    arrow(ax, 2.15, 1.1, 3.75, 1.5, color=DARK)
    arrow(ax, 5.45, 1.65, 6.75, 1.65, color=DARK, text="wait", fs=8)
    box(ax, 9.3, 0.5, 2.5, 2.6, "STATE (clipboard)\n\nfound: A = $49/mo\nfound: B = $29/mo\ndecided: target SMBs\nto-do: verify prices", fc="#f0fdf4",
        ec=GREEN, fs=8.5, ha="left")
    for x, y in [(1.3, 2.65), (1.3, 0.65), (4.6, 2.0), (7.6, 2.0)]:
        ax.plot([x, 9.3], [y, 1.8], color=GREEN, lw=0.8, ls=":")
    ax.text(0.2, 0.05, "Test for a job: fits on ONE sticky note.   Test for an arrow: something really flows through it.",
            fontsize=9, color=GRAY)
    save(fig, OUT, "01_vocabulary.png")


# ------------------------------------------------------------------ 02 fake arrows: gantt before/after
def fig_fake_arrows():
    jobs = [("summarize file", 4, []), ("check calendar", 2, []), ("draft reply", 5, ["summarize file"]),
            ("look up CRM record", 3, []), ("personalize", 3, ["draft reply", "look up CRM record"]),
            ("send (human gate)", 1, ["personalize", "check calendar"])]
    names = [j[0] for j in jobs]
    dur = {n: d for n, d, _ in jobs}
    # straight line: each waits for the previous
    start_seq, t = {}, 0
    for n in names:
        start_seq[n] = t; t += dur[n]
    total_seq = t
    # true dependencies (critical path)
    start_dag = {}
    for n, d, deps in jobs:
        start_dag[n] = max([start_dag[p] + dur[p] for p in deps], default=0)
    total_dag = max(start_dag[n] + dur[n] for n in names)
    fig, axes = plt.subplots(1, 2, figsize=(13, 3.8), sharey=True)
    for ax, starts, title, total in [(axes[0], start_seq, "Straight line: every job waits for the one before", total_seq),
                                     (axes[1], start_dag, "Graph: only REAL arrows kept → independent jobs overlap", total_dag)]:
        for i, n in enumerate(names):
            col = AMBER if n == "send (human gate)" else BLUE
            ax.barh(i, dur[n], left=starts[n], color=col, alpha=0.85, edgecolor=DARK)
            ax.text(starts[n] + dur[n] / 2, i, f"{dur[n]} min" if dur[n] > 1 else "1", ha="center", va="center", color="white", fontsize=8.5, weight="bold")
        ax.axvline(total, color=RED, ls="--"); ax.text(total + 0.2, len(names) - 0.6, f"done at {total} min", color=RED, fontsize=9)
        ax.set_title(title); ax.set_xlabel("minutes"); ax.set_xlim(0, 21)
    axes[0].set_yticks(range(len(names))); axes[0].set_yticklabels(names); axes[0].invert_yaxis()
    fig.suptitle(f"Cutting fake arrows (calendar ≠ needs summary; CRM lookup ≠ needs draft):  {total_seq} min → {total_dag} min, same jobs",
                 weight="bold", y=1.03)
    save(fig, OUT, "02_fake_arrows_gantt.png")
    print("sequential", total_seq, "dag", total_dag)


# ------------------------------------------------------------------ 03 diamond
def fig_diamond():
    fig, ax = canvas(12, 6.2, (0, 12), (0, 6.2))
    ax.text(6, 5.95, "The diamond: SPLIT → WORK (in parallel) → CHECK → MERGE → human gate", ha="center", fontsize=12, weight="bold")
    node(ax, 6, 5.1, "LEAD / SPLIT\nbreak the task into lanes", fc="#eff6ff", ec=BLUE, w=3.0, h=0.8, weight="bold")
    xs = [1.6, 3.8, 6.0, 8.2, 10.4]
    for i, x in enumerate(xs):
        node(ax, x, 3.5, f"WORKER {i+1}\nown context,\none lane only", fc="white", ec=BLUE, w=1.9, h=0.9, fs=8.5)
        arrow(ax, 6, 4.7, x, 3.95, color=BLUE)
        arrow(ax, x, 3.05, 6, 2.35, color=BLUE)
    node(ax, 6, 2.0, "CHECK — a DIFFERENT agent\nattacks claims, sources, consistency", fc="#fffbeb", ec=AMBER, w=4.0, h=0.7, weight="bold")
    node(ax, 6, 1.0, "MERGE → one answer", fc="#f0fdf4", ec=GREEN, w=3.0, h=0.55, weight="bold")
    arrow(ax, 6, 1.65, 6, 1.28, color=AMBER)
    node(ax, 6, 0.3, "HUMAN GATE (only before irreversible actions)", fc="#fef2f2", ec=RED, w=4.6, h=0.45, fs=8.5)
    arrow(ax, 6, 0.72, 6, 0.53, color=GREEN)
    ax.text(0.2, 5.1, "narrow", fontsize=9, color=GRAY); ax.text(0.2, 3.5, "wide", fontsize=9, color=GRAY)
    ax.text(0.2, 1.5, "narrow", fontsize=9, color=GRAY)
    save(fig, OUT, "03_diamond.png")


# ------------------------------------------------------------------ 04 parallel latency (Monte Carlo)
def fig_parallel_latency():
    Ns = np.arange(1, 11)
    runs = 20000
    lead, check, merge = 20, 40, 15            # seconds
    seq_med, par_med, par_p95 = [], [], []
    for n in Ns:
        w = rng.lognormal(np.log(60), 0.5, size=(runs, n))       # each worker ~1 min, long tail
        seq = lead + w.sum(1) + check + merge
        par = lead + w.max(1) + check + merge
        seq_med.append(np.median(seq)); par_med.append(np.median(par)); par_p95.append(np.percentile(par, 95))
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.9))
    ax = axes[0]
    ax.plot(Ns, np.array(seq_med) / 60, "o-", color=RED, lw=2, label="one agent does all lanes in sequence")
    ax.plot(Ns, np.array(par_med) / 60, "o-", color=GREEN, lw=2, label="diamond: lanes in parallel (median)")
    ax.plot(Ns, np.array(par_p95) / 60, "o--", color=GREEN, lw=1.5, alpha=0.6, label="diamond: slow runs (95th percentile)")
    ax.set_xlabel("number of research lanes"); ax.set_ylabel("wall-clock minutes")
    ax.set_title("Monte-Carlo: parallel time ≈ the SLOWEST worker,\nnot the sum (each lane ~1 min, long-tailed)")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    ax = axes[1]
    speed = np.array(seq_med) / np.array(par_med)
    ax.plot(Ns, speed, "o-", color=PURPLE, lw=2, label="measured speed-up (Monte-Carlo)")
    ax.plot(Ns, Ns, ":", color=GRAY, label="ideal (N×)")
    ax.set_xlabel("number of research lanes"); ax.set_ylabel("speed-up ×")
    ax.set_title("Diminishing returns: the fixed lead/check/merge time\nand the slowest lane cap the gain (Amdahl's law)")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    save(fig, OUT, "04_parallel_latency.png")


# ------------------------------------------------------------------ 05 self-check vs independent check (toy model)
def fig_checker():
    claims, trials = 20, 4000
    p_err = 0.15
    fig, ax = plt.subplots(figsize=(8.5, 4))
    configs = [("no check", 0.0, RED), ("same agent re-reads its own answer\n(shares its blind spots: catches 10%)", 0.10, AMBER),
               ("separate skeptic agent\n(catches 55%)", 0.55, BLUE), ("separate skeptic + external evidence\n(search, tests, sources: catches 85%)", 0.85, GREEN)]
    for i, (lab, catch, col) in enumerate(configs):
        errs = rng.random((trials, claims)) < p_err
        caught = errs & (rng.random((trials, claims)) < catch)
        residual = (errs & ~caught).sum(1)
        pct_clean = np.mean(residual == 0) * 100
        ax.barh(i, pct_clean, color=col)
        ax.text(pct_clean + 1, i, f"{pct_clean:.0f}% of reports have zero errors  (avg {residual.mean():.1f} wrong claims)",
                va="center", fontsize=8.5)
    ax.set_yticks(range(len(configs))); ax.set_yticklabels([c[0] for c in configs], fontsize=8.5)
    ax.set_xlim(0, 105); ax.invert_yaxis(); ax.set_xlabel("% of 20-claim reports with no wrong claim left")
    ax.set_title("Toy model: 20 claims, each wrong with 15% probability.\nThe checker's catch rate decides whether the output is trustworthy")
    save(fig, OUT, "05_checker_toy_model.png")


# ------------------------------------------------------------------ 06 stop rules (toy model)
def fig_stop_rules():
    iters = np.arange(0, 61)
    quality = 1 - 0.55 * np.exp(-iters / 4) + np.cumsum(rng.normal(0, 0.004, len(iters)))
    quality = np.clip(quality, 0, 0.99)
    cost = iters * 0.10
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(iters, quality * 100, color=BLUE, lw=2.5, label="answer quality (%)")
    ax2 = ax.twinx(); ax2.plot(iters, cost, color=RED, lw=2.5, label="money spent ($)")
    ax2.set_ylabel("$ spent", color=RED); ax.set_ylabel("quality %", color=BLUE)
    bar_it = int(np.argmax(quality >= 0.93))
    for x, lab, col in [(5, "CAP: 5 tries", PURPLE), (bar_it, f"BAR: quality ≥ 93%\n(iteration {bar_it})", GREEN),
                        (20, "BUDGET: $2 spent", AMBER)]:
        ax.axvline(x, color=col, ls="--", lw=1.6); ax.text(x + 0.4, {5: 58, 20: 72}.get(x, 46), lab, color=col, fontsize=8.5)
    ax.annotate("no stop rule: quality flat,\nbill keeps climbing all night", (58, 99), (33, 55), fontsize=9, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED))
    ax.set_xlabel("loop iteration"); ax.set_ylim(40, 105)
    ax.set_title("Toy model of an improve-the-answer loop: quality saturates, cost is linear")
    ax.spines["right"].set_visible(True)
    save(fig, OUT, "06_stop_rules.png")


# ------------------------------------------------------------------ 07 human gate placement
def fig_gate():
    fig, ax = canvas(13, 3.4, (0, 13), (0, 3.4))
    ax.text(6.5, 3.15, "Put the gate where the regret lives: before IRREVERSIBLE actions only", ha="center", fontsize=12, weight="bold")
    steps = [("find leads", True), ("research each", True), ("draft emails", True), ("edit / check", True),
             ("HUMAN GATE", None), ("send 500 emails", False), ("log in CRM", True)]
    for i, (s, rev) in enumerate(steps):
        x = 0.95 + i * 1.85
        if rev is None:
            node(ax, x, 1.7, "HUMAN GATE\npause · review\n· resume", fc="#fef2f2", ec=RED, w=1.65, h=1.0, fs=8.5, weight="bold")
        else:
            node(ax, x, 1.7, s, fc="#f0fdf4" if rev else "#fee2e2", ec=GREEN if rev else RED, w=1.55, h=0.7, fs=9)
            ax.text(x, 1.05, "reversible\n→ run freely" if rev else "IRREVERSIBLE", ha="center", fontsize=7.5,
                    color=GREEN if rev else RED, va="top")
        if i:
            arrow(ax, x - 1.85 + 0.8, 1.7, x - 0.8, 1.7, color=GRAY)
    ax.text(6.5, 0.2, "✗ gating every step = manual work again      ✗ no gate before 'send' = a broken draft reaches real clients",
            ha="center", fontsize=9, color=GRAY)
    save(fig, OUT, "07_human_gate.png")


# ------------------------------------------------------------------ 08 three builds
def fig_builds():
    fig, axes = plt.subplots(1, 3, figsize=(15, 5.2))
    builds = [("Deep research desk", "question:\n'launch in Germany?'", ["market\nsize", "competitors", "rules &\ntaxes", "pricing", "risks"],
               "SKEPTIC\nweak/stale sources", "brief, source\nnext to each claim"),
              ("SEO content machine", "keyword +\nsearch intent", ["intro", "section 1", "section 2", "section 3", "conclusion"],
               "EDITOR\nfacts, filler, one voice", "publish-ready\narticle"),
              ("Go-to-market kit", "one paragraph\nabout the product", ["positioning", "launch\nemails", "landing\npage", "ad angles", "social\nposts"],
               "REVIEWER\nsame story everywhere?", "folder of\nconsistent copy")]
    for ax, (title, inp, lanes, check, out) in zip(axes, builds):
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off"); ax.set_title(title, weight="bold")
        node(ax, 5, 9, inp, fc="#eff6ff", ec=BLUE, w=4, h=1.2, fs=9)
        for i, l in enumerate(lanes):
            x = 1 + i * 2
            node(ax, x, 6.4, l, fc="white", ec=BLUE, w=1.85, h=1.2, fs=8)
            arrow(ax, 5, 8.4, x, 7.0, color=BLUE, lw=1)
            arrow(ax, x, 5.8, 5, 4.6, color=BLUE, lw=1)
        node(ax, 5, 4.0, check, fc="#fffbeb", ec=AMBER, w=4.4, h=1.1, fs=8.5)
        node(ax, 5, 2.3, out, fc="#f0fdf4", ec=GREEN, w=3.6, h=1.1, fs=8.5)
        node(ax, 5, 0.7, "human gate", fc="#fef2f2", ec=RED, w=2.6, h=0.7, fs=8.5)
        arrow(ax, 5, 3.45, 5, 2.85, color=AMBER); arrow(ax, 5, 1.75, 5, 1.05, color=GREEN)
    save(fig, OUT, "08_three_builds.png")


# ------------------------------------------------------------------ 09 token cost (published numbers)
def fig_tokens():
    fig, ax = plt.subplots(figsize=(8, 3.4))
    labels = ["chat interaction", "single agent", "multi-agent system"]
    vals = [1, 4, 15]
    bars = ax.barh(labels, vals, color=[GRAY, BLUE, PURPLE])
    for b, v in zip(bars, vals):
        ax.text(v + 0.2, b.get_y() + b.get_height() / 2, f"≈ {v}× tokens", va="center", fontsize=10)
    ax.invert_yaxis(); ax.set_xlim(0, 18); ax.set_xlabel("relative token usage")
    ax.set_title("The price of the diamond (Anthropic, 'How we built our multi-agent research system', 2025)\n"
                 "multi-agent research beat single-agent by 90.2% on their internal eval, but used ~15× the tokens of chat",
                 fontsize=9.5)
    save(fig, OUT, "09_token_cost.png")


if __name__ == "__main__":
    fig_vocab(); fig_fake_arrows(); fig_diamond(); fig_parallel_latency(); fig_checker(); fig_stop_rules()
    fig_gate(); fig_builds(); fig_tokens()
