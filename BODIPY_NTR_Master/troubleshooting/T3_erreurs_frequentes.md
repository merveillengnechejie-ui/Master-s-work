# Troubleshooting T3 — Erreurs ORCA Fréquentes
## Référence rapide

---

## Erreur : "SMDSolvent not recognized" ou résultats phase gaz inattendus

**Cause** : `SMDSolvent "mixed"` est invalide dans ORCA 6.1.1.

**Solution** :
```orca
# FAUX
%cpcm
  SMDSolvent "mixed"
end

# CORRECT
%cpcm
  SMD true
  SMDSolvent "water"
end
```

---

## Erreur : "ORCA TERMINATED NORMALLY" mais λ_max aberrant

**Cause** : `StateSpecificSolvation true` oublié pour les excitations verticales.

**Solution** : Toujours ajouter pour TD-DFT et Δ-DFT excitations :
```orca
%cpcm
  SMD true
  SMDSolvent "water"
  StateSpecificSolvation true   ← obligatoire pour excitations
end
```

---

## Erreur : "Multiplicity and charge are not compatible"

**Cause** : Mauvaise combinaison charge/multiplicité.

**Règle** :
```
Molécule neutre, singulet  : * xyz 0 1
Molécule neutre, triplet   : * xyz 0 3
Molécule cationique (+1), singulet : * xyz 1 1
TPP-BODIPY (cation +1)    : * xyz 1 1
```

---

## Erreur : "No basis set found for element"

**Cause** : L'élément (ex: B, I) n'est pas couvert par la base choisie.

**Solution** : def2-SVP et def2-TZVP couvrent tous les éléments jusqu'à Kr (Z=36). Pour l'iode (Z=53), utiliser def2-SVP avec ZORA pour les effets relativistes :
```orca
! UKS PBE0 def2-SVP ZORA ...
```

---

## Erreur : "DIIS error too large"

**Cause** : Convergence SCF difficile.

**Solution** : Voir [`T1_convergence_SCF.md`](T1_convergence_SCF.md).

---

## Erreur : "Newton-Raphson step too large"

**Cause** : Pas géométrique trop grand pendant l'optimisation.

**Solution** :
```orca
%geom
  MaxStep 0.1    # Réduire de 0.2 à 0.1
  Trust 0.15
end
```

---

## Erreur : "Imaginary frequency found"

**Cause** : La géométrie optimisée n'est pas un minimum (c'est un point selle).

**Solution** :
1. Visualiser la fréquence imaginaire avec Avogadro (mode de vibration)
2. Déplacer légèrement la géométrie dans la direction du mode imaginaire
3. Relancer l'optimisation avec `TIGHTOPT`

---

## Erreur : "Out of memory" / "Cannot allocate"

**Cause** : `%maxcore` trop élevé ou calcul trop grand pour 32 GB RAM.

**Solution** :
```orca
# Réduire maxcore (laisser ~4 GB pour le système)
%maxcore 6000   # au lieu de 7500

# Pour les grandes molécules (TPP-Iodo-BODIPY ~90 atomes)
# Rester sur def2-SVP, ne pas passer à def2-TZVP
```

**Estimation RAM** :
- def2-SVP, ~60 atomes : ~4–6 GB
- def2-TZVP, ~60 atomes : ~8–12 GB
- def2-TZVP, ~90 atomes : ~16–24 GB ← limite de 32 GB

---

## Erreur : "STDA keyword not recognized"

**Cause** : sTDA non disponible dans votre version d'ORCA.

**Solution** : Utiliser TDA (Tamm-Dancoff Approximation) à la place :
```orca
# Au lieu de ! STDA
%tddft
  TDA true      # Active l'approximation Tamm-Dancoff
  n_roots 10
end
```

---

## Vérifications rapides après chaque calcul

```bash
# 1. Le calcul a-t-il terminé normalement ?
grep "ORCA TERMINATED NORMALLY" calcul.out

# 2. La géométrie a-t-elle convergé ?
grep "GEOMETRY OPTIMIZATION CONVERGED" calcul.out

# 3. Y a-t-il des fréquences imaginaires ?
grep "imaginary" calcul.out

# 4. Le SCF a-t-il convergé ?
grep "SCF CONVERGED" calcul.out

# 5. Quelle est l'énergie finale ?
grep "FINAL SINGLE POINT ENERGY" calcul.out | tail -1

# 6. Quel est le λ_max ?
grep "nm" calcul.out | grep -E "[0-9]{3}\.[0-9]" | head -5
```
