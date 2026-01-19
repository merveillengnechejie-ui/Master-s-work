# Résumé Exécutif : Comparaison TD-DFT vs OO-DFT/ΔDFT et Aide-Mémoire Pratique

> Rappel méthodologique (à lire en première minute) :
>
>- Pour les émissions CT en solution, privilégier un modèle de solvatation état-spécifique non-équilibre (ptSS-PCM).
>- Fonctionnelles recommandées : OT-ωB97M-V (ΔUKS/ΔROKS), PBE0 (ΔUKS robuste), PBE38-D4 (robustesse E_em).
>- Méthode IMOM conseillée pour les systèmes ICT (dimères / transfert de charge intermoléculaire).
>- Cibles de benchmarking : ΔE_{ST} MAE < 0,05 eV ; λ_max / E_em MAE ≤ 0,1 eV ; R² > 0.90.
>- **Nouveau** : Utiliser ΔDFT+SOC au lieu de NEVPT2 pour gain de temps (10×) et cohérence méthodologique.
>- **Nouveau** : Effectuer validation méthodologique étendue avec ensemble de BODIPY de référence.

Thématique du stage : Optimisation de nanoparticules de BODIPY pour une thérapie combinée photodynamique et photothermique ciblée sur les cellules de cancer du sein triple négatif.
Ces points résument les ajustements pratiques intégrés dans `demarche_methodologique_stage_v2_integree.md`.

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

---

## Partie 2 : Protocole de Calcul Recommandé (Résumé Exécutif)

### Stratégie en 6 étapes (portée révisée : 1 référence + 2 prototypes)

```
ÉTAPE 1 (rapide)     → S0 optimisation (DFT, phase gaz)
        ↓
ÉTAPE 2 (rapide)     → S0 optimisation (DFT, CPCM-eau)   [REFERENCE]
        ↓
ÉTAPE 3 (cher)       → Excitation verticale (ADC(2)/def2-TZVP ou def2-SVP*) [λ_max]
        ↓
ÉTAPE 4 (cher)       → T1 optimisation (ΔUKS, CPCM)      [ISC]
        ↓
ÉTAPE 5 (très cher)  → S1 optimisation (ΔSCF, CPCM)      [PTT]
        ↓
ÉTAPE 6 (cher)       → SOC (ΔDFT+SOC - rapide, ou TD-DFT) [PDT]
[ou validation ponctuelle: NEVPT2 - très cher]
        ↓
ÉTAPE 7              → Analyse MEP/ciblage pour TPP-BODIPY
        ↓
ANALYSE & DECISION   → Comparer prototypes, scorer les candidats (grille Go/No-Go)
```
*Effectuer test comparatif def2-SVP vs def2-TZVP en semaine 3 pour optimiser le planning

### Flux des données

```
S0_opt.gbw (Étape 2)
    ├─→ ADC2_vertical.inp  (Étape 3) → λ_max, spectrum
    ├─→ T1_opt.inp         (Étape 4) → E_T1, geometry
    ├─→ S1_opt.inp         (Étape 5) → E_S1, ΔE_ST
    ├─→ SOC_opt.inp        (Étape 6) → SOC matrix (ΔDFT+SOC)
    └─→ MEP_analysis.inp   (Étape 7) → Charges, ciblage

Résultats:  E_ad = E_S0 - E_S1  (PTT potential)
            ΔE_ST = E_S1 - E_T1  (ISC/PDT potential)
            k_{ISC} via SOC (PDT efficiency)
            PSI = (k_{ISC} + k_f) / (k_{nr} + k_{dég}) (photostabilité)
            TCI = k_{nr} / (k_f + k_{ISC}) (conversion PTT)
```

---

## Partie 3 : Guide de Sélection de Prototypes (Grille Go/No-Go Révisée)

### Portée (révisée le 15/11/2025)
- **1 molécule de référence expérimentale** (λ_max, Φ_f, SOC publiés)
- **Prototype 1** : Iodo-BODIPY (PDT optimisée) - atome lourd pour ISC
- **Prototype 2** : TPP-Iodo-BODIPY (théranostique ciblé) - ciblage mitochondrial

### Critères d'évaluation quantitatifs

#### Prototype 1 : Iodo-BODIPY (PDT optimisée)
| Critère | Cible | Poids | Calcul ORCA | Note sur 25/25 |
|:---|:---|:---|:---|:---|
| **λ_max (absorption)** | 680-720 nm (NIR-I) | 25% | ADC(2) | |
| **E_adiabatic (PTT)** | < 1.0 eV | 15% | ΔE_S0-S1 | |
| **ΔE_ST (ISC/PDT)** | < 0.05 eV | 25% | ΔE_S1-T1 | |
| **SOC (ISC speed)** | > 50 cm⁻¹ | 25% | ΔDFT+SOC | |
| **Photostabilité** | PSI > 1 | 10% | Calculs k | |

#### Prototype 2 : TPP-Iodo-BODIPY (théranostique ciblé)
| Critère | Cible | Poids | Calcul ORCA | Note sur 25/25 |
|:---|:---|:---|:---|:---|
| **λ_max (absorption)** | 690-730 nm (NIR-I, légère perturbation par TPP+) | 20% | ADC(2) | |
| **E_adiabatic (PTT)** | < 1.2 eV | 15% | ΔE_S0-S1 | |
| **ΔE_ST (ISC/PDT)** | < 0.08 eV | 20% | ΔE_S1-T1 | |
| **SOC (ISC speed)** | > 40 cm⁻¹ | 15% | ΔDFT+SOC | |
| **Ciblage mitochondrial** | Quantitatif | 30% | MEP + affinité membranaire | |

#### Critères de ciblage mitochondrial quantitatifs (Prototype 2)
- Charge TPP⁺: +1,00 e (localisée sur TPP, analysée par Hirshfeld)
- Distance minimale TPP⁺ → centre BODIPY : > 5 Å (exposition maximale)
- Angle dièdre TPP⁺-BODIPY : > 90° (orientation perpendiculaire)
- Potentiel membranaire prédit : ΔΨ > 150 mV pour accumulation efficace
- Coefficient de perméabilité apparente (P_app) > 10⁻⁶ cm/s pour pénétration cellulaire
- Rapport d'accumulation : [TPP-BODIPY]_mito/[TPP-BODIPY]_cyto ≥ 10 pour ciblage sélectif
- Énergie de liaison à la membrane ≥ -20 kcal/mol pour ancrage stable

### Tableau de scoring (Grille Go/No-Go)

```
Prototype | λ_max | E_ad | ΔE_ST | SOC | Ciblage | TOTAL | Verdict
----------|-------|------|-------|-----|---------|-------|----------
Référence |  /25  |  /15 |  /25  |  /25|  /10   | /100  | Benchmark
Iodo-BODY |  /25  |  /15 |  /25  |  /25|  /10   | /100  | Score ≥ 70% = Go
TPP-Iodo  |  /20  |  /15 |  /20  |  /15|  /30   | /100  | Score ≥ 70% = Go
```

**Règles de scoring :**
- λ_max ∈ [680-720] (Iodo): 25/25; ∈ [690-730] (TPP-Iodo): 20/25; ∈ [600-900]: 15/25; ailleurs: ≤ 10/25
- E_ad < 0.8: 15/15; < 1.0: 12/15 (Iodo), 15/15 (TPP-Iodo); < 1.2: 10/15 (TPP-Iodo); ailleurs: < 8/15
- ΔE_ST < 0.05: 25/25; < 0.08: 20/25 (TPP-Iodo); < 0.15: 15/25; > 0.3: < 5/25
- SOC > 100: 25/25 (Iodo), 15/15 (TPP-Iodo); > 50: 20/25 (Iodo), 12/15 (TPP-Iodo); > 40: 15/15 (TPP-Iodo); < 10: < 5/25 (Iodo), < 5/15 (TPP-Iodo)
- Ciblage (TPP-Iodo): Score basé sur critères quantitatifs (30/30 maximum)

---

## Partie 4 : Aide-Mémoire Pratique (A4 à Imprimer)

### Pour démarrer

```bash
# 1. Charger ORCA et configurer
module load orca/6.1
export PATH=/path/to/orca:$PATH

# 2. Créer les répertoires de travail (3 prototypes: 1 référence + 2 conçus)
mkdir -p {reference,iodo,tpp-iodo}/{S0,S1,T1,ADC2,SOC,MEP}

# 3. Copier les fichiers d'entrée
cp S0_gas_opt.inp reference/
cp S0_water_opt.inp reference/

# 4. Lancer les calculs (exemple SLURM)
sbatch submit_S0.slurm

# 5. Vérifier le statut
squeue -u $USER
```

### Commandes clés ORCA

| Action | Commande |
|:---|:---|
| **Lancer calcul** | `orca input.inp > output.out &` |
| **Voir progression** | `tail -f output.out` |
| **Extraire énergie** | `grep "FINAL SINGLE POINT" output.out` |
| **Voir λ_max (ADC2)** | `grep "S_1 state" output.out` |
| **Vérifier SOC** | `grep -A5 "Spin-Orbit" output.out` |
| **Converger géométrie** | `grep "Geometry convergence" output.out` |
| **Vérifier fréquences** | `grep "imaginary frequencies" output.out` |
| **Voir charges atomiques** | `Multiwfn S0_water_opt.out` |

### Conversions utiles

$$\lambda_{\text{max}} (\text{nm}) = \frac{1240 \text{ eV·nm}}{E (\text{eV})}$$

$$\Delta E (\text{eV}) = E (\text{a.u.}) \times 27.211$$

$$E (\text{cm}^{-1}) = E (\text{eV}) \times 8066$$

$$\text{Indice de photostabilité (PSI)} = \frac{k_{ISC} + k_f}{k_{nr} + k_{dég}}$$

$$\text{Indice de conversion thermique (TCI)} = \frac{k_{nr}}{k_f + k_{ISC}}$$

### Signaux d'alerte

| Signal | Cause probable | Action |
|:---|:---|:---|
| SCF ne converge pas | Géométrie mauvaise | Revoir XYZ, réduire MaxStep |
| Fréquences imaginaires | Point selle, pas minimum | Relancer optimisation |
| S1 collapse → S0 | Pas de configuration excitée | Augmenter damping, utiliser TRAH, essayer différents guess |
| λ_max très différent | Mauvaise méthode/base | Benchmarking requis |
| SOC très faible (< 1) | Atome lourd absent ? | Vérifier composition moléculaire |
| E_ad > 1.0 eV (Iodo) ou > 1.2 eV (TPP-Iodo) | Mauvaise conversion PTT | Analyser modes de désexcitation non radiative |
| Charges mal localisées | Mauvaise charge TPP⁺ | Vérifier MEP, analyser Hirshfeld |

---

## Partie 5 : Analyse des Propriétés Photophysiques

### Évaluations à effectuer pour chaque prototype

**Rendements quantiques :**
- Rendement quantique de fluorescence (Φ_f)
- Rendement quantique de phosphorescence (Φ_p)
- Rendement quantique de génération d'oxygène singulet (Φ_Δ)

**Temps de vie des états excités :**
- Temps de vie des états S₁ et T₁
- Temps de vie de fluorescence (τ_f)

**Taux de processus photophysiques :**
- Constantes de vitesse de fluorescence (k_f)
- Constantes de vitesse de conversion inter-système (k_{ISC})
- Constantes de vitesse de conversion énergie (k_{EC})
- Constantes de vitesse de désexcitation non radiative (k_{nr})

**Paramètres de photostabilité :**
- Taux de photodégradation prédit
- Stabilité face aux cycles d'excitation-radiation
- Indice de photostabilité (PSI) > 1

### Indicateurs de performance PTT
- **Indice de conversion thermique (TCI)** : TCI > 3 indique un bon convertisseur photothermique
- Énergie adiabatique faible (E_ad < 0.8 eV) pour conversion rapide
- Temps de vie S₁ > 10 ps pour conversion non radiative
- Faible k_f / élevé k_{nr} pour conversion énergie efficace

---

## Partie 6 : Chronogramme Réaliste (14 semaines - Version Révisée)

### Semaine 1-2 : Immersion et conception stratégique
- Formation Linux/Slurm, lecture intensive
- Validation chaîne de calcul (jeu de test pré-rempli)
- Synthèse bibliographique (2-3 pages)
- **Jeu de test pré-rempli** : Équipe fournit BODIPY de référence avec fichiers ORCA pour valider la chaîne complète
- **Archivage systématique** : Convention de nommage pour fichiers

### Semaine 3 : Préparation et test comparatif
- Construction des 3 fichiers XYZ (référence + 2 prototypes)
- Lancer optimisations rapides GFN2-xTB
- **TEST CRITIQUE** : ADC(2) def2-SVP vs def2-TZVP sur référence
- Comparer λ_max (MAE par rapport à expérience)
- **Décision** : Si écart < 5 nm → garder def2-SVP (gain ~3h/molécule)
- **Impact** : Peut économiser 9h mur sur le projet si def2-SVP suffisant

### Semaine 4 : S0 optimisations (3-4 heures mur total)
- S0 gas + S0 water pour les 3 prototypes
- **Total estimé** : ~3-4 h mur pour les 3 en parallèle
- **Stratégie** : Lancer les 3 calculs gaz simultanément

### Semaines 5-6 : Excitations verticales (12-18 heures mur total)
- ADC(2)/def2-TZVP ou def2-SVP* pour λ_max de tous les prototypes
- **Total estimé** : ~12-18 h mur pour les 3 (à faire en série, batch de nuit)
- Comparer avec données expérimentales (benchmarking)
- *Base dépend du test comparatif semaine 3*

### Semaines 7-9 : États excités relaxés et SOC
- **Optimisations T₁** (rapide, lancer en parallèle)
- **Optimisations S₁ (ΔSCF)** (critique, +200-300% buffer)
  - Utiliser `./gen_s1_guesses.sh` pour tester 3 configurations électroniques
  - Utiliser `./run_troubleshoot_S1.sh` pour escalade automatique
- **Couplage spin-orbite (SOC)** : Standard ΔDFT+SOC (30-60 min/molécule)
- **VALIDATION PONCTUELLE** : FIC-NEVPT2 si ressources disponibles (facultatif)

### Semaine 10 : Analyse approfondie et décision
- Analyse des spectres, ciblage MEP, charges
- **Benchmarking** : Comparer calculs de la référence avec données expérimentales
- Évaluer MAE (λ_max) : doit être < 0.1 eV (≈ 10 nm)
- **Grille Go/No-Go** : Appliquer critères quantitatifs
- **Score final** : Calculer score pour chaque prototype

### Semaine 11 : Évaluation finale
- **Décision finale** : Sélectionner molécule avec score ≥ 70%
- Identifier le prototype le plus prometteur
- Analyse comparative détaillée

### Semaines 12-14 : Rapport et soutenance
- Rédaction du rapport (30-50 pages)
- Création diapositives (15-20 diapositives)
- Répétitions et finalisation
- **Module optionnel** : Régression simple avec scikit-learn

**Total mur estimé pour 3 molécules** : ~51 h mur (réaliste avec buffer S1)
**Buffer recommandé** : +200-300% pour ΔSCF S₁ (3-5 tentatives par molécule)
**Recommandation** : Démarrer T1 optim. dès que S0 est terminée

---

## Partie 7 : Stratégies de Réduction de Temps et Plan B

### Si le temps est limité ou problèmes de convergence

| Stratégie | Gain de temps | Compromise |
|:---|:---|:---|
| Utiliser def-SVP au lieu de def-TZVP | -50% (temps ADC(2)) | Precision -0.05 eV (si test comparatif le justifie) |
| Calculer SOC seulement pour meilleur prototype | -60% | Perdre comparaison SOC entre tous |
| Plan B S₁ : TD-DFT au lieu de ΔSCF | -70% | Moins précis mais converge |
| Utiliser 2 prototypes seulement | -33% | Réduire à 1 référence + 1 prototype |

### Plan B si S₁ échoue (après 5 tentatives)
- TD-DFT (ωB97X-D) pour excitations verticales diagnostiques uniquement
- Continuer T1 (ΔUKS) + SOC (ΔDFT+SOC) pour les tendances
- Reporter l'optimisation S₁ complète en perspective

---

## Partie 8 : Résumé des Fichiers à Sauvegarder

```
projet/
├── reference/
│   ├── S0_water_opt.gbw        [CRITICAL]
│   ├── S0_water_opt.xyz        [CRITICAL]
│   ├── S1_water_opt.gbw        [Important]
│   ├── T1_water_opt.gbw        [Important]
│   ├── ADC2_vertical.out       [Important - contient λ_max]
│   ├── SOC_DeltaDFT.out        [Important - contient SOC]
│   └── analysis_reference.txt  [Summary]
│
├── iodo/
│   └── [même structure]
│
├── tpp-iodo/
│   └── [même structure]
│
├── results_comparison.csv      [Tableau final]
├── prototypes_scoring.xlsx     [Matrice de décision - Grille Go/No-Go]
├── benchmarking_results.txt    [Validation méthodologique]
└── rapport_stage_final.pdf     [Livrable]
```

**Archivage recommandé :**
- Tous les `.gbw` et `.out` archivés avec version
- Convention de nommage : `S1_protoA_attempt3_opt.gbw`, `ADC2_ref_def2TZVP.out`
- Compresser après chaque étape majeure

---

## Partie 9 : Analyse de Photostabilité et Toxicité Prédictive

### Indicateurs de photostabilité à évaluer
- **Indice de photostabilité (PSI)** = (k_{ISC} + k_f) / (k_{nr} + k_{dég})
- Une molécule stable a PSI > 1, indiquant que les voies souhaitées prédominent
- Calcul des barrières de décomposition photochimique
- Analyse des surfaces d'énergie potentielle et intersections coniques

### Critères de toxicité prédictive à considérer
- Identification des centres électrophiles potentiels
- Analyse des interactions hydrophobes avec résidus protéiques
- Calcul des paramètres ADME (Absorption, Distribution, Metabolism, Excretion)
- Évaluation du potentiel génotoxique via analogies structurelles

---

## Partie 10 : Checklist Finale Avant Soutenance

### Validation méthodologique
- [ ] Méthode validée contre BODIPY de référence (MAE < 0.1 eV)
- [ ] Ensemble de validation étendu (3-5 BODIPY supplémentaires)
- [ ] Statistiques calculées (MAE, RMSE, R²)
- [ ] Sensibilité aux paramètres testée (fonctionnelles, solvatation, bases)

### Calculs et analyses
- [ ] Tous les calculs terminés et validés
- [ ] Tableau comparatif des 3 prototypes rédigé
- [ ] Graphiques λ_max, spectres, MEP générés
- [ ] Scoring des candidats complété via grille Go/No-Go
- [ ] Analyse de photostabilité effectuée
- [ ] Critères de ciblage mitochondrial quantifiés (Prototype 2)
- [ ] Indicateurs PSI et TCI calculés
- [ ] Analyse de toxicité prédictive (sites réactifs, ADME)

### Communication scientifique
- [ ] Rapport (draft) relecture par co-encadrant
- [ ] Diapositives préparées (15-20 slides, avec grille Go/No-Go)
- [ ] Résumé exécutif (1 page) écrit
- [ ] Références formatées (ACS ou JACS standard)
- [ ] Répétition de la présentation (15 min)
- [ ] Lettre d'intention avec équipe expérimentale (optionnel)

**Document mis à jour le 15 novembre 2025 pour intégrer la portée révisée (1 référence + 2 prototypes), la grille Go/No-Go quantitative, la validation méthodologique étendue, l'analyse de photostabilité et de toxicité prédictive, ainsi que les critères de ciblage mitochondrial quantitatifs.**

---

**Document créé pour un démarrage rapide — À imprimer et afficher dans le bureau !**
