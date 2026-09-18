"""Figures for 'Agent Memory - Long-Term Memory with Mem0'.
Figure 06 is computed by code/agent_memory_mini.py (a runnable mini version of the pipeline).
Run:  python figures/agent_memory/make_figs.py
"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "code"))
from _style import *

OUT = out_dir(__file__)


# ------------------------------------------------------------------ 01 stateless LLM, history resent
def fig_history_cost():
    turns = np.arange(1, 41)
    per_turn = 350  # tokens per user+assistant exchange (assumption)
    system = 1500
    sent = system + per_turn * turns
    cum = np.cumsum(sent)
    fig, axes = plt.subplots(1, 2, figsize=(12, 3.9))
    ax = axes[0]
    ax.bar(turns, sent, color=BLUE)
    ax.axhline(system, color=AMBER, ls="--"); ax.text(1, system + 300, "system prompt", color=AMBER, fontsize=8)
    ax.set_xlabel("turn number"); ax.set_ylabel("tokens sent to the LLM this turn")
    ax.set_title("The LLM is stateless: EVERY turn resends the whole history")
    ax = axes[1]
    ax.plot(turns, cum / 1000, color=RED, lw=2.5, label="resend full history (grows ~quadratically)")
    ax.plot(turns, np.cumsum(np.full_like(turns, system + per_turn + 400)) / 1000, color=GREEN, lw=2.5,
            label="system + latest exchange + ~400 tokens of recalled memories")
    ax.set_xlabel("turn number"); ax.set_ylabel("total tokens processed (thousands)")
    ax.set_title("Cumulative cost of a long conversation\n(assumes 350 tokens per exchange)"); ax.legend(fontsize=8)
    save(fig, OUT, "01_stateless_history_cost.png")


# ------------------------------------------------------------------ 02 short-term vs long-term
def fig_short_long():
    fig, ax = canvas(12, 5.2, (0, 12), (0, 5.2))
    ax.text(6, 4.95, "Conversational (short-term) memory vs long-term memory", ha="center", fontsize=12, weight="bold")
    for i, (name, col) in enumerate([("Conversation A (Monday)", BLUE), ("Conversation B (Friday)", PURPLE)]):
        x = 0.3 + i * 3.1
        ax.add_patch(FancyBboxPatch((x, 2.2), 2.8, 2.3, boxstyle="round,pad=0.03", fc="#f9fafb", ec=col, lw=1.5))
        ax.text(x + 1.4, 4.2, name, ha="center", fontsize=9, weight="bold", color=col)
        for j, m in enumerate(["user: I'm vegan", "AI: noted!", "user: …", "AI: …"] if i == 0 else ["user: dinner ideas?", "AI: ???", "", ""]):
            ax.text(x + 0.15, 3.75 - j * 0.38, m, fontsize=8.5, family="monospace")
        ax.text(x + 1.4, 2.35, "history lives only in THIS session", ha="center", fontsize=7.5, color=GRAY)
    ax.text(3.2, 3.3, "✗", fontsize=26, color=RED, ha="center", va="center")
    box(ax, 7.0, 2.3, 4.7, 2.1, "LONG-TERM MEMORY SERVICE\n(external to every session)\n\n• 'user is vegan'\n• 'user lives in Berlin'",
        fc="#f0fdf4", ec=GREEN, fs=9, weight="bold")
    arrow(ax, 3.1, 2.2, 7.0, 2.8, color=GREEN, rad=0.25, text="ingest after turns", fs=8)
    arrow(ax, 7.0, 3.6, 6.2, 3.6, color=GREEN, text="recall", fs=8)
    for i, a in enumerate(["ChatGPT", "Claude", "your support bot"]):
        box(ax, 7.0 + i * 1.6, 0.4, 1.45, 0.8, a, fc="white", ec=GRAY, fs=8.5)
        arrow(ax, 7.7 + i * 1.6, 1.2, 9.35, 2.3, color=GRAY, lw=1)
    ax.text(3.2, 0.8, "same user → memory can be shared across\nmany agents (with attribution per agent)", ha="center", fontsize=9)
    save(fig, OUT, "02_short_vs_long_term.png")


# ------------------------------------------------------------------ 03 three stores
def fig_stores():
    fig, ax = canvas(12, 4.8, (0, 12), (0, 4.8))
    ax.text(6, 4.55, "Mem0's three stores", ha="center", fontsize=12, weight="bold")
    box(ax, 0.2, 0.4, 4.3, 3.7,
        "① MAIN MEMORY STORE (vector DB)\n\n"
        "text: 'user's favorite neighborhood\n        in Paris is Marais'\n"
        "vector: [0.12, -0.33, …]\n"
        "created / updated: 2026-09-01\n"
        "owner: user | agent\n"
        "hash: 9f2c…  (exact dedup)\n"
        "lemmas: 'user favorite neighborhood …'\n"
        "expires: —      agent: travel-bot", fc="#eff6ff", ec=BLUE, fs=8.5, ha="left")
    box(ax, 5.0, 2.2, 3.2, 1.9,
        "② ENTITY STORE (vector DB)\n\n"
        "'Paris'  → memories {12, 40}\n"
        "'Marais' → memories {12}\n"
        "'Spotify' → memories {7}", fc="#fffbeb", ec=AMBER, fs=8.5, ha="left")
    box(ax, 5.0, 0.4, 3.2, 1.5,
        "③ SQLite\n• change history (ADD / UPDATE / DELETE)\n• rolling buffer: last 10 messages", fc="#f5f3ff", ec=PURPLE, fs=8.5, ha="left")
    arrow(ax, 5.0, 3.2, 4.5, 3.0, color=AMBER, text="links", fs=8)
    box(ax, 8.7, 0.4, 3.1, 3.7,
        "Why each exists\n\n"
        "① semantic recall:\n   'food I like' ≈ 'vegan restaurants'\n\n"
        "② specific names boost the\n   right memories\n\n"
        "③ resolve 'it' / 'he' during\n   extraction; audit trail",
        fc="#f9fafb", ec=GRAY, fs=8.5, ha="left")
    save(fig, OUT, "03_three_stores.png")


# ------------------------------------------------------------------ 04 ingestion pipeline
def fig_ingestion():
    fig, ax = canvas(13, 5.4, (0, 13), (0, 5.4))
    ax.text(6.5, 5.15, "Ingestion: after every agent turn", ha="center", fontsize=12, weight="bold")
    box(ax, 0.2, 2.2, 1.7, 1.0, "messages of\nthis turn", fc="#f9fafb", ec=GRAY, fs=9)
    box(ax, 2.5, 4.0, 2.4, 0.8, "procedural: summarize\nsteps & tool calls", fc="white", ec=GRAY, fs=8.5)
    box(ax, 2.5, 2.3, 2.4, 0.8, "infer = false:\nembed & store as-is", fc="white", ec=GRAY, fs=8.5)
    box(ax, 2.5, 0.6, 2.4, 0.8, "infer = true:\nLLM extraction", fc="#eff6ff", ec=BLUE, fs=8.5, weight="bold")
    for y in (4.4, 2.7, 1.0):
        arrow(ax, 1.9, 2.7, 2.5, y, color=GRAY)
    ctx = ["role: 'memory extractor'", "user summary", "new messages", "recently saved memories",
           "related memories (vector search)", "last 10 messages (SQLite)", "conversation date + today"]
    ax.add_patch(FancyBboxPatch((5.5, 0.3), 3.3, 4.4, boxstyle="round,pad=0.03", fc="#eff6ff", ec=BLUE, lw=1.4))
    ax.text(7.15, 4.45, "① build extraction prompt", ha="center", fontsize=9, weight="bold", color=BLUE)
    for i, c in enumerate(ctx):
        ax.text(5.7, 3.95 - i * 0.5, "• " + c, fontsize=8.5)
    arrow(ax, 4.9, 1.0, 5.5, 1.5, color=BLUE)
    box(ax, 9.3, 3.2, 3.5, 1.3, "② small LLM → JSON\n{\"memory\": \"user prefers\n  vegan restaurants\"}", fc="white", ec=BLUE, fs=8.5)
    box(ax, 9.3, 0.4, 3.5, 2.4, "③ save\n• dates, owner, agent\n• hash → skip exact duplicates\n• lemmatized text (for BM25)\n• entities → entity store\n• log + update 10-msg buffer",
        fc="#f0fdf4", ec=GREEN, fs=8.5)
    arrow(ax, 8.8, 3.8, 9.3, 3.8, color=BLUE); arrow(ax, 11.05, 3.2, 11.05, 2.8, color=GREEN)
    save(fig, OUT, "04_ingestion_pipeline.png")


# ------------------------------------------------------------------ 05 retrieval pipeline
def fig_retrieval():
    fig, ax = canvas(13, 4.6, (0, 13), (0, 4.6))
    ax.text(6.5, 4.35, "Retrieval: same pipeline for the 'search memory' tool and automatic recall", ha="center",
            fontsize=12, weight="bold")
    steps = [("query\n(+ top_k, threshold,\nidentity)", "#f9fafb", GRAY),
             ("① embed query\n(same model as\nthe store)", "#eff6ff", BLUE),
             ("② vector search\npool = max(4·top_k, 60)\ncandidates", "#eff6ff", BLUE),
             ("③ BM25 on lemmas\nscore 0 – 1", "#fffbeb", AMBER),
             ("④ entity boost\n0 – 0.5, bigger for\nrare entities", "#fef3c7", AMBER),
             ("⑤ (sem + bm25 + ent)\n÷ 2.5 → 0 – 1\nkeep top_k ≥ threshold", "#f0fdf4", GREEN)]
    for i, (t, fc, ec) in enumerate(steps):
        x = 0.2 + i * 2.15
        box(ax, x, 1.6, 1.95, 1.6, t, fc=fc, ec=ec, fs=8.5)
        if i:
            arrow(ax, x - 0.2, 2.4, x, 2.4, color=DARK)
    ax.text(6.5, 0.7, "Reranking (③ ④ ⑤) can only REORDER the pool from ②: a memory the vector search missed can never come back.",
            ha="center", fontsize=9.5, color=RED)
    save(fig, OUT, "05_retrieval_pipeline.png")


# ------------------------------------------------------------------ 06 worked scoring (computed)
def fig_scoring():
    from agent_memory_mini import MemoryStore
    store = MemoryStore()
    for m in ["The user prefers vegan restaurants", "The user's favorite neighborhood in Paris is Marais",
              "The user is planning a trip to Paris in October", "The user works as a data engineer at Spotify",
              "The user is allergic to peanuts", "The user likes jazz bars"]:
        store.add(m)
    q = "Where should I eat in Paris?"
    rows = store.search(q, top_k=6, explain=True)
    labels = [store.memories[mid]["text"].replace("The user", "user") for _, mid, *_ in rows][::-1]
    sem = np.array([r[2] for r in rows])[::-1] / 2.5
    kw = np.array([r[3] for r in rows])[::-1] / 2.5
    ent = np.array([r[4] for r in rows])[::-1] / 2.5
    fig, ax = plt.subplots(figsize=(10, 3.8))
    y = np.arange(len(rows))
    ax.barh(y, sem, color=BLUE, label="semantic ÷ 2.5")
    ax.barh(y, kw, left=sem, color=AMBER, label="BM25 keyword ÷ 2.5")
    ax.barh(y, ent, left=sem + kw, color=GREEN, label="entity boost ÷ 2.5")
    for yi, tot in zip(y, sem + kw + ent):
        ax.text(tot + 0.01, yi, f"{tot:.3f}", va="center", fontsize=9)
    ax.set_yticks(y); ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("final score (0 – 1)"); ax.set_xlim(0, 0.8)
    ax.set_title(f"Computed by code/agent_memory_mini.py for the query: \"{q}\"")
    ax.legend(fontsize=8, loc="lower right")
    save(fig, OUT, "06_scoring_worked_example.png")


# ------------------------------------------------------------------ 07 entity specificity
def fig_entity_specificity():
    n = np.arange(1, 1001)
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    ax.semilogx(n, 0.5 / np.sqrt(n), color=GREEN, lw=2.5)
    for k, lab in [(1, "'Marais': 1 memory"), (2, "'Paris': 2 memories"), (50, "'Paris' after\na year of travel chats"), (1000, "'Monday': 1000")]:
        ax.scatter([k], [0.5 / np.sqrt(k)], color=DARK, zorder=4)
        ax.annotate(lab, (k, 0.5 / np.sqrt(k)), (8, 6), textcoords="offset points", fontsize=8.5)
    ax.set_xlabel("number of memories linked to the matched entity"); ax.set_ylabel("entity boost")
    ax.set_title("Entity boost rewards SPECIFIC entities\n(shape used in our mini implementation: 0.5/√n — Mem0's exact formula may differ)")
    ax.grid(alpha=0.3); ax.set_ylim(0, 0.6)
    save(fig, OUT, "07_entity_specificity.png")


# ------------------------------------------------------------------ 08 memory taxonomy
def fig_taxonomy():
    fig, ax = canvas(12, 4.6, (0, 12), (0, 4.6))
    ax.text(6, 4.35, "Types of agent memory (borrowed from cognitive science, e.g. the CoALA framework)", ha="center",
            fontsize=11.5, weight="bold")
    cols = [("WORKING / SHORT-TERM", "the context window:\ncurrent conversation,\ntool results", "resent every turn;\nlost when session ends", BLUE),
            ("SEMANTIC", "facts:\n'user is vegan',\n'API key rotates monthly'", "Mem0 extracted memories;\nuser profiles", GREEN),
            ("EPISODIC", "experiences:\n'last Tuesday the deploy\nfailed because …'", "past conversation logs,\nsummaries with dates", AMBER),
            ("PROCEDURAL", "how-to:\n'to release, run tests,\nthen tag, then …'", "saved tool-call sequences,\nskills, CLAUDE.md files", PURPLE)]
    for i, (t, what, impl, c) in enumerate(cols):
        x = 0.2 + i * 2.95
        box(ax, x, 3.1, 2.75, 0.7, t, fc="white", ec=c, fs=9.5, weight="bold", tc=c)
        box(ax, x, 1.7, 2.75, 1.2, what, fc="#f9fafb", ec=c, fs=8.5)
        box(ax, x, 0.3, 2.75, 1.2, impl, fc="white", ec=c, fs=8.5, lw=1)
    ax.text(0.05, 2.3, "what", rotation=90, fontsize=8, color=GRAY, va="center")
    ax.text(0.05, 0.9, "how built", rotation=90, fontsize=8, color=GRAY, va="center")
    save(fig, OUT, "08_memory_taxonomy.png")


if __name__ == "__main__":
    fig_history_cost(); fig_short_long(); fig_stores(); fig_ingestion(); fig_retrieval(); fig_scoring()
    fig_entity_specificity(); fig_taxonomy()
