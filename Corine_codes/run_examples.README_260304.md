# Run Examples and Quick Notes (Version 260304)

> **Mise à jour : 04 mars 2026 (260304)**
> - Exécution locale 16 Go RAM / TD-DFT ωB97X-D3
> - Configuration : 4 cœurs, %maxcore 3500
> - Séquentiel local (nohup) au lieu de SLURM

---

## 📋 Vue d'ensemble

Ce fichier contient des **exemples d'utilisation** et des **notes pratiques** pour exécuter les calculs ORCA du projet.

**Portée révisée** :
- 1 molécule de référence expérimentale (benchmarking uniquement)
- 2 prototypes internes : Iodo-BODIPY + TPP-Iodo-BODIPY
- Configuration : Local 16 Go RAM, 4 cœurs

---

## 🚀 Workflow Recommandé (Local 16 Go)

### Étape 1 : Préparation des fichiers

```bash
# 1. Créer un dossier pour chaque molécule
mkdir -p molecules/reference
mkdir -p molecules/iodo_bodipy
mkdir -p molecules/tpp_iodo_bodipy

# 2. Copier les fichiers de géométrie depuis Corine_codes/
cp ../Corine_codes/Iodo_Opt.xyz molecules/iodo_bodipy/
cp ../Corine_codes/TPP_Iodo_BODIPY.xyz molecules/tpp_iodo_bodipy/
# (La référence doit être construite en semaine 2)

# 3. Copier les templates d'inputs depuis md files/
cp ../md\ files/Guide_Pratique_ORCA_Scripts_Troubleshooting_260304.md/*.inp molecules/iodo_bodipy/
```

### Étape 2 : Optimisation S₀ (Phase 1)

```bash
cd molecules/iodo_bodipy

# 1. Lancer S0 gaz (30-60 min)
nohup orca S0_gas_opt.inp > S0_gas_opt.out &

# 2. Après convergence, lancer S0 eau (SMD mixed) (45-90 min)
nohup orca S0_water_opt.inp > S0_water_opt.out &

# 3. Vérifier la convergence
grep "FINAL SINGLE POINT ENERGY" S0_gas_opt.out
grep "FINAL SINGLE POINT ENERGY" S0_water_opt.out

# 4. Sauvegarder les fichiers critiques
cp S0_water_opt.gbw S0_water_opt.gbw.backup
cp S0_water_opt.xyz S0_water_opt.xyz.backup
```

### Étape 3 : Excitations verticales (Phase 2 - TD-DFT)

```bash
# TD-DFT ωB97X-D3 (15-30 min)
nohup orca TDDFT_vertical.inp > TDDFT_vertical.out &

# Extraire λ_max
grep "Excitation energy" TDDFT_vertical.out | head -1

# Ou utiliser le script Python
python3 analyze_results.py TDDFT_vertical.out
```

### Étape 4 : États excités relaxés (Phase 3)

```bash
# 1. Optimisation T₁ (robuste, 60-120 min)
nohup orca T1_opt_UKS.inp > T1_opt_UKS.out &

# 2. Pré-test des guesses S₁ (Semaine 7)
../Corine_codes/gen_s1_guesses.sh -t S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 4

# 3. Lancer S₁ avec meilleur guess (Semaine 8-9, 120-180 min)
nohup orca S1_opt_DeltaUKS.inp > S1_opt_DeltaUKS.out &

# 4. Si S₁ ne converge pas après 5 tentatives
../Corine_codes/run_troubleshoot_S1.sh -i S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 4

# 5. Vérifier convergence
grep "FINAL SINGLE POINT ENERGY" S1_opt_DeltaUKS.out
```

### Étape 5 : Couplage spin-orbite (Phase 4)

```bash
# 1. Lancer ΔDFT+SOC (recommandé, 30-60 min)
nohup orca DeltaSCF_SOC.inp > DeltaSCF_SOC.out &

# 2. Ou TD-DFT SOC (Plan B si ΔSCF S₁ échoue, 15-30 min)
nohup orca TDDFT_SOC_quick.inp > TDDFT_SOC_quick.out &

# 3. Extraire les résultats
grep "Spin-Orbit Coupling" DeltaSCF_SOC.out
```

---

## 📝 Paramètres à Adapter

### Configuration standard (16 Go RAM, 4 cœurs)

| Paramètre | Valeur | Notes |
| :--- | :--- | :--- |
| **%maxcore** | 3500 | Pour 16 Go RAM (14 Go pour ORCA + OS) |
| **%pal nprocs** | 4 | Nombre de cœurs |
| **Basis set** | def2-SVP | Recommandé pour rapidité |
| **MaxIter (SCF)** | 500 | Augmenter à 1000 si difficile |
| **DampPercentage** | 40 | Augmenter à 60-80 pour S₁ |
| **LevelShift** | 0.2 | Augmenter à 0.5-1.0 pour S₁ |

### Exemple : Adapter pour S₁ difficile

```orca
%maxcore 3500
%pal nprocs 4 end

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

### Problème : Out of Memory

**Symptôme** : Erreur "Insufficient memory"

**Solutions** :
```bash
# 1. Réduire %maxcore
# Modifier .inp : %maxcore 3000

# 2. 1 seul calcul à la fois
# Ne pas lancer plusieurs orca en parallèle

# 3. Fermer autres applications
```

### Problème : S₁ ne converge pas

**Symptôme** : Énergie oscille ou augmente

**Solutions** :
```bash
# 1. Utiliser gen_s1_guesses.sh (3 guesses)
../Corine_codes/gen_s1_guesses.sh -t S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 4

# 2. Utiliser run_troubleshoot_S1.sh (escalade auto)
../Corine_codes/run_troubleshoot_S1.sh -i S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 4

# 3. Escalade manuelle
# - DampPercentage : 40 → 60 → 80
# - LevelShift : 0.2 → 0.5 → 1.0
# - MaxStep : 0.2 → 0.1 → 0.05

# 4. Plan B : TD-DFT pour diagnostics
orca TDDFT_SOC_quick.inp > TDDFT_SOC_quick.out &
```

### Problème : λ_max très différent de l'attendu

**Solutions** :
```bash
# 1. Vérifier benchmarking (semaine 3)
# Comparer avec données expérimentales

# 2. Test def2-SVP vs def2-TZVP
# Lancer les deux bases sur référence
# Choisir celle avec MAE < 5 nm

# 3. Vérifier géométrie S0
# Relancer optimisation S0
```

---

## 📊 Convention de Nommage

### Recommandée pour l'archivage

```
<phase>_<molécule>_<tentative>_<base>.<ext>

Exemples :
- S1_iodo_attempt1_SVP.gbw
- S1_iodo_attempt2_TZVP.gbw
- TDDFT_ref_def2SVP.out
- SOC_tpp_iodo_DELTADFT.out
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

- **Document principal** : `md files/demarche_methodologique_stage_v3_260302.md`
- **Guide scripts** : `md files/Guide_Pratique_ORCA_Scripts_Troubleshooting_260304.md`
- **Description molécules** : `Corine_codes/PROTOTYPES_260302.md`
- **Résumé** : `md files/Resume_Executif_Aide_Memoire_260304.md`

### Inputs ORCA

| Phase | Fichier | Utilité | Temps |
| :--- | :--- | :--- | :--- |
| 1a | `S0_gas_opt.inp` | Optimisation S₀ gaz | 30-60 min |
| 1b | `S0_water_opt.inp` | Optimisation S₀ SMD | 45-90 min |
| 2 | `TDDFT_vertical.inp` | Excitations verticales | 15-30 min |
| 3a | `T1_opt_UKS.inp` | Optimisation T₁ | 60-120 min |
| 3b | `S1_opt_DeltaUKS.inp` | Optimisation S₁ | 120-180 min |
| 4 | `DeltaSCF_SOC.inp` | ΔDFT+SOC (standard) | 30-60 min |
| 4 | `TDDFT_SOC_quick.inp` | TD-DFT SOC (Plan B) | 15-30 min |

### Scripts Bash

| Fichier | Utilité |
| :--- | :--- |
| `gen_s1_guesses.sh` | Générer 3 guesses S₁ |
| `run_troubleshoot_S1.sh` | Escalade auto S₁ |
| `prepare_and_submit.sh` | Préparer et soumettre |

---

## ✅ Checklist Avant de Lancer

- [ ] Vérifier que les fichiers `.xyz` sont présents
- [ ] Vérifier que les fichiers `.inp` ont les bonnes coordonnées
- [ ] Vérifier configuration : %maxcore 3500, %pal nprocs 4
- [ ] Vérifier que la base est correcte (def2-SVP)
- [ ] Vérifier que l'espace disque est suffisant (≥ 50 Go)
- [ ] Vérifier que la RAM est suffisante (16 Go)
- [ ] Tester sur benzène avant BODIPY

---

## 🎯 Workflow Complet (Semaines 4-9)

```bash
# Semaine 4 : S₀ pour les 3 molécules
cd reference && nohup orca S0_gas_opt.inp > S0_gas_opt.out &
cd ../iodo && nohup orca S0_gas_opt.inp > S0_gas_opt.out &
cd ../tpp-iodo && nohup orca S0_gas_opt.inp > S0_gas_opt.out &

# Semaine 5-6 : TD-DFT vertical
nohup orca TDDFT_vertical.inp > TDDFT_vertical.out &

# Semaine 7 : T₁ + pré-test S₁
nohup orca T1_opt_UKS.inp > T1_opt_UKS.out &
../Corine_codes/gen_s1_guesses.sh -t S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 4

# Semaine 8-9 : S₁ + escalade si nécessaire
nohup orca S1_opt_DeltaUKS.inp > S1_opt_DeltaUKS.out &
# Si échec : ../Corine_codes/run_troubleshoot_S1.sh ...

# Semaine 9 : SOC
nohup orca DeltaSCF_SOC.inp > DeltaSCF_SOC.out &
```

---

## 📈 Extraction des Résultats

### Script Python : analyze_results.py

```bash
# Extraire énergies et propriétés
python3 analyze_results.py S0_water_opt.out
python3 analyze_results.py TDDFT_vertical.out
python3 analyze_results.py DeltaSCF_SOC.out
```

### Commandes grep utiles

```bash
# Énergie finale
grep "FINAL SINGLE POINT ENERGY" S0_water_opt.out

# λ_max (TD-DFT)
grep "Excitation energy" TDDFT_vertical.out | head -1

# SOC
grep "Spin-Orbit Coupling" DeltaSCF_SOC.out

# Convergence géométrie
grep "Geometry convergence" S0_water_opt.out

# Fréquences imaginaires
grep "imaginary frequencies" S0_water_opt.out
```

---

**Dernière mise à jour** : 04 mars 2026 (260304)

**Version** : 3.0 (Exécution locale 16 Go / TD-DFT ωB97X-D3)

**Configuration** : 4 cœurs, %maxcore 3500, SMD mixed
