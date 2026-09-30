import os
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

OUT_DIR = r"c:\PROJECTS\Learnmat\academics\compiler\images"
os.makedirs(OUT_DIR, exist_ok=True)

# Common styling constants
FONT_FAMILY = "sans-serif"
COLOR_BG = "#F8FAFC"
COLOR_TEXT = "#0F172A"
COLOR_MUTED = "#64748B"

# -----------------------------------------------------------------------------
# FIG 1: Language Processing System Pipeline & Assembly Advantage
# -----------------------------------------------------------------------------
def generate_fig01():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")

    # Title & Subtitle
    ax.text(7, 7.5, "Language Processing System Ecosystem & De-Coupled Pipeline", 
            ha="center", va="center", fontsize=15, fontweight="bold", color="#0F172A", fontfamily=FONT_FAMILY)
    ax.text(7, 7.1, "Architectural Rationale: Why Production Compilers Emit Symbolic Assembly Rather Than Raw Machine Code",
            ha="center", va="center", fontsize=10, color="#475569", fontfamily=FONT_FAMILY)

    # 4 Main Stages (Cards)
    stages = [
        {"x": 0.5, "w": 2.7, "title": "1. Preprocessing", "sub": "Macro & Header Inlining", "tool": "Preprocessor (cpp)", "in": "Source Program (.c/.cpp)", "out": "Modified Source (.i)", "c": "#2563EB", "bg": "#EFF6FF"},
        {"x": 3.7, "w": 2.7, "title": "2. Compilation", "sub": "Analysis & Synthesis", "tool": "Compiler Core (cc1)", "in": "Modified Source", "out": "Assembly Code (.s)", "c": "#7C3AED", "bg": "#FAF5FF"},
        {"x": 6.9, "w": 2.7, "title": "3. Assembly", "sub": "Mnemonic to Binary Opcode", "tool": "Assembler (as)", "in": "Assembly Mnemonics", "out": "Relocatable Object (.o)", "c": "#D97706", "bg": "#FFFBEB"},
        {"x": 10.1, "w": 3.4, "title": "4. Linking & Loading", "sub": "Symbol Resolution & Binding", "tool": "Linker/Loader (ld/ld.so)", "in": "Relocatable Object + Libs", "out": "Absolute Executable (a.out)", "c": "#059669", "bg": "#ECFDF5"},
    ]

    for st in stages:
        # Outer Card Box
        rect = patches.FancyBboxPatch((st["x"], 3.2), st["w"], 3.4, boxstyle="round,pad=0.1,rounding_size=0.2",
                                      facecolor=st["bg"], edgecolor=st["c"], linewidth=1.8)
        ax.add_patch(rect)
        
        # Stage Header Pill
        pill = patches.FancyBboxPatch((st["x"] + 0.15, 6.0), st["w"] - 0.3, 0.45, boxstyle="round,pad=0.05,rounding_size=0.1",
                                      facecolor=st["c"], edgecolor="none")
        ax.add_patch(pill)
        ax.text(st["x"] + st["w"]/2, 6.22, st["title"], ha="center", va="center", fontsize=9.5, fontweight="bold", color="#FFFFFF")

        # Subtitle
        ax.text(st["x"] + st["w"]/2, 5.75, st["sub"], ha="center", va="center", fontsize=8.5, color="#64748B", style="italic")

        # Tool Box
        tbox = patches.FancyBboxPatch((st["x"] + 0.2, 4.7), st["w"] - 0.4, 0.7, boxstyle="round,pad=0.05,rounding_size=0.1",
                                      facecolor="#FFFFFF", edgecolor=st["c"], linewidth=1, linestyle="--")
        ax.add_patch(tbox)
        ax.text(st["x"] + st["w"]/2, 5.15, "Engine / Tool:", ha="center", va="center", fontsize=7.5, color="#64748B")
        ax.text(st["x"] + st["w"]/2, 4.88, st["tool"], ha="center", va="center", fontsize=8.5, fontweight="bold", color=st["c"])

        # Input & Output Tags
        ax.text(st["x"] + 0.25, 4.25, "In: " + st["in"], ha="left", va="center", fontsize=8, color="#334155")
        ax.text(st["x"] + 0.25, 3.75, "Out: " + st["out"], ha="left", va="center", fontsize=8, fontweight="bold", color="#0F172A")

    # Flow arrows between stages
    arrows = [(3.2, 4.9, 3.7, 4.9), (6.4, 4.9, 6.9, 4.9), (9.6, 4.9, 10.1, 4.9)]
    for x1, y1, x2, y2 in arrows:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->,head_width=0.35,head_length=0.45", color="#1E293B", lw=2))

    # Bottom Architectural Callout: The 4 Strategic Advantages of Assembly Output
    callout = patches.FancyBboxPatch((0.5, 0.4), 13.0, 2.4, boxstyle="round,pad=0.1,rounding_size=0.2",
                                     facecolor="#F8FAFC", edgecolor="#94A3B8", linewidth=1.5)
    ax.add_patch(callout)

    badge = patches.FancyBboxPatch((0.8, 2.4), 3.8, 0.35, boxstyle="round,pad=0.05,rounding_size=0.08",
                                   facecolor="#1E293B", edgecolor="none")
    ax.add_patch(badge)
    ax.text(2.7, 2.57, "Key Architectural Advantages of Assembly Target", ha="center", va="center", fontsize=8.5, fontweight="bold", color="#FFFFFF")

    advs = [
        "1. Modularity & Retargetability: Decouples high-level language parsing from hardware opcodes; M front-ends + N back-ends = M + N compilers.",
        "2. Hardware Abstraction & Simplification: The compiler generates symbolic names and registers, delegating relocatable binary encoding to the Assembler.",
        "3. Independent Assembly Optimizations: The assembler handles hardware branch span calculation and instruction relaxation independently.",
        "4. Human Readability & Auditability: Assembly output allows engineers and compiler developers to inspect, verify, and debug compiler optimizations."
    ]
    for i, adv in enumerate(advs):
        ax.text(0.8, 2.05 - i*0.42, adv, ha="left", va="center", fontsize=8.2, color="#1E293B")

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "fig01_language_processing_pipeline.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Saved:", out_path)

# -----------------------------------------------------------------------------
# FIG 2: Relational Operators & Unsigned Numbers Transition Diagrams
# -----------------------------------------------------------------------------
def generate_fig02():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")

    # --- TOP SUBPLOT: Relational Operators Transition Diagram ---
    ax1.set_facecolor("#FFFFFF")
    ax1.set_xlim(-0.5, 13.5)
    ax1.set_ylim(-0.5, 5.5)
    ax1.axis("off")
    ax1.text(6.5, 5.0, "Transition Diagram: Relational Operators (RELOP) Recognition",
             ha="center", va="center", fontsize=12, fontweight="bold", color="#0F172A")

    def draw_state(ax, x, y, name, is_final=False, has_retract=False):
        c = "#2563EB" if not is_final else "#059669"
        circle = plt.Circle((x, y), 0.38, facecolor="#EFF6FF" if not is_final else "#ECFDF5",
                            edgecolor=c, lw=1.8, zorder=2)
        ax.add_patch(circle)
        if is_final:
            inner = plt.Circle((x, y), 0.31, facecolor="none", edgecolor=c, lw=1.2, zorder=3)
            ax.add_patch(inner)
        label = name + ("*" if has_retract else "")
        ax.text(x, y, label, ha="center", va="center", fontsize=9, fontweight="bold", color="#0F172A", zorder=4)

    # State 0 (Start)
    draw_state(ax1, 1.0, 2.5, "0")
    ax1.annotate("", xy=(0.95, 2.5), xytext=(0.1, 2.5),
                 arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.4", color="#475569", lw=1.5))
    ax1.text(0.5, 2.7, "start", fontsize=8, color="#475569", fontstyle="italic")

    # Branch '<': State 1
    draw_state(ax1, 4.0, 3.8, "1")
    ax1.annotate("", xy=(3.6, 3.7), xytext=(1.4, 2.65), arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.4))
    ax1.text(2.3, 3.4, "'<'", fontsize=9, fontweight="bold", color="#2563EB")

    # From 1: State 2 (<=), State 3 (<>), State 4 (< other)
    draw_state(ax1, 8.0, 4.6, "2", is_final=True)
    ax1.annotate("", xy=(7.6, 4.6), xytext=(4.4, 3.9), arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.4))
    ax1.text(5.9, 4.5, "'='", fontsize=8.5, fontweight="bold")
    ax1.text(9.2, 4.6, "return (RELOP, LE)", fontsize=8, fontweight="bold", color="#059669")

    draw_state(ax1, 8.0, 3.8, "3", is_final=True)
    ax1.annotate("", xy=(7.6, 3.8), xytext=(4.4, 3.8), arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.4))
    ax1.text(5.9, 3.95, "'>'", fontsize=8.5, fontweight="bold")
    ax1.text(9.2, 3.8, "return (RELOP, NE)", fontsize=8, fontweight="bold", color="#059669")

    draw_state(ax1, 8.0, 3.0, "4", is_final=True, has_retract=True)
    ax1.annotate("", xy=(7.6, 3.05), xytext=(4.4, 3.65), arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.4))
    ax1.text(5.6, 3.15, "other", fontsize=8.5, fontstyle="italic")
    ax1.text(9.2, 3.0, "retract(); return (RELOP, LT)", fontsize=8, fontweight="bold", color="#059669")

    # Branch '=': State 5 (=)
    draw_state(ax1, 8.0, 2.0, "5", is_final=True)
    ax1.annotate("", xy=(7.6, 2.05), xytext=(1.4, 2.45), arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.4))
    ax1.text(4.0, 2.45, "'='", fontsize=8.5, fontweight="bold")
    ax1.text(9.2, 2.0, "return (RELOP, EQ)", fontsize=8, fontweight="bold", color="#059669")

    # Branch '>': State 6
    draw_state(ax1, 4.0, 0.9, "6")
    ax1.annotate("", xy=(3.6, 1.0), xytext=(1.4, 2.3), arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.4))
    ax1.text(2.3, 1.4, "'>'", fontsize=9, fontweight="bold", color="#2563EB")

    # From 6: State 7 (>=), State 8 (> other)
    draw_state(ax1, 8.0, 1.2, "7", is_final=True)
    ax1.annotate("", xy=(7.6, 1.2), xytext=(4.4, 0.95), arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.4))
    ax1.text(5.9, 1.25, "'='", fontsize=8.5, fontweight="bold")
    ax1.text(9.2, 1.2, "return (RELOP, GE)", fontsize=8, fontweight="bold", color="#059669")

    draw_state(ax1, 8.0, 0.4, "8", is_final=True, has_retract=True)
    ax1.annotate("", xy=(7.6, 0.45), xytext=(4.4, 0.8), arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.4))
    ax1.text(5.6, 0.45, "other", fontsize=8.5, fontstyle="italic")
    ax1.text(9.2, 0.4, "retract(); return (RELOP, GT)", fontsize=8, fontweight="bold", color="#059669")


# --- BOTTOM SUBPLOT: Unsigned Numbers Transition Diagram ---
    ax2.set_facecolor("#FFFFFF")
    ax2.set_xlim(-0.5, 13.5)
    ax2.set_ylim(-1.2, 4.0)
    ax2.axis("off")
    ax2.text(6.5, 3.6, "Transition Diagram: Unsigned Numbers (Integer, Decimal, Scientific Exponential)",
             ha="center", va="center", fontsize=12, fontweight="bold", color="#0F172A")

    # States: 12 (start), 13 (digits), 14 (dot), 15 (digits after dot), 16 (E), 17 (+/-), 18 (exp digits), 19* (accept)
    num_states = [
        (0.8, 1.6, "12", False, False),
        (2.3, 1.6, "13", False, False),
        (4.0, 1.6, "14", False, False),
        (5.7, 1.6, "15", False, False),
        (7.4, 1.6, "16", False, False),
        (9.1, 2.5, "17", False, False),
        (10.5, 1.6, "18", False, False),
        (12.3, 1.6, "19", True, True)
    ]
    for x, y, name, is_final, retract in num_states:
        draw_state(ax2, x, y, name, is_final, retract)

    # Start arrow into 12
    ax2.annotate("", xy=(0.75, 1.6), xytext=(0.0, 1.6), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.5))
    ax2.text(0.35, 1.9, "start", fontsize=8.5, color="#475569", fontstyle="italic")

    # 12 -> 13 on digit
    ax2.annotate("", xy=(1.9, 1.6), xytext=(1.2, 1.6), arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.4))
    ax2.text(1.55, 1.85, "digit", fontsize=8, fontweight="bold")

    # 13 self-loop on digit
    ax2.annotate("", xy=(2.4, 2.0), xytext=(2.2, 2.0),
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-2.5", color="#1E293B", lw=1.3))
    ax2.text(2.3, 2.55, "digit", ha="center", fontsize=7.5)

    # 13 -> 14 on '.'
    ax2.annotate("", xy=(3.6, 1.6), xytext=(2.7, 1.6), arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.4))
    ax2.text(3.15, 1.85, "'.'", fontsize=8.5, fontweight="bold")

    # 14 -> 15 on digit
    ax2.annotate("", xy=(5.3, 1.6), xytext=(4.4, 1.6), arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.4))
    ax2.text(4.85, 1.85, "digit", fontsize=8, fontweight="bold")

    # 15 self-loop on digit
    ax2.annotate("", xy=(5.8, 2.0), xytext=(5.6, 2.0),
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-2.5", color="#1E293B", lw=1.3))
    ax2.text(5.7, 2.55, "digit", ha="center", fontsize=7.5)

    # 15 -> 16 on 'E' | 'e'
    ax2.annotate("", xy=(7.0, 1.6), xytext=(6.1, 1.6), arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.4))
    ax2.text(6.55, 1.85, "'E'|'e'", fontsize=8, fontweight="bold")

    # Direct 13 -> 16 on 'E'|'e' (integer scientific: 12E5) - arc high over 14 & 15
    ax2.annotate("", xy=(7.2, 1.95), xytext=(2.5, 1.95),
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.45", color="#7C3AED", lw=1.3))
    ax2.text(4.85, 3.1, "'E'|'e' (integer base)", ha="center", fontsize=8, fontweight="bold", color="#7C3AED")

    # 16 -> 17 on '+' | '-'
    ax2.annotate("", xy=(8.7, 2.4), xytext=(7.7, 1.8), arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.4))
    ax2.text(8.0, 2.45, "'+'|'-'", fontsize=8, fontweight="bold")

    # 17 -> 18 on digit
    ax2.annotate("", xy=(10.2, 1.85), xytext=(9.4, 2.4), arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.4))
    ax2.text(10.0, 2.3, "digit", fontsize=8, fontweight="bold")

    # 16 -> 18 on digit directly (no sign)
    ax2.annotate("", xy=(10.1, 1.55), xytext=(7.8, 1.55), arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.4))
    ax2.text(8.95, 1.35, "digit (unsigned exp)", ha="center", fontsize=7.5)

    # 18 self-loop on digit
    ax2.annotate("", xy=(10.6, 2.0), xytext=(10.4, 2.0),
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-2.5", color="#1E293B", lw=1.3))
    ax2.text(10.5, 2.55, "digit", ha="center", fontsize=7.5)

    # 18 -> 19 on other
    ax2.annotate("", xy=(11.9, 1.6), xytext=(10.9, 1.6), arrowprops=dict(arrowstyle="->", color="#1E293B", lw=1.4))
    ax2.text(11.4, 1.85, "other", fontsize=8, fontstyle="italic")

    # 15 -> 19 on other (fixed decimal without exp: 12.34)
    ax2.annotate("", xy=(12.05, 1.3), xytext=(5.9, 1.3),
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.3", color="#059669", lw=1.3))
    ax2.text(9.0, 0.45, "other (fixed decimal: 12.34)", ha="center", fontsize=8, color="#059669")

    # 13 -> 19 on other (plain integer: 123)
    ax2.annotate("", xy=(12.15, 1.2), xytext=(2.4, 1.2),
                 arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.45", color="#2563EB", lw=1.3))
    ax2.text(7.2, -0.65, "other (pure integer: 123)", ha="center", fontsize=8, color="#2563EB")

    ax2.text(12.3, 2.4, "retract();\nreturn (NUM, val)", ha="center", va="center", fontsize=8, fontweight="bold", color="#059669")

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "fig02_relop_and_number_dfa.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Saved:", out_path)

# -----------------------------------------------------------------------------
# FIG 3: Shift-Reduce Parser Architecture & Parsing Conflicts
# -----------------------------------------------------------------------------
def generate_fig03():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")

    ax.text(7, 7.5, "The Shift-Reduce / LR Parser Architectural Model & Conflict Taxonomy",
            ha="center", va="center", fontsize=15, fontweight="bold", color="#0F172A")
    ax.text(7, 7.1, "Data Flow between Input Buffer, Pushdown Stack, Driver Program, and Parsing Tables",
            ha="center", va="center", fontsize=10, color="#475569")

    # Input Buffer
    rect_in = patches.FancyBboxPatch((0.5, 4.4), 3.2, 2.0, boxstyle="round,pad=0.1,rounding_size=0.15",
                                     facecolor="#EFF6FF", edgecolor="#2563EB", lw=1.8)
    ax.add_patch(rect_in)
    ax.text(2.1, 6.0, "INPUT BUFFER", ha="center", va="center", fontsize=10, fontweight="bold", color="#2563EB")
    ax.text(2.1, 5.4, "[ a1 | a2 | ... | ai | ... | $ ]", ha="center", va="center", fontsize=9, fontfamily="monospace")
    ax.text(2.1, 4.8, "Lookahead Pointer  ▲", ha="center", va="center", fontsize=8, color="#1E293B")

    # Pushdown Stack
    rect_st = patches.FancyBboxPatch((0.5, 1.2), 3.2, 2.5, boxstyle="round,pad=0.1,rounding_size=0.15",
                                     facecolor="#FAF5FF", edgecolor="#7C3AED", lw=1.8)
    ax.add_patch(rect_st)
    ax.text(2.1, 3.3, "PUSHDOWN STACK", ha="center", va="center", fontsize=10, fontweight="bold", color="#7C3AED")
    ax.text(2.1, 2.7, "[ Top of Stack: Sm ]", ha="center", va="center", fontsize=8.5, fontweight="bold", color="#7C3AED")
    ax.text(2.1, 2.2, "Symbol Stack: [ $ X1 X2 ... Xm ]", ha="center", va="center", fontsize=8, fontfamily="monospace")
    ax.text(2.1, 1.6, "State Stack:  [ s0 s1 s2 ... sm ]", ha="center", va="center", fontsize=8, fontfamily="monospace")

    # Parser Driver Engine (Center)
    rect_dr = patches.FancyBboxPatch((4.8, 2.4), 3.8, 3.8, boxstyle="round,pad=0.1,rounding_size=0.2",
                                     facecolor="#F8FAFC", edgecolor="#0F172A", lw=2.2)
    ax.add_patch(rect_dr)
    ax.text(6.7, 5.8, "LR PARSER DRIVER", ha="center", va="center", fontsize=11, fontweight="bold", color="#0F172A")
    ax.text(6.7, 5.3, "Executes Loop-and-Match:", ha="center", va="center", fontsize=8.5, fontstyle="italic", color="#475569")
    
    actions = [
        "1. Inspect State Sm and Token ai",
        "2. Action = Action_Table[Sm, ai]",
        "   • Shift Sj: Push ai, Push Sj",
        "   • Reduce A->β: Pop 2|β|, Push Goto",
        "   • Accept: Parsing complete ✓",
        "   • Error: Call Error Handler ✗"
    ]
    for i, act in enumerate(actions):
        c = "#059669" if "Accept" in act else ("#DC2626" if "Error" in act else "#1E293B")
        ax.text(5.1, 4.8 - i*0.4, act, ha="left", va="center", fontsize=8, color=c, fontfamily="monospace")

    # Parsing Tables (Right)
    rect_tb = patches.FancyBboxPatch((9.7, 4.0), 3.8, 2.4, boxstyle="round,pad=0.1,rounding_size=0.15",
                                     facecolor="#FFFBEB", edgecolor="#D97706", lw=1.8)
    ax.add_patch(rect_tb)
    ax.text(11.6, 5.95, "PARSING TABLES", ha="center", va="center", fontsize=10, fontweight="bold", color="#D97706")
    ax.text(11.6, 5.35, "ACTION Table [State x Terminals]\n(shift, reduce, accept, error)", ha="center", va="center", fontsize=8, color="#334155")
    ax.text(11.6, 4.55, "GOTO Table [State x Non-Terminals]\n(target state after handle reduction)", ha="center", va="center", fontsize=8, color="#334155")

    # Connectors
    ax.annotate("", xy=(4.8, 5.0), xytext=(3.7, 5.0), arrowprops=dict(arrowstyle="->", color="#2563EB", lw=2))
    ax.text(4.25, 5.25, "ai", ha="center", fontsize=9, fontweight="bold", color="#2563EB")

    ax.annotate("", xy=(4.8, 3.2), xytext=(3.7, 3.2), arrowprops=dict(arrowstyle="<->", color="#7C3AED", lw=2))
    ax.text(4.25, 3.45, "Sm", ha="center", fontsize=9, fontweight="bold", color="#7C3AED")

    ax.annotate("", xy=(8.6, 5.2), xytext=(9.7, 5.2), arrowprops=dict(arrowstyle="<-", color="#D97706", lw=2))
    ax.text(9.15, 5.45, "Action", ha="center", fontsize=8.5, fontweight="bold", color="#D97706")

    # Output Arrow
    ax.annotate("", xy=(6.7, 1.5), xytext=(6.7, 2.4), arrowprops=dict(arrowstyle="->", color="#059669", lw=2))
    ax.text(6.7, 1.15, "OUTPUT: Parse Tree / AST / Target Translation", ha="center", va="center", fontsize=9, fontweight="bold", color="#059669")

    # Bottom Right Box: Conflicts Taxonomy
    rect_cf = patches.FancyBboxPatch((9.7, 0.8), 3.8, 2.8, boxstyle="round,pad=0.1,rounding_size=0.15",
                                     facecolor="#FEF2F2", edgecolor="#DC2626", lw=1.8)
    ax.add_patch(rect_cf)
    ax.text(11.6, 3.2, "PARSING CONFLICTS", ha="center", va="center", fontsize=10, fontweight="bold", color="#DC2626")
    ax.text(9.9, 2.65, "1. Shift / Reduce (S/R) Conflict:", fontsize=8, fontweight="bold", color="#991B1B")
    ax.text(9.9, 2.25, "Parser cannot decide whether to shift\ntoken or reduce handle (e.g. Dangling Else).", fontsize=7.5, color="#1E293B")
    ax.text(9.9, 1.6, "2. Reduce / Reduce (R/R) Conflict:", fontsize=8, fontweight="bold", color="#991B1B")
    ax.text(9.9, 1.15, "Parser cannot decide between two distinct\nproductions to reduce (Fatal ambiguity!).", fontsize=7.5, color="#1E293B")

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "fig03_shift_reduce_parser_architecture.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Saved:", out_path)

# -----------------------------------------------------------------------------
# FIG 4: Handle Pruning Reduction Tree & Rightmost Derivation in Reverse
# -----------------------------------------------------------------------------
def generate_fig04():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")

    ax.text(7, 7.5, "Handle Pruning Mechanics in Bottom-Up Shift-Reduce Parsing",
            ha="center", va="center", fontsize=15, fontweight="bold", color="#0F172A")
    ax.text(7, 7.1, "Tracing string 'aaa*a++' reducing to Start Symbol 'S' in Grammar S -> SS+ | SS* | a",
            ha="center", va="center", fontsize=10, color="#475569")

    # Step table of reductions (Left Side)
    steps = [
        ("0", "a a a * a + +", "Initial Input String", "Shift tokens to stack"),
        ("1", "S a a * a + +", "Handle: a at pos 1", "Reduce S -> a"),
        ("2", "S S a * a + +", "Handle: a at pos 2", "Reduce S -> a"),
        ("3", "S S S * a + +", "Handle: a at pos 3", "Reduce S -> a"),
        ("4", "S S a + +", "Handle: SS* (pos 2, 3, 4)", "Reduce S -> SS*"),
        ("5", "S S S + +", "Handle: a at pos 3", "Reduce S -> a"),
        ("6", "S S +", "Handle: SS+ (pos 2, 3, 4)", "Reduce S -> SS+"),
        ("7", "S", "Handle: SS+ (pos 1, 2, 3)", "Reduce S -> SS+ [ACCEPT!]")
    ]

    card_t = patches.FancyBboxPatch((0.5, 0.8), 6.5, 5.8, boxstyle="round,pad=0.1,rounding_size=0.15",
                                    facecolor="#F8FAFC", edgecolor="#64748B", lw=1.5)
    ax.add_patch(card_t)
    ax.text(3.75, 6.25, "Seven-Step Handle Pruning Sequence", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#0F172A")

    y_start = 5.6
    for i, (st_num, sent, handle, action) in enumerate(steps):
        y = y_start - i * 0.65
        bg = "#ECFDF5" if i == 7 else ("#EFF6FF" if i % 2 == 0 else "#FFFFFF")
        row_box = patches.FancyBboxPatch((0.7, y - 0.22), 6.1, 0.52, boxstyle="round,pad=0.03,rounding_size=0.08",
                                         facecolor=bg, edgecolor="#CBD5E1", lw=0.8)
        ax.add_patch(row_box)
        ax.text(0.9, y, f"[{st_num}]", ha="left", va="center", fontsize=8, fontweight="bold", color="#475569")
        ax.text(1.4, y, sent, ha="left", va="center", fontsize=8.5, fontfamily="monospace", fontweight="bold", color="#0F172A")
        ax.text(4.2, y, action, ha="left", va="center", fontsize=7.5, color="#059669" if i == 7 else "#2563EB")

    # Reduction Tree Diagram (Right Side)
    card_tr = patches.FancyBboxPatch((7.4, 0.8), 6.1, 5.8, boxstyle="round,pad=0.1,rounding_size=0.15",
                                     facecolor="#FFFFFF", edgecolor="#2563EB", lw=1.8)
    ax.add_patch(card_tr)
    ax.text(10.45, 6.25, "Synthesized Parse Tree (Leaves to Root)", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#2563EB")

    def draw_node(x, y, label, is_leaf=False, is_op=False):
        c = "#059669" if not is_leaf and not is_op else ("#D97706" if is_op else "#2563EB")
        bg = "#ECFDF5" if not is_leaf and not is_op else ("#FFFBEB" if is_op else "#EFF6FF")
        box = patches.Circle((x, y), 0.24, facecolor=bg, edgecolor=c, lw=1.4, zorder=3)
        ax.add_patch(box)
        ax.text(x, y, label, ha="center", va="center", fontsize=8.5, fontweight="bold", color="#0F172A", zorder=4)

    # Coords with ample horizontal spacing:
    # S_root (Step 7) at (10.4, 5.4)
    draw_node(10.4, 5.4, "S")
    draw_node(8.0, 4.4, "S")
    draw_node(10.4, 4.4, "S")
    draw_node(12.7, 4.4, "+", is_op=True)

    ax.plot([10.4, 8.0], [5.4, 4.4], color="#64748B", lw=1.2)
    ax.plot([10.4, 10.4], [5.4, 4.4], color="#64748B", lw=1.2)
    ax.plot([10.4, 12.7], [5.4, 4.4], color="#64748B", lw=1.2)

    # S_left (8.0) derives leaf 'a' (8.0, 1.8)
    draw_node(8.0, 1.8, "a", is_leaf=True)
    ax.plot([8.0, 8.0], [4.4, 1.8], color="#64748B", lw=1.2)

    # S_mid (10.4, 4.4) derives S_left2, S_mid2, '+'
    draw_node(9.4, 3.4, "S")
    draw_node(11.2, 3.4, "S")
    draw_node(12.1, 3.4, "+", is_op=True)

    ax.plot([10.4, 9.4], [4.4, 3.4], color="#64748B", lw=1.2)
    ax.plot([10.4, 11.2], [4.4, 3.4], color="#64748B", lw=1.2)
    ax.plot([10.4, 12.1], [4.4, 3.4], color="#64748B", lw=1.2)

    # S_left2 (9.4, 3.4) derives S_1, S_2, '*'
    draw_node(8.8, 2.6, "S")
    draw_node(9.6, 2.6, "S")
    draw_node(10.4, 2.6, "*", is_op=True)

    ax.plot([9.4, 8.8], [3.4, 2.6], color="#64748B", lw=1.2)
    ax.plot([9.4, 9.6], [3.4, 2.6], color="#64748B", lw=1.2)
    ax.plot([9.4, 10.4], [3.4, 2.6], color="#64748B", lw=1.2)

    # Leaves from S_1 and S_2
    draw_node(8.8, 1.8, "a", is_leaf=True)
    draw_node(9.6, 1.8, "a", is_leaf=True)
    ax.plot([8.8, 8.8], [2.6, 1.8], color="#64748B", lw=1.2)
    ax.plot([9.6, 9.6], [2.6, 1.8], color="#64748B", lw=1.2)

    # Leaf from S_mid2
    draw_node(11.2, 1.8, "a", is_leaf=True)
    ax.plot([11.2, 11.2], [3.4, 1.8], color="#64748B", lw=1.2)

    # Bottom leaf sequence label
    ax.text(10.4, 1.1, "Terminal Leaves:   a     a     a     *     a     +     +", ha="center", va="center",
            fontsize=9.5, fontweight="bold", fontfamily="monospace", color="#0F172A")

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "fig04_handle_pruning_reduction_tree.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Saved:", out_path)

# -----------------------------------------------------------------------------
# FIG 5: Directed Acyclic Graph (DAG) for Three-Address Code Block (2024 End Q6(b))
# -----------------------------------------------------------------------------
def generate_fig05():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")

    ax.text(7, 7.5, "Directed Acyclic Graph (DAG) with Value-Numbering & Subexpression Sharing",
            ha="center", va="center", fontsize=15, fontweight="bold", color="#0F172A")
    ax.text(7, 7.1, "Auditing 2024 End-Sem Q6(b): Elimination of redundant '4 * i' and loop increment graph",
            ha="center", va="center", fontsize=10, color="#475569")

    # Left: Three-Address Code Box
    card_c = patches.FancyBboxPatch((0.5, 0.8), 4.2, 5.8, boxstyle="round,pad=0.1,rounding_size=0.15",
                                    facecolor="#F8FAFC", edgecolor="#64748B", lw=1.5)
    ax.add_patch(card_c)
    ax.text(2.6, 6.25, "Basic Block TAC (10 Statements)", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#0F172A")

    tac_lines = [
        "1.  t1 := 4 * i",
        "2.  t2 := a[t1]",
        "3.  t3 := 4 * i   <-- REDUNDANT!",
        "4.  t4 := b[t3]",
        "5.  t5 := t2 * t4",
        "6.  t6 := prod + t5",
        "7.  prod := t6",
        "8.  t7 := i + 1",
        "9.  i := t7",
        "10. if i <= 20 goto 1"
    ]
    for i, line in enumerate(tac_lines):
        c = "#DC2626" if "REDUNDANT" in line else ("#059669" if "prod" in line else "#1E293B")
        ax.text(0.8, 5.6 - i*0.48, line, ha="left", va="center", fontsize=8.5, fontfamily="monospace", color=c)

    # Right: Directed Acyclic Graph Box
    card_d = patches.FancyBboxPatch((5.1, 0.8), 8.4, 5.8, boxstyle="round,pad=0.1,rounding_size=0.15",
                                     facecolor="#FFFFFF", edgecolor="#2563EB", lw=1.8)
    ax.add_patch(card_d)
    ax.text(9.3, 6.25, "Common Subexpression Elimination (CSE) in DAG", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#2563EB")

    def draw_dag_node(x, y, op_label, var_labels="", is_shared=False):
        c = "#7C3AED" if is_shared else ("#059669" if op_label in ["+", "*", "<="] else "#2563EB")
        bg = "#FAF5FF" if is_shared else ("#ECFDF5" if op_label in ["+", "*", "<="] else "#EFF6FF")
        box = patches.FancyBboxPatch((x-0.45, y-0.26), 0.9, 0.52, boxstyle="round,pad=0.04,rounding_size=0.1",
                                     facecolor=bg, edgecolor=c, lw=1.6, zorder=3)
        ax.add_patch(box)
        ax.text(x, y, op_label, ha="center", va="center", fontsize=9.5, fontweight="bold", color="#0F172A", zorder=4)
        if var_labels:
            ax.text(x, y+0.42, var_labels, ha="center", va="center", fontsize=8, fontweight="bold", color=c, zorder=4)

    # Leaf nodes (base inputs)
    draw_dag_node(6.2, 1.4, "4")
    draw_dag_node(7.8, 1.4, "i_0")

    # Shared Subexpression 4 * i (t1, t3)
    draw_dag_node(7.0, 2.9, "*", "t1, t3", is_shared=True)
    ax.annotate("", xy=(6.9, 2.65), xytext=(6.3, 1.7), arrowprops=dict(arrowstyle="<-", color="#7C3AED", lw=1.5))
    ax.annotate("", xy=(7.1, 2.65), xytext=(7.7, 1.7), arrowprops=dict(arrowstyle="<-", color="#7C3AED", lw=1.5))

    # Explanatory badge
    ax.text(7.0, 2.15, "★ Reused node for t1 & t3", ha="center", fontsize=7.5, fontweight="bold", color="#7C3AED")

    # Leaves 'a' and 'b' for arrays
    draw_dag_node(5.8, 4.1, "a")
    draw_dag_node(8.2, 4.1, "b")

    # Array access nodes t2 = a[t1] and t4 = b[t3]
    draw_dag_node(6.2, 4.8, "=[]", "t2")
    ax.annotate("", xy=(6.1, 4.55), xytext=(5.9, 4.35), arrowprops=dict(arrowstyle="<-", color="#475569", lw=1.3))
    ax.annotate("", xy=(6.35, 4.55), xytext=(6.9, 3.2), arrowprops=dict(arrowstyle="<-", color="#475569", lw=1.3))

    draw_dag_node(7.8, 4.8, "=[]", "t4")
    ax.annotate("", xy=(7.9, 4.55), xytext=(8.1, 4.35), arrowprops=dict(arrowstyle="<-", color="#475569", lw=1.3))
    ax.annotate("", xy=(7.65, 4.55), xytext=(7.1, 3.2), arrowprops=dict(arrowstyle="<-", color="#475569", lw=1.3))

    # Product node t5 = t2 * t4
    draw_dag_node(7.0, 5.7, "*", "t5")
    ax.annotate("", xy=(6.9, 5.45), xytext=(6.3, 5.05), arrowprops=dict(arrowstyle="<-", color="#475569", lw=1.3))
    ax.annotate("", xy=(7.1, 5.45), xytext=(7.7, 5.05), arrowprops=dict(arrowstyle="<-", color="#475569", lw=1.3))

    # Accumulator prod_0
    draw_dag_node(9.6, 4.8, "prod_0")

    # Addition node t6 = prod + t5 (prod)
    draw_dag_node(8.8, 5.7, "+", "prod, t6")
    ax.annotate("", xy=(8.35, 5.7), xytext=(7.5, 5.7), arrowprops=dict(arrowstyle="<-", color="#059669", lw=1.4))
    ax.annotate("", xy=(9.0, 5.45), xytext=(9.5, 5.05), arrowprops=dict(arrowstyle="<-", color="#059669", lw=1.4))

    # Loop index increment t7 = i + 1 (i)
    draw_dag_node(11.2, 1.4, "1")
    draw_dag_node(10.5, 2.9, "+", "i, t7")
    ax.annotate("", xy=(10.2, 2.7), xytext=(8.1, 1.6), arrowprops=dict(arrowstyle="<-", color="#2563EB", lw=1.3))
    ax.annotate("", xy=(10.7, 2.65), xytext=(11.1, 1.7), arrowprops=dict(arrowstyle="<-", color="#2563EB", lw=1.3))

    # Condition node if i <= 20
    draw_dag_node(12.6, 2.9, "20")
    draw_dag_node(11.8, 4.3, "<=", "if goto 1")
    ax.annotate("", xy=(11.6, 4.05), xytext=(10.7, 3.2), arrowprops=dict(arrowstyle="<-", color="#DC2626", lw=1.4))
    ax.annotate("", xy=(12.0, 4.05), xytext=(12.4, 3.2), arrowprops=dict(arrowstyle="<-", color="#DC2626", lw=1.4))

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "fig05_dag_value_numbering.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Saved:", out_path)

# -----------------------------------------------------------------------------
# FIG 6: Syntax Error Recovery Architecture & LL(1) Synchronizing Table
# -----------------------------------------------------------------------------
def generate_fig06():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis("off")

    ax.text(7, 7.5, "Compiler Syntax Error Handling & Recovery Architecture",
            ha="center", va="center", fontsize=15, fontweight="bold", color="#0F172A")
    ax.text(7, 7.1, "Four Error Classes, Four Universal Recovery Strategies, and LL(1) Synchronizing Set Mechanics",
            ha="center", va="center", fontsize=10, color="#475569")

    # Column 1: Four Error Classes
    card_ec = patches.FancyBboxPatch((0.5, 0.8), 3.8, 5.8, boxstyle="round,pad=0.1,rounding_size=0.15",
                                     facecolor="#FEF2F2", edgecolor="#DC2626", lw=1.8)
    ax.add_patch(card_ec)
    ax.text(2.4, 6.25, "The 4 Compiler Error Classes", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#DC2626")

    err_classes = [
        ("1. Lexical Errors", "Scanned by Lexer\n• Misspelled keywords (whlie)\n• Invalid characters (@, #)\n• Unterminated strings"),
        ("2. Syntactic Errors", "Detected by Parser\n• Unbalanced parens: (a + b *\n• Missing semicolons ';'\n• Illegal operator order: a + * b"),
        ("3. Semantic Errors", "Checked by Type Checker\n• Type incompatibility: float = str\n• Undeclared identifier use\n• Function arity mismatch"),
        ("4. Logical Errors", "Runtime Program Flaws\n• Infinite loops without exit\n• Off-by-one array indexing\n★ CANNOT BE DETECTED STATICALLY!")
    ]
    for i, (title, desc) in enumerate(err_classes):
        y = 5.5 - i * 1.3
        ax.text(0.7, y, title, ha="left", va="center", fontsize=8.5, fontweight="bold", color="#991B1B")
        ax.text(0.7, y - 0.45, desc, ha="left", va="center", fontsize=7.5, color="#1E293B")

    # Column 2: Four Recovery Strategies
    card_rs = patches.FancyBboxPatch((4.7, 0.8), 4.2, 5.8, boxstyle="round,pad=0.1,rounding_size=0.15",
                                     facecolor="#F8FAFC", edgecolor="#2563EB", lw=1.8)
    ax.add_patch(card_rs)
    ax.text(6.8, 6.25, "The 4 Recovery Strategies", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#2563EB")

    strategies = [
        ("1. Panic-Mode Recovery", "Discards tokens until reaching a synchronizing token (;, }).\n• Strengths: Guaranteed termination; zero infinite loops.\n• Weakness: Skips broad code chunks; misses bugs."),
        ("2. Phrase-Level Recovery", "Local string mutations: insert ';', delete rogue comma.\n• Strengths: Immediate recovery without token skips.\n• Danger: Infinite loops if tokens remain unconsumed!"),
        ("3. Error Productions", "Augments CFG with common student/programmer errors.\n• Strengths: Extremely accurate diagnostic messages.\n• Weakness: Bloats grammar and parser state tables."),
        ("4. Global Correction", "Computes minimum edit distance (Levenshtein) to valid code.\n• Strengths: Mathematically optimal least-cost fix.\n• Weakness: Prohibitively slow O(N³); theoretical only.")
    ]
    for i, (title, desc) in enumerate(strategies):
        y = 5.5 - i * 1.3
        ax.text(4.9, y, title, ha="left", va="center", fontsize=8.5, fontweight="bold", color="#1D4ED8")
        ax.text(4.9, y - 0.45, desc, ha="left", va="center", fontsize=7.5, color="#1E293B")

    # Column 3: LL(1) Predictive Synchronizing Table Decisions
    card_ll = patches.FancyBboxPatch((9.3, 0.8), 4.2, 5.8, boxstyle="round,pad=0.1,rounding_size=0.15",
                                     facecolor="#FAF5FF", edgecolor="#7C3AED", lw=1.8)
    ax.add_patch(card_ll)
    ax.text(11.4, 6.25, "LL(1) Synch Set Decision Table", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#7C3AED")

    ax.text(9.5, 5.65, "Dragon Book & Biswas Heuristics:", fontsize=8.5, fontweight="bold", color="#5B21B6")
    ax.text(9.5, 5.25, "• Synch Set for Non-Terminal A = FOLLOW(A)\n• Heuristic 2: Include FIRST(A) for re-expansion\n• Heuristic 3: Terminal mismatch => Pop terminal", fontsize=7.5, color="#1E293B")

    # Table Action Box
    t_box1 = patches.FancyBboxPatch((9.5, 3.6), 3.8, 1.1, boxstyle="round,pad=0.05,rounding_size=0.08",
                                    facecolor="#FFFFFF", edgecolor="#059669", lw=1.2)
    ax.add_patch(t_box1)
    ax.text(9.65, 4.4, "Case A: Table Entry is Production", fontsize=8, fontweight="bold", color="#059669")
    ax.text(9.65, 3.95, "Action: Pop A; Push body in reverse order.\nNormal deterministic derivation.", fontsize=7.5, color="#1E293B")

    t_box2 = patches.FancyBboxPatch((9.5, 2.3), 3.8, 1.1, boxstyle="round,pad=0.05,rounding_size=0.08",
                                    facecolor="#FFFFFF", edgecolor="#7C3AED", lw=1.2)
    ax.add_patch(t_box2)
    ax.text(9.65, 3.1, "Case B: Table Entry is 'synch'", fontsize=8, fontweight="bold", color="#7C3AED")
    ax.text(9.65, 2.65, "Action: POP NON-TERMINAL A FROM STACK!\nDo NOT skip input token (token is in FOLLOW).", fontsize=7.5, color="#1E293B")

    t_box3 = patches.FancyBboxPatch((9.5, 1.0), 3.8, 1.1, boxstyle="round,pad=0.05,rounding_size=0.08",
                                    facecolor="#FFFFFF", edgecolor="#DC2626", lw=1.2)
    ax.add_patch(t_box3)
    ax.text(9.65, 1.8, "Case C: Table Entry is BLANK", fontsize=8, fontweight="bold", color="#DC2626")
    ax.text(9.65, 1.35, "Action: SKIP UNEXPECTED INPUT TOKEN!\nDo NOT pop stack symbol (await valid token).", fontsize=7.5, color="#1E293B")

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, "fig06_syntax_error_recovery_architecture.png")
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    print("Saved:", out_path)

if __name__ == "__main__":
    print("Generating all 6 publication-grade figures at 300 DPI...")
    generate_fig01()
    generate_fig02()
    generate_fig03()
    generate_fig04()
    generate_fig05()
    generate_fig06()
    print("ALL 6 FIGURES GENERATED SUCCESSFULLY!")
