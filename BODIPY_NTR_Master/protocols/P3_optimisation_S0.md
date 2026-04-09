# Protocole P3 — Optimisation de l'État Fondamental S₀
## Semaine 3

---

## 1. Input ORCA — S₀ phase gaz

```orca
# calculations/S0_opt/BODIPY_Ph_S0_gas.inp

! Opt RKS B3LYP D3BJ def2-SVP AutoAux RIJCOSX TightSCF TIGHTOPT
%pal nprocs 4 end
%maxcore 7000
%scf
  MaxIter 500
  ConvForce 1e-6
end
%geom
  MaxStep 0.2
  Trust 0.3
end
* xyzfile 0 1 ../tier0_xtb/BODIPY_Ph_S0_T0_opt.xyz
```

---

## 2. Input ORCA — S₀ en solution (SMD water)

```orca
# calculations/S0_opt/BODIPY_Ph_S0_water.inp

! Opt RKS B3LYP D3BJ def2-SVP AutoAux RIJCOSX TightSCF TIGHTOPT
! CPCM(water)
%pal nprocs 4 end
%maxcore 7000
%cpcm
  SMD true
  SMDSolvent "water"
end
%scf
  MaxIter 500
  ConvForce 1e-6
end
%geom
  MaxStep 0.2
  Trust 0.3
end
* xyzfile 0 1 BODIPY_Ph_S0_gas.xyz
```

**Ordre** : Toujours optimiser en phase gaz d'abord, puis utiliser cette géométrie comme point de départ pour l'optimisation en solution.

---

## 3. Vérification de la convergence

```bash
# Vérifier la convergence géométrique
grep "GEOMETRY OPTIMIZATION CONVERGED" BODIPY_Ph_S0_water.out

# Vérifier l'absence de fréquences imaginaires (optionnel mais recommandé)
# Ajouter "Freq" au mot-clé si doute :
# ! Opt Freq RKS B3LYP ...
grep "imaginary" BODIPY_Ph_S0_water.out
# Ne doit rien afficher (pas de fréquences imaginaires)

# Extraire la géométrie finale
grep -A 5 "CARTESIAN COORDINATES (ANGSTROEM)" BODIPY_Ph_S0_water.out | tail -60
# OU utiliser le fichier .xyz généré automatiquement
```

---

## 4. Lancer les 8 molécules en parallèle

```bash
#!/bin/bash
# run_S0_opt.sh

molecules=("BODIPY_Ph" "BODIPY_Ph_NO2" "BODIPY_Ph_NH2" "Iodo_BODIPY")

# Batch 1 : 4 molécules en parallèle (phase gaz)
for mol in "${molecules[@]}"; do
    orca calculations/S0_opt/${mol}_S0_gas.inp \
         > calculations/S0_opt/${mol}_S0_gas.out &
done
wait
echo "Batch gaz terminé"

# Batch 2 : 4 molécules en parallèle (eau)
for mol in "${molecules[@]}"; do
    orca calculations/S0_opt/${mol}_S0_water.inp \
         > calculations/S0_opt/${mol}_S0_water.out &
done
wait
echo "Batch eau terminé"
```

---

## 5. Extraire les géométries optimisées

```bash
# ORCA génère automatiquement un fichier .xyz avec la géométrie finale
# Il s'appelle : nom_du_calcul.xyz

# Renommer selon la convention
mv calculations/S0_opt/BODIPY_Ph_S0_water.xyz \
   calculations/S0_opt/BODIPY_Ph_S0_water_opt.xyz
```

---

## 6. Livrable

- `calculations/S0_opt/BODIPY_Ph_S0_water_opt.xyz` (et .gbw) pour les 8 molécules
- Tableau de vérification dans `JOURNAL_DE_BORD.md` (semaine 3)
