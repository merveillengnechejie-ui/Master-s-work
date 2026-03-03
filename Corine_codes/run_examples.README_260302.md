# Run Examples and Quick Notes

## 📋 Vue d'ensemble

Ce fichier contient des **exemples d'utilisation** et des **notes pratiques** pour exécuter les calculs ORCA du projet révisé (15/11/2025).

**Portée révisée** :
- 1 molécule de référence expérimentale (externe, publiée)
- 2 prototypes internes : Iodo-BODIPY + TPP–Iodo–BODIPY
- Méthodologie : ΔDFT+SOC (remplace NEVPT2)

---

## 🚀 Workflow Recommandé

### Étape 1 : Préparation des fichiers

```bash
# 1. Créer un dossier pour chaque molécule
mkdir -p molecules/reference
mkdir -p molecules/iodo_bodipy
mkdir -p molecules/tpp_iodo_bodipy

# 2. Copier les fichiers de géométrie
cp Iodo_Opt.xyz molecules/iodo_bodipy/
cp TPP_Iodo_BODIPY.xyz molecules/tpp_iodo_bodipy/
# (La référence doit être construite en semaine 2)

# 3. Copier les templates d'inputs
cp Corine_codes/*.inp molecules/reference/
cp Corine_codes/*.inp molecules/iodo_bodipy/
cp Corine_codes/*.inp molecules/tpp_iodo_bodipy/
```

### Étape 2 : Optimisation S₀ (Phase 1)

```bash
# 1. Remplacer [COORDINATES] par la géométrie
# Option A : Éditer le fichier .inp directement
sed -i 's/\[COORDINATES\]/[contenu du fichier .xyz]/g' S0_gas_opt.inp

# Option B : Utiliser le fichier .xyz directement
# Modifier la dernière ligne du .inp :
# * xyz 0 1
# [COORDINATES]
# *
# En :
# * xyzfile 0 1 S0_gas_opt.xyz

# 2. Lancer S0 gaz
orca S0_gas_opt.inp > S0_gas_opt.out &

# 3. Après convergence, lancer S0 eau
orca S0_water_opt.inp > S0_water_opt.out &

# 4. Vérifier la convergence
grep "FINAL SINGLE POINT ENERGY" S0_gas_opt.out
grep "FINAL SINGLE POINT ENERGY" S0_water_opt.out
```

### Étape 3 : Excitations verticales (Phase 2 - TD-DFT)

```bash
# ⚠️ REMPLACE ADC(2) POUR EXÉCUTION LOCALE RAPIDE

# 1. Lancer TD-DFT
orca TDDFT_vertical.inp > TDDFT_vertical.out &

# 2. Extraire λ_max
grep "Excitation energy" TDDFT_vertical.out | head -1
```

### Étape 4 : États excités relaxés (Phase 3)

```bash
# 1. Optimisation T₁ (robuste)
orca T1_opt_UKS.inp > T1_opt_UKS.out &

# 2. Pré-test des guesses S₁ (Semaine 7)
./gen_s1_guesses.sh -t S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 4

# 3. Lancer S₁ (Semaine 8–9)
orca S1_opt_DeltaUKS.inp > S1_opt_DeltaUKS.out &

# 4. Si S₁ ne converge pas après 5 tentatives
./run_troubleshoot_S1.sh -i S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 8

# 5. Vérifier convergence
grep "FINAL SINGLE POINT ENERGY" S1_opt_DeltaUKS.out
```

### Étape 5 : Couplage spin-orbite (Phase 4)

```bash
# 1. Lancer ΔDFT+SOC (recommandé)
orca DeltaSCF_SOC.inp > DeltaSCF_SOC.out &

# 2. Ou TD-DFT SOC (Plan B si ΔSCF S₁ échoue)
orca TDDFT_SOC_quick.inp > TDDFT_SOC_quick.out &

# 3. Extraire les résultats
grep "Spin-Orbit Coupling" DeltaSCF_SOC.out
```

---

## 📝 Paramètres à Adapter

### Avant de lancer les calculs

| Paramètre | Défaut | Production | Notes |
| :--- | :--- | :--- | :--- |
| **nprocs** | 4 | 4 | Limite matérielle |
| **maxcore** | 3500 | 3500 | Pour 16 Go RAM (14 Go total + OS) |
| **Basis set** | def2-SVP | def2-SVP | Recommandé pour rapidité |
| **MaxIter (SCF)** | 500 | 500–1000 | Augmenter si convergence difficile |
| **ConvForce (géom)** | 1e-6 | 1e-6 | Critère de convergence |
| **DampPercentage** | 40 | 60–80 | Augmenter pour S₁ difficile |
| **LevelShift** | 0.2 | 0.5–1.0 | Augmenter pour S₁ difficile |

### Exemple : Adapter pour S₁ difficile

```orca
%scf
  HFTyp UKS
  SCF_ALGORITHM DIIS_TRAH
  MaxIter 1000              # Augmenter
  ConvForce 1e-6
  LevelShift 0.5            # Augmenter
  DampPercentage 60         # Augmenter
end

%geom
  MaxStep 0.1               # Réduire
  Trust 0.15
end
```

---

## 🔧 Troubleshooting Rapide

### Problème : ADC(2) manque de RAM

**Symptôme** : Erreur "out of memory"

**Solutions** :
```bash
# 1. Réduire à def2-SVP
# Modifier ADC2_vertical.inp : ! RI-ADC(2) def2-SVP AutoAux FrozenCore

# 2. Lancer sur nœud avec plus de RAM
sbatch --mem=64G submit_ADC2.slurm

# 3. Réduire nprocs
# Modifier submit_ADC2.slurm : #SBATCH --cpus-per-task=4
```

### Problème : S₁ ne converge pas

**Symptôme** : Énergie oscille ou augmente

**Solutions** :
```bash
# 1. Utiliser le script d'escalade auto
./run_troubleshoot_S1.sh -i S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 8

# 2. Ou escalade manuelle (voir section 5 du document principal)
# - Augmenter DampPercentage (40 → 60 → 80)
# - Augmenter LevelShift (0.2 → 0.5 → 1.0)
# - Réduire MaxStep (0.2 → 0.1 → 0.05)

# 3. Générer 3 guesses différents
./gen_s1_guesses.sh -t S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 8

# 4. Plan B : Utiliser TD-DFT
orca TDDFT_SOC_quick.inp > TDDFT_SOC_quick.out &
```

### Problème : File d'attente HPC saturée

**Symptôme** : Attente > 24h

**Solutions** :
```bash
# 1. Lancer batch de nuit
sbatch --begin=22:00 submit_ADC2.slurm

# 2. Réduire nprocs pour accès plus rapide
# Modifier submit_ADC2.slurm : #SBATCH --cpus-per-task=4

# 3. Utiliser nœuds dédiés si disponibles
sbatch --partition=gpu submit_ADC2.slurm
```

---

## 📊 Convention de Nommage

### Recommandée pour l'archivage

```
<phase>_<molécule>_<tentative>_<base>.<ext>

Exemples :
- S1_protoA_attempt1_SVP.gbw
- S1_protoA_attempt2_TZVP.gbw
- ADC2_ref_def2TZVP.out
- SOC_protoB_DELTADFT.out
- T1_protoC_attempt1_SVP.gbw
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

### Documents clés

- **Document principal** : `demarche_methodologique_stage_v2_integree.md`
- **Guide scripts** : `Corine_codes/README.md`
- **Description molécules** : `Corine_codes/PROTOTYPES.md`
- **Dépannage** : `Guide_Pratique_ORCA_Scripts_Troubleshooting.md`

### Inputs ORCA

| Phase | Fichier | Utilité |
| :--- | :--- | :--- |
| 1a | `S0_gas_opt.inp` | Optimisation S₀ gaz |
| 1b | `S0_water_opt.inp` | Optimisation S₀ eau |
| 2 | `ADC2_vertical.inp` | Excitations verticales |
| 3a | `T1_opt_UKS.inp` | Optimisation T₁ |
| 3b | `S1_opt_DeltaUKS.inp` | Optimisation S₁ |
| 4 | `DeltaSCF_SOC.inp` | ΔDFT+SOC (recommandé) |
| 4 | `TDDFT_SOC_quick.inp` | TD-DFT SOC (Plan B) |

### Scripts SLURM

| Fichier | Utilité |
| :--- | :--- |
| `submit_S0.slurm` | Soumettre S₀ gaz |
| `submit_S0_water.slurm` | Soumettre S₀ eau |
| `submit_ADC2.slurm` | Soumettre ADC(2) |
| `submit_T1.slurm` | Soumettre T₁ |
| `submit_S1.slurm` | Soumettre S₁ |
| `submit_SOC.slurm` | Soumettre SOC |

### Scripts Bash

| Fichier | Utilité |
| :--- | :--- |
| `gen_s1_guesses.sh` | Générer 3 guesses S₁ |
| `run_troubleshoot_S1.sh` | Escalade auto S₁ |
| `copy_and_prepare.sh` | Copier et préparer |
| `prepare_and_submit.sh` | Préparer et soumettre |

---

## ✅ Checklist Avant de Lancer

- [ ] Vérifier que les fichiers `.xyz` sont présents
- [ ] Vérifier que les fichiers `.inp` ont les bonnes coordonnées
- [ ] Vérifier que `nprocs` correspond aux ressources disponibles
- [ ] Vérifier que la base est correcte (def2-SVP ou def2-TZVP)
- [ ] Vérifier que les scripts SLURM ont les bons chemins
- [ ] Vérifier que l'espace disque est suffisant (≥ 100 Go)
- [ ] Vérifier que la RAM est suffisante (≥ 32–64 Go pour ADC(2))

---

## 🎯 Workflow Complet (Semaines 4–9)

```bash
# Semaine 4 : S₀ pour les 3 molécules
sbatch submit_S0.slurm
sbatch submit_S0_water.slurm

# Semaine 5–6 : ADC(2) avec test comparatif
# (Semaine 3 : test comparatif def2-SVP vs def2-TZVP)
sbatch submit_ADC2.slurm

# Semaine 7 : T₁ + pré-test S₁
sbatch submit_T1.slurm
./gen_s1_guesses.sh -t S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 8

# Semaine 8–9 : S₁ + escalade si nécessaire
sbatch submit_S1.slurm
# Si échec : ./run_troubleshoot_S1.sh ...

# Semaine 9–10 : SOC
sbatch submit_SOC.slurm
```

---

**Dernière mise à jour** : 15 novembre 2025
**Version** : 2.0 (révisée)
**Statut** : À jour
