"""Figures for 'Python DSA - Templates Patterns and Performance' (target/py/).

Every figure is MEASURED by target/py/code/dsa/dsa_benchmarks.py on the machine that
runs this script. Needs numpy, matplotlib (and sortedcontainers for one bar).
Run:  py -3.12 target/py/images/make_dsa_figs.py      (about 2-3 minutes)
"""
import os
import platform
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "code", "dsa"))
import dsa_benchmarks as B  # noqa: E402

BLUE, RED, GREEN, AMBER, PURPLE, GRAY, LIGHT = "#2563eb", "#dc2626", "#16a34a", "#d97706", "#7c3aed", "#6b7280", "#e5e7eb"
plt.rcParams.update({
    "figure.dpi": 150, "savefig.bbox": "tight", "savefig.facecolor": "white",
    "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titleweight": "bold", "axes.titlesize": 11, "legend.frameon": False,
})
MACHINE = f"Measured: CPython {sys.version.split()[0]}, {platform.system()}, best of 3"


def save(fig, name):
    fig.savefig(os.path.join(HERE, name))
    plt.close(fig)
    print("wrote", name)


def note(ax, text, loc=(0.02, 0.97)):
    ax.text(*loc, text, transform=ax.transAxes, fontsize=8, color=GRAY, va="top",
            bbox=dict(fc="white", ec=LIGHT, pad=3))


def fig04_queue():
    rows = B.bench_queue()
    n = [r[0] for r in rows]
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.loglog(n, [r[1] for r in rows], "o-", color=RED, label="list.pop(0)   (each pop shifts every pointer)")
    ax.loglog(n, [r[2] for r in rows], "o-", color=GREEN, label="deque.popleft()")
    ax.set_xlabel("items in the queue (n, log scale)")
    ax.set_ylabel("seconds to drain it (log scale)")
    ax.set_title(f"Using a list as a queue: {rows[-1][1] / rows[-1][2]:.0f}x slower at n = {n[-1]:,}")
    ax.legend(loc="upper left", fontsize=8)
    note(ax, MACHINE + "\nRed slope is about 2 on log-log = O(n^2) total;\ngreen slope is about 1 = O(n).", (0.0, -0.20))
    save(fig, "fig04_queue_pop0.png")


def fig05_strings():
    rows = B.bench_strings()
    n = [r[0] for r in rows]
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.loglog(n, [r[3] for r in rows], "o-", color=RED, label="t = s; s = t + 'x'   (another reference: full copy)")
    ax.loglog(n, [r[2] for r in rows], "o-", color=AMBER, label="s += 'x', with occasional extra references")
    ax.loglog(n, [r[1] for r in rows], "o-", color=BLUE, label="s += 'x'   (CPython resizes in place)")
    ax.loglog(n, [r[4] for r in rows], "o-", color=GREEN, label="''.join(list)")
    ax.set_xlabel("characters appended (log scale)")
    ax.set_ylabel("seconds (log scale)")
    ax.set_title("String building: += is only quadratic when the string is shared")
    ax.legend(loc="upper left", fontsize=8)
    note(ax, MACHINE + "\nThe in-place += trick is a CPython detail;\nPyPy and other runtimes don't promise it.", (0.52, 0.22))
    save(fig, "fig05_string_building.png")


def fig06_input():
    n, startup, res = B.bench_input()
    names = list(res)
    vals = [res[k] for k in names]
    fig, ax = plt.subplots(figsize=(7.5, 3.4))
    bars = ax.barh(names[::-1], vals[::-1], color=[GREEN, GREEN, AMBER, RED])
    for b, v in zip(bars, vals[::-1]):
        ax.text(v + max(vals) * 0.01, b.get_y() + b.get_height() / 2, f"{v:.2f} s", va="center", fontsize=8)
    ax.set_xlabel(f"seconds to read and sum {n:,} integers (interpreter startup removed)")
    ax.set_title("Fast input: read everything at once")
    ax.set_xlim(0, max(vals) * 1.25)
    note(ax, MACHINE + "\nInput from a file redirected to stdin.\nJudges' pipes and machines differ.", (0.60, 0.40))
    save(fig, "fig06_input_reading.png")


def fig07_priority():
    n, res = B.bench_priority()
    names = list(res)
    vals = [res[k] for k in names]
    colours = {"heapq push + pop": GREEN, "heapify + pop": GREEN, "queue.PriorityQueue": AMBER,
               "bisect.insort list": RED, "SortedList": BLUE}
    fig, ax = plt.subplots(figsize=(7.5, 3.6))
    bars = ax.barh(names[::-1], vals[::-1], color=[colours[k] for k in names[::-1]])
    for b, v in zip(bars, vals[::-1]):
        ax.text(v + max(vals) * 0.01, b.get_y() + b.get_height() / 2, f"{v:.3f} s", va="center", fontsize=8)
    ax.set_xlabel(f"seconds to push {n:,} random floats, then pop them all")
    ax.set_title("Priority structures: heapq wins; insort is O(n) per insert")
    ax.set_xlim(0, max(vals) * 1.2)
    note(ax, MACHINE + "\nPriorityQueue pays for thread locks.\nSortedList also gives order queries.", (0.58, 0.97))
    save(fig, "fig07_priority_structures.png")


def fig08_bignum():
    rows = B.bench_bignum()
    n = [r[0] for r in rows]
    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    ax.loglog(n, [r[2] for r in rows], "o-", color=RED, label="multiply everything, % MOD once at the end")
    ax.loglog(n, [r[1] for r in rows], "o-", color=GREEN, label="p = p * x % MOD every step")
    ax.set_xlabel("numbers multiplied (each up to 1e9, log scale)")
    ax.set_ylabel("seconds (log scale)")
    ax.set_title(f"No overflow, but {rows[-1][2] / rows[-1][1]:.0f}x slower at n = {n[-1]:,}")
    ax.legend(loc="upper left", fontsize=8)
    note(ax, MACHINE + "\nRed slope about 2: the product grows by ~30 bits per step\nand each step re-touches all of it, so total work is O(n^2).", (0.0, -0.20))
    save(fig, "fig08_bignum_mod.png")


def fig09_recursion():
    cap, rows = B.bench_recursion()
    names = {"plain": "plain recursion", "cache": "@functools.cache recursion", "dict": "dict memo (manual)"}
    labels = [f"{names[k]} ({w})" for k, w, _ in rows]
    depths = [d for _, _, d in rows]
    cols = [RED if d < 10_000 else GREEN for d in depths]
    fig, ax = plt.subplots(figsize=(7.8, 3.8))
    bars = ax.barh(labels[::-1], depths[::-1], color=cols[::-1])
    ax.set_xscale("log")
    for b, d in zip(bars, depths[::-1]):
        ax.text(d * 1.15, b.get_y() + b.get_height() / 2,
                f"{d:,}" + ("+ (search cap)" if d == cap else ""), va="center", fontsize=8)
    ax.set_xlim(100, cap * 30)
    ax.set_xlabel("deepest call chain that worked (log scale)")
    ax.set_title("sys.setrecursionlimit(10**6) does not lift @cache's limit")
    note(ax, MACHINE.replace(", best of 3", "") + "\n'thread' = 64 MiB thread stack.\nOther versions/OSes differ: test on your judge.", (0.0, -0.20))
    save(fig, "fig09_recursion_limits.png")


def fig12_fenwick(n=16):
    """Which range of the array each Fenwick slot tree[i] sums: (i - lowbit(i), i]."""
    fig, ax = plt.subplots(figsize=(8.6, 4.6))
    for i in range(1, n + 1):
        low = i & -i
        lo, hi = i - low, i
        col = {1: GRAY, 2: BLUE, 4: GREEN, 8: AMBER, 16: RED}[low]
        ax.barh(i, hi - lo, left=lo + 0.5, height=0.7, color=col, alpha=0.85)
        ax.text(hi + 0.65, i, f"tree[{i}] = a[{lo + 1}..{hi}]   ({i:05b}, lowbit {low})",
                va="center", fontsize=7.5)
    # path for prefix(13): 13 -> 12 -> 8 -> 0
    path, i = [], 13
    while i:
        path.append(i)
        i -= i & -i
    for k in path:
        ax.plot(k - (k & -k) / 2 + 0.5, k, marker="*", color="black", ms=9)
    ax.set_yticks(range(1, n + 1))
    ax.set_xticks(range(1, n + 1))
    ax.set_xlim(0.5, n + 12)
    ax.invert_yaxis()
    ax.set_xlabel("array position a[1..16] (1-based, as Fenwick trees use internally)")
    ax.set_ylabel("slot i of tree[]")
    ax.set_title("Fenwick tree: slot i covers the last lowbit(i) positions ending at i")
    ax.text(0.0, -0.13, "Computed from i & -i, not drawn by hand. Stars: prefix(13) = tree[13] + tree[12] + tree[8] "
            "(13 -> 12 -> 8 -> 0 by i -= i & -i), so 3 slots instead of 13 additions.",
            transform=ax.transAxes, fontsize=8, color=GRAY, va="top")
    save(fig, "fig12_fenwick_ranges.png")


def fig13_binary_search_answer():
    """Feasibility of 'ship weights 1..10 within 5 days' as capacity grows: False...False True...True."""
    weights, days = list(range(1, 11)), 5

    def days_needed(cap):
        need, load = 1, 0
        for w in weights:
            if load + w > cap:
                need, load = need + 1, 0
            load += w
        return need

    caps = list(range(max(weights), sum(weights) + 1))
    need = [days_needed(c) for c in caps]
    ok = [d <= days for d in need]
    answer = caps[ok.index(True)]
    fig, ax = plt.subplots(figsize=(8, 3.8))
    ax.bar(caps, need, color=[GREEN if o else RED for o in ok], width=0.8)
    ax.axhline(days, color=GRAY, ls="--", lw=1)
    ax.text(caps[-1], days + 0.15, f"limit: {days} days", ha="right", fontsize=8, color=GRAY)
    ax.annotate(f"first capacity that works = {answer}\n(the answer first_true finds)",
                xy=(answer, days_needed(answer)), xytext=(answer + 12, 6.2),
                arrowprops=dict(arrowstyle="->", color="black"), fontsize=9)
    ax.set_xlabel("ship capacity tried")
    ax.set_ylabel("days needed")
    ax.set_title("Binary search on the answer: red (too small) then green (works), never mixed")
    ax.text(0.0, -0.22, f"Computed for weights 1..10. Capacities {caps[0]}..{caps[-1]} = {len(caps)} candidates; "
            f"binary search checks about log2({len(caps)}) = {len(caps).bit_length()} of them.",
            transform=ax.transAxes, fontsize=8, color=GRAY, va="top")
    save(fig, "fig13_binary_search_answer.png")


if __name__ == "__main__":
    fig12_fenwick()
    fig13_binary_search_answer()
    fig04_queue()
    fig05_strings()
    fig06_input()
    fig07_priority()
    fig08_bignum()
    fig09_recursion()
