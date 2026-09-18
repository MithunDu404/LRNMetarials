"""Shared plotting style + small drawing helpers for every study-guide figure script.

Usage inside figures/<topic>/make_figs.py:
    import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from _style import *
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon, FancyArrowPatch

BLUE = "#2563eb"
RED = "#dc2626"
GREEN = "#16a34a"
AMBER = "#d97706"
PURPLE = "#7c3aed"
TEAL = "#0d9488"
PINK = "#db2777"
GRAY = "#6b7280"
LIGHT = "#e5e7eb"
DARK = "#111827"

plt.rcParams.update({
    "figure.dpi": 150, "savefig.bbox": "tight", "savefig.facecolor": "white",
    "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titleweight": "bold", "axes.titlesize": 11, "legend.frameon": False,
})


def out_dir(script_file):
    d = os.path.dirname(os.path.abspath(script_file))
    os.makedirs(d, exist_ok=True)
    return d


def save(fig, out, name):
    fig.savefig(os.path.join(out, name))
    plt.close(fig)
    print("wrote", name)


def box(ax, x, y, w, h, text, fc="white", ec=DARK, fs=9, tc=DARK, lw=1.4, weight="normal",
        style="round,pad=0.02,rounding_size=0.08", ha="center", zorder=3):
    """Rounded box whose (x, y) is the lower-left corner."""
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=style, fc=fc, ec=ec, lw=lw, zorder=zorder))
    tx = x + w / 2 if ha == "center" else x + 0.08
    ax.text(tx, y + h / 2, text, ha=ha, va="center", fontsize=fs, color=tc, weight=weight,
            zorder=zorder + 1, wrap=True)


def arrow(ax, x1, y1, x2, y2, color=DARK, lw=1.4, style="-|>", ms=12, ls="-", rad=0.0, zorder=2,
          text=None, fs=8, tcolor=None, toff=(0, 0.08)):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=ms, color=color,
                                 lw=lw, linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=zorder))
    if text:
        ax.text((x1 + x2) / 2 + toff[0], (y1 + y2) / 2 + toff[1], text, fontsize=fs, ha="center",
                va="bottom", color=tcolor or color, zorder=zorder + 5,
                bbox=dict(fc="white", ec="none", pad=0.5, alpha=0.9))


def canvas(w=10, h=5, xlim=(0, 10), ylim=(0, 5)):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")
    return fig, ax
