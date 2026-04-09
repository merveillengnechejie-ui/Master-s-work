# Troubleshooting T1 — SCF ne Converge Pas
## Diagnostic et solutions par ordre d'escalade

---

## Symptômes

Dans le fichier `.out` ORCA, vous voyez :
```
*** ORCA SCF FAILED TO CONVERGE AFTER 500 ITERATIONS ***
```
ou
```
Energy change      :  0.123456789  (threshold: 1e-08)
Max gradient       :  0.987654321  (threshold: 1e-05)
```
(les valeurs oscillent sans diminuer)

---

## Diagnostic rapide

```bash
# Chercher les signes de non-convergence
grep -E "FAILED|not converged|oscillat" votre_calcul.out

# Voir l'évolution de l'énergie SCF
grep "ITER" votre_calcul.out | tail -20
```

Si l'énergie oscille (monte et descend alternativement) → problème de convergence SCF classique.

---

## Niveau 1 : Augmenter l'amortissement (le plus souvent suffisant)

```orca
%scf
  DampFac    0.7    # Amortissement (défaut ~0.5)
  DampErr    0.05   # Seuil pour désactiver l'amortissement
  MaxIter    500
end
```

---

## Niveau 2 : Changer l'algorithme SCF

```orca
%scf
  SCF_ALGORITHM DIIS_TRAH   # Plus robuste que DIIS standard
  TRAH_MaxDim 20
  MaxIter 500
end
```

---

## Niveau 3 : Level Shift

```orca
%scf
  LevelShift    0.3    # Décale les orbitales virtuelles vers le haut
  LevelShiftErr 0.01   # Seuil pour désactiver le shift
  MaxIter 500
end
```

---

## Niveau 4 : Combinaison robuste (pour les cas difficiles)

```orca
%scf
  SCF_ALGORITHM DIIS_TRAH
  TRAH_MaxDim 20
  DampFac 0.7
  LevelShift 0.5
  MaxIter 500
  ConvForce 1e-5    # Critère légèrement assoupli
end
```

---

## Niveau 5 : Changer le guess initial

```orca
# Option A : guess Hückel (plus simple que le défaut)
%scf
  Guess Huckel
end

# Option B : guess depuis un calcul précédent
%moinp "calcul_precedent.gbw"
```

---

## Niveau 6 : Réduire la base

Si le problème persiste avec def2-TZVP, essayer def2-SVP :
```orca
! RKS PBE0 def2-SVP ...  # au lieu de def2-TZVP
```

---

## Cas spécial : T₁ (UKS) ne converge pas

Pour les calculs triplet (multiplicité 3), ajouter :

```orca
%scf
  HFTyp UKS
  SCF_ALGORITHM DIIS_TRAH
  DampFac 0.7
  LevelShift 0.3
  MaxIter 500
end
* xyz 0 3   ← multiplicité 3 !
```

Vérifier aussi que `<S²>` est raisonnable :
```bash
grep "S\*\*2" votre_calcul.out
# Doit donner ~2.0 pour un triplet pur
# Si > 2.1 → contamination de spin → utiliser ROKS
```

---

## Cas spécial : S₁ ΔSCF s'effondre vers S₀

Voir [`T2_S1_effondrement.md`](T2_S1_effondrement.md) — ce cas est traité séparément car il nécessite une stratégie différente.

---

## Tableau de décision

| Symptôme | Action |
|----------|--------|
| Énergie oscille | Niveau 1 : augmenter DampFac |
| Énergie diverge | Niveau 2 : DIIS_TRAH |
| Convergence très lente | Niveau 3 : LevelShift |
| Rien ne marche | Niveau 4 : combinaison + réduire base |
| T₁ `<S²>` > 2.1 | Passer à ROKS |
| S₁ retombe sur S₀ | Voir T2_S1_effondrement.md |

---

## Règle des 3 tentatives

Après 3 tentatives avec escalade → passer à la molécule suivante et documenter l'échec dans le mémoire. Un échec de convergence est un résultat scientifique valide s'il est bien documenté.
