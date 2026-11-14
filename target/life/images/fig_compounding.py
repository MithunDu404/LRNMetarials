import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def fv(pmt, rate, years):
    r = rate / 12
    n = years * 12
    return pmt * ((1 + r) ** n - 1) / r


years = np.arange(0, 30.01, 0.25)
early = [fv(100, 0.07, y) for y in years]
late = [fv(100, 0.07, y - 10) if y >= 10 else 0 for y in years]
paid_early = [100 * 12 * y for y in years]

fig, ax = plt.subplots(figsize=(8, 4.6), facecolor="white")
ax.plot(years, early, color="#059669", lw=2.4, label="Asha: starts at 22, invests 100/month")
ax.plot(years, late, color="#D97706", lw=2.4, label="Ravi: starts at 32, invests 100/month")
ax.plot(years, paid_early, color="grey", ls="--", lw=1.4, label="Money Asha actually put in")
ax.annotate("122,000", (30, 121997), textcoords="offset points", xytext=(-55, 6), color="#059669")
ax.annotate("52,100", (30, 52093), textcoords="offset points", xytext=(-48, 6), color="#D97706")
ax.annotate("36,000", (30, 36000), textcoords="offset points", xytext=(-48, -16), color="grey")
ax.set_ylim(-3000, 138000)
ax.set_xlabel("Years from age 22")
ax.set_ylabel("Value (any currency)")
ax.set_title("Same habit, 10 years later: less than half the result (7% a year)")
ax.grid(alpha=0.3)
ax.legend(loc="upper left")
fig.tight_layout()
fig.savefig("images/fig_compounding.png", dpi=300)
