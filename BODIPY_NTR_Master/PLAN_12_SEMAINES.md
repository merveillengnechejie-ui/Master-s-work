# Plan de Travail — 12 Semaines
## BODIPY-NTR pour PDT/PTT ciblée TNBC

---

## Vue d'ensemble

```
Sem 1   : Installation + validation chaîne
Sem 2   : Construction molécules + xTB (Tier 0)
Sem 3   : Optimisation S₀ + sTDA (Tier 1)
Sem 4-5 : Benchmark TD-DFT 6 fonctionnelles (Tier 2)
Sem 6   : Protocole NTR ON/OFF + optimisation T₁
Sem 7   : Δ-DFT ΔE_ST + SOC (Tier 2.5)
Sem 8   : Scoring PDT/PTT + Go/No-Go
Sem 9   : Rédaction sections Introduction + Méthodes
Sem 10  : Rédaction Résultats + figures
Sem 11  : Discussion + Conclusion
Sem 12  : Finalisation + soutenance
```

> **Principe de chevauchement** : Les calculs longs (Tier 2, sem 4–5) tournent en arrière-plan pendant que vous rédigez la bibliographie et préparez les inputs suivants. Ne pas attendre la fin d'un calcul pour commencer la tâche suivante.

---

## Semaine 1 — Installation et validation

**Objectifs** :
- Installer ORCA 6.1.1, xTB 6.6, RDKit, Multiwfn
- Vérifier sTDA et CC2 dans ORCA 6.1.1
- Corriger bug `SMDSolvent "mixed"` → `"water"`
- Test de chaîne sur BODIPY-Ph (λ_max cible ~505 nm)
- Créer convention de nommage + `.gitignore`

**Protocole** : [`protocols/P1_installation_verification.md`](protocols/P1_installation_verification.md)

**Livrable** : `SEMAINE1_RAPPORT_VALIDATION.md`

**Temps calcul** : ~2 h (test de chaîne)

---

## Semaine 2 — Construction des molécules + Tier 0

**Objectifs** :
- Construire les 8 molécules avec Avogadro/IQmol → `.xyz`
- Pré-optimisation GFN2-xTB + ALPB water pour les 8 molécules
- Construire `data/experimental_benchmark.csv`
- Vérifier dans les articles : ΦT Baig 2024, η Bartusik-Aebisher 2025

**Protocole** : [`protocols/P2_construction_molecules.md`](protocols/P2_construction_molecules.md)

**Livrable** : 8 fichiers `.xyz` validés + `results/xTB_screening.csv`

**Temps calcul** : ~0.5 h (xTB très rapide)

---

## Semaine 3 — Optimisation S₀ + sTDA (Tiers 0→1)

**Objectifs** :
- Optimisation S₀ gaz + CPCM/SMD-water (B3LYP-D3/def2-SVP)
- Lancer 4 calculs gaz en parallèle, puis 4 en eau
- sTDA-PBE0/def2-SVP pour criblage rapide λ_max
- Validation fréquences (pas de fréquences imaginaires)

**Protocole** : [`protocols/P3_optimisation_S0.md`](protocols/P3_optimisation_S0.md)

**Livrable** : `S0_*_water_opt.gbw/.xyz` pour 8 molécules + `results/sTDA_screening.csv`

**Temps calcul** : ~10 h mur (S₀ × 8 molécules × 2 solvants)

---

## Semaines 4–5 — Benchmark TD-DFT 6 fonctionnelles (Tier 2)

**Objectifs** :
- TD-DFT vertical avec 6 fonctionnelles × 8 molécules
- `StateSpecificSolvation true` obligatoire pour toutes les excitations
- Comparer avec `data/experimental_benchmark.csv`
- Sélectionner la meilleure fonctionnelle (MAE < 0.2 eV)

**Protocole** : [`protocols/P4_benchmark_TDDFT.md`](protocols/P4_benchmark_TDDFT.md)

**Livrable** : `results/TDDFT_benchmark.csv` + `results/functional_benchmark.md`

**Temps calcul** : ~36 h mur (6 fonctionnelles × 8 mol × ~3 h, 4 parallèles)

> **Conseil** : Lancer les calculs le soir. Préparer les inputs le matin, lancer à 18h, analyser le lendemain matin. Pendant que les calculs tournent, rédiger la section État de l'art du mémoire.

---

## Semaine 6 — Protocole NTR ON/OFF + optimisation T₁

**Objectifs** :
- Optimisation T₁ (UUKS/PBE0/def2-SVP + SMD-water, **équilibre**) pour les 6 molécules NTR (ON + OFF)
- TD-DFT comparatif ON vs OFF avec la meilleure fonctionnelle sélectionnée en sem 4–5
- Extraire Δλ_max, Δf pour chaque paire

**Protocole** : [`protocols/P5_protocole_NTR_ON_OFF.md`](protocols/P5_protocole_NTR_ON_OFF.md)

**Livrable** : `results/NTR_activation.csv`

**Temps calcul** : ~20 h mur (T₁ × 6 mol × ~2 h + TD-DFT ON/OFF)

---

## Semaine 7 — Δ-DFT ΔE_ST + SOC

**Objectifs** :
- ΔROKS/PBE0/def2-SVP + ptSS-PCM pour ΔE_ST précis (8 molécules ON+OFF)
- ΔDFT+SOC/PBE0/ZORA pour constantes SOC
- Analyse MEP + charges Hirshfeld (Multiwfn) pour TPP-Iodo-BODIPY

**Protocole** : [`protocols/P6_Delta_DFT_SOC.md`](protocols/P6_Delta_DFT_SOC.md)

**Livrable** : `results/deltaDFT_results.csv` + `results/SOC_results.csv`

**Temps calcul** : ~20 h mur (Δ-DFT × 8 mol × ~4 h + SOC × 8 mol × ~1 h)

---

## Semaine 8 — Scoring PDT/PTT + Grille Go/No-Go

**Objectifs** :
- Calculer PDT_Score, PTT_Score, Synergy_Score pour toutes les molécules
- Analyse de sensibilité ±20% sur les poids
- Appliquer grille Go/No-Go (seuil ≥ 70%)
- Sélectionner top 3 candidats

**Protocole** : [`protocols/P7_scoring_PDT_PTT.md`](protocols/P7_scoring_PDT_PTT.md)

**Livrable** : `results/PDT_PTT_synergy.csv` + feuille de scoring

**Temps calcul** : ~2 h (calcul Python, pas de QM)

---

## Semaines 9–10 — Rédaction (sections 1–4)

**Semaine 9** :
- Introduction : TNBC → hypoxie → NTR → BODIPY → gap computationnel
- État de l'art : 2–3 pages, citer Bartusik-Aebisher 2025, Baig 2024, Overchuk 2023
- Théorie/Méthodes : cascade xTB→sTDA→TD-DFT→Δ-DFT→SOC, justification exclusion ADC(2)

**Semaine 10** :
- Résultats : benchmarking TD-DFT, activation NTR ON/OFF, ΔE_ST, SOC, scoring
- Figures prioritaires :
  1. Scaffold BODIPY + mécanisme NTR (OFF→ON)
  2. Parity plot TD-DFT (6 fonctionnelles vs expérience)
  3. Scatter ΔE_ST vs SOC (coloré Type I/II)
  4. Overlay spectres ON/OFF top 3 candidats
  5. Heatmap synergy scoring

**Livrable** : Draft sections 1–4

---

## Semaine 11 — Discussion + Conclusion

**Objectifs** :
- Relier résultats aux défis cliniques TNBC
- Documenter les limitations (proxies PTT, poids exploratoires, pas d'expérience)
- Perspectives : lien avec Roadmap NTR complet (Tiers 1–8, 310 molécules)
- Mentionner cibles de publication : JCTC (72–78%) + JCIM (75–82%)

**Livrable** : Rapport complet (draft final)

---

## Semaine 12 — Finalisation + Soutenance

- Correction rapport + mise en forme
- Présentation 15–20 diapositives
- Répétition soutenance
- Archivage GitHub final

**Livrable** : Rapport final + présentation orale

---

## Budget temps total

| Phase | Méthode | Temps mur estimé |
|-------|---------|-----------------|
| xTB Tier 0 | GFN2-xTB × 8 mol | ~0.5 h |
| sTDA Tier 1 | sTDA-PBE0 × 8 mol | ~1 h |
| S₀ opt | B3LYP-D3/def2-SVP × 8 mol × 2 | ~10 h |
| TD-DFT Tier 2 | 6 fonctionnelles × 8 mol | ~36 h |
| T₁ opt | UKS PBE0 × 8 mol (ON+OFF) | ~16 h |
| Δ-DFT Tier 2.5 | ΔROKS × 8 mol (ON+OFF) | ~16 h |
| SOC | ΔDFT+SOC × 8 mol | ~8 h |
| **Total nominal** | | **~88 h mur** |
| **Avec buffer +30%** | | **~115 h mur** |

À 8 h/jour de calcul continu : **~14 jours de calcul** répartis sur 7 semaines (sem 3–9).
