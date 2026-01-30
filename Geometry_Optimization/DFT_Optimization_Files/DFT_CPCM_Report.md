# Rapport d'Analyse DFT : Propriétés Électroniques et Structurelles
**Méthode :** DFT (B3LYP/def2-SVP) + D3BJ + SMD(Water) / CPCM
**Date :** 30 Janvier 2026

## 1. Introduction
Ce rapport synthétise l'analyse des calculs d'optimisation de géométrie avec la DFT effectués sur trois molécules :
*   **BODIPY** (Référence neutre)
*   **Iodo-BODIPY** (Dérivé à atome lourd, neutre)
*   **TPP-BODIPY** (Dérivé cationique conjugué, charge +1)

Les calculs ont été réalisés avec le code ORCA 6.1.0 en milieu biologique (eau)

## 2. Tableau Récapitulatif Global

| Propriété | BODIPY | Iodo-BODIPY | TPP-BODIPY |
| :--- | :---: | :---: | :---: |
| **Formule / Charge** | Neutre (S=0) | Neutre (S=0) | Cation +1 (S=0) |
| **Nombre d'électrons** | 98 | 146 (ECP utilisé) | 234 |           ##ECP signifie Effective Core Potential, utilisé pour réduire le cout de calcul et prendre en compte la relativité
| **Temps de Calcul** | 7 min 41 s | 5 min 42 s | 54 min 05 s |
| **Énergie Totale (Eh)** | -680.576456 | -1274.779347 | -1715.133210 |
| **HOMO (eV)** | -5.9577 | -5.8619 | -6.2142 |
| **LUMO (eV)** | -2.7642 | -2.9328 | -3.4552 |
| **Gap HOMO-LUMO (eV)** | 3.1935 | 2.9291 | 2.7590 |
| **Moment Dipolaire (Debye)** | 5.9237 | 5.8439 | 11.5760 |


| Propriété Énergétique | BODIPY | Iodo-BODIPY | TPP-BODIPY |
| :--- | :---: | :---: | :---: |
| **Répulsion Nucléaire** | 858,78217190 | 1381,82298530 | 3540,30729182 |
| **Énergie Électronique** | -1539,30248402 | -2656,53081529 | -5255,20707518 |
| **Énergie d'Échange (EX)** | -68,67737212 | -101,82011931 | -164,35483377 |
| **Énergie de Corrélation (EC)** | -4,01196713 | -6,26280743 | -9,53113044 |
| **Dispersion (D3BJ)** | -0,04326670 | -0,05401691 | -0,15569377 |
| **Rapport du Viriel** | 2,00897165 | 2,41555358 | 2,00864592 |

## 3. Analyse Détaillée

### 3.1 Structure Électronique et Réactivité (Orbitales Frontières)
*   **BODIPY (Référence) :** Présente le gap le plus large (**3.19 eV**), signifiant une stabilité relative importante et une absorption dans la région classique (**vert/bleu**).
*   **Effet de l'Iode (Iodo-BODIPY) :** L'introduction de l'atome lourd déstabilise légèrement le HOMO (**-5.8616 eV**  vs **-5.9577 eV**). Le gap se réduit à **2.9291 eV**.Cela suggère une oxydation légèrement plus facile et une absorption décalée vers le rouge. L'analyse de valence (1.09) confirme une liaison simple I-C classique.
*   **Effet de Conjugaison (TPP-BODIPY) :** C'est la modification la plus impactante. L'ajout des groupements triphénylposphonium (TPP) stabilise fortement le LUMO (**-3.4552** eV), réduisant le gap à **2.7590 eV**. Cela prédit un déplacement bathochrome (vers le rouge) de l'absorption, favorable pour les applications thérapeutiques (PDT). Le HOMO très bas (**-6.2142 eV**) indique paradoxalement une bonne résistance à l'oxydation, malgré la charge positive globale.

### 3.2 Interaction avec le Milieu et Solvatation
*   **Polarité Géante du TPP-BODIPY :** Avec un moment dipolaire de **11.5760 Debye** (contre ~5.9 D pour les autres), le cation TPP-BODIPY est une espèce hautement polaire. Cette polarité s'explique par la séparation de charge induite par le centre cationique Phosphore (charge Mulliken +0.66) et le cœur BODIPY.
*   **Stabilisation Énergétique :**
    *   **Composante Diélectrique (CPCM) :** Le TPP-BODIPY interagit très fortement avec le champ du solvant, quatre fois plus que le BODIPY neutre.
    *   **Correction Non-Électrostatique (SMD-CDS) :** La correction de cavité/dispersion est également double pour le TPP (11.17 kcal/mol), reflétant sa surface accessible au solvant beaucoup plus grande .

### 3.3 Performance et Coût Numérique
*   **Complexité :** Le passage au TPP-BODIPY (234 électrons, 571 fonctions de base) entraîne un coût de calcul **7 fois supérieur** (54 min vs ~7 min).
*   **Stratégie Iode (ECP) :** L'utilisation des pseudopotentiels (Def2-ECP) pour l'Iode est validée : malgré la lourdeur de l'atome (53 protons), le calcul est plus rapide (5 min 42) que pour le BODIPY standard, car seuls les électrons de valence sont traités explicitement.

## 4. Conclusion 
L'analyse confirme que le **TPP-BODIPY** est le candidat le plus prometteur pour ses propriétés optiques (gap réduit) et sa solubilité/interaction biologique (forte polarité), mais il représente un défi numérique. L'**Iodo-BODIPY** est correctement modélisé pour servir de plateforme à l'étude du couplage spin-orbite (SOC) grâce aux ECP, sans surcoût.


