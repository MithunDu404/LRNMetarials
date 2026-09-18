"""Figures for 'Backpropagation - How Neural Networks Learn'.
Every data plot is produced by actually running the algorithm described in the note.
Run:  python figures/backprop/make_figs.py
"""
import sys, os, time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _style import *

OUT = out_dir(__file__)
rng = np.random.default_rng(3)

# shared dataset: noisy samples of a wiggly function on [-1, 1]
N = 14
X = np.sort(rng.uniform(-1, 1, N))
TRUE = lambda x: 0.6 * np.sin(3.2 * x) + 0.3 * x ** 2
Y = TRUE(X) + rng.normal(0, 0.08, N)
POW = np.stack([X ** p for p in range(6)], 1)  # (N, 6)


def poly(k, x):
    return sum(k[p] * x ** p for p in range(6))


def loss(k):
    return float(np.sum((Y - POW @ k) ** 2))


def grad(k):
    return -2 * POW.T @ (Y - POW @ k)


def run_gd(k0, lr, steps, record=()):
    k = k0.copy(); hist = []; snaps = {}
    for t in range(steps + 1):
        if t in record:
            snaps[t] = k.copy()
        hist.append(loss(k))
        k -= lr * grad(k)
    return k, np.array(hist), snaps


K_INIT = rng.normal(0, 0.6, 6)
xs = np.linspace(-1.05, 1.05, 300)


# ------------------------------------------------------------------ 01 curve fitting
def fig_curve_fitting():
    k_fit, _, _ = run_gd(K_INIT, 0.02, 40000)
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.8), sharey=True)
    for ax, k, title, col in [(axes[0], K_INIT, "Random knob settings", RED),
                              (axes[1], k_fit, "After gradient descent", GREEN)]:
        pred = POW @ k
        for xi, yi, pi in zip(X, Y, pred):
            ax.plot([xi, xi], [yi, pi], color=AMBER, lw=1.2, zorder=1)
        ax.plot(xs, poly(k, xs), color=col, lw=2.2, label="curve  y(x)")
        ax.scatter(X, Y, color=DARK, s=22, zorder=3, label="data points")
        ax.set_title(f"{title}\nloss L = sum of squared gaps = {loss(k):.3f}")
        ax.set_xlabel("x"); ax.set_ylim(-1.6, 1.6)
    axes[0].set_ylabel("y")
    axes[0].plot([], [], color=AMBER, lw=1.2, label="gap (y - ŷ), gets squared")
    axes[0].legend(loc="lower right", fontsize=8)
    fig.suptitle("Curve fitting: turn six knobs k0..k5 until the total squared gap is as small as possible",
                 fontsize=11, weight="bold", y=1.09)
    save(fig, OUT, "01_curve_fitting.png")


# ------------------------------------------------------------------ 02 derivative as limit of secants
def fig_derivative():
    f = lambda x: 0.6 * (x - 1.5) ** 2 + 0.5
    df = lambda x: 1.2 * (x - 1.5)
    x0 = 0.0
    xx = np.linspace(-1, 3.2, 300)
    fig, ax = plt.subplots(figsize=(7.5, 4.2))
    ax.plot(xx, f(xx), color=DARK, lw=2.2, label="loss as a function of one knob")
    for dx, c in [(2.0, "#fca5a5"), (1.0, "#f87171"), (0.3, RED)]:
        x1 = x0 + dx
        slope = (f(x1) - f(x0)) / dx
        ax.plot(xx, f(x0) + slope * (xx - x0), color=c, lw=1.2, ls="--",
                label=f"secant, Δx = {dx}: slope Δy/Δx = {slope:+.2f}")
        ax.scatter([x1], [f(x1)], color=c, s=22, zorder=4)
    ax.plot(xx, f(x0) + df(x0) * (xx - x0), color=BLUE, lw=2.2,
            label=f"tangent (Δx → 0): derivative = {df(x0):+.2f}")
    ax.scatter([x0], [f(x0)], color=BLUE, s=45, zorder=5)
    ax.annotate("current knob value\n(slope is negative → turn knob RIGHT)", (x0, f(x0)), (-0.95, 0.35),
                fontsize=9, arrowprops=dict(arrowstyle="->", color=GRAY))
    ax.set_ylim(-0.5, 3.4); ax.set_xlim(-1, 3.2)
    ax.set_xlabel("knob value k"); ax.set_ylabel("loss L(k)")
    ax.set_title("A derivative is the slope you get as the nudge Δx shrinks to zero")
    ax.legend(fontsize=8, loc="upper right")
    save(fig, OUT, "02_derivative_secant.png")


# ------------------------------------------------------------------ 03 1-D gradient descent & learning rates
def fig_learning_rates():
    bowl = lambda x: (x - 0.5) ** 2 + 0.5
    dbowl = lambda x: 2 * (x - 0.5)
    bumpy = lambda x: 0.25 * x ** 4 - 0.5 * x ** 2 + 0.25 * x + 1.2
    dbumpy = lambda x: x ** 3 - x + 0.25
    fig, axes = plt.subplots(1, 4, figsize=(15, 3.7))
    cases = [(bowl, dbowl, 0.05, 2.3, "Too small (η = 0.05)\nslow crawl: 12 steps, still far"),
             (bowl, dbowl, 0.35, 2.3, "Good (η = 0.35)\nreaches the bottom quickly"),
             (bowl, dbowl, 1.05, 1.0, "Too large (η = 1.05)\neach jump overshoots MORE → diverges"),
             (bumpy, dbumpy, 0.1, 1.7, "Bumpy loss (η = 0.1)\nstuck in a local valley")]
    for ax, (f, df, lr, x, title) in zip(axes, cases):
        path = [x]
        for _ in range(12):
            x = x - lr * df(x); path.append(x)
        path = np.array(path)
        lo, hi = min(path.min(), -1.9) - 0.2, max(path.max(), 2.4) + 0.2
        xx = np.linspace(lo, hi, 300)
        ax.plot(xx, f(xx), color=DARK, lw=2)
        ax.plot(path, f(path), color=RED, lw=1, alpha=0.5)
        ax.scatter(path, f(path), c=np.linspace(0.2, 1, len(path)), cmap="Reds", s=30, zorder=4,
                   edgecolor=DARK, linewidth=0.4)
        ax.scatter([path[0]], [f(path[0])], marker="*", s=180, color=AMBER, zorder=5, label="start")
        ax.set_title(title, fontsize=10); ax.set_xlabel("knob k")
        ax.set_ylim(0, min(f(xx).max(), 12))
    axes[0].set_ylabel("loss L(k)"); axes[0].legend(loc="upper center")
    fig.suptitle("Gradient descent:  k ← k − η · dL/dk      (η = learning rate, darker dots = later steps)",
                 weight="bold", y=1.07)
    save(fig, OUT, "03_gd_learning_rates.png")


# ------------------------------------------------------------------ 04 gradient field in 2-D
def fig_gradient_2d():
    # only k0 (offset) and k1 (slope) free, fit a line to straight-ish data
    x = np.linspace(-1, 1, 12); y = 0.8 * x + 0.3 + rng.normal(0, 0.12, 12)
    L = lambda a, b: np.sum((y[None, None, :] - (a[..., None] + b[..., None] * x[None, None, :])) ** 2, -1)
    a = np.linspace(-1.5, 2, 200); b = np.linspace(-1.5, 3, 200)
    A, B = np.meshgrid(a, b)
    Z = L(A, B)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.4), gridspec_kw=dict(width_ratios=[1.15, 1]))
    ax = axes[0]
    cs = ax.contourf(A, B, Z, levels=30, cmap="viridis_r", alpha=0.85)
    ax.contour(A, B, Z, levels=15, colors="white", linewidths=0.4, alpha=0.6)
    ga, gb = np.meshgrid(np.linspace(-1.3, 1.8, 9), np.linspace(-1.2, 2.7, 9))
    GA = np.array([[-2 * np.sum(y - (p + q * x)) for p, q in zip(r1, r2)] for r1, r2 in zip(ga, gb)])
    GB = np.array([[-2 * np.sum((y - (p + q * x)) * x) for p, q in zip(r1, r2)] for r1, r2 in zip(ga, gb)])
    mag = np.hypot(GA, GB) + 1e-9
    ax.quiver(ga, gb, -GA / mag, -GB / mag, color="white", scale=22, width=0.004, alpha=0.9)
    p = np.array([-1.2, 2.6]); path = [p.copy()]
    for _ in range(40):
        g = np.array([-2 * np.sum(y - (p[0] + p[1] * x)), -2 * np.sum((y - (p[0] + p[1] * x)) * x)])
        p = p - 0.03 * g; path.append(p.copy())
    path = np.array(path)
    ax.plot(path[:, 0], path[:, 1], color=RED, lw=2, marker="o", ms=3, label="gradient-descent path")
    ax.scatter(*path[0], marker="*", s=200, color=AMBER, zorder=5, label="start")
    ax.set_xlabel("k0 (offset)"); ax.set_ylabel("k1 (slope)")
    ax.set_title("Loss surface seen from above\nwhite arrows = −gradient (the downhill direction)")
    ax.legend(loc="lower right", fontsize=8)
    fig.colorbar(cs, ax=ax, label="loss")
    ax = axes[1]
    ax.scatter(x, y, color=DARK, s=22, zorder=3)
    for i, c in zip([0, 3, 8, 40], ["#fecaca", "#f87171", RED, GREEN]):
        ax.plot([-1, 1], [path[i, 0] - path[i, 1], path[i, 0] + path[i, 1]], color=c, lw=2,
                label=f"step {i}: L = {float(np.sum((y - path[i,0] - path[i,1]*x)**2)):.2f}")
    ax.set_title("The same steps, shown as fitted lines"); ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.legend(fontsize=8)
    save(fig, OUT, "04_gradient_2d.png")


# ------------------------------------------------------------------ 05 chain rule with numbers
def fig_chain_rule():
    fig, ax = canvas(12, 3.8, (0, 12), (0, 3.8))
    x = 1.5; j = x ** 2; f = np.sin(j); dj = 2 * x; df = np.cos(j)
    box(ax, 0.1, 1.5, 1.6, 1.0, f"input\nx = {x}", fc="#eff6ff", ec=BLUE, fs=10)
    box(ax, 2.6, 1.5, 2.8, 1.0, "machine 1:  j(x) = x²\nlocal slope j'(x) = 2x = 3.0", fs=9.5)
    box(ax, 6.4, 1.5, 3.3, 1.0, f"machine 2:  f(u) = sin(u)\nlocal slope f'(u) = cos(u) = {df:.3f}", fs=9.5)
    box(ax, 10.5, 1.5, 1.4, 1.0, f"output\n{f:.3f}", fc="#f0fdf4", ec=GREEN, fs=10)
    arrow(ax, 1.7, 2.0, 2.6, 2.0); arrow(ax, 5.4, 2.0, 6.4, 2.0, text=f"u = {j:.2f}", fs=9)
    arrow(ax, 9.7, 2.0, 10.5, 2.0)
    ax.text(0.9, 1.1, "nudge x by δ", ha="center", color=RED, fontsize=9.5)
    ax.text(5.9, 1.1, "u moves by δ·3.0", ha="center", color=RED, fontsize=9.5)
    ax.text(10.6, 1.1, f"output moves by\nδ·3.0·({df:.3f})", ha="center", color=RED, fontsize=9.5, va="top")
    ax.text(6, 3.35, "Chain rule:  d/dx f(j(x)) = f'(j(x)) · j'(x)  — the local slopes MULTIPLY along the chain",
            ha="center", fontsize=11, weight="bold")
    num = (np.sin((x + 1e-6) ** 2) - np.sin(x ** 2)) / 1e-6
    ax.text(6, 0.2, f"chain rule: 3.0 × ({df:.3f}) = {df*dj:.4f}      numerical check (nudge x by 10⁻⁶): {num:.4f}",
            ha="center", fontsize=10, color=DARK, bbox=dict(fc="#fffbeb", ec=AMBER, boxstyle="round,pad=0.3"))
    save(fig, OUT, "05_chain_rule.png")


# ------------------------------------------------------------------ 06 local gradient rules
def fig_node_rules():
    fig, axes = plt.subplots(1, 3, figsize=(14, 3.8))
    for ax in axes:
        ax.set_xlim(0, 4); ax.set_ylim(0, 3.2); ax.axis("off")

    def node(ax, x, y, label, fc="white"):
        ax.add_patch(Circle((x, y), 0.32, fc=fc, ec=DARK, lw=1.5, zorder=3))
        ax.text(x, y, label, ha="center", va="center", fontsize=13, weight="bold", zorder=4)

    # ADD
    ax = axes[0]; ax.set_title("Addition node: gradient is copied\nunchanged to both inputs")
    node(ax, 2.2, 1.6, "+")
    for yy, nm, v in [(2.6, "A", 3), (0.6, "B", -1)]:
        ax.text(0.4, yy, f"{nm} = {v}", fontsize=10, color=BLUE, va="center")
        arrow(ax, 1.05, yy, 1.92, 1.6 + (yy - 1.6) * 0.25, color=BLUE)
        ax.text(1.25, yy + (0.25 if yy > 2 else -0.35), "∂L/∂%s = 5" % nm, color=RED, fontsize=10)
    arrow(ax, 2.52, 1.6, 3.4, 1.6, color=BLUE)
    ax.text(3.0, 1.85, "A+B = 2", color=BLUE, fontsize=9, ha="center")
    ax.text(3.0, 1.15, "∂L/∂(A+B) = 5", color=RED, fontsize=10, ha="center")
    # MULTIPLY
    ax = axes[1]; ax.set_title("Multiplication node: gradient is multiplied\nby the OTHER input (swap)")
    node(ax, 2.2, 1.6, "×")
    for yy, nm, v, g in [(2.6, "A", 3, "5·(−1) = −5"), (0.6, "B", -1, "5·3 = 15")]:
        ax.text(0.4, yy, f"{nm} = {v}", fontsize=10, color=BLUE, va="center")
        arrow(ax, 1.05, yy, 1.92, 1.6 + (yy - 1.6) * 0.25, color=BLUE)
        ax.text(0.9, yy + (0.25 if yy > 2 else -0.35), f"∂L/∂{nm} = {g}", color=RED, fontsize=10)
    arrow(ax, 2.52, 1.6, 3.4, 1.6, color=BLUE)
    ax.text(3.0, 1.85, "A·B = −3", color=BLUE, fontsize=9, ha="center")
    ax.text(3.0, 1.15, "∂L/∂(AB) = 5", color=RED, fontsize=10, ha="center")
    # BRANCH
    ax = axes[2]; ax.set_title("Branching: one value used twice →\ngradients from each path ADD")
    node(ax, 1.0, 1.6, "A", fc="#eff6ff")
    node(ax, 2.9, 2.6, "f"); node(ax, 2.9, 0.6, "g")
    arrow(ax, 1.3, 1.75, 2.6, 2.5, color=BLUE); arrow(ax, 1.3, 1.45, 2.6, 0.7, color=BLUE)
    ax.text(2.0, 2.45, "path 1 gives 2", color=RED, fontsize=10, ha="right")
    ax.text(2.0, 0.55, "path 2 gives 4", color=RED, fontsize=10, ha="right")
    ax.text(1.0, 0.95, "∂L/∂A = 2 + 4 = 6", color=RED, fontsize=11, ha="center", weight="bold")
    fig.text(0.5, -0.02, "blue = forward values   ·   red = gradients flowing backward (∂L/∂ something)",
             ha="center", fontsize=10)
    save(fig, OUT, "06_node_rules.png")


# ------------------------------------------------------------------ 07 worked computational graph
def fig_worked_graph():
    fig, ax = canvas(12, 5.4, (0, 12), (0, 5.4))
    k0, k1, x, y = 1.0, 0.5, 2.0, 3.0
    m = k1 * x; yhat = k0 + m; d = y - yhat; L = d ** 2
    gL = 1; gd = 2 * d; gyhat = -gd; gk0 = gyhat; gm = gyhat; gk1 = gm * x; gx = gm * k1

    def nd(xc, yc, label, fwd, grd, fc="white", r=0.42):
        ax.add_patch(Circle((xc, yc), r, fc=fc, ec=DARK, lw=1.5, zorder=3))
        ax.text(xc, yc, label, ha="center", va="center", fontsize=12, weight="bold", zorder=4)
        ax.text(xc, yc + r + 0.12, fwd, ha="center", va="bottom", color=BLUE, fontsize=9.5)
        ax.text(xc, yc - r - 0.12, grd, ha="center", va="top", color=RED, fontsize=9.5, weight="bold")

    nd(0.8, 3.7, "k1", f"= {k1}", f"∂L/∂k1 = {gk1:+.0f}", fc="#fef3c7")
    nd(0.8, 1.9, "x", f"= {x:.0f}", f"({gx:+.0f}, ignored:\ndata is fixed)", fc=LIGHT)
    nd(3.0, 2.8, "×", f"k1·x = {m:.0f}", f"{gm:+.0f}")
    nd(3.0, 0.9, "k0", f"= {k0:.0f}", f"∂L/∂k0 = {gk0:+.0f}", fc="#fef3c7")
    nd(5.3, 2.0, "+", f"ŷ = {yhat:.0f}", f"{gyhat:+.0f}")
    nd(5.3, 4.1, "y", f"= {y:.0f}", "", fc=LIGHT)
    nd(7.5, 3.0, "−", f"y − ŷ = {d:.0f}", f"{gd:+.0f}")
    nd(9.6, 3.0, "sq", f"L = {L:.0f}", f"∂L/∂L = {gL}")
    for (a, b, c, d_) in [(1.22, 3.55, 2.6, 2.95), (1.22, 2.05, 2.6, 2.65), (3.4, 2.65, 4.9, 2.15),
                          (3.4, 1.05, 4.9, 1.85), (5.7, 2.2, 7.1, 2.85), (5.7, 3.95, 7.1, 3.15),
                          (7.92, 3.0, 9.18, 3.0)]:
        arrow(ax, a, b, c, d_, color=GRAY)
    ax.text(6, 5.25, "One data point (x = 2, y = 3), line ŷ = k0 + k1·x with k0 = 1, k1 = 0.5",
            ha="center", fontsize=11, weight="bold")
    legend = ("FORWARD (blue, left → right): compute every value.\n"
              "BACKWARD (red, right → left): start with 1 at L, then\n"
              "  • square node:  × 2·(y−ŷ) = ×2  → +2\n"
              "  • minus node:  ŷ has sign −1  → −2\n"
              "  • plus node:  copy  → −2 to both k0 and (k1·x)\n"
              "  • times node:  × other input  → k1 gets −2·x = −4")
    ax.text(8.0, 0.05, legend, fontsize=9, va="bottom", family="monospace",
            bbox=dict(fc="#f9fafb", ec=GRAY, boxstyle="round,pad=0.4"))
    save(fig, OUT, "07_worked_graph.png")


# ------------------------------------------------------------------ 08 training loop progress
def fig_training_progress():
    rec = (0, 30, 300, 3000, 40000)
    k, hist, snaps = run_gd(K_INIT, 0.02, 40000, record=rec)
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.9))
    ax = axes[0]
    ax.scatter(X, Y, color=DARK, s=20, zorder=5, label="data")
    cols = ["#fecaca", "#fca5a5", "#f87171", RED, GREEN]
    for t, c in zip(rec, cols):
        ax.plot(xs, poly(snaps[t], xs), color=c, lw=2, label=f"step {t:,}: L = {hist[t]:.3f}")
    ax.set_ylim(-1.6, 1.6); ax.legend(fontsize=8, loc="lower right"); ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title("Forward → backward → nudge, repeated")
    ax = axes[1]
    ax.loglog(np.arange(1, len(hist) + 1), hist, color=BLUE, lw=2)
    for t, c in zip(rec, cols):
        ax.scatter([t + 1], [hist[t]], color=c, s=50, zorder=4, edgecolor=DARK)
    ax.set_xlabel("training step (log scale)"); ax.set_ylabel("loss (log scale)")
    ax.set_title("Loss falls fast at first, then slowly\n(the valley gets flatter near the bottom)")
    ax.grid(alpha=0.3, which="both")
    save(fig, OUT, "08_training_progress.png")


# ------------------------------------------------------------------ tiny MLP with manual backprop
class MLP:
    def __init__(self, sizes, act="tanh", seed=0):
        r = np.random.default_rng(seed)
        self.W = [r.normal(0, np.sqrt((2.0 if act == "relu" else 1.0) / a), (b, a)) for a, b in zip(sizes[:-1], sizes[1:])]
        self.b = [np.zeros(b) for b in sizes[1:]]
        self.act = act

    def f(self, z):
        return {"tanh": np.tanh, "relu": lambda v: np.maximum(v, 0), "sigmoid": lambda v: 1 / (1 + np.exp(-v))}[self.act](z)

    def df(self, z):
        if self.act == "tanh":
            return 1 - np.tanh(z) ** 2
        if self.act == "relu":
            return (z > 0).astype(float)
        s = 1 / (1 + np.exp(-z)); return s * (1 - s)

    def forward(self, x):
        self.zs, self.hs = [], [x]
        h = x
        for i, (W, b) in enumerate(zip(self.W, self.b)):
            z = h @ W.T + b
            self.zs.append(z)
            h = z if i == len(self.W) - 1 else self.f(z)
            self.hs.append(h)
        return h

    def backward(self, gout):
        gW, gb = [], []
        g = gout
        for i in reversed(range(len(self.W))):
            if i != len(self.W) - 1:
                g = g * self.df(self.zs[i])
            gW.insert(0, g.T @ self.hs[i]); gb.insert(0, g.sum(0))
            g = g @ self.W[i]
        return gW, gb

    def params(self):
        return self.W + self.b


def fig_mlp_fit():
    xs_ = np.linspace(-3, 3, 200)[:, None]
    target = np.sin(2 * xs_) * np.exp(-0.1 * xs_ ** 2) + 0.3 * np.cos(5 * xs_)
    net = MLP([1, 32, 32, 1], "tanh", seed=1)
    snaps, hist = {}, []
    lr = 0.003; m = [np.zeros_like(p) for p in net.params()]; v = [np.zeros_like(p) for p in net.params()]
    for t in range(1, 4001):
        out = net.forward(xs_ / 3)
        err = out - target; hist.append(float(np.mean(err ** 2)))
        if t in (1, 100, 500, 4000):
            snaps[t] = out.copy()
        gW, gb = net.backward(2 * err / len(xs_))
        # Adam: same gradients, smarter step sizes (what real frameworks use)
        for i, (p, g) in enumerate(zip(net.params(), gW + gb)):
            m[i] = 0.9 * m[i] + 0.1 * g; v[i] = 0.999 * v[i] + 0.001 * g * g
            p -= lr * 0.5 * (1 + np.cos(np.pi * t / 4000)) * (m[i] / (1 - 0.9 ** t)) / (np.sqrt(v[i] / (1 - 0.999 ** t)) + 1e-8)
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.8))
    ax = axes[0]
    ax.plot(xs_, target, color=DARK, lw=3, alpha=0.35, label="target function")
    for t, c in zip((1, 100, 500, 4000), ["#fecaca", "#f87171", RED, GREEN]):
        ax.plot(xs_, snaps[t], color=c, lw=1.8, label=f"step {t}")
    ax.legend(fontsize=8); ax.set_title("A 1→32→32→1 neural network (1,121 weights)\ntrained by the SAME backward pass")
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax = axes[1]
    ax.semilogy(hist, color=BLUE, lw=2); ax.grid(alpha=0.3, which="both")
    ax.set_xlabel("training step"); ax.set_ylabel("mean squared error (log)")
    ax.set_title("Loss during training\n(Adam optimizer + cosine learning-rate decay)")
    save(fig, OUT, "09_mlp_fit.png")


# ------------------------------------------------------------------ 10 finite differences vs backprop cost (measured)
def fig_cost():
    widths = [4, 8, 16, 32, 64, 128]
    P, t_fd, t_bp = [], [], []
    xb = rng.normal(size=(64, 10)); yb = rng.normal(size=(64, 1))
    for w in widths:
        net = MLP([10, w, w, 1], "tanh", seed=2)
        nparam = sum(p.size for p in net.params()); P.append(nparam)
        lossf = lambda: float(np.mean((net.forward(xb) - yb) ** 2))
        t0 = time.perf_counter()
        for _ in range(20):
            out = net.forward(xb); net.backward(2 * (out - yb) / len(xb))
        t_bp.append((time.perf_counter() - t0) / 20)
        t0 = time.perf_counter()
        base = lossf()
        for p in net.params():
            flat = p.reshape(-1)
            for i in range(flat.size):
                old = flat[i]; flat[i] = old + 1e-5; _ = lossf(); flat[i] = old
        t_fd.append(time.perf_counter() - t0)
    P = np.array(P)
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.9))
    ax = axes[0]
    ax.loglog(P, t_fd, "o-", color=RED, lw=2, label="nudge each knob separately\n(finite differences)")
    ax.loglog(P, t_bp, "o-", color=GREEN, lw=2, label="backpropagation")
    for p_, a, b in zip(P, t_fd, t_bp):
        ax.text(p_, a * 1.5, f"{a/b:,.0f}×", fontsize=8, ha="center", color=RED)
    ax.set_xlabel("number of parameters"); ax.set_ylabel("seconds for ONE gradient")
    ax.set_title("Measured on this laptop (tiny networks)"); ax.legend(fontsize=8); ax.grid(alpha=0.3, which="both")
    ax = axes[1]
    Ps = np.logspace(2, 12, 50)
    ax.loglog(Ps, Ps + 1, color=RED, lw=2, label="finite differences: ≈ N + 1 forward passes")
    ax.loglog(Ps, np.full_like(Ps, 3), color=GREEN, lw=2, label="backprop: ≈ 3 forward passes, always")
    for name, n in [("MNIST MLP\n~100 K", 1e5), ("ResNet-50\n25 M", 2.5e7), ("GPT-2\n1.5 B", 1.5e9),
                    ("frontier LLM\n~1 T", 1e12)]:
        ax.axvline(n, color=GRAY, ls=":", lw=1)
        ax.text(n, 40, name, fontsize=8, ha="center",
                bbox=dict(fc="white", ec="none"))
    ax.set_xlabel("number of parameters N"); ax.set_ylabel("cost of one gradient\n(in forward passes)")
    ax.set_title("Why this matters: backprop's cost does NOT grow with N")
    ax.legend(fontsize=8, loc="upper left"); ax.set_ylim(1, 1e13)
    save(fig, OUT, "10_cost_backprop_vs_finite_diff.png")


# ------------------------------------------------------------------ 11 vanishing gradients
def fig_vanishing():
    depth = 20; xb = rng.normal(size=(256, 64))
    fig, ax = plt.subplots(figsize=(8, 4))
    for act, col, lab in [("sigmoid", RED, "sigmoid (1980s–2000s default)"), ("tanh", AMBER, "tanh"),
                          ("relu", GREEN, "ReLU + He init (modern default)")]:
        norms = np.zeros(depth)
        for s in range(5):
            net = MLP([64] * (depth + 1) + [1], act, seed=10 + s)
            out = net.forward(xb)
            gW, _ = net.backward(np.ones_like(out) / len(xb))
            norms += np.array([np.linalg.norm(g) for g in gW[:depth]]) / 5
        ax.semilogy(np.arange(1, depth + 1), norms, "o-", color=col, lw=2, ms=4, label=lab)
    ax.set_xlabel("layer (1 = closest to the input)"); ax.set_ylabel("size of gradient ‖∂L/∂W‖ (log)")
    ax.set_title("Vanishing gradients in a 20-layer network\n(each sigmoid layer multiplies the gradient by ≤ 0.25)")
    ax.legend(fontsize=9); ax.grid(alpha=0.3, which="both")
    save(fig, OUT, "11_vanishing_gradients.png")


# ------------------------------------------------------------------ 12 gradient check
def fig_gradcheck():
    net = MLP([3, 5, 1], "tanh", seed=4)
    xb = rng.normal(size=(8, 3)); yb = rng.normal(size=(8, 1))
    out = net.forward(xb); gW, gb = net.backward(2 * (out - yb) / len(xb))
    analytic = np.concatenate([g.ravel() for g in gW + gb])
    numeric = []
    for p in net.params():
        flat = p.reshape(-1)
        for i in range(flat.size):
            old = flat[i]
            flat[i] = old + 1e-5; lp = float(np.mean((net.forward(xb) - yb) ** 2))
            flat[i] = old - 1e-5; lm = float(np.mean((net.forward(xb) - yb) ** 2))
            flat[i] = old; numeric.append((lp - lm) / 2e-5)
    numeric = np.array(numeric)
    fig, ax = plt.subplots(figsize=(4.8, 4.4))
    lim = max(abs(analytic).max(), abs(numeric).max()) * 1.1
    ax.plot([-lim, lim], [-lim, lim], color=GRAY, ls="--", lw=1)
    ax.scatter(numeric, analytic, color=BLUE, s=30, zorder=3)
    rel = np.max(np.abs(analytic - numeric) / (np.abs(analytic) + np.abs(numeric) + 1e-12))
    ax.set_xlabel("gradient by nudging (finite differences)"); ax.set_ylabel("gradient by backprop")
    ax.set_title(f"Gradient check on all 26 parameters\nmax relative error = {rel:.1e}")
    save(fig, OUT, "12_gradient_check.png")


if __name__ == "__main__":
    fig_curve_fitting(); fig_derivative(); fig_learning_rates(); fig_gradient_2d(); fig_chain_rule()
    fig_node_rules(); fig_worked_graph(); fig_training_progress(); fig_mlp_fit(); fig_cost()
    fig_vanishing(); fig_gradcheck()
