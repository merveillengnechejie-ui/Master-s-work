# Protocole P2 — Construction des Molécules et Pré-optimisation xTB
## Semaine 2

---

## 1. Construire les géométries avec Avogadro

Avogadro est un éditeur moléculaire gratuit (https://avogadro.cc).

**Étapes pour chaque molécule** :
1. Ouvrir Avogadro → Dessiner le squelette BODIPY
2. Ajouter les substituants (NO₂, NH₂, I, TPP⁺)
3. Optimisation rapide avec le champ de force MMFF94 (Extensions → Optimize Geometry)
4. Exporter en `.xyz` (File → Export → Molecule → .xyz)

**Ordre recommandé** : Commencer par BODIPY-Ph (le plus simple), puis ajouter les substituants progressivement.

---

## 2. Pré-optimisation GFN2-xTB

```bash
# Pour chaque molécule :
xtb BODIPY_Ph.xyz --opt tight --gfn 2 --alpb water > xTB_BODIPY_Ph.out

# Vérifier la convergence :
grep "GEOMETRY OPTIMIZATION CONVERGED" xTB_BODIPY_Ph.out
# Doit afficher : "GEOMETRY OPTIMIZATION CONVERGED"

# La géométrie optimisée est dans :
# xtbopt.xyz → renommer en BODIPY_Ph_S0_T0_opt.xyz
mv xtbopt.xyz calculations/tier0_xtb/BODIPY_Ph_S0_T0_opt.xyz
```

**Script batch** :
```bash
#!/bin/bash
# run_xtb_all.sh
molecules=("BODIPY_Ph" "BODIPY_Ph_NO2" "BODIPY_Ph_NH2"
           "Iodo_BODIPY" "Iodo_BODIPY_NO2" "Iodo_BODIPY_NH2"
           "TPP_Iodo_BODIPY" "aza_BODIPY_NO2")

for mol in "${molecules[@]}"; do
    echo "Optimisation xTB : $mol"
    cd calculations/tier0_xtb/
    xtb ../../data/${mol}.xyz --opt tight --gfn 2 --alpb water \
        > xTB_${mol}.out 2>&1
    mv xtbopt.xyz ${mol}_S0_T0_opt.xyz
    cd ../..
done
echo "Terminé."
```

---

## 3. Extraire les propriétés xTB

```bash
# HOMO-LUMO gap
grep "HOMO-LUMO GAP" xTB_BODIPY_Ph.out

# Dipôle
grep "molecular dipole" xTB_BODIPY_Ph.out -A 3

# Énergie totale
grep "TOTAL ENERGY" xTB_BODIPY_Ph.out | tail -1
```

Remplir `results/xTB_screening.csv` :
```
molecule,E_total_Eh,HOMO_eV,LUMO_eV,gap_eV,dipole_D,converged
BODIPY_Ph,...
```

---

## 4. Construire experimental_benchmark.csv

```csv
molecule,lambda_max_exp_nm,solvent,phi_f,phi_delta,source
BODIPY_Ph,505,DMSO,0.80,,Sandoval_2023
Br_BODIPY,535,CH2Cl2,0.45,0.35,Ponte_2018
I_BODIPY,545,CH2Cl2,0.02,0.99,Baig_2024
BODIPY_dimer,680,DMSO,0.15,,Porolnik_2024
```

> **Important** : Vérifier chaque valeur dans l'article original avant de l'utiliser. Ne jamais copier des valeurs sans les avoir lues dans la source primaire.
