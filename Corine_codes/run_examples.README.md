# Run Examples and Quick Notes

## 📋 Vue d'ensemble

Ce fichier contient des **exemples d'utilisation** et des **notes pratiques** pour exécuter les calculs ORCA du projet révisé (15/11/2025).

**Portée révisée** :
- 1 molécule de référence expérimentale (externe, publiée)
- 2 prototypes internes : Iodo-BODIPY + TPP–Iodo–BODIPY
- Méthodologie : ΔDFT+SOC (remplace NEVPT2)

**Méthodes recommandées** :
- **ΔDFT+SOC** pour le couplage spin-orbite (10× plus rapide que NEVPT2)
- **Protocole avancé de convergence S₁** avec buffer +200-300% (3-5 tentatives)
- **Test comparatif def2-SVP vs def2-TZVP** en semaine 3 pour optimiser le timing

---

## 🧪 Workflow Complet des Calculs

### Étape 1 : Optimisation géométrique de l'état fondamental (S₀)

```bash
# Optimisation en phase gazeuse (reconnaissance)
orca S0_gas_opt.inp > S0_gas_opt.out &

# Optimisation en phase aqueuse (géométrie de référence pour calculs)
orca S0_water_opt.inp > S0_water_opt.out &
```

### Étape 2 : Calculs d'excitation verticale (ADC(2))

```bash
# Calcul λ_max via ADC(2) - base def2-TZVP (standard)
orca ADC2_vertical.inp > ADC2_vertical.out

# ⚠️ Test critique semaine 3 : def2-SVP vs def2-TZVP sur la molécule de référence
# Si MAE < 5 nm : utiliser def2-SVP (gain ~3h/molécule)
# Si MAE > 10 nm : utiliser def2-TZVP (précision requise)
```

### Étape 3 : Optimisation des états excités (T₁ et S₁)

```bash
# Optimisation T₁ (triplet) - rapide, robuste
orca T1_opt_UKS.inp > T1_opt_UKS.out

# Optimisation S₁ (singulet) - délicate, nécessite protocole avancé
# Utiliser les scripts d'automatisation pour convergence :

# 1. Générer plusieurs guess électroniques
./gen_s1_guesses.sh -t S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 8

# 2. Lancer avec protocole d'escalade automatique
./run_troubleshoot_S1.sh -i S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 8
```

**Protocole avancé de convergence S₁ (ΔSCF)** :
- Analyse préalable de la nature de l'état excité (π→π*, n→π*, CT) via ADC(2) + NTOs
- Génération de 3 guesses électroniques (HOMO→LUMO, HOMO-1→LUMO, HOMO→LUMO+1) via IMOM
- Adaptation des algorithmes selon type d'excitation : π→π* (ΔUKS), n→π* (ΔROKS), CT (ωB97M-V + ptSS-PCM)
- Stratégies de convergence : LevelShift, DampPercentage, TRAH_MaxDim
- Buffer +200-300% (3-5 tentatives) pour convergence fiable

### Étape 4 : Couplage Spin-Orbite (SOC) - Méthode recommandée

```bash
# ΔDFT+SOC (recommandé) - cohérent avec workflow ΔDFT, 10× plus rapide que NEVPT2
orca DeltaSCF_SOC.inp > DeltaSCF_SOC.out

# Temps estimé : 30-60 min par molécule
# Constantes SOC typiques : 1-10 cm⁻¹ (sans atome lourd), 50-200 cm⁻¹ (avec I)
```

**Options alternatives** :
- TD-DFT SOC rapide : pour screening initial (TDDFT_SOC_quick.inp)
- Validation ponctuelle NEVPT2 : pour candidats retenus si ressources disponibles

---

## 📊 Grille Go/No-Go Quantitative

### Prototype 1 : Iodo-BODIPY (PDT optimisée)
| Critère | Cible | Poids | Score max |
| :--- | :--- | :--- | :--- |
| **λ_max (absorption)** | 680-720 nm (NIR-I) | 25% | 25/25 |
| **E_adiabatic (PTT)** | < 1.0 eV | 15% | 15/15 |
| **ΔE_ST (ISC/PDT)** | < 0.05 eV | 25% | 25/25 |
| **SOC (ISC speed)** | > 50 cm⁻¹ | 25% | 25/25 |
| **Photostabilité** | PSI > 1 | 10% | 10/10 |
| **TOTAL** | **Score ≥ 70% = Go** | **100%** | **100/100** |

### Prototype 2 : TPP-Iodo-BODIPY (théranostique ciblé)
| Critère | Cible | Poids | Score max |
| :--- | :--- | :--- | :--- |
| **λ_max (absorption)** | 690-730 nm (NIR-I, légère perturbation par TPP+) | 20% | 20/25 |
| **E_adiabatic (PTT)** | < 1.2 eV | 15% | 15/15 |
| **ΔE_ST (ISC/PDT)** | < 0.08 eV | 20% | 20/25 |
| **SOC (ISC speed)** | > 40 cm⁻¹ | 15% | 15/15 |
| **Ciblage mitochondrial** | Quantitatif (critères ci-dessous) | 30% | 30/30 |
| **TOTAL** | **Score ≥ 70% = Go** | **100%** | **100/100** |

#### Critères de ciblage mitochondrial quantitatifs (Prototype 2)
- Charge TPP⁺: +1,00 e (localisée sur TPP)
- Distance minimale TPP⁺ → centre BODIPY : > 5 Å
- Angle dièdre TPP⁺-BODIPY : > 90°
- Potentiel membranaire prédit : ΔΨ > 150 mV
- Coefficient de perméabilité apparente (P_app) > 10⁻⁶ cm/s
- Rapport d'accumulation : ≥ 10
- Énergie de liaison à la membrane ≥ -20 kcal/mol

---

## 🚀 Exemples de Workflows

### Workflow complet pour une molécule

```bash
# 1. Optimisation S₀ (gaz + eau)
sbatch submit_S0.slurm    # 30-60 min
sbatch submit_S0_water.slurm  # 45-90 min

# 2. Excitations verticales - tester def2-SVP vs def2-TZVP
sbatch submit_ADC2.slurm      # 240-360 min

# 3. États excités
sbatch submit_T1.slurm        # 60-120 min
# S₁ optimization avec protocole avancé (peut nécessiter plusieurs tentatives)
sbatch submit_S1.slurm        # 120-180 min × (3-5) tentatives

# 4. SOC via ΔDFT+SOC
sbatch submit_SOC.slurm       # 30-60 min
```

### Workflow de validation méthodologique

```bash
# 1. Calculer sur la molécule de référence
# 2. Comparer λ_max, ΔE_ST, SOC avec données expérimentales
# 3. Calculer MAE < 0.1 eV, R² > 0.95
# 4. Valider sur ensemble de 3-5 BODIPY supplémentaires

# Exemple avec validation étendue :
python3 analyze_results.py ADC2_vertical.out  # Extraction λ_max
python3 compare_prototypes.py ref_data.csv results.csv  # Validation
```

---

## 🛠️ Scripts Utiles

### Scripts d'automatisation

```bash
# Générer plusieurs guess pour S₁ (HOMO→LUMO, HOMO-1→LUMO, HOMO→LUMO+1)
./gen_s1_guesses.sh -t S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 8

# Troubleshooting automatique avec escalade (LevelShift/Damp/DIIS_TRAH)
./run_troubleshoot_S1.sh -i S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 8

# Copier fichiers ORCA avec bonnes conventions
./copy_and_prepare.sh /path/to/working/dir

# Préparer et soumettre tous les calculs pour un prototype
./prepare_and_submit.sh /path/to/working/dir 8 verbose
```

---

## ⚠️ Points de Vigilance

### Gestion des ressources computationnelles
- ADC(2) : Base def2-TZVP coûteuse → Tester semaine 3 si def2-SVP suffisant
- S₁ optimizations : Buffer +200-300% pour convergence (3-5 tentatives)
- SOC : ΔDFT+SOC est 10× plus rapide que NEVPT2

### Convergence des calculs
- S₁ optimization délicate → Utiliser protocole avancé
- Générer plusieurs guess électroniques pour améliorer chances de convergence
- Utiliser TRAH et algorithmes robustes (DIIS_TRAH) pour états excités

### Validation des résultats
- Comparer λ_max avec données expérimentales (MAE < 0.1 eV)
- Vérifier absence de fréquences imaginaires parasites
- Analyser les propriétés photophysiques (Φ_f, τ, k_processus)
- Évaluer les indicateurs de photostabilité (PSI) et PTT (TCI)

## 🚀 Workflow Recommandé

### Étape 1 : Préparation des fichiers

```bash
# 1. Créer un dossier pour chaque molécule
mkdir -p molecules/reference
mkdir -p molecules/iodo_bodipy
mkdir -p molecules/tpp_iodo_bodipy

# 2. Copier les fichiers de géométrie
cp Iodo_Opt.xyz molecules/iodo_bodipy/
cp TPP_Opt.xyz molecules/tpp_iodo_bodipy/
# (La référence doit être construite en semaine 2)

# 3. Copier les templates d'inputs
cp S0_gas_opt.inp molecules/reference/
cp S0_water_opt.inp molecules/reference/
# ... etc pour toutes les phases
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

### Étape 3 : Excitations verticales (Phase 2)

```bash
# ⚠️ IMPORTANT : Test comparatif def2-SVP vs def2-TZVP (Semaine 3)

# 1. Créer deux versions d'ADC2_vertical.inp
cp ADC2_vertical.inp ADC2_vertical_SVP.inp
cp ADC2_vertical.inp ADC2_vertical_TZVP.inp

# 2. Modifier les bases
# ADC2_vertical_SVP.inp : ! RI-ADC(2) def2-SVP AutoAux FrozenCore
# ADC2_vertical_TZVP.inp : ! RI-ADC(2) def2-TZVP AutoAux FrozenCore

# 3. Lancer en parallèle (batch de nuit recommandé)
sbatch submit_ADC2.slurm  # SVP
sbatch submit_ADC2.slurm  # TZVP

# 4. Comparer λ_max calculé vs expérimental
# Décision : Si écart < 5 nm → garder def2-SVP; si > 10 nm → garder def2-TZVP
grep "Excitation energy" ADC2_vertical_SVP.out | head -1
grep "Excitation energy" ADC2_vertical_TZVP.out | head -1
```

### Étape 4 : États excités relaxés (Phase 3)

```bash
# 1. Optimisation T₁ (robuste)
sbatch submit_T1.slurm

# 2. Pré-test des guesses S₁ (Semaine 7)
./gen_s1_guesses.sh -t S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 8

# 3. Lancer S₁ (Semaine 8–9)
sbatch submit_S1.slurm

# 4. Si S₁ ne converge pas après 5 tentatives
./run_troubleshoot_S1.sh -i S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 8

# 5. Vérifier convergence
grep "FINAL SINGLE POINT ENERGY" S1_opt_DeltaUKS.out
```

### Étape 5 : Couplage spin-orbite (Phase 4)

```bash
# 1. Lancer ΔDFT+SOC (recommandé)
sbatch submit_SOC.slurm

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
| **nprocs** | 8 | 8–16 | Nombre de cœurs CPU |
| **Basis set (ADC(2))** | def2-SVP | def2-TZVP | Test comparatif en semaine 3 |
| **Basis set (autres)** | def2-SVP | def2-SVP | Bon compromis |
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
