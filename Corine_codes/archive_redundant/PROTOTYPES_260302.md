# PROTOTYPES : Description des 3 Molécules

## 📋 Vue d'ensemble

Ce document décrit les **3 molécules** du projet révisé (Mar. 2026) :
- **1 molécule de référence expérimentale** (externe, publiée) pour benchmarking
- **2 prototypes internes** : Iodo-BODIPY + TPP–Iodo–BODIPY
- **Configuration** : 4 cœurs / 16 Go RAM (%maxcore 3500)

---

## 🔬 Molécule 1 : Référence Expérimentale (Externe)

### Rôle
Valider la **chaîne de calcul ΔDFT+SOC** en reproduisant une molécule dont les propriétés sont **déjà publiées**. **Cette molécule est utilisée UNIQUEMENT à des fins de validation/benchmarking, PAS pour l'évaluation finale des propriétés photophysiques.**

### Critères de sélection

| Critère | Priorité | Détails |
| :--- | :--- | :--- |
| **λ_max expérimental** | 1 | 500–600 nm (visible, bien caractérisé, loin de NIR) |
| **Rendement quantique Φ_f** | 2 | > 0.1 (molécule fluorescente robuste) |
| **Données SOC** | 3 | Si disponibles, constants S1↔T1 (rare mais idéal) |
| **Accessibilité** | 4 | Article récent (< 5 ans), données complètes |

### Exemple concret recommandé

**Molécule** : BODIPY méso-phényle (BODIPY-Ph)

| Propriété | Valeur | Source |
| :--- | :--- | :--- |
| **λ_max exp.** | ~505 nm | DMSO (ou milieu biologique pertinent) |
| **Φ_f exp.** | ~0.8 | DMSO (ou milieu biologique pertinent) |
| **Structure** | Simple (pas de substituants complexes) | Facile à modéliser |
| **Justification** | Loin de NIR (bon contraste avec prototypes) | Permet validation claire |

### Sources recommandées

- *European Journal of Organic Chemistry* (BODIPY design)
- *Journal of Medicinal Chemistry* (BODIPY théranostique)
- *Photochemistry and Photobiology Science* (propriétés photophysiques)
- *Journal of Physical Chemistry A* (SOC, états excités)

### Procédure de benchmarking (Référence seulement)

1. **Construire la géométrie de la molécule de référence** (Avogadro/IQmol)
2. **Optimiser S₀** pour la molécule de référence (B3LYP-D3/def2-SVP, SMD mixed pour environnement biologique complexe)
3. **Calculer λ_max** pour la molécule de référence (TD-DFT/wB97X-D3/def2-SVP, SMD mixed)
4. **Comparer avec expérience** :
   - **Critère de validation** : MAE < 0.1 eV (≈ 10 nm à 700 nm)
   - Si MAE > 0.1 eV : Investiguer (base? solvant? géométrie?)
5. **Notes sur le milieu biologique** : Les calculs sont effectués dans un environnement biologique complexe (SMD mixed) pour une meilleure corrélation avec les conditions physiologiques
6. **Valider la chaîne** avant d'attaquer les prototypes
7. **IMPORTANT** : La molécule de référence est UTILISÉE UNIQUEMENT pour la validation de la méthode, PAS pour les calculs finaux d'évaluation des prototypes

### Fichiers associés

```
Référence_BODIPY_Ph.xyz          # Géométrie optimisée
S0_ref_opt.gbw                   # Résultat S0 optimisé
TDDFT_ref_vertical.out           # Résultat TD-DFT (wB97X-D3)
T1_ref_opt.gbw                   # Résultat T1 optimisé
S1_ref_opt.gbw                   # Résultat S1 optimisé
SOC_ref_DELTADFT.out             # Résultat SOC (Quick/ΔDFT)
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
TDDFT_iodo_vertical.out          # Résultat TD-DFT (wB97X-D3)
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
TDDFT_tpp_iodo_vertical.out     # Résultat TD-DFT (wB97X-D3)
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

### ⚠️ Clarification Importante sur les Calculs

**Molécule de référence** :
- Utilisée UNIQUEMENT pour la validation de la méthode (benchmarking)
- Ne fait PAS l'objet d'une évaluation complète des propriétés photophysiques
- Ne participe PAS à la grille Go/No-Go finale

**Prototypes (Iodo-BODIPY et TPP-Iodo-BODIPY)** :
- Sont les SEULES molécules soumises à la chaîne de calcul complète
- Seules ces deux molécules subissent les calculs S₀, T₁, S₁, ADC(2), et SOC
- Seules ces deux molécules sont évaluées via la grille Go/No-Go

**Calculs effectués sur les prototypes** :
- Optimisation S₀ (état fondamental)
- Optimisation T₁ (état triplet)
- Optimisation S₁ (état singulet excité)
- Calculs TD-DFT (wB97X-D3) pour λ_max
- Calculs SOC (couplage spin-orbite)
- Évaluation finale via grille Go/No-Go

---

**Dernière mise à jour** : 3 mars 2026
**Version** : 3.0 (révisée pour exécution matériel local)
**Statut** : À jour (16 Go RAM / TD-DFT)
