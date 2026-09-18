"""Figures for 'Agent Harnesses - Why the Scaffold Beats the Model'.
Source talk: 'Why The Harness Matters More Than The Model' (YC Paper Club).
04 and 08 are toy simulations (assumptions stated on the plots); the rest are diagrams / timelines.
Numbers attributed to the talk are plotted as reported, not independently verified.
Run:  python figures/agent_harness/make_figs.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _style import *

OUT = out_dir(__file__)
rng = np.random.default_rng(3)


def node(ax, x, y, text, fc="white", ec=DARK, w=1.8, h=0.8, fs=9, weight="normal"):
    box(ax, x - w / 2, y - h / 2, w, h, text, fc=fc, ec=ec, fs=fs, weight=weight)


# ------------------------------------------------------------------ 01 what a harness is
def fig_harness_anatomy():
    fig, ax = canvas(12, 6.4, (0, 12), (0, 6.4))
    ax.text(6, 6.15, "A harness = everything between the raw model and the world", ha="center", fontsize=12.5, weight="bold")
    ax.add_patch(Circle((6, 3.1), 2.75, fc="#f8fafc", ec=GRAY, lw=1.2, ls="--"))
    ax.add_patch(Circle((6, 3.1), 1.0, fc="#eff6ff", ec=BLUE, lw=2))
    ax.text(6, 3.1, "LLM\nfixed weights\ntokens in → token out", ha="center", va="center", fontsize=8.5, weight="bold")
    parts = [(90, "context compilation\n(what goes in the prompt)"), (30, "tools\n(APIs, code execution)"),
             (-30, "memory & state\n(files, DB, REPL vars)"), (-90, "skills\n(saved procedures)"),
             (-150, "sub-agents\n(delegation, recursion)"), (150, "loop + limits\n(turns, budget, compaction)")]
    for ang, lab in parts:
        r = np.deg2rad(ang)
        x, y = 6 + 1.9 * np.cos(r), 3.1 + 1.9 * np.sin(r)
        node(ax, x, y, lab, fc="white", ec=PURPLE, w=2.1, h=0.75, fs=8)
    for x, y, lab in [(0.9, 5.4, "user / Slack"), (11.1, 5.4, "cron schedule"), (0.9, 0.8, "sandbox / computer"),
                      (11.1, 0.8, "company data & APIs")]:
        node(ax, x, y, lab, fc="#f0fdf4", ec=GREEN, w=1.7, h=0.6, fs=8.5)
    ax.text(6, 0.05, "Same weights + different harness → very different capability", ha="center", fontsize=9.5, color=GRAY)
    save(fig, OUT, "01_harness_anatomy.png")


# ------------------------------------------------------------------ 02 timeline
def fig_timeline():
    # (year, label, lane, label_x, label_dy)
    events = [(2019.1, "GPT-2: 'zero harness'\n(loop until EOS)", 0, 2019.3, -0.3), (2020.5, "GPT-3 few-shot\n(in-context learning)", 0, 2020.6, 0.3),
              (2022.05, "chain of thought", 0, 2022.1, -0.3),
              (2021.95, "WebGPT (browsing)", 1, 2021.5, 0.3), (2023.1, "Toolformer (tools)", 1, 2022.6, -0.32),
              (2023.4, "Voyager (skills)", 1, 2023.1, 0.34), (2023.45, "InterCode\n(code as action)", 1, 2024.35, 0.34),
              (2023.8, "MemGPT\n(CRUD on context)", 1, 2024.5, -0.32),
              (2022.8, "ReAct (reason + act)", 2, 2022.2, 0.32), (2023.2, "Self-Refine, Reflexion\n(critique & retry)", 2, 2023.6, -0.34),
              (2025.1, "sub-agents,\nRecursive LMs", 2, 2025.3, 0.34),
              (2023.8, "DSPy (learned prompts)", 3, 2023.5, 0.3), (2025.4, "Darwin Gödel Machine\n(evolves agent code)", 3, 2024.9, -0.36),
              (2025.55, "GEPA (reflective\nprompt evolution)", 3, 2025.4, 0.36), (2026.2, "continual /\nself-improving\nharnesses", 3, 2026.3, -0.42)]
    lanes = ["context &\noutput space", "tools &\nexternal state", "reflection &\nmulti-agent", "LEARNED harness\n(v2)"]
    cols = [BLUE, GREEN, AMBER, PURPLE]
    fig, ax = plt.subplots(figsize=(13.5, 6))
    for x, lab, lane, lx, dy in events:
        ax.scatter([x], [lane], color=cols[lane], s=60, zorder=3)
        ax.annotate(lab, (x, lane), (lx, lane + dy), fontsize=7.8, ha="center", va="center", color=DARK,
                    bbox=dict(fc="white", ec=cols[lane], boxstyle="round,pad=0.25", lw=0.8),
                    arrowprops=dict(arrowstyle="-", color=cols[lane], lw=0.7))
    ax.set_yticks(range(4)); ax.set_yticklabels(lanes)
    ax.set_ylim(-0.7, 3.7); ax.set_xlim(2018.6, 2026.9)
    ax.axvspan(2024.9, 2026.9, color=PURPLE, alpha=0.05); ax.text(2025.9, 3.6, "self-improving era", ha="center", fontsize=9, color=PURPLE)
    ax.set_title("A coarse history of harness ideas (years approximate): static harness 'v1' → learned harness 'v2'")
    ax.grid(axis="x", alpha=0.3)
    save(fig, OUT, "02_harness_timeline.png")


# ------------------------------------------------------------------ 03 harness v1 loop
def fig_loop():
    fig, ax = canvas(12.5, 5.0, (0, 12.5), (0, 5.0))
    ax.text(6.25, 4.75, "'Harness v1': a static loop designed by a human", ha="center", fontsize=12, weight="bold")
    node(ax, 1.2, 3.6, "trigger:\nuser in Slack", fc="#f0fdf4", ec=GREEN, w=1.9, h=0.8, fs=8.5)
    node(ax, 1.2, 2.3, "trigger:\ncron (hourly)", fc="#f0fdf4", ec=GREEN, w=1.9, h=0.8, fs=8.5)
    node(ax, 1.2, 0.9, "agent spec:\nprompt · tools · skills\n· sub-agents · limits", fc="#f9fafb", ec=GRAY, w=2.1, h=1.0, fs=8)
    steps = [(3.9, 3.0, "session\nmanagement"), (6.2, 3.0, "context\ncompilation"), (8.5, 3.0, "LLM call\n→ action"),
             (8.5, 1.2, "run tool /\nsub-agent"), (6.2, 1.2, "append result\nto context")]
    for x, y, t in steps:
        node(ax, x, y, t, fc="#eff6ff", ec=BLUE, w=1.8, h=0.9, fs=9)
    arrow(ax, 2.15, 3.5, 3.0, 3.1); arrow(ax, 2.15, 2.4, 3.0, 2.9)
    arrow(ax, 4.8, 3.0, 5.3, 3.0); arrow(ax, 7.1, 3.0, 7.6, 3.0); arrow(ax, 8.5, 2.55, 8.5, 1.65, text="tool call", fs=8, toff=(0.45, -0.05))
    arrow(ax, 7.6, 1.2, 7.1, 1.2); arrow(ax, 6.2, 1.65, 6.2, 2.55, text="loop", fs=8, toff=(-0.35, -0.05))
    node(ax, 11.2, 3.0, "final answer\n(or limit hit)", fc="#fef2f2", ec=RED, w=1.9, h=0.9, fs=9)
    arrow(ax, 9.4, 3.0, 10.25, 3.0, text="done", fs=8)
    arrow(ax, 2.25, 0.9, 5.3, 2.7, color=GRAY, ls="--", lw=1)
    save(fig, OUT, "03_harness_v1_loop.png")


# ------------------------------------------------------------------ 04 same weights, different harness (toy simulation)
def fig_same_weights():
    """Toy model: a 'model' that makes per-step arithmetic slips. Harness features change how errors play out."""
    steps = np.arange(1, 21)                          # number of reasoning steps a problem needs
    trials = 20000
    p_direct = 0.10                                   # per-step slip when doing everything 'in one token'
    p_cot = 0.03                                      # per-step slip when writing steps out
    res = {}
    for name in ["direct answer (zero harness)", "chain of thought", "CoT + calculator tool",
                 "CoT + tool + verifier & retry (≤3)"]:
        acc = []
        for n in steps:
            if name.startswith("direct"):
                ok = rng.random((trials, n)) > p_direct * (1 + n / 5)
                acc.append(ok.all(1).mean())
            elif name == "chain of thought":
                acc.append((rng.random((trials, n)) > p_cot).all(1).mean())
            elif name == "CoT + calculator tool":
                acc.append((rng.random((trials, n)) > p_cot * 0.25).all(1).mean())   # tool removes arithmetic slips; planning slips remain
            else:
                success = np.zeros(trials, bool)
                active = np.ones(trials, bool)                                       # still trying
                for attempt in range(3):
                    ok = (rng.random((trials, n)) > p_cot * 0.25).all(1)
                    success |= active & ok
                    caught = ~ok & (rng.random(trials) < 0.8)                        # verifier catches 80% of wrong answers
                    active = active & caught                                         # uncaught wrong answers get submitted
                acc.append(success.mean())
        res[name] = acc
    fig, ax = plt.subplots(figsize=(8.5, 4.2))
    for (name, acc), c in zip(res.items(), [RED, AMBER, BLUE, GREEN]):
        ax.plot(steps, np.array(acc) * 100, "o-", ms=3, lw=2.2, color=c, label=name)
    ax.set_xlabel("reasoning steps the problem needs"); ax.set_ylabel("accuracy (%)")
    ax.set_title("Toy simulation: identical 'model' (same slip rates), four harnesses\n"
                 "(assumed: 10% slips when answering directly, 3% per written step, tool fixes 75% of slips)")
    ax.legend(fontsize=8.5); ax.grid(alpha=0.3); ax.set_ylim(0, 102)
    save(fig, OUT, "04_same_weights_different_harness.png")


# ------------------------------------------------------------------ 05 reported ARC-AGI numbers
def fig_arc_reported():
    fig, ax = plt.subplots(figsize=(8, 3.4))
    labels = ["Claude Opus, evaluated directly\n(as reported in the talk)", "Claude Opus inside the\nPrime Agent harness (reported)"]
    vals = [30, 95.5]
    bars = ax.barh(labels, vals, color=[GRAY, PURPLE])
    for b, v in zip(bars, vals):
        ax.text(v + 1, b.get_y() + b.get_height() / 2, f"≈{v:g}%", va="center", fontsize=10, weight="bold")
    ax.set_xlim(0, 110); ax.invert_yaxis(); ax.set_xlabel("ARC-AGI score (%)")
    ax.set_title("The talk's headline claim: same model family, harness changes ~30% → ~95%\n"
                 "(numbers as stated by the speakers; check the ARC Prize leaderboard for verified results)", fontsize=9.5)
    save(fig, OUT, "05_arc_agi_reported.png")


# ------------------------------------------------------------------ 06 adaptation ladder
def fig_ladder():
    fig, ax = plt.subplots(figsize=(10, 4.4))
    items = [("in-context examples\n(saturates ~40–50 ex.)", 1, 1, BLUE), ("retrieval / memory", 1.6, 2.2, GREEN),
             ("skills / tools / REPL\n(harness)", 2.1, 3.1, GREEN), ("prompt optimization\n(DSPy, GEPA)", 3.0, 3.6, PURPLE),
             ("LoRA (low rank)", 4.2, 4.5, AMBER), ("LoRA (high rank)", 5.0, 5.0, AMBER), ("full fine-tuning (SFT / RL)", 6.2, 5.8, RED)]
    for lab, x, y, c in items:
        ax.scatter([x], [y], s=380, color=c, alpha=0.85, zorder=3)
        ax.annotate(lab, (x, y), (x + 0.18, y - 0.1), fontsize=8.5, va="top")
    ax.annotate("", (2.9, 3.4), (1.1, 1.2), arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.5, ls="--"))
    ax.text(1.0, 4.5, "the 'fast adaptation' gap the talk\nsays harnesses fill: adapt procedurally,\nwithout gradient updates", fontsize=9,
            color=PURPLE, bbox=dict(fc="#f5f3ff", ec=PURPLE, boxstyle="round,pad=0.4"))
    ax.set_xlim(0.5, 8.2); ax.set_ylim(0, 6.8)
    ax.set_xlabel("cost & time to adapt  →"); ax.set_ylabel("how deep / durable the change  →")
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("Ways to make a deployed model better at a new task (conceptual map, not measured)")
    save(fig, OUT, "06_adaptation_ladder.png")


# ------------------------------------------------------------------ 07 memory hierarchy
def fig_memory_hierarchy():
    fig, ax = canvas(12.5, 5.2, (0, 12.5), (0, 5.2))
    ax.text(6.25, 4.95, "Seth's cache-hierarchy view of where an agent's information lives", ha="center", fontsize=12, weight="bold")
    layers = [("weights", "baked-in knowledge", "fine-tuning (expensive)", "instant to use, slow to change", "#dbeafe", 4.0, 3.0),
              ("L1: active context", "prompt + recent turns", "COMPACTION (summarize)", "limited tokens, fully visible", "#e0e7ff", 3.2, 4.4),
              ("L2: live REPL / sub-agents", "variables in RAM, idle sub-agents", "agentic GARBAGE COLLECTION", "large; costs no context tokens until read", "#ede9fe", 2.4, 6.0),
              ("L3: filesystem / DB", "skills, memories, prompts, results", "REFINEMENT (update/delete)", "huge, persistent, must be searched", "#f5f3ff", 1.6, 7.6)]
    for i, (name, what, update, prop, fc, y, w) in enumerate(layers):
        ax.add_patch(FancyBboxPatch((6.25 - w / 2 - 1.2, y - 0.35), w, 0.7, boxstyle="round,pad=0.02", fc=fc, ec=PURPLE, lw=1.2))
        ax.text(6.25 - 1.2, y + 0.08, name, ha="center", va="center", fontsize=9.5, weight="bold")
        ax.text(6.25 - 1.2, y - 0.18, what, ha="center", va="center", fontsize=8)
        ax.text(10.0, y + 0.08, update, ha="left", va="center", fontsize=8.5, color=GREEN, weight="bold")
        ax.text(10.0, y - 0.18, prop, ha="left", va="center", fontsize=8, color=GRAY)
    ax.text(10.0, 4.55, "update mechanism / property", fontsize=9, weight="bold")
    ax.annotate("", (0.5, 1.3), (0.5, 4.3), arrowprops=dict(arrowstyle="->", color=DARK))
    ax.text(0.3, 2.8, "bigger,\ncheaper,\nfurther\nfrom the\nmodel", fontsize=8, ha="center", va="center", rotation=0)
    ax.text(6.25, 0.55, "Like CPU cache → RAM → disk: every layer needs a way to WRITE new state and to PRUNE old state (CRUD).",
            ha="center", fontsize=9, color=GRAY)
    save(fig, OUT, "07_memory_hierarchy.png")


# ------------------------------------------------------------------ 08 context pressure (toy simulation)
def fig_context_pressure():
    steps = 120
    limit = 200_000
    outputs = rng.lognormal(np.log(2500), 1.0, steps)          # tokens returned by each tool call
    def simulate(mode):
        ctx, series, failed_at = 8000, [], None
        for i, o in enumerate(outputs):
            if mode == "subagents" and o > 3000:
                o = 400                                          # a sub-agent reads the big output, returns a summary
            ctx += o + 150
            if mode in ("compaction", "subagents") and ctx > 0.8 * limit:
                ctx = 8000 + 0.1 * ctx                           # summarize history to ~10%
            if ctx > limit and failed_at is None:
                failed_at = i
            series.append(min(ctx, limit * 1.05))
        return np.array(series), failed_at
    fig, ax = plt.subplots(figsize=(9, 4))
    for mode, col, lab in [("none", RED, "append everything"), ("compaction", AMBER, "+ compaction at 80%"),
                           ("subagents", GREEN, "+ sub-agents for bulky tool output")]:
        s, f = simulate(mode)
        ax.plot(s / 1000, color=col, lw=2.2, label=lab + (f"  (overflows at step {f})" if f is not None else ""))
    ax.axhline(limit / 1000, color=DARK, ls="--"); ax.text(1, limit / 1000 + 4, "context window (200K tokens)", fontsize=8.5)
    ax.set_xlabel("agent step (tool calls)"); ax.set_ylabel("tokens in context (thousands)")
    ax.set_title("Toy simulation: a long-horizon agent's context budget\n(tool outputs ~2.5K tokens median, heavy-tailed)")
    ax.legend(fontsize=8.5, loc="upper left", bbox_to_anchor=(0, 0.93)); ax.set_ylim(0, 225)
    save(fig, OUT, "08_context_pressure.png")


# ------------------------------------------------------------------ 09 learned harness (v2)
def fig_learned_harness():
    fig, axes = plt.subplots(1, 2, figsize=(13, 4.8))
    for ax in axes:
        ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax = axes[0]; ax.set_title("Prompt optimization (DSPy / GEPA style)", weight="bold")
    node(ax, 5, 9, "small training set + metric", fc="#f9fafb", ec=GRAY, w=5, h=1.0)
    node(ax, 2.3, 6.4, "candidate\nprompts", fc="#eff6ff", ec=BLUE, w=2.8, h=1.3)
    node(ax, 7.7, 6.4, "run on examples\n→ score", fc="#fffbeb", ec=AMBER, w=2.8, h=1.3)
    node(ax, 7.7, 3.0, "reflect on failures,\nmutate / merge best", fc="#f5f3ff", ec=PURPLE, w=3.0, h=1.3)
    node(ax, 2.3, 3.0, "keep a Pareto set\nof strong prompts", fc="#f0fdf4", ec=GREEN, w=2.8, h=1.3)
    arrow(ax, 3.7, 6.4, 6.3, 6.4); arrow(ax, 7.7, 5.75, 7.7, 3.65); arrow(ax, 6.2, 3.0, 3.7, 3.0); arrow(ax, 2.3, 3.65, 2.3, 5.75)
    arrow(ax, 5, 8.5, 5, 7.2, color=GRAY)
    ax.text(5, 1.0, "searches PROMPTS; the program/harness code stays fixed", ha="center", fontsize=9, color=GRAY)
    ax = axes[1]; ax.set_title("Evolving the harness itself (Darwin Gödel Machine style)", weight="bold")
    node(ax, 5, 8.6, "ARCHIVE of agents\n(harness code + prompts), diverse", fc="#f0fdf4", ec=GREEN, w=5.6, h=1.3)
    node(ax, 2.3, 5.2, "sample a parent", fc="#eff6ff", ec=BLUE, w=2.8, h=1.0)
    node(ax, 7.7, 5.2, "agent REWRITES its\nown harness code", fc="#f5f3ff", ec=PURPLE, w=3.0, h=1.2)
    node(ax, 7.7, 2.2, "evaluate child on\nbenchmark (sandboxed!)", fc="#fffbeb", ec=AMBER, w=3.2, h=1.2)
    node(ax, 2.3, 2.2, "add to archive\nif valid", fc="#f0fdf4", ec=GREEN, w=2.8, h=1.0)
    arrow(ax, 3.5, 8.0, 2.3, 5.7); arrow(ax, 3.7, 5.2, 6.2, 5.2); arrow(ax, 7.7, 4.6, 7.7, 2.8); arrow(ax, 6.1, 2.2, 3.7, 2.2)
    arrow(ax, 2.3, 2.7, 4.2, 7.95)
    ax.text(5, 0.5, "searches CODE; needs strong sandboxing — agents find exploits (see the 99.9% 'cheating' run)",
            ha="center", fontsize=8.5, color=RED)
    save(fig, OUT, "09_learned_harness.png")


# ------------------------------------------------------------------ 10 Open Jarvis
def fig_open_jarvis():
    fig, ax = canvas(12.5, 5.0, (0, 12.5), (0, 5.0))
    ax.text(6.25, 4.75, "Open Jarvis: five primitives, tuned by a cloud model, run locally", ha="center", fontsize=12, weight="bold")
    prims = [("① user interfaces", "desktop app, chat, cron agents"), ("② agentic logic", "how tools & models are orchestrated"),
             ("③ intelligence", "local LLM: Qwen, GPT-OSS, Gemma"), ("④ inference engine + hardware", "Ollama, llama.cpp, vLLM, SGLang · Apple Silicon / NVIDIA"),
             ("⑤ tools, memory, learning", "MCP tools · prompt opt (DSPy/GEPA) · weights (LoRA/SFT/GRPO)")]
    for i, (a, b) in enumerate(prims):
        y = 3.9 - i * 0.8
        box(ax, 0.3, y - 0.32, 6.4, 0.64, "", fc="#eff6ff", ec=BLUE)
        ax.text(0.5, y + 0.08, a, fontsize=9.5, weight="bold", va="center")
        ax.text(0.5, y - 0.17, b, fontsize=8, va="center", color=GRAY)
    ax.text(3.5, 4.35, "the on-device stack (a structured spec)", ha="center", fontsize=9, color=BLUE, weight="bold")
    node(ax, 10.0, 3.3, "CLOUD model\n(occasionally)\ndiagnose + propose\nnew configuration", fc="#fef3c7", ec=AMBER, w=3.2, h=1.6, fs=9)
    node(ax, 10.0, 0.9, "every day queries run\nLOCALLY: cheap, private,\nlow energy", fc="#f0fdf4", ec=GREEN, w=3.2, h=1.1, fs=9)
    arrow(ax, 8.4, 3.6, 6.8, 3.6, color=AMBER, text="proposed config", fs=8)
    arrow(ax, 6.8, 2.6, 8.4, 3.0, color=BLUE, text="eval results", fs=8, toff=(0, -0.35))
    ax.text(6.25, 0.1, "Reported: ~800× lower cost than cloud stacks on their test suite, with gaps remaining on some tasks.",
            ha="center", fontsize=9, color=GRAY)
    save(fig, OUT, "10_open_jarvis.png")


# ------------------------------------------------------------------ 11 QM evolution
def fig_qm():
    fig, axes = plt.subplots(2, 1, figsize=(13, 6.6), gridspec_kw=dict(height_ratios=[1, 1.35]))
    ax = axes[0]; ax.set_xlim(0, 13); ax.set_ylim(0, 2.6); ax.axis("off")
    ax.set_title("YC's internal agents: each step gave the model more capability ('unhobbling')", weight="bold")
    steps = [("Jan 2025", "General agent", "prompt + tools in a loop;\none shared instance"),
             ("Jun 2025", "VM coding agents", "Claude Code / Codex in VMs,\ntriggered from Slack"),
             ("Jan 2026", "OpenClaw", "agent with ITS OWN\ncomputer"),
             ("Apr 2026", "Hermes fleet", "50+ per-user VMs;\n'whack-a-mole' ops"),
             ("May 2026", "QM", "brain in Postgres;\nsandboxes as resources")]
    for i, (d, n, t) in enumerate(steps):
        x = 1.3 + i * 2.6
        node(ax, x, 1.5, f"{n}\n{d}", fc="#eff6ff" if i < 4 else "#f5f3ff", ec=BLUE if i < 4 else PURPLE, w=2.2, h=0.8, fs=9, weight="bold")
        ax.text(x, 0.85, t, ha="center", va="top", fontsize=8)
        if i:
            arrow(ax, x - 2.6 + 1.1, 1.5, x - 1.1, 1.5, color=GRAY)
    ax = axes[1]; ax.set_xlim(0, 13); ax.set_ylim(0, 4.6); ax.axis("off")
    ax.set_title("QM architecture: keep the harness thin, push decisions into the agent", weight="bold")
    node(ax, 1.4, 3.3, "Slack", fc="#f0fdf4", ec=GREEN, w=1.6, h=0.6); node(ax, 1.4, 2.3, "web UI", fc="#f0fdf4", ec=GREEN, w=1.6, h=0.6)
    node(ax, 1.4, 1.3, "cron jobs", fc="#f0fdf4", ec=GREEN, w=1.6, h=0.6)
    node(ax, 4.6, 2.3, "agent loop\n(per-user context,\nmultiplayer channels)", fc="#eff6ff", ec=BLUE, w=2.6, h=1.3, fs=9, weight="bold")
    for y in (3.3, 2.3, 1.3):
        arrow(ax, 2.2, y, 3.3, 2.3 + (y - 2.3) * 0.3, color=GREEN, lw=1)
    node(ax, 4.6, 0.5, "Postgres: ALL sessions & traces\n(also a growing eval set)", fc="#fffbeb", ec=AMBER, w=3.6, h=0.75, fs=8.5)
    arrow(ax, 4.6, 1.65, 4.6, 0.9, color=AMBER, style="<|-|>")
    core = [("① remote sandbox exec", "agent PICKS the machine size"), ("② object storage read/write", ""),
            ("③ publish internal apps", "git-backed")]
    for i, (a, b) in enumerate(core):
        node(ax, 8.6, 3.7 - i * 0.95, a + ("\n" + b if b else ""), fc="#f5f3ff", ec=PURPLE, w=3.2, h=0.75, fs=8.5)
        arrow(ax, 5.9, 2.3, 7.0, 3.7 - i * 0.95, color=PURPLE, lw=1)
    node(ax, 11.7, 3.2, "company CLI · API keys ·\nOAuth keychain", fc="white", ec=GRAY, w=2.3, h=0.8, fs=8)
    node(ax, 11.7, 1.9, "DB: read-only by default;\nwrites = human-reviewed\nbulk upsert", fc="#fef2f2", ec=RED, w=2.3, h=1.0, fs=8)
    node(ax, 11.7, 0.7, "model provider chosen\nby the agent at runtime", fc="white", ec=GRAY, w=2.3, h=0.8, fs=8)
    save(fig, OUT, "11_qm_evolution_architecture.png")


if __name__ == "__main__":
    fig_harness_anatomy(); fig_timeline(); fig_loop(); fig_same_weights(); fig_arc_reported(); fig_ladder()
    fig_memory_hierarchy(); fig_context_pressure(); fig_learned_harness(); fig_open_jarvis(); fig_qm()
