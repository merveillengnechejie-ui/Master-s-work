# Planification Détaillée et Optimisation des Ressources (Version 260304)

> **Mise à jour : 04 mars 2026 (260304)**
> - Exécution locale 16 Go RAM / TD-DFT ωB97X-D3
> - Configuration : 4 cœurs, %maxcore 3500
> - Séquentiel local (nohup) au lieu de SLURM

**Portée révisée** : 1 molécule de référence expérimentale + 2 prototypes internes (Iodo-BODIPY + TPP-Iodo-BODIPY).

---

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
- Prise en main ORCA 6.1 (local)
- Configuration : %maxcore 3500, %pal nprocs 4
- Validation du jeu de test pré-rempli (benzène)

**Jours 3-5 (Mercredi-Vendredi)**
- Lecture : TNBC, fenêtre thérapeutique (6h)
- Lecture : BODIPY photophysique (6h)
- Lecture : TD-DFT/ΔDFT, SOC (6h)
- Mise en place convention de nommage

**Livrables :** Notes de lecture, liste des 10 articles clés

---

### Semaine 2 : Synthèse et Sélection des Prototypes

**Jours 1-3 (L-M-M)**
- Rédaction synthèse bibliographique (4h)
- Identification modifications chimiques clés (4h)
- Sélection molécule de référence expérimentale (2h)

**Jours 4-5 (J-V)**
- Définition des 2 prototypes internes (2h)
- Rédaction grille Go/No-Go quantitative (2h)
- Review avec encadrant (1h)

**Livrables :** Document synthèse (2-3 pages), descriptions prototypes, grille Go/No-Go

---

### Semaine 3 : Construction Moléculaire et Test Comparatif

**Jours 1-3 (L-M-M)**
- Construire référence dans Avogadro (3h)
- Construire Iodo-BODIPY dans Avogadro (3h)
- Construire TPP-Iodo-BODIPY dans Avogadro (3h)

**Jours 4-5 (J-V)**
- Pré-optimisation GFN2-xTB (3h calcul + 1h validation)
- Validation des géométries (2h)
- **TEST CRITIQUE** : TD-DFT def2-SVP vs def2-TZVP sur référence
- Comparer λ_max (MAE par rapport à expérience)

**Livrables :** 3 fichiers `.xyz` validés, rapport test def2-SVP vs def2-TZVP

---

### Semaine 4 : S0 Optimisations (Local 16 Go)

**Configuration pour tous les calculs :**
```
%maxcore 3500
%pal nprocs 4 end
```

**Lundi-Mercredi : S0 gas phase**
```bash
nohup orca S0_gas_opt.inp > S0_gas_opt.out &
# Référence, Iodo, TPP-Iodo (séquentiel)
# 30-60 min par molécule
```

**Jeudi-Vendredi : S0 eau (SMD mixed) + validation**
```bash
nohup orca S0_water_opt.inp > S0_water_opt.out &
# 45-90 min par molécule

Validation géométries (fréquences imaginaires : 1h)
```

**Livrables :** 3 fichiers S0_water_opt.gbw (CRITICAL)

---

### Semaine 5-6 : Excitations Verticales (TD-DFT)

**Semaine 5 : Calculs TD-DFT (ωB97X-D3)**
```bash
# Séquentiel local (1 calcul à la fois)
nohup orca TDDFT_vertical.inp > TDDFT_vertical.out &
# 15-30 min par molécule
```

**Semaine 6 : Extraction et Benchmarking**
```
Lundi-Mardi:   Extraction λ_max des 3 molécules
               Compilation des spectres

Mercredi-Jeudi: Benchmarking vs littérature
               Validation des méthodes (MAE < 0.1 eV)
               Comparaison def2-SVP vs def2-TZVP

Vendredi:      Graphiques comparatifs
               Tableau des propriétés d'absorption
```

**Livrables :**
- Tableau λ_max pour les 3 molécules
- Graphiques spectres d'absorption
- Rapport benchmarking (MAE, R²)
- Décision sur base à utiliser

---

### Semaine 7-8 : États Excités Relaxés (ΔE_{ST}, PTT)

#### Semaine 7 : T1 Optimisations (robustes, 60-120 min/molécule)

```bash
# Séquentiel local
nohup orca T1_opt_UKS.inp > T1_opt_UKS.out &
# Référence, Iodo, TPP-Iodo

Extraction E_T1
Premiers calculs ΔE_{ST}
```

#### Semaine 8 : S1 Optimisations (critiques, 120-180 min/molécule)

```bash
# Pré-test des guesses (gen_s1_guesses.sh)
./gen_s1_guesses.sh -t S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 4

# Lancer S1 avec meilleur guess
nohup orca S1_opt_DeltaUKS.inp > S1_opt_DeltaUKS.out &

# Si échec : run_troubleshoot_S1.sh (escalade auto)
./run_troubleshoot_S1.sh -i S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 4
```

**Buffer recommandé : +200-300% (3-5 tentatives par molécule)**

**Livrables :**
- 3 fichiers S1_water_opt.gbw (Important)
- Tableau ΔE_ST = E_S1 - E_T1
- Protocole de convergence S₁ documenté

---

### Semaine 9 : Couplage Spin-Orbite (ΔDFT+SOC)

**Stratégie recommandée : ΔDFT+SOC (ZORA, dosoc)**

```bash
# Séquentiel local (30-60 min/molécule)
nohup orca DeltaSCF_SOC.inp > DeltaSCF_SOC.out &

# Extraction des constantes SOC
# Analyse comparative (S1↔Tn couplages)
```

**Validation ponctuelle NEVPT2 (si ressources disponibles)**
```bash
# Optionnel : sur meilleur candidat uniquement
# 150-300 min (2.5-5 heures)
```

**Livrables :**
- 3 fichiers SOC_DeltaDFT.out
- Tableau des constantes SOC
- Analyse comparative

---

### Semaine 9-10 : Analyse Post-Traitement

**Jours 1-3 : Analyse de charge et MEP**

```bash
# Multiwfn pour charges Hirshfeld
multiwfn S0_water_opt.out

# Générer cartes MEP
# Valider localisation charge TPP+ (sur TPP-Iodo-BODIPY)
# Vérifier accessibilité (distance > 5 Å, angle > 90°)
```

**Jours 4-5 : Analyse des propriétés photophysiques**

```
- Rendements quantiques (Φ_f, Φ_p, Φ_Δ)
- Temps de vie des états excités
- Taux de processus (k_f, k_{ISC}, k_{nr})
- Indicateurs PSI et TCI
```

**Livrables :**
- Tableau comparatif complet
- Cartes MEP des 3 molécules
- Graphiques comparatifs

---

### Semaine 10 : Scoring et Décision (Grille Go/No-Go)

**Application de la grille Go/No-Go quantitative**

```
Prototype Iodo-BODIPY :
- λ_max [680-720nm] (25%)
- E_ad < 1.0 eV (15%)
- ΔE_ST < 0.05 eV (25%)
- SOC > 50 cm⁻¹ (25%)
- PSI > 1 (10%)

Prototype TPP-Iodo-BODIPY :
- λ_max [690-730nm] (20%)
- E_ad < 1.2 eV (15%)
- ΔE_ST < 0.08 eV (20%)
- SOC > 40 cm⁻¹ (15%)
- Ciblage mitochondrial (30%)
  - Charge TPP⁺: +1,00 e
  - Distance > 5 Å
  - Angle > 90°
  - ΔΨ > 150 mV
  - P_app > 10⁻⁶ cm/s
  - Ratio ≥ 10
  - Énergie ≥ -20 kcal/mol
```

**Livrables :**
- Feuille de scoring (candidats rankés)
- Analyse écrite du candidat optimal
- Recommendations

---

### Semaine 11 : Synthèse Résultats et Perspectives

**Jours 1-3 : Finaliser les analyses**
- Double-check tous les résultats
- Générer graphiques finaux haute qualité
- Analyse validation méthodologique

**Jours 4-5 : Brainstorm perspectives**
- Stratégies futures (PDT Type I, pH-sensitivity)
- Nanomédecine : intégration nanoparticule
- Applications cliniques
- Toxicité prédictive

**Livrables :**
- Suite complète de graphiques publiables
- Document "Perspectives Future" (2-3 pages)

---

### Semaine 12 : Rédaction du Rapport (Draft)

**Plan du Rapport (30-50 pages)**

```
1. Introduction (3-4 pages)
2. État de l'Art (5-7 pages)
3. Théorie et Méthodes (8-10 pages)
4. Résultats (10-12 pages)
5. Discussion (5-8 pages)
6. Perspectives et Conclusion (3-4 pages)
7. Annexes
```

**Schedule de rédaction**

```
Lundi-Mardi:    Intro + État de l'art
Mercredi-Jeudi: Théorie + Méthodes
Vendredi:       Résultats (début)
```

---

### Semaine 13 : Finalisation Rapport + Préparation Soutenance

**Rédaction Finale**
```
Lundi-Mardi:   Résultats (suite + fin) + Discussion
Mercredi-Jeudi: Perspectives + Conclusion + Relecture
Vendredi:      Relecture finale + references
```

**Préparation Soutenance**
```
Lundi-Mercredi: Créer diapositives (15-20 slides)
Jeudi-Vendredi: Préparer discours + Répétition
```

**Livrables :** Rapport final + Slides

---

### Semaine 14 : Soutenance et Finalisation

**Lundi-Mercredi : Préparation Finale**
- Corrections finales du rapport
- Dernière répétition

**Jeudi : SOUTENANCE**
- Présentation orale (15 min)
- Défense questions (5-10 min)

**Vendredi : Clôture**
- Archivage final des calculs
- Dépôt du rapport définitif

---

## Partie 3 : Optimisation des Ressources (Local 16 Go)

### 3.1 Configuration Optimale

```bash
# Dans tous les fichiers .inp
%maxcore 3500
%pal nprocs 4 end
```

### 3.2 Exécution Séquentielle

```bash
# Lancer avec nohup pour sessions longues
nohup orca S0_gas_opt.inp > S0_gas_opt.out &

# Surveiller
tail -f S0_gas_opt.out

# Vérifier convergence
grep "FINAL SINGLE POINT ENERGY" S0_gas_opt.out
```

### 3.3 Checkpointing et Reprise

```bash
# Script de relance automatique pour S1
for i in {1..5}; do
  echo "Tentative $i de S1 optim..."
  DAMP=$((40 + i*10))
  sed -i "s/DampPercentage.*/DampPercentage $DAMP/" S1.inp
  orca S1.inp > S1_attempt_$i.out 2>&1
  if grep -q "FINAL SINGLE POINT ENERGY" S1_attempt_$i.out; then
    echo "✓ Success on attempt $i"
    break
  fi
done
```

### 3.4 Sauvegarde Incrémentale

```bash
# Backup tous les 2 jours
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/projet_${TIMESTAMP}"
mkdir -p $BACKUP_DIR
cp */*.gbw $BACKUP_DIR/
cp */*.out $BACKUP_DIR/
cp */*.xyz $BACKUP_DIR/
tar -czf "${BACKUP_DIR}.tar.gz" $BACKUP_DIR/
```

---

## Partie 4 : Métriques de Suivi

### Tableau d'avancement

```
Étape                        | Status  | Date Start | Date End | Temps   | Issues
===================================================================================
S0 gas (3 mol)              | ✓ DONE  |            |          | 3h      |
S0 water (3 mol)            | ✓ DONE  |            |          | 5h      |
TD-DFT vertical (3 mol)     | ⏳ RUN  |            |          | 1.5h    |
T1 opt (3 mol)              | ⏱ WAIT  |            |          | 6h      |
S1 opt (3 mol)              | ⏱ WAIT  |            |          | 18h     | Buffer +200-300%
ΔDFT+SOC (3 mol)            | ⏱ WAIT  |            |          | 3h      |
MEP/ciblage (2 mol)         | ⏱ WAIT  |            |          | 1h      |
Analyse                      | 🔄 IP   |            |          |         |
Grille Go/No-Go              | 🔄 IP   |            |          |         |
Rapport (draft)              | 🔄 IP   |            |          |         |
Soutenance                   | ⏱ WAIT  |            |          |         |
```

---

## Partie 5 : Gestion des Crises (Local 16 Go)

### Si S1 ne converge pas après 3-5 tentatives

**Plan B :**
1. Vérifier S0_water_opt.gbw (corrompu ?)
2. Utiliser gen_s1_guesses.sh (3 guesses)
3. Utiliser run_troubleshoot_S1.sh (escalade auto)
4. Si échec : TD-DFT (ωB97X-D3) pour diagnostics

**Impact :** Perdre E_adiabatic, mais conserver λ_max, ΔE_ST, SOC

---

## Partie 6 : Ressources à Archiver

```
/archive/projet_BODIPY_260304/
├── COMPUTE/
│   ├── reference/
│   ├── iodo/
│   └── tpp-iodo/
├── RESULTS/
│   ├── comparison_table.csv
│   ├── scoring_matrix.xlsx
│   └── figures/
├── DOCUMENTATION/
│   ├── input_templates/
│   └── output_logs/
└── FINAL/
    ├── Rapport_stage_final.pdf
    └── Presentation_soutenance.pdf
```

---

**Document de planification — Version 260304 (04 mars 2026)**

**Configuration : Local 16 Go RAM / 4 cœurs / TD-DFT ωB97X-D3**
