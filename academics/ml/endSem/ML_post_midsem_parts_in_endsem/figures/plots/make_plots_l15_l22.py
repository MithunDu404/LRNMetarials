"""Plots for the Lec 15-22 learning guides. Run from the guides' folder:
py -3.12 figures/plots/make_plots_l15_l22.py"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

BLUE, GREEN, AMBER, RED, PURPLE, GREY = "#2563EB", "#059669", "#D97706", "#DC2626", "#7C3AED", "#6B7280"
OUT = "figures/plots/"


def style(ax, title, xl, yl):
    ax.set_title(title, fontsize=11)
    ax.set_xlabel(xl)
    ax.set_ylabel(yl)
    ax.grid(alpha=0.3)


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT + name, dpi=300, facecolor="white")
    plt.close(fig)


# 1. AlexNet vs VGG16: parameters per layer (millions) ---------------------------------
def vgg_layers():
    rows, c = [], 3
    for blk, (k, r) in enumerate([(64, 2), (128, 2), (256, 3), (512, 3), (512, 3)], 1):
        for i in range(r):
            rows.append((f"c{blk}-{i + 1}", 9 * c * k + k))
            c = k
    rows += [("fc6", 25088 * 4096 + 4096), ("fc7", 4096 * 4096 + 4096), ("fc8", 4096 * 1000 + 1000)]
    return rows


rows = vgg_layers()
fig, ax = plt.subplots(figsize=(9, 4.4))
cols = [BLUE if n.startswith("c") else AMBER for n, _ in rows]
ax.bar([n for n, _ in rows], [p / 1e6 for _, p in rows], color=cols)
for n, p in rows:
    if p > 4e6:
        ax.annotate(f"{p / 1e6:.1f}M", (n, p / 1e6), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=8)
ax.tick_params(axis="x", rotation=60, labelsize=8)
style(ax, "VGG16: 13 conv layers hold 14.7M weights; the 3 FC layers hold 123.6M (89%)", "Layer", "Parameters (millions)")
ax.bar([0], [0], color=BLUE, label="Convolution (3x3)")
ax.bar([0], [0], color=AMBER, label="Fully connected")
ax.legend()
save(fig, "fig_vgg_params.png")

# 2. Sparse AE: KL(rho || rho_hat) for rho = 0.05 ---------------------------------------
rh = np.linspace(0.002, 0.95, 600)
rho = 0.05
kl = rho * np.log(rho / rh) + (1 - rho) * np.log((1 - rho) / (1 - rh))
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(rh, kl, color=PURPLE, lw=2.4)
ax.axvline(rho, color=GREEN, ls="--", lw=1.2)
ax.annotate("target ρ = 0.05: penalty 0", (rho, 0), textcoords="offset points", xytext=(8, 60), color=GREEN, fontsize=9,
            arrowprops=dict(arrowstyle="->", color=GREEN))
v = rho * math.log(rho / 0.1) + (1 - rho) * math.log(0.95 / 0.9)
ax.plot(0.1, v, "o", color=RED)
ax.annotate(f"slide example ρ̂ = 0.1: {v:.4f}", (0.1, v), textcoords="offset points", xytext=(20, 30), color=RED, fontsize=9,
            arrowprops=dict(arrowstyle="->", color=RED))
v5 = rho * math.log(rho / 0.5) + (1 - rho) * math.log(0.95 / 0.5)
ax.plot(0.5, v5, "o", color=AMBER)
ax.annotate(f"ρ̂ = 0.5: {v5:.3f}", (0.5, v5), textcoords="offset points", xytext=(10, -18), color=AMBER, fontsize=9)
ax.set_ylim(0, 2.5)
style(ax, "Sparsity penalty KL(ρ ‖ ρ̂): zero at the target, grows as neurons fire more", "Average activation ρ̂ of a hidden neuron", "KL penalty (nats)")
save(fig, "fig_kl_sparsity.png")

# 3. VAE: KL of one latent dimension vs sigma, for several mu ---------------------------
s = np.linspace(0.05, 3, 600)
fig, ax = plt.subplots(figsize=(8, 4.2))
for mu, col in [(0, GREEN), (1, BLUE), (2, RED)]:
    ax.plot(s, -0.5 * (1 + np.log(s ** 2) - mu ** 2 - s ** 2), color=col, lw=2.4, label=f"μ = {mu}")
ax.plot(1, 0, "o", color=GREEN)
ax.annotate("μ = 0, σ = 1: KL = 0\n(exactly the prior N(0,1))", (1, 0), textcoords="offset points", xytext=(25, 40), fontsize=9,
            color=GREEN, arrowprops=dict(arrowstyle="->", color=GREEN))
ax.set_ylim(0, 4)
style(ax, "VAE KL term for one latent dimension: −½(1 + log σ² − μ² − σ²)", "σ (standard deviation output by the encoder)", "KL (nats)")
ax.legend()
save(fig, "fig_vae_kl.png")

# 4. VAE latent space: prior, three encoded Gaussians, interpolation line ---------------
fig, ax = plt.subplots(figsize=(6.4, 6))
for r_, a in [(1, 0.5), (2, 0.3), (3, 0.15)]:
    ax.add_patch(Ellipse((0, 0), 2 * r_, 2 * r_, fill=False, ls="--", color=GREY, alpha=a + 0.3))
ax.text(0.05, -3.25, "prior p(z) = N(0, I): 1σ, 2σ, 3σ circles", color=GREY, fontsize=9, ha="center")
pts = [((-1.6, 0.9), (0.9, 0.6), "q(z|x) for a '0'", RED), ((1.5, 1.2), (0.7, 0.9), "q(z|x) for a '1'", BLUE),
       ((0.2, -1.5), (1.0, 0.5), "q(z|x) for a '7'", PURPLE)]
for (cx, cy), (w, h), lab, col in pts:
    ax.add_patch(Ellipse((cx, cy), 2 * w, 2 * h, color=col, alpha=0.25))
    ax.plot(cx, cy, "o", color=col)
    ax.text(cx, cy + h + 0.12, lab, ha="center", color=col, fontsize=9)
z0, z1 = np.array(pts[0][0]), np.array(pts[1][0])
ts = [0, 0.25, 0.5, 0.75, 1]
line = np.array([(1 - t) * z0 + t * z1 for t in ts])
ax.plot(line[:, 0], line[:, 1], "-", color=AMBER, lw=1.5)
ax.plot(line[1:-1, 0], line[1:-1, 1], "s", color=AMBER, ms=7)
ax.text(0, 1.25, "interpolated points\nt = 0.25, 0.5, 0.75", color=AMBER, fontsize=9, ha="center")
ax.set_xlim(-3.5, 3.5)
ax.set_ylim(-3.5, 3.5)
ax.set_aspect("equal")
style(ax, "A 2-D VAE latent space (illustration)", "z₁", "z₂")
save(fig, "fig_vae_latent.png")

# 5. RNN: gradient factor w^k over k steps back ------------------------------------------
k = np.arange(0, 51)
fig, ax = plt.subplots(figsize=(10, 4.4))
for w, col in [(0.5, RED), (0.9, AMBER), (1.0, GREY), (1.1, PURPLE), (1.5, BLUE)]:
    ax.plot(k, w ** k, color=col, lw=2.2, label=f"factor per step = {w}")
ax.set_yscale("log")
ax.set_ylim(1e-12, 1e6)
ax.axhspan(1e-12, 1e-3, color=RED, alpha=0.06)
ax.axhspan(1e3, 1e6, color=BLUE, alpha=0.06)
ax.text(1, 2e-11, "vanishing: early steps get almost no signal", color=RED, fontsize=9)
ax.text(2, 2e4, "exploding: updates blow up", color=BLUE, fontsize=9)
style(ax, "BPTT multiplies one factor per time step: the product shrinks or blows up", "Steps back in time (k)", "Size of gradient factor (log scale)")
ax.legend(fontsize=8, loc="upper left", bbox_to_anchor=(1.01, 1))
save(fig, "fig_rnn_gradient.png")

# 6. Gate activations: sigmoid vs tanh ---------------------------------------------------
x = np.linspace(-6, 6, 600)
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(x, 1 / (1 + np.exp(-x)), color=GREEN, lw=2.4, label="sigmoid σ(x): 0 to 1, used as a gate (how much)")
ax.plot(x, np.tanh(x), color=PURPLE, lw=2.4, label="tanh(x): −1 to 1, used for content (what)")
ax.axhline(0, color=GREY, lw=0.8)
ax.axhline(1, color=GREY, lw=0.8, ls=":")
ax.axhline(-1, color=GREY, lw=0.8, ls=":")
ax.set_ylim(-1.25, 1.25)
style(ax, "Why gates use sigmoid and the candidate uses tanh", "Weighted input", "Output")
ax.legend(loc="lower right", fontsize=9)
save(fig, "fig_sigmoid_tanh.png")

# 7. Memory retention: keep-factor per step (LSTM forget gate f, GRU update gate z) -------
steps = np.arange(0, 101)
fig, ax = plt.subplots(figsize=(8, 4.2))
for g, col in [(0.5, RED), (0.9, AMBER), (0.99, GREEN), (1.0, BLUE)]:
    ax.plot(steps, g ** steps, color=col, lw=2.2, label=f"keep factor = {g}")
ax.annotate(f"0.99¹⁰⁰ ≈ {0.99 ** 100:.2f}", (100, 0.99 ** 100), textcoords="offset points", xytext=(-80, 15), color=GREEN, fontsize=9)
ax.annotate(f"0.9¹⁰ ≈ {0.9 ** 10:.2f}", (10, 0.9 ** 10), textcoords="offset points", xytext=(18, 30), color=AMBER, fontsize=9)
style(ax, "How much of an old memory survives when nothing new is written", "Time steps", "Fraction of old memory left")
ax.legend(fontsize=9, loc="upper left", bbox_to_anchor=(0.6, 0.88))
save(fig, "fig_memory_keep.png")
print("done")


# 8. tanh vs ReLU slope (Lec 15) ------------------------------------------------------
x = np.linspace(-5, 5, 1001)
fig, ax = plt.subplots(figsize=(7, 3.6))
ax.plot(x, 1 - np.tanh(x) ** 2, color=BLUE, lw=2, label="tanh slope: 1 - tanh²(x)")
ax.plot(x, (x > 0).astype(float), color=GREEN, lw=2, label="ReLU slope: 0 or 1")
ax.plot([3], [1 - math.tanh(3) ** 2], "o", color=RED)
ax.annotate("x = 3: tanh slope ≈ 0.0099", (3, 0.0099), (2.0, 0.3), color=RED,
            arrowprops=dict(arrowstyle="->", color=RED))
style(ax, "Slopes passed back in backpropagation", "input x", "slope")
ax.set_ylim(-0.05, 1.15)
ax.legend(loc="upper left", fontsize=9)
save(fig, "fig_relu_tanh_slope.png")

# 9. Receptive field of three stacked 3x3 convolutions (Lec 16) -----------------------
from matplotlib.patches import Rectangle
fig, ax = plt.subplots(figsize=(7, 6))
levels = [("Input: 7×7 patch seen", 7, 0), ("Layer 1 output: 5×5 used", 5, 1), ("Layer 2 output: 3×3 used", 3, 2), ("Layer 3: 1 output neuron", 1, 3)]
cols = [GREY, BLUE, GREEN, RED]
for (lab, n, lvl), col in zip(levels, cols):
    y0 = lvl * 3.2
    for i in range(9):
        inside = abs(i - 4) <= (n - 1) / 2
        ax.add_patch(Rectangle((i, y0), 1, 1, facecolor=col if inside else "white",
                               alpha=0.75 if inside else 1, edgecolor="#334155", lw=0.8))
    ax.text(9.4, y0 + 0.5, lab, va="center", fontsize=10, color=col if col != GREY else "#334155")
for lvl in range(3):
    n = 7 - 2 * lvl
    lo, hi = 4 - (n - 1) / 2, 4 + (n - 1) / 2 + 1
    y_top, y_bot = (lvl + 1) * 3.2, lvl * 3.2 + 1
    ax.plot([lo + 1, lo], [y_top, y_bot], color="#94A3B8", lw=1, ls="--")
    ax.plot([hi - 1, hi], [y_top, y_bot], color="#94A3B8", lw=1, ls="--")
ax.set_xlim(-0.5, 16.5); ax.set_ylim(-0.5, 11.2); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("Three 3×3 layers see a 7×7 input patch (one row shown per layer)", fontsize=11)
save(fig, "fig_receptive_field.png")
