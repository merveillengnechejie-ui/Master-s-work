# Protocole P4 — Benchmark TD-DFT : 6 Fonctionnelles
## Semaines 4–5 — Trouver la meilleure fonctionnelle pour vos molécules

---

## Objectif

Déterminer quelle fonctionnelle TD-DFT prédit le mieux λ_max pour les BODIPY-NTR en comparant les calculs aux données expérimentales de la littérature.

**Résultat attendu** : Une fonctionnelle recommandée avec MAE < 0.2 eV pour toutes les analyses suivantes.

---

## 1. Données expérimentales de référence

Remplir `../data/experimental_benchmark.csv` avec ces données :

| Molécule | λ_max exp (nm) | Solvant | Φ_f | Source |
|----------|---------------|---------|-----|--------|
| BODIPY-Ph | 505 | DMSO | 0.80 | Sandoval 2023 |
| Br-BODIPY | 535 | CH₂Cl₂ | 0.45 | Ponte 2018 |
| I-BODIPY | 545 | CH₂Cl₂ | 0.02 | Baig 2024 |
| BODIPY-dimer | 680 | DMSO | 0.15 | Porolnik 2024 |

> **À compléter** : Extraire les valeurs exactes en relisant les articles originaux. Ne jamais utiliser des valeurs sans les avoir vérifiées dans la source primaire.

---

## 2. Input ORCA pour TD-DFT vertical (template)

Créer un fichier par fonctionnelle. Exemple pour ωB97X-D :

```orca
# Fichier : calculations/tier2_tddft/wB97X-D/BODIPY_Ph_T2_wB97XD.inp

! RKS wB97X-D def2-SVP AutoAux RIJCOSX TightSCF
! CPCM(water)
%pal nprocs 4 end
%maxcore 7000
%cpcm
  SMD true
  SMDSolvent "water"
  StateSpecificSolvation true
end
%tddft
  n_roots 10
  DoNTOs true
  PrintNTOs true
end
* xyzfile 0 1 ../S0_opt/BODIPY_Ph_S0_water_opt.xyz
```

**Remplacer** `wB97X-D` par chaque fonctionnelle :
- `wB97X-D` → ωB97X-D
- `CAM-B3LYP` → CAM-B3LYP
- `PBE0` → PBE0
- `B3LYP` → B3LYP
- `M06-2X` → M06-2X
- `MN15` → MN15

---

## 3. Script de génération automatique des inputs

```python
#!/usr/bin/env python3
# scripts/generate_tddft_inputs.py

import os

molecules = ["BODIPY_Ph", "BODIPY_Ph_NO2", "BODIPY_Ph_NH2",
             "Iodo_BODIPY", "Iodo_BODIPY_NO2", "Iodo_BODIPY_NH2",
             "TPP_Iodo_BODIPY", "aza_BODIPY_NO2"]

functionals = ["wB97X-D", "CAM-B3LYP", "PBE0", "B3LYP", "M06-2X", "MN15"]

template = """! RKS {func} def2-SVP AutoAux RIJCOSX TightSCF
! CPCM(water)
%pal nprocs 4 end
%maxcore 7000
%cpcm
  SMD true
  SMDSolvent "water"
  StateSpecificSolvation true
end
%tddft
  n_roots 10
  DoNTOs true
end
* xyzfile 0 1 ../../tier0_xtb/{mol}_S0_T0_opt.xyz
"""

for func in functionals:
    os.makedirs(f"calculations/tier2_tddft/{func}", exist_ok=True)
    for mol in molecules:
        fname = f"calculations/tier2_tddft/{func}/{mol}_T2_{func}.inp"
        with open(fname, "w") as f:
            f.write(template.format(func=func, mol=mol))
        print(f"Créé : {fname}")
```

```bash
python scripts/generate_tddft_inputs.py
```

---

## 4. Lancer les calculs en parallèle

```bash
# Lancer 4 jobs simultanément (4 cœurs chacun = 16 cœurs total)
# Adapter selon votre machine

for func in wB97X-D CAM-B3LYP PBE0 B3LYP; do
    orca calculations/tier2_tddft/${func}/BODIPY_Ph_T2_${func}.inp \
         > calculations/tier2_tddft/${func}/BODIPY_Ph_T2_${func}.out &
done
wait
echo "Batch 1 terminé"

for func in M06-2X MN15; do
    orca calculations/tier2_tddft/${func}/BODIPY_Ph_T2_${func}.inp \
         > calculations/tier2_tddft/${func}/BODIPY_Ph_T2_${func}.out &
done
wait
echo "Batch 2 terminé"
```

---

## 5. Parser les résultats

```python
#!/usr/bin/env python3
# scripts/parse_tddft_results.py

import re, os, csv

def extract_lambda_max(outfile):
    """Extrait λ_max (nm) et f du premier état excité."""
    with open(outfile) as f:
        content = f.read()
    # Chercher le tableau d'absorption
    pattern = r'(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)'
    matches = re.findall(pattern, content)
    if matches:
        # Premier état avec f > 0.01
        for state, energy_cm, wavelength, fosc in matches:
            if float(fosc) > 0.01:
                return float(wavelength), float(fosc)
    return None, None

functionals = ["wB97X-D", "CAM-B3LYP", "PBE0", "B3LYP", "M06-2X", "MN15"]
molecules   = ["BODIPY_Ph", "Br_BODIPY", "I_BODIPY"]

results = []
for mol in molecules:
    row = {"molecule": mol}
    for func in functionals:
        outfile = f"calculations/tier2_tddft/{func}/{mol}_T2_{func}.out"
        if os.path.exists(outfile):
            lmax, fosc = extract_lambda_max(outfile)
            row[f"lmax_{func}"] = lmax
            row[f"fosc_{func}"] = fosc
    results.append(row)

# Sauvegarder
with open("results/TDDFT_benchmark.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)

print("Résultats sauvegardés dans results/TDDFT_benchmark.csv")
```

---

## 6. Calculer les métriques de benchmark

```python
#!/usr/bin/env python3
# scripts/benchmark_metrics.py

import pandas as pd
import numpy as np

# Charger résultats calculés
calc = pd.read_csv("results/TDDFT_benchmark.csv")

# Données expérimentales
exp = {"BODIPY_Ph": 505, "Br_BODIPY": 535, "I_BODIPY": 545}

functionals = ["wB97X-D", "CAM-B3LYP", "PBE0", "B3LYP", "M06-2X", "MN15"]

print(f"{'Fonctionnelle':<15} {'MAE (nm)':>10} {'RMSE (nm)':>10} {'MAE (eV)':>10}")
print("-" * 50)

for func in functionals:
    errors = []
    for mol, lmax_exp in exp.items():
        row = calc[calc["molecule"] == mol]
        if not row.empty and f"lmax_{func}" in row.columns:
            lmax_calc = row[f"lmax_{func}"].values[0]
            if lmax_calc:
                errors.append(lmax_calc - lmax_exp)

    if errors:
        mae_nm  = np.mean(np.abs(errors))
        rmse_nm = np.sqrt(np.mean(np.array(errors)**2))
        # Conversion nm → eV à ~650 nm : 1 nm ≈ 0.003 eV
        mae_ev  = mae_nm * 1240 / (650**2)
        print(f"{func:<15} {mae_nm:>10.1f} {rmse_nm:>10.1f} {mae_ev:>10.3f}")
```

---

## 7. Critères de sélection de la meilleure fonctionnelle

| Critère | Seuil | Signification |
|---------|-------|---------------|
| MAE | < 0.2 eV (< ~20 nm à 650 nm) | Précision acceptable |
| RMSE | < 0.25 eV | Pas d'erreurs aberrantes |
| R² | > 0.90 | Bonne corrélation calc/exp |
| Biais systématique | < ±0.1 eV | Pas de décalage systématique |

**Si plusieurs fonctionnelles passent les critères** : choisir celle avec le MAE le plus bas. En cas d'égalité, préférer ωB97X-D (meilleure pour les états CT).

**Si aucune fonctionnelle ne passe** (MAE > 0.3 eV pour toutes) : c'est un résultat scientifique en soi — documenter et discuter dans le mémoire.

---

## 8. Livrable

- `results/TDDFT_benchmark.csv` — λ_max calculé pour toutes les fonctionnelles
- `results/functional_benchmark.md` — analyse, parity plots, recommandation
- Figure : parity plot (λ_max calculé vs expérimental) pour les 6 fonctionnelles
