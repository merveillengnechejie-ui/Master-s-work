# Rapport d'Analyse DFT : Phase Gazeuse (Optimisation)
**Méthode :** DFT (B3LYP/def2-SVP) + D3BJ
**Logiciel :** ORCA 6.1.0
**Date :** 30 Janvier 2026

## 1. Introduction
Ce rapport synthétise les propriétés essentielles extraites des optimisations de géométrie en **phase gazeuse** pour la série BODIPY. Conformément au manuel ORCA 6.1.0 , ces calculs valident la structure électronique fondamentale avant l'inclusion des effets de solvant.

## 2. Tableau Récapitulatif Comparatif

| Propriété Calculée | BODIPY (Base) | Iodo-BODIPY | TPP-BODIPY |
| :--- | :---: | :---: | :---: |
| **Charge / Multiplicité** |   0 / 1 (Singulet) |  0 / 1 (Singulet) |  **+1 / 1 (Cation)** |
| **Nombre d'électrons ** | 98 | 146 (ECP) | 234 |
| **Énergie Totale (Etot)** | -680,567381 Eh | -1274,765556 Eh | -1715,063726 Eh |
| **Moment Dipolaire (D)** | 4,1126 Debye | 3,9981 Debye | **~8,82 Debye** |
| **HOMO (eV)** | -6,1546 eV | -6,2415 eV | -9,0158 eV |
| **LUMO (eV)** | -3,0495 eV | -3,4056 eV | -6,3233 eV |
| **Gap HOMO-LUMO (eV)** | **3,1051 eV** | **2,8359 eV** | **2,6925 eV** |
| **Valence Mayer (Hétéro)** | B : 4,24 | I : 1,11 | P : 4,23 |
| **État de Convergence** | Succès (13 cycles) | Succès (6 cycles) | Succès (12 cycles) |

## 3. Évaluation et Analyse Approfondie

### 3.1 Traitement de l'Iode et Effets Relativistes
Pour l'**Iodo-BODIPY**, l'utilisation du pseudo-potentiel **Def2-ECP** est cruciale. En remplaçant 28 électrons de cœur par atome d'iode, ORCA réduit le coût de calcul (NEL de 202 à 146) tout en intégrant les effets relativistes indispensables pour décrire correctement cet atome lourd. La valence de Mayer (1,11) confirme une liaison sigmatique stable.

### 3.2 Stabilité Électronique du TPP-BODIPY
L'utilisation d'une **charge +1** pour le TPP-BODIPY stabilise le système à 234 électrons. Cela permet une description en couche fermée (RKS Singulet), ce qui est cohérent avec la stabilité observée expérimentalement pour ces dérivés cationiques.

### 3.3 Polarité et Distribution de Charge
Le moment dipolaire du **TPP-BODIPY (~8,82 D)** est plus du double de celui de la base neutre. Cette forte polarisation est induite par le groupement tétraphénylphosphonium. Bien que déjà élevée en phase gazeuse, cette valeur augmentera significativement en solution (effet de polarisation du solvant).

### 3.4 Évolution du Gap et Propriétés Optiques
On observe une réduction monotone du Gap HOMO-LUMO :
- **Base :** 3,11 eV
- **Iodo :** 2,84 eV
- **TPP :** 2,69 eV 
Cette tendance bathochrome confirme que la fonctionnalisation par le TPP et l'iode déplace l'absorption vers le rouge, optimisant les molécules pour des applications comme la thérapie photodynamique (PDT).

## 4. Conclusion
Les optimisations en phase gazeuse ont toutes convergé avec succès, confirmant la validité des structures de départ. Le **TPP-BODIPY** se distingue par sa forte polarité et son gap réduit, tandis que l'**Iodo-BODIPY** est prêt pour les futures études de couplage spin-orbite (SOC) grâce à l'intégration correcte des effets relativistes via l'ECP.
