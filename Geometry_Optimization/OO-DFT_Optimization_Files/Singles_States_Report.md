# Rapport d'Analyse OO-DFT : BODIPY, Iodo-BODIPY et TPP-BODIPY

**Logiciel** : ORCA Version 6.1.0  
**Méthode** : OO-DFT (UKS B3LYP) avec correction de dispersion D3BJ et solvatation SMD (Eau)  

---

## 1. Introduction
Ce rapport présente une analyse croisée des optimisations de géométrie et des propriétés électroniques pour les molécules BODIPY (Référence), Iodo-BODIPY et TPP-BODIPY. L'étude se concentre sur l'identification des configurations électroniques les plus stables via la méthode **OO-DFT (Orbital Optimized DFT)**, en utilisant des rotations d'orbitales ("guesses") pour préparer les calculs d'états excités.

---

## 2. Extraction des Propriétés par Fichier de Test
Cette section résume les propriétés physiques extraites pour les différentes configurations électroniques testées.

## 2.1 BODIPY
| Propriété  | Test HOMO → LUMO+1 | Test HOMO-1 → LUMO | Test HOMO → LUMO |
|  :---: | :---: | :---: | :---: |
| **Rotation (Orbitales)** | {48, 50} | {47, 49} |{48, 49} |
| **Énergie Totale (Eh)** |  -680,576457 | -680,576455 | -680,576452 |
| **Correction D3BJ (Eh)** |  -0,043265 | -0,043265 | -0,043265 |
| **Solvatation (kcal/mol)** |  6,09565 | 6,09565 | 6,09565 |
| **Moment Dipolaire (D)** |  5,923 | 5,923 | 5,923 |
| **Rapport du Viriel** | 2,0089 | 2,0089 | 2,0089 |
| **Gap HOMO-LUMO (eV)** | 3,1446 |3,1445 | 3,1446 |
| **Cycles SCF** |  17 | 33 | 42 |

## 2.1 Iodo-BODIPY
| Propriété | HOMO-1 → LUMO | HOMO → LUMO+1 | HOMO → LUMO |
| :--- | :---: | :---: | :---: |
| **Rotation (Orbitales)** | {71, 73} | {72, 74} | {72, 73} |
| **Énergie Totale (Eh)** | -1274,779340 | -1274,779343 | -1274,779347 |
| **Dispersion (D3BJ)** | -0,054037 Eh | -0,054037 Eh | -0,054037 Eh |
| **Solvatation (SMD CDS)** | 5,2625 kcal/mol | 5,2625 kcal/mol | 5,2625 kcal/mol |
| **Moment Dipolaire** | 5,8438 Debye | 5,8441 Debye | 5,8438 Debye |
| **Rapport du Viriel** | 2,4155 | 2,4155 | 2,4155 |
| **Gap HOMO-LUMO (eV)** | 2,8748 | 2,8745 | 2,8748 |
| **Cycles SCF** | 16 | 17 | 35 |

## 2.1 TPP-BODIPY
| Propriété |  Test HOMO → LUMO+1 | Test HOMO → LUMO | Test HOMO-1 → LUMO |
| :--- |  :---: | :---: | :---: |
| **Rotation (Orbitales)** | {116, 118} | {116, 117} | {115, 117} |
| **Énergie Totale (Eh)** |  -1715,133218 | -1715,133211 | -1715,133207 |
| **Correction D3BJ (Eh)** |  -0,155699 | -0,155699 | -0,155699 |
| **Solvatation (Gcds)** |  11,15 kcal/mol | 11,15 kcal/mol | 11,15 kcal/mol |
| **Moment Dipolaire (D)** |  11,5760 | 11,5760 | 11,5761 |
| **Rapport du Viriel** |  2,0086 | 2,0086 | 2,0086 |
| **Gap HOMO-LUMO (eV)** | 2,7448 | 2,7447 | 2,7447 |
| **Cycles SCF** | 18 | 39 | 26 |



---

## 3. Analyse Détaillée des Fichiers de Sortie

### 3.1 BODIPY (Référence)
Pour stabiliser l'optimisation OO-DFT, trois rotations d'orbitales ont été évaluées :
- **test_HOMO_to_LUMO_BODIPY.txt** : Rotation {48, 49}. Énergie : -680,576452 Eh. Convergence en 42 cycles (difficultés de courbure BFGS).
- **test_HOMO-1_to_LUMO_BODIPY.txt** : Rotation {47, 49}. Énergie : -680,576455 Eh. Convergence en 33 cycles.
- **test_HOMO_to_LUMO+1_BODIPY.txt** : Rotation {48, 50}. C'est la configuration la plus stable avec -680,576457 Eh.

### 3.2 Iodo-BODIPY
L'iode impose l'usage d'un potentiel de cœur effectif (Def2-ECP) pour les effets relativistes.
- **test_HOMO-1_to_LUMO_IODO.txt** : Rotation {71, 73}. Énergie : -1274,779340 Eh.
- **test_HOMO_to_LUMO+1_IODO.txt** : Rotation {72, 74}. Énergie : -1274,779343 Eh.
- **test_HOMO_to_LUMO_IODO.txt** : Rotation {72, 73}. Énergie la plus basse : -1274,779346 Eh. Ce calcul a été le plus exigeant (35 cycles).

### 3.3 TPP-BODIPY
Ce système cationique (charge +1) présente une complexité électronique accrue.
- **test_HOMO-1_to_LUMO_TPP.txt** : Rotation {115, 117}. Énergie : -1715,133207 Eh.
- **test_HOMO_to_LUMO_TPP.txt** : Rotation {116, 117}. Énergie : -1715,133211 Eh. Convergence en 39 cycles.
- **test_HOMO_to_LUMO+1_TPP.txt** : Rotation {116, 118}. Énergie optimale : -1715,133218 Eh.

---

## 4. Choix de la configuration la plus stable (Best Guess)
Le tableau ci-dessous acte les choix finaux pour les calculs d'optimisation ultérieurs.

| Molécule | Transition Retenue | Orbitale Donneur | Orbitale Accepteur |
| :--- | :--- | :---: | :---: |
| **BODIPY** | HOMO → LUMO+1 | 48 | 50 |
| **Iodo-BODIPY** | HOMO → LUMO | 72 | 73 |
| **TPP-BODIPY** | HOMO → LUMO+1 | 116 | 118 |

---

## 5. Interprétation des Résultats

1. **Stabilité Numérique et Viriel** : Le rapport du viriel (~2,008) pour BODIPY et TPP-BODIPY indique une excellente convergence. La valeur atypique pour l'Iodo-BODIPY (2,4155) est la signature normale de l'utilisation d'un ECP sur l'iode, modifiant la balance entre énergies cinétique et potentielle.
2. **Impact de la Charge Cationique (TPP)** : Le groupement TPP induit un moment dipolaire très élevé (~11,58 D), doublant la force de solvatation (11,15 kcal/mol) par rapport aux dérivés neutres (~5-6 kcal/mol). Par comparaison avec des BODIPY neutres, la stabilisation par l'eau est ici presque doublée.
3. **Convergence et Contamination de Spin** : L'usage des algorithmes **AutoTRAH** et **DoMOM** a permis de contourner les avertissements de gaps réduits. La contamination de spin (**⟨S²⟩**) est nulle (0,000), garantissant la pureté des états singulets.
4. **Analyse Orbitale (S0)** : Le BODIPY possède un gap de 3,14 eV (HOMO -5,99 eV / LUMO -2,85 eV). L'extension de la conjugaison stabilisera ces niveaux pour les applications de thérapie photodynamique.
5. **Propriétés Optiques** : Par rapport à un BODIPY non substitué (~3,14 eV), l'iode et le TPP-BODIPY  réduisent le gap (de 2,8748 à 2,7448 eV) suggérant un effet **bathochrome (déplacement vers le rouge)** par rapport au BODIPY de référence, ce qui confirme l'effet de l'extension de la conjugaison par le substituant TPP.

---

## 6. Conclusion
L'étude systématique des configurations électroniques par OO-DFT a permis d'identifier les minimums locaux les plus stables pour chaque chromophore. La robustesse des calculs est confirmée par les indices de viriel et de spin. Ces "Best Guesses" constituent une base de départ fiable pour l'exploration des états excités S1 et des croisements inter-systèmes (ISC).
