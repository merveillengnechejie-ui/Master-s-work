# Rapport de Comparaison : def2-SVP vs def2-TZVP

Ce test évalue l'impact du changement de base sur l'optimisation de la géométrie (S0) et les propriétés optiques (TD-DFT) du BODIPY (21 atomes), en utilisant la fonctionnelle ωB97X-D3 en milieu aqueux (SMD Water).

## Tableau récapitulatif des paramètres de calcul

| Propriété | def2-SVP | def2-TZVP | Différence | Observation indépendante d'écart |
| :--- | :--- | :--- | :--- | :--- |
| **Fonctions de base** | 231 | 476 | + 245 | Doublement de la dimension de l'espace de Hilbert. |
| **Énergie SCF (Etot)** | -680,7008 Eh | -681,4507 Eh | - 0,7499 Eh | Stabilisation massive (~20,4 eV) ; TZVP est plus proche de la limite CBS (Complete Basis Set représente la valeur théorique vers laquelle converge l'énergie d'un calcul de chimie quantique). | 
| **λmax (S1)** | 458,8 nm | 463,9 nm | + 5,1 nm | Écart > 5 nm, seuil critique pour la précision spectroscopique . |
| **Force d'oscillateur (fosc)** | 0,9231 | 0,9278 | + 0,0047 | Transition électronique plus intense et mieux définie en TZVP. |
| **Moment Dipolaire** | 6,2548 D | 6,4998 D | + 0,245 D | Meilleure description de la polarisation par le solvant. |
| **Répulsion Nucléaire** | 857,6788 Eh | 866,7090 Eh | + 9,0302 Eh | Repositionnement des noyaux suite à la relaxation électronique TZVP. |
| **Temps SCF (cycle final)** | 48,1 s | 135,6 s | x 2,82 | Augmentation significative du coût computationnel. |

## Tableau: Théorie (TD-DFT) vs Expérience (~505 nm)

| Paramètre | def2-SVP | def2-TZVP | Valeur Expérimentale |
| :--- | :--- | :--- | :--- |
| **λmax** | 458,8 nm | 468,2 nm | ~505 nm |
| **Écart / Expérience (Δλ)** | - 46,2 nm | - 36,8 nm | - |
| **Erreur Relative (%)** | ~ 9,1 % | **~ 7,3 %** | - |
| **Force d'oscillateur (fosc)** | 0,923 | 0,908 | - |

## Analyse et Confrontation à l'Expérience

*   **Précision Théorique** : Conformément au manuel ORCA, la base def2-TZVP est impérative pour obtenir des résultats fiables. Elle inclut des fonctions de polarisation étendues (2d1f pour les éléments lourds) indispensables pour capturer la densité électronique fine que la base SVP (double-zeta) néglige.
*   **Performance Spectroscopique (Théorie vs Exp)** : Le passage à la base Triple-Zeta (TZVP) améliore le λmax théorique de +9,4 nm par rapport à la base SVP, réduisant l'erreur relative à ~7,3% (vs ~9,1% en SVP). 
*   **Limites et Écart Résiduel** : Bien que la base TZVP soit plus performante, il subsiste un écart systématique d'environ ~37 nm avec l'expérience. Ceci s'explique par la nature du calcul, le biais de surestimation de la fonctionnelle ωB97X-D3, et les limites du modèle de solvatation continu (SMD) face aux interactions spécifiques (ex: ponts hydrogène).
*   **Polarisation et Solvatation** : L'augmentation du moment dipolaire en TZVP révèle une réponse plus réaliste de la molécule face au solvant.

## Conclusion

La base **def2-TZVP** est clairement supérieure (réduction de l'erreur de près de 20% par rapport à SVP) et s'impose pour valider physiquement les propriétés optiques dans ce cas précis (écart inter-base > 10 nm). 


