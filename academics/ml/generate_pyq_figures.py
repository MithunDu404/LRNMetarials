import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set clean font and styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.edgecolor'] = '#4a5568'
plt.rcParams['axes.linewidth'] = 1.2

OUT_DIR = r"c:\PROJECTS\Learnmat\academics\ml\pyq_images"
os.makedirs(OUT_DIR, exist_ok=True)

# ==============================================================================
# FIGURE 1: Logic Gates Architecture & XOR Non-Linearity
# ==============================================================================
def make_fig1():
    fig = plt.figure(figsize=(16, 9), dpi=300)
    
    # ------------------ Row 1: Architectures ------------------
    # AND Gate Architecture
    ax_arch1 = fig.add_subplot(2, 3, 1)
    ax_arch1.set_xlim(-0.2, 2.3)
    ax_arch1.set_ylim(-0.2, 1.7)
    ax_arch1.axis('off')
    ax_arch1.set_title("(i) AND Gate: Single Perceptron Architecture\n$w_1=+1.0, w_2=+1.0, b=-1.5$ (Threshold $\\theta=1.5$)",
                       fontsize=10.5, fontweight='bold', pad=8, color='#1a202c')
    
    # Input nodes
    c_x1 = plt.Circle((0.2, 1.1), 0.20, facecolor='#bee3f8', edgecolor='#2b6cb0', lw=1.5, zorder=4)
    c_x2 = plt.Circle((0.2, 0.3), 0.20, facecolor='#bee3f8', edgecolor='#2b6cb0', lw=1.5, zorder=4)
    ax_arch1.add_patch(c_x1)
    ax_arch1.add_patch(c_x2)
    ax_arch1.text(0.2, 1.1, "$x_1$", ha='center', va='center', fontsize=11, fontweight='bold', zorder=10)
    ax_arch1.text(0.2, 0.3, "$x_2$", ha='center', va='center', fontsize=11, fontweight='bold', zorder=10)
    
    # Neuron node
    c_sum = plt.Circle((1.3, 0.7), 0.32, facecolor='#feebc8', edgecolor='#c05621', lw=1.5, zorder=4)
    ax_arch1.add_patch(c_sum)
    ax_arch1.text(1.3, 0.80, r"$\sum w_i x_i + b$", ha='center', va='center', fontsize=9.5, fontweight='bold', zorder=10)
    ax_arch1.text(1.3, 0.58, "Step Unit", ha='center', va='center', fontsize=8, color='#7b341e', zorder=10)
    
    # Connections
    ax_arch1.annotate("", xy=(1.00, 0.77), xytext=(0.40, 1.05),
                      arrowprops=dict(arrowstyle="->", color="#2b6cb0", lw=1.8))
    ax_arch1.text(0.65, 1.02, "$w_1 = +1.0$", fontsize=9, fontweight='bold', color='#2b6cb0', zorder=10)
    
    ax_arch1.annotate("", xy=(1.00, 0.63), xytext=(0.40, 0.35),
                      arrowprops=dict(arrowstyle="->", color="#2b6cb0", lw=1.8))
    ax_arch1.text(0.65, 0.38, "$w_2 = +1.0$", fontsize=9, fontweight='bold', color='#2b6cb0', zorder=10)
    
    # Bias input
    ax_arch1.annotate("", xy=(1.3, 1.02), xytext=(1.3, 1.55),
                      arrowprops=dict(arrowstyle="->", color="#e53e3e", lw=1.8))
    ax_arch1.text(1.35, 1.35, "$b = -1.5$", fontsize=9, fontweight='bold', color='#c53030', zorder=10)
    
    # Output
    ax_arch1.annotate("", xy=(2.05, 0.7), xytext=(1.62, 0.7),
                      arrowprops=dict(arrowstyle="->", color="#276749", lw=2.0))
    ax_arch1.text(2.1, 0.7, "$y$", ha='left', va='center', fontsize=12, fontweight='bold', color='#276749', zorder=10)

    # OR Gate Architecture
    ax_arch2 = fig.add_subplot(2, 3, 2)
    ax_arch2.set_xlim(-0.2, 2.3)
    ax_arch2.set_ylim(-0.2, 1.7)
    ax_arch2.axis('off')
    ax_arch2.set_title("(ii) OR Gate: Single Perceptron Architecture\n$w_1=+1.0, w_2=+1.0, b=-0.5$ (Threshold $\\theta=0.5$)",
                       fontsize=10.5, fontweight='bold', pad=8, color='#1a202c')
    
    c_x1_or = plt.Circle((0.2, 1.1), 0.20, facecolor='#bee3f8', edgecolor='#2b6cb0', lw=1.5, zorder=4)
    c_x2_or = plt.Circle((0.2, 0.3), 0.20, facecolor='#bee3f8', edgecolor='#2b6cb0', lw=1.5, zorder=4)
    ax_arch2.add_patch(c_x1_or)
    ax_arch2.add_patch(c_x2_or)
    ax_arch2.text(0.2, 1.1, "$x_1$", ha='center', va='center', fontsize=11, fontweight='bold', zorder=10)
    ax_arch2.text(0.2, 0.3, "$x_2$", ha='center', va='center', fontsize=11, fontweight='bold', zorder=10)
    
    c_sum_or = plt.Circle((1.3, 0.7), 0.32, facecolor='#feebc8', edgecolor='#c05621', lw=1.5, zorder=4)
    ax_arch2.add_patch(c_sum_or)
    ax_arch2.text(1.3, 0.80, r"$\sum w_i x_i + b$", ha='center', va='center', fontsize=9.5, fontweight='bold', zorder=10)
    ax_arch2.text(1.3, 0.58, "Step Unit", ha='center', va='center', fontsize=8, color='#7b341e', zorder=10)
    
    ax_arch2.annotate("", xy=(1.00, 0.77), xytext=(0.40, 1.05),
                      arrowprops=dict(arrowstyle="->", color="#2b6cb0", lw=1.8))
    ax_arch2.text(0.65, 1.02, "$w_1 = +1.0$", fontsize=9, fontweight='bold', color='#2b6cb0', zorder=10)
    
    ax_arch2.annotate("", xy=(1.00, 0.63), xytext=(0.40, 0.35),
                      arrowprops=dict(arrowstyle="->", color="#2b6cb0", lw=1.8))
    ax_arch2.text(0.65, 0.38, "$w_2 = +1.0$", fontsize=9, fontweight='bold', color='#2b6cb0', zorder=10)
    
    ax_arch2.annotate("", xy=(1.3, 1.02), xytext=(1.3, 1.55),
                      arrowprops=dict(arrowstyle="->", color="#e53e3e", lw=1.8))
    ax_arch2.text(1.35, 1.35, "$b = -0.5$", fontsize=9, fontweight='bold', color='#c53030', zorder=10)
    
    ax_arch2.annotate("", xy=(2.05, 0.7), xytext=(1.62, 0.7),
                      arrowprops=dict(arrowstyle="->", color="#276749", lw=2.0))
    ax_arch2.text(2.1, 0.7, "$y$", ha='left', va='center', fontsize=12, fontweight='bold', color='#276749', zorder=10)

    # XOR Gate Architecture (2-Layer Network)
    ax_arch3 = fig.add_subplot(2, 3, 3)
    ax_arch3.set_xlim(-0.2, 2.7)
    ax_arch3.set_ylim(-0.2, 1.7)
    ax_arch3.axis('off')
    ax_arch3.set_title("(iii) XOR Gate: 2-Layer MLP Architecture\nRequires 2 Hidden Neurons ($h_1$: OR, $h_2$: NAND)",
                       fontsize=10.5, fontweight='bold', pad=8, color='#1a202c')
    
    # Inputs
    c_x1_xor = plt.Circle((0.15, 1.1), 0.18, facecolor='#bee3f8', edgecolor='#2b6cb0', lw=1.5, zorder=4)
    c_x2_xor = plt.Circle((0.15, 0.3), 0.18, facecolor='#bee3f8', edgecolor='#2b6cb0', lw=1.5, zorder=4)
    ax_arch3.add_patch(c_x1_xor)
    ax_arch3.add_patch(c_x2_xor)
    ax_arch3.text(0.15, 1.1, "$x_1$", ha='center', va='center', fontsize=10, fontweight='bold', zorder=10)
    ax_arch3.text(0.15, 0.3, "$x_2$", ha='center', va='center', fontsize=10, fontweight='bold', zorder=10)
    
    # Hidden Neurons
    c_h1 = plt.Circle((1.1, 1.1), 0.24, facecolor='#c6f6d5', edgecolor='#276749', lw=1.5, zorder=4)
    c_h2 = plt.Circle((1.1, 0.3), 0.24, facecolor='#fed7d7', edgecolor='#9b2c2c', lw=1.5, zorder=4)
    ax_arch3.add_patch(c_h1)
    ax_arch3.add_patch(c_h2)
    ax_arch3.text(1.1, 1.1, "$h_1$\n(OR)", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#22543d', zorder=10)
    ax_arch3.text(1.1, 0.3, "$h_2$\n(NAND)", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#742a2a', zorder=10)
    
    # Output Neuron
    c_out = plt.Circle((2.05, 0.7), 0.24, facecolor='#feebc8', edgecolor='#c05621', lw=1.5, zorder=4)
    ax_arch3.add_patch(c_out)
    ax_arch3.text(2.05, 0.7, "$y$\n(AND)", ha='center', va='center', fontsize=8.5, fontweight='bold', color='#7b341e', zorder=10)
    
    # Connecting Arrows
    ax_arch3.annotate("", xy=(0.86, 1.1), xytext=(0.33, 1.1), arrowprops=dict(arrowstyle="->", color="#2b6cb0", lw=1.2))
    ax_arch3.annotate("", xy=(0.86, 0.3), xytext=(0.33, 0.3), arrowprops=dict(arrowstyle="->", color="#2b6cb0", lw=1.2))
    ax_arch3.annotate("", xy=(0.88, 0.44), xytext=(0.31, 0.98), arrowprops=dict(arrowstyle="->", color="#2b6cb0", lw=1.2))
    ax_arch3.annotate("", xy=(0.88, 0.96), xytext=(0.31, 0.42), arrowprops=dict(arrowstyle="->", color="#2b6cb0", lw=1.2))
    
    ax_arch3.annotate("", xy=(1.81, 0.76), xytext=(1.34, 1.04), arrowprops=dict(arrowstyle="->", color="#276749", lw=1.5))
    ax_arch3.annotate("", xy=(1.81, 0.64), xytext=(1.34, 0.36), arrowprops=dict(arrowstyle="->", color="#276749", lw=1.5))
    
    ax_arch3.annotate("", xy=(2.60, 0.7), xytext=(2.29, 0.7), arrowprops=dict(arrowstyle="->", color="#276749", lw=2.0))
    ax_arch3.text(2.62, 0.7, "$y$", ha='left', va='center', fontsize=11, fontweight='bold', color='#276749', zorder=10)

    # ------------------ Row 2: Decision Boundaries in 2D ------------------
    x_vals = np.linspace(-0.2, 1.4, 200)

    # Subplot 4: AND Decision Boundary
    ax1 = fig.add_subplot(2, 3, 4)
    ax1.set_title("AND Decision Boundary (2D)\n$x_1 + x_2 - 1.5 = 0$", fontsize=10.5, fontweight='bold', pad=8, color='#1a202c')
    ax1.scatter([0, 0, 1], [0, 1, 0], color='#e53e3e', s=100, edgecolors='k', zorder=5, label='Class 0 (False)')
    ax1.scatter([1], [1], color='#3182ce', s=120, marker='s', edgecolors='k', zorder=5, label='Class 1 (True)')
    ax1.plot(x_vals, 1.5 - x_vals, color='#2b6cb0', linestyle='--', linewidth=2, label=r'Boundary: $x_1+x_2=1.5$')
    ax1.fill_between(x_vals, np.clip(1.5 - x_vals, -0.2, 1.4), 1.4, color='#bee3f8', alpha=0.35)
    ax1.set_xlim(-0.2, 1.4)
    ax1.set_ylim(-0.2, 1.4)
    ax1.set_xlabel(r"Input $x_1$", fontsize=10)
    ax1.set_ylabel(r"Input $x_2$", fontsize=10)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='lower left', fontsize=8, framealpha=0.95)

    # Subplot 5: OR Decision Boundary
    ax2 = fig.add_subplot(2, 3, 5)
    ax2.set_title("OR Decision Boundary (2D)\n$x_1 + x_2 - 0.5 = 0$", fontsize=10.5, fontweight='bold', pad=8, color='#1a202c')
    ax2.scatter([0], [0], color='#e53e3e', s=100, edgecolors='k', zorder=5, label='Class 0 (False)')
    ax2.scatter([0, 1, 1], [1, 0, 1], color='#3182ce', s=120, marker='s', edgecolors='k', zorder=5, label='Class 1 (True)')
    ax2.plot(x_vals, 0.5 - x_vals, color='#2b6cb0', linestyle='--', linewidth=2, label=r'Boundary: $x_1+x_2=0.5$')
    ax2.fill_between(x_vals, np.clip(0.5 - x_vals, -0.2, 1.4), 1.4, color='#bee3f8', alpha=0.35)
    ax2.set_xlim(-0.2, 1.4)
    ax2.set_ylim(-0.2, 1.4)
    ax2.set_xlabel(r"Input $x_1$", fontsize=10)
    ax2.set_ylabel(r"Input $x_2$", fontsize=10)
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='lower left', fontsize=8, framealpha=0.95)

    # Subplot 6: XOR Decision Boundary
    ax3 = fig.add_subplot(2, 3, 6)
    ax3.set_title("XOR Non-Linear Boundary (2D)\nRequires 2 Separating Hyperplanes", fontsize=10.5, fontweight='bold', pad=8, color='#1a202c')
    ax3.scatter([0, 1], [0, 1], color='#e53e3e', s=100, edgecolors='k', zorder=5, label='Class 0 (False)')
    ax3.scatter([0, 1], [1, 0], color='#3182ce', s=120, marker='s', edgecolors='k', zorder=5, label='Class 1 (True)')
    
    ax3.plot(x_vals, 0.5 - x_vals, color='#38a169', linestyle='--', linewidth=2, label=r'$h_1$ (OR): $x_1+x_2=0.5$')
    ax3.plot(x_vals, 1.5 - x_vals, color='#d69e2e', linestyle='--', linewidth=2, label=r'$h_2$ (NAND): $x_1+x_2=1.5$')
    
    y_low = np.clip(0.5 - x_vals, -0.2, 1.4)
    y_high = np.clip(1.5 - x_vals, -0.2, 1.4)
    ax3.fill_between(x_vals, y_low, y_high, where=(y_high >= y_low), color='#bee3f8', alpha=0.45, label='XOR Active Region (True)')
    
    ax3.set_xlim(-0.2, 1.4)
    ax3.set_ylim(-0.2, 1.4)
    ax3.set_xlabel(r"Input $x_1$", fontsize=10)
    ax3.set_ylabel(r"Input $x_2$", fontsize=10)
    ax3.grid(True, linestyle=':', alpha=0.6)
    ax3.legend(loc='center right', fontsize=8, framealpha=0.95)

    plt.tight_layout()
    p = os.path.join(OUT_DIR, "pyq_fig01_logic_gates_and_xor.png")
    plt.savefig(p, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved:", p)

# ==============================================================================
# FIGURE 3: Multilayer Backprop Output Layer Derivation (Clean Badge & Contrast)
# ==============================================================================
def make_fig3():
    fig, ax = plt.subplots(figsize=(13.5, 6.5), dpi=300)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6.5)
    ax.axis('off')
    
    # Title
    ax.text(5.25, 6.2, "Multilayer Feedforward Neural Network: Output Layer Backpropagation",
            ha='center', va='center', fontsize=13, fontweight='bold', color='#1a202c')
    ax.text(5.25, 5.8, r"Forward Activation Flow vs Backward Error Propagation ($\delta_{j,K}$ Signal)",
            ha='center', va='center', fontsize=10, fontstyle='italic', color='#4a5568')

    # Draw Layer K-1 (Hidden Layer)
    rect_h = patches.FancyBboxPatch((0.5, 1.2), 2.2, 4.3, boxstyle="round,pad=0.2",
                                    facecolor="#ebf8ff", edgecolor="#3182ce", linewidth=1.8)
    ax.add_patch(rect_h)
    ax.text(1.6, 5.15, "Hidden Layer $(K-1)$\n$M_{K-1}$ Neurons", ha='center', va='center',
            fontsize=10.5, fontweight='bold', color='#2b6cb0')
    
    hy_list = [4.3, 3.2, 1.9]
    hl_list = [r"$O_{1, K-1}$", r"$O_{m, K-1}$", r"$O_{M_{K-1}, K-1}$"]
    for hy, hl in zip(hy_list, hl_list):
        c = plt.Circle((1.6, hy), 0.38, facecolor="#90cdf4", edgecolor="#2b6cb0", linewidth=1.5, zorder=5)
        ax.add_patch(c)
        ax.text(1.6, hy, hl, ha='center', va='center', fontsize=9.5, fontweight='bold', color='#1a365d', zorder=10)
    ax.text(1.6, 2.55, r"$\vdots$", ha='center', va='center', fontsize=15, fontweight='bold', color='#2b6cb0')

    # Draw Layer K (Output Layer) - Shifted right to x=5.3 to avoid arrow collision
    rect_o = patches.FancyBboxPatch((5.3, 1.2), 2.7, 4.3, boxstyle="round,pad=0.2",
                                    facecolor="#f0fff4", edgecolor="#38a169", linewidth=1.8)
    ax.add_patch(rect_o)
    ax.text(6.65, 5.15, "Output Layer $K$\n$M_K$ Neurons (Sigmoid)", ha='center', va='center',
            fontsize=10.5, fontweight='bold', color='#276749')

    # Output Neuron j
    c_out = plt.Circle((6.65, 3.2), 0.58, facecolor="#9ae6b4", edgecolor="#276749", linewidth=1.8, zorder=5)
    ax.add_patch(c_out)
    ax.text(6.65, 3.44, r"$\theta_{j, K} = \sum w_{jm,K} O_m + b_j$", ha='center', va='center',
            fontsize=8.5, fontweight='bold', color='#1c4532', zorder=10)
    ax.text(6.65, 3.02, r"$O_{j, K} = \sigma(\theta_{j, K})$", ha='center', va='center',
            fontsize=9.0, fontweight='bold', color='#22543d', zorder=10)

    # Loss Box
    rect_l = patches.FancyBboxPatch((8.8, 2.3), 1.5, 1.8, boxstyle="round,pad=0.15",
                                    facecolor="#fed7d7", edgecolor="#e53e3e", linewidth=1.8)
    ax.add_patch(rect_l)
    ax.text(9.55, 3.5, "Squared Error\n" + r"$E = \frac{1}{2}(t_j - O_{j,K})^2$",
            ha='center', va='center', fontsize=8.5, fontweight='bold', color='#9b2c2c')
    ax.text(9.55, 2.7, r"Target $t_j$", ha='center', va='center', fontsize=9.5, fontweight='bold', color='#742a2a')

    # Forward Arrow (m to j)
    ax.annotate("", xy=(6.05, 3.2), xytext=(1.98, 3.2),
                arrowprops=dict(arrowstyle="->", color="#3182ce", lw=2.5))
    ax.text(4.0, 3.45, r"Forward Pass: $w_{jm, K} \cdot O_{m, K-1}$", ha='center', va='bottom',
            fontsize=9.5, color='#2b6cb0', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor='none', alpha=0.9))

    # Arrow from Neuron j to Loss
    ax.annotate("", xy=(8.8, 3.2), xytext=(7.23, 3.2),
                arrowprops=dict(arrowstyle="->", color="#276749", lw=2.2))
    ax.text(8.0, 3.45, r"$O_{j,K}$", ha='center', va='bottom', fontsize=9.5, fontweight='bold', color='#276749')

    # Backward Error Propagation Arrow (Delta)
    ax.annotate("", xy=(1.98, 2.7), xytext=(6.05, 2.7),
                arrowprops=dict(arrowstyle="->", color="#e53e3e", lw=2.2, linestyle='--'))
    ax.text(4.0, 2.45, r"Backward Error: $\delta_{j, K} = (t_j - O_{j, K}) \cdot O_{j, K}(1 - O_{j, K})$",
            ha='center', va='top', fontsize=9.5, color='#c53030', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.25', facecolor='white', edgecolor='#e2e8f0', alpha=0.95))

    # Weight Update Formula Box at Bottom
    formula_text = (
        r"$\mathbf{1.\ Chain\ Rule:}\ \frac{\partial E}{\partial w_{jm,K}} = "
        r"\frac{\partial E}{\partial O_{j,K}} \cdot \frac{\partial O_{j,K}}{\partial \theta_{j,K}} \cdot \frac{\partial \theta_{j,K}}{\partial w_{jm,K}} "
        r"= -(t_j - O_{j,K}) \cdot O_{j,K}(1 - O_{j,K}) \cdot O_{m, K-1} = -\delta_{j,K} \cdot O_{m,K-1}$"
        "\n"
        r"$\mathbf{2.\ Gradient\ Descent\ Update:}\ w_{jm,K}^{(\text{new})} = w_{jm,K}^{(\text{old})} - \eta \frac{\partial E}{\partial w_{jm,K}} "
        r"= w_{jm,K}^{(\text{old})} + \eta \, \delta_{j,K} \, O_{m,K-1}$"
    )
    ax.text(5.25, 0.55, formula_text, ha='center', va='center', fontsize=9.2,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#fffaf0', edgecolor='#dd6b20', lw=1.5))

    plt.tight_layout()
    p = os.path.join(OUT_DIR, "pyq_fig03_backprop_output_layer.png")
    plt.savefig(p, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved:", p)

# ==============================================================================
# FIGURE 4: Perceptron Convergence & Margin Geometry (Clean Layout)
# ==============================================================================
def make_fig4():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.2), dpi=300)
    
    # Subplot 1: Geometric Margin & Hyperplane
    ax1.set_title(r"Perceptron Convergence Geometry (Novikoff Bound)" + "\n" + r"Separating Vector $\mathbf{w}^*$ & Margin $\gamma$",
                  fontsize=11, fontweight='bold', pad=12, color='#1a202c')
    
    x_line = np.linspace(-1.5, 1.5, 100)
    ax1.plot(x_line, -x_line, color='#2b6cb0', linewidth=2, label=r'Optimal Hyperplane $\mathbf{w}^{*T} \mathbf{x} = 0$')
    
    gamma = 0.4
    ax1.plot(x_line, -x_line + gamma * np.sqrt(2), color='#3182ce', linestyle=':', label=r'Positive Margin: $\mathbf{w}^{*T}\mathbf{x} = +\gamma$')
    ax1.plot(x_line, -x_line - gamma * np.sqrt(2), color='#e53e3e', linestyle=':', label=r'Negative Margin: $\mathbf{w}^{*T}\mathbf{x} = -\gamma$')
    
    ax1.scatter([0.2, 0.8, 0.5, 1.1], [0.6, 0.4, 1.0, 0.2], color='#3182ce', s=90, edgecolors='k', zorder=5, label='Class +1 ($y_i=+1$)')
    ax1.scatter([-0.3, -0.7, -0.4, -1.0], [-0.5, -0.3, -0.9, -0.2], color='#e53e3e', s=90, edgecolors='k', zorder=5, label='Class -1 ($y_i=-1$)')
    
    ax1.annotate("", xy=(0.7, 0.7), xytext=(0, 0),
                 arrowprops=dict(arrowstyle="->", color="#1a365d", lw=2.5))
    ax1.text(0.75, 0.72, r"$\mathbf{w}^*$ (Norm 1)", fontsize=11, fontweight='bold', color='#1a365d')

    circle_r = plt.Circle((0, 0), 1.5, fill=False, edgecolor='#718096', linestyle='--', linewidth=1.5, label=r'Data Sphere: $\|\mathbf{x}_i\| \leq R$')
    ax1.add_patch(circle_r)
    
    ax1.set_xlim(-1.6, 1.6)
    ax1.set_ylim(-1.6, 1.6)
    ax1.set_xlabel(r"Feature $x_1$", fontsize=10)
    ax1.set_ylabel(r"Feature $x_2$", fontsize=10)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper left', fontsize=8, framealpha=0.92)
    ax1.set_aspect('equal')

    # Subplot 2: Analytical Bound on Mistakes k <= (R / gamma)^2
    ax2.set_title("Perceptron Proof Mechanics\n" + r"Cos-Angle Bound: $\cos(\theta_k) \leq 1 \Rightarrow k \leq (R/\gamma)^2$",
                  fontsize=11, fontweight='bold', pad=12, color='#1a202c')
    
    k_vals = np.linspace(1, 30, 200)
    gamma_val = 0.35
    R_val = 1.4
    k_max = int((R_val / gamma_val)**2)
    
    num = k_vals * gamma_val
    denom = np.sqrt(k_vals) * R_val
    cos_theta = num / denom
    
    ax2.plot(k_vals, cos_theta, color='#805ad5', linewidth=2.5, label=r'$\frac{\mathbf{w}_k^T \mathbf{w}^\ast}{\|\mathbf{w}_k\|} \geq \frac{k\gamma}{\sqrt{k}R} = \frac{\sqrt{k}\gamma}{R}$')
    ax2.axhline(1.0, color='#e53e3e', linestyle='--', linewidth=2, label=r'Geometric Ceiling: $\cos(\theta_k) \leq 1.0$')
    ax2.axvline(k_max, color='#dd6b20', linestyle=':', linewidth=2, label=rf'Max Updates: $k_{{max}} = \lfloor(R/\gamma)^2\rfloor = {k_max}$')
    
    ax2.scatter([k_max], [1.0], color='#e53e3e', s=120, zorder=6)
    ax2.annotate(f"Convergence Point\n$k \\leq {k_max}$ Mistakes", xy=(k_max, 1.0), xytext=(k_max - 9, 1.15),
                 arrowprops=dict(arrowstyle="->", color="#e53e3e", lw=1.8), fontsize=9.5, fontweight='bold', color='#9b2c2c')

    ax2.set_xlabel("Cumulative Update Count (Mistakes) $k$", fontsize=10)
    ax2.set_ylabel(r"Ratio $\frac{\mathbf{w}_k^T \mathbf{w}^\ast}{\|\mathbf{w}_k\| \|\mathbf{w}^\ast\|}$", fontsize=10)
    ax2.set_xlim(0, 32)
    ax2.set_ylim(0, 1.4)
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='lower right', fontsize=8.5, framealpha=0.95)

    plt.tight_layout()
    p = os.path.join(OUT_DIR, "pyq_fig04_perceptron_convergence.png")
    plt.savefig(p, bbox_inches='tight', dpi=300)
    plt.close()
    print("Saved:", p)

if __name__ == '__main__':
    make_fig1()
    make_fig3()
    make_fig4()
    print("Figures 1, 3, and 4 refined successfully.")
