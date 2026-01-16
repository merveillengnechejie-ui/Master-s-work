# Rapport : Calcul des écarts d'énergie Singlet-Triplet (ΔE_ST)

Ce rapport présente les calculs de $\Delta E_{ST} = E_{S1} - E_{T1}$ pour les molécules BODIPY, Iodo-BODIPY et TPP-BODIPY.

## Détails des Énergies

Les énergies $E_{S1}$ sont extraites du dossier `OO-DFT_SH` (exécutions `HOMO_to_LUMO`) et les énergies $E_{T1}$ sont extraites du dossier `Etats_triplets`.

### Tableau récapitulatif

| Molécule | $E_{S1}$ (Eh) | $E_{T1}$ (Eh) | $\Delta E_{ST}$ (Eh) | $\Delta E_{ST}$ (eV) |
| :--- | :---: | :---: | :---: | :---: |
| **BODIPY** | -680.57645203 | -680.51579242 | -0.06065961 | -1.6506 |
| **Iodo-BODIPY** | -1274.77934655 | -1274.72147278 | -0.05787377 | -1.5748 |
| **TPP-BODIPY** | -1715.13321165 | -1715.08784531 | -0.04536635 | -1.2345 |

> [!NOTE]
> 1 Hartree (Eh) ≈ 27.2114 eV.
> Les valeurs de $\Delta E_{ST}$ obtenues sont négatives, ce qui indique que l'état singlet extrait est plus stable (énergie plus basse) que l'état triplet extrait dans ces calculs spécifiques.

## Fichiers sources utilisés

- **BODIPY**: 
  - $E_{S1}$: `OO-DFT_SH/BODIPY_SH/S1_guess_runs/HOMO_to_LUMO/test_HOMO_to_LUMO.out`
  - $E_{T1}$: `Etats_triplets/BODIPY_Triplets/BODIPY_T1.out`
- **Iodo-BODIPY**:
  - $E_{S1}$: `OO-DFT_SH/Iodo_SH/S1_guess_runs/HOMO_to_LUMO/test_HOMO_to_LUMO.out`
  - $E_{T1}$: `Etats_triplets/Iodo_Triplets/Iodo_T1.out`
- **TPP-BODIPY**:
  - $E_{S1}$: `OO-DFT_SH/TPP-BODIPY_SH/S1_guess_runs/HOMO_to_LUMO/test_HOMO_to_LUMO.out`
  - $E_{T1}$: `Etats_triplets/TPP_Triplets/TPP_Bodipy_T1.out`
