"""Figures for 'Predictive Coding - How the Brain May Learn Instead'.

Every data plot here comes from an actual simulation of the equations in the note
(linear predictive coding network, video's convention: top layer predicts the layer below).
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)

BLUE = "#2563eb"    # predictions / representational neurons
RED = "#dc2626"     # errors / error neurons
GREEN = "#16a34a"   # weight updates / learning
GRAY = "#6b7280"
DARK = "#111827"
AMBER = "#d97706"

plt.rcParams.update({
    "figure.dpi": 150, "savefig.bbox": "tight", "savefig.facecolor": "white",
    "font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titleweight": "bold",
})

def save(fig, name):
    fig.savefig(os.path.join(OUT, name))
    plt.close(fig)
    print("wrote", name)


# ---------------------------------------------------------------- 01 credit assignment
def fig_credit():
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.set_xlim(-0.5, 4.4); ax.set_ylim(-0.8, 4.0); ax.axis("off"); ax.set_aspect("equal")
    layers = [3, 4, 2]
    pos = {}
    for li, n in enumerate(layers):
        ys = np.linspace(0.3, 3.5, n) if n > 1 else [1.9]
        for j, y in enumerate(ys):
            pos[(li, j)] = (li * 1.4, y)
    for li in range(2):
        for a in range(layers[li]):
            for b in range(layers[li + 1]):
                (x1, y1), (x2, y2) = pos[(li, a)], pos[(li + 1, b)]
                ax.plot([x1, x2], [y1, y2], color=GRAY, lw=rng.uniform(0.4, 2.2), alpha=0.6, zorder=1)
    # label a few weights with "?"
    for (la, a, b) in [(0, 0, 1), (0, 2, 3), (1, 1, 0), (1, 3, 1), (0, 1, 2)]:
        (x1, y1), (x2, y2) = pos[(la, a)], pos[(la + 1, b)]
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, "?", color=AMBER, fontsize=14, fontweight="bold",
                ha="center", va="center", bbox=dict(boxstyle="circle,pad=0.1", fc="white", ec=AMBER))
    for (li, j), (x, y) in pos.items():
        ax.add_patch(Circle((x, y), 0.17, fc="white", ec=DARK, lw=1.5, zorder=3))
    ax.text(0, -0.45, "input\n(image pixels)", ha="center", fontsize=9)
    ax.text(1.4, -0.45, "hidden", ha="center", fontsize=9)
    ax.text(2.8, -0.45, "output", ha="center", fontsize=9)
    ax.annotate("", xy=(3.02, 3.5), xytext=(3.45, 3.5), arrowprops=dict(arrowstyle="-|>", color=RED, lw=2))
    ax.text(3.5, 3.5, "ERROR!\nsaid 'dog'\nbut it was 'cat'", color=RED, fontsize=9, fontweight="bold", va="center")
    ax.set_title("The credit assignment problem: the output is wrong — which of the many weights is to blame, and by how much?",
                 fontsize=10)
    save(fig, "01_credit_assignment.png")


# ---------------------------------------------------------------- 02 timelines
def fig_timeline():
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(9, 5.6), sharex=True)
    names = ["Layer 1 (input)", "Layer 2", "Layer 3", "Layer 4 (output)"]
    # backprop
    for i in range(4):
        a1.barh(i, 1, left=i, color=BLUE, alpha=0.85)                      # forward
        a1.barh(i, 7 - i - (i), left=i + 1, color="none", hatch="///", edgecolor=GRAY, lw=0)  # frozen
        a1.barh(i, 1, left=5 + (3 - i), color=RED, alpha=0.85)             # backward
        a1.barh(i, 0.8, left=9, color=GREEN, alpha=0.85)                   # update
    a1.barh(3, 1, left=4, color=AMBER, alpha=0.9)
    a1.set_yticks(range(4), names)
    a1.set_title("Backpropagation: strict phases, global clock, activity must be FROZEN while errors travel back")
    for x, t in [(2, "① forward"), (4.5, "② error"), (7.0, "③ backward\n(reverse order!)"), (9.4, "④ update")]:
        a1.text(x, 3.75, t, ha="center", va="bottom", fontsize=9, fontweight="bold")
    a1.set_ylim(-0.6, 4.7)
    a1.text(4.5, 0, "frozen: hold the forward snapshot, no new processing", fontsize=8, color=DARK,
            ha="center", va="center", bbox=dict(fc="white", ec=GRAY, pad=2))

    # predictive coding
    t = np.linspace(0, 10, 600)
    for i in range(4):
        base = i
        pred = base + 0.18 * np.sin(2.2 * t + i) * np.exp(-0.25 * t) + 0.05
        err = base - 0.18 * np.cos(2.7 * t + 2 * i) * np.exp(-0.35 * t) - 0.05
        a2.plot(t, pred, color=BLUE, lw=1.4)
        a2.plot(t, err, color=RED, lw=1.4)
        a2.fill_between(t, base - 0.33, base + 0.33, color=GREEN, alpha=0.07)
    a2.set_yticks(range(4), names)
    a2.set_ylim(-0.6, 4.0)
    a2.set_title("Predictive coding: every layer predicts, compares and learns at the same time (no phases, no clock)")
    a2.plot([], [], color=BLUE, label="prediction / activity"); a2.plot([], [], color=RED, label="prediction error")
    a2.fill_between([], [], [], color=GREEN, alpha=0.2, label="weights adapting continuously")
    a2.legend(loc="upper right", fontsize=8, ncol=3, frameon=False)
    a2.set_xlabel("time →")
    a2.set_xticks([])
    save(fig, "02_backprop_vs_pc_timeline.png")


# ---------------------------------------------------------------- 03 hierarchy
def fig_hierarchy():
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.set_xlim(0, 12); ax.set_ylim(-0.3, 7.0); ax.axis("off"); ax.set_aspect("equal")
    rows = [(0.6, "Layer 1 — raw sensory input (pixels)", "edges? light? dark?", True),
            (2.9, "Layer 2 — simple features", "edges, curves, textures", False),
            (5.2, "Layer 3 — abstract causes", "'whisker', 'ear', 'cat'", False)]
    for y, name, ex, clamped in rows:
        ax.add_patch(FancyBboxPatch((1.5, y), 5.2, 1.1, boxstyle="round,pad=0.05",
                                    fc="#e5e7eb" if clamped else "#eff6ff", ec=DARK, lw=1.3))
        for k in range(5):
            ax.add_patch(Circle((2.1 + k * 1.0, y + 0.55), 0.22, fc="white", ec=BLUE, lw=1.5))
        ax.text(7.0, y + 0.72, name, fontsize=9.5, fontweight="bold")
        ax.text(7.0, y + 0.3, ex, fontsize=9, color=GRAY, style="italic")
    for y0, y1 in [(5.2, 4.0), (2.9, 1.7)]:
        ax.annotate("", xy=(2.9, y1 + 0.02), xytext=(2.9, y0 - 0.02),
                    arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=3))
        ax.text(2.35, (y0 + y1) / 2, "prediction\n(top-down)", color=BLUE, ha="right", va="center", fontsize=9, fontweight="bold")
        ax.annotate("", xy=(5.3, y0 - 0.02), xytext=(5.3, y1 + 0.02),
                    arrowprops=dict(arrowstyle="-|>", color=RED, lw=3))
        ax.text(5.55, (y0 + y1) / 2, "prediction error\n(bottom-up)", color=RED, ha="left", va="center", fontsize=9, fontweight="bold")
    ax.text(0.2, 0.2, "clamped to\nthe world", fontsize=8, color=GRAY)
    ax.annotate("", xy=(4.1, 0.58), xytext=(4.1, -0.25), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=2))
    ax.text(4.25, -0.2, "sensory data", fontsize=8, color=GRAY)
    ax.set_title("Predictive coding hierarchy: predictions flow DOWN, only the surprises (errors) flow UP", fontsize=11)
    save(fig, "03_pc_hierarchy.png")


# ---------------------------------------------------------------- 04 springs & posts
def spring(ax, x, y0, y1, color, turns=7, width=0.12):
    n = turns * 2 + 1
    ys = np.linspace(y0, y1, n + 2)
    xs = [x] + [x + (width if k % 2 else -width) for k in range(n)] + [x]
    ax.plot(xs, ys, color=color, lw=1.6)

def fig_springs():
    fig, ax = plt.subplots(figsize=(9, 5.8))
    ax.set_xlim(-0.2, 10.5); ax.set_ylim(-0.5, 8.4); ax.axis("off")
    upper_x = [2.5, 6.5]
    upper_y = [6.6, 7.4]
    lower_x = [1.5, 4.5, 7.5]
    W = np.array([[0.55, 0.2], [0.35, 0.3], [0.1, 0.5]])  # prediction = W @ upper (scaled for drawing)
    base = 0.0
    actual = [4.2, 2.1, 5.2]
    for j, (x, y) in enumerate(zip(upper_x, upper_y)):
        ax.plot([x, x], [5.6, 8.2], color="#9ca3af", lw=4, solid_capstyle="round", zorder=0)
        ax.add_patch(Circle((x, y), 0.25, fc=BLUE, ec=DARK, zorder=5))
        ax.text(x + 0.35, y + 0.15, f"$x^{{(2)}}_{j+1}$", fontsize=11)
    for k, x in enumerate(lower_x):
        pred = base + 1.0 + 4.5 * (W[k] @ np.array([0.9, 1.0])) * 1.2
        ax.plot([x, x], [-0.2, 6.0], color="#9ca3af", lw=4, solid_capstyle="round", zorder=0)
        ax.add_patch(Rectangle((x - 0.45, pred - 0.06), 0.9, 0.12, fc=DARK, zorder=4))
        for j, ux in enumerate(upper_x):
            ax.plot([ux, x + (0.3 if ux > x else -0.3)], [upper_y[j] - 0.25, pred + 0.06],
                    color=GREEN, lw=1 + 3 * W[k, j], alpha=0.8, zorder=2)
        a = actual[k]
        spring(ax, x + 0.0, min(a, pred) + 0.2, max(a, pred) - 0.05, RED if abs(a - pred) > 0.4 else AMBER)
        ax.add_patch(Circle((x, a), 0.25, fc="white", ec=BLUE, lw=2.5, zorder=5))
        ax.text(x + 0.5, a, f"actual $x^{{(1)}}_{k+1}$", fontsize=9, va="center", color=BLUE)
        ax.text(x + 0.5, pred + 0.15, "prediction $\\mu$", fontsize=9, va="bottom", color=DARK)
        ax.annotate("", xy=(x - 0.6, a), xytext=(x - 0.6, pred),
                    arrowprops=dict(arrowstyle="<->", color=RED, lw=1.2))
        ax.text(x - 0.7, (a + pred) / 2, "$\\varepsilon$", color=RED, ha="right", va="center", fontsize=13)
    ax.text(9.1, 7.0, "upper layer\n(causes)", fontsize=9, color=GRAY)
    ax.text(9.1, 3.2, "lower layer", fontsize=9, color=GRAY)
    ax.text(0.0, -0.45,
            "● node height = neuron activity     ▬ platform = prediction from above (weighted sum)     "
            "green rods = weights (thicker = bigger)     spring energy = ½ ε²",
            fontsize=8.2, color=DARK)
    ax.set_title("The mechanical analogy: nodes on posts, platforms set by rods (weights), springs store ½·error²")
    save(fig, "04_springs_and_posts.png")


# ---------------------------------------------------------------- 05 energy landscape
def fig_energy():
    # A real 2-parameter PC energy: top activity fixed at 1, hidden x free, weights w (top->hidden fixed = 0.5)
    # and v (hidden->input) free, input clamped to 2:  E(x, v) = 1/2 (x - 0.5)^2 + 1/2 (2 - v x)^2
    X, V = np.meshgrid(np.linspace(-2.5, 3, 300), np.linspace(-4.5, 3.5, 300))
    E = 0.5 * (X - 0.5) ** 2 + 0.5 * (2 - V * X) ** 2
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    cs = ax.contourf(X, V, np.log1p(E), levels=30, cmap="viridis")
    ax.contour(X, V, np.log1p(E), levels=15, colors="white", linewidths=0.4, alpha=0.5)
    for (x, v), c in [((-1.8, -1.5), "#f97316"), ((2.6, -2.0), "#f472b6"), ((-2.0, 3.0), "white")]:
        path = [(x, v)]
        for _ in range(400):
            ex = x - 0.5; e0 = 2 - v * x
            dx = -ex + v * e0          # activity rule: -own error + weight * error below
            dv = e0 * x                # weight rule: error below * presynaptic activity
            x += 0.03 * dx; v += 0.03 * dv
            path.append((x, v))
        p = np.array(path)
        ax.plot(p[:, 0], p[:, 1], color=c, lw=2)
        ax.plot(*p[0], "o", color=c, ms=7, mec="black")
        ax.plot(*p[-1], "*", color=c, ms=14, mec="black")
    ax.set_xlabel("hidden activity  $x$")
    ax.set_ylabel("weight  $v$")
    ax.set_title("Energy landscape  $E=\\frac{1}{2}(x-0.5)^2+\\frac{1}{2}(2-v\\,x)^2$\n"
                 "balls (●) roll downhill using ONLY the local update rules and stop in the valley (★)", fontsize=10)
    cb = fig.colorbar(cs, ax=ax); cb.set_label("log(1 + energy)")
    save(fig, "05_energy_landscape.png")


# ---------------------------------------------------------------- PC network used for sims
def make_patterns():
    s = 7
    a = np.zeros((s, s)); a[0, :] = a[-1, :] = a[:, 0] = a[:, -1] = 1            # square ring
    b = np.zeros((s, s)); np.fill_diagonal(b, 1); np.fill_diagonal(np.fliplr(b), 1)  # X
    c = np.zeros((s, s)); c[s // 2, :] = 1; c[:, s // 2] = 1                      # plus
    return [a, b, c], ["□ ring", "✕ cross", "+ plus"]

PROTOS, PNAMES = make_patterns()

def sample(n):
    ys = rng.integers(0, 3, n)
    X = np.stack([PROTOS[y].ravel() for y in ys]).astype(float)
    flip = rng.random(X.shape) < 0.1
    X = np.abs(X - flip) + 0.25 * rng.standard_normal(X.shape)
    X = X / 3.0  # keep input vector norm ~1 so activities/weights stay in a sane range
    return X, ys

class PCNet:
    """Linear 3-layer predictive coding net.  x0 (input, 49) <- W1 x1 (hidden, 12) <- W2 x2 (label, 3)."""
    def __init__(self, n0=49, n1=12, n2=3, feedback_mode="tied", decay=0.005):
        self.W1 = 0.1 * rng.standard_normal((n0, n1))
        self.W2 = 0.1 * rng.standard_normal((n1, n2))
        self.B1 = 0.1 * rng.standard_normal((n0, n1))  # separate feedback synapse (used if untied)
        self.mode, self.decay = feedback_mode, decay

    def energy(self, x0, x1, x2):
        e0 = x0 - self.W1 @ x1; e1 = x1 - self.W2 @ x2
        return 0.5 * (e0 @ e0 + e1 @ e1)

    def relax(self, x0, x2=None, T=60, lr_x=0.1, learn=False, lr_w=0.0, clamp0=True, record=False):
        x1 = np.zeros(self.W1.shape[1])
        x2c = x2 is not None
        x2 = x2.copy() if x2c else np.zeros(self.W2.shape[1])
        x0 = x0.copy()
        hist = []
        # stable step size: the relaxation is gradient descent, so it must stay below 2 / curvature
        fb0 = self.W1 if self.mode == "tied" else self.B1
        lr_x = min(lr_x, 1.0 / (1.0 + np.linalg.norm(fb0, 2) ** 2 + np.linalg.norm(self.W2, 2) ** 2))
        for _ in range(T):
            e0 = x0 - self.W1 @ x1
            e1 = x1 - self.W2 @ x2
            fb = self.W1 if self.mode == "tied" else self.B1
            d1 = -e1 + fb.T @ e0
            d2 = self.W2.T @ e1
            if record:
                hist.append(dict(x1=x1.copy(), x2=x2.copy(), E=0.5 * (e0 @ e0 + e1 @ e1),
                                 own=-e1.copy(), below=(fb.T @ e0).copy()))
            x1 = x1 + lr_x * d1
            if not x2c: x2 = x2 + lr_x * d2
            if not clamp0: x0 = x0 + lr_x * (-e0)
            if learn:  # weights change continuously, alongside activities
                self.W1 += lr_w * (np.outer(e0, x1) - self.decay * self.W1)
                self.W2 += lr_w * (np.outer(e1, x2) - self.decay * self.W2)
                self.B1 += lr_w * (np.outer(e0, x1) - self.decay * self.B1)
        return x0, x1, x2, hist

def accuracy(net, n=300):
    X, ys = sample(n)
    pred = [np.argmax(net.relax(x, T=80)[2]) for x in X]
    return np.mean(np.array(pred) == ys)

CHECKPOINTS = [0, 4, 16, 64, 256, 600]

def generate(net, k):
    return net.relax(np.zeros(49), np.eye(3)[k], T=300, clamp0=False)[0]

def train(net, lr_w=0.01):
    """Online training: one example at a time, activities and weights change together."""
    E_seen, acc, gens, seen = [], [], {}, 0
    for cp in CHECKPOINTS:
        if cp > seen:
            X, ys = sample(cp - seen)
            for x, y in zip(X, ys):
                _, x1, x2, _ = net.relax(x, np.eye(3)[y], T=40, learn=True, lr_w=lr_w)
                E_seen.append(net.energy(x, x1, x2))
            seen = cp
        acc.append(accuracy(net, 300))
        gens[cp] = [generate(net, k) for k in range(3)]
    return E_seen, acc, gens


# ---------------------------------------------------------------- 06 relaxation dynamics
def fig_relaxation(net):
    X, ys = sample(1)
    _, _, _, h = net.relax(X[0], np.eye(3)[ys[0]], T=60, record=True)
    x1 = np.array([s["x1"] for s in h]); E = np.array([s["E"] for s in h])
    own = np.array([s["own"] for s in h]); below = np.array([s["below"] for s in h])
    i = int(np.argmax(np.abs(x1[-1])))
    fig, axs = plt.subplots(1, 3, figsize=(12, 3.6))
    axs[0].plot(E, color=DARK, lw=2); axs[0].set_title("① total energy goes down")
    axs[0].set_xlabel("relaxation step"); axs[0].set_ylabel("E = ½ Σ ε²")
    axs[1].plot(x1, lw=1.2); axs[1].set_title("② hidden activities settle")
    axs[1].set_xlabel("relaxation step"); axs[1].set_ylabel("$x^{(1)}_i$")
    axs[2].plot(own[:, i], color=RED, lw=2, label="pull to own prediction  $-\\varepsilon_i$")
    axs[2].plot(below[:, i], color=BLUE, lw=2, label="pull to explain layer below  $\\sum_k w_{ki}\\varepsilon_k$")
    axs[2].plot(own[:, i] + below[:, i], color=GREEN, lw=2, ls="--", label="net change  $\\Delta x_i$")
    axs[2].axhline(0, color=GRAY, lw=0.8)
    axs[2].set_title(f"③ tug-of-war for one neuron (#{i}) → balance")
    axs[2].set_xlabel("relaxation step"); axs[2].legend(fontsize=7.5, frameon=False)
    fig.suptitle("Inference = relaxation: input and label clamped, a trained network settles to an energy minimum",
                 fontweight="bold", y=1.03)
    fig.tight_layout()
    save(fig, "06_relaxation_dynamics.png")


# ---------------------------------------------------------------- 07 circuit
def fig_circuit():
    fig, ax = plt.subplots(figsize=(8.5, 6.5))
    ax.set_xlim(0, 10.5); ax.set_ylim(0, 9.4); ax.axis("off"); ax.set_aspect("equal")
    rows = {"L+1": 7.6, "L": 4.6, "L-1": 1.6}
    xr, xe = 3.0, 6.6
    def rep(y, lab):
        ax.add_patch(Circle((xr, y), 0.55, fc="#dbeafe", ec=BLUE, lw=2, zorder=3))
        ax.text(xr, y, lab, ha="center", va="center", fontsize=12, zorder=4)
    def err(y, lab):
        ax.add_patch(Polygon([[xe - 0.6, y - 0.45], [xe + 0.6, y - 0.45], [xe, y + 0.6]], closed=True,
                             fc="#fee2e2", ec=RED, lw=2, zorder=3))
        ax.text(xe, y - 0.1, lab, ha="center", va="center", fontsize=12, zorder=4)
    for name, y in rows.items():
        sup = {"L+1": "(L+1)", "L": "(L)", "L-1": "(L-1)"}[name]
        rep(y, f"$x^{{{sup}}}$"); err(y, f"$\\varepsilon^{{{sup}}}$")
        ax.text(0.2, y, f"layer {name}", fontsize=10, color=GRAY, va="center")

    def conn(p0, p1, kind, rad=0.0, label=None, lpos=None, color=None):
        color = color or (GREEN if kind == "exc" else "#7c3aed")
        style = "-|>" if kind == "exc" else "-"
        ax.annotate("", xy=p1, xytext=p0, zorder=2,
                    arrowprops=dict(arrowstyle=style, color=color, lw=2, connectionstyle=f"arc3,rad={rad}",
                                    shrinkA=2, shrinkB=2))
        if kind == "inh":
            ax.plot(*p1, "o", color=color, ms=9, zorder=5)
        if label:
            ax.text(*lpos, label, fontsize=8.5, color=color, ha="center", va="center",
                    bbox=dict(fc="white", ec="none", pad=1))
    yL, yU, yD = rows["L"], rows["L+1"], rows["L-1"]
    # own error neuron compares actual (exc) with prediction from above (inh)
    conn((xr + 0.55, yL + 0.15), (xe - 0.5, yL + 0.15), "exc", label="actual activity (+)", lpos=(4.8, yL + 0.45))
    conn((xr + 0.45, yU - 0.35), (xe - 0.25, yL + 0.5), "inh", label="prediction $Wx^{(L+1)}$ (−)", lpos=(4.25, 6.35))
    # error inhibits its own rep neuron
    conn((xe - 0.5, yL - 0.25), (xr + 0.5, yL - 0.25), "inh", label="$-\\varepsilon^{(L)}$ pulls x back", lpos=(4.8, yL - 0.55))
    # error from below excites rep neuron (via weights)
    conn((xe - 0.4, yD + 0.35), (xr + 0.35, yL - 0.45), "exc", rad=-0.0,
         label="$+\\sum_k w_{ki}\\varepsilon^{(L-1)}_k$", lpos=(5.3, 3.35))
    # rep neuron predicts layer below (inhibits lower error)
    conn((xr, yL - 0.55), (xe - 0.35, yD + 0.1), "inh", rad=0.25, label="prediction (−)", lpos=(3.6, 2.6))
    # error at L excites rep L+1
    conn((xe + 0.15, yL + 0.6), (xr + 0.55, yU - 0.1), "exc", rad=0.25, label="error up (+)", lpos=(6.9, 6.3))
    ax.plot([], [], color=GREEN, lw=2, marker=">", label="excitatory (+)")
    ax.plot([], [], color="#7c3aed", lw=2, marker="o", label="inhibitory (−)")
    ax.add_patch(Circle((8.3, 8.9), 0.18, fc="#dbeafe", ec=BLUE)); ax.text(8.6, 8.9, "representational neuron", va="center", fontsize=8.5)
    ax.add_patch(Polygon([[8.12, 8.25], [8.48, 8.25], [8.3, 8.6]], fc="#fee2e2", ec=RED)); ax.text(8.6, 8.4, "error neuron", va="center", fontsize=8.5)
    ax.legend(loc="lower right", fontsize=8.5, frameon=False)
    ax.set_title("The predictive coding micro-circuit read directly off the equations\n"
                 "(shown for the middle layer; every layer repeats this motif)", fontsize=11)
    save(fig, "07_error_neuron_circuit.png")


# ---------------------------------------------------------------- 08 training results
def fig_training(net, E_seen, acc, gens):
    fig = plt.figure(figsize=(12, 8.2))
    gs = fig.add_gridspec(4, 7, height_ratios=[1.5, 1, 1, 1], hspace=0.7)
    a = fig.add_subplot(gs[0, 0:3]); b = fig.add_subplot(gs[0, 4:7])
    E = np.array(E_seen); w = 20
    a.plot(np.arange(1, len(E) + 1), E, color=GRAY, lw=0.6, alpha=0.5, label="per example")
    a.plot(np.arange(w, len(E) + 1), np.convolve(E, np.ones(w) / w, "valid"), color=DARK, lw=2, label="moving average")
    a.set_title("Energy left after relaxing (training)"); a.set_xlabel("training examples seen"); a.set_ylabel("energy")
    a.legend(frameon=False, fontsize=8)
    xs = [max(c, 1) for c in CHECKPOINTS]
    b.plot(xs, np.array(acc) * 100, color=GREEN, lw=2, marker="o")
    b.set_xscale("log"); b.set_xticks(xs, [str(c) for c in CHECKPOINTS])
    b.axhline(100 / 3, color=GRAY, ls="--", lw=1); b.text(1.1, 37, "chance", color=GRAY, fontsize=8)
    b.set_ylim(0, 105); b.set_title("Test accuracy (clamp input only → read top)")
    b.set_xlabel("training examples seen"); b.set_ylabel("accuracy %")
    for k in range(3):
        for j, cp in enumerate(CHECKPOINTS):
            ax = fig.add_subplot(gs[k + 1, j])
            ax.imshow(gens[cp][k].reshape(7, 7), cmap="gray_r"); ax.set_xticks([]); ax.set_yticks([])
            if k == 0: ax.set_title(f"imagined after\n{cp} examples", fontsize=8.5)
            if j == 0: ax.set_ylabel(f"clamp\n'{PNAMES[k]}'", fontsize=9)
    X, ys = sample(1)
    _, x1, x2, _ = net.relax(X[0], T=80)
    ax = fig.add_subplot(gs[1, 6]); ax.imshow(X[0].reshape(7, 7), cmap="gray_r"); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("noisy input", fontsize=9)
    ax = fig.add_subplot(gs[2, 6]); ax.imshow((net.W1 @ x1).reshape(7, 7), cmap="gray_r"); ax.set_xticks([]); ax.set_yticks([])
    ax.set_title("its prediction", fontsize=9)
    ax = fig.add_subplot(gs[3, 6]); ax.bar(range(3), x2, color=[BLUE if i == np.argmax(x2) else GRAY for i in range(3)])
    ax.set_xticks(range(3), ["ring", "cross", "plus"], fontsize=7); ax.set_title("top layer", fontsize=9)
    fig.suptitle("A real predictive coding network trained with ONLY local rules on noisy 7×7 shapes", fontweight="bold", y=0.95)
    save(fig, "08_training_results.png")


# ---------------------------------------------------------------- 09 weight transport
def angle(A, B):
    c = np.sum(A * B) / (np.linalg.norm(A) * np.linalg.norm(B))
    return np.degrees(np.arccos(np.clip(c, -1, 1)))

def fig_transport():
    res = {}
    for decay in [0.0, 0.005]:
        net = PCNet(feedback_mode="untied", decay=decay)
        net.B1 = 0.3 * rng.standard_normal(net.B1.shape)  # start deliberately different
        angs, accs, gaps = [angle(net.W1, net.B1)], [], [np.linalg.norm(net.W1 - net.B1)]
        for ep in range(30):
            X, ys = sample(100)
            for x, y in zip(X, ys):
                net.relax(x, np.eye(3)[y], T=40, learn=True, lr_w=0.01)
            angs.append(angle(net.W1, net.B1)); gaps.append(np.linalg.norm(net.W1 - net.B1))
            accs.append(accuracy(net, 150))
        res[decay] = (angs, gaps, accs)
    fig, axs = plt.subplots(1, 2, figsize=(10, 3.8))
    for decay, c, lab in [(0.0, RED, "no weight decay"), (0.005, GREEN, "with weight decay (λ=0.005)")]:
        angs, gaps, accs = res[decay]
        axs[0].plot(angs, color=c, lw=2, label=lab)
        axs[1].plot(gaps, color=c, lw=2, label=lab)
    axs[0].set_title("angle between forward W and feedback B"); axs[0].set_ylabel("degrees"); axs[0].set_xlabel("epoch")
    axs[1].set_title("‖W − B‖  (the mismatch)"); axs[1].set_xlabel("epoch")
    for a in axs: a.legend(fontsize=8, frameon=False)
    fig.suptitle("Weight transport: two physically separate synapses with the same local Hebbian rule become aligned",
                 fontweight="bold", y=1.03)
    fig.tight_layout()
    save(fig, "09_weight_transport.png")
    return res


# ---------------------------------------------------------------- 10 clamping modes
def fig_clamping():
    fig, axs = plt.subplots(1, 4, figsize=(12, 4))
    modes = [
        ("Nothing clamped", [False, False, False], "free", "all activities → 0\nenergy = 0\n(useless!)"),
        ("Supervised TRAINING", [True, False, True], "learn", "input + label fixed\nweights LEARN the\nmapping"),
        ("CLASSIFICATION", [True, False, False], "frozen", "input fixed\nweights frozen\nread label on top"),
        ("GENERATION", [False, False, True], "frozen", "label fixed\nweights frozen\nread 'imagined' input"),
    ]
    names = ["input (bottom)", "hidden", "label (top)"]
    for ax, (title, cl, w, note) in zip(axs, modes):
        ax.set_xlim(0, 4); ax.set_ylim(-1.8, 3.6); ax.axis("off")
        for li in range(3):
            y = li * 1.1
            fc = "#9ca3af" if cl[li] else "white"
            ax.add_patch(FancyBboxPatch((0.4, y), 3.2, 0.7, boxstyle="round,pad=0.03", fc=fc, ec=DARK, lw=1.3))
            ax.text(2.0, y + 0.35, names[li] + (" [clamped]" if cl[li] else ""), ha="center", va="center", fontsize=9,
                    fontweight="bold" if cl[li] else "normal")
        wc = {"learn": GREEN, "frozen": GRAY, "free": AMBER}[w]
        ax.text(2.0, -0.45, f"weights: {w}", ha="center", color=wc, fontsize=9, fontweight="bold")
        ax.text(2.0, -1.3, note, ha="center", va="center", fontsize=8.5, color=DARK)
        ax.set_title(title, fontsize=10, fontweight="bold")
    fig.suptitle("Clamping decides the task (gray = clamped to a fixed value)", fontweight="bold")
    save(fig, "10_clamping_modes.png")


# ---------------------------------------------------------------- run
if __name__ == "__main__":
    fig_credit(); fig_timeline(); fig_hierarchy(); fig_springs(); fig_energy(); fig_circuit(); fig_clamping()
    print("initial accuracy", accuracy(PCNet(), 150))
    net = PCNet()
    E_seen, acc, gens = train(net)
    print("accuracy at checkpoints", CHECKPOINTS, np.round(acc, 3))
    fig_relaxation(net)
    fig_training(net, E_seen, acc, gens)
    res = fig_transport()
    for d, (angs, gaps, accs) in res.items():
        print(f"decay={d}: angle {angs[0]:.1f} -> {angs[-1]:.1f}, gap {gaps[0]:.2f} -> {gaps[-1]:.2f}, acc {accs[-1]:.2f}")
