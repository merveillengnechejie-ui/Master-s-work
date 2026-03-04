# Résumé Exécutif : Comparaison TD-DFT vs OO-DFT/ΔDFT et Aide-Mémoire Pratique

> **Mise à jour : 04 mars 2026 (260304)**
> - Exécution locale 16 Go RAM / TD-DFT ωB97X-D3
> - Configuration : 4 cœurs, %maxcore 3500
> - Tous les calculs en milieu biologique complexe (SMD mixed)

> **Rappel méthodologique (à lire en première minute) :**
>
> - Pour les émissions CT en solution, privilégier un modèle de solvatation état-spécifique non-équilibre (ptSS-PCM).
> - Fonctionnelles recommandées : OT-ωB97M-V (ΔUKS/ΔROKS), PBE0 (ΔUKS robuste), PBE38-D4 (robustesse E_em).
> - Méthode IMOM conseillée pour les systèmes ICT (dimères / transfert de charge intermoléculaire).
> - Cibles de benchmarking : ΔE_{ST} MAE < 0,05 eV ; λ_max / E_em MAE ≤ 0,1 eV ; R² > 0.90.
> - **ΔDFT+SOC** remplace NEVPT2 pour gain de temps (10×) et cohérence méthodologique.
> - **Validation étendue** avec ensemble de BODIPY de référence.
> - **Exécution locale** : 16 Go RAM, 4 cœurs, séquentiel (nohup)

**Thématique du stage** : Optimisation de nanoparticules de BODIPY pour une thérapie combinée photodynamique et photothermique ciblée sur les cellules de cancer du sein triple négatif.

---

## Partie 1 : Tableau Comparatif Détaillé TD-DFT vs OO-DFT/ΔDFT

| Aspect | TD-DFT (Ancien) | OO-DFT/ΔDFT (Nouveau) | Avantage pour BODIPY |
|:---|:---|:---|:---|
| **Théorie** | Réponse linéaire, oscillateur | Orbitales optimisées, état spécifique | ★★★★★ ΔDFT |
| **Précision S₁** | Surestime (erreur +0.3-0.5 eV) | Précision chimique (<0.05 eV) | ★★★★★ ΔDFT |
| **Précision T₁** | Sous-estime (erreur -0.3-0.5 eV) | Précision chimique (<0.05 eV) | ★★★★★ ΔDFT |
| **ΔE_ST** | Mauvais (erreur > 0.5 eV) | Excellent (erreur < 0.05 eV) | ★★★★★ ΔDFT |
| **λ_max** | Acceptable si bien calibré | Excellent (surtout avec ADC(2)) | ★★★★ Hybride |
| **Relaxation orbitale** | Non capturée (LR-TDDFT) | Explicitement capturée | ★★★★★ ΔDFT |
| **Doubles excitations** | Partiellement (RPA) | Implicites (meilleur traitement) | ★★★★ ΔDFT |
| **États CT** | Surcharge (charge-transfer band problématique) | Meilleur traitement | ★★★★ ΔDFT |
| **Coût computationnel** | Bas-Moyen | Moyen-Élevé (ΔUKS/ΔROKS rapides) | ★★★ TD-DFT pour screening |
| **SOC intégré** | Oui, mais imprécis | Non (nécessite méthode MR, mais ΔDFT+SOC possible) | ★★★★★ ΔDFT+SOC |
| **Compatibilité CPCM** | Oui (LR-PCM) | Oui (SS-PCM, meilleur) | ★★★ ΔDFT |
| **Applicabilité BODIPY** | ⚠ Problématique (open-shell character) | ★★★★★ Idéale | ★★★★★ ΔDFT |
| **SOC calcul** | TD-DFT (rapide, imprécis) | ΔDFT+SOC (rapide, plus cohérent) | ★★★★★ ΔDFT+SOC |
| **Validation étendue** | Limitée | Ensemble de BODIPY, R², MAE, RMSE | ★★★★★ ΔDFT |
| **Exécution locale** | Possible (16 Go) | Possible (16 Go, 4 cœurs) | ★★★★★ Adapté |

---

## Partie 2 : Protocole de Calcul Recommandé (Résumé Exécutif)

### Stratégie en 7 étapes (portée révisée : 1 référence + 2 prototypes)

**Configuration locale (16 Go RAM, 4 cœurs) :**
```
%maxcore 3500
%pal nprocs 4 end
```

```
ÉTAPE 1 (rapide)     → S0 optimisation (DFT, phase gaz)
                       ⏱ 30-60 min, B3LYP-D3/def2-SVP
        ↓
ÉTAPE 2 (rapide)     → S0 optimisation (DFT, SMD mixed)
                       ⏱ 45-90 min, B3LYP-D3/def2-SVP
        ↓
ÉTAPE 3 (rapide)     → Excitation verticale (TD-DFT/ωB97X-D3/def2-SVP)
                       ⏱ 15-30 min, λ_max screening
        ↓
ÉTAPE 4 (moyen)      → T1 optimisation (ΔUKS, SMD mixed)
                       ⏱ 60-120 min, robuste
        ↓
ÉTAPE 5 (très cher)  → S1 optimisation (ΔSCF, SMD mixed)
                       ⏱ 120-180 min, +200-300% buffer
        ↓
ÉTAPE 6 (moyen)      → SOC (ΔDFT+SOC - ZORA, dosoc)
                       ⏱ 30-60 min, cohérent
        ↓
ÉTAPE 7              → Analyse MEP/ciblage pour TPP-BODIPY
                       ⏱ 5-15 min, Multiwfn
        ↓
ANALYSE & DÉCISION   → Grille Go/No-Go, scoring prototypes
```

*Test comparatif def2-SVP vs def2-TZVP en semaine 3 sur référence pour optimiser*

### Flux des données

```
S0_opt.gbw (Étape 2)
    ├─→ TDDFT_vertical.inp  (Étape 3) → λ_max, spectrum
    ├─→ T1_opt.inp         (Étape 4) → E_T1, geometry
    ├─→ S1_opt.inp         (Étape 5) → E_S1, ΔE_ST
    ├─→ SOC_opt.inp        (Étape 6) → SOC matrix (ΔDFT+SOC)
    └─→ MEP_analysis.inp   (Étape 7) → Charges, ciblage

Résultats:
  E_ad = E_S0 - E_S1         (PTT potential)
  ΔE_ST = E_S1 - E_T1        (ISC/PDT potential)
  k_{ISC} via SOC            (PDT efficiency)
  PSI = (k_{ISC} + k_f) / (k_{nr} + k_{dég})  (photostabilité)
  TCI = k_{nr} / (k_f + k_{ISC})              (conversion PTT)
```

---

## Partie 3 : Guide de Sélection des Prototypes (Grille Go/No-Go Révisée)

### Portée (révisée : 1 référence + 2 prototypes)

| Molécule | Rôle | Calculs complets |
|:---|:---|:---|
| **Référence expérimentale** | Benchmarking uniquement | Non |
| **Prototype 1 : Iodo-BODIPY** | PDT optimisée | Oui |
| **Prototype 2 : TPP-Iodo-BODIPY** | Théranostique ciblé | Oui |

### Critères d'évaluation quantitatifs

#### Prototype 1 : Iodo-BODIPY (PDT optimisée)

| Critère | Cible | Poids | Calcul ORCA |
|:---|:---|:---|:---|
| **λ_max (absorption)** | 680-720 nm (NIR-I) | 25% | TD-DFT (ωB97X-D3) |
| **E_adiabatic (PTT)** | < 1.0 eV | 15% | ΔE_S0-S1 |
| **ΔE_ST (ISC/PDT)** | < 0.05 eV | 25% | ΔE_S1-T1 |
| **SOC (ISC speed)** | > 50 cm⁻¹ | 25% | ΔDFT+SOC |
| **Photostabilité** | PSI > 1 | 10% | Calculs k |

#### Prototype 2 : TPP-Iodo-BODIPY (théranostique ciblé)

| Critère | Cible | Poids | Calcul ORCA |
|:---|:---|:---|:---|
| **λ_max (absorption)** | 690-730 nm (NIR-I) | 20% | TD-DFT (ωB97X-D3) |
| **E_adiabatic (PTT)** | < 1.2 eV | 15% | ΔE_S0-S1 |
| **ΔE_ST (ISC/PDT)** | < 0.08 eV | 20% | ΔE_S1-T1 |
| **SOC (ISC speed)** | > 40 cm⁻¹ | 15% | ΔDFT+SOC |
| **Ciblage mitochondrial** | Quantitatif | 30% | MEP + affinité |

#### Critères de ciblage mitochondrial (Prototype 2)

| Critère | Valeur | Méthode |
|:---|:---|:---|
| Charge TPP⁺ | +1,00 e (idéalement +1 à +2) | Analyse Hirshfeld (Multiwfn) |
| Distance TPP⁺ → centre BODIPY | > 5 Å | Géométrie (Multiwfn/VMD) |
| Angle dièdre TPP⁺-BODIPY | > 90° | Angle dièdre (Multiwfn) |
| Potentiel membranaire ΔΨ | > 150 mV | Calcul affinité |
| Coefficient P_app | > 10⁻⁶ cm/s | Perméabilité |
| Ratio accumulation | ≥ 10 | [TPP-BODIPY]_mito/[TPP-BODIPY]_cyto |
| Énergie liaison membrane | ≥ -20 kcal/mol | Docking |

### Tableau de scoring (Grille Go/No-Go)

```
Prototype      | λ_max | E_ad | ΔE_ST | SOC | Ciblage | TOTAL  | Verdict
---------------|-------|------|-------|-----|---------|--------|----------
Référence      |  /25  |  /15 |  /25  |  /25|  /10    | /100   | Benchmark
Iodo-BODIPY    |  /25  |  /15 |  /25  |  /25|  /10    | /100   | ≥ 70% = Go
TPP-Iodo-BODIPY|  /20  |  /15 |  /20  |  /15|  /30    | /100   | ≥ 70% = Go
```

**Règles de scoring :**
- λ_max ∈ [680-720] (Iodo) : 25/25 ; ∈ [690-730] (TPP-Iodo) : 20/25 ; hors NIR : ≤ 10/25
- E_ad < 0.8 : 15/15 ; < 1.0 : 12/15 (Iodo) ; < 1.2 : 15/15 (TPP-Iodo)
- ΔE_ST < 0.05 : 25/25 ; < 0.08 : 20/25 ; > 0.15 : < 10/25
- SOC > 100 : 25/25 (Iodo) ; > 50 : 20/25 ; > 40 : 15/15 (TPP-Iodo) ; < 10 : < 5/25
- Ciblage (TPP-Iodo) : Score basé sur critères quantitatifs (30/30 maximum)

---

## Partie 4 : Aide-Mémoire Pratique (A4 à Imprimer)

### Pour démarrer (Exécution Locale)

```bash
# 1. Vérifier ORCA accessible
which orca
orca -v

# 2. Créer les répertoires de travail (3 molécules: 1 ref + 2 prototypes)
mkdir -p {reference,iodo,tpp-iodo}/{S0,S1,T1,TDDFT,SOC,MEP}

# 3. Copier les fichiers d'entrée depuis Corine_codes/
cp ../Corine_codes/S0_gas_opt.inp reference/
cp ../Corine_codes/S0_water_opt.inp reference/

# 4. Lancer les calculs (local, 4 cœurs, 16 Go RAM)
orca S0_gas_opt.inp > S0_gas_opt.out &

# 5. Surveiller (nohup pour sessions longues)
tail -f S0_gas_opt.out
```

### Commandes clés ORCA

| Action | Commande |
|:---|:---|
| Lancer calcul | `orca input.inp > output.out &` |
| Voir progression | `tail -f output.out` |
| Extraire énergie | `grep "FINAL SINGLE POINT" output.out` |
| Voir λ_max (TD-DFT) | `grep "STATE 1:" output.out` |
| Vérifier SOC | `grep -A5 "Spin-Orbit" output.out` |
| Converger géométrie | `grep "Geometry convergence" output.out` |
| Vérifier fréquences | `grep "imaginary frequencies" output.out` |
| Voir charges atomiques | `Multiwfn S0_water_opt.out` |

### Conversions utiles

```
λ_max (nm) = 1240 eV·nm / E (eV)

ΔE (eV) = E (a.u.) × 27.211

E (cm⁻¹) = E (eV) × 8066

PSI (Photostabilité) = (k_ISC + k_f) / (k_nr + k_dég)

TCI (Conversion Thermique) = k_nr / (k_f + k_ISC)
```

### Signaux d'alerte (Troubleshooting)

| Signal | Cause probable | Action |
|:---|:---|:---|
| SCF ne converge pas | Géométrie mauvaise | Revoir XYZ, réduire MaxStep |
| Fréquences imaginaires | Point selle, pas minimum | Relancer optimisation |
| S1 collapse → S0 | Pas de configuration excitée | Damping++, TRAH, guesses multiples |
| λ_max très différent | Mauvaise méthode/base | Benchmarking requis |
| SOC très faible (< 1) | Atome lourd absent ? | Vérifier composition moléculaire |
| E_ad > 1.0 eV (Iodo) ou > 1.2 eV (TPP-Iodo) | Mauvaise conversion PTT | Analyser modes non radiatifs |
| Charges mal localisées | Mauvaise charge TPP⁺ | Vérifier MEP, analyser Hirshfeld |
| Out of memory | RAM insuffisante (16 Go) | Réduire %maxcore à 3000 |

---

## Partie 5 : Analyse des Propriétés Photophysiques

### Évaluations à effectuer pour chaque prototype

**Rendements quantiques :**
- Φ_f : Rendement quantique de fluorescence
- Φ_p : Rendement quantique de phosphorescence
- Φ_Δ : Rendement quantique de génération d'oxygène singulet (PDT)

**Temps de vie des états excités :**
- τ_f : Temps de vie de fluorescence
- τ_S1, τ_T1 : Temps de vie des états S₁ et T₁

**Taux de processus photophysiques :**
- k_f : Constante de vitesse de fluorescence
- k_{ISC} : Constante de vitesse de conversion inter-système
- k_{EC} : Constante de vitesse de conversion énergie
- k_{nr} : Constante de vitesse de désexcitation non radiative

**Paramètres de photostabilité :**
- PSI > 1 : Molécule stable
- TCI > 3 : Bon convertisseur photothermique

---

## Partie 6 : Chronogramme Réaliste (14 semaines - Version 260304)

### Semaine 1-2 : Immersion et conception stratégique
- Formation ORCA 6.1, lecture intensive
- Validation chaîne de calcul (benzène test)
- Synthèse bibliographique (2-3 pages)
- **Convention d'archivage** : `<phase>_<molécule>_<tentative>_<base>`

### Semaine 3 : Préparation et optimisations
- Construction des 3 fichiers XYZ (1 ref + 2 prototypes)
- Lancer optimisations S0 (4 cœurs, 16 Go RAM)
- **TEST CRITIQUE** : def2-SVP vs def2-TZVP sur référence
- **Configuration** : %maxcore 3500, %pal nprocs 4

### Semaine 4 : S0 optimisations (3-4 heures mur total)
- S0 gas + S0 water (SMD mixed) pour les 3 molécules
- **Total** : ~3-4 h mur (séquentiel local)

### Semaines 5-6 : Excitations verticales (Screening rapide)
- TD-DFT/ωB97X-D3 pour λ_max de tous
- **Total** : ~1-2 h mur (calculs rapides)
- Comparer avec données expérimentales

### Semaines 7-9 : États excités relaxés et SOC
- **T1 optimisation** (robuste, 60-120 min)
- **S1 optimisation (ΔSCF)** (critique, +200-300% buffer)
  - Utiliser `gen_s1_guesses.sh` (3 guesses)
  - Utiliser `run_troubleshoot_S1.sh` (escalade auto)
- **SOC ΔDFT+SOC** (30-60 min/molécule)

### Semaine 10 : Analyse approfondie et décision
- Analyse des spectres, ciblage MEP, charges
- **Benchmarking** : MAE < 0.1 eV (≈ 10 nm)
- **Grille Go/No-Go** : Appliquer critères quantitatifs

### Semaine 11 : Évaluation finale
- **Décision** : Sélectionner molécule avec score ≥ 70%
- Analyse comparative détaillée

### Semaines 12-14 : Rapport et soutenance
- Rédaction (30-50 pages)
- Diapositives (15-20 slides)
- Répétitions et finalisation

**Total mur estimé (16 Go, 4 cœurs)** : ~20 h mur (+ buffer S1)
**Buffer recommandé** : +200-300% pour ΔSCF S₁ (3-5 tentatives)

---

## Partie 7 : Stratégies de Réduction de Temps et Plan B

### Si le temps est limité ou problèmes de convergence

| Stratégie | Gain de temps | Compromis |
|:---|:---|:---|
| def2-SVP au lieu de def2-TZVP | -50% (ADC(2)) | Précision -0.05 eV (si test justifie) |
| SOC seulement pour meilleur prototype | -60% | Perdre comparaison SOC |
| Plan B S₁ : TD-DFT au lieu de ΔSCF | -70% | Moins précis mais converge |
| 2 prototypes seulement | -33% | Réduire à 1 ref + 1 prototype |

### Plan B si S₁ échoue (après 5 tentatives)
- TD-DFT (ωB97X-D3) pour excitations verticales diagnostiques
- Continuer T1 (ΔUKS) + SOC (ΔDFT+SOC) pour tendances
- Reporter optimisation S₁ complète en perspective

---

## Partie 8 : Résumé des Fichiers à Sauvegarder

```
projet/
├── reference/
│   ├── S0_water_opt.gbw        [CRITICAL]
│   ├── S0_water_opt.xyz        [CRITICAL]
│   ├── TDDFT_vertical.out      [λ_max]
│   ├── T1_opt.gbw              [Important]
│   ├── S1_opt.gbw              [Important]
│   ├── SOC_DeltaDFT.out        [SOC]
│   └── analysis_reference.txt  [Summary]
│
├── iodo/
│   └── [même structure]
│
├── tpp-iodo/
│   └── [même structure]
│
├── results_comparison.csv      [Tableau final]
├── prototypes_scoring.xlsx     [Grille Go/No-Go]
├── benchmarking_results.txt    [Validation]
└── rapport_stage_final.pdf     [Livrable]
```

**Archivage recommandé :**
- Tous les `.gbw` et `.out` archivés avec version
- Convention : `S1_protoA_attempt3_opt.gbw`, `ADC2_ref_def2TZVP.out`
- Compresser après chaque étape majeure

---

## Partie 9 : Analyse de Photostabilité et Toxicité Prédictive

### Indicateurs de photostabilité
- **PSI** = (k_{ISC} + k_f) / (k_{nr} + k_{dég}) > 1
- Barrières de décomposition photochimique
- Intersections coniques

### Critères de toxicité prédictive
- Centres électrophiles potentiels
- Interactions hydrophobes avec résidus protéiques
- Paramètres ADME (Absorption, Distribution, Metabolism, Excretion)
- Potentiel génotoxique via analogies structurelles

---

## Partie 10 : Checklist Finale Avant Soutenance

### Validation méthodologique
- [ ] Méthode validée contre référence (MAE < 0.1 eV)
- [ ] Ensemble validation étendu (3-5 BODIPY)
- [ ] Statistiques calculées (MAE, RMSE, R²)
- [ ] Sensibilité aux paramètres testée

### Calculs et analyses
- [ ] Tous les calculs terminés et validés
- [ ] Tableau comparatif des 3 molécules rédigé
- [ ] Graphiques λ_max, spectres, MEP générés
- [ ] Scoring via grille Go/No-Go complété
- [ ] PSI et TCI calculés
- [ ] Critères ciblage mitochondrial quantifiés
- [ ] Analyse toxicité prédictive effectuée

### Communication scientifique
- [ ] Rapport relu par encadrant
- [ ] Diapositives préparées (15-20 slides)
- [ ] Résumé exécutif (1 page) écrit
- [ ] Références formatées (ACS/JACS)
- [ ] Répétition présentation (15 min)

---

**Document mis à jour le 04 mars 2026 (260304)**
**Version : 3.0 (Exécution locale 16 Go / TD-DFT ωB97X-D3)**
**Configuration : 4 cœurs, %maxcore 3500, SMD mixed**

---

**À imprimer et afficher dans le bureau !** 📄
