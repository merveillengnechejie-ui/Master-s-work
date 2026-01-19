# Planification Détaillée et Optimisation des Ressources (Version Révisée 15/11/2025)

**Portée révisée (15/11/2025)** : 1 molécule de référence expérimentale + 2 prototypes internes (Iodo-BODIPY + TPP-Iodo-BODIPY) au lieu des 3 prototypes initiaux.

## Partie 1 : Chronogramme Gantt Détaillé (14 semaines)

### Vue d'ensemble par phase

```
PHASE 1: IMMERSION (Semaines 1-3)
|========================================| 3 semaines, effort: 100% théorie

PHASE 2: CALCULS FONDAMENTAUX (Semaines 4-8)
|===|===|========|========|=========| 5 semaines, effort: 80% calcul, 20% suivi

PHASE 3: ANALYSE (Semaines 9-11)
|===|===|===| 3 semaines, effort: 100% analyse

PHASE 4: SYNTHÈSE (Semaines 12-14)
|===|===|===| 3 semaines, effort: 100% rédaction/présentation
```

---

## Partie 2 : Calendrier Détaillé par Semaine

### Semaine 1 : Formation et Bibliographie

**Jours 1-2 (Lundi-Mardi)**
- Prise en main Linux/SLURM
- Installation/configuration ORCA 6.1
- Accès au cluster HPC
- Validation du jeu de test pré-rempli (S0_opt.gbw, etc.) pour vérifier la chaîne de calcul

**Jours 3-5 (Mercredi-Vendredi)**
- Lecture : TNBC, fenêtre thérapeutique (6h)
- Lecture : BODIPY photophysique (6h)
- Lecture : DFT/ADC(2)/ΔDFT, SOC (6h)
- Mise en place convention de nommage pour les fichiers (ex: S1_protoA_attempt3_opt.gbw)

**Livrables :** Notes de lecture, liste des 10 articles clés, convention de nommage documentée

---

### Semaine 2 : Synthèse et Sélection des Prototypes

**Jours 1-3 (L-M-M)**
- Rédaction synthèse bibliographique (4h)
- Identification des modifications chimiques clés (4h)
- Sélection de la molécule de référence expérimentale (λ_max, Φ_f, SOC publiés) (2h)

**Jours 4-5 (J-V)**
- Définition des 2 prototypes internes : Iodo-BODIPY (PDT), TPP-Iodo-BODIPY (théranostique) (2h)
- Rédaction de la grille Go/No-Go quantitative (2h)
- Review avec encadrant (1h)

**Livrables :** Document synthèse (2-3 pages), descriptions prototypes, grille Go/No-Go

---

### Semaine 3 : Construction Moléculaire et Test Comparatif

**Jours 1-3 (L-M-M)**
- Construire la molécule de référence dans Avogadro (3h)
- Construire Iodo-BODIPY dans Avogadro (3h)
- Construire TPP-Iodo-BODIPY dans Avogadro (3h)

**Jours 4-5 (J-V)**
- Pré-optimisation GFN2-xTB (3h calcul + 1h validation)
- Validation des géométries (2h)
- **TEST CRITIQUE** : Lancer ADC(2) def2-SVP vs def2-TZVP sur la référence (batch de nuit)
- Comparer λ_max (MAE par rapport à expérience)

**Livrables :** 3 fichiers `.xyz` validés, rapport test def2-SVP vs def2-TZVP

---

### Semaine 4 : S0 Optimisations (8 heures CPU/prototype)

**Lundi-Mercredi** : S0 gas phase
```
Référence: submit S0_gas_opt.inp     (30-60 min, validation du workflow)
Iodo-BODY: submit S0_gas_opt.inp     (parallèle)
TPP-Iodo:  submit S0_gas_opt.inp     (parallèle)
```

**Jeudi-Vendredi** : S0 eau + validation
```
Référence: submit S0_water_opt.inp   (45-90 min, après S0_gas)
Iodo-BODY: submit S0_water_opt.inp   (parallèle)
TPP-Iodo:  submit S0_water_opt.inp   (parallèle)

Validation géométries (fréquences imaginaires : 1h)
```

**Livrables :** 3 fichiers S0_water_opt.gbw (CRITICAL)

---

### Semaine 5-6 : Excitations Verticales (60 heures CPU)

**Semaine 5 : Calculs ADC(2)**
```
Lundi:    Référence ADC2_vertical.inp    submit (60-120 min)
Mardi:    Iodo-BODY ADC2_vertical.inp    submit (parallèle)
Mercredi: TPP-Iodo  ADC2_vertical.inp    submit (parallèle)
```

**Semaine 6 : Extraction et Benchmarking**
```
Lundi-Mardi:   Extraction λ_max des 3 prototypes
               Compilation des spectres

Mercredi-Jeudi: Benchmarking vs littérature
               Validation des méthodes (MAE < 0.1 eV)
               Comparaison def2-SVP vs def2-TZVP (si applicable)

Vendredi:      Graphiques comparatifs
               Tableau des propriétés d'absorption
```

**Livrables :**
- Tableau λ_max pour les 3 prototypes
- Graphiques spectres d'absorption
- Rapport benchmarking (MAE, R²)
- Décision sur base à utiliser (def2-SVP vs def2-TZVP)

---

### Semaine 7-8 : États Excités Relaxés (ΔE_{ST}, PTT)

#### Semaine 7 : T1 Optimisations (rapides, 60-120 min/prototype)

```
Lundi-Mercredi:   T1 optimisations (parallèles)
                  Référence submit T1_water_opt.inp
                  Iodo-BODY submit T1_water_opt.inp
                  TPP-Iodo  submit T1_water_opt.inp

Jeudi-Vendredi:   Extraction E_T1
                  Premiers calculs ΔE_{ST}
```

#### Semaine 8 : S1 Optimisations (très difficiles, 120-180 min/prototype)

```
Lundi:    Iodo-BODY submit S1_water_opt.inp (préparation spéciale via gen_s1_guesses.sh)
Mardi:    TPP-Iodo  submit S1_water_opt.inp (via gen_s1_guesses.sh)
Mercredi: Référence submit S1_water_opt.inp  (pour validation)

Jeudi-Vendredi: Monitoring et troubleshooting
                Si convergence difficile: utiliser run_troubleshoot_S1.sh
                Retry si nécessaire (prévoir buffer +200-300%)
```

**Stratégie de sauvegarde :**
- Lancer les S1 dans l'ordre de priorité (Iodo-BODY, TPP-Iodo, Référence)
- Utiliser gen_s1_guesses.sh pour générer 3 guess (HOMO→LUMO, HOMO-1→LUMO, HOMO→LUMO+1)
- Utiliser run_troubleshoot_S1.sh avec escalade automatique (LevelShift/Damp/DIIS_TRAH)
- Prévoir des strategies de recovery (voir Troubleshooting guide)

**Livrables :**
- 3 fichiers S1_water_opt.gbw (Important)
- Tableau ΔE_ST = E_S1 - E_T1
- Protocole de convergence S₁ documenté

---


### Semaine 9 : Couplage Spin-Orbite (ΔDFT+SOC) — Stratégie Pragmatique (Version Révisée)

> **Encart pratique SOC**
>
> - Pour le screening et la validation rapide des tendances SOC, utiliser systématiquement la méthode **ΔDFT+SOC (ZORA, dosoc)** sur tous les prototypes. Cette approche est **10× plus rapide** que NEVPT2, **cohérente** avec le workflow ΔDFT (S1/T1), et fiable pour les comparaisons relatives.
> - Les méthodes multi-références (FIC-NEVPT2/CASSCF) sont réservées à **une validation ponctuelle** si ressources disponibles, ou pour des candidats retenus. Elles sont très coûteuses.
> - Mentionner explicitement dans le rapport que les valeurs SOC proviennent de ΔDFT+SOC, et présenter NEVPT2 comme une **validation ponctuelle** (optionnelle).
> - Cette stratégie garantit un workflow **efficace, reproductible et adapté aux contraintes du projet**.

**Stratégie recommandée : ΔDFT+SOC (ZORA, dosoc)**

```
Lundi:    Référence submit DeltaSOC_recommended.inp  (30-60 min)
Mardi:    Iodo-BODY submit DeltaSOC_recommended.inp  (30-60 min)
Mercredi: TPP-Iodo  submit DeltaSOC_recommended.inp  (30-60 min)

Jeudi-Vendredi: Extraction des constantes SOC
                Analyse comparative (S1↔Tn couplages)
                (Continuer en parallèle avec phase d'analyse)
```

**Validation ponctuelle NEVPT2 (si ressources disponibles)**

```
Vendredi de la semaine 9 (ou semaine 10) :
         Lancer NEVPT2_SOC_validation.inp sur le meilleur candidat identifié
         Comparaison ΔDFT+SOC vs NEVPT2 (validation de tendance)
```

**Stratégie optimale :** Utiliser ΔDFT+SOC pour le screening (gain 10× temps), validation ponctuelle NEVPT2 si ressources.

---

### Semaine 9-10 : Analyse Post-Traitement (Parallèle avec SOC)

**Jours 1-3 : Analyse de charge et MEP pour ciblage mitochondrial**

```
Lundi-Mercredi:
- Calculer charges Mulliken/Hirshfeld pour 3 molécules
- Générer cartes MEP (Multiwfn)
- Valider localisation charge TPP+ (sur TPP-Iodo-BODY)
- Vérifier accessibilité stériquement (distance TPP⁺ → centre BODIPY > 5 Å)
- Analyser angle dièdre TPP⁺-BODIPY (> 90°)
- Évaluer la distribution spatiale du cation lipophile
```

**Jours 4-5 : Analyse des propriétés photophysiques**

```
Jeudi-Vendredi:
- Extraction des rendements quantiques (Φ_f, Φ_p, Φ_Δ)
- Analyse des temps de vie des états excités
- Taux de processus photophysiques (k_f, k_{ISC}, k_{nr})
- Calcul des indicateurs de photostabilité (PSI)
- Calcul des indicateurs PTT (TCI)
- Compilation résultats : λ_max, E_ad, ΔE_ST, SOC, charges, PSI, TCI
```

**Livrables :**
- Tableau comparatif complet (3 molécules × propriétés photophysiques)
- Cartes MEP des 3 molécules (mise en évidence charge TPP+)
- Graphiques comparatifs λ_max, E_ad, ΔE_ST
- Analyse des propriétés photophysiques

---

### Semaine 10 : Scoring et Décision (Grille Go/No-Go Quantitative)

**Tâches Principales**

```
Lundi-Mercredi: Application de la grille Go/No-Go quantitative
- Prototype Iodo-BODIPY : λ_max [680-720nm] (25%), E_ad < 1.0 eV (15%),
  ΔE_ST < 0.05 eV (25%), SOC > 50 cm⁻¹ (25%), PSI > 1 (10%)
- Prototype TPP-Iodo-BODIPY : λ_max [690-730nm] (20%), E_ad < 1.2 eV (15%),
  ΔE_ST < 0.08 eV (20%), SOC > 40 cm⁻¹ (15%), critères ciblage (30%):
  - Charge TPP⁺: +1,00 e
  - Distance TPP⁺ → centre BODIPY: > 5 Å
  - Angle dièdre TPP⁺-BODIPY: > 90°
  - Potentiel membranaire prédit: ΔΨ > 150 mV
  - Coefficient de perméabilité: P_app > 10⁻⁶ cm/s
  - Rapport d'accumulation: ≥ 10
  - Énergie liaison membrane: ≥ -20 kcal/mol
- Calcul des scores pondérés
- Identification du candidat optimal (score ≥ 70%)
```

**Jeudi-Vendredi: Analyse des tendances et validation**
- Effet de l'iode sur λ_max et ISC ?
- Effet du groupe TPP sur ciblage et propriétés ?
- Synergie PDT + PTT : quelle combinaison est meilleure ?
- Analyse de la photostabilité relative
- Validation méthodologique (MAE, R²)

**Livrables :**
- Feuille de scoring avec grille Go/No-Go (candidats rankés)
- Analyse écrite : "Pourquoi tel candidat est le meilleur ?"
- Recommendations pour améliorations futures
- Validation méthodologique complète

---

### Semaine 11 : Synthèse Résultats et Perspectives

**Tâches Principales**

```
Lundi-Mercredi: Finaliser les analyses
- Double-check tous les résultats
- Générer graphiques finaux de haute qualité
- Préparer diagrammes pour rapport
- Analyse de la validation méthodologique (ensemble de BODIPY)

Jeudi-Vendredi: Brainstorm perspectives
- Stratégies futures (PDT Type I, pH-sensitivity, etc.)
- Nanomédecine : comment intégrer ce candidat dans une nanoparticule ?
- Applications cliniques potentielles
- Analyse de toxicité prédictive (sites réactifs, ADME, génotoxicité)
- Perspectives pour une validation expérimentale
```

**Livrables :**
- Suite complète de graphiques publiables
- Document "Perspectives Future" (2-3 pages)
- Analyse de toxicité prédictive

---

### Semaine 12 : Rédaction du Rapport (Draft)

**Plan du Rapport (30-50 pages)**

```
1. Introduction (3-4 pages)
   - TNBC et challenge
   - PDT/PTT concepts
   - Objectives du projet

2. État de l'Art (5-7 pages)
   - BODIPY design
   - Fenêtre thérapeutique NIR
   - Ciblage mitochondrial
   - Littérature pertinente

3. Théorie et Méthodes (8-10 pages)
   - DFT, ADC(2), ΔDFT, ΔDFT+SOC (voir document principal)
   - Justification du changement TD-DFT → ΔDFT
   - Protocole ORCA 6.1 complet
   - Protocole avancé de convergence S₁ (ΔSCF)
   - Analyse des propriétés photophysiques
   - Critères d'évaluation

4. Résultats (10-12 pages)
   - Géométries S0 (structures, distances)
   - λ_max et spectres (tableaux + graphiques)
   - E_adiabatic et potentiel PTT
   - ΔE_ST et potentiel PDT/ISC
   - SOC values via ΔDFT+SOC et validation ponctuelle NEVPT2
   - Charges atomiques et ciblage mitochondrial
   - Propriétés photophysiques (Φ_f, Φ_Δ, temps de vie)
   - Photostabilité (PSI, TCI)
   - Critères de toxicité prédictive

5. Discussion (5-8 pages)
   - Comparaison 3 molécules (référence, Iodo-BODY, TPP-Iodo)
   - Scoring et ranking via grille Go/No-Go
   - Candidat optimal et justification
   - Connexion aux défis cliniques (hypoxie, sélectivité, TME)
   - Limitations des calculs
   - Perspectives nanotechnologiques et expérimentales

6. Perspectives et Conclusion (3-4 pages)
   - Améliorations futures (design molecular)
   - Stratégies nanotechnologiques
   - Perspectives pre-cliniques
   - Conclusion générale

7. Annexes
   - Fichiers d'input ORCA complets
   - Données brutes
   - Graphiques supplémentaires
   - Protocole de validation méthodologique
```

**Schedule de rédaction**

```
Lundi-Mardi:    Intro + État de l'art (2-3 pages/jour)
Mercredi-Jeudi: Théorie + Méthodes (3-4 pages/jour)
Vendredi:       Résultats (intro + premier tiers)
```

**Livrables :** Draft complet du rapport

---

### Semaine 13 : Finalisation Rapport + Préparation Soutenance

**Rédaction Finale**

```
Lundi-Mardi:   Résultats (suite + fin)
               Discussion complète

Mercredi-Jeudi: Perspectives + Conclusion
               Review et corrections
               Validation méthodologique étendue (ensemble de BODIPY)

Vendredi:      Relecture finale + references
```

**Préparation Soutenance**

```
Lundi-Mercredi: Créer les diapositives (15-20 slides)
               - Titre + contexte (2)
               - Challenges + objectifs (2)
               - Théorie abrégée ΔDFT (2)
               - Résultats λ_max (2)
               - Résultats ΔE_ST + SOC (2)
               - Grille Go/No-Go et décision (2)
               - Ciblage mitochondrial (2)
               - Q&A slide (1)

Jeudi-Vendredi: Préparer discours
               Répétition 1 (chronométrage)
               Ajustements
```

**Livrables :**
- Rapport final (PDF)
- Slides de présentation (PDF + PPTX backup)

---

### Semaine 14 : Soutenance et Finalisation

**Lundi-Mercredi : Préparation Finale**

```
- Réunion de relecture (1h)
- Corrections finales du rapport
- Dernière répétition (1h)
- Validation du plan B si S₁ a échoué (voir guide troubleshooting)
```

**Jeudi : SOUTENANCE**

```
- Présentation orale (15 min)
- Défense questions (5-10 min)
- Feedback du jury
```

**Vendredi : Clôture**

```
- Intégrer les feedbacks du jury (si demandé)
- Archivage final des calculs
- Dépôt du rapport définitif
- Lettre d'intention avec partenaire expérimental (si applicable)
```

---

## Partie 3 : Stratégies d'Optimisation des Ressources Computationnelles

### 3.1 Parallélisation

**Bonne pratique 1 : Lancer les 3 molécules en parallèle**

```bash
# Semaine 4 : S0 optim. pour tous les 3
for mol in reference iodo tpp-iodo; do
  cd $mol
  sbatch S0_gas_opt.slurm &
done

# Attendre puis lancer eau
for mol in reference iodo tpp-iodo; do
  cd $mol
  sbatch S0_water_opt.slurm &
done
```

**Gain de temps :** 3× parallélisation = 1/3 du temps

**Bonne pratique 2 : Chevauchement des étapes**

```
Semaine 6: Référence & Iodo font ADC(2)
           TPP-Iodo continue S0 optim. (s'il y a problème)

Semaine 8: Référence & Iodo font S1 optim.
           TPP-Iodo peut commencer SOC si S0/S1 terminés
```

---

### 3.2 Optimisation des allocations SLURM

**Fichier de soumission recommandé :** `submit_S0.slurm`

```bash
#!/bin/bash
#SBATCH --job-name=S0_optim
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=1
#SBATCH --mem=32GB
#SBATCH --time=02:00:00           # 2 heures pour S0 (generous)
#SBATCH --partition=gpu           # Utiliser GPU si disponible
#SBATCH --gres=gpu:1              # 1 GPU accélère de 3-4×

module load orca/6.1
cd $SLURM_SUBMIT_DIR

orca S0_water_opt.inp > S0_water_opt.out 2>&1

# Email notification
sbatch --mail-user=user@uni.fr --mail-type=END submit_next.slurm
```

**Allocation par étape :**

| Étape | CPUs | GPU | Mémoire | Temps | Notes |
|:---|:---|:---|:---|:---|:---|
| S0 opt | 8 | 1 (si dispo) | 32 GB | 2h | Rapide |
| ADC(2) | 8 | 1 (si dispo) | 32 GB | 4h | Coûteux |
| T1 opt | 8 | 1 (si dispo) | 32 GB | 2h | Rapide |
| S1 opt | 8 | 1 (si dispo) | 48 GB | 4h | Difficile (buffer +200-300%) |
| ΔDFT+SOC | 8 | 1 (si dispo) | 32 GB | 1h | Rapide (gain 10× vs NEVPT2) |
| MEP/ciblage | 4 | 0 | 16 GB | 15 min | Très rapide |

---

### 3.3 Checkpointing et Reprise

Créer un système de checkpoints pour les calculs longs :

```bash
# Script de relance automatique pour S1 optim.
for i in {1..5}; do  # Jusqu'à 5 tentatives avec buffer
  echo "Tentative $i de S1 optim..."

  # Lancer avec damping progressif et autres stratégies
  DAMP=$((40 + i*10))
  sed -i "s/DampPercentage.*/DampPercentage $DAMP/" S1_water_opt.inp

  LEVELSHIFT=$((20 + i*10))
  sed -i "s/LevelShift.*/LevelShift 0.$LEVELSHIFT/" S1_water_opt.inp

  orca S1_water_opt.inp > S1_water_opt_attempt_$i.out 2>&1

  if grep -q "FINAL SINGLE POINT ENERGY" S1_water_opt_attempt_$i.out; then
    echo "✓ Success on attempt $i"
    break
  else
    echo "✗ Failed attempt $i, trying next strategy"
  fi
done
```

---

### 3.4 Sauvegarde Incrémentale

```bash
# Créer snapshots tous les 2 jours
#!/bin/bash

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/projet_stage_${TIMESTAMP}"

mkdir -p $BACKUP_DIR

# Copier fichiers importants
for mol in reference iodo tpp-iodo; do
  cp $mol/*.gbw $BACKUP_DIR/
  cp $mol/*.xyz $BACKUP_DIR/
  cp $mol/*.out $BACKUP_DIR/  # Fichiers sorties importants
  cp $mol/*.log $BACKUP_DIR/  # Fichiers log si existants
done

# Compresser
tar -czf "${BACKUP_DIR}.tar.gz" $BACKUP_DIR/
echo "Backup saved: ${BACKUP_DIR}.tar.gz"
```

---

## Partie 4 : Métriques de Suivi (Tracking)

### Tableau d'avancement

```
Étape                        | Status  | Date Start | Date End | CPU Hours | Issues
=======================================================================================
S0 gas (3 mol)              | ✓ DONE  | 2025-11-20 | 2025-11-21 | 3       | None
S0 water (3 mol)            | ✓ DONE  | 2025-11-22 | 2025-11-23 | 5       | None
ADC2 (3 mol)                | ⏳ RUN   | 2025-11-24 |            | 18/60   | Slow?
T1 opt (3 mol)              | ⏱ WAIT  | 2025-12-01 |            |         | Après ADC2
S1 opt (3 mol)              | ⏱ WAIT  | 2025-12-02 |            |         | Difficile (buffer +200-300%)
ΔDFT+SOC (3 mol)            | ⏱ WAIT  | 2025-12-04 |            | 2       | Rapide
MEP/ciblage (2 mol)         | ⏱ WAIT  | 2025-12-05 |            | 0.5     | Rapide
Analyse                      | 🔄 IP   | 2025-12-08 | 2025-12-10 |         | En cours
Grille Go/No-Go              | 🔄 IP   | 2025-12-09 | 2025-12-10 |         | En cours
Rapport (draft)              | 🔄 IP   | 2025-12-10 | 2025-12-16 |         | Rédaction
Soutenance                   | ⏱ WAIT  | 2025-12-19 |            |         |

Légende: ✓ DONE, 🔄 IP (in progress), ⏱ WAIT, ⏳ RUN, ✗ FAILED, ⚠ RETRY
```

---

## Partie 5 : Gestion des Crises

### Si les calculs prennent du retard

**Scénario 1 : ADC(2) trop lent**

**Action :**
- Comparer def2-SVP vs def2-TZVP (test fait semaine 3)
- Si MAE < 5 nm pour def2-SVP : utiliser def2-SVP pour tous les ADC(2) (économie 3h/molécule)
- Économie potentielle : 9h CPU total sur le projet

---

### Si S1 ne converge pas après 3-5 tentatives (Semaine 8)

**Action d'urgence (Plan B) :**
1. Vérifier le fichier S0_water_opt.gbw (corrompu ?)
2. Relancer S0 optim. si nécessaire (1-2 heures)
3. Utiliser stratégies de convergence robuste (voir Troubleshooting)
4. Si toujours échec :
   - TD-DFT (ωB97X-D) pour excitations verticales diagnostiques uniquement
   - Continuer T1 (ΔUKS) + SOC (ΔDFT+SOC) pour les tendances
   - Reporter l'optimisation S1 complète en perspective

**Impact :** Perdre E_adiabatic (PTT), mais conserver λ_max, ΔE_ST et SOC

---

### Si ΔDFT+SOC n'est pas nécessairement terminé avant Semaine 11

**Action :**
- ΔDFT+SOC est rapide (30-60 min/mol) → très improbable
- Si problème : utiliser TD-DFT rapide pour SOC comme solution de repli
- Note dans le rapport : "SOC values from ΔDFT+SOC (ZORA, dosoc)" (standard)
- Mentionner NEVPT2 comme validation ponctuelle seulement

**Impact :** ΔDFT+SOC est bien adapté, pas de perte d'information

---

## Partie 6 : Ressources à Archiver

À la fin du projet, conserver :

```
/archive/projet_stage_BODIPY_2025/
├── COMPUTE
│   ├── reference/            (géométries référence)
│   ├── iodo/                 (géométries Iodo-BODY)
│   ├── tpp-iodo/             (géométries TPP-Iodo-BODY)
│   ├── S0_optim/             (tous les S0)
│   ├── ADC2_spectra/         (λ_max data)
│   ├── S1_S0_analysis/       (énergies)
│   ├── T1_ISC_analysis/      (ΔE_ST)
│   ├── SOC_calculations/     (ΔDFT+SOC values)
│   └── MEP_analysis/         (ciblage)
│
├── RESULTS
│   ├── comparison_table.csv  (tableau final 3 molécules)
│   ├── scoring_matrix.xlsx   (grille Go/No-Go)
│   ├── figures/              (graphiques HQ)
│   └── summary_report.txt    (1 page résumé)
│
├── DOCUMENTATION
│   ├── demarche_methodologique_v2_integree.md
│   ├── Guide_Pratique_ORCA_Scripts.md
│   ├── input_templates/      (tous les INP)
│   ├── output_logs/          (tous les OUT)
│   └── validation_results/   (ensemble de BODIPY, MAE, R²)
│
└── FINAL
    ├── Rapport_stage_final.pdf
    ├── Presentation_soutenance.pdf
    └── README.md  (guide pour archivage futur)
```

---

**Document de planification pour le stage complet — À mettre à jour chaque lundi !**
