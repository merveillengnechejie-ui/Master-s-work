# Planification Détaillée et Optimisation des Ressources

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

**Jours 3-5 (Mercredi-Vendredi)**
- Lecture : TNBC, fenêtre thérapeutique (6h)
- Lecture : BODIPY photophysique (6h)
- Lecture : DFT/ADC(2)/OO-DFT (6h)

**Livrables :** Notes de lecture, liste des 10 articles clés

---

### Semaine 2 : Synthèse et Sélection des Prototypes

**Jours 1-3 (L-M-M)**
- Rédaction synthèse bibliographique (4h)
- Identification des modifications chimiques clés (4h)
- Sélection des 3 prototypes (2h)

**Jours 4-5 (J-V)**
- Justification du design de chaque prototype (2h)
- Review avec encadrant (1h)

**Livrables :** Document synthèse (2-3 pages), descriptions prototypes

---

### Semaine 3 : Construction Moléculaire

**Jours 1-3 (L-M-M)**
- Construire proto-A dans Avogadro (3h)
- Construire proto-B dans Avogadro (3h)
- Construire proto-C dans Avogadro (3h)

**Jours 4-5 (J-V)**
- Pré-optimisation GFN2-xTB (3h calcul + 1h validation)
- Validation des géométries (2h)

**Livrables :** 3 fichiers `.xyz` validés

---

### Semaine 4 : S0 Optimisations (8 heures CPU/prototype)

**Lundi-Mercredi** : S0 gas phase
```
Proto-A: submit S0_gas_opt.inp     (30-60 min)
Proto-B: submit S0_gas_opt.inp     (parallèle)
Proto-C: submit S0_gas_opt.inp     (parallèle)
```

**Jeudi-Vendredi** : S0 eau + validation
```
Proto-A: submit S0_water_opt.inp   (45-90 min, après S0_gas)
Proto-B: submit S0_water_opt.inp   (parallèle)
Proto-C: submit S0_water_opt.inp   (parallèle)

Validation géométries (fréquences imaginaires : 1h)
```

**Livrables :** 3 fichiers S0_water_opt.gbw (CRITICAL)

---

### Semaine 5-6 : Excitations Verticales (60 heures CPU)

**Semaine 5 : Calculs ADC(2)**
```
Lundi:    Proto-A ADC2_vertical.inp    submit (60-120 min)
Mardi:    Proto-B ADC2_vertical.inp    submit (parallèle)
Mercredi: Proto-C ADC2_vertical.inp    submit (parallèle)
```

**Semaine 6 : Extraction et Benchmarking**
```
Lundi-Mardi:   Extraction λ_max des 3 prototypes
               Compilation des spectres
               
Mercredi-Jeudi: Benchmarking vs littérature
               Validation des méthodes
               
Vendredi:      Graphiques comparatifs
               Tableau des propriétés d'absorption
```

**Livrables :** 
- Tableau λ_max pour les 3 prototypes
- Graphiques spectres d'absorption
- Rapport benchmarking

---

### Semaine 7-8 : États Excités Relaxés (ΔE_{ST}, PTT)

#### Semaine 7 : T1 Optimisations (rapides, 60-120 min/prototype)

```
Lundi-Mercredi:   T1 optimisations (parallèles)
                  Proto-A submit T1_water_opt.inp
                  Proto-B submit T1_water_opt.inp
                  Proto-C submit T1_water_opt.inp
                  
Jeudi-Vendredi:   Extraction E_T1
                  Premiers calculs ΔE_{ST}
```

#### Semaine 8 : S1 Optimisations (très difficiles, 120-180 min/prototype)

```
Lundi:    Proto-A submit S1_water_opt.inp (préparation spéciale)
Mardi:    Proto-B submit S1_water_opt.inp
Mercredi: Proto-C submit S1_water_opt.inp

Jeudi-Vendredi: Monitoring et troubleshooting
                Si convergence difficile: adapter les stratégies
                Retry si nécessaire (peut doubler le temps)
```

**Stratégie de sauvegarde :** 
- Lancer tous les S1 le même jour (so they fail together = easy to fix all at once)
- Prévoir des strategies de recovery (voir Troubleshooting guide)

**Livrables :**
- 3 fichiers S1_water_opt.gbw (Important)
- Tableau ΔE_ST = E_S1 - E_T1

---


### Semaine 9 : Couplage Spin-Orbite (SOC) — Stratégie Pragmatique

> **Encart pratique SOC**
>
> - Pour le screening et la validation rapide des tendances SOC, utiliser systématiquement la méthode TD-DFT/ΔSCF (`dosoc` ORCA) sur tous les prototypes. Cette approche est rapide, fiable pour les comparaisons relatives, et adaptée au cadre d'un stage.
> - Les méthodes multi-références (FIC-NEVPT2/CASSCF) sont réservées aux finalistes ou aux cas où les ressources CPU le permettent. Elles sont très coûteuses et ne doivent pas être utilisées pour le screening de routine.
> - Mentionner explicitement dans le rapport si les valeurs SOC proviennent de TD-DFT rapide, et présenter NEVPT2/CASSCF comme une perspective future ou une validation ultime.
> - Cette stratégie garantit un workflow efficace, reproductible et adapté aux contraintes du projet.

**Option 1 : FIC-NEVPT2 (Haute Précision, 150-300 h CPU)**

```
Lundi:    Proto-A submit NEVPT2_SOC.inp  (150-300 min)
Mardi:    Proto-B submit NEVPT2_SOC.inp
Mercredi: Proto-C submit NEVPT2_SOC.inp

Jeudi-Vendredi: Monitoring et extraction des matrices SOC
                Benchmark SOC values vs literature
                (Continuer en parallèle avec phase d'analyse)
```

**Option 2 : TD-DFT Rapide (30-60 h CPU, si temps limité)**

```
Lundi:    Proto-A submit TDDFT_SOC_fast.inp  (30-60 min)
Mardi:    Proto-B submit TDDFT_SOC_fast.inp
Mercredi: Proto-C submit TDDFT_SOC_fast.inp

Jeudi-Vendredi: Extraction SOC values
                Comparaison rapide
```

**Stratégie optimale :** Commencer avec TDDFT rapide (semaine 9 jeudi), puis lancer NEVPT2 en fond si temps permet (continuer en semaine 9-10).

---

### Semaine 9-10 : Analyse Post-Traitement (Parallèle avec SOC)

**Jours 1-3 : Analyse de charge et MEP**

```
Lundi-Mercredi:
- Calculer charges Mulliken/Hirshfeld pour 3 prototypes
- Générer cartes MEP (Multiwfn)
- Valider localisation charge TPP+
- Vérifier accessibilité stériquement
```

**Jours 4-5 : Tableau Comparatif**

```
Jeudi-Vendredi:
- Compilation résultats : λ_max, E_ad, ΔE_ST, SOC
- Création tableau synthétique
- Première analyse des tendances
```

**Livrables :**
- Tableau comparatif complet (3 prototypes × 8 propriétés)
- Cartes MEP des 3 prototypes
- Graphiques comparatifs λ_max, E_ad, ΔE_ST

---

### Semaine 10 : Scoring et Décision

**Tâches Principales**

```
Lundi-Mercredi: Scoring des 3 prototypes
- Attribuer points pour chaque critère (voir Résumé Exécutif)
- Calculer scores pondérés
- Identifier meilleur candidat et alternatives

Jeudi-Vendredi: Analyse des tendances
- Effet de l'iode sur λ_max ?
- Effet du groupe TPP ?
- Synergie PDT + PTT : quelle combinaison est meilleure ?
```

**Livrables :**
- Feuille de scoring (candidats rankés)
- Analyse écrite : "Pourquoi proto-X est le meilleur ?"
- Recommendations pour améliorations futures

---

### Semaine 11 : Synthèse Résultats et Perspectives

**Tâches Principales**

```
Lundi-Mercredi: Finaliser les analyses
- Double-check tous les résultats
- Générer graphiques finaux de haute qualité
- Préparer diagrammes pour rapport

Jeudi-Vendredi: Brainstorm perspectives
- Stratégies futures (PDT Type I, pH-sensitivity, etc.)
- Nanomédecine : comment intégrer ce candidat dans une nanoparticule ?
- Applications cliniques potentielles
```

**Livrables :**
- Suite complète de graphiques publiables
- Document "Perspectives Future" (2-3 pages)

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
   - DFT, ADC(2), OO-DFT, ΔDFT (voir document principal)
   - Justification du changement TD-DFT → OO-DFT
   - Protocole ORCA 6.1 complet
   - Critères d'évaluation

4. Résultats (10-12 pages)
   - Géométries S0 (structures, distances)
   - λ_max et spectres (tableaux + graphiques)
   - E_adiabatic et potentiel PTT
   - ΔE_ST et potentiel PDT/ISC
   - SOC values et analyse
   - Charges atomiques et ciblage

5. Discussion (5-8 pages)
   - Comparaison prototypes
   - Scoring et ranking
   - Candidat optimal et justification
   - Connexion aux défis cliniques (hypoxie, sélectivité, TME)
   - Limitations des calculs

6. Perspectives et Conclusion (3-4 pages)
   - Améliorations futures (design molecular)
   - Stratégies nanotechnologiques
   - Perspectives pre-cliniques
   - Conclusion générale

7. Annexes
   - Fichiers d'input ORCA compllets
   - Données brutes
   - Graphiques supplémentaires
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
               
Vendredi:      Relecture finale + references
```

**Préparation Soutenance**

```
Lundi-Mercredi: Créer les diapositives (15-20 slides)
               - Titre + contexte (2)
               - Challenges + objectifs (2)
               - Théorie abrégée (2)
               - Résultats λ_max (2)
               - Résultats ΔE_ST + SOC (2)
               - Scoring + conclusion (2)
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
```

---

## Partie 3 : Stratégies d'Optimisation des Ressources Computationnelles

### 3.1 Parallélisation

**Bonne pratique 1 : Lancer les 3 prototypes en parallèle**

```bash
# Semaine 4 : S0 optim. pour tous les 3
for proto in proto-{A,B,C}; do
  cd $proto
  sbatch S0_gas_opt.slurm &
done

# Attendre puis lancer eau
for proto in proto-{A,B,C}; do
  cd $proto
  sbatch S0_water_opt.slurm &
done
```

**Gain de temps :** 3× parallélisation = 1/3 du temps

**Bonne pratique 2 : Chevauchement des étapes**

```
Semaine 6: Proto-A & B font ADC(2)
           Proto-C continue S0 optim. (s'il y a problème)
           
Semaine 8: Proto-A & B font S1 optim.
           Proto-C peut commencer SOC si S0/S1 terminés
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
| S1 opt | 8 | 1 (si dispo) | 48 GB | 4h | Difficile |
| NEVPT2 | 16 | 0 | 64 GB | 8h | Très coûteux |
| TDDFT SOC | 8 | 1 (si dispo) | 32 GB | 1h | Rapide |

---

### 3.3 Checkpointing et Reprise

Créer un système de checkpoints pour les calculs longs :

```bash
# Script de relance automatique
for i in {1..3}; do
  echo "Tentative $i de S1 optim..."
  
  # Lancer avec damping progressif
  DAMP=$((40 + i*10))
  sed -i "s/DampPercentage.*/DampPercentage $DAMP/" S1_water_opt.inp
  
  orca S1_water_opt.inp > S1_water_opt_attempt_$i.out 2>&1
  
  if grep -q "FINAL SINGLE POINT ENERGY" S1_water_opt_attempt_$i.out; then
    echo "✓ Success on attempt $i"
    break
  else
    echo "✗ Failed attempt $i"
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
for proto in proto-{A,B,C}; do
  cp $proto/*.gbw $BACKUP_DIR/
  cp $proto/*.xyz $BACKUP_DIR/
  cp $proto/*.out $BACKUP_DIR/  # Fichiers sorties importants
done

# Compresser
tar -czf "${BACKUP_DIR}.tar.gz" $BACKUP_DIR/
echo "Backup saved: ${BACKUP_DIR}.tar.gz"
```

---

## Partie 4 : Métriques de Suivi (Tracking)

### Tableau d'avancement

```
Étape              | Status  | Date Start | Date End | CPU Hours | Issues
================================================================================
S0 gas (3 proto)   | ✓ DONE  | 2025-11-20 | 2025-11-21 | 3       | None
S0 water (3 proto) | ✓ DONE  | 2025-11-22 | 2025-11-23 | 5       | None
ADC2 (3 proto)     | ⏳ RUN   | 2025-11-24 |            | 18/60   | Slow?
T1 opt (3 proto)   | ⏱ WAIT  | 2025-12-01 |            |         | Après ADC2
S1 opt (3 proto)   | ⏱ WAIT  | 2025-12-02 |            |         | Difficile
NEVPT2 (3 proto)   | ⏱ WAIT  | 2025-12-05 |            |         | Très cher
Analyse            | 🔄 IP   | 2025-12-08 | 2025-12-10 |         | En cours
Rapport (draft)    | 🔄 IP   | 2025-12-10 | 2025-12-16 |         | Rédaction
Soutenance         | ⏱ WAIT  | 2025-12-19 |            |         |

Légende: ✓ DONE, 🔄 IP (in progress), ⏱ WAIT, ⏳ RUN, ✗ FAILED, ⚠ RETRY
```

---

## Partie 5 : Gestion des Crises

### Si les calculs prennent du retard

**Scénario 1 : ADC(2) trop lent**

**Action :** 
- Réduire n_exc_states de 10 à 5
- Utiliser def-SVP à la place de def-TZVP
- Utiliser TDA-ADC(2) plus rapide

**Impact :** Perte de précision négligeable pour λ_max

---

### Si S1 ne converge pas (Semaine 8)

**Action d'urgence :**
1. Vérifier le fichier S0_water_opt.gbw (corrompu ?)
2. Relancer S0 optim. si nécessaire (1-2 heures)
3. Utiliser stratégies de convergence robuste (voir Troubleshooting)
4. Si toujours échec : sauter S1, utiliser S1 approximation de TD-DFT

**Impact :** Perdre E_adiabatic (PTT), mais conserver λ_max et ΔE_ST

---

### Si NEVPT2 n'est pas terminé avant Semaine 11

**Action :**
- Utiliser TD-DFT rapide pour SOC (30 min/prototype)
- Note dans le rapport : "SOC values from fast TD-DFT" (transparent)
- Mentionner NEVPT2 comme perspective future

**Impact :** Moins précis, mais toujours informatif

---

## Partie 6 : Ressources à Archiver

À la fin du projet, conserver :

```
/archive/projet_stage_BODIPY_2025/
├── COMPUTE
│   ├── S0_optim/             (géométries)
│   ├── ADC2_spectra/         (λ_max data)
│   ├── S1_S0_analysis/       (énergies)
│   ├── T1_ISC_analysis/      (ΔE_ST)
│   └── SOC_calculations/     (SOC values)
│
├── RESULTS
│   ├── comparison_table.csv  (tableau final)
│   ├── scoring_matrix.xlsx   (ranking)
│   ├── figures/              (graphiques HQ)
│   └── summary_report.txt    (1 page résumé)
│
├── DOCUMENTATION
│   ├── demarche_methodologique_v2_integree.md
│   ├── Guide_Pratique_ORCA_Scripts.md
│   ├── input_templates/      (tous les INP)
│   └── output_logs/          (tous les OUT)
│
└── FINAL
    ├── Rapport_stage_final.pdf
    ├── Presentation_soutenance.pdf
    └── README.md  (guide pour archivage futur)
```

---

**Document de planification pour le stage complet — À mettre à jour chaque lundi !**
