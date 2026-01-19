# Protocole de Convergence de l'État S₁ (OO-DFT)

Ce document détaille le protocole technique utilisé pour atteindre la convergence de l'état excité singulet ($S_1$) en utilisant la méthode Orbital-Optimized DFT (OO-DFT) dans ORCA 6.1.

## 1. Analyse de la Configuration Électronique

Avant de lancer le calcul de l'état excité, il est crucial d'identifier correctement les orbitales frontières (HOMO/LUMO).
- **Correction ECP** : Pour les molécules contenant de l'iode (Iodo-BODIPY), le calcul de l'indice HOMO doit soustraire les 28 électrons de cœur remplacés par le pseudopotentiel (Def2-ECP).
- **Indices** : L'indice HOMO est calculé comme $(N_{électrons} / 2) - 1$ (base 0).

## 2. Génération du Guess (Rotation d'Orbitales)

L'état $S_1$ est initialisé en effectuant une rotation d'orbitales pour simuler une transition électronique.
- **Paramètre** : `Rotate {i, j, 90, 1, 1}`
- **Signification** : Une rotation de 90° entre l'orbitale occupée $i$ et l'orbitale virtuelle $j$ crée un état mixte "open-shell singlet-like", idéal comme point de départ pour l'optimisation OO-DFT.
- **Stratégies testées** :
  - $HOMO \to LUMO$ (Transition standard)
  - $HOMO-1 \to LUMO$ (Si mélange d'orbitales)
  - $HOMO \to LUMO+1$

## 3. Techniques de Convergence SCF

La convergence des états excités est souvent instable. Les paramètres suivants sont appliqués pour stabiliser le cycle SCF :
- **AutoTRAH** : `AutoTRAH true` active l'algorithme Trust Radius Augmented Hessian, plus robuste que le DIIS standard pour les cas difficiles.
- **Level Shifting** : `LevelShift 0.2` décale virtuellement les énergies des orbitales pour éviter les oscillations.
- **Damping** : `CNVDamp true` et `DampFac 0.7` amortissent les variations de la matrice de Fock entre les itérations.
- **SlowConv** : Utilisation de grilles et de critères plus lents mais plus sûrs.

## 4. Préservation de l'État Excité (MOM)

Pour éviter que le système ne "retombe" vers l'état fondamental ($S_0$) pendant l'optimisation :
- **Maximum Overlap Method** : `DoMOM true` force ORCA à sélectionner les orbitales qui ont le plus grand recouvrement avec le guess initial à chaque itération.

## 5. Algorithme de Sélection du Meilleur État

Le protocole automatise l'exécution des différentes stratégies de rotation et sélectionne l'état final selon deux critères :
1. **Convergence** : Le calcul doit afficher `SCF CONVERGED`.
2. **Énergie Minimale** : Parmi les états convergés, celui ayant l'énergie totale la plus basse est retenu comme l'état $S_1$ le plus stable physiquement.

---
*Ce protocole est implémenté via le script `gen_s1_guesses.sh` dans le dossier `OO-DFT`.*
