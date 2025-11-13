# Guide Pratique ORCA 6.1 : Scripts Prêts à l'Emploi et Troubleshooting

## Partie 1 : Suite de scripts ORCA pour le protocole complet

### 1.1 Workflow automatisé (bash script)

Créer un fichier `run_protocol.sh` pour lancer l'ensemble des calculs :

```bash
#!/bin/bash
# Script pour lancer le protocole complet OO-DFT pour les 3 prototypes

PROTOTYPES=("proto-A" "proto-B" "proto-C")
WORKDIR="/path/to/work/directory"

for proto in "${PROTOTYPES[@]}"; do
    echo "========================================="
    echo "Processing: $proto"
    echo "========================================="
    
    cd "$WORKDIR/$proto"
    
    # Étape 1 : Optimisation S0 en phase gaz (reconnaissance rapide)
    echo "Step 1: S0 optimization (gas phase) - FAST"
    orca S0_gas_opt.inp > S0_gas_opt.out 2>&1
    if [ $? -eq 0 ]; then
        echo "✓ S0 gas phase completed"
    else
        echo "✗ S0 gas phase FAILED - Check output file"
        exit 1
    fi
    
    # Étape 2 : Optimisation S0 en solution (point de départ principal)
    echo "Step 2: S0 optimization (CPCM-Water) - MEDIUM"
    orca S0_water_opt.inp > S0_water_opt.out 2>&1
    if [ $? -eq 0 ]; then
        echo "✓ S0 water phase completed"
    else
        echo "✗ S0 water phase FAILED"
        exit 1
    fi
    
    # Étape 3 : Excitation verticale (ADC2)
    echo "Step 3: Vertical excitation (ADC2) - EXPENSIVE"
    orca ADC2_vertical.inp > ADC2_vertical.out 2>&1
    if [ $? -eq 0 ]; then
        echo "✓ ADC2 calculation completed"
    else
        echo "✗ ADC2 calculation FAILED"
        exit 1
    fi
    
    # Étape 4 : Optimisation T1
    echo "Step 4: T1 optimization (ΔUKS) - MEDIUM"
    orca T1_water_opt.inp > T1_water_opt.out 2>&1
    if [ $? -eq 0 ]; then
        echo "✓ T1 optimization completed"
    else
        echo "✗ T1 optimization FAILED"
        exit 1
    fi
    
    # Étape 5 : Optimisation S1 (CRITIQUE)
    echo "Step 5: S1 optimization (ΔSCF) - EXPENSIVE & DIFFICULT"
    orca S1_water_opt.inp > S1_water_opt.out 2>&1
    if [ $? -eq 0 ]; then
        echo "✓ S1 optimization completed"
    else
        echo "⚠ S1 optimization FAILED - Applying recovery strategy..."
        # Strategy: augment damping and retry
        sed -i 's/DampPercentage 40/DampPercentage 60/g' S1_water_opt.inp
        orca S1_water_opt.inp > S1_water_opt_retry.out 2>&1
        if [ $? -eq 0 ]; then
            echo "✓ S1 optimization succeeded on retry"
            mv S1_water_opt_retry.out S1_water_opt.out
        else
            echo "✗ S1 optimization failed even after retry"
            exit 1
        fi
    fi
    
    # Étape 6 : Couplage spin-orbite (NEVPT2) - TRÈS COÛTEUX
    echo "Step 6: SOC calculation (FIC-NEVPT2) - VERY EXPENSIVE"
    orca NEVPT2_SOC.inp > NEVPT2_SOC.out 2>&1
    if [ $? -eq 0 ]; then
        echo "✓ NEVPT2 SOC calculation completed"
    else
        echo "⚠ NEVPT2 SOC failed - Using fast TD-DFT alternative..."
        orca TDDFT_SOC_fast.inp > TDDFT_SOC_fast.out 2>&1
        if [ $? -eq 0 ]; then
            echo "✓ Fast TD-DFT SOC (alternative) completed"
        else
            echo "✗ SOC calculation completely failed"
            exit 1
        fi
    fi
    
    echo "========================================="
    echo "$proto completed successfully!"
    echo "========================================="
    echo
done

echo "All prototypes processed. Check results in subdirectories."
```

---

### 1.2 Templates d'input ORCA 6.1

#### Template 1 : S0 Optimization (Gas Phase - Fast)

**Fichier :** `S0_gas_opt.inp`

```orca
#==============================================================================
# ORCA 6.1 - S0 Geometry Optimization (Gas Phase)
# Purpose: Fast reconnaissance, identify major geometry issues
# Time: 30-60 min, 8 CPUs
#==============================================================================

! Opt RKS B3LYP D3BJ def2-SVP TightSCF TIGHTOPT
! Freq # Optional: add if you want to verify no imaginary frequencies

%pal
  nprocs 8
end

%scf
  MaxIter 500
  ConvForce 1e-6
end

%geom
  MaxStep 0.2
  Trust 0.3
  TolE 1e-6      # Energy convergence
end

* xyz 0 1
C    0.00000000    0.00000000    0.00000000
N    1.50000000    0.00000000    0.00000000
# ... INSERT YOUR BODIPY COORDINATES HERE FROM AVOGADRO
*
```

---

#### Template 2 : S0 Optimization (CPCM-Water, Main Reference)

**Fichier :** `S0_water_opt.inp`

```orca
#==============================================================================
# ORCA 6.1 - S0 Geometry Optimization (CPCM-Water)
# Purpose: Obtain reference ground-state geometry for all following calculations
# Time: 45-90 min, 8 CPUs
# Output files to save: S0_water_opt.gbw, S0_water_opt.xyz
#==============================================================================

! Opt RKS B3LYP D3BJ def2-SVP TightSCF TIGHTOPT
! CPCM(Water)

%pal
  nprocs 8
end

%cpcm
  epsilon 80.0   # Water dielectric constant
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
C    0.00000000    0.00000000    0.00000000
N    1.50000000    0.00000000    0.00000000
# ... INSERT YOUR BODIPY COORDINATES HERE FROM S0_gas_opt.xyz
*
```

---

#### Template 3 : Vertical Excitation (ADC(2) - λ_max)

**Fichier :** `ADC2_vertical.inp`

```orca
#==============================================================================
# ORCA 6.1 - Vertical Excitation (ADC2)
# Purpose: Calculate absorption spectrum (λ_max), first excited state S1
# Time: 60-120 min, 8 CPUs
# Key output: S1 excitation energy in eV (convert to nm using: λ = 1240/E)
#==============================================================================

! RI-ADC(2) def2-SVP AutoAux FrozenCore
! CPCM(Water)

%pal
  nprocs 8
end

%cpcm
  epsilon 80.0
end

%adc
  n_exc_states 10         # Calculate 10 singlet excited states
  do_triplets true        # Also calculate triplet states (useful for analysis)
  DoNTOs true            # Calculate Natural Transition Orbitals
  TransDensity true      # Calculate transition density
end

* xyzfile 0 1 S0_water_opt.xyz
```

**Post-processing:** After calculation, grep for "S_1 state" in the output to find λ_max.

---

#### Template 4 : T1 Optimization (ΔUKSfor ISC evaluation)

**Fichier :** `T1_water_opt.inp`

```orca
#==============================================================================
# ORCA 6.1 - T1 Geometry Optimization (ΔUKSwith Triplet Multiplicty)
# Purpose: Optimize lowest triplet state, calculate ΔE_ST (crucial for PDT)
# Time: 60-120 min, 8 CPUs
# Output: T1_water_opt.gbw, T1_water_opt.xyz, energies
#==============================================================================

! Opt UKS B3LYP D3BJ def2-SVP TightSCF TIGHTOPT
! CPCM(Water)

%pal
  nprocs 8
end

%cpcm
  epsilon 80.0
end

%scf
  HFTyp UKS                    # Unrestricted Kohn-Sham for triplet
  SCF_ALGORITHM DIIS_TRAH     # Robust algorithm for difficult cases
  MaxIter 500
  ConvForce 1e-6
  DampPercentage 40           # Damping factor
  LevelShift 0.2              # Orbital shift for convergence
end

%geom
  MaxStep 0.2
  Trust 0.3
end

* xyz 0 3
C    0.00000000    0.00000000    0.00000000
N    1.50000000    0.00000000    0.00000000
# ... INSERT YOUR BODIPY COORDINATES HERE FROM S0_water_opt.xyz
*
```

**Important:** Multiplicité = 3 (for triplet). The multiplicity is specified as `0 3` in the XYZ block (charge 0, multiplicity 3).

---

#### Template 5 : S1 Optimization (ΔSCF - Critical Step)

**Fichier :** `S1_water_opt.inp`

```orca
#==============================================================================
# ORCA 6.1 - S1 Geometry Optimization (ΔSCF = Delta-SCF)
# PURPOSE: Optimize first excited singlet state
# DIFFICULTY: ★★★★★ (Highest - requires careful tuning)
# Time: 120-180 min, 8 CPUs (may need retries)
# OUTPUT: S1_water_opt.gbw, S1_water_opt.xyz, E_adiabatic
#
# STRATEGY: Use Unrestricted DFT (broken-spin determinant) + robust SCF solver
# The key is to prevent variational collapse back to S0
#==============================================================================

! Opt UKS B3LYP D3BJ def2-SVP TightSCF TIGHTOPT SlowConv
! CPCM(Water)

%pal
  nprocs 8
end

%cpcm
  epsilon 80.0
end

%scf
  HFTyp UKS
  SCF_ALGORITHM DIIS_TRAH       # TRAH (Trust-Region with Augmented Hessian)
  MaxIter 500
  ConvForce 1e-6
  
  # Convergence stabilization strategies
  DampPercentage 40             # Moderate damping (increase to 60 if needed)
  LevelShift 0.2               # Orbital energy shift (increase to 0.5+ if difficult)
  
  # Advanced options
  MaxCore 8000
end

%geom
  MaxStep 0.2
  Trust 0.3
  TolG 1e-4
  TolE 1e-6
end

# CRITICAL: Read S0 orbitals and swap HOMO-LUMO configuration
# This ensures we start from an excited-state-like configuration
%moinp "S0_water_opt.gbw"

* xyz 0 1
C    0.00000000    0.00000000    0.00000000
N    1.50000000    0.00000000    0.00000000
# ... INSERT YOUR BODIPY COORDINATES HERE FROM S0_water_opt.xyz
*
```

**Recovery strategies if convergence fails:**

```orca
# STRATEGY A: Increase damping
! Opt UKS B3LYP D3BJ def2-SVP TightSCF TIGHTOPT SlowConv
%scf
  DampPercentage 70        # Stronger damping
  LevelShift 0.5          # Larger shift
end

# STRATEGY B: Use larger basis set
! Opt UKS B3LYP D3BJ def2-TZVP TightSCF TIGHTOPT SlowConv
# (More flexible, but slower)

# STRATEGY C: Reduce geometry step size
%geom
  MaxStep 0.1             # Smaller steps
  Trust 0.1
end

# STRATEGY D: Use alternative functional (if B3LYP fails)
! Opt UKS wB97X-D3BJ def2-SVP TightSCF TIGHTOPT
```

---

#### Template 6 : Adiabatic Energy Calculation (Post-processing)

After S0 and S1 optimizations, calculate:

```
E_adiabatic = E_S0(optimized geom) - E_S1(optimized geom)
ΔE_ST = E_S1 - E_T1  (use energies from optimized geometries)
```

**Python script to extract energies:**

```python
#!/usr/bin/env python3
import re

def extract_energy(filename):
    """Extract FINAL SCF Energy from ORCA output"""
    with open(filename, 'r') as f:
        content = f.read()
    
    # Search for "FINAL SINGLE POINT ENERGY"
    match = re.search(r'FINAL SINGLE POINT ENERGY\s+([-+]?\d+\.\d+)', content)
    if match:
        return float(match.group(1))
    else:
        raise ValueError(f"Could not find FINAL SINGLE POINT ENERGY in {filename}")

# Read energies
E_S0 = extract_energy("S0_water_opt.out")
E_S1 = extract_energy("S1_water_opt.out")
E_T1 = extract_energy("T1_water_opt.out")

# Calculate
E_ad = E_S0 - E_S1
Delta_E_ST = E_S1 - E_T1

print(f"E_S0 = {E_S0:.6f} a.u.")
print(f"E_S1 = {E_S1:.6f} a.u.")
print(f"E_T1 = {E_T1:.6f} a.u.")
print(f"\nE_adiabatic (S0 -> S1) = {E_ad:.6f} a.u. = {E_ad*27.211:.4f} eV")
print(f"ΔE_ST = {Delta_E_ST:.6f} a.u. = {Delta_E_ST*27.211:.4f} eV")

# Interpretation
if E_ad * 27.211 < 1.0:
    print("✓ Good PTT potential (small adiabatic energy)")
else:
    print("⚠ Large adiabatic energy (may be less suitable for PTT)")

if Delta_E_ST * 27.211 < 0.1:
    print("✓ Good ISC efficiency (small S1-T1 gap)")
else:
    print("⚠ Large S1-T1 gap (may limit PDT effectiveness)")
```

---

#### Template 7 : Couplage Spin-Orbite (FIC-NEVPT2 - Gold Standard)

**Fichier :** `NEVPT2_SOC.inp`

```orca
#==============================================================================
# ORCA 6.1 - Spin-Orbit Coupling Calculation (FIC-NEVPT2)
# Purpose: Calculate S1-T1 coupling constant for ISC prediction (PDT potential)
# COMPLEXITY: ★★★★★ (Very expensive, highly accurate)
# Time: 150-300 min, 8 CPUs
#
# NOTE: This is the "gold standard" for SOC calculations on BODIPY.
# For faster alternative, see TDDFT_SOC_fast.inp
#==============================================================================

! FIC-NEVPT2 wB97X-D3BJ def2-TZVP ZORA RIJCOSX AutoAux
! CPCM(Water)

%pal
  nprocs 8
end

%cpcm
  epsilon 80.0
end

# Define active space for BODIPY (typically 8 electrons in 6 orbitals around HOMO/LUMO)
%casscf
  nel 8                  # Number of active electrons
  norb 6                 # Number of active orbitals
  
  # Calculate both singlet and triplet roots
  mult 1,3              # Multiplicities: 1 = singlet, 3 = triplet
  nroots 1,1            # 1 root for S1, 1 root for T1
  
  # NEVPT2 perturbative correction
  PTMethod FIC_NEVPT2   # Fully-Internally-Contracted NEVPT2
  
  # Convergence parameters
  TraceCI 1.0
  MaxIter 150
end

# Relativistic effects (ZORA) and Spin-Orbit Coupling
%rel
  DoSOC true            # Enable spin-orbit coupling calculation
  Method ZORA           # Scalar-relativistic ZORA approach
  zcora_model 6         # Standard ZORA model
  
  # SOC-specific options
  SOCType PerturbativeSOC  # Use perturbative SOC
end

* xyzfile 0 1 S0_water_opt.xyz
```

**Expected output:**
- Look for: "Spin-Orbit Coupling Matrix" in output
- Units: cm⁻¹ (wave numbers)
- Typical BODIPY values: 1-10 cm⁻¹ (no heavy atom), 50-200 cm⁻¹ (with I)

---

#### Template 8 : Couplage Spin-Orbite (TD-DFT Fast Alternative)

**Fichier :** `TDDFT_SOC_fast.inp`

```orca
#==============================================================================
# ORCA 6.1 - Spin-Orbit Coupling (TD-DFT Fast Alternative)
# PURPOSE: Quick estimate of SOC if FIC-NEVPT2 not feasible
# ACCURACY: Medium (less accurate than NEVPT2, but fast)
# TIME: 30-60 min, 8 CPUs
#
# USE WHEN: Computational resources are limited or validation needed quickly
#==============================================================================

! wB97X-D3BJ def2-SVP ZORA RIJCOSX AutoAux
! CPCM(Water)

%pal
  nprocs 8
end

%cpcm
  epsilon 80.0
end

%tddft
  nstates 10             # Number of singlet states
  ntrips 10              # Number of triplet states
  dosoc true             # Enable SOC calculation
  
  # Advanced options for accuracy
  UseAuxJ true
end

* xyzfile 0 1 S0_water_opt.xyz
```

**Note:** This is faster but less accurate. Use primarily for screening or validation.

---

### 1.3 Script Python pour l'analyse post-traitement

**Fichier :** `analyze_results.py`

```python
#!/usr/bin/env python3
"""
ORCA Results Analyzer for BODIPY Theragnosis Project
Extracts key properties: λ_max, ΔE_ST, energies, charges
"""

import re
import sys
from pathlib import Path

class ORCAAnalyzer:
    def __init__(self, outfile):
        self.outfile = outfile
        with open(outfile, 'r') as f:
            self.content = f.read()
    
    def extract_final_energy(self):
        """Extract FINAL SINGLE POINT ENERGY"""
        match = re.search(r'FINAL SINGLE POINT ENERGY\s+([-+]?\d+\.\d+)', self.content)
        return float(match.group(1)) if match else None
    
    def extract_s1_energy(self):
        """Extract S1 excitation energy from ADC(2) output"""
        # For ADC(2): look for "S_1 state"
        match = re.search(r'S_1\s+state:\s+([-+]?\d+\.\d+)\s+eV', self.content)
        if match:
            e_ev = float(match.group(1))
            wavelength_nm = 1240 / e_ev
            return e_ev, wavelength_nm
        return None, None
    
    def extract_soc_values(self):
        """Extract SOC matrix elements"""
        matches = re.findall(r'<S\d+\|SOC\|T\d+>\s*=\s*([-+]?\d+\.\d+)', self.content)
        return matches if matches else []
    
    def extract_charges(self):
        """Extract Mulliken or Hirshfeld charges"""
        charges = {}
        # This is simplified; actual implementation would be more robust
        for line in self.content.split('\n'):
            if 'Mulliken charge' in line or 'Hirshfeld charge' in line:
                parts = line.split()
                if len(parts) > 2:
                    try:
                        charges[parts[0]] = float(parts[-1])
                    except ValueError:
                        pass
        return charges
    
    def report(self):
        """Print comprehensive analysis"""
        print(f"\n{'='*60}")
        print(f"ORCA Output Analysis: {self.outfile}")
        print(f"{'='*60}\n")
        
        # Energy
        E = self.extract_final_energy()
        if E:
            print(f"✓ Final Energy: {E:.10f} a.u.")
        
        # S1 and λ_max (if ADC(2))
        E_S1, lambda_max = self.extract_s1_energy()
        if E_S1:
            print(f"✓ S1 Excitation Energy: {E_S1:.4f} eV")
            print(f"✓ λ_max: {lambda_max:.1f} nm")
            
            # Check if in therapeutic window
            if 600 <= lambda_max <= 900:
                print(f"  ✓ Within NIR-I window (600-900 nm) ✓")
            elif 1000 <= lambda_max <= 1700:
                print(f"  ✓ Within NIR-II window (1000-1700 nm) ✓")
            else:
                print(f"  ⚠ Outside therapeutic windows")
        
        # SOC
        soc_vals = self.extract_soc_values()
        if soc_vals:
            print(f"✓ SOC values (cm⁻¹): {soc_vals}")
            max_soc = max(float(v) for v in soc_vals)
            print(f"  Max SOC: {max_soc:.2f} cm⁻¹")
            if max_soc > 50:
                print(f"  ✓ Strong SOC → Good PDT potential ✓")
            elif max_soc > 10:
                print(f"  ⚠ Moderate SOC → Acceptable PDT potential")
            else:
                print(f"  ✗ Weak SOC → Limited PDT potential")
        
        # Charges
        charges = self.extract_charges()
        if charges:
            print(f"✓ Atomic Charges:")
            for atom, charge in list(charges.items())[:5]:  # Print first 5
                print(f"  {atom}: {charge:+.4f}")
        
        print(f"\n{'='*60}\n")

def compare_prototypes(proto_files):
    """Compare results across multiple prototypes"""
    print("\n" + "="*80)
    print("PROTOTYPE COMPARISON TABLE")
    print("="*80 + "\n")
    
    results = {}
    for name, outfile in proto_files.items():
        analyzer = ORCAAnalyzer(outfile)
        E = analyzer.extract_final_energy()
        E_S1, lambda_max = analyzer.extract_s1_energy()
        soc_vals = analyzer.extract_soc_values()
        
        results[name] = {
            'Energy': E,
            'λ_max (nm)': lambda_max,
            'SOC (cm⁻¹)': max(float(v) for v in soc_vals) if soc_vals else 0
        }
    
    # Print table
    print(f"{'Prototype':<15} {'Energy (a.u.)':<20} {'λ_max (nm)':<15} {'Max SOC (cm⁻¹)':<15}")
    print("-" * 80)
    for proto, data in results.items():
        print(f"{proto:<15} {data['Energy']:<20.10f} {data['λ_max (nm)']:<15.1f} {data['SOC (cm⁻¹)']:<15.2f}")
    print("\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_results.py <output_file> [other_files...]")
        sys.exit(1)
    
    # Single analysis
    analyzer = ORCAAnalyzer(sys.argv[1])
    analyzer.report()
    
    # Comparison if multiple files
    if len(sys.argv) > 2:
        proto_files = {f"Proto-{i}": sys.argv[i+1] for i in range(len(sys.argv)-1)}
        compare_prototypes(proto_files)
```

---

## Partie 2 : Troubleshooting Guide

### Problème 1 : Optimisation S0 ne converge pas

**Symptôme :** Le calcul s'arrête après MaxIter itérations sans converger.

**Solutions (ordre d'escalade) :**

1. **Vérifier la géométrie initiale**
   - S'assurer que les coordonnées XYZ sont raisonnables (pas d'atomes trop proches)
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
     SCF_ALGORITHM DIIS_TRAH  # Plus robuste que DIIS pur
   end
   ```

4. **Utiliser une base plus grande**
   ```orca
   ! Opt RKS B3LYP D3BJ def2-TZVP  # Passer de SVP à TZVP
   ```

5. **Augmenter les itérations**
   ```orca
   %scf
     MaxIter 1000  # Augmenter de 500 à 1000
   end
   ```

---

### Problème 2 : Optimisation S1 (ΔSCF) échoue complètement

**Symptôme :** L'état S1 s'effondre vers S0 ou le SCF diverge.

**Causes probables :**
- Pas de configuration initiale excitée appropriée
- Manque de stabilisation du SCF
- Base insuffisante

**Solutions :**

1. **Augmenter l'amortissement et le shift**
   ```orca
   %scf
     DampPercentage 60   # Augmenter progressivement
     LevelShift 0.5      # Augmenter de 0.2 à 0.5
     TRAH_MaxDim 30      # Augmenter la mémoire TRAH
   end
   ```

2. **Ajouter des variables d'optimisation graduelles**
   ```orca
   %geom
     MaxStep 0.1
     Trust 0.1
     # Optimiser d'abord sans gradient strict
   end
   ```

3. **Utiliser une géométrie initiale meilleure**
   - Lancer d'abord une optimisation rapide avec TD-DFT pour obtenir une géométrie S1 approchée
   - Utiliser cette géométrie comme point de départ pour ΔSCF

4. **Alternative : Utiliser TDDFT-OPT si disponible**
   ```orca
   ! OptTS TD-DFT B3LYP def2-SVP  # Chercher un TS entre S0 et S1
   ```

---

### Problème 3 : Calcul ADC(2) est trop lent

**Symptôme :** ADC(2) prend > 4 heures.

**Solutions :**

1. **Utiliser une base plus petite**
   ```orca
   ! RI-ADC(2) def2-SVP  # C'est déjà petit; utiliser def-TZVP seulement si nécessaire
   ```

2. **Réduire le nombre d'états calculés**
   ```orca
   %adc
     n_exc_states 5      # Réduire de 10 à 5 (suffit pour λ_max)
     do_triplets false   # Désactiver triplets pour calcul plus rapide
   end
   ```

3. **Utiliser le Tamm-Dancoff approximation (TDA)**
   ```orca
   ! RI-ADC(2)-x def2-SVP  # Version TDA plus rapide
   ```

4. **Paralléliser davantage**
   ```orca
   %pal
     nprocs 16  # Augmenter le nombre de processeurs
   end
   ```

---

### Problème 4 : NEVPT2 SOC prend trop longtemps

**Symptôme :** FIC-NEVPT2 dépasse 6 heures.

**Solutions :**

1. **Réduire l'espace actif CAS**
   ```orca
   %casscf
     nel 6      # Réduire de 8 à 6
     norb 4     # Réduire de 6 à 4
   end
   ```

2. **Utiliser une base plus petite pour le CAS**
   ```orca
   ! FIC-NEVPT2 wB97X-D3BJ def2-SVP ZORA  # Passer de TZVP à SVP
   ```

3. **Utiliser une approximation plus rapide (DLPNO-STEOM-CCSD ou autre)**
   ```orca
   ! DLPNO-STEOM-CCSD def2-TZVP
   ```

4. **Utiliser TD-DFT rapide à la place (acceptable pour validation)**
   ```orca
   ! wB97X-D3BJ def2-SVP ZORA RIJCOSX
   %tddft
     dosoc true
   end
   ```

---

### Problème 5 : Fichiers GBW manquants ou corrompus

**Symptôme :** Message d'erreur : "Cannot open gbw file"

**Solutions :**

1. **Vérifier que le fichier existe**
   ```bash
   ls -la *.gbw
   ```

2. **Vérifier le chemin correct dans %moinp**
   ```orca
   %moinp "S0_water_opt.gbw"  # Chemin relatif ou absolu
   ```

3. **Régénérer le fichier GBW en relançant le calcul précédent**
   ```bash
   orca S0_water_opt.inp
   ```

4. **Utiliser le fichier backup si disponible**
   ```bash
   cp S0_water_opt.gbw.bak S0_water_opt.gbw
   ```

---

### Problème 6 : Erreur de mémoire ("MaxCore exceeded")

**Symptôme :** Message : "Insufficient memory"

**Solutions :**

1. **Réduire MaxCore**
   ```orca
   %scf
     MaxCore 2000  # Réduire de 8000 à 2000 (en MB)
   end
   ```

2. **Utiliser l'approche RIJCOSX au lieu de RI**
   ```orca
   ! Opt RKS B3LYP RIJCOSX AutoAux  # Plus efficace en mémoire
   ```

3. **Réduire la base**
   ```orca
   ! Opt RKS B3LYP def2-SVP  # Passer de TZVP à SVP
   ```

4. **Augmenter la mémoire du système** (si possible via SLURM)
   ```bash
   #SBATCH --mem=32GB  # Augmenter l'allocation mémoire
   ```

---

### Problème 7 : Résultats λ_max loin des attentes

**Symptôme :** λ_max calculé ≠ λ_max expérimental.

**Solutions :**

1. **Vérifier le benchmarking** : Comparer d'abord avec un BODIPY de référence
   - Si écart > 50 nm → vérifier la méthode

2. **Essayer une fonctionnelle différente**
   ```orca
   ! RI-ADC(2) wB97X-D3BJ def2-SVP  # Changer de B3LYP à wB97X
   ```

3. **Utiliser une base plus grande**
   ```orca
   ! RI-ADC(2) B3LYP def2-TZVP  # Passer de SVP à TZVP
   ```

4. **Vérifier la géométrie S0** : Relancer l'optimisation S0 avec critères plus stricts
   ```orca
   %scf
     ConvForce 1e-7  # Très strict
   end
   ```

5. **Utiliser une méthode plus précise pour le benchmarking**
   ```orca
   ! RI-CC2 def2-SVP  # CC2 plus précis que ADC(2)
   ```

---

## Partie 3 : Checklist avant de soumettre les calculs

- [ ] Vérifier que tous les fichiers XYZ sont correctement formattés (nombre d'atomes, charges)
- [ ] S'assurer que le répertoire de travail a au moins 50 GB d'espace disque libre
- [ ] Vérifier les allocations SLURM : temps, CPUs, mémoire
- [ ] Tester les scripts ORCA sur une molécule test petite (ex: benzène) avant le BODIPY complet
- [ ] Sauvegarder les fichiers GBW importants régulièrement
- [ ] Mettre en place des logs de suivi (quel job, quel calcul, quel statut)
- [ ] Prévoir des points de sauvegarde (checkpoints) tous les 50-100 itérations pour les calculs longs

---

**Document complément à "demarche_methodologique_stage_v2_integree.md"**
