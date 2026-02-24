#HEK293 + NT/CT Plasmid → Lipofection (18.12.)
#→ 3w Blasticidin → NT: survived ✓ | CT: toxic ✗

# imports
import matplotlib.pyplot as plt
import numpy as np

#darkmode
#plt.style.use("dark_background")

# PHASE 2: Transfection Survival MIT ACHSEN
fig, ax = plt.subplots(1,1, figsize=(9,7))

# data from labbook
days = np.array([0, 25, 35])  # 18.12. → 12.01. → 24.02. (35 Tage)
nt_cells = np.array([100, 95, 90])   # NT: stable cell line ~90-100% (ng/μL equivalent)
ct_cells = np.array([100, 20, 0])    # CT: crashout after selection

# PLOT with lines and markers
ax.plot(days, nt_cells, "o-", color="#2ECC71", linewidth=4, markersize=12,
        label="NT Clone", markerfacecolor="white", markeredgewidth=2)
ax.plot(days, ct_cells, "o-", color="#E74C3C", linewidth=4, markersize=12,
        label="CT Clone", markerfacecolor="white", markeredgewidth=2)

# achses
ax.set_xlabel("Time since lipofection (days)", fontsize=14, fontweight="bold")
ax.set_ylabel("relative cell concentration (%)", fontsize=14, fontweight="bold")
ax.set_title("Phase 2: Blasticidin Selection Survival Curve",
             fontsize=16, fontweight="bold", pad=20)

# achses + GRID
ax.set_xlim(-2, 38)
ax.set_ylim(-5, 105)
ax.grid(True, alpha=0.3, linestyle="--")
ax.legend(fontsize=12, loc="lower left", frameon=True, fancybox=True, shadow=True)

#anotations with specific lab data
ax.annotate("Lipofection\nNT/CT equal", xy=(0,100), xytext=(2, 50), fontweight="bold",
            arrowprops=dict(arrowstyle="->", color="black", lw=1.5), fontsize=11,
            bbox = dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

# Pfeil 1: Zu NT-Kurve (grün)
ax.annotate("", xy=(25, 90), xytext=(20, 60),  # xy=NT-Punkt, xytext=Text-Position
            arrowprops=dict(arrowstyle="->", color="black", lw=2), fontsize=11,
            bbox = dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))


# Pfeil 2: Zu CT-Kurve (rot)
ax.annotate("", xy=(25, 20), xytext=(20, 60),  # xy=CT-Punkt, xytext=Text-Position
            arrowprops=dict(arrowstyle="->", color="black", lw=2), fontsize=12)

# Text ohne Pfeil (mittig positioniert)
ax.annotate("3w Blasticidin\nNT: 95%\nCT: 20%", xy=(20, 60), fontsize=11,
            ha="center", va="center", fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

ax.annotate("Today\nNT stable", xy=(35, 90), xytext=(30, 75), fontweight="bold",
            arrowprops=dict(arrowstyle="->", color="black", lw=2), fontsize=11,
            bbox = dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

# design
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_linewidth(1.2)
ax.spines['bottom'].set_linewidth(1.2)

plt.tight_layout()
plt.savefig("phase2_survival_final.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()
