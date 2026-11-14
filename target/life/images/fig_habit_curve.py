import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Simple asymptotic model of automaticity used in Lally et al. (2010): A(t) = 1 - exp(-k t),
# with k chosen so that 95% of the plateau is reached at 18, 66 (median) and 254 days.
t = np.linspace(0, 260, 600)
fig, ax = plt.subplots(figsize=(8, 4.6), facecolor="white")
for days, colour, label in [(18, "#059669", "Fast habit (18 days)"),
                            (66, "#2563EB", "Median habit (66 days)"),
                            (254, "#D97706", "Slow habit (254 days)")]:
    k = math.log(20) / days
    ax.plot(t, 1 - np.exp(-k * t), color=colour, lw=2.2, label=label)
    ax.plot([days], [0.95], "o", color=colour)
ax.axhline(0.95, color="grey", ls="--", lw=1)
ax.text(105, 0.925, "95% of plateau = 'formed'", va="center", ha="left", fontsize=9, color="grey")
ax.axvline(21, color="#DC2626", ls=":", lw=1.4)
ax.text(23, 0.08, "the '21 days' myth", color="#DC2626", fontsize=9)
ax.set_xlim(0, 300)
ax.set_ylim(0, 1.05)
ax.set_xlabel("Days of daily repetition")
ax.set_ylabel("Automaticity (fraction of its plateau)")
ax.set_title("A habit grows fast at first, then levels off")
ax.grid(alpha=0.3)
ax.legend(loc="lower right")
fig.tight_layout()
fig.savefig("images/fig_habit_curve.png", dpi=300)
