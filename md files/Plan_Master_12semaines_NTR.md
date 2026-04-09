# Plan Master 12 Semaines — BODIPY-NTR pour TNBC
## Restructuration intégrant Research_Paper_Roadmap_BODIPY_NTR.md

**Dernière mise à jour** : Avril 2026  
**Contraintes matérielles** : 32 GB RAM, 4–8 cœurs (local)  
**Logiciels** : ORCA 6.1.1, xTB 6.6, RDKit 2024, Multiwfn 3.8+, Python 3.10+

---

## Principe de la restructuration

Le Roadmap NTR cible une publication JCTC/JCIM sur **310 molécules** en **18–20 semaines** avec une cascade Tier 1–8 (incluant TSH-MD via Newton-X 2.2). Le projet Master dispose de **12 semaines** et doit produire un **mémoire de Master 2** solide.

La stratégie : exécuter les **Tiers 1–4 du Roadmap NTR** sur une **mini-bibliothèque de 20–30 molécules** centrée sur l'activation NTR. Cela produit des résultats originaux publiables, cohérents avec la méthodologie ΔDFT+SOC déjà maîtrisée, et positionne le travail comme **fondation du projet de publication** complet.

### Ce qui est retenu du Roadmap NTR
- Concept NTR (nitroreductase) comme trigger hypoxie → activation ON/OFF
- Cascade xTB → sTDA → TD-DFT → Δ-DFT (Tiers 1–4)
- Protocole dual-state nitro (OFF) / amine (ON)
- Synergy scoring PDT/PTT (version simplifiée)
- Benchmarking fonctionnelles TD-DFT (6 fonctionnelles)
- Solvation non-équilibre ptSS-PCM pour excitations verticales

### Ce qui est reporté (hors portée 12 semaines)
- TSH-MD / Newton-X 2.2 (Tier 7) → 40–80 h/molécule, trop coûteux
- SOS-CIS(D) et DLPNO-STEOM-CCSD (Tiers 4.5 et 8) → réservés à la publication
- SF-TDDFT + CI-NEB (Tier 6) → reporté en perspectives
- Bibliothèque complète 310 molécules → réduite à 20–30 molécules justifiées
- MD classique AMBER 22 → reporté

---

## Molécules cibles (20–30 molécules, catégories A+B+E du Roadmap)

| # | Molécule | Catégorie NTR | Trigger | Rôle |
|---|----------|--------------|---------|------|
| 1 | BODIPY-Ph (référence) | A | — | Benchmarking expérimental |
| 2 | BODIPY-Ph-NO₂ (meso) | E | Ph-NO₂ | Forme OFF (NTR prodrug) |
| 3 | BODIPY-Ph-NH₂ (meso) | E | Ph-NH₂ | Forme ON (activée) |
| 4 | Iodo-BODIPY | B | — | SOC élevé, PDT de référence |
| 5 | Iodo-BODIPY-Ph-NO₂ | B+E | Ph-NO₂ | OFF : atome lourd + NTR |
| 6 | Iodo-BODIPY-Ph-NH₂ | B+E | Ph-NH₂ | ON : atome lourd + NTR activé |
| 7 | TPP-Iodo-BODIPY | B | — | Ciblage mitochondrial (projet initial) |
| 8–15 | Variants 3,5-NMe₂ / Br / aza-BODIPY | C+B | ±NO₂ | Extension NIR-I, criblage rapide |

**Total recommandé** : 8 molécules prioritaires (1–7 + 1 aza-BODIPY) + 8–12 variants si le temps le permet.

---

## Planning 12 semaines

### Semaine 1 — Installation + validation de la chaîne + bibliographie ciblée

**Objectifs** :
- Installer et tester ORCA 6.1.1, xTB 6.6, RDKit, Multiwfn
- Vérifier la disponibilité de CC2 dans ORCA 6.1.1 via `%mdci Method CC2` (item bloquant du Roadmap NTR)
- Vérifier que `! STDA` fonctionne dans ORCA 6.1.1 (Tier 1 du Roadmap)
- Corriger le bug `SMDSolvent "mixed"` → remplacer par `SMDSolvent "water"` dans tous les inputs archivés
- Lecture ciblée : Baig 2024 (I-BODIPY TSH-MD), Bartusik-Aebisher 2025 (design BODIPY), Alkhatib 2022 (benchmark 36 fonctionnelles)
- Créer la convention de nommage : `{molecule}_{state}_{tier}_{attempt}.{ext}` (ex: `IodoBODIPY_NO2_S0_T2_opt.xyz`)

**Livrables** :
- Rapport de validation chaîne (1 page)
- `environment.yml` + `.gitignore` (exclure `*.gbw`, `*.tmp`, `*.densities`)
- Structure de répertoires créée (voir section Organisation)

---

### Semaine 2 — Construction bibliothèque + pré-optimisation xTB (Tier 0)

**Objectifs** :
- Construire les 8 molécules prioritaires via Avogadro/IQmol → fichiers `.xyz`
- Pré-optimisation GFN2-xTB avec solvation ALPB water :
  ```bash
  xtb molecule.xyz --opt tight --gfn 2 --alpb water > xtb_opt.out
  ```
- Extraire HOMO-LUMO gap, dipôle, flexibilité (proxy PTT) → `results/xTB_screening.csv`
- Construire `data/experimental_benchmark.csv` : extraire λ_max, Φ_f, Φ_Δ depuis Ponte 2018, Baig 2024, Porolnik 2024, Sandoval 2023
- Vérifier les valeurs : ΦT = 0.85 et Φ_Δ = 0.99 (Baig 2024), η = 61–66% pour tBu (Bartusik-Aebisher 2025)

**Livrables** :
- 8 fichiers `.xyz` validés (géométries xTB)
- `data/experimental_benchmark.csv`
- `results/xTB_screening.csv`

---

### Semaine 3 — Optimisation S₀ + sTDA screening (Tiers 0→1)

**Objectifs** :
- Optimisation S₀ en phase gaz puis CPCM/SMD-water pour les 8 molécules (B3LYP-D3/def2-SVP)
- Lancer les 8 calculs gaz en parallèle (2 jobs × 4 cœurs)
- sTDA-PBE0/def2-SVP pour screening rapide λ_max (Tier 1 du Roadmap) :

```orca
! RKS PBE0 def2-SVP AutoAux RIJCOSX TightSCF
! STDA
! CPCM(water)
%pal nprocs 4 end
%maxcore 6000
%cpcm
  SMD true
  SMDSolvent "water"
end
%tddft
  n_roots 10
  DoNTOs true
end
* xyzfile 0 1 S0_opt.xyz
```

- Validation fréquences (pas de fréquences imaginaires)

**Livrables** :
- `S0_*_water_opt.gbw` et `.xyz` pour les 8 molécules
- `results/sTDA_screening.csv` (λ_max, f, ΔE_ST estimé)

---

### Semaines 4–5 — Benchmark TD-DFT 6 fonctionnelles (Tier 2 du Roadmap)

**Objectifs** :
- TD-DFT vertical sur les 8 molécules avec **6 fonctionnelles** (Tier 2 du Roadmap NTR) :

| Fonctionnelle | Type | Justification |
|---|---|---|
| ωB97X-D | Range-separated | Meilleure pour états CT |
| CAM-B3LYP | Range-separated | Bonne pour S₁ BODIPY |
| PBE0 | Global hybrid | Standard littérature |
| B3LYP | Global hybrid | Baseline Baig 2024 |
| M06-2X | Meta-hybrid | Meilleure 2PA (Elayan 2025) |
| MN15 | Meta-hybrid | Meilleure λ_max (Elayan 2025) |

- Utiliser **ptSS-PCM non-équilibre** pour toutes les excitations verticales :
  ```orca
  %cpcm
    SMD true
    SMDSolvent "water"
    StateSpecificSolvation true
  end
  ```
- Comparer avec `data/experimental_benchmark.csv` → MAE, RMSE, R²
- Cible : MAE < 0.2 eV ; sélectionner la meilleure fonctionnelle

**Temps estimé** : 8 mol × 6 fonctionnelles × ~3 h = ~144 h → 4 jobs parallèles → ~36 h (~2 jours continus)

**Livrables** :
- `results/TDDFT_benchmark.csv`
- `results/functional_benchmark.md` (parity plots, recommandation fonctionnelle)

---

### Semaines 5–6 — Protocole dual-state NTR : ON/OFF (Tier 2.5 du Roadmap)

**Objectifs** :
- Calculer chaque molécule NTR dans les deux états : nitro (OFF) et amine (ON)
- Extraire : Δλ_max, Δ(ΔE_ST), ΔSOC, Δf → quantifier le switch photophysique
- Optimisation T₁ (ΔUKS/PBE0/def2-SVP + SMD-water) pour les 8 molécules :

```orca
! Opt UKS PBE0 D3BJ def2-SVP TightSCF RIJCOSX
! CPCM(water)
%pal nprocs 4 end
%maxcore 7000
%cpcm
  SMD true
  SMDSolvent "water"
end
%scf
  HFTyp UKS
  SCF_ALGORITHM DIIS_TRAH
  MaxIter 500
end
* xyz 0 3
[COORDINATES]
*
```

- Calcul ΔE_ST adiabatique : E(S₁, géom S₁) − E(T₁, géom T₁)
- Classification PDT Type I vs Type II (multi-critères) :
  - ΔE_ST < 0.12 eV → Type I (préféré en hypoxie)
  - SOC > 20 cm⁻¹ ET T₁ > 0.98 eV → Type II (¹O₂)
  - Rapporter comme score continu (0–1), pas binaire

**Livrables** :
- `results/NTR_activation.csv` (Δλ_max ON/OFF pour les 8 molécules)
- `results/PDT_mechanism.csv` (Type I/II score)

---

### Semaine 7 — Δ-DFT pour ΔE_ST + SOC (Tier 2.5 + SOC du Roadmap)

**Objectifs** :
- ΔROKS/PBE0/def2-SVP + ptSS-PCM pour ΔE_ST précis (MAE < 0.05 eV) sur les 8 molécules :

```orca
! ROKS PBE0 D3BJ def2-SVP RIJCOSX TightSCF
! CPCM(water)
%pal nprocs 4 end
%maxcore 7000
%cpcm
  SMD true
  SMDSolvent "water"
  StateSpecificSolvation true
end
%scf
  HFTyp ROKS
  SCF_ALGORITHM DIIS_TRAH
  MaxIter 500
end
* xyzfile 0 3
[T1 COORDINATES]
*
```

- ΔDFT+SOC perturbatif (ZORA, PBE0) pour constantes SOC :

```orca
! UKS PBE0 D3BJ def2-SVP ZORA RIJCOSX AutoAux TightSCF
! CPCM(water)
%tddft
  dosoc true
  SOCROTs 20
end
```

- Valeurs cibles : SOC > 50 cm⁻¹ (avec I), > 30 cm⁻¹ (avec Br), < 10 cm⁻¹ (sans atome lourd)
- Analyse MEP + charges Hirshfeld (Multiwfn) pour TPP-Iodo-BODIPY

**Livrables** :
- `results/deltaDFT_results.csv` (ΔE_ST Δ-DFT pour 8 molécules ON+OFF)
- `results/SOC_results.csv` (constantes SOC cm⁻¹)
- Rapport ciblage mitochondrial TPP-Iodo-BODIPY

---

### Semaine 8 — Scoring PDT/PTT + grille Go/No-Go

**Objectifs** :
- Appliquer le scoring synergique du Roadmap NTR (version simplifiée) :

```
PDT_Score = 0.30·(¹O₂_propensity) + 0.30·(SOC/100) + 0.25·(T1_energy/1.5) + 0.15·f_S1
PTT_Score = 0.40·(non_radiative_propensity) + 0.35·(flexibility_index) + 0.25·(twist_factor)
Synergy_Score = 0.35·PDT_Score + 0.35·PTT_Score + 0.30·(PDT_Score × PTT_Score)
```

- Analyse de sensibilité ±20% sur les poids (obligatoire pour la publication)
- Appliquer la grille Go/No-Go (seuil ≥ 70%) :

| Critère | Iodo-BODIPY-NO₂ (OFF) | Iodo-BODIPY-NH₂ (ON) | Poids |
|---|---|---|---|
| λ_max NIR-I (650–750 nm) | — | 680–720 nm | 25% |
| ΔE_ST | — | < 0.05 eV | 25% |
| SOC | — | > 50 cm⁻¹ | 20% |
| Δλ_max ON/OFF | > 20 nm | — | 15% |
| E_ad | — | < 1.0 eV | 15% |

- Sélectionner le(s) candidat(s) le(s) plus prometteur(s) (score ≥ 70% = Go)

**Livrables** :
- `results/PDT_PTT_synergy.csv`
- Feuille de scoring + recommandation finale (top 3 candidats)

---

### Semaines 9–10 — Rédaction rapport (sections 1–4)

**Semaine 9** : Introduction + État de l'art + Théorie/Méthodes
- Introduction : TNBC → hypoxie → NTR → BODIPY → gap computationnel → ce travail
- Méthodes : cascade xTB → sTDA → TD-DFT → Δ-DFT → SOC ; justification exclusion ADC(2) (6 raisons du Roadmap NTR, Appendice D)
- Positionner par rapport au Roadmap NTR : ce mémoire = Tiers 1–4 sur mini-bibliothèque = fondation du projet de publication

**Semaine 10** : Résultats
- Benchmarking TD-DFT (6 fonctionnelles vs expérience)
- Activation NTR : Δλ_max, ΔΔE_ST, ΔSOC pour les 8 molécules
- Grille Go/No-Go + scoring synergique
- Figures prioritaires :
  1. Scaffold BODIPY + mécanisme NTR (OFF → ON)
  2. Parity plot TD-DFT (calc. vs exp. λ_max, 6 fonctionnelles)
  3. Scatter ΔE_ST vs SOC (coloré par Type I/II)
  4. Overlay spectres ON/OFF pour top 3 candidats
  5. Heatmap synergy scoring

**Livrables** : Draft sections 1–4

---

### Semaine 11 — Discussion + conclusion + perspectives

**Objectifs** :
- Relier résultats computationnels aux défis cliniques TNBC :
  - Hypoxie → NTR upregulé 3–8× → activation sélective ON/OFF
  - Type I PDT préféré en hypoxie (ΔE_ST < 0.12 eV)
  - Ciblage mitochondrial (TPP⁺) → accumulation dans cellules TNBC
- Limitations à documenter explicitement :
  - Pas de couplage vibronique (positions de bande, pas de formes)
  - Proxies PTT non validés expérimentalement
  - Poids synergiques exploratoires (analyse de sensibilité fournie)
  - Pas de validation expérimentale (synthèse/biologie)
- Perspectives (lien direct avec Roadmap NTR complet) :
  - Extension à 310 molécules (Tiers 1–8 complets)
  - TSH-MD via Newton-X 2.2 pour ΦT, Φf, kISC prédits
  - SOS-CIS(D) + DLPNO-STEOM-CCSD pour validation gold-standard
  - Collaboration expérimentale (synthèse + tests MDA-MB-231)
  - Cibles de publication : JCTC (72–78%) + JCIM (75–82%)

**Livrables** : Rapport complet (draft final)

---

### Semaine 12 — Finalisation + soutenance

- Correction rapport + mise en forme
- Préparation présentation (15–20 diapositives)
- Répétition soutenance
- Archivage final GitHub : tous `.gbw`, `.out`, `.xyz`, `.csv`, scripts Python

**Livrables** : Rapport final + présentation orale

---

## Tableau de risques (adapté du Roadmap NTR)

| Risque | Probabilité | Impact | Action |
|--------|------------|--------|--------|
| sTDA non disponible dans ORCA 6.1.1 | Faible | Moyen | Fallback : `! TDDFT` + `TDA true` |
| S₁ ΔSCF ne converge pas | Moyen | Moyen | Plan B après 5 tentatives : T₁ + SOC suffisants ; utiliser `./run_troubleshoot_S1.sh` |
| TD-DFT MAE > 0.3 eV (toutes fonctionnelles) | Faible | Élevé | Publier comme finding ; ajouter DSD-BLYP comme 7ème fonctionnelle |
| `SMDSolvent "mixed"` dans anciens inputs | Certain | Moyen | Corriger en `SMDSolvent "water"` dès semaine 1 (bug documenté dans Roadmap NTR) |
| Δλ_max ON/OFF < 10 nm | Faible | Élevé | Redesigner trigger (azo, disulfure) ; rapporter comme limitation de design |
| Retard cumulatif | Moyen | Moyen | Réduire à 5 molécules prioritaires (1–6 du tableau) + référence |
| Poids synergiques contestés par jury | Moyen | Faible | Analyse de sensibilité ±20% fournie ; labelliser "exploratoire" |

---

## Organisation des fichiers

```
Master-s-work/
├── data/
│   ├── library_NTR_8mol.csv        # 8 molécules prioritaires (SMILES + catégorie)
│   ├── experimental_benchmark.csv  # λ_max, Φ_f, Φ_Δ depuis littérature
│   └── substitution_map.md
├── calculations/
│   ├── tier0_xtb/
│   ├── tier1_stda/
│   ├── tier2_tddft/
│   │   ├── wB97X-D/
│   │   ├── CAM-B3LYP/
│   │   ├── PBE0/
│   │   ├── B3LYP/
│   │   ├── M06-2X/
│   │   └── MN15/
│   ├── tier25_deltadft/
│   └── soc/
├── results/
│   ├── xTB_screening.csv
│   ├── sTDA_screening.csv
│   ├── TDDFT_benchmark.csv
│   ├── functional_benchmark.md
│   ├── deltaDFT_results.csv
│   ├── NTR_activation.csv
│   ├── PDT_mechanism.csv
│   ├── SOC_results.csv
│   ├── PDT_PTT_synergy.csv
│   └── top_candidates.md
├── figures/
├── scripts/
│   ├── parse_orca_tddft.py         # Parser ORCA (Roadmap NTR Appendice C.3)
│   └── generate_stda_inputs.py     # Générateur batch inputs sTDA
├── manuscript/
│   └── memoire_master2.tex
└── .gitignore                      # *.gbw, *.tmp, *.densities, *.bigtmp
```

---

## Comparaison avec les deux plans précédents

| Aspect | Plan 14 sem. (original) | Plan 12 sem. (v1) | Plan 12 sem. NTR (ce plan) |
|---|---|---|---|
| Molécules | 3 (Ref + Iodo + TPP-Iodo) | 3 | 8 (+ variants NTR) |
| Concept central | PDT/PTT BODIPY | PDT/PTT BODIPY | PDT/PTT + **activation NTR hypoxie** |
| λ_max | ADC(2)/def2-TZVP | TD-DFT/ωB97X-D3 | **TD-DFT 6 fonctionnelles** (benchmark) |
| Solvation excitations | SMD-mixed (bug) | SMD-water | **ptSS-PCM non-équilibre** (correct) |
| ΔE_ST | ΔUKS/B3LYP | ΔUKS/B3LYP | **ΔROKS/PBE0 + ptSS-PCM** (MAE < 0.05 eV) |
| Protocole ON/OFF | Non | Non | **Oui** (nitro ↔ amine, Δλ_max, ΔSOC) |
| Scoring synergique | Non | Non | **Oui** (PDT_Score + PTT_Score + γ) |
| Lien publication | Non | Non | **Oui** (fondation Roadmap NTR JCTC/JCIM) |
| NEVPT2 | Optionnel | Supprimé | Supprimé (reporté Tier 8) |
| TSH-MD | Non | Non | Reporté (hors portée 12 sem.) |

---

## Budget temps total (32 GB RAM, 4 cœurs)

| Phase | Méthode | Molécules | Temps/mol | Temps mur (4 parallèles) |
|---|---|---|---|---|
| xTB (Tier 0) | GFN2-xTB | 8 | 2 min | ~0.1 h |
| sTDA (Tier 1) | sTDA-PBE0/def2-SVP | 8 | 10 min | ~0.3 h |
| TD-DFT (Tier 2) | 6 fonctionnelles/def2-SVP | 8 | ~3 h | ~36 h |
| T₁ opt | UKS PBE0/def2-SVP | 8 (ON+OFF) | ~2 h | ~8 h |
| Δ-DFT (Tier 2.5) | ΔROKS/PBE0/def2-SVP | 8 (ON+OFF) | ~4 h | ~16 h |
| SOC | ΔDFT+SOC ZORA | 8 (ON+OFF) | ~1 h | ~4 h |
| S₀ opt | B3LYP-D3/def2-SVP | 8 | ~1 h | ~2 h |
| **Total** | | | | **~66 h mur** (~3–4 jours continus) |

Avec buffer +50% pour convergence S₁ et re-runs : **~100 h mur réaliste** (~2 semaines à 8 h/jour).

---

*Ce plan constitue les Tiers 1–4 du Research_Paper_Roadmap_BODIPY_NTR.md appliqués à une mini-bibliothèque de 8 molécules. Les résultats obtenus seront directement réutilisables dans le projet de publication complet (Tiers 1–8, 310 molécules).*
