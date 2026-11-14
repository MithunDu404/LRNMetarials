"""Extra plots for the Life guides. Run from target/life:  py -3.12 images/fig_extra_plots.py"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BLUE, GREEN, AMBER, RED, PURPLE, GREY = "#2563EB", "#059669", "#D97706", "#DC2626", "#7C3AED", "#6B7280"


def style(ax, title, xl, yl):
    ax.set_title(title)
    ax.set_xlabel(xl)
    ax.set_ylabel(yl)
    ax.grid(alpha=0.3)


# 1. Guide 1: 1% better vs 1% worse each day --------------------------------------------
d = np.arange(0, 366)
fig, ax = plt.subplots(figsize=(8, 4.6), facecolor="white")
ax.plot(d, 1.01 ** d, color=GREEN, lw=2.4, label="1% better each day: 1.01ⁿ")
ax.plot(d, np.ones_like(d, dtype=float), color=GREY, ls="--", lw=1.4, label="No change: 1")
ax.plot(d, 0.99 ** d, color=RED, lw=2.4, label="1% worse each day: 0.99ⁿ")
ax.set_yscale("log")
ax.set_ylim(0.01, 100)
ax.annotate("≈ 37.8", (365, 1.01 ** 365), textcoords="offset points", xytext=(-48, 6), color=GREEN)
ax.annotate("≈ 0.026", (365, 0.99 ** 365), textcoords="offset points", xytext=(-60, -20), color=RED)
ax.annotate("Day 30: 1.35 vs 0.74\n(easy to ignore)", (30, 1.01 ** 30), textcoords="offset points",
            xytext=(10, 28), fontsize=9, color=GREY, arrowprops=dict(arrowstyle="->", color=GREY))
style(ax, "Small daily differences seem minor for a month, then become huge", "Days", "Value (log scale)")
ax.legend(loc="upper left")
fig.tight_layout()
fig.savefig("images/fig_one_percent.png", dpi=300)
plt.close(fig)

# 2. Guide 2: an emotion wave, with and without dwelling (schematic) ----------------------
t = np.linspace(0, 60, 1200)


def wave(t0, peak=1.0, rise=1.5, decay=6.0):
    x = np.clip(t - t0, 0, None)
    return peak * (x / rise) * np.exp(1 - x / rise) * (x <= rise) + peak * np.exp(-(x - rise) / decay) * (x > rise)


once = wave(2)
dwell = np.maximum.reduce([wave(2), wave(14, 0.95), wave(26, 0.9), wave(38, 0.92), wave(50, 0.88)])
fig, ax = plt.subplots(figsize=(8, 4.4), facecolor="white")
ax.plot(t, dwell, color=RED, lw=2.2, label="Dwelling: each replay restarts the wave")
ax.plot(t, once, color=GREEN, lw=2.6, label="Felt fully once, then let go")
for x0 in (14, 26, 38, 50):
    ax.annotate("replay", (x0 + 1.5, 0.95), textcoords="offset points", xytext=(-6, 10), fontsize=8, color=RED, ha="center")
ax.set_ylim(0, 1.2)
ax.set_xlim(0, 60)
style(ax, "An emotion is a wave; dwelling keeps restarting it (illustration, not measured data)",
      "Minutes after the trigger", "Intensity")
ax.title.set_fontsize(10.5)
ax.legend(loc="upper right", fontsize=9)
fig.tight_layout()
fig.savefig("images/fig_emotion_wave.png", dpi=300)
plt.close(fig)

# 3. Guide 2: cyclic sighing, lung volume over two breaths (schematic timing) -------------
seg = []  # (duration s, start volume, end volume, label)
for _ in range(2):
    seg += [(2.0, 0.0, 0.75, "inhale"), (0.8, 0.75, 1.0, "top-up"), (6.0, 1.0, 0.0, "long exhale")]
ts, vs, t0 = [], [], 0.0
for dur, a, b, _ in seg:
    tt = np.linspace(0, dur, 200)
    ts.append(t0 + tt)
    vs.append(a + (b - a) * (0.5 - 0.5 * np.cos(np.pi * tt / dur)))
    t0 += dur
fig, ax = plt.subplots(figsize=(8, 3.8), facecolor="white")
ax.plot(np.concatenate(ts), np.concatenate(vs), color=BLUE, lw=2.6)
t0 = 0.0
for i, (dur, a, b, lab) in enumerate(seg[:3]):
    col = {"inhale": GREEN, "top-up": PURPLE, "long exhale": AMBER}[lab]
    ax.axvspan(t0, t0 + dur, color=col, alpha=0.12)
    ax.text(t0 + dur / 2, 1.22 if lab == "top-up" else 1.06, {"inhale": "1 · Inhale\n(nose)", "top-up": "2 · Short\ntop-up", "long exhale": "3 · Slow, long exhale (mouth)"}[lab],
            ha="center", va="bottom", fontsize=9, color=col)
    t0 += dur
ax.set_ylim(-0.05, 1.5)
ax.set_xlim(0, t0 * 2)
ax.set_yticks([0, 1])
ax.set_yticklabels(["empty", "full"])
style(ax, "Cyclic sighing: two inhales, then an exhale longer than both (timing is illustrative)",
      "Seconds", "Air in lungs")
ax.title.set_fontsize(10.5)
fig.tight_layout()
fig.savefig("images/fig_cyclic_sigh.png", dpi=300)
plt.close(fig)

# 4. Guide 2: Kjaervik & Bushman (2024) pooled effects with 95% CIs ------------------------
labels = ["Arousal-DEcreasing\n(slow breathing, meditation,\nslow yoga, time-out)", "Arousal-INcreasing\n(venting, running,\nhitting a bag)"]
g = [-0.63, -0.02]
lo = [-0.82, -0.13]
hi = [-0.43, 0.09]
fig, ax = plt.subplots(figsize=(8, 3.6), facecolor="white")
y = [1, 0]
for yi, gi, l, h, c in zip(y, g, lo, hi, [GREEN, RED]):
    ax.plot([l, h], [yi, yi], color=c, lw=3)
    ax.plot(gi, yi, "o", color=c, ms=11)
    ax.annotate(f"g = {gi:+.2f}  [{l:+.2f}, {h:+.2f}]", (gi, yi), textcoords="offset points", xytext=(0, 13) if gi < -0.3 else (-12, 13), ha="center" if gi < -0.3 else "right", color=c, fontsize=10)
ax.axvline(0, color=GREY, ls="--")
ax.text(0.01, -0.45, "no effect", color=GREY, fontsize=9)
ax.text(-0.95, -0.45, "← anger and aggression go DOWN", color=GREEN, fontsize=9)
ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=9)
ax.set_xlim(-1.0, 0.3)
ax.set_ylim(-0.6, 1.6)
style(ax, "154 studies, 10,189 people: calming works, venting doesn't", "Effect on anger and aggression (Hedges' g, 95% CI)", "")
fig.tight_layout()
fig.savefig("images/fig_anger_meta.png", dpi=300)
plt.close(fig)

# 5. Guide 4: credit-card debt of 1,000 at 3% a month ---------------------------------------
fig, ax = plt.subplots(figsize=(8, 4.4), facecolor="white")
for pay, col in [(30, RED), (40, AMBER), (100, GREEN)]:
    bal, xs, ys = 1000.0, [0], [1000.0]
    for m in range(1, 61):
        bal = bal * 1.03 - pay
        if bal <= 0:
            xs.append(m); ys.append(0.0)
            break
        xs.append(m); ys.append(bal)
    lab = {30: "Pay 30/month: never ends (30 = the interest)", 40: "Pay 40/month: 47 months, ≈876 interest",
           100: "Pay 100/month: 13 months, ≈207 interest"}[pay]
    ax.plot(xs, ys, color=col, lw=2.4, label=lab)
ax.set_ylim(0, 1150)
ax.set_xlim(0, 60)
style(ax, "1,000 owed on a card at 36% a year (3% a month)", "Months", "Balance still owed")
ax.legend(loc="upper right", bbox_to_anchor=(1, 0.8), fontsize=9)
fig.tight_layout()
fig.savefig("images/fig_debt.png", dpi=300)
plt.close(fig)

# 6. Guide 4: happiness rises with the log of income (schematic) ---------------------------
inc = np.linspace(10_000, 200_000, 800)
h = np.log2(inc / 10_000)
fig, ax = plt.subplots(figsize=(8, 4.4), facecolor="white")
ax.plot(inc / 1000, h, color=BLUE, lw=2.6)
for a, b, col, off in [(20_000, 40_000, GREEN, (6, -14)), (50_000, 100_000, PURPLE, (6, -16)), (100_000, 110_000, AMBER, (-30, 14))]:
    ha, hb = math.log2(a / 10_000), math.log2(b / 10_000)
    ax.plot([a / 1000, b / 1000], [ha, ha], color=col, lw=2)
    ax.plot([b / 1000, b / 1000], [ha, hb], color=col, lw=2)
    ax.annotate(f"{a // 1000}k → {b // 1000}k: +{hb - ha:.2f}", (b / 1000, hb), textcoords="offset points",
                xytext=off, color=col, fontsize=9)
style(ax, "Each doubling of income adds the same happiness (log model, illustration)",
      "Yearly income (thousands, any currency)", "Happiness (units = doublings)")
fig.tight_layout()
fig.savefig("images/fig_log_income.png", dpi=300)
plt.close(fig)
print("done")
