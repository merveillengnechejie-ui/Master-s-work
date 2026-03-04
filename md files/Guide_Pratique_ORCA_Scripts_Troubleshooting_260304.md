# Guide Pratique ORCA 6.1 : Scripts Prêts à l'Emploi et Troubleshooting

> **Mise à jour : 04 mars 2026 (260304)**
> - Exécution locale 16 Go RAM / TD-DFT ωB97X-D3
> - Configuration : 4 cœurs, %maxcore 3500
> - Séquentiel local (nohup) au lieu de SLURM

---

## Partie 1 : Templates d'input ORCA 6.1 (Local 16 Go)

### Configuration standard pour tous les calculs

```
%maxcore 3500
%pal nprocs 4 end
```

---

### Template 1 : S0 Optimization (Phase Gaz - Rapide)

**Fichier :** `S0_gas_opt.inp`

```orca
#==============================================================================
# ORCA 6.1 - S0 Geometry Optimization (Gas Phase)
# Purpose: Fast reconnaissance, identify major geometry issues
# Time: 30-60 min, 4 CPUs (local 16 Go)
#==============================================================================

! Opt RKS B3LYP D3BJ def2-SVP TightSCF TIGHTOPT
! Freq

%maxcore 3500
%pal nprocs 4 end

%scf
  MaxIter 500
  ConvForce 1e-6
end

%geom
  MaxStep 0.2
  Trust 0.3
  TolE 1e-6
end

* xyz 0 1
C    0.00000000    0.00000000    0.00000000
# ... INSERT YOUR BODIPY COORDINATES HERE
*
```

---

### Template 2 : S0 Optimization (SMD Mixed - Biological Environment)

**Fichier :** `S0_water_opt.inp`

```orca
#==============================================================================
# ORCA 6.1 - S0 Geometry Optimization (SMD Mixed - Biological Environment)
# Purpose: Obtain reference ground-state geometry for all following calculations
# Time: 45-90 min, 4 CPUs (local 16 Go)
#==============================================================================

! Opt RKS B3LYP D3BJ def2-SVP TightSCF TIGHTOPT
! CPCM SMD

%maxcore 3500
%pal nprocs 4 end

%cpcm
  SMDSolvent "mixed"
end

%scf
  MaxIter 500
  ConvForce 1e-6
end

%geom
  MaxStep 0.2
  Trust 0.3
  TolE 1e-6
end

* xyz 0 1
# Coordinates from S0_gas_opt.xyz
*
```

---

### Template 3 : Vertical Excitation (TD-DFT ωB97X-D3 - λ_max)

**Fichier :** `TDDFT_vertical.inp`

```orca
#==============================================================================
# ORCA 6.1 - Vertical Excitation (TD-DFT ωB97X-D3)
# Purpose: Calculate absorption spectrum (λ_max), fast for local 16 Go
# Time: 15-30 min, 4 CPUs
#==============================================================================

! wB97X-D3 def2-SVP TightSCF TD-DFT(nroots=10) CPCM SMD

%maxcore 3500
%pal nprocs 4 end

%cpcm
  SMDSolvent "mixed"
end

%tddft
  nroots 10
  DoNTOs true
end

* xyzfile 0 1 S0_water_opt.xyz
```

---

### Template 4 : T1 Optimization (ΔUKS)

**Fichier :** `T1_opt_UKS.inp`

```orca
#==============================================================================
# ORCA 6.1 - T1 Geometry Optimization (ΔUKS)
# Purpose: Optimize lowest triplet state, calculate ΔE_ST (crucial for PDT)
# Time: 60-120 min, 4 CPUs (local 16 Go)
#==============================================================================

! Opt UKS B3LYP D3BJ def2-SVP TightSCF TIGHTOPT CPCM SMD

%maxcore 3500
%pal nprocs 4 end

%cpcm
  SMDSolvent "mixed"
end

%scf
  HFTyp UKS
  SCF_ALGORITHM DIIS_TRAH
  MaxIter 500
  ConvForce 1e-6
  DampPercentage 40
  LevelShift 0.2
end

%geom
  MaxStep 0.2
  Trust 0.3
end

* xyz 0 3
# Coordinates from S0_water_opt.xyz (multiplicity = 3 for triplet)
*
```

---

### Template 5 : S1 Optimization (ΔSCF - Critical Step)

**Fichier :** `S1_opt_DeltaUKS.inp`

```orca
#==============================================================================
# ORCA 6.1 - S1 Geometry Optimization (ΔSCF)
# PURPOSE: Optimize first excited singlet state
# DIFFICULTY: ★★★★★ (Highest - requires careful tuning)
# Time: 120-180 min, 4 CPUs (may need retries with +200-300% buffer)
#==============================================================================

! Opt UKS B3LYP D3BJ def2-SVP TightSCF TIGHTOPT SlowConv CPCM SMD

%maxcore 3500
%pal nprocs 4 end

%cpcm
  SMDSolvent "mixed"
end

%scf
  HFTyp UKS
  SCF_ALGORITHM DIIS_TRAH
  MaxIter 150
  ConvForce 1e-6
  MOM true
  NoIncFock true
  DampPercentage __DAMP__
  LevelShift __LEVELSHIFT__
end

%geom
  MaxStep 0.2
  Trust 0.3
  TolG 1e-4
  TolE 1e-6
end

%moinp "S0_water_opt.gbw"

* xyz 0 1
# Coordinates from S0_water_opt.xyz
*
```

**Placeholders pour scripts d'automatisation :**
- `__DAMP__` → 40, 60, 80 (escalade)
- `__LEVELSHIFT__` → 0.0, 0.2, 0.5 (escalade)
- `__ALGO__` → DIIS, DIIS_TRAH (escalade)

---

### Template 6 : ΔDFT+SOC (Standard - Rapide)

**Fichier :** `DeltaSCF_SOC.inp`

```orca
#==============================================================================
# ORCA 6.1 - Spin-Orbit Coupling (ΔDFT+SOC)
# Purpose: Calculate S1-T1 coupling constant for ISC prediction (PDT)
# COMPLEXITY: ★★☆☆☆ (Fast, 10× vs NEVPT2)
# Time: 30-60 min, 4 CPUs (local 16 Go)
#==============================================================================

! B3LYP D3BJ def2-SVP ZORA DOSOC TightSCF CPCM SMD

%maxcore 3500
%pal nprocs 4 end

%cpcm
  SMDSolvent "mixed"
end

%rel
  DoSOC true
  Method ZORA
end

* xyzfile 0 1 S0_water_opt.xyz
```

---

### Template 7 : TD-DFT SOC (Plan B)

**Fichier :** `TDDFT_SOC_quick.inp`

```orca
#==============================================================================
# ORCA 6.1 - Spin-Orbit Coupling (TD-DFT Fast Alternative)
# PURPOSE: Quick estimate of SOC if ΔSCF S1 fails
# ACCURACY: Medium (less accurate than ΔDFT+SOC, but fast)
# TIME: 15-30 min, 4 CPUs
#==============================================================================

! wB97X-D3 def2-SVP ZORA RIJCOSX AutoAux CPCM SMD

%maxcore 3500
%pal nprocs 4 end

%cpcm
  SMDSolvent "mixed"
end

%tddft
  nstates 10
  ntrips 10
  dosoc true
end

* xyzfile 0 1 S0_water_opt.xyz
```

---

## Partie 2 : Scripts Bash (Automatisation Locale)

### Script 1 : gen_s1_guesses.sh

**Utilisation :**
```bash
./gen_s1_guesses.sh -t S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 4
```

**Fonction :** Génère 3 guesses électroniques (HOMO→LUMO, HOMO-1→LUMO, HOMO→LUMO+1) et teste la convergence.

---

### Script 2 : run_troubleshoot_S1.sh

**Utilisation :**
```bash
./run_troubleshoot_S1.sh -i S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 4
```

**Fonction :** Escalade automatique des paramètres (LevelShift, Damp, DIIS_TRAH) jusqu'à convergence.

---

### Script 3 : Exécution séquentielle locale

```bash
#!/bin/bash
# run_local_sequential.sh - Exécution locale séquentielle (16 Go, 4 cœurs)

PROTOTYPES=("iodo" "tpp-iodo")

for proto in "${PROTOTYPES[@]}"; do
    echo "========================================="
    echo "Processing: $proto"
    echo "========================================="

    cd "$proto"

    # Étape 1 : S0 gaz
    echo "Step 1: S0 optimization (gas phase)"
    nohup orca S0_gas_opt.inp > S0_gas_opt.out &
    wait
    echo "✓ S0 gas phase completed"

    # Étape 2 : S0 eau (SMD mixed)
    echo "Step 2: S0 optimization (SMD mixed)"
    nohup orca S0_water_opt.inp > S0_water_opt.out &
    wait
    echo "✓ S0 biological environment completed"

    # Étape 3 : TD-DFT vertical
    echo "Step 3: Vertical excitation (TD-DFT)"
    nohup orca TDDFT_vertical.inp > TDDFT_vertical.out &
    wait
    echo "✓ TD-DFT calculation completed"

    # Étape 4 : T1 optimization
    echo "Step 4: T1 optimization (ΔUKS)"
    nohup orca T1_opt_UKS.inp > T1_opt_UKS.out &
    wait
    echo "✓ T1 optimization completed"

    # Étape 5 : S1 optimization (CRITIQUE)
    echo "Step 5: S1 optimization (ΔSCF)"
    ../gen_s1_guesses.sh -t S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 4
    nohup orca S1_opt_DeltaUKS.inp > S1_opt_DeltaUKS.out &
    wait
    if [ $? -eq 0 ]; then
        echo "✓ S1 optimization completed"
    else
        echo "⚠ S1 optimization FAILED - Applying recovery..."
        ../run_troubleshoot_S1.sh -i S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 4
    fi

    # Étape 6 : SOC (ΔDFT+SOC)
    echo "Step 6: SOC calculation (ΔDFT+SOC)"
    nohup orca DeltaSCF_SOC.inp > DeltaSCF_SOC.out &
    wait
    echo "✓ SOC calculation completed"

    echo "========================================="
    echo "$proto completed successfully!"
    echo "========================================="
    echo
done

echo "All prototypes processed."
```

---

## Partie 3 : Troubleshooting Guide

### Problème 1 : Optimisation S0 ne converge pas

**Symptôme :** Le calcul s'arrête après MaxIter itérations sans converger.

**Solutions (ordre d'escalade) :**

1. **Vérifier la géométrie initiale**
   - S'assurer que les coordonnées XYZ sont raisonnables
   - Utiliser Avogadro pour visualiser et corriger

2. **Réduire le pas de géométrie**
   ```orca
   %geom
     MaxStep 0.1   # Réduire de 0.2 à 0.1
     Trust 0.1
   end
   ```

3. **Changer le solveur SCF**
   ```orca
   %scf
     SCF_ALGORITHM DIIS_TRAH
   end
   ```

4. **Augmenter les itérations**
   ```orca
   %scf
     MaxIter 1000
   end
   ```

---

### Problème 2 : Optimisation S1 (ΔSCF) échoue complètement

**Symptôme :** L'état S1 s'effondre vers S0 ou le SCF diverge.

**Solutions :**

1. **Utiliser gen_s1_guesses.sh** (3 guesses différents)
   ```bash
   ./gen_s1_guesses.sh -t S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 4
   ```

2. **Augmenter l'amortissement et le shift**
   ```orca
   %scf
     DampPercentage 60
     LevelShift 0.5
   end
   ```

3. **Utiliser run_troubleshoot_S1.sh** (escalade auto)
   ```bash
   ./run_troubleshoot_S1.sh -i S1_opt_DeltaUKS.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 4
   ```

4. **Réduire le pas de géométrie**
   ```orca
   %geom
     MaxStep 0.1
     Trust 0.1
   end
   ```

5. **Plan B : TD-DFT pour diagnostics**
   ```orca
   ! wB97X-D3 def2-SVP TD-DFT
   ```

---

### Problème 3 : Out of Memory (16 Go)

**Symptôme :** Message "Insufficient memory"

**Solutions :**

1. **Réduire MaxCore**
   ```orca
   %maxcore 3000  # Réduire de 3500 à 3000
   ```

2. **Utiliser une base plus petite**
   ```orca
   ! Opt RKS B3LYP def2-SVP  # def2-SVP est déjà léger
   ```

3. **1 seul calcul à la fois**
   ```bash
   # Ne pas lancer plusieurs orca en parallèle
   ```

---

### Problème 4 : Résultats λ_max loin des attentes

**Symptôme :** λ_max calculé ≠ λ_max attendu.

**Solutions :**

1. **Vérifier le benchmarking** (semaine 3)
   - Comparer avec données expérimentales
   - Si écart > 10 nm → vérifier méthode

2. **Test def2-SVP vs def2-TZVP**
   ```bash
   # Lancer les deux bases sur référence
   # Choisir celle avec MAE < 5 nm
   ```

3. **Vérifier la géométrie S0**
   - Relancer optimisation S0 avec critères stricts

---

## Partie 4 : Checklist avant de soumettre

- [ ] Vérifier que les fichiers XYZ sont correctement formatés
- [ ] S'assurer que le répertoire a ≥ 50 GB d'espace libre
- [ ] Vérifier configuration : %maxcore 3500, %pal nprocs 4
- [ ] Tester sur molécule test (benzène) avant BODIPY
- [ ] Sauvegarder les fichiers GBW régulièrement
- [ ] Utiliser nohup pour sessions longues

---

## Partie 5 : Extraction des Résultats

### Script Python : analyze_results.py

```python
#!/usr/bin/env python3
"""ORCA Results Analyzer for BODIPY Project (Local 16 Go)"""

import re
import sys

def extract_energy(filename):
    with open(filename, 'r') as f:
        content = f.read()
    match = re.search(r'FINAL SINGLE POINT ENERGY\s+([-+]?\d+\.\d+)', content)
    return float(match.group(1)) if match else None

def extract_lambda_max(filename):
    with open(filename, 'r') as f:
        content = f.read()
    match = re.search(r'Excitation energy:\s+([-+]?\d+\.\d+)\s+eV', content)
    if match:
        e_ev = float(match.group(1))
        return 1240 / e_ev
    return None

def extract_soc(filename):
    with open(filename, 'r') as f:
        content = f.read()
    matches = re.findall(r'<S\d+\|SOC\|T\d+>\s*=\s*([-+]?\d+\.\d+)', content)
    return [float(v) for v in matches] if matches else []

# Usage
if __name__ == "__main__":
    E_S0 = extract_energy("S0_water_opt.out")
    E_S1 = extract_energy("S1_water_opt.out")
    E_T1 = extract_energy("T1_water_opt.out")
    lambda_max = extract_lambda_max("TDDFT_vertical.out")
    soc = extract_soc("DeltaSCF_SOC.out")

    print(f"E_S0 = {E_S0:.6f} a.u.")
    print(f"E_S1 = {E_S1:.6f} a.u.")
    print(f"E_T1 = {E_T1:.6f} a.u.")
    print(f"ΔE_ST = {(E_S1-E_T1)*27.211:.4f} eV")
    print(f"λ_max = {lambda_max:.1f} nm")
    print(f"SOC max = {max(soc):.2f} cm⁻¹")
```

---

**Document complément — Version 260304 (04 mars 2026)**

**Configuration : Local 16 Go RAM / 4 cœurs / TD-DFT ωB97X-D3**
