# Rapport Technique : Criblage Spectral Tier 1 et Stratégie de Sélection

**Projet :** Optimisation de nanoparticules de BODIPY activables par NTR pour la thérapie du cancer du sein triple négatif (TNBC)  
**Logiciel :** ORCA 6.1.1  
**Méthodologie :** sTDA / PBE0 / def2-SVP  
**Date :** 28 mai 2026  

---

## 1. Architecture et Objectifs du Tier 1

Le Tier 1 agit comme le second filtre de notre entonnoir computationnel. L'objectif est d'exploiter la rapidité et la faible exigence en ressources de la méthode sTDA (*Simplified Tamm-Dancoff Approximation*) pour estimer les propriétés optiques d'une chimiothèque de 8 molécules avant d'engager des calculs de haute précision (plus coûteux en temps de calcul et en mémoire).

Le triage repose sur trois critères spectroscopiques et fonctionnels :
1. **L'absorption dans la fenêtre thérapeutique** : Cibler le domaine du proche infrarouge (NIR-I, 600-900 nm) pour maximiser la pénétration tissulaire.
2. **L'intensité photonique** : Évaluée via la force d'oscillateur ($f_{\text{osc}}$) pour garantir un fort rendement d'absorption.
3. **La réponse au trigger enzymatique** : Évaluer l'amplitude du décalage spectral vers le rouge (redshift) lors de la réduction enzymatique du groupement nitro en groupement amine (passage de l'état $\text{NO}_2$ à l'état $\text{NH}_2$, modélisant l'activation OFF $\rightarrow$ ON par la NTR).

---

## 2. Analyse Comparative des Données Spectroscopiques

Le tableau suivant regroupe les transitions électroniques les plus basses en énergie ($S_0 \rightarrow S_1$) extraites des 8 calculs sTDA.

| Molécule | État NTR | $\lambda_{\max}$ (nm) | Force d'osc. ($f_{\text{osc}}$) | Transition majeure | 
| :--- | :---: | :---: | :---: | :---: | 
| **BODIPY_Ph** | — | 758,7 | 0,0511 | $36\beta \rightarrow 37\beta$ | 
| **BODIPY_Ph_NO2** | OFF | 689,0 | 0,0442 | $42\beta \rightarrow 43\beta$ | 
| **BODIPY_Ph_NH2** | ON | 940,2 | 0,1169 | $39\beta \rightarrow 40\beta$ | 
| **Iodo_BODIPY** | — | 877,7 | 0,0230 | $41\beta \rightarrow 42\beta$ | 
| **Iodo_BODIPY_NO2** | OFF | 787,4 | 0,0163 | $47\beta \rightarrow 48\beta$ | 
| **Iodo_BODIPY_NH2** | ON | 1135,0 | 0,1214 | $45\beta \rightarrow 46\beta$ | 
| **TPP_Iodo_BODIPY** | — | 641,7* | 0,0007 | $92 \rightarrow 94$ |
| **Aza_BODIPY_NO2** | OFF | 589,4 | 0,9971 | $92 \rightarrow 93$ | 

*\*Note : Pour le TPP_Iodo_BODIPY, la transition fondamentale (Root 0) présente une intensité négligeable ; le pic d'absorption principal se situe à 427,3 nm ($f = 0,115$).*

---

## 3. Classification des Systèmes pour le Triage

Afin de structurer l'analyse, la chimiothèque est divisée en deux catégories distinctes de systèmes :

### 3.1 Prototypes de Contrôle Physique
Ces molécules servent d'étalons de comparaison pour isoler et quantifier l'impact de chaque modification structurale sur la photophysique globale :
- **BODIPY_Ph** : Référence fondamentale pour le benchmarking de la méthode ($\Delta\text{DFT}$) et l'évaluation de l'erreur absolue moyenne (MAE).
- **Iodo_BODIPY** : Contrôle destiné à isoler et quantifier l'effet d'atome lourd (iode) sur le couplage spin-orbite (SOC) et la transition intersystème (ISC), sans interférence avec le trigger nitro/amine.

### 3.2 Candidats Théranostiques
Systèmes conçus pour assurer la fonction biologique ciblée (activation tumorale par la NTR et adressage subcellulaire) :
- **Couples Iodo-NO2 / Iodo-NH2** : Ces dérivés permettent de valider la porte logique moléculaire. On observe un redshift exceptionnel de 347,6 nm lors du passage de l'état « OFF » (iodé-nitro) à l'état « ON » (iodé-amine).
- **Aza_BODIPY_NO2** : Classé prioritaire pour la thérapie photothermique (PTT) en raison d'une force d'oscillateur quasi-unitaire ($f \approx 0,997$), garantissant une absorption photonique maximale.
- **TPP_Iodo_BODIPY** : Conçu pour évaluer si l'introduction du vecteur de ciblage mitochondrial (triphenylphosphonium, $\text{TPP}^+$) altère les propriétés optiques ou l'efficacité théranostique globale.

---

## 4. Grille de Décision Quantitative (Go/No-Go)

Cette grille définit les systèmes sélectionnés pour la phase finale de caractérisation théranostique de haute précision (Tier 2.5 : calculs de couplage spin-orbite (SOC) et calculs d'états excités $\Delta\text{ROKS}$).

| Prototype | Rôle | Décision | Justification Scientifique |
| :--- | :--- | :---: | :--- |
| **BODIPY_Ph** | Référence MAE | **Référence** | Étalon spectroscopique requis au Chapitre 2 pour valider la précision méthodologique. |
| **Iodo_BODIPY** | Contrôle SOC | **Go** | Isolation de l'effet d'atome lourd (iode) sur l'ISC avant complexification structurale. |
| **Aza_BODIPY_NO2** | Candidat PTT | **Go** | Rendement photonique exceptionnel ($f \approx 1$), idéal pour la conversion thermique. |
| **Iodo_BODIPY_NO2** | Candidat OFF | **Go** | État « éteint » idéal, absorbant à 787 nm (fenêtre thérapeutique NIR-I). |
| **Iodo_BODIPY_NH2** | Candidat ON | **Go** | Étude du redshift extrême vers la fenêtre NIR-II (1135 nm). |
| **TPP_Iodo_BODIPY** | Ciblage | **Go** | Validation impérative de la synergie avec le groupement de ciblage mitochondrial $\text{TPP}^+$. |
| **BODIPY_Ph_NO2/NH2** | Test du trigger | **No-Go\*** | Remplacés par les dérivés iodés, plus pertinents cliniquement (SOC renforcé par l'iode). |

*\*Les molécules classées en No-Go sont archivées comme références de tendance dans la chimiothèque, mais ne subiront pas l'optimisation géométrique coûteuse des états excités relaxés.*

---

## 5. Conclusion sur le Choix des Molécules

L'analyse du Tier 1 confirme la viabilité théorique du concept de sonde « Turn-ON » activable par la NTR. La réduction enzymatique du groupement nitro en amine induit un décalage spectral massif (redshift de plus de 300 nm), ce qui permet théoriquement une activation thérapeutique hautement sélective au sein du microenvironnement tumoral.

Cinq systèmes prioritaires ont été retenus pour les calculs d'états excités de haute précision ($\Delta\text{ROKS}$). La phase suivante consistera à optimiser l'état fondamental ($S_0$) en phase aqueuse (modèle de solvant implicite SMD) sur ces candidats, avant d'engager les calculs de couplage spin-orbite. 
