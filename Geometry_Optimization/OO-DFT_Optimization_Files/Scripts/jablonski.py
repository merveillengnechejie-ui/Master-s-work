import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

# ─────────────────────────────────────────────────────────────────────────────
# Utilitaire : gaussienne normalisée
# ─────────────────────────────────────────────────────────────────────────────
def gaussian(x, center, width, amplitude):
    return amplitude * np.exp(-((x - center) ** 2) / (2 * width ** 2))

# Style commun
BG_COLOR = '#e8e8f0'

# =============================================================================
# FIGURE 1 — Absorption Spectra Comparison
# =============================================================================
def plot_absorption_spectra():
    wl = np.linspace(200, 1000, 2000)

    # ── BODIPY-ref : pics à ~290, ~340, ~500 nm ──────────────────────────────
    bodipy = (gaussian(wl, 290, 12, 0.080) +
              gaussian(wl, 340, 12, 0.120) +
              gaussian(wl, 500, 18, 0.450))

    # ── I-BODIPY : pics à ~300, ~350, ~420, ~675 nm ──────────────────────────
    i_bodipy = (gaussian(wl, 300, 13, 0.063) +
                gaussian(wl, 350, 13, 0.053) +
                gaussian(wl, 420, 18, 0.100) +
                gaussian(wl, 675, 38, 0.385))

    # ── TPP-I-BODIPY : pics à ~310, ~355, ~425, ~710 nm ─────────────────────
    tpp = (gaussian(wl, 310, 13, 0.055) +
           gaussian(wl, 355, 13, 0.052) +
           gaussian(wl, 425, 18, 0.092) +
           gaussian(wl, 710, 45, 0.350))

    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    # Zones NIR
    ax.axvspan(600, 950, color='wheat',      alpha=0.45, label='NIR-I window')
    ax.axvspan(750, 850, color='lightgreen', alpha=0.45, label='Optimal NIR-I')

    # Courbes
    ax.plot(wl, bodipy,  color='steelblue',   lw=2.0, label='BODIPY-ref')
    ax.plot(wl, i_bodipy, color='darkorange', lw=2.0, label='I-BODIPY')
    ax.plot(wl, tpp,     color='forestgreen', lw=2.0, label='TPP-I-BODIPY')

    # Lignes verticales pointillées aux maxima
    for center, color in [(500, 'steelblue'), (675, 'darkorange'), (710, 'forestgreen')]:
        ax.axvline(center, color=color, lw=1.0, linestyle='--', alpha=0.7)
    for center, color in [(290, 'steelblue'), (340, 'steelblue'),
                          (300, 'darkorange'), (350, 'darkorange'), (420, 'darkorange'),
                          (310, 'forestgreen'), (355, 'forestgreen'), (425, 'forestgreen')]:
        ax.axvline(center, color=color, lw=0.8, linestyle='--', alpha=0.5)

    ax.set_xlim(200, 1000)
    ax.set_ylim(-0.01, 0.50)
    ax.set_xlabel('Wavelength (nm)', fontsize=13)
    ax.set_ylabel('Absorption Intensity (a.u.)', fontsize=13)
    ax.set_title('Absorption Spectra Comparison', fontsize=15, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10, framealpha=0.9)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig('absorption_spectra_comparison.png', dpi=300, bbox_inches='tight',
                facecolor=BG_COLOR)
    print("✓ absorption_spectra_comparison.png")
    plt.close()


# =============================================================================
# FIGURE 2 — Energy Level Diagram (S0, S1, T1)
# =============================================================================
def plot_energy_levels():
    # Données énergétiques (eV)
    molecules = {
        'BODIPY-ref': {'S0': 0.0, 'S1': 2.46, 'T1': 2.10},
        'I-BODIPY':   {'S0': 0.0, 'S1': 1.82, 'T1': 1.75},
        'TPP-I-BODIPY':{'S0': 0.0, 'S1': 1.74, 'T1': 1.68},
    }
    delta_ST = {'BODIPY-ref': 0.380, 'I-BODIPY': 0.070, 'TPP-I-BODIPY': 0.060}

    fig, ax = plt.subplots(figsize=(13, 7))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor('#dde0ee')

    x_positions = {'BODIPY-ref': 1.0, 'I-BODIPY': 3.5, 'TPP-I-BODIPY': 6.0}
    bar_half = 0.55
    colors = {'S0': 'blue', 'S1': 'red', 'T1': 'green'}

    for mol, levels in molecules.items():
        xc = x_positions[mol]

        # Niveaux horizontaux
        for state, energy in levels.items():
            ax.hlines(energy, xc - bar_half, xc + bar_half,
                      colors=colors[state], linewidths=3.5)
            ax.text(xc + bar_half + 0.05, energy, state,
                    va='center', fontsize=10, color='black')

        # Flèche verticale S1→S0
        s1 = levels['S1']
        ax.annotate('', xy=(xc, 0.02), xytext=(xc, s1 - 0.02),
                    arrowprops=dict(arrowstyle='->', color='purple',
                                   lw=2.5, mutation_scale=18))
        ax.text(xc + 0.08, s1 / 2, f"{s1:.2f} eV",
                ha='left', va='center', fontsize=9, color='purple', rotation=90)

        # Flèche courbe S1→T1 (ISC) pour BODIPY-ref
        if mol == 'BODIPY-ref':
            ax.annotate('', xy=(xc + 0.3, levels['T1']),
                        xytext=(xc + 0.05, levels['S1']),
                        arrowprops=dict(arrowstyle='->', color='orange',
                                       lw=1.8, connectionstyle='arc3,rad=-0.4'))

        # ΔE_ST annotation
        dst = delta_ST[mol]
        y_mid = (levels['S1'] + levels['T1']) / 2
        ax.text(xc + bar_half + 1.05, y_mid + 0.06,
                f'ΔE_ST\n{dst:.3f} eV',
                fontsize=8, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow',
                          edgecolor='gray', alpha=0.85))

        # Étiquette molécule en bas
        ax.text(xc, -0.38, mol, ha='center', fontsize=11, fontweight='bold')

    # Légende manuelle
    handles = [mpatches.Patch(color='blue',  label='S₀'),
               mpatches.Patch(color='red',   label='S₁'),
               mpatches.Patch(color='green', label='T₁')]
    ax.legend(handles=handles, loc='upper right', fontsize=10)

    ax.set_xlim(0, 8.5)
    ax.set_ylim(-0.5, 2.7)
    ax.set_ylabel('Relative Energy (eV)', fontsize=12)
    ax.set_title('Energy Level Diagram (S₀, S₁, T₁)', fontsize=14, fontweight='bold')
    ax.set_xticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.grid(axis='y', color='white', alpha=0.6, lw=0.8)

    plt.tight_layout()
    plt.savefig('energy_levels_diagram.png', dpi=300, bbox_inches='tight',
                facecolor=BG_COLOR)
    print("✓ energy_levels_diagram.png")
    plt.close()


# =============================================================================
# FIGURE 3 — Diagramme de Jablonski : I-BODIPY
# =============================================================================
def plot_jablonski():
    fig, ax = plt.subplots(figsize=(10, 9))
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor(BG_COLOR)

    # Niveaux d'énergie
    E_S0 = 0.0
    E_S1 = 1.82
    E_T1 = 1.75

    # Positions x
    x_S0  = (0.3, 1.3)   # S0
    x_S1  = (0.8, 1.8)   # S1
    x_T1  = (2.5, 3.5)   # T1

    lw = 4

    # Traits des niveaux
    ax.hlines(E_S0, *x_S0, colors='blue',  linewidths=lw)
    ax.hlines(E_S1, *x_S1, colors='red',   linewidths=lw)
    ax.hlines(E_T1, *x_T1, colors='darkgreen', linewidths=lw)

    # Labels des niveaux
    ax.text(0.28, E_S0 - 0.09, 'S$_o$', fontsize=14, fontweight='bold', color='black')
    ax.text(0.75, E_S1 + 0.04, 'S$_1$', fontsize=14, fontweight='bold', color='black')
    ax.text(2.48, E_T1 + 0.04, 'T$_1$', fontsize=14, fontweight='bold', color='black')

    # Énergie en eV sur les niveaux
    ax.text(0.28, E_S1,  f'{E_S1:.2f} eV', fontsize=9,
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='red', alpha=0.9))
    ax.text(3.52, E_T1, f'{E_T1:.2f} eV',  fontsize=9,
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='green', alpha=0.9))

    # ── Flèche Absorption (S0→S1) ─────────────────────────────────────────────
    ax.annotate('', xy=(1.05, E_S1 - 0.02), xytext=(1.05, E_S0 + 0.02),
                arrowprops=dict(arrowstyle='->', color='purple', lw=2.5,
                                mutation_scale=20))
    ax.text(0.72, E_S0 + 0.3, 'Absorption\n(hν)',
            fontsize=9, ha='center',
            bbox=dict(boxstyle='round', facecolor='white', edgecolor='black', alpha=0.8))

    # ── Flèche IC/VR interne (tirets rouges) ─────────────────────────────────
    ax.annotate('', xy=(1.20, E_S0 + 0.15), xytext=(1.20, E_S1 - 0.05),
                arrowprops=dict(arrowstyle='->', color='salmon', lw=1.5,
                                linestyle='dashed', mutation_scale=15))

    # ── Flèche Fluorescence (tirets cyan) ────────────────────────────────────
    ax.annotate('', xy=(1.35, E_S0 + 0.15), xytext=(1.35, E_S1 - 0.05),
                arrowprops=dict(arrowstyle='->', color='cyan', lw=1.5,
                                linestyle='dashed', mutation_scale=15))
    ax.text(1.42, 0.85, 'Fluorescence', fontsize=8, color='darkcyan',
            bbox=dict(boxstyle='round', facecolor='lightcyan', edgecolor='cyan', alpha=0.8))

    # ── IC/VR label ──────────────────────────────────────────────────────────
    ax.text(1.22, 1.2, 'IC/VT', fontsize=8, color='salmon', rotation=90)

    # ── Flèche ISC courbe (S1→T1) ────────────────────────────────────────────
    ax.annotate('', xy=(2.5, E_T1), xytext=(1.8, E_S1),
                arrowprops=dict(arrowstyle='->', color='darkorange', lw=2.0,
                                connectionstyle='arc3,rad=-0.25',
                                mutation_scale=16))

    # ── Box ISC ──────────────────────────────────────────────────────────────
    ax.text(2.05, 2.05,
            'ISC\nSOC=120.5 cm⁻¹',
            fontsize=9, ha='center',
            bbox=dict(boxstyle='round', facecolor='wheat', edgecolor='darkorange', alpha=0.9))

    # ── ΔE_ST annotation ─────────────────────────────────────────────────────
    ax.text(2.05, (E_S1 + E_T1) / 2 - 0.02,
            'ΔE_ST = 0.070 eV',
            fontsize=9, ha='center',
            bbox=dict(boxstyle='round', facecolor='yellow', edgecolor='olive', alpha=0.85))

    # ── Flèche Phosphorescence (tirets verts) ────────────────────────────────
    ax.annotate('', xy=(3.0, E_S0 + 0.15), xytext=(3.0, E_T1 - 0.05),
                arrowprops=dict(arrowstyle='->', color='limegreen', lw=1.5,
                                linestyle='dashed', mutation_scale=15))
    ax.text(2.75, 0.85, 'Phosphorescence', fontsize=8, color='darkgreen',
            bbox=dict(boxstyle='round', facecolor='lightgreen', edgecolor='green', alpha=0.8))

    ax.set_xlim(0.0, 4.2)
    ax.set_ylim(-0.5, 2.6)
    ax.set_ylabel('Energy (eV)', fontsize=12)
    ax.set_title('Jablonski Diagram: I-BODIPY', fontsize=14, fontweight='bold')
    ax.set_xticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.grid(axis='y', color='white', alpha=0.5, lw=0.8)

    plt.tight_layout()
    plt.savefig('jablonski_I_BODIPY.png', dpi=300, bbox_inches='tight',
                facecolor=BG_COLOR)
    print("✓ jablonski_I_BODIPY.png")
    plt.close()


# =============================================================================
# Main
# =============================================================================
if __name__ == '__main__':
    plot_absorption_spectra()
    plot_energy_levels()
    plot_jablonski()
    print("\nToutes les figures ont été générées avec succès.")
