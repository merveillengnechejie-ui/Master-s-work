# Protocole P6 — Δ-DFT ΔE_ST et Couplage Spin-Orbite (SOC)
## Semaine 7

---

## 1. Calcul ΔE_ST par ΔROKS

### Étape A : Optimisation T₁ (UUKS, équilibre)

L'optimisation géométrique de T₁ utilise la **solvation à l'équilibre** (le solvant se relaxe avec la géométrie) :

```orca
# calculations/T1_opt/Iodo_BODIPY_NH2_T1_opt.inp

! Opt UKS PBE0 D3BJ def2-SVP AutoAux RIJCOSX TightSCF TIGHTOPT
! CPCM(water)
%pal nprocs 4 end
%maxcore 7000
%cpcm
  SMD true
  SMDSolvent "water"
  # PAS de StateSpecificSolvation ici : c'est une optimisation, pas une excitation
end
%scf
  HFTyp UKS
  SCF_ALGORITHM DIIS_TRAH
  MaxIter 500
  ConvForce 1e-6
end
%geom
  MaxStep 0.2
  Trust 0.3
end
* xyz 0 3
[Coordonnées de S0_water_opt.xyz]
*
```

### Étape B : Énergie T₁ point fixe (ΔROKS, non-équilibre)

Une fois la géométrie T₁ optimisée, on calcule l'énergie avec **ptSS-PCM non-équilibre** pour la cohérence avec ΔE_ST :

```orca
# calculations/tier25_deltadft/Iodo_BODIPY_NH2_T1_ROKS.inp

! ROKS PBE0 D3BJ def2-SVP AutoAux RIJCOSX TightSCF
! CPCM(water)
%pal nprocs 4 end
%maxcore 7000
%cpcm
  SMD true
  SMDSolvent "water"
  StateSpecificSolvation true   # non-équilibre pour l'énergie finale
end
%scf
  HFTyp ROKS
  SCF_ALGORITHM DIIS_TRAH
  MaxIter 500
end
* xyzfile 0 3 ../T1_opt/Iodo_BODIPY_NH2_T1_opt.xyz
```

### Input S₀ énergie (RKS, équilibre)

```orca
# calculations/tier25_deltadft/Iodo_BODIPY_NH2_S0_RKS.inp

! RKS PBE0 D3BJ def2-SVP AutoAux RIJCOSX TightSCF
! CPCM(water)
%pal nprocs 4 end
%maxcore 7000
%cpcm
  SMD true
  SMDSolvent "water"
end
* xyzfile 0 1 ../S0_opt/Iodo_BODIPY_NH2_S0_water_opt.xyz
```

### Calcul de ΔE_ST

```python
# Dans les fichiers .out, chercher :
# "FINAL SINGLE POINT ENERGY"

# E(S₀) depuis S0_RKS.out
# E(T₁) depuis T1_ROKS.out

# ΔE_ST = E(T₁) - E(S₀)  en Hartree → convertir en eV (× 27.2114)
delta_E_ST_eV = (E_T1_Eh - E_S0_Eh) * 27.2114
```

---

## 2. Calcul SOC (ΔDFT+SOC perturbatif)

```orca
# calculations/soc/Iodo_BODIPY_NH2_SOC.inp

! UKS PBE0 D3BJ def2-SVP ZORA AutoAux RIJCOSX TightSCF
! CPCM(water)
%pal nprocs 4 end
%maxcore 7000
%cpcm
  SMD true
  SMDSolvent "water"
end
%scf
  HFTyp UKS
  SCF_ALGORITHM DIIS_TRAH
  MaxIter 500
end
%tddft
  dosoc true
  SOCROTs 20
  n_roots 5
end
* xyzfile 0 1 ../S0_opt/Iodo_BODIPY_NH2_S0_water_opt.xyz
```

### Extraire les constantes SOC

```bash
grep -A 20 "Spin-Orbit Coupling" Iodo_BODIPY_NH2_SOC.out | grep "S1\|T1\|cm"
```

Chercher des lignes comme :
```
  S1 <-> T1 :   87.3 cm-1
```

---

## 3. Analyse MEP pour TPP-Iodo-BODIPY (Multiwfn)

Pour générer les charges Hirshfeld, ajouter dans l'input ORCA de S₀ :

```orca
# Ajouter dans l'input S₀ de TPP_Iodo_BODIPY :
%output
  Print[P_Hirshfeld] 1
  Print[P_Mayer] 1
end
```

Puis lancer Multiwfn sur le fichier `.out` :

```bash
multiwfn calculations/S0_opt/TPP_Iodo_BODIPY_S0_water.out

# Dans le menu interactif Multiwfn :
# 7  → Population analysis and atomic charges
# 11 → Hirshfeld charge
# 0  → Quitter

# Chercher dans la sortie :
# Atom  P  (phosphore du TPP) : charge ≈ +0.3 à +0.5 e
# La charge totale du fragment TPP doit être ≈ +1.0 e
```

**Critères de ciblage mitochondrial** :
- Charge totale TPP⁺ ≥ +0.8 e (localisée sur le fragment phosphonium)
- Distance TPP⁺ → centre BODIPY > 5 Å (exposition en surface)
- Visualiser le potentiel électrostatique (MEP) avec VMD ou Avogadro

---

## 4. Livrable

- `results/deltaDFT_results.csv` : ΔE_ST Δ-DFT pour toutes les molécules ON+OFF
- `results/SOC_results.csv` : constantes SOC (cm⁻¹)
- Rapport ciblage TPP-Iodo-BODIPY (charges Hirshfeld)
