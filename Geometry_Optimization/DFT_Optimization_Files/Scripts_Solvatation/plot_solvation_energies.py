#!/usr/bin/env python3
"""
Plot Solvation Energies - BODIPY, Iodo-BODIPY, TPP-BODIPY
==========================================================
Reproduit le graphique des énergies de solvatation CPCM et SMD CDS.

Dépendances : matplotlib, numpy
    pip install matplotlib numpy
"""

import matplotlib.pyplot as plt
import numpy as np

# ── Données ──────────────────────────────────────────────────────────────────
molecules = ['BODIPY', 'Iodo-BODIPY', 'TPP-BODIPY']

cpcm_values = [-13.164837, -15.305188, -57.812263]   # kcal/mol (énergie diélectrique CPCM)
smd_values  = [5.97321,    5.14586,    10.86420]      # kcal/mol (énergie SMD CDS)

# ── Couleurs (reproduit l'image originale) ────────────────────────────────────
colors_cpcm = ['#4c6e8a', '#3a7d7a', '#5bbf6e']   # bleu-gris, teal, vert
colors_smd  = ['#4b2e83', '#c2547a', '#e8956d']   # violet, rose, saumon

# ── Style seaborn-like ────────────────────────────────────────────────────────
plt.rcParams.update({
    'axes.facecolor':    '#eaeaf2',
    'figure.facecolor':  'white',
    'axes.grid':         True,
    'grid.color':        'white',
    'grid.linewidth':    1.0,
    'axes.spines.top':   False,
    'axes.spines.right': False,
    'axes.spines.left':  False,
    'axes.spines.bottom':False,
    'xtick.bottom':      False,
    'ytick.left':        False,
    'font.size':         11,
})

x = np.arange(len(molecules))
bar_width = 0.5

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# ── Panneau 1 : CPCM ─────────────────────────────────────────────────────────
bars1 = ax1.bar(x, cpcm_values, width=bar_width, color=colors_cpcm)

ax1.set_title('CPCM Dielectric Energy (eV)', fontsize=13, pad=12)
ax1.set_xlabel('Molecule', fontsize=11)
ax1.set_ylabel('Energy (eV)', fontsize=11)
ax1.set_xticks(x)
ax1.set_xticklabels(molecules, rotation=45, ha='right')
ax1.set_ylim(-62, 2)
ax1.axhline(0, color='white', linewidth=1.2)

# Étiquettes sur les barres
for bar, val in zip(bars1, cpcm_values):
    ax1.text(
        bar.get_x() + bar.get_width() / 2,
        val - 1.5,
        f'{val:.2f}',
        ha='center', va='top',
        fontsize=11, fontweight='bold', color='black'
    )

# ── Panneau 2 : SMD ──────────────────────────────────────────────────────────
bars2 = ax2.bar(x, smd_values, width=bar_width, color=colors_smd)

ax2.set_title('SMD CDS Energy (kcal/mol)', fontsize=13, pad=12)
ax2.set_xlabel('Molecule', fontsize=11)
ax2.set_ylabel('Energy (kcal/mol)', fontsize=11)
ax2.set_xticks(x)
ax2.set_xticklabels(molecules, rotation=45, ha='right')
ax2.set_ylim(0, 12)

# Étiquettes sur les barres
for bar, val in zip(bars2, smd_values):
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        val + 0.15,
        f'{val:.2f}',
        ha='center', va='bottom',
        fontsize=11, fontweight='bold', color='black'
    )

plt.tight_layout()
plt.savefig('solvation_energies.png', dpi=300, bbox_inches='tight')
print("Image sauvegardée : solvation_energies.png")
plt.show()
