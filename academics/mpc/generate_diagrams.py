import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Ensure output directory exists
OUT_DIR = r"c:\PROJECTS\Learnmat\academics\mpc\images"
os.makedirs(OUT_DIR, exist_ok=True)

# Set high-quality styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.autolayout'] = False

# ==============================================================================
# FIG 1: Mobile-to-Mobile Call Setup Architecture & Protocol Flow
# ==============================================================================
def generate_fig1_call_setup():
    fig, ax = plt.subplots(figsize=(12, 9.0), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#FFFFFF')
    
    # Define vertical lifelines
    entities = [
        ("MS-A\n(Calling Mobile)", 1.0, '#2563EB'),
        ("BS-1\n(Serving Cell A)", 3.2, '#0D9488'),
        ("MSC / VLR / HLR\n(Switching Core)", 5.6, '#4F46E5'),
        ("BS-2\n(Serving Cell B)", 8.0, '#0D9488'),
        ("MS-B\n(Called Mobile)", 10.2, '#10B981')
    ]
    
    for name, x, color in entities:
        # Box header
        rect = patches.FancyBboxPatch((x-0.9, 10.2), 1.8, 0.95, boxstyle="round,pad=0.1",
                                      facecolor=color, edgecolor='#1E293B', linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x, 10.67, name, ha='center', va='center', color='white', weight='bold', fontsize=9.5)
        # Lifeline
        ax.plot([x, x], [0.5, 10.2], color='#94A3B8', linestyle='--', linewidth=1.2, zorder=1)

    # Sequence steps with distinct vertical coordinates to prevent collision
    # (y, x_start, x_end, title, subtext, color, type)
    steps = [
        (9.5, 1.0, 3.2, "1. Call Request (MIN, Dialed Digits)", "Reverse Control Channel [RCC]", '#DC2626', 'arrow'),
        (8.6, 3.2, 5.6, "2. Relays Call Request via Backhaul Link", "Wired MSC Backhaul", '#475569', 'arrow'),
        (7.7, 5.6, 5.6, "3. MSC Validates MS-A & Queries HLR/VLR to locate MS-B", "Core Database Tracking", '#7C3AED', 'self'),
        (6.8, 5.6, 8.0, "4. Dispatches Paging Order to Target BS-2", "Wired MSC Backhaul", '#475569', 'arrow'),
        (5.9, 8.0, 10.2, "5. Paging Broadcast with MIN of MS-B", "Forward Control Channel [FCC]", '#D97706', 'arrow'),
        (5.0, 10.2, 8.0, "6. MS-B Acknowledges Paging Broadcast (ACK)", "Reverse Control Channel [RCC]", '#16A34A', 'arrow'),
        (4.1, 8.0, 5.6, "7. BS-2 Relays Paging ACK to MSC", "Wired MSC Backhaul", '#475569', 'arrow'),
        (3.3, 5.6, 3.2, "8a. MSC Allocates Voice Channel Pair (FVC/RVC-1)", "Core Resource Allocation", '#2563EB', 'arrow'),
        (2.6, 5.6, 8.0, "8b. MSC Allocates Voice Channel Pair (FVC/RVC-2)", "Core Resource Allocation", '#2563EB', 'arrow'),
        (1.9, 3.2, 1.0, "9a. Order to tune to FVC/RVC-1", "FCC Order", '#0284C7', 'arrow'),
        (1.9, 8.0, 10.2, "9b. Alert / Ringing + Tune to FVC/RVC-2", "FCC Alert", '#0284C7', 'arrow'),
        (0.9, 1.0, 10.2, "10. Full-Duplex Active Conversation Established (MS-A <---> MS-B)", "FVC / RVC Dedicated Voice Channels", '#059669', 'duplex')
    ]

    for y, x1, x2, desc, channel, color, stype in steps:
        if stype == 'self':
            rect = patches.FancyBboxPatch((x1-2.2, y-0.3), 4.4, 0.6, boxstyle="round,pad=0.08",
                                          facecolor='#EDE9FE', edgecolor='#7C3AED', linewidth=1.2, zorder=3)
            ax.add_patch(rect)
            ax.text(x1, y, desc, ha='center', va='center', color='#5B21B6', weight='bold', fontsize=8.5)
        elif stype == 'duplex':
            ax.annotate('', xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle='<->', color=color, lw=2.5), zorder=2)
            # Text box with white background so lifeline does not cross text
            tbox = dict(boxstyle='round,pad=0.25', facecolor='#ECFDF5', edgecolor=color, linewidth=1.2)
            ax.text((x1+x2)/2, y+0.25, desc, ha='center', va='bottom', color=color, weight='bold', fontsize=9, bbox=tbox)
            ax.text((x1+x2)/2, y-0.28, f"[{channel}]", ha='center', va='top', color='#065F46', fontsize=8, style='italic', weight='bold')
        else:
            ax.annotate('', xy=(x2, y), xytext=(x1, y),
                        arrowprops=dict(arrowstyle='->', color=color, lw=1.8), zorder=2)
            mid = (x1 + x2) / 2
            ax.text(mid, y+0.16, desc, ha='center', va='bottom', color='#1E293B', weight='bold', fontsize=8.2)
            ax.text(mid, y-0.16, f"[{channel}]", ha='center', va='top', color=color, fontsize=7.6, style='italic', weight='bold')

    ax.set_xlim(-0.2, 11.4)
    ax.set_ylim(0.2, 11.5)
    ax.axis('off')
    plt.title("Step-by-Step Call Establishment Flow Between Two Mobile Stations (MS-to-MS)", 
              fontsize=13.5, weight='bold', pad=15, color='#0F172A')
    
    out_path = os.path.join(OUT_DIR, "fig_call_setup_flow.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

# ==============================================================================
# FIG 2: Regular Polygons Tessellation & Coverage Geometry
# ==============================================================================
def generate_fig2_geometry():
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.8), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    
    shapes = [
        ("Equilateral Triangle", 3, r"$A = \frac{3\sqrt{3}}{4} R^2 \approx 1.299 R^2$", "50.0% Relative Area", '#EF4444', 30),
        ("Square", 4, r"$A = 2 R^2 = 2.000 R^2$", "77.0% Relative Area", '#F59E0B', 45),
        ("Regular Hexagon", 6, r"$A = \frac{3\sqrt{3}}{2} R^2 \approx 2.598 R^2$", "100.0% (Maximum / Optimal)", '#10B981', 30)
    ]
    
    R = 1.0
    for ax, (title, n_sides, formula, eff, color, rot) in zip(axes, shapes):
        ax.set_facecolor('#F8FAFC')
        ax.set_aspect('equal')
        
        # Draw circumscribed circle (antenna isotropic range R)
        circ = plt.Circle((0, 0), R, color='#94A3B8', fill=False, linestyle='--', linewidth=1.5, label='Circle of Radius R')
        ax.add_patch(circ)
        
        # Calculate polygon vertices
        angles = np.linspace(0, 2*np.pi, n_sides, endpoint=False) + np.radians(rot)
        x_pts = R * np.cos(angles)
        y_pts = R * np.sin(angles)
        poly = patches.Polygon(np.column_stack([x_pts, y_pts]), closed=True, 
                               facecolor=color, alpha=0.25, edgecolor=color, linewidth=2.5)
        ax.add_patch(poly)
        
        # Radius line
        ax.plot([0, x_pts[0]], [0, y_pts[0]], color='#0F172A', linewidth=1.6, linestyle='-')
        ax.scatter([0], [0], color='#0F172A', s=35, zorder=5)
        ax.text(x_pts[0]*0.5, y_pts[0]*0.5 + 0.08, "R", ha='center', va='bottom', fontsize=11, weight='bold', color='#0F172A')
        
        ax.set_xlim(-1.35, 1.35)
        ax.set_ylim(-1.35, 1.35)
        ax.axis('off')
        
        # Titles and stats
        ax.text(0, 1.22, title, ha='center', va='center', fontsize=12, weight='bold', color='#1E293B')
        ax.text(0, -1.15, formula, ha='center', va='center', fontsize=10.5, color='#0F172A')
        
        # Badge for efficiency
        badge_box = dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.9, edgecolor='none')
        ax.text(0, -1.35, eff, ha='center', va='center', fontsize=9.5, weight='bold', color='white', bbox=badge_box)

    fig.suptitle("Comparison of Plane-Tessellating Polygons for Cellular Footprint Design", 
                 fontsize=14, weight='bold', y=1.02, color='#0F172A')
    
    out_path = os.path.join(OUT_DIR, "fig_cell_geometry_tessellation.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

# ==============================================================================
# FIG 3: S/I Ratio vs. Cluster Size N Trade-off Curve
# ==============================================================================
def generate_fig3_sir_curve():
    fig, ax = plt.subplots(figsize=(10.5, 6.2), dpi=300)
    ax.set_facecolor('#F8FAFC')
    fig.patch.set_facecolor('#FFFFFF')
    
    # Continuous range of N
    N_cont = np.linspace(1, 22, 500)
    
    # Formula: S/I = (1/6) * (sqrt(3N))^k
    # S/I (dB) = 10 * log10( (1/6) * (3N)^(k/2) )
    sir_k3_cont = 10 * np.log10((1/6) * (3 * N_cont)**(1.5))
    sir_k4_cont = 10 * np.log10((1/6) * (3 * N_cont)**(2.0))
    
    ax.plot(N_cont, sir_k3_cont, label=r'Path Loss $k = 3$ (Light Urban / Free-Space)', color='#2563EB', linewidth=2.5)
    ax.plot(N_cont, sir_k4_cont, label=r'Path Loss $k = 4$ (Standard Urban)', color='#10B981', linewidth=2.5)
    
    # Discrete valid cluster sizes: N = i^2 + ij + j^2
    valid_N = [1, 3, 4, 7, 9, 12, 13, 19]
    for n in valid_N:
        val_k3 = 10 * np.log10((1/6) * (3 * n)**(1.5))
        val_k4 = 10 * np.log10((1/6) * (3 * n)**(2.0))
        ax.scatter([n], [val_k3], color='#1D4ED8', s=45, zorder=4)
        ax.scatter([n], [val_k4], color='#047857', s=45, zorder=4)
        
        # Position labels cleanly without collisions
        if n == 1:
            ax.text(n + 0.35, val_k3 + 0.3, "N=1", ha='left', va='bottom', fontsize=8, color='#1E40AF', weight='bold')
        elif n == 12:
            ax.text(n - 0.4, val_k3 - 1.5, "N=12", ha='right', va='top', fontsize=8, color='#991B1B', weight='bold')
        elif n == 13:
            ax.text(n + 0.4, val_k3 - 1.5, "N=13", ha='left', va='top', fontsize=8, color='#1E40AF', weight='bold')
        else:
            ax.text(n, val_k3 - 1.4, f"N={n}", ha='center', va='top', fontsize=8, color='#1E40AF', weight='bold')

    # Draw 15 dB threshold line
    ax.axhline(15, color='#DC2626', linestyle='--', linewidth=1.8, label=r'Exam Threshold: $S/I \geq 15\ \mathrm{dB}$')
    
    # Highlight exact intersection for k=3: N = 11.01 -> N = 12
    val_12_k3 = 10 * np.log10((1/6) * (36)**1.5)
    ax.scatter([12], [val_12_k3], color='#DC2626', s=130, edgecolors='#7F1D1D', linewidth=2, zorder=6)
    
    ax.annotate(r'$\mathbf{Minimum\ Valid\ N = 12}$ for $k=3$' + '\n' + r'$(S/I = 15.38\ \mathrm{dB} \geq 15\ \mathrm{dB})$',
                xy=(12, val_12_k3), xytext=(12.5, 7.5),
                arrowprops=dict(facecolor='#DC2626', shrink=0.08, width=1.5, headwidth=7),
                bbox=dict(boxstyle="round,pad=0.45", facecolor='#FEE2E2', edgecolor='#DC2626', linewidth=1.2),
                fontsize=9.5, color='#991B1B', weight='bold')

    # Highlight N = 7 for k=4
    val_7_k4 = 10 * np.log10((1/6) * (21)**2)
    ax.scatter([7], [val_7_k4], color='#047857', s=110, edgecolors='#064E3B', linewidth=2, zorder=6)
    ax.annotate(r'$N = 7$ for $k=4$' + '\n' + r'$(S/I = 18.66\ \mathrm{dB} \geq 15\ \mathrm{dB})$',
                xy=(7, val_7_k4), xytext=(3.5, 23.0),
                arrowprops=dict(facecolor='#047857', shrink=0.08, width=1.5, headwidth=7),
                bbox=dict(boxstyle="round,pad=0.4", facecolor='#D1FAE5', edgecolor='#10B981', linewidth=1.2),
                fontsize=9, color='#065F46', weight='bold')

    ax.set_xlabel("Cluster Size $N$ (Compact Pattern Size)", fontsize=11, weight='bold', color='#1E293B')
    ax.set_ylabel("Signal-to-Interference Ratio $S/I$ (dB)", fontsize=11, weight='bold', color='#1E293B')
    ax.set_title(r"Worst-Case Signal-to-Interference Ratio ($S/I$) vs. Cluster Size ($N$) for $i_0 = 6$ Co-Channel Cells", 
                 fontsize=12, weight='bold', pad=12, color='#0F172A')
    
    ax.set_xlim(0.5, 21.0)
    ax.set_ylim(-1.5, 28)
    ax.set_xticks(valid_N)
    ax.grid(True, linestyle=':', alpha=0.6, color='#94A3B8')
    ax.legend(loc='lower right', frameon=True, facecolor='#FFFFFF', edgecolor='#CBD5E1', fontsize=9.5)
    
    out_path = os.path.join(OUT_DIR, "fig_sir_vs_cluster_size.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

# ==============================================================================
# FIG 4: 1G vs 2G MAHO Handoff Comparison Architecture
# ==============================================================================
def generate_fig4_handoff():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6.8), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    
    for ax in [ax1, ax2]:
        ax.set_facecolor('#F8FAFC')
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')

    # Panel 1: 1G Network-Controlled Handoff (NCHO)
    ax1.text(5, 9.4, "1G Handoff: Network-Controlled (NCHO)", ha='center', va='center',
             fontsize=12, weight='bold', color='#991B1B')
    
    # 1G Flow boxes with ample vertical spacing for clean arrows
    box_1g = [
        (5, 7.8, "Base Station (BS)", "Monitors Uplink Reverse Voice Channel (RVC)\nSignal Strength continuously", '#FEE2E2', '#DC2626'),
        (5, 5.7, "Mobile Switching Centre (MSC)", "Central Coordinator: MSC polls surrounding BSs\nto measure MS signal & deduce relative location", '#FEF3C7', '#D97706'),
        (5, 3.6, "Centralized Decision & Switching", "MSC selects target cell & switches voice channel\nExecution Latency: 5 to 10 seconds", '#FEE2E2', '#DC2626'),
        (5, 1.4, "Critical Bottleneck", "Heavy CPU loading at central MSC\nCannot support small cells / microcells", '#450A0A', '#991B1B')
    ]
    for x, y, title, desc, bg, border in box_1g:
        text_color = 'white' if border == '#991B1B' and bg == '#450A0A' else '#1E293B'
        rect = patches.FancyBboxPatch((x-4.2, y-0.7), 8.4, 1.4, boxstyle="round,pad=0.12",
                                      facecolor=bg, edgecolor=border, linewidth=1.8)
        ax1.add_patch(rect)
        ax1.text(x, y+0.32, title, ha='center', va='center', weight='bold', fontsize=10, color=border if text_color != 'white' else 'white')
        ax1.text(x, y-0.22, desc, ha='center', va='center', fontsize=8.5, color=text_color)

    ax1.annotate('', xy=(5, 6.4), xytext=(5, 7.1), arrowprops=dict(arrowstyle='->', lw=2.2, color='#DC2626'))
    ax1.annotate('', xy=(5, 4.3), xytext=(5, 5.0), arrowprops=dict(arrowstyle='->', lw=2.2, color='#DC2626'))
    ax1.annotate('', xy=(5, 2.1), xytext=(5, 2.9), arrowprops=dict(arrowstyle='->', lw=2.2, color='#991B1B'))

    # Panel 2: 2G Mobile-Assisted Handoff (MAHO)
    ax2.text(5, 9.4, "2G Handoff: Mobile-Assisted (MAHO)", ha='center', va='center',
             fontsize=12, weight='bold', color='#065F46')
             
    box_2g = [
        (5, 7.8, "Mobile Station (MS)", "Measures Downlink Beacons (FCC)\nof neighboring BSs during idle TDMA slots", '#D1FAE5', '#059669'),
        (5, 5.7, "Serving Base Station Controller (BSC)", "MS continuously reports RSSI measurements\nBSC detects handoff threshold without MSC intervention", '#DBEAFE', '#2563EB'),
        (5, 3.6, "Distributed Decision & Swift Execution", "BSC reallocates channel directly between BTSs\nExecution Latency: Tens of milliseconds", '#D1FAE5', '#059669'),
        (5, 1.4, "Key Architectural Triumph", "MSC CPU relieved of continuous monitoring\nEnables dense microcells & picocells", '#064E3B', '#047857')
    ]
    for x, y, title, desc, bg, border in box_2g:
        text_color = 'white' if border == '#047857' and bg == '#064E3B' else '#1E293B'
        rect = patches.FancyBboxPatch((x-4.2, y-0.7), 8.4, 1.4, boxstyle="round,pad=0.12",
                                      facecolor=bg, edgecolor=border, linewidth=1.8)
        ax2.add_patch(rect)
        ax2.text(x, y+0.32, title, ha='center', va='center', weight='bold', fontsize=10, color=border if text_color != 'white' else 'white')
        ax2.text(x, y-0.22, desc, ha='center', va='center', fontsize=8.5, color=text_color)

    ax2.annotate('', xy=(5, 6.4), xytext=(5, 7.1), arrowprops=dict(arrowstyle='->', lw=2.2, color='#059669'))
    ax2.annotate('', xy=(5, 4.3), xytext=(5, 5.0), arrowprops=dict(arrowstyle='->', lw=2.2, color='#059669'))
    ax2.annotate('', xy=(5, 2.1), xytext=(5, 2.9), arrowprops=dict(arrowstyle='->', lw=2.2, color='#047857'))

    fig.suptitle("Architectural Evolution: 1G Network-Controlled vs. 2G Mobile-Assisted Handoff (MAHO)", 
                 fontsize=13.5, weight='bold', y=1.01, color='#0F172A')
    
    out_path = os.path.join(OUT_DIR, "fig_handoff_1g_vs_2g.png")
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated: {out_path}")

if __name__ == '__main__':
    generate_fig1_call_setup()
    generate_fig2_geometry()
    generate_fig3_sir_curve()
    generate_fig4_handoff()
