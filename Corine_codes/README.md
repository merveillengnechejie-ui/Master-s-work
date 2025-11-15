# Corine_codes : Scripts et Inputs ORCA pour le Projet BODIPY

## 📋 Vue d'ensemble

Ce dossier contient tous les **scripts SLURM**, **inputs ORCA 6.1**, et **fichiers de géométrie** nécessaires pour le projet de Master 2 sur l'optimisation computationnelle de nanoparticules BODIPY pour une thérapie combinée PDT/PTT.

**Portée révisée (15/11/2025)** :
- **1 molécule de référence expérimentale** (externe, publiée) pour benchmarking
- **2 prototypes internes** : Iodo-BODIPY (PDT) + TPP–Iodo–BODIPY (théranostique)
- **Méthodologie** : ΔDFT+SOC (remplace NEVPT2)
- **Durée** : 14 semaines

---

## 📁 Structure des fichiers

### 1. Inputs ORCA 6.1 (Phase par phase)

#### Phase 1 : Optimisation S₀ (État fondamental)

| Fichier | Objectif | Temps estimé | Notes |
| :--- | :--- | :--- | :--- |
| `S0_gas_opt.inp` | Optimisation S₀ en phase gaz | 30–60 min | Étape de reconnaissance rapide |
| `S0_water_opt.inp` | Optimisation S₀ en solution (CPCM eau) | 45–90 min | Point de départ pour tous les calculs |

**Utilisation** :
```bash
# Lancer S0 gaz
orca S0_gas_opt.inp > S0_gas_opt.out &

# Lancer S0 eau (après S0 gaz)
orca S0_water_opt.inp > S0_water_opt.out &
```

#### Phase 2 : Excitations verticales (ADC(2))

| Fichier | Objectif | Temps estimé | Notes |
| :--- | :--- | :--- | :--- |
| `ADC2_vertical.inp` | Calcul λ_max (absorption verticale) | 240–360 min (4–6 h) | **Standardisé def2-TZVP** pour précision |

**Utilisation** :
```bash
# Lancer ADC(2) en batch de nuit (recommandé)
sbatch submit_ADC2.slurm
```

**⚠️ Important** : En semaine 3, tester **def2-SVP vs def2-TZVP** sur la molécule de référence pour décider de la base à utiliser pour tous les calculs. Cela peut économiser **9h mur** sur le projet.

#### Phase 3 : États excités relaxés (T₁ et S₁)

| Fichier | Objectif | Temps estimé | Notes |
| :--- | :--- | :--- | :--- |
| `T1_opt_UKS.inp` | Optimisation T₁ (état triplet) | 60–120 min | Robuste, généralement bon |
| `S1_opt_DeltaUKS.inp` | Optimisation S₁ (état singulet excité) | 120–180 min | **Étape critique** : prévoir 3–5 tentatives |

**Utilisation** :
```bash
# Lancer T1 (robuste)
sbatch submit_T1.slurm

# Lancer S1 (avec pré-test des guesses)
./gen_s1_guesses.sh -t S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 8
sbatch submit_S1.slurm
```

#### Phase 4 : Couplage spin-orbite (SOC)

| Fichier | Objectif | Temps estimé | Notes |
| :--- | :--- | :--- | :--- |
| `DeltaSCF_SOC.inp` | **ΔDFT+SOC** (recommandé) | 30–60 min | Cohérent avec ΔDFT, 10× plus rapide que NEVPT2 |
| `TDDFT_SOC_quick.inp` | TD-DFT SOC (Plan B) | 30–60 min | À utiliser si ΔSCF S₁ échoue |

**Utilisation** :
```bash
# Lancer ΔDFT+SOC (standard)
sbatch submit_SOC.slurm

# Ou TD-DFT SOC (Plan B)
orca TDDFT_SOC_quick.inp > TDDFT_SOC_quick.out &
```

---

### 2. Scripts SLURM (Soumission de jobs)

| Fichier | Utilité | Temps de file | Notes |
| :--- | :--- | :--- | :--- |
| `submit_S0.slurm` | Soumettre S₀ gaz | < 1h | Rapide |
| `submit_S0_water.slurm` | Soumettre S₀ eau | < 2h | Rapide |
| `submit_ADC2.slurm` | Soumettre ADC(2) | 4–6h | **Batch de nuit recommandé** |
| `submit_T1.slurm` | Soumettre T₁ | 1–2h | Robuste |
| `submit_S1.slurm` | Soumettre S₁ | 2–3h | **Peut nécessiter plusieurs tentatives** |
| `submit_SOC.slurm` | Soumettre SOC | 1h | Rapide |

**Utilisation générale** :
```bash
# Soumettre un job
sbatch submit_S0.slurm

# Vérifier l'état des jobs
squeue -u $USER

# Annuler un job
scancel <job_id>
```

---

### 3. Scripts Bash (Automatisation)

| Fichier | Utilité | Statut |
| :--- | :--- | :--- |
| `copy_and_prepare.sh` | Copier et préparer fichiers | À vérifier |
| `prepare_and_submit.sh` | Préparer et soumettre jobs | À vérifier |
| `gen_s1_guesses.sh` | Générer 3 guesses pour S₁ | ✅ Recommandé |
| `run_troubleshoot_S1.sh` | Escalade auto pour S₁ | ✅ Recommandé |

**Utilisation** :
```bash
# Pré-test des guesses S₁ (semaine 7)
./gen_s1_guesses.sh -t S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 8

# Escalade auto si S₁ ne converge pas
./run_troubleshoot_S1.sh -i S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 8
```

---

### 4. Fichiers de Géométrie (Molécules)

| Fichier | Molécule | Statut | Action |
| :--- | :--- | :--- | :--- |
| `Iodo_Opt.xyz` | Iodo-BODIPY (Prototype 1) | ✅ | À utiliser |
| `TPP_Opt.xyz` | TPP-BODIPY | ⚠️ | À remplacer par TPP-Iodo-BODIPY |
| `Bodipy_Opt.xyz` | BODIPY de base | ❌ | À supprimer (hors portée) |

**Note** : La molécule de référence expérimentale doit être construite en semaine 2 (voir section 8.1 du document principal).

---

## 🚀 Workflow Recommandé

### Semaine 1 : Validation de la chaîne

```bash
# 1. Tester S0 gaz sur benzène (molécule test)
orca S0_gas_opt.inp > S0_gas_opt.out

# 2. Vérifier convergence
grep "FINAL SINGLE POINT ENERGY" S0_gas_opt.out
```

### Semaine 3 : Test comparatif def2-SVP vs def2-TZVP

```bash
# 1. Créer deux versions d'ADC2_vertical.inp
cp ADC2_vertical.inp ADC2_vertical_SVP.inp
cp ADC2_vertical.inp ADC2_vertical_TZVP.inp

# 2. Modifier les bases dans les fichiers
# ADC2_vertical_SVP.inp : ! RI-ADC(2) def2-SVP AutoAux FrozenCore
# ADC2_vertical_TZVP.inp : ! RI-ADC(2) def2-TZVP AutoAux FrozenCore

# 3. Lancer en parallèle (batch de nuit)
sbatch submit_ADC2.slurm  # SVP
sbatch submit_ADC2.slurm  # TZVP

# 4. Comparer λ_max calculé vs expérimental
# Décision : Si écart < 5 nm → garder def2-SVP; si > 10 nm → garder def2-TZVP
```

### Semaines 4–6 : Calculs S₀ et ADC(2)

```bash
# 1. Lancer S0 pour les 3 molécules (référence + 2 prototypes)
sbatch submit_S0.slurm
sbatch submit_S0_water.slurm

# 2. Lancer ADC(2) en batch de nuit
sbatch submit_ADC2.slurm

# 3. Extraire λ_max
grep "Excitation energy" ADC2_vertical.out | head -1
```

### Semaines 7–9 : Calculs T₁, S₁, SOC

```bash
# 1. Lancer T₁ (robuste)
sbatch submit_T1.slurm

# 2. Pré-test des guesses S₁ (semaine 7)
./gen_s1_guesses.sh -t S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 8

# 3. Lancer S₁ (semaine 8–9)
sbatch submit_S1.slurm

# 4. Si S₁ ne converge pas après 5 tentatives
./run_troubleshoot_S1.sh -i S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 8

# 5. Lancer SOC (après S₁ convergé)
sbatch submit_SOC.slurm
```

---

## ⚠️ Troubleshooting

### Problème : ADC(2) manque de RAM

**Symptôme** : Erreur "out of memory"

**Solutions** :
1. Réduire à def2-SVP (moins de fonctions de base)
2. Lancer sur nœud avec plus de RAM (> 64 Go)
3. Réduire nprocs (8 → 4)

### Problème : S₁ ne converge pas

**Symptôme** : Énergie oscille ou augmente

**Solutions** (voir section 5 du document principal) :
1. Augmenter amortissement SCF (`DampPercentage 60`)
2. Utiliser `DIIS_TRAH` avec `TRAH_MaxDim 20`
3. Réduire pas géométrique (`MaxStep 0.1`)
4. Générer 3 guesses différents (HOMO→LUMO, HOMO−1→LUMO, HOMO→LUMO+1)
5. Utiliser `./run_troubleshoot_S1.sh` pour escalade auto

**Plan B** : Si après 5 tentatives S₁ échoue, utiliser `TDDFT_SOC_quick.inp` pour excitations verticales diagnostiques.

### Problème : File d'attente HPC saturée

**Symptôme** : Attente > 24h

**Solutions** :
1. Lancer batch de nuit (moins de charge)
2. Réduire nprocs (8 → 4) pour accès plus rapide
3. Utiliser nœuds dédiés si disponibles

---

## 📊 Archivage et Nommage des Fichiers

### Convention de nommage recommandée

```
<phase>_<molécule>_<tentative>_<base>.<ext>

Exemples :
- S1_protoA_attempt1_SVP.gbw
- S1_protoA_attempt2_TZVP.gbw
- ADC2_ref_def2TZVP.out
- SOC_protoB_DELTADFT.out
```

### Archivage systématique

```bash
# Créer dossier archive
mkdir -p results/archive_v1

# Archiver tous les .gbw et .out
cp *.gbw results/archive_v1/
cp *.out results/archive_v1/

# Garder les fichiers de géométrie optimisée
cp *.xyz results/
```

---

## 📚 Références

- **Document principal** : `demarche_methodologique_stage_v2_integree.md`
- **Analyse critique** : `Analyse251115.md`
- **Guide pratique** : `Guide_Pratique_ORCA_Scripts_Troubleshooting.md`
- **ORCA 6.1 Manual** : https://www.orcasoftware.de/

---

**Dernière mise à jour** : 15 novembre 2025
**Version** : 2.0 (révisée)
**Statut** : À jour
