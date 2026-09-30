"""Generate computed figures for the Foundations, Linear & Logistic Regression Visual Guide.

Lectures covered: 1.ML_Lec_1, 2.ML_Lec_2, 3.ML_Lec_3
Run: py make_figures.py
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "reg_clf_guide_images")
os.makedirs(OUT, exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 130,
    "savefig.dpi": 130,
    "font.size": 9.5,
    "font.family": "sans-serif",
    "axes.grid": True,
    "grid.alpha": 0.3,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

BLUE, ORANGE, GREEN, RED, PURPLE = "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"

def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Generated: {name}")

# --- Fig 0: Data Science vs Machine Learning Paradigm ---
def fig_ds_vs_ml_paradigm():
    fig, ax = plt.subplots(1, 2, figsize=(14, 5.3), dpi=130)
    
    # Left: Traditional Programming vs Machine Learning
    ax[0].set_xlim(0, 10); ax[0].set_ylim(0, 10); ax[0].axis("off")
    ax[0].set_title("The Fundamental Paradigm Shift: Rules vs. Learning", fontsize=11, fontweight="bold", pad=12)
    
    # Card 1: Traditional
    c1 = patches.FancyBboxPatch((0.4, 5.2), 9.2, 4.3, boxstyle="round,pad=0.2", facecolor="#f8fafc", edgecolor="#94a3b8", lw=1.5)
    ax[0].add_patch(c1)
    ax[0].text(5.0, 9.0, "TRADITIONAL SOFTWARE ENGINEERING", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#0f172a")
    ax[0].text(5.0, 8.45, "Human writes explicit rules; computer executes them blindly", ha="center", va="center", fontsize=8, fontstyle="italic", color="#475569")
    
    # Elements Traditional
    b1_data = patches.FancyBboxPatch((0.8, 5.7), 2.2, 2.0, boxstyle="round,pad=0.1", facecolor="#dbeafe", edgecolor="#2563eb", lw=1.3)
    b1_rules = patches.FancyBboxPatch((3.7, 5.7), 2.6, 2.0, boxstyle="round,pad=0.1", facecolor="#fee2e2", edgecolor="#dc2626", lw=1.3)
    b1_out = patches.FancyBboxPatch((7.0, 5.7), 2.2, 2.0, boxstyle="round,pad=0.1", facecolor="#dcfce7", edgecolor="#16a34a", lw=1.3)
    ax[0].add_patch(b1_data); ax[0].add_patch(b1_rules); ax[0].add_patch(b1_out)
    
    ax[0].text(1.9, 6.7, "DATA\n(Inputs)", ha="center", va="center", fontsize=9, fontweight="bold", color="#1e40af")
    ax[0].text(3.35, 6.7, "+", ha="center", va="center", fontsize=16, fontweight="bold", color="#64748b")
    ax[0].text(5.0, 6.7, "EXPLICIT RULES\n(Handcrafted Code)", ha="center", va="center", fontsize=8, fontweight="bold", color="#991b1b")
    ax[0].text(6.65, 6.7, "➔", ha="center", va="center", fontsize=16, fontweight="bold", color="#64748b")
    ax[0].text(8.1, 6.7, "ANSWERS\n(Outputs)", ha="center", va="center", fontsize=9, fontweight="bold", color="#15803d")
    
    # Card 2: Machine Learning
    c2 = patches.FancyBboxPatch((0.4, 0.3), 9.2, 4.4, boxstyle="round,pad=0.2", facecolor="#eff6ff", edgecolor="#3b82f6", lw=1.8)
    ax[0].add_patch(c2)
    ax[0].text(5.0, 4.25, "MACHINE LEARNING (The Inversion)", ha="center", va="center", fontsize=9.5, fontweight="bold", color="#1d4ed8")
    ax[0].text(5.0, 3.75, "Data & desired answers are provided; computer discovers the rules!", ha="center", va="center", fontsize=8, fontstyle="italic", color="#2563eb")
    
    # Elements ML
    b2_data = patches.FancyBboxPatch((0.8, 1.0), 2.2, 2.0, boxstyle="round,pad=0.1", facecolor="#dbeafe", edgecolor="#2563eb", lw=1.3)
    b2_ans = patches.FancyBboxPatch((3.7, 1.0), 2.6, 2.0, boxstyle="round,pad=0.1", facecolor="#dcfce7", edgecolor="#16a34a", lw=1.3)
    b2_model = patches.FancyBboxPatch((7.0, 1.0), 2.2, 2.0, boxstyle="round,pad=0.1", facecolor="#fef3c7", edgecolor="#d97706", lw=1.6)
    ax[0].add_patch(b2_data); ax[0].add_patch(b2_ans); ax[0].add_patch(b2_model)
    
    ax[0].text(1.9, 2.0, "DATA\n(Inputs X)", ha="center", va="center", fontsize=9, fontweight="bold", color="#1e40af")
    ax[0].text(3.35, 2.0, "+", ha="center", va="center", fontsize=16, fontweight="bold", color="#64748b")
    ax[0].text(5.0, 2.0, "ANSWERS\n(Labels Y)", ha="center", va="center", fontsize=9, fontweight="bold", color="#15803d")
    ax[0].text(6.65, 2.0, "➔", ha="center", va="center", fontsize=16, fontweight="bold", color="#64748b")
    ax[0].text(8.1, 2.0, "MODEL\n(Learned Rules)", ha="center", va="center", fontsize=9, fontweight="bold", color="#b45309")
    
    # Right: Data Science vs Machine Learning (Rectangle vs Square)
    ax[1].set_xlim(0, 10); ax[1].set_ylim(0, 10); ax[1].axis("off")
    ax[1].set_title("Data Science vs. Machine Learning Hierarchy", fontsize=11, fontweight="bold", pad=12)
    
    # Outer rectangle: Data Science
    ds_outer = patches.FancyBboxPatch((0.5, 0.4), 9.0, 9.1, boxstyle="round,pad=0.25", facecolor="#f0f9ff", edgecolor="#0284c7", lw=2)
    ax[1].add_patch(ds_outer)
    ax[1].text(5.0, 9.05, "DATA SCIENCE (The Rectangle)", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#0369a1")
    ax[1].text(5.0, 8.55, "Broad multidisciplinary field covering the end-to-end data lifecycle", ha="center", va="center", fontsize=8, color="#0284c7")
    
    # Bullets for DS
    ax[1].text(1.0, 7.8, "• Big Data Engineering, Pipelines & Warehouses (Spark, SQL)", fontsize=8, color="#0f172a")
    ax[1].text(1.0, 7.3, "• Data Cleansing, Imputation & Feature Engineering", fontsize=8, color="#0f172a")
    ax[1].text(1.0, 6.8, "• Business Intelligence (BI), KPI Dashboards & Analytics", fontsize=8, color="#0f172a")
    ax[1].text(1.0, 6.3, "• Domain Expertise, A/B Testing & Causal Decision Science", fontsize=8, color="#0f172a")
    
    # Inner square: Machine Learning
    ml_inner = patches.FancyBboxPatch((1.0, 0.7), 8.0, 5.0, boxstyle="round,pad=0.2", facecolor="#ffffff", edgecolor="#2563eb", lw=2.2)
    ax[1].add_patch(ml_inner)
    ax[1].text(5.0, 5.3, "MACHINE LEARNING (The Square)", ha="center", va="center", fontsize=10.5, fontweight="bold", color="#1e40af")
    ax[1].text(5.0, 4.85, "The specialized algorithmic & statistical learning core", ha="center", va="center", fontsize=8, fontstyle="italic", color="#475569")
    
    # ML internal highlights
    pill_a = patches.FancyBboxPatch((1.3, 2.7), 7.4, 1.7, boxstyle="round,pad=0.1", facecolor="#eff6ff", edgecolor="#93c5fd", lw=1)
    ax[1].add_patch(pill_a)
    ax[1].text(5.0, 3.8, "Statistical Learning & Optimization Algorithms:", ha="center", va="center", fontsize=8, fontweight="bold", color="#1e3a8a")
    ax[1].text(5.0, 3.15, "Linear / Logistic Regression, Trees, SVMs, Neural Nets", ha="center", va="center", fontsize=7.8, color="#1e40af")
    
    pill_b = patches.FancyBboxPatch((1.3, 1.1), 7.4, 1.25, boxstyle="round,pad=0.1", facecolor="#fef3c7", edgecolor="#fcd34d", lw=1)
    ax[1].add_patch(pill_b)
    ax[1].text(5.0, 1.9, "Lecture 1 Geometric Maxim:", ha="center", va="center", fontsize=7.8, fontweight="bold", color="#92400e")
    ax[1].text(5.0, 1.4, "\"All squares are rectangles, but not all rectangles are squares.\"", ha="center", va="center", fontsize=7.5, fontstyle="italic", color="#b45309")
    
    save(fig, "00_ds_vs_ml_paradigm.png")

# --- Fig 0b: 2x2 Grid of the 4 Machine Learning Paradigms ---
def fig_ml_taxonomy_2x2():
    fig, axes = plt.subplots(2, 2, figsize=(14, 9.4), dpi=130)
    plt.subplots_adjust(hspace=0.22, wspace=0.18)
    
    # Subplot 1: Supervised Learning
    ax1 = axes[0, 0]
    ax1.set_xlim(0, 10); ax1.set_ylim(0, 10); ax1.axis("off")
    c1 = patches.FancyBboxPatch((0.2, 0.2), 9.6, 9.6, boxstyle="round,pad=0.2", facecolor="#eff6ff", edgecolor="#3b82f6", lw=1.8)
    ax1.add_patch(c1)
    h1 = patches.FancyBboxPatch((0.4, 8.2), 9.2, 1.3, boxstyle="round,pad=0.1", facecolor="#1e40af", edgecolor="none")
    ax1.add_patch(h1)
    ax1.text(5.0, 9.0, "1. Supervised Learning", ha="center", va="center", fontsize=11, fontweight="bold", color="white")
    ax1.text(5.0, 8.5, "Learning with a Teacher (Labeled Targets y Provided)", ha="center", va="center", fontsize=8, color="#bfdbfe")
    
    ax1.text(0.7, 7.6, "• Dataset: Pairs of (Input feature vector x, Ground-truth target label y)", fontsize=8, color="#0f172a")
    ax1.text(0.7, 7.1, "• Objective: Learn mapping f(x) ≈ y that generalizes accurately to unseen test data", fontsize=8, color="#0f172a")
    
    # Sub-boxes for classification and regression
    b_clf = patches.FancyBboxPatch((0.5, 2.5), 4.2, 4.3, boxstyle="round,pad=0.1", facecolor="white", edgecolor="#60a5fa", lw=1.2)
    b_reg = patches.FancyBboxPatch((5.3, 2.5), 4.2, 4.3, boxstyle="round,pad=0.1", facecolor="white", edgecolor="#60a5fa", lw=1.2)
    ax1.add_patch(b_clf); ax1.add_patch(b_reg)
    
    ax1.text(2.6, 6.35, "A. Classification", ha="center", va="center", fontweight="bold", fontsize=9, color="#1d4ed8")
    clf_desc = "Target y is Discrete Category\n\n• Binary: 0 or 1 (Spam vs. Ham)\n• Multiclass: Fish, Fruits, Digits\n• Output: Class probability / label\n• Boundary: Decision surface"
    ax1.text(2.6, 5.9, clf_desc, ha="center", va="top", fontsize=7.3, color="#334155")
    
    ax1.text(7.4, 6.35, "B. Regression", ha="center", va="center", fontweight="bold", fontsize=9, color="#1d4ed8")
    reg_desc = "Target y is Continuous Value\n\n• Numerical values: y ∈ ℝ\n• Sales vs. Advertising budget\n• House price & temperature\n• Output: Continuous fitted curve"
    ax1.text(7.4, 5.9, reg_desc, ha="center", va="top", fontsize=7.3, color="#334155")
    
    # Analogy footer
    f1 = patches.FancyBboxPatch((0.5, 0.5), 9.0, 1.7, boxstyle="round,pad=0.1", facecolor="#dbeafe", edgecolor="#93c5fd", lw=1)
    ax1.add_patch(f1)
    ax1.text(5.0, 1.5, "Classroom Analogy (Lecture 1):", ha="center", va="center", fontweight="bold", fontsize=8.2, color="#1e40af")
    ax1.text(5.0, 0.95, "A student solving textbook practice problems with the full answer key provided.", ha="center", va="center", fontsize=7.6, fontstyle="italic", color="#1e3a8a")

    # Subplot 2: Unsupervised Learning
    ax2 = axes[0, 1]
    ax2.set_xlim(0, 10); ax2.set_ylim(0, 10); ax2.axis("off")
    c2 = patches.FancyBboxPatch((0.2, 0.2), 9.6, 9.6, boxstyle="round,pad=0.2", facecolor="#fff7ed", edgecolor="#f97316", lw=1.8)
    ax2.add_patch(c2)
    h2 = patches.FancyBboxPatch((0.4, 8.2), 9.2, 1.3, boxstyle="round,pad=0.1", facecolor="#c2410c", edgecolor="none")
    ax2.add_patch(h2)
    ax2.text(5.0, 9.0, "2. Unsupervised Learning", ha="center", va="center", fontsize=11, fontweight="bold", color="white")
    ax2.text(5.0, 8.5, "Learning without a Teacher (No Target Labels y Provided)", ha="center", va="center", fontsize=8, color="#fed7aa")
    
    ax2.text(0.7, 7.6, "• Dataset: Raw input features x ONLY (Zero human supervisor feedback)", fontsize=8, color="#0f172a")
    ax2.text(0.7, 7.1, "• Objective: Discover hidden patterns, intrinsic geometry, and natural groupings", fontsize=8, color="#0f172a")
    
    # 3 mini boxes
    b_clu = patches.FancyBboxPatch((0.4, 2.5), 2.9, 4.3, boxstyle="round,pad=0.1", facecolor="white", edgecolor="#fb923c", lw=1.2)
    b_ass = patches.FancyBboxPatch((3.55, 2.5), 2.9, 4.3, boxstyle="round,pad=0.1", facecolor="white", edgecolor="#fb923c", lw=1.2)
    b_dim = patches.FancyBboxPatch((6.7, 2.5), 2.9, 4.3, boxstyle="round,pad=0.1", facecolor="white", edgecolor="#fb923c", lw=1.2)
    ax2.add_patch(b_clu); ax2.add_patch(b_ass); ax2.add_patch(b_dim)
    
    ax2.text(1.85, 6.35, "A. Clustering", ha="center", va="center", fontweight="bold", fontsize=8.2, color="#ea580c")
    clu_desc = "Group by similarity\n\n• K-Means\n• DBSCAN density\n• Customer segments\n• Anomaly detection"
    ax2.text(1.85, 5.9, clu_desc, ha="center", va="top", fontsize=7.2, color="#334155")
    
    ax2.text(5.0, 6.35, "B. Association", ha="center", va="center", fontweight="bold", fontsize=8.2, color="#ea580c")
    ass_desc = "Item dependencies\n\n• Market Basket:\n  \"Diapers ➔ Beer\"\n• Apriori, FP-Growth\n• Recommenders"
    ax2.text(5.0, 5.9, ass_desc, ha="center", va="top", fontsize=7.2, color="#334155")
    
    ax2.text(8.15, 6.35, "C. Dim. Reduction", ha="center", va="center", fontweight="bold", fontsize=8.2, color="#ea580c")
    dim_desc = "Compress features\n\n• PCA (Eigenvectors)\n• t-SNE, UMAP\n• Noise removal\n• 2D/3D visualization"
    ax2.text(8.15, 5.9, dim_desc, ha="center", va="top", fontsize=7.2, color="#334155")
    
    f2 = patches.FancyBboxPatch((0.5, 0.5), 9.0, 1.7, boxstyle="round,pad=0.1", facecolor="#ffedd5", edgecolor="#fed7aa", lw=1)
    ax2.add_patch(f2)
    ax2.text(5.0, 1.5, "Archaeology Analogy:", ha="center", va="center", fontweight="bold", fontsize=8.2, color="#9a3412")
    ax2.text(5.0, 0.95, "Sorting thousands of ancient pottery shards into cohesive piles based on shape.", ha="center", va="center", fontsize=7.6, fontstyle="italic", color="#7c2d12")

    # Subplot 3: Semi-Supervised Learning
    ax3 = axes[1, 0]
    ax3.set_xlim(0, 10); ax3.set_ylim(0, 10); ax3.axis("off")
    c3 = patches.FancyBboxPatch((0.2, 0.2), 9.6, 9.6, boxstyle="round,pad=0.2", facecolor="#faf5ff", edgecolor="#a855f7", lw=1.8)
    ax3.add_patch(c3)
    h3 = patches.FancyBboxPatch((0.4, 8.2), 9.2, 1.3, boxstyle="round,pad=0.1", facecolor="#7e22ce", edgecolor="none")
    ax3.add_patch(h3)
    ax3.text(5.0, 9.0, "3. Semi-Supervised Learning", ha="center", va="center", fontsize=11, fontweight="bold", color="white")
    ax3.text(5.0, 8.5, "The Hybrid Economy (Small Labeled Seed + Vast Unlabeled Pool)", ha="center", va="center", fontsize=8, color="#e9d5ff")
    
    ax3.text(0.7, 7.6, "• Economic Reality: Unlabeled data is cheap; expert human labeling is costly", fontsize=7.8, color="#0f172a")
    ax3.text(0.7, 7.1, "• Medical Example: 1,000,000 cell scans exist, but only 100 labeled by doctors", fontsize=7.8, color="#0f172a")
    
    # Two Core Assumptions
    b_asm1 = patches.FancyBboxPatch((0.5, 2.5), 4.2, 4.3, boxstyle="round,pad=0.1", facecolor="white", edgecolor="#c084fc", lw=1.2)
    b_asm2 = patches.FancyBboxPatch((5.3, 2.5), 4.2, 4.3, boxstyle="round,pad=0.1", facecolor="white", edgecolor="#c084fc", lw=1.2)
    ax3.add_patch(b_asm1); ax3.add_patch(b_asm2)
    
    ax3.text(2.6, 6.35, "A. Smoothness Assumption", ha="center", va="center", fontweight="bold", fontsize=8.6, color="#9333ea")
    sm_desc = "Points close together share labels:\n\nIf two data points x_1, x_2 are close\nin a high-density feature region,\ntheir true labels y_1, y_2\nmust almost certainly be identical."
    ax3.text(2.6, 5.9, sm_desc, ha="center", va="top", fontsize=7.3, color="#334155")
    
    ax3.text(7.4, 6.35, "B. Cluster Assumption", ha="center", va="center", fontweight="bold", fontsize=8.6, color="#9333ea")
    cl_desc = "Boundaries avoid dense groups:\n\nThe decision boundary must pass\nthrough low-density empty gaps;\nit should NEVER slice directly\nthrough dense clusters of data."
    ax3.text(7.4, 5.9, cl_desc, ha="center", va="top", fontsize=7.3, color="#334155")
    
    f3 = patches.FancyBboxPatch((0.5, 0.5), 9.0, 1.7, boxstyle="round,pad=0.1", facecolor="#f3e8ff", edgecolor="#d8b4fe", lw=1)
    ax3.add_patch(f3)
    ax3.text(5.0, 1.5, "Classroom Primer Analogy (Lecture 1):", ha="center", va="center", fontweight="bold", fontsize=8.2, color="#6b21a8")
    ax3.text(5.0, 0.95, "Teacher solves 2 examples on the board; student solves 200 independently at home.", ha="center", va="center", fontsize=7.6, fontstyle="italic", color="#581c87")

    # Subplot 4: Reinforcement Learning
    ax4 = axes[1, 1]
    ax4.set_xlim(0, 10); ax4.set_ylim(0, 10); ax4.axis("off")
    c4 = patches.FancyBboxPatch((0.2, 0.2), 9.6, 9.6, boxstyle="round,pad=0.2", facecolor="#f0fdf4", edgecolor="#22c55e", lw=1.8)
    ax4.add_patch(c4)
    h4 = patches.FancyBboxPatch((0.4, 8.2), 9.2, 1.3, boxstyle="round,pad=0.1", facecolor="#15803d", edgecolor="none")
    ax4.add_patch(h4)
    ax4.text(5.0, 9.0, "4. Reinforcement Learning (RL)", ha="center", va="center", fontsize=11, fontweight="bold", color="white")
    ax4.text(5.0, 8.5, "Learning by Trial-and-Error Interaction with an Environment", ha="center", va="center", fontsize=8, color="#bbf7d0")
    
    # Interaction loop box
    loop_box = patches.FancyBboxPatch((0.5, 3.4), 9.0, 4.5, boxstyle="round,pad=0.1", facecolor="white", edgecolor="#86efac", lw=1.2)
    ax4.add_patch(loop_box)
    
    # Agent & Environment blocks
    ag_box = patches.FancyBboxPatch((0.9, 5.2), 2.8, 2.0, boxstyle="round,pad=0.1", facecolor="#dcfce7", edgecolor="#16a34a", lw=1.4)
    env_box = patches.FancyBboxPatch((6.3, 5.2), 2.8, 2.0, boxstyle="round,pad=0.1", facecolor="#fee2e2", edgecolor="#ef4444", lw=1.4)
    ax4.add_patch(ag_box); ax4.add_patch(env_box)
    ax4.text(2.3, 6.2, "AGENT\n(Decision Maker)", ha="center", va="center", fontsize=8.2, fontweight="bold", color="#166534")
    ax4.text(7.7, 6.2, "ENVIRONMENT\n(Dynamic World)", ha="center", va="center", fontsize=8.2, fontweight="bold", color="#991b1b")
    
    # Arrows and clear text labels
    ax4.annotate("", xy=(6.2, 6.8), xytext=(3.8, 6.8), arrowprops=dict(arrowstyle="->", lw=2.2, color="#16a34a"))
    ax4.text(5.0, 7.25, "Action a_t (Policy π)", ha="center", va="center", fontsize=8, fontweight="bold", color="#15803d")
    
    ax4.annotate("", xy=(3.8, 5.6), xytext=(6.2, 5.6), arrowprops=dict(arrowstyle="->", lw=2.2, color="#dc2626"))
    ax4.text(5.0, 5.15, "State s_t+1 + Reward r_t+1", ha="center", va="center", fontsize=8, fontweight="bold", color="#b91c1c")
    
    ax4.text(5.0, 4.15, "• Value Function V(s) / Q(s, a): Expected discounted future reward\n• Trade-off: Exploration (try new moves) vs. Exploitation (pick known best)", ha="center", va="center", fontsize=7.4, color="#1e293b")
    
    # Analogy footer
    f4 = patches.FancyBboxPatch((0.5, 0.5), 9.0, 2.6, boxstyle="round,pad=0.1", facecolor="#dcfce7", edgecolor="#bbf7d0", lw=1)
    ax4.add_patch(f4)
    ax4.text(5.0, 2.6, "Learning to Ride a Bicycle Analogy:", ha="center", va="center", fontweight="bold", fontsize=8.2, color="#15803d")
    ax4.text(5.0, 2.05, "• Fall over = Negative reward (Pain!) ➔ Policy updates to correct balance", ha="center", va="center", fontsize=7.5, color="#166534")
    ax4.text(5.0, 1.55, "• Stay upright = Positive reward (Speed) ➔ Reinforced successful behavior", ha="center", va="center", fontsize=7.5, color="#166534")
    ax4.text(5.0, 0.95, "Real Applications: Self-driving cars, Robotics, Chess & AlphaGo", ha="center", va="center", fontsize=7.5, fontstyle="italic", color="#14532d")
    
    save(fig, "00b_ml_taxonomy_and_paradigms.png")

# --- Fig 1: Fish Classification (1D vs 2D Feature Space) ---
def fig_fish_features():
    np.random.seed(42)
    salmon_len = np.random.normal(10, 2.0, 50)
    salmon_ltn = np.random.normal(3.5, 1.2, 50)
    bass_len = np.random.normal(14, 2.2, 50)
    bass_ltn = np.random.normal(8.0, 1.3, 50)
    
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    
    # 1D feature length
    ax[0].hist(salmon_len, bins=15, alpha=0.6, color=ORANGE, label="Salmon (y=0)", density=True)
    ax[0].hist(bass_len, bins=15, alpha=0.6, color=BLUE, label="Sea Bass (y=1)", density=True)
    ax[0].axvline(12.0, color=RED, linestyle="--", lw=2, label="Threshold l*=12 (Overlaps!)")
    ax[0].set_title("1D Feature: Length Alone Has Overlap")
    ax[0].set_xlabel("Fish Length (cm)")
    ax[0].set_ylabel("Density")
    ax[0].legend(frameon=False, loc="upper right")
    
    # 2D feature space
    ax[1].scatter(salmon_len, salmon_ltn, color=ORANGE, label="Salmon", edgecolors="k", s=40, alpha=0.8)
    ax[1].scatter(bass_len, bass_ltn, color=BLUE, label="Sea Bass", edgecolors="k", s=40, alpha=0.8)
    x_vals = np.linspace(6, 19, 100)
    y_vals = -0.7 * x_vals + 14.5
    ax[1].plot(x_vals, y_vals, color=GREEN, lw=2, label="Linear Boundary (Clean separation)")
    ax[1].set_title("2D Space: Length + Lightness Separates Species")
    ax[1].set_xlabel("Fish Length (cm)")
    ax[1].set_ylabel("Scale Lightness")
    ax[1].legend(frameon=False, loc="upper right")
    
    save(fig, "01_fish_feature_space.png")

# --- Fig 2: SLR & Least Squares with Residuals and Assumptions ---
def fig_slr_least_squares():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([1, 1, 2, 2, 4])  # From Sir's Slide 1 table!
    
    n = len(x)
    c_hat = (n * np.sum(x*y) - np.sum(x)*np.sum(y)) / (n * np.sum(x**2) - (np.sum(x))**2)
    a_hat = (np.sum(y) - c_hat * np.sum(x)) / n
    y_pred = a_hat + c_hat * x
    
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    
    # Left: Data and residuals
    x_grid = np.linspace(0.5, 5.5, 100)
    ax[0].plot(x_grid, a_hat + c_hat * x_grid, color=BLUE, lw=2, label=f"Fitted Line: y = {a_hat:.2f} + {c_hat:.2f}x")
    ax[0].scatter(x, y, color=ORANGE, s=70, zorder=5, edgecolors="k", label="Actual Observations (y_i)")
    for xi, yi, ypi in zip(x, y, y_pred):
        ax[0].plot([xi, xi], [yi, ypi], color=RED, linestyle=":", lw=1.8)
    ax[0].plot([], [], color=RED, linestyle=":", label="Residuals e_i = y_i - ŷ_i")
    ax[0].set_title(f"Least Squares Fit on Sir's Data (Slope={c_hat:.2f}, Intercept={a_hat:.2f})")
    ax[0].set_xlabel("Adv. Cost X (Rs.)")
    ax[0].set_ylabel("Sales Amount Y (Qty)")
    ax[0].legend(frameon=False)
    
    # Right: Normal distribution bells at each X
    ax[1].plot(x_grid, a_hat + c_hat * x_grid, color=BLUE, lw=2, label="E(Y|X) = a + cX")
    for xi in [1.5, 3.0, 4.5]:
        mean_y = a_hat + c_hat * xi
        y_range = np.linspace(mean_y - 1.5, mean_y + 1.5, 100)
        prob = np.exp(-0.5 * ((y_range - mean_y)/0.4)**2) / (0.4 * np.sqrt(2*np.pi))
        ax[1].plot(xi + prob * 0.4, y_range, color=PURPLE, lw=1.5)
        ax[1].plot([xi, xi + np.max(prob)*0.4], [mean_y, mean_y], color="gray", linestyle="--")
    ax[1].scatter(x, y, color=ORANGE, s=40, alpha=0.6)
    ax[1].set_title("Assumption: Normal Error Distribution y_i ~ N(a + cx_i, σ²)")
    ax[1].set_xlabel("X (Controlled Regressor)")
    ax[1].set_ylabel("Y (Response Distribution)")
    ax[1].legend(frameon=False)
    
    save(fig, "02_slr_geometry_and_assumptions.png")

# --- Fig 3: ANOVA & Sum of Squares Partitioning ---
def fig_anova_sum_of_squares():
    x = np.array([1, 2, 3, 4, 5])
    y = np.array([1, 1, 2, 2, 4])
    y_bar = np.mean(y)
    c_hat = 0.7
    a_hat = -0.1
    y_pred = a_hat + c_hat * x
    
    ss_tot = np.sum((y - y_bar)**2)
    ss_reg = np.sum((y_pred - y_bar)**2)
    ss_res = np.sum((y - y_pred)**2)
    r2 = ss_reg / ss_tot
    
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.bar(["SS_Total (n-1 = 4)", "SS_Reg (k-1 = 1)", "SS_Res (n-k = 3)"], 
                  [ss_tot, ss_reg, ss_res], 
                  color=[PURPLE, GREEN, RED], width=0.55, edgecolor="k")
    
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., h + 0.1, f"{h:.2f}", ha="center", va="bottom", fontweight="bold")
        
    ax.set_ylim(0, ss_tot + 1.2)
    ax.set_ylabel("Sum of Squares")
    ax.set_title(f"ANOVA Partitioning: SS_T ({ss_tot:.2f}) = SS_Reg ({ss_reg:.2f}) + SS_Res ({ss_res:.2f})\nR² = {r2:.3f} (81.7% of variance explained)")
    
    save(fig, "03_anova_ss_partitioning.png")

# --- Fig 4: Linear vs Logistic Regression for Classification ---
def fig_linear_vs_logistic():
    x = np.array([1, 2, 3, 4, 6, 7, 8, 9, 10, 16])
    y = np.array([0, 0, 0, 0, 1, 1, 1, 1, 1, 1])
    
    m, b = np.polyfit(x, y, 1)
    
    from sklearn.linear_model import LogisticRegression
    clf = LogisticRegression()
    clf.fit(x.reshape(-1, 1), y)
    
    x_test = np.linspace(0, 18, 200).reshape(-1, 1)
    y_lin = m * x_test + b
    y_log = clf.predict_proba(x_test)[:, 1]
    
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    
    # Linear regression on 0/1
    ax[0].scatter(x, y, color=ORANGE, s=50, edgecolors="k", zorder=5, label="Data (0=Fail, 1=Pass)")
    ax[0].plot(x_test, y_lin, color=RED, lw=2, label="Linear Fit (Spills <0 and >1)")
    ax[0].axhline(0, color="k", lw=0.6)
    ax[0].axhline(1, color="k", lw=0.6)
    ax[0].axhline(0.5, color="gray", linestyle="--", label="Decision Cutoff 0.5")
    ax[0].set_ylim(-0.3, 1.4)
    ax[0].set_title("Linear Regression Fails for Probabilities")
    ax[0].set_xlabel("Study Hours")
    ax[0].set_ylabel("Predicted Output")
    ax[0].legend(frameon=False, loc="upper left")
    
    # Logistic regression sigmoid
    ax[1].scatter(x, y, color=ORANGE, s=50, edgecolors="k", zorder=5, label="Data")
    ax[1].plot(x_test, y_log, color=BLUE, lw=2.2, label="Sigmoid: P(Y=1|X) = σ(wX + b)")
    ax[1].axhline(0.5, color="gray", linestyle="--", label="Threshold = 0.5 (Boundary)")
    ax[1].axvline(4.8, color=GREEN, linestyle=":", lw=2, label="Decision Boundary x ≈ 4.8h")
    ax[1].set_ylim(-0.1, 1.1)
    ax[1].set_title("Logistic Regression Squashes Output to (0, 1)")
    ax[1].set_xlabel("Study Hours")
    ax[1].set_ylabel("Predicted Probability")
    ax[1].legend(frameon=False, loc="upper left")
    
    save(fig, "04_linear_vs_logistic_classification.png")

# --- Fig 5: Probability, Odds, and Log-Odds Transformation ---
def fig_odds_logodds():
    p = np.linspace(0.01, 0.99, 500)
    odds = p / (1 - p)
    log_odds = np.log(odds)
    
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    
    # Probability vs Odds
    ax[0].plot(p, odds, color=ORANGE, lw=2)
    ax[0].set_title("Probability to Odds: Odds = P / (1 - P)")
    ax[0].set_xlabel("Probability P ∈ (0, 1)")
    ax[0].set_ylabel("Odds ∈ (0, ∞)")
    ax[0].set_ylim(0, 20)
    ax[0].axvline(0.5, color="gray", linestyle="--")
    ax[0].text(0.52, 2.5, "P=0.5 → Odds=1 (1:1 even)", color="black", fontsize=9)
    
    # Probability vs Log-Odds
    ax[1].plot(p, log_odds, color=BLUE, lw=2)
    ax[1].set_title("Probability to Log-Odds (Logit): ln(P / (1 - P))")
    ax[1].set_xlabel("Probability P ∈ (0, 1)")
    ax[1].set_ylabel("Log-Odds ∈ (-∞, +∞)")
    ax[1].axhline(0, color="gray", linestyle="--")
    ax[1].axvline(0.5, color="gray", linestyle="--")
    ax[1].text(0.52, 0.4, "P=0.5 → Logit=0", color="black", fontsize=9)
    ax[1].text(0.1, -2.5, "Negative Log-Odds\n(Unlikely)", color=RED, fontsize=9)
    ax[1].text(0.65, 2.5, "Positive Log-Odds\n(Likely)", color=GREEN, fontsize=9)
    
    save(fig, "05_odds_and_log_odds_mapping.png")

# --- Fig 6: Cost Surface: Non-Convex MSE vs Convex Log-Loss ---
def fig_loss_surfaces():
    w = np.linspace(-3, 3, 200)
    z = w * 2.0
    sig = 1.0 / (1.0 + np.exp(-z))
    mse = 0.5 * (sig - 1.0)**2
    log_loss = -np.log(np.clip(sig, 1e-12, 1.0))
    
    fig, ax = plt.subplots(1, 2, figsize=(11, 4))
    
    ax[0].plot(w, mse, color=RED, lw=2.2)
    ax[0].set_title("Squared Error + Sigmoid: Flat Plateaus (Stalls!)")
    ax[0].set_xlabel("Weight w")
    ax[0].set_ylabel("MSE Cost")
    ax[0].annotate("Zero gradient plateau\n(Model is wrong but stalls)", 
                   xy=(-2.0, 0.48), xytext=(-2.8, 0.3),
                   arrowprops=dict(arrowstyle="->", color=RED))
    
    ax[1].plot(w, log_loss, color=GREEN, lw=2.2)
    ax[1].set_title("Log-Loss (Binary Cross-Entropy): Strictly Convex")
    ax[1].set_xlabel("Weight w")
    ax[1].set_ylabel("Log Loss Cost")
    ax[1].annotate("Steep gradient downhill\n(Fast learning when wrong)", 
                   xy=(-1.5, 3.2), xytext=(-0.8, 4.0),
                   arrowprops=dict(arrowstyle="->", color=GREEN))
    
    save(fig, "06_loss_surface_mse_vs_logloss.png")

# --- Fig 7: L1 vs L2 Regularization Geometry ---
def fig_regularization_contours():
    w1 = np.linspace(-2.5, 2.5, 200)
    w2 = np.linspace(-2.5, 2.5, 200)
    W1, W2 = np.meshgrid(w1, w2)
    Loss = (W1 - 1.5)**2 + 2*(W2 - 1.5)**2
    
    fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
    
    # L1 Lasso (Diamond)
    ax[0].contour(W1, W2, Loss, levels=8, colors="gray", alpha=0.7)
    diamond = np.array([[1, 0], [0, 1], [-1, 0], [0, -1], [1, 0]]) * 1.2
    ax[0].plot(diamond[:, 0], diamond[:, 1], color=RED, lw=2.5, label="L1 Penalty (|w1| + |w2| ≤ C)")
    ax[0].scatter([0], [1.2], color=GREEN, s=80, zorder=5, label="Sparse Solution (w1=0!)")
    ax[0].axhline(0, color="k", lw=0.7)
    ax[0].axvline(0, color="k", lw=0.7)
    ax[0].set_title("L1 Lasso: Hits Corners → Feature Selection (w1=0)")
    ax[0].set_xlabel("w1")
    ax[0].set_ylabel("w2")
    ax[0].legend(frameon=False, loc="lower left")
    
    # L2 Ridge (Circle)
    ax[1].contour(W1, W2, Loss, levels=8, colors="gray", alpha=0.7)
    circle = plt.Circle((0, 0), 1.2, color=BLUE, fill=False, lw=2.5, label="L2 Penalty (w1² + w2² ≤ C)")
    ax[1].add_patch(circle)
    ax[1].scatter([0.85], [0.85], color=ORANGE, s=80, zorder=5, label="Shrunk Solution (w1, w2 ≠ 0)")
    ax[1].axhline(0, color="k", lw=0.7)
    ax[1].axvline(0, color="k", lw=0.7)
    ax[1].set_title("L2 Ridge: Shrinks Smoothly, Retains All Features")
    ax[1].set_xlabel("w1")
    ax[1].set_ylabel("w2")
    ax[1].legend(frameon=False, loc="lower left")
    
    save(fig, "07_regularization_l1_vs_l2_geometry.png")

# --- Fig 8: Multiclass Fruit Classification (From Slide 66) ---
def fig_multiclass_fruits():
    weight = np.array([150, 120, 100, 130, 160, 110])
    sweetness = np.array([8, 6, 7, 5, 9, 6])
    classes = ["Apple", "Banana", "Orange", "Banana", "Apple", "Orange"]
    color_map = {"Apple": RED, "Banana": ORANGE, "Orange": GREEN}
    
    fig, ax = plt.subplots(figsize=(7, 4.2))
    for w, s, c in zip(weight, sweetness, classes):
        ax.scatter(w, s, color=color_map[c], s=100, edgecolors="k", zorder=5)
        ax.text(w + 1.2, s, f"{c}", verticalalignment="center", fontsize=9, fontweight="bold")
        
    ax.set_title("Multiclass Fruit Classification (Lecture 3 Worked Example)\nFeatures: Weight (g) vs Sweetness (1-10)")
    ax.set_xlabel("Weight (g)")
    ax.set_ylabel("Sweetness Scale")
    ax.set_xlim(90, 175)
    ax.set_ylim(4, 10.5)
    
    for c, col in color_map.items():
        ax.scatter([], [], color=col, edgecolors="k", s=70, label=c)
    ax.legend(frameon=False, loc="lower right")
    
    save(fig, "08_multiclass_fruit_dataset.png")

# --- Fig 9: Multiclass One-vs-Rest vs Multinomial Softmax ---
def fig_ovr_vs_softmax():
    np.random.seed(42)
    n = 35
    c0 = np.random.randn(n, 2) * 0.7 + np.array([2.5, 6.5])
    c1 = np.random.randn(n, 2) * 0.7 + np.array([6.5, 6.5])
    c2 = np.random.randn(n, 2) * 0.7 + np.array([4.5, 2.5])
    
    fig, ax = plt.subplots(1, 2, figsize=(12, 5), dpi=130)
    
    # Left: One-vs-Rest (OvR)
    ax[0].scatter(c0[:, 0], c0[:, 1], color=RED, edgecolors="k", s=45, label="Class 0 (Apple)")
    ax[0].scatter(c1[:, 0], c1[:, 1], color=ORANGE, edgecolors="k", s=45, label="Class 1 (Banana)")
    ax[0].scatter(c2[:, 0], c2[:, 1], color=GREEN, edgecolors="k", s=45, label="Class 2 (Orange)")
    
    ax[0].plot([1.0, 7.0], [4.5, 8.5], color=RED, linestyle="--", lw=2, label="Classifier 0 (Apple vs Rest)")
    ax[0].plot([3.0, 8.5], [8.5, 3.5], color=ORANGE, linestyle="--", lw=2, label="Classifier 1 (Banana vs Rest)")
    ax[0].plot([1.5, 8.0], [4.5, 4.5], color=GREEN, linestyle="--", lw=2, label="Classifier 2 (Orange vs Rest)")
    
    amb_circle = plt.Circle((4.5, 5.5), 0.9, color="#94a3b8", alpha=0.3, linestyle=":", lw=1.5)
    ax[0].add_patch(amb_circle)
    ax[0].text(4.5, 5.5, "Ambiguous\nZone!", ha="center", va="center", fontsize=8, fontweight="bold", color="#1e293b")
    
    ax[0].set_title("Strategy 1: One-vs-Rest (OvR)\n3 Independent Binary Lines → Ambiguous Overlaps", fontsize=10.5, fontweight="bold")
    ax[0].set_xlabel("Feature 1 (Weight)")
    ax[0].set_ylabel("Feature 2 (Sweetness)")
    ax[0].set_xlim(0.5, 8.5)
    ax[0].set_ylim(1.0, 9.0)
    ax[0].legend(frameon=True, facecolor="white", edgecolor="#cbd5e1", fontsize=7.8, loc="upper right")
    
    # Right: Multinomial Softmax
    centers = np.array([[2.5, 6.5], [6.5, 6.5], [4.5, 2.5]])
    xx, yy = np.meshgrid(np.linspace(0.5, 8.5, 100), np.linspace(1.0, 9.0, 100))
    grid = np.c_[xx.ravel(), yy.ravel()]
    d0 = np.sum((grid - centers[0])**2, axis=1)
    d1 = np.sum((grid - centers[1])**2, axis=1)
    d2 = np.sum((grid - centers[2])**2, axis=1)
    Z0, Z1, Z2 = -d0, -d1, -d2
    exp0, exp1, exp2 = np.exp(Z0), np.exp(Z1), np.exp(Z2)
    sum_exp = exp0 + exp1 + exp2
    P0 = (exp0 / sum_exp).reshape(xx.shape)
    P1 = (exp1 / sum_exp).reshape(xx.shape)
    P2 = (exp2 / sum_exp).reshape(xx.shape)
    pred = np.argmax(np.stack([P0, P1, P2], axis=-1), axis=-1)
    
    ax[1].contourf(xx, yy, pred, levels=[-0.5, 0.5, 1.5, 2.5], colors=["#fee2e2", "#ffedd5", "#dcfce7"], alpha=0.6)
    ax[1].contour(xx, yy, pred, levels=[0.5, 1.5], colors=["#475569"], linewidths=2.2)
    
    ax[1].scatter(c0[:, 0], c0[:, 1], color=RED, edgecolors="k", s=45, label="Class 0 (Apple)")
    ax[1].scatter(c1[:, 0], c1[:, 1], color=ORANGE, edgecolors="k", s=45, label="Class 1 (Banana)")
    ax[1].scatter(c2[:, 0], c2[:, 1], color=GREEN, edgecolors="k", s=45, label="Class 2 (Orange)")
    
    ax[1].set_title("Strategy 2: Multinomial Softmax\nJoint Probability Distribution (P0+P1+P2=1.0 Everywhere)", fontsize=10.5, fontweight="bold")
    ax[1].set_xlabel("Feature 1 (Weight)")
    ax[1].set_ylabel("Feature 2 (Sweetness)")
    ax[1].set_xlim(0.5, 8.5)
    ax[1].set_ylim(1.0, 9.0)
    ax[1].legend(frameon=True, facecolor="white", edgecolor="#cbd5e1", fontsize=7.8, loc="upper right")
    
    save(fig, "09_ovr_vs_softmax_multiclass.png")

if __name__ == "__main__":
    fig_ds_vs_ml_paradigm()
    fig_ml_taxonomy_2x2()
    fig_fish_features()
    fig_slr_least_squares()
    fig_anova_sum_of_squares()
    fig_linear_vs_logistic()
    fig_odds_logodds()
    fig_loss_surfaces()
    fig_regularization_contours()
    fig_multiclass_fruits()
    fig_ovr_vs_softmax()
    print("All 11 figures successfully generated!")
