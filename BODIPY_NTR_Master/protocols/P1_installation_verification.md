# Protocole P1 — Installation et Vérification de la Chaîne de Calcul
## Semaine 1 — À faire avant tout calcul

---

## Checklist semaine 1

- [ ] ORCA 6.1.1 installé et testé
- [ ] xTB 6.6 installé
- [ ] RDKit 2024 installé
- [ ] Multiwfn 3.8+ installé
- [ ] Python 3.10+ avec packages
- [ ] Bug `SMDSolvent "mixed"` corrigé dans les anciens inputs
- [ ] CC2 disponibilité vérifiée dans ORCA 6.1.1
- [ ] sTDA disponibilité vérifiée dans ORCA 6.1.1
- [ ] Test de chaîne complet sur BODIPY-Ph de référence
- [ ] Convention de nommage documentée
- [ ] `.gitignore` créé
- [ ] Structure de répertoires créée

---

## 1. Installation ORCA 6.1.1

```bash
# Télécharger depuis : https://orcaforum.kofo.mpg.de
# (inscription gratuite requise)

# Décompresser
tar -xzf orca_6_1_1_linux_x86-64_shared_openmpi416.tar.gz

# Ajouter au PATH (dans ~/.bashrc)
export PATH="/chemin/vers/orca_6_1_1:$PATH"
export LD_LIBRARY_PATH="/chemin/vers/orca_6_1_1:$LD_LIBRARY_PATH"

# Tester
orca --version
# Doit afficher : ORCA version 6.1.1
```

---

## 2. Installation xTB 6.6

```bash
conda install -c conda-forge xtb
# OU
pip install xtb

# Tester
xtb --version
# Doit afficher : xtb version 6.6.x
```

---

## 3. Installation Python et packages

```bash
# Créer l'environnement conda
conda create -n bodipy_ntr python=3.10
conda activate bodipy_ntr

# Installer les packages
conda install -c conda-forge rdkit
pip install scikit-learn matplotlib pandas numpy

# Sauvegarder l'environnement
conda env export > environment.yml
```

---

## 4. Vérification critique : sTDA dans ORCA 6.1.1

Créer le fichier `test_stda.inp` :

```orca
! RKS PBE0 def2-SVP AutoAux RIJCOSX TightSCF
! STDA
! CPCM(water)
%pal nprocs 4 end
%maxcore 6000
%cpcm
  SMD true
  SMDSolvent "water"
end
%tddft
  n_roots 5
end
* xyz 0 1
C  0.000  0.000  0.000
H  0.629  0.629  0.629
H -0.629 -0.629  0.629
H -0.629  0.629 -0.629
H  0.629 -0.629 -0.629
*
```

```bash
orca test_stda.inp > test_stda.out

# Vérifier dans test_stda.out :
grep "STDA" test_stda.out
# Si "sTDA" apparaît → disponible ✓
# Si "keyword not recognized" → utiliser ! TDDFT TDA true à la place
```

---

## 5. Vérification critique : CC2 dans ORCA 6.1.1

```orca
# test_cc2.inp
! RHF def2-SVP TightSCF
%pal nprocs 4 end
%maxcore 6000
%mdci
  Method CC2
  NRoots 3
end
* xyz 0 1
C  0.000  0.000  0.000
H  0.629  0.629  0.629
H -0.629 -0.629  0.629
H -0.629  0.629 -0.629
H  0.629 -0.629 -0.629
*
```

```bash
orca test_cc2.inp > test_cc2.out
grep -i "cc2\|error\|not available" test_cc2.out
```

**Résultat attendu** : Si CC2 est disponible, noter pour utilisation future dans le projet de publication.

---

## 6. Correction du bug SMDSolvent

```bash
# Chercher tous les anciens inputs avec "mixed"
grep -r "SMDSolvent" /chemin/vers/anciens/inputs/ | grep "mixed"

# Corriger automatiquement
find /chemin/vers/anciens/inputs/ -name "*.inp" \
  -exec sed -i 's/SMDSolvent "mixed"/SMDSolvent "water"/g' {} \;

# Vérifier
grep -r "SMDSolvent" /chemin/vers/anciens/inputs/
# Ne doit plus contenir "mixed"
```

---

## 7. Test de chaîne complet sur BODIPY-Ph

Télécharger ou construire la géométrie de BODIPY-Ph (disponible dans `../data/`).

```bash
# Étape 1 : xTB
xtb BODIPY_Ph.xyz --opt tight --gfn 2 --alpb water > xTB_BODIPY_Ph.out
# Vérifier : "GEOMETRY OPTIMIZATION CONVERGED" dans le .out

# Étape 2 : S₀ optimisation ORCA
orca S0_BODIPY_Ph.inp > S0_BODIPY_Ph.out
# Vérifier : "GEOMETRY OPTIMIZATION CONVERGED" + pas de fréquences imaginaires

# Étape 3 : TD-DFT vertical
orca TDDFT_BODIPY_Ph.inp > TDDFT_BODIPY_Ph.out
# Vérifier : λ_max calculé ≈ 505 nm (expérimental)
# Tolérance : ±30 nm acceptable pour def2-SVP
```

**Résultat attendu pour BODIPY-Ph** :
- λ_max expérimental : ~505 nm (DMSO)
- λ_max calculé TD-DFT/PBE0/def2-SVP : ~490–530 nm ✓

---

## 8. Convention de nommage des fichiers

```
Format : {molecule}_{state}_{tier}_{attempt}.{ext}

Exemples :
  BODIPY_Ph_S0_T0_opt.xyz          → xTB optimisé
  BODIPY_Ph_NO2_S0_T2_PBE0.inp    → TD-DFT PBE0, forme OFF
  Iodo_BODIPY_NH2_T1_T25_opt.gbw  → T₁ Δ-DFT, forme ON
  Iodo_BODIPY_S1_T25_attempt3.out → S₁ ΔSCF, 3ème tentative

Abréviations :
  T0  = Tier 0 (xTB)
  T1  = Tier 1 (sTDA)
  T2  = Tier 2 (TD-DFT)
  T25 = Tier 2.5 (Δ-DFT)
  SOC = calcul SOC
```

---

## 9. Créer le .gitignore

```bash
cat > .gitignore << 'EOF'
# Fichiers ORCA volumineux
*.gbw
*.tmp
*.densities
*.bigtmp
*.cis
*.mdci
*.trr
*.prop

# Fichiers temporaires
*.tmp.*
*_tmp/

# Grands fichiers de sortie (garder les .out importants)
# Ne pas ignorer les .out — ils contiennent les résultats !

# Environnements Python
__pycache__/
*.pyc
.ipynb_checkpoints/
EOF
```

---

## 10. Livrable de la semaine 1

Créer `SEMAINE1_RAPPORT_VALIDATION.md` avec :
- [ ] Versions de tous les logiciels installés
- [ ] Résultat du test sTDA (disponible/non)
- [ ] Résultat du test CC2 (disponible/non)
- [ ] λ_max calculé pour BODIPY-Ph (test de chaîne)
- [ ] Confirmation correction bug SMDSolvent
- [ ] Convention de nommage adoptée
