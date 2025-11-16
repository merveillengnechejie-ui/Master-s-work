# PROTOTYPES : Description des 3 Molécules

## 📋 Vue d'ensemble

Ce document décrit les **3 molécules** du projet révisé (15/11/2025) :
- **1 molécule de référence expérimentale** (externe, publiée) pour benchmarking
- **2 prototypes internes** : Iodo-BODIPY + TPP–Iodo–BODIPY

---

## 🔬 Molécule 1 : Référence Expérimentale (Externe)

### Rôle
Valider la **chaîne de calcul ΔDFT+SOC** en reproduisant une molécule dont les propriétés sont **déjà publiées**.

### Critères de sélection

| Critère | Priorité | Détails |
| :--- | :--- | :--- |
| **λ_max expérimental** | 1 | 500–600 nm (visible, bien caractérisé, loin de NIR) |
| **Rendement quantique Φ_f** | 2 | > 0.1 (molécule fluorescente robuste) |
| **Données SOC** | 3 | Si disponibles, constants S1↔T1 (rare mais idéal) |
| **Accessibilité** | 4 | Article récent (< 5 ans), données complètes |
| **Structures cristallines** | 5 | Disponibilité pour validation géométrique |

### Exemple concret recommandé

**Molécule** : BODIPY méso-phényle (BODIPY-Ph)

| Propriété | Valeur | Source |
| :--- | :--- | :--- |
| **λ_max exp.** | ~505 nm | DMSO |
| **Φ_f exp.** | ~0.8 | DMSO |
| **SOC exp.** | ~50 cm⁻¹ | Si disponible |
| **Structure cristalline** | Disponible | Pour validation géométrique |
| **Justification** | Loin de NIR (bon contraste avec prototypes) | Permet validation claire |

### Sources recommandées

- *European Journal of Organic Chemistry* (BODIPY design)
- *Journal of Medicinal Chemistry* (BODIPY théranostique)
- *Photochemistry and Photobiology Science* (propriétés photophysiques)
- *Journal of Physical Chemistry A* (SOC, états excités)

### Procédure de benchmarking

#### Étape 1 : Comparaison avec la géométrie cristalline
- Calculer les écarts RMSD (Root Mean Square Deviation) entre les structures
- Analyser les différences dans les angles dièdres critiques affectant l'absorption

#### Étape 2 : Analyse de l'espace conformationnel
- Effectuer des recherches conformationnelles pour s'assurer que la structure choisie correspond à un minimum énergétique global
- Vérifier que la structure cristalline est proche du minimum global calculé

#### Étape 3 : Validation de la reproductibilité
- Comparer plusieurs structures de référence publiées dans la littérature
- Identifier les tendances systématiques dans les propriétés calculées

#### Étape 4 : Critères géométriques de validation
- Fréquences normales : absence de fréquences imaginaires pour la structure optimisée
- Énergie relative : la structure cristalline doit être proche du minimum global (ΔE < 0.05 eV)
- Paramètres géométriques : longueurs et angles de liaison cohérents avec la structure de référence

#### Étape 5 : Critères de précision
- MAE (Mean Absolute Error) < 0.1 eV pour λ_max
- RMSE (Root Mean Square Error) < 0.15 eV
- Coefficient de corrélation (R²) > 0.95
- Ensemble de validation : au moins 3-5 BODIPY supplémentaires pour validation étendue

---

## 🔬 Prototype 1 : Iodo-BODIPY (PDT optimisée)

### Objectif
Optimiser le **potentiel PDT** via l'**effet d'atome lourd** (I) pour améliorer la **transition inter-système** (ISC) et l'**efficacité de génération d'oxygène singulet**.

### Structure
- BODIPY de base avec **atome d'iode** en position 5
- Conservation des propriétés photophysiques principales
- **Redshift** modéré (680–720 nm) dans la **fenêtre NIR-I**

### Critères d'évaluation quantitatifs (Grille Go/No-Go)

| Critère | Cible | Poids | Score max | Méthode calcul |
| :--- | :--- | :--- | :--- | :--- |
| **λ_max (absorption)** | 680-720 nm (NIR-I) | 25% | 25/25 | ADC(2)/def2-TZVP |
| **E_adiabatic (PTT)** | < 1.0 eV | 15% | 15/15 | ΔE_S0-S1 (ΔUKS/ΔROKS) |
| **ΔE_ST (ISC/PDT)** | < 0.05 eV | 25% | 25/25 | ΔE_S1-T1 (ΔUKS/ΔROKS) |
| **SOC (ISC speed)** | > 50 cm⁻¹ | 25% | 25/25 | ΔDFT+SOC (ZORA, dosoc) |
| **Photostabilité** | PSI > 1 | 10% | 10/10 | Calculs k_processus |

### Analyse des propriétés photophysiques

#### Rendements quantiques
- **Φ_f** (fluorescence) : rapport entre photons émis et photons absorbés
- **Φ_p** (phosphorescence) : pour les états triplet
- **Φ_Δ** (génération d'oxygène singulet) : critère central pour la PDT efficace

#### Temps de vie des états excités
- **τ_f** (fluorescence) : mesuré ou calculé à partir de Φ_f et taux de relaxation radiative
- **τ_S1 et τ_T1** : déterminent les compétitions radiatives vs non radiatives

#### Taux de processus photophysiques
- **k_f** (fluorescence)
- **k_{ISC}** (conversion inter-système)
- **k_{EC}** (conversion énergie)
- **k_{nr}** (désexcitation non radiative)

#### Indices de performance
- **PSI (Photostabilité)** : PSI = (k_{ISC} + k_f) / (k_{nr} + k_{dég})
- **TCI (Conversion Thermique)** : TCI = k_{nr} / (k_f + k_{ISC})

### Validation ciblage mitochondrial
- Non applicable pour ce prototype
- **Objectif principal** : PDT optimisée via ISC améliorée

---

## 🔬 Prototype 2 : TPP–Iodo–BODIPY (théranostique ciblé)

### Objectif
Combinaison de **PDT optimisée** (via Iodo-BODIPY) et **ciblage mitochondrial** (via groupe cationique lipophile TPP⁺) pour une **thérapie combinée** efficace.

### Structure
- Iodo-BODIPY avec **groupement triarylphosphonium (TPP⁺)** en position 1
- Fonctionnalisation pour **ciblage mitochondrial cationique**
- Maintien des propriétés photophysiques optimisées du Iodo-BODIPY

### Critères d'évaluation quantitatifs (Grille Go/No-Go)

| Critère | Cible | Poids | Score max | Méthode calcul |
| :--- | :--- | :--- | :--- | :--- |
| **λ_max (absorption)** | 690-730 nm (NIR-I, légère perturbation par TPP+) | 20% | 20/25 | ADC(2)/def2-TZVP |
| **E_adiabatic (PTT)** | < 1.2 eV | 15% | 15/15 | ΔE_S0-S1 (ΔUKS/ΔROKS) |
| **ΔE_ST (ISC/PDT)** | < 0.08 eV | 20% | 20/25 | ΔE_S1-T1 (ΔUKS/ΔROKS) |
| **SOC (ISC speed)** | > 40 cm⁻¹ | 15% | 15/15 | ΔDFT+SOC (ZORA, dosoc) |
| **Ciblage mitochondrial** | Quantitatif (voir ci-dessous) | 30% | 30/30 | MEP + affinité membranaire |

### Critères de ciblage mitochondrial quantitatifs

#### Charges et localisation
- **Charge totale du groupe TPP⁺** : Doit être ≥ +1 (idéalement +1 à +2)
- **Localisation** : La charge doit être concentrée sur le groupe TPP⁺, pas diffuse
- **Charge TPP⁺** : +1,00 e (localisée sur TPP⁺, analysée par Hirshfeld)
- **Accessibilité** : Vérifier visuellement que le groupe est exposé en surface

#### Paramètres géométriques critiques
- **Distance minimale TPP⁺ → centre BODIPY** : > 5 Å (exposition maximale)
- **OU Angle dièdre TPP⁺-BODIPY** : > 90° (orientation perpendiculaire)
- **Visualisation MEP** : groupe TPP⁺ doit être en surface (pas enfoui)

#### Paramètres biologiques de ciblage
- **Potentiel membranaire prédit** : ΔΨ > 150 mV pour accumulation efficace
- **Coefficient de perméabilité apparente (P_app)** : P_app > 10⁻⁶ cm/s pour pénétration cellulaire
- **Rapport d'accumulation** : [TPP-BODIPY]_mito/[TPP-BODIPY]_cyto ≥ 10 pour ciblage sélectif
- **Énergie de liaison à la membrane** : ≥ -20 kcal/mol pour ancrage stable

### Analyse des propriétés photophysiques

#### Rendements quantiques
- **Φ_f** (fluorescence) : conservation de l'intensité fluorescente
- **Φ_Δ** (génération d'oxygène singulet) : maintien de l'efficacité PDT
- Comparaison avec Iodo-BODIPY pour évaluer l'impact du groupe TPP⁺

#### Indicateurs de performance
- **PSI (Photostabilité)** : Doit rester > 1 pour une excellente stabilité
- **TCI (Conversion Thermique)** : TCI > 3 indique un bon convertisseur photothermique
- **Indice de conversion photothermique (TCI)** : TCI = k_{nr} / (k_f + k_{ISC})

### Modélisation des interactions moléculaires
- **Calculs d'affinité moléculaire** : estimation des énergies de liaison entre le groupe TPP⁺ et les composants de la membrane mitochondriale
- **Analyse de la distribution spatiale du cation lipophile** : évaluation de l'orientation du groupe TPP⁺ par rapport au plan de la membrane
- **Modélisation des interactions avec la membrane mitochondriale** : construction de modèles de bicouche lipidique (ex. : DOPC/DOPG 4:1) pour simuler la membrane mitochondriale interne

---

## 📊 Grille Go/No-Go Quantitative (Critères de Décision)

### Méthodologie d'évaluation
Chaque prototype est évalué selon une **grille Go/No-Go quantitative** avec **critères pondérés** :

| Prototype | Score requis | Statut |
| :--- | :--- | :--- |
| Iodo-BODIPY | ≥ 70% | Go/No-Go |
| TPP-Iodo-BODIPY | ≥ 70% | Go/No-Go |
| Référence | Benchmark | N/A |

### Pondération des critères
- **λ_max** : 20-25% (selon prototype)
- **E_adiabatic** : 15% (constante)
- **ΔE_ST** : 20-25% (selon prototype)
- **SOC** : 15-25% (selon prototype)
- **Ciblage** : 30% (TPP-Iodo-BODIPY seulement)

### Processus de décision
1. **Calcul des scores individuels** pour chaque critère
2. **Application des pondérations** pour chaque prototype
3. **Calcul du score total** pour chaque prototype
4. **Comparaison avec seuil 70%** pour décision Go/No-Go
5. **Sélection du candidat optimal** basé sur le score total
6. **Analyse comparative** des 3 molécules pour validation

---

## 🧠 Validation méthodologique étendue

### Ensemble de validation
- **Validation sur un ensemble de 3-5 BODIPY** supplémentaires de la littérature avec propriétés photophysiques complètes
- **Comparaison λ_max, ΔE_ST, et SOC** (si disponibles) avec des valeurs expérimentales
- **Calcul des statistiques** : MAE, RMSE, coefficient de corrélation (R²)

### Sensibilité aux paramètres
- **Évaluation de la sensibilité des résultats aux choix de fonctionnelles** (PBE0, B3LYP, ωB97M-V)
- **Évaluation de la sensibilité aux modèles de solvatation** (CPCM vs SMD vs COSMO)
- **Évaluation de la sensibilité aux tailles de base** (def2-SVP vs def2-TZVP)

1. **Construire la géométrie** (Avogadro/IQmol)
2. **Optimiser S₀** (B3LYP-D3/def2-SVP, CPCM eau)
3. **Calculer λ_max** (ADC(2)/def2-TZVP, CPCM eau)
4. **Comparer avec expérience** :
   - **Critère de validation** : MAE < 0.1 eV (≈ 10 nm à 700 nm)
   - Si MAE > 0.1 eV : Investiguer (base? solvant? géométrie?)
5. **Valider la chaîne** avant d'attaquer les prototypes

### Fichiers associés

```
Référence_BODIPY_Ph.xyz          # Géométrie optimisée
S0_ref_opt.gbw                   # Résultat S0 optimisé
ADC2_ref_vertical.out            # Résultat ADC(2)
T1_ref_opt.gbw                   # Résultat T1 optimisé
S1_ref_opt.gbw                   # Résultat S1 optimisé
SOC_ref_DELTADFT.out             # Résultat SOC
```

---

## 🔬 Prototype 1 : Iodo-BODIPY (PDT Optimisée)

### Rôle
Tester l'**effet de l'atome lourd (iode) sur l'ISC et le redshift NIR** sans le "bruit" du ciblage mitochondrial.

### Objectif scientifique

**Question** : "L'iode suffit-il à placer le BODIPY en NIR et à activer efficacement la PDT ?"

### Cahier des charges quantitatif

| Propriété | Critère de succès | Pondération | Justification |
| :--- | :--- | :--- | :--- |
| **λ_max** | 680–720 nm | 30% | NIR-I, redshift par atome lourd |
| **ΔE_ST** | < 0,05 eV | 30% | ISC efficace (crucial pour PDT) |
| **SOC** | > 50 cm⁻¹ | 25% | Effet iode confirmé |
| **E_ad** | < 1,0 eV | 15% | Potentiel PTT (conversion chaleur) |

**Score final** : Go si ≥ 70% des critères satisfaits

### Structure chimique

```
Squelette BODIPY + Iode (position 2 ou 6)
Exemple : 2-Iodo-BODIPY ou 2,6-Diiodo-BODIPY

Modifications possibles :
- Position 3,5 : groupes donneurs (redshift supplémentaire)
- Position 2,6 : iode (effet SOC)
```

### Propriétés attendues

| Propriété | Valeur attendue | Justification |
| :--- | :--- | :--- |
| **λ_max** | 680–720 nm | Redshift ~150–200 nm vs BODIPY-Ph (505 nm) |
| **ΔE_ST** | 0,03–0,05 eV | Iode augmente SOC → ISC plus efficace |
| **SOC** | 50–100 cm⁻¹ | Iode : effet lourd confirmé |
| **Φ_f** | 0,05–0,15 | Réduit vs BODIPY-Ph (ISC compétitif) |
| **E_ad** | 0,8–1,0 eV | Potentiel PTT modéré |

### Fichiers associés

```
Iodo_BODIPY.xyz                  # Géométrie optimisée
S0_iodo_opt.gbw                  # Résultat S0 optimisé
ADC2_iodo_vertical.out           # Résultat ADC(2)
T1_iodo_opt.gbw                  # Résultat T1 optimisé
S1_iodo_opt.gbw                  # Résultat S1 optimisé
SOC_iodo_DELTADFT.out            # Résultat SOC
```

### Analyse comparative

**Comparaison avec référence** :
- Δλ_max = λ_max(Iodo) - λ_max(Ref) → Redshift attendu ~150–200 nm
- ΔE_ST(Iodo) < ΔE_ST(Ref) → ISC plus efficace
- SOC(Iodo) >> SOC(Ref) → Effet iode confirmé

---

## 🔬 Prototype 2 : TPP–Iodo–BODIPY (Théranostique Ciblé)

### Rôle
Ajouter le **ciblage mitochondrial (TPP⁺) au prototype 1** et vérifier qu'il ne dégrade pas les performances photophysiques.

### Objectif scientifique

**Question** : "Le TPP⁺ compromet-il les performances optiques pour le gain de ciblage ?"

### Cahier des charges quantitatif

| Propriété | Critère de succès | Pondération | Justification |
| :--- | :--- | :--- | :--- |
| **λ_max** | 690–730 nm | 25% | NIR-I, légère perturbation par TPP⁺ |
| **ΔE_ST** | < 0,08 eV | 25% | Préservation de l'ISC |
| **SOC** | > 40 cm⁻¹ | 20% | Légère perte acceptable |
| **E_ad** | < 1,2 eV | 15% | Synergie PTT maintenue |
| **Ciblage** | Charge TPP⁺ + accessibilité | 15% | Critères quantitatifs (voir ci-dessous) |

**Score final** : Go si ≥ 70% des critères satisfaits

### Structure chimique

```
Squelette BODIPY + Iode (position 2 ou 6) + TPP⁺ (groupement cationique)
Exemple : 2-Iodo-BODIPY-TPP ou 2,6-Diiodo-BODIPY-TPP

Groupement TPP⁺ :
- Triarylphosphonium (TPP) : (C6H5)3P⁺
- Ou ammonium quaternaire : N(CH3)3⁺
- Lié via chaîne alkyle (ex: C2–C4)
```

### Propriétés attendues

| Propriété | Valeur attendue | Justification |
| :--- | :--- | :--- |
| **λ_max** | 690–730 nm | Légère perturbation vs Iodo-BODIPY (~10–20 nm) |
| **ΔE_ST** | 0,05–0,08 eV | Préservation de l'ISC (légère augmentation acceptable) |
| **SOC** | 40–80 cm⁻¹ | Légère perte vs Iodo-BODIPY (acceptable) |
| **Φ_f** | 0,03–0,12 | Similaire à Iodo-BODIPY |
| **E_ad** | 0,9–1,2 eV | Synergie PTT maintenue |
| **Charge TPP⁺** | +1,00 e | Localisée sur TPP (Hirshfeld) |

### Critères de ciblage quantitatifs

#### Charge TPP⁺

| Critère | Valeur | Méthode |
| :--- | :--- | :--- |
| **Charge totale TPP⁺** | +1,00 e (idéalement +1 à +2) | Analyse Hirshfeld (Multiwfn) |
| **Localisation** | Concentrée sur TPP (pas diffuse) | Visualisation MEP |

#### Accessibilité TPP⁺

**Option A** : Distance minimale TPP⁺ → centre BODIPY
- **Critère** : > 5 Å (exposition maximale)
- **Mesure** : Distance géométrique (Multiwfn ou VMD)

**Option B** : Angle dièdre TPP⁺-BODIPY
- **Critère** : > 90° (orientation perpendiculaire)
- **Mesure** : Angle dièdre (Multiwfn ou VMD)

**Option C** : Visualisation MEP
- **Critère** : Groupe TPP⁺ en surface (pas enfoui)
- **Mesure** : Inspection visuelle (GaussView, VESTA)

### Fichiers associés

```
TPP_Iodo_BODIPY.xyz             # Géométrie optimisée
S0_tpp_iodo_opt.gbw             # Résultat S0 optimisé
ADC2_tpp_iodo_vertical.out      # Résultat ADC(2)
T1_tpp_iodo_opt.gbw             # Résultat T1 optimisé
S1_tpp_iodo_opt.gbw             # Résultat S1 optimisé
SOC_tpp_iodo_DELTADFT.out       # Résultat SOC
MEP_tpp_iodo.cube               # Potentiel électrostatique
```

### Analyse comparative

**Comparaison avec Iodo-BODIPY** :
- Δλ_max = λ_max(TPP-Iodo) - λ_max(Iodo) → Perturbation attendue ~10–20 nm
- ΔE_ST(TPP-Iodo) vs ΔE_ST(Iodo) → Légère augmentation acceptable
- SOC(TPP-Iodo) vs SOC(Iodo) → Légère perte acceptable
- Charge TPP⁺ > +1,00 e → Ciblage confirmé
- Distance TPP⁺ > 5 Å → Accessibilité confirmée

---

## 📊 Tableau Comparatif des 3 Molécules

| Propriété | Référence (BODIPY-Ph) | Prototype 1 (Iodo-BODIPY) | Prototype 2 (TPP-Iodo-BODIPY) |
| :--- | :--- | :--- | :--- |
| **λ_max (nm)** | ~505 (exp) | 680–720 (calc) | 690–730 (calc) |
| **ΔE_ST (eV)** | — | < 0,05 | < 0,08 |
| **SOC (cm⁻¹)** | — | > 50 | > 40 |
| **E_ad (eV)** | — | < 1,0 | < 1,2 |
| **Charge TPP⁺** | N/A | N/A | +1,00 e |
| **Ciblage** | N/A | N/A | Distance > 5 Å |
| **Rôle** | Validation méthode | Test PDT | Test théranostique |

---

## 🎯 Grille Go/No-Go

### Prototype 1 : Iodo-BODIPY

```
Score = 0.30×(λ_max_score) + 0.30×(ΔE_ST_score) + 0.25×(SOC_score) + 0.15×(E_ad_score)

Critères :
- λ_max : 680–720 nm → score 1.0; < 680 ou > 720 nm → score 0.5; hors NIR → score 0
- ΔE_ST : < 0,05 eV → score 1.0; 0,05–0,08 eV → score 0.7; > 0,08 eV → score 0
- SOC : > 50 cm⁻¹ → score 1.0; 30–50 cm⁻¹ → score 0.7; < 30 cm⁻¹ → score 0
- E_ad : < 1,0 eV → score 1.0; 1,0–1,2 eV → score 0.7; > 1,2 eV → score 0

Décision :
- Score ≥ 0.70 → GO (candidat retenu)
- Score < 0.70 → NO-GO (candidat rejeté)
```

### Prototype 2 : TPP–Iodo–BODIPY

```
Score = 0.25×(λ_max_score) + 0.25×(ΔE_ST_score) + 0.20×(SOC_score) + 0.15×(E_ad_score) + 0.15×(ciblage_score)

Critères :
- λ_max : 690–730 nm → score 1.0; < 690 ou > 730 nm → score 0.5; hors NIR → score 0
- ΔE_ST : < 0,08 eV → score 1.0; 0,08–0,10 eV → score 0.7; > 0,10 eV → score 0
- SOC : > 40 cm⁻¹ → score 1.0; 25–40 cm⁻¹ → score 0.7; < 25 cm⁻¹ → score 0
- E_ad : < 1,2 eV → score 1.0; 1,2–1,4 eV → score 0.7; > 1,4 eV → score 0
- Ciblage : Charge > +1,00 e ET Distance > 5 Å → score 1.0; l'un des deux → score 0.5; aucun → score 0

Décision :
- Score ≥ 0.70 → GO (candidat retenu)
- Score < 0.70 → NO-GO (candidat rejeté)
```

---

## 📝 Notes Importantes

### Semaine 2 : Sélection de la référence

- Chercher un BODIPY avec λ_max 500–600 nm et Φ_f > 0.1
- Vérifier que les données sont complètes et reproductibles
- Construire la géométrie en Avogadro/IQmol

### Semaine 3 : Test comparatif def2-SVP vs def2-TZVP

- Lancer ADC(2) sur la **référence** avec les deux bases
- Comparer MAE par rapport aux données expérimentales
- **Décision** : Choisir la base qui minimise MAE avec le moins de CPU

### Semaines 4–11 : Calculs des 3 molécules

- Appliquer la même chaîne de calcul à tous les 3
- Archiver systématiquement tous les `.gbw` et `.out`
- Utiliser convention de nommage : `<phase>_<molécule>_<tentative>_<base>`

### Semaine 11 : Décision finale

- Appliquer la grille Go/No-Go à chaque prototype
- Calculer le score final
- Identifier le prototype le plus prometteur (score ≥ 70%)

---

**Dernière mise à jour** : 15 novembre 2025
**Version** : 2.0 (révisée)
**Statut** : À jour
