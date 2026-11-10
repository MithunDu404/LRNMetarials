# Learnmat Workspace Guidelines (Antigravity)

This workspace is an interactive engineering study repository and Obsidian vault containing:
- **Study Guides (`Theory/`):** Self-contained, deeply researched study guides covering machine learning, AI engineering, and systems design (each with diagrams, formulas, code, and self-quizzes).
- **Original Source Files (`_originals/`):** Raw video transcripts, lecture notes, and research papers/PDFs used as source material.
- **Native Learning & Quiz Skills (`.agent/skills/`):** Socratic teaching and interactive testing workflows configured specifically for Antigravity.

---

## 1. Interaction Modes

### Mode A: Guided Teaching (`teach` skill)
When the user asks to **learn, understand, or study** a topic or reference file (e.g., *"Teach me MLA from `_originals/...`"*):
- Apply the **teach** skill (`.agent/skills/teach/SKILL.md`).
- Follow the 3-phase flow: **Probe** (knowledge frontier via `ask_question`) $\rightarrow$ **Plan** (Mermaid DAG + approval) $\rightarrow$ **Teach** (Motivate $\rightarrow$ Establish $\rightarrow$ Connect $\rightarrow$ Quiz-check loop).
- Focus on first principles ("unconditional truths first") and motivated discovery ("how could I have discovered this?").
- **Adaptive Visuals:** Prioritize embedding original figures from `figures/<topic>/` when available, or draw native Mermaid diagrams.
- **Spaced Recall Checkpoints:** Interleave recall & synthesis questions testing earlier concepts every 2–3 nodes.
- **Timing:** Always write question callouts to the Obsidian note on disk *before* launching the interactive popup.

### Mode B: Pure Quizzing (`quiz` skill)
When the user asks to **be quizzed, tested, or examined** on a topic or file (e.g., *"Quiz me on Backpropagation"*):
- Apply the **quiz** skill (`.agent/skills/quiz/SKILL.md`).
- **Continuous by default:** Never stop at 5 questions or set an arbitrary limit. Keep generating questions one at a time indefinitely until the user explicitly says to stop.
- Deliver questions **one at a time** using the interactive `ask_question` tool.
- **Answer Shuffling:** The correct answer must **NEVER default to Option 1**. Randomly distribute the correct answer across slots (Option 1, 2, 3, etc.), with "I don't know" always at the very bottom.
- Provide instant feedback (✓/✗/I don't know), correct answer, and diagnostic explanations.
- Never dump multiple questions in static chat text.

---

## 2. Formatting & Obsidian Standards

- **Math & LaTeX Standards:**
  - Inline: `$E = mc^2$`
  - Display: Isolated `$$` on its own line at column 0, preceded and followed by an empty blank line:
    ```markdown
    $$
    \nabla_\theta \mathcal{L}(\theta)
    $$
    ```
  - **Decouple Math from Bold:** Never embed math inside bold asterisks (`**Label ($math$):**` is forbidden). Always keep math outside bold: `**Label** ($math$):`.
  - **Matrix Row Breaks:** In LaTeX environments (`matrix`, `aligned`, `cases`), place `\\` at the end of the line before a newline (never mid-line) to prevent CommonMark from collapsing rows.
- **Code Fences:** Fenced code blocks strictly require $\ge 3$ backticks (` ``` `). Never use two backticks (` `` `) to open or close blocks; two backticks is parsed by CommonMark as an inline code span that swallows subsequent markdown and hides math from rendering.
- **Diagrams & Visuals:**
  - Use native Mermaid fenced blocks (```mermaid ... ```). Both Antigravity and Obsidian render Mermaid natively without external dependencies.
  - **Zero ASCII Art:** Never generate monospace sketch boxes with `+---+` or `|...|`. Use native Mermaid diagrams or high-resolution Python plots.
- **Obsidian Live Logging:** When the user specifies a note to log or study into (e.g. `MyTopic.md`), write/append directly to the file on disk. Use native Obsidian callouts:
  - `> [!abstract] Teacher`
  - `> [!question] Question / Quiz`
  - `> [!success] Correct ✓`
  - `> [!failure] Incorrect ✗`
  - `> [!quote] Learner`
