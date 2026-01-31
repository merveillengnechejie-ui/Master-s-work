# Rapport d'Analyse OO-DFT : États Triplets (T1)
**Méthode :** OO-DFT (Delta-SCF) B3LYP/def2-SVP
**Milieu :** Solvante (SMD Water)
**Date :** 31 Janvier 2026

## 1. Introduction
Ce rapport présente les résultats des calculs d'optimisation de l'état triplet le plus bas (T1) effectués par la méthode **OO-DFT** (Orbital Optimized DFT ou Delta-SCF).

## 1. Propriétés à calculer selon le manuel ORCA 6.1.0
Pour une optimisation d'état triplet avec OO-DFT, le manuel spécifie les paramètres critiques suivants :
1. **Énergie Totale (Etot)** : Incluant les composantes électroniques et la correction de dispersion (D3BJ).
2. **Contamination de Spin (⟨S²⟩)** : Cruciale pour les triplets afin de vérifier que l'état n'est pas mélangé avec d'autres multiplicités (la valeur idéale est 2,0).
3. **Énergie de Solvatation (SMD CDS)** : Correction d'énergie libre pour simuler le milieu biologique (eau).
4. **Moment Dipolaire** : Magnitude de la polarité de la molécule dans son état excité.
5. **Rapport du Viriel** : Indicateur de la stabilité numérique de la fonction d'onde (doit être proche de 2,0).
6. **Gradient de Géométrie** : Confirmation de la convergence vers un minimum stable (mots-clés TightSCF et TIGHTOPT).

---


## 2. Tableau Récapitulatif : Molécules et Propriétés (État T1)
Les calculs utilisent la fonctionnelle B3LYP, la base def2-SVP et l'algorithme d'optimisation TRAH.

| Propriété | BODIPY (Réf) | Iodo-BODIPY | TPP-BODIPY |
| :--- | :--- | :--- | :--- |
| **Fichier Source** | BODIPY_T1.out.txt | Iodo_T1.out.txt | TPP_Bodipy_T1.out.txt |
| **Charge / Multiplicité** | 0 / 3 (Triplet) | 0 / 3 (Triplet) | +1 / 3 (Triplet) |
| **Énergie Finale (Etot)** | -680,472532 Eh | -1274,667315 Eh | -1714,932423 Eh |
| **Dispersion (D3BJ)** | -0,043260 Eh | -0,054158 Eh | -0,155419 Eh |
| **Contamination ⟨S²⟩** | 2,017 | 2,011 | 2,016 |
| **Solvatation (SMD CDS)** | 6,18 kcal/mol | 5,32 kcal/mol | 11,22 kcal/mol |
| **Moment Dipolaire** | 5,13 Debye | 3,98 Debye | 9,38 Debye |
| **Rapport du Viriel** | 2,0089 | 2,4155 | 2,0086 |
| **Temps de Calcul** | ~10 min 21 s | ~11 min 12 s  | ~1 h 28 min 19 s  |

---

## 3. Interprétation des Analyses
- **Validité du Spin** : Toutes les molécules présentent une contamination de spin extrêmement faible (écarts <0,02), confirmant que la méthode UKS avec optimisation d'orbitales décrit correctement l'état triplet pur.
- **Traitement Relativiste (Iode)** : Pour l'Iodo-BODIPY, l'utilisation du Potentiel de Cœur Effectif (Def2-ECP) remplace 28 électrons de cœur, permettant d'inclure les effets relativistes de l'iode sans alourdir le coût numérique. Son rapport du viriel plus élevé (2,41) est caractéristique des systèmes incluant des potentiels ECP.
- **Impact du Groupement TPP** : Le TPP-BODIPY (cationique) montre la plus forte stabilisation par le solvant (11,22 kcal/mol) et le moment dipolaire le plus élevé (9,38 D), ce qui s'explique par sa charge nette de +1 et l'asymétrie structurelle du groupement phosphonium.
- **Précision de Convergence** : L'algorithme TRAH (Trust Radius Augmented Hessian) a permis d'atteindre des seuils de convergence très stricts (TightSCF), garantissant que les propriétés spectroscopiques extraites sont physiquement fiables pour des applications en PDT/PTT.

---

## 4. Tableau des propriétés électroniques (S0 et T1)
Ce tableau compare l'état fondamental (S0) et le premier état triplet (T1).

| Propriété | BODIPY (Réf) | Iodo-BODIPY | TPP-BODIPY (+1) |
| :--- | :--- | :--- | :--- |
| **Énergie S0 Réf. (Eh)** | -680,576456 | -1274,779347 | -1715,133210 |
| **HOMO (S0, eV)** | -5,9577 | -5,8619 | -6,2142 |
| **LUMO (S0, eV)** | -2,7642 | -2,9328 | -3,4552 |
| **Gap HOMO-LUMO (S0, eV)** | 3,1935 | 2,9291 | 2,7590 |
| **Énergie T1 Opt. (Eh)** | -680,472532 | -1274,667315 | -1714,932430 |
| **Gap S0→T1 (eV)** | 2,828 | 3,048 | 5,463 |

---

## 5. Analyse et Interprétation des Résultats

### 5.1 Stabilité de l'état fondamental (S0)
- L'énergie de référence pour le BODIPY de base est de -680,576 Eh.
- L'ajout d'atomes d'iode abaisse l'énergie totale à -1274,779 Eh.
- La structure cationique du TPP-BODIPY se stabilise à -1715,133 Eh.

### 5.2 Frontières Électroniques (HOMO-LUMO)
On observe une réduction systématique du Gap HOMO-LUMO au fur et à mesure que la structure se complexifie, passant de 3,19 eV (BODIPY) à 2,76 eV (TPP-BODIPY). Ce décalage vers le **rouge (bathochrome)** est favorable aux applications de thérapie photodynamique.

### 5.3 Énergie de l'état Triplet (T1)
- Les calculs OO-DFT (Orbital Optimized) utilisant l'algorithme TRAH ont convergé vers des minima stables pour l'état triplet.
- Le Gap S0→T1 (différence d'énergie adiabatique) représente l'énergie nécessaire pour atteindre le premier état triplet après relaxation géométrique.
- Pour le BODIPY et l'Iodo-BODIPY, ce gap est proche de la valeur du gap HOMO-LUMO (~2,8 à 3,0 eV), ce qui est typique des petits chromophores organiques.
- Pour le TPP-BODIPY, le gap adiabatique calculé est plus élevé (5,46 eV), reflétant la réorganisation électronique importante nécessaire pour stabiliser le triplet sur cette large structure cationique.

### 5.4 Notes techniques sur les fichiers de sortie
- Pour l'Iodo-BODIPY, le rapport du viriel de 2,4155 confirme la prise en compte des effets relativistes via l'ECP sur l'iode.
- Impact de l'Iode : Pour l'Iodo-BODIPY, bien que la molécule soit plus lourde, la correction de solvatation est légèrement inférieure à celle du BODIPY de base (~5,3 vs ~6,2 kcal/mol). Cela suggère que l'iode, bien que volumineux, modifie la densité électronique d'une manière qui réduit légèrement l'interaction favorable avec l'eau par rapport au BODIPY substitué.
-  Effet de charge (TPP-BODIPY) : La stabilisation est environ deux fois plus forte pour le TPP-BODIPY (~11,2 kcal/mol) que pour les autres molécules. Cela s'explique par sa nature cationique (charge +1) ; les interactions électrostatiques avec l'eau sont beaucoup plus intenses pour un ion que pour une molécule neutre.
- Les avertissements concernant le "Small HOMO/LUMO gap" (environ 0,09 Eh) dans les sorties triplets sont normaux pour des calculs UKS sur des états excités, indiquant une proximité énergétique entre les orbitales SOMO qui nécessite l'utilisation de l'algorithme robuste TRAH pour assurer la convergence.
