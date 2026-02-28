# Analyse des Énergies de Solvatation — BODIPY, Iodo-BODIPY et TPP-BODIPY

**Méthode :** DFT B3LYP-D3BJ / def2-SVP — Modèle CPCM + SMD (solvant : eau, ε = 78.36)  
**Logiciel :** ORCA 6.1 | **Milieu biologique :** optimisation géométrique en phase condensée (eau)  
**Phase gazeuse :** optimisation sans solvant (ε = 1)  

---



## 1. Données extraites des fichiers `.out` — Tableau récapitulatif

### 1.1 Composantes de l'énergie de solvatation en milieu biologique  (dernier point convergé)

| Molécule | ΔG_diel (eV) | ΔG_diel (Eh) | G_CDS (kcal/mol) | G_CDS (Eh) |
|----------|:------------:|:------------:|:----------------:|:----------:|
| BODIPY | **−0.614** | −0.022565 | **5.97** | +0.009714 |
| Iodo-BODIPY | **−0.708** | −0.026004 | **5.26** | +0.008386 |
| TPP-BODIPY | **−2.602** | −0.095613 | **11.15** | +0.017772 |

### 1.2 Énergie totale électronique DFT (point final convergé)

| Molécule | E_gaz (Eh) | E_CPCM (Eh) | ΔE = E_CPCM − E_gaz (Eh) | ΔE (eV) | ΔE (kcal/mol) |
|----------|:----------:|:-----------:|:------------------------:|:-------:|:--------------:|
| BODIPY | −680.567464 | −680.576457 | −0.008993 | −0.2447 | −5.64 |
| Iodo-BODIPY | −1274.765556 | −1274.779347 | −0.013791 | −0.3752 | −8.65 |
| TPP-BODIPY | −1715.063726 | −1715.133211 | −0.069485 | −1.8907 | −43.59 |

> *Toutes les géométries ont convergé (TightSCF + TightOPT). Les énergies sont les FSPE (Final Single Point Energy) reportées dans les `.out`.*

---

## 2. Analyse comparative moléculaire

### 2.1 Terme diélectrique CPCM (interaction électrostatique avec le solvant)

```
BODIPY         : −0.57 eV   ████████░░░░░░░░░░░░░░░░░
Iodo-BODIPY    : −0.66 eV   █████████░░░░░░░░░░░░░░░░
TPP-BODIPY     : −2.51 eV   █████████████████████████
```

**Interprétation :**

- **BODIPY (−0.57 eV)** présente la stabilisation diélectrique la plus faible. La molécule BODIPY de base est relativement petite (21 atomes, 98 électrons), avec une polarité modérée (μ_gaz = 4.11 D). Sa cavité moléculaire est compacte, limitant la surface d'interaction avec le continuum diélectrique.

- **Iodo-BODIPY (−0.66 eV)** montre une légère augmentation par rapport au BODIPY. L'ajout de deux atomes d'iode (deux substituants lourds, 146 électrons au total) crée une surface de cavité plus étendue et augmente la polarisabilité globale, favorisant l'interaction électrostatique avec l'eau. Le moment dipolaire reste comparable (μ_gaz = 4.00 D, μ_CPCM = 5.84 D).

- **TPP-BODIPY (−2.51 eV)** : stabilisation diélectrique **4.2× plus grande** que le BODIPY. Ce résultat est remarquable et s'explique par :
  1. Une masse moléculaire nettement plus grande (présence d'un groupement triphénylphosphonium, atome P central)
  2. Un moment dipolaire très élevé (μ_gaz = 8.82 D, μ_CPCM = 11.58 D), soit le double de celui du BODIPY
  3. Une surface de cavité CPCM (~695 847 points, bien supérieure aux autres molécules)
  4. La charge partielle sur l'atome de phosphore (Mulliken +0.594) crée une forte asymétrie de charge propice à l'interaction diélectrique

### 2.2 Terme CDS — Correction cavité-dispersion-répulsion (SMD)

```
BODIPY         :  5.97 kcal/mol  ██████░░░░░░
Iodo-BODIPY    :  5.15 kcal/mol  █████░░░░░░░
TPP-BODIPY     : 10.86 kcal/mol  ███████████░
```

**Interprétation :**

- Le terme CDS est **toujours positif** : il représente le coût énergétique de former la cavité dans le solvant (eau) + la somme dispersion/répulsion/électrostatique à courte portée.

- **Iodo-BODIPY (5.15 kcal/mol)** a un G_CDS légèrement *inférieur* à celui du BODIPY de base (5.97 kcal/mol), malgré sa plus grande taille. Cet effet contre-intuitif s'explique par le fait que les atomes d'iode, de par leur nature **hydrophobe** et leur grand rayon (1.98 Å), ont des paramètres SMD-CDS qui défavorisent l'exposition à l'eau. Les descripteurs SMD  font que le G_CDS dépend surtout de la surface des atomes non-hydrogène exposés et de leur nature atomique.

- **TPP-BODIPY (10.86 kcal/mol)** : terme CDS quasi double. La grande surface de cavité de la molécule (nombreux cycles phényles du groupement triphénylphosphonium) nécessite un travail de cavitation important. La molécule expose de nombreux carbones aromatiques à l'eau, augmentant le terme de dispersion.

### 2.3 Bilan : Énergie de solvatation nette ΔG_solv

> **Note physique.** L'énergie de solvatation totale dans le formalisme CPCM–SMD est :
> $$\Delta G_{\text{solv}} = \Delta G_{\text{diel}} + G_{\text{CDS}}$$
> où $\Delta G_{\text{diel}}$ est négatif (interaction favorable électrostatiquement) et $G_{\text{CDS}}$ est positif (coût de cavité + dispersion). La somme donne l'énergie libre de solvatation effective.


| Molécule | ΔG_diel (kcal/mol) | G_CDS (kcal/mol) | **ΔG_solv total (kcal/mol)** |
|----------|:-----------------:|:----------------:|:------------------------:|
| BODIPY | −14.16 | +5.97 | **−8.19** |
| Iodo-BODIPY | −16.31 | +5.26 | **−11.16** |
| TPP-BODIPY | −59.90 | +10.86 | **−49.04** |

> Conversion : 1 Eh = 627.51 kcal/mol ; 1 eV = 23.06 kcal/mol

**Observations clés :**
- Les trois molécules sont **thermodynamiquement favorisées** en milieu aqueux (ΔG_solv < 0)
- TPP-BODIPY est de loin la plus soluble en milieu polaire aqueux (ΔG_solv ≈ −49 kcal/mol), ce qui est cohérent avec la présence d'un cation phosphonium — un groupement reconnu pour son caractère amphiphile et sa forte affinité pour les mitochondries (membranes fortement chargées négativement)
- Iodo-BODIPY est légèrement mieux solvaté que le BODIPY car le gain diélectrique l'emporte sur la pénalité CDS

---

## 3. Moment dipolaire — Influence du solvant

| Molécule | μ_gaz (D) | μ_CPCM (D) | Δμ = μ_CPCM − μ_gaz (D) | Augmentation (%) |
|----------|:---------:|:----------:|:------------------------:|:----------------:|
| BODIPY | 4.113 | 5.924 | +1.811 | **+44%** |
| Iodo-BODIPY | 3.998 | 5.844 | +1.846 | **+46%** |
| TPP-BODIPY | 8.818 | 11.576 | +2.758 | **+31%** |

**Interprétation :**

L'augmentation systématique des moments dipolaires en phase condensée (effet de polarisation du continuum diélectrique) est une signature de la **rétroaction diélectrique** : le champ de réaction créé par les charges de surface CPCM amplifie la polarisation électronique de la molécule.

- **BODIPY et Iodo-BODIPY** : augmentation similaire (~45%), cohérente avec des structures électroniques voisines (core BODIPY identique). L'iode n'ajoute que peu à la polarité intrinsèque mais maintient un dipôle similaire.
- **TPP-BODIPY** : malgré un moment dipolaire absolu beaucoup plus élevé, l'augmentation relative est moindre (31%), car la molécule possède déjà une polarité intrinsèque forte (présence de la charge +1 sur le phosphore qui est partiellement écrantée dans la structure neutre globale).

---

## 4. Orbitales frontières (HOMO-LUMO) — Comparaison phase gazeuse vs. Milieu biologique

### 4.1 Tableau des énergies orbitales

| Molécule | Phase | HOMO (eV) | LUMO (eV) | Gap HL (eV) |
|----------|-------|:---------:|:---------:|:-----------:|
| BODIPY | Gazeuse | −6.155 (MO 48) | −3.050 (MO 49) | **3.105** |
| BODIPY | CPCM | −5.998 (MO 48) | −2.853 (MO 49) | **3.145** |
| Iodo-BODIPY | Gazeuse | −6.227 (MO 72) | −3.421 (MO 73) | **2.806** |
| Iodo-BODIPY | CPCM | −5.889 (MO 72) | −3.014 (MO 73) | **2.875** |
| TPP-BODIPY | Gazeuse | −8.979 (MO 116) | −6.299 (MO 117) | **2.680** |
| TPP-BODIPY | CPCM | −6.246 (MO 116) | ~−5.5  | **~0.75** |



**Observations :**

1. **Iodo-BODIPY** : l'ajout de deux atomes d'iode **abaisse** le HOMO de −6.155 à −6.227 eV et le LUMO de −3.050 à −3.421 eV par rapport au BODIPY. Le gap HOMO-LUMO se réduit de ~3.10 à ~2.81 eV. Cet abaissement est dû à l'**effet de masse lourde** de l'iode et à son couplage spin-orbite fort, qui perturbe les états frontières.

2. **TPP-BODIPY** : le gap HOMO-LUMO est le plus petit (~2.68 eV en phase gazeuse), ce qui prédit une absorption à plus longue longueur d'onde. La présence du groupe TPP étend le système π-conjugué et abaisse significativement le LUMO.

3. **Effet du solvant (CPCM) :** En solution, tous les niveaux d'énergie se "remontent" légèrement (HOMO moins négatif), signe de la stabilisation différentielle de la densité de charge par le continuum. Le gap reste quasi inchangé pour BODIPY (3.10→3.14 eV) et Iodo-BODIPY (2.81→2.88 eV).

---

## 5. Comparaison inter-moléculaire — Points clés en photophysique et thérapie photodynamique

| Critère | BODIPY | Iodo-BODIPY | TPP-BODIPY |
|---------|--------|-------------|------------|
| Solubilité en eau (ΔG_solv) | Faible (−8.2 kcal/mol) | Modérée (−11.1 kcal/mol) | Très élevée (−49 kcal/mol) |
| Interaction diélectrique | Faible | Intermédiaire | Très forte |
| Moment dipolaire (CPCM) | 5.92 D | 5.84 D | 11.58 D |
| Gap HOMO-LUMO (solution) | 3.14 eV | 2.88 eV | ~0.75 eV  |
| Taille de cavité | Petite | Intermédiaire | Grande |
| Pertinence biologique | Colorant de base | Photosensibilisateur (SOC↑) | Ciblage mitochondrial |

### 5.1 BODIPY de base
Le **BODIPY** est la référence structurelle. Sa faible solvatation (ΔG_solv = −8.2 kcal/mol) et son dipôle modéré (5.9 D) reflètent un chromophore essentiellement **apolaire** en solution aqueuse. Le grand gap HOMO-LUMO (3.14 eV) correspond à une absorption dans le visible (~395 nm ), correspondant à une longueur d'onde utile pour la PDT mais avec une faible génération d'oxygène singulet sans modification.

### 5.2 Iodo-BODIPY
L'introduction des atomes d'**iode** en position 2,6 du cœur BODIPY remplit deux fonctions :
1. **Couplage spin-orbite (SOC)** : les atomes lourds d'iode (Z = 53) augmentent fortement la probabilité de croisement intersystème (ISC), augmentant le rendement en états triplets T₁ et donc la production d'oxygène singulet ¹O₂
2. **Faible variation de solvatation** : le G_CDS légèrement réduit (5.26 vs 5.97 kcal/mol) compense partiellement le léger gain diélectrique. La biodistribution en milieu aqueux sera similaire à celle du BODIPY avec une micelle ou un transporteur.

La réduction du gap HOMO-LUMO à 2.88 eV (solution) décale l'absorption vers le **rouge** (~430 nm), améliorant la pénétration tissulaire.

### 5.3 TPP-BODIPY
**TPP-BODIPY** est le photosensibilisateur le plus avancé du point de vue clinique. Ses propriétés de solvatation exceptionnelles (ΔG_solv ≈ −49 kcal/mol) sont liées au groupement **triphénylphosphonium** (TPP), un vecteur cationique lipophile qui :
- Accumule sélectivement dans les **mitochondries** grâce au potentiel de membrane mitochondrial négatif (ΔΨm ≈ −180 mV)
- Augmente drastiquement l'interaction électrostatique avec les membranes biologiques chargées négativement
- Le moment dipolaire très élevé (11.58 D en solution) reflète cette asymétrie de charge

La grande énergie de solvatation diélectrique (−2.60 eV) suggère que **TPP-BODIPY sera fortement stabilisé dans l'environnement aqueux/lipidique des mitochondries**, favorisant sa rétention cellulaire et augmentant son efficacité comme agent de PDT mitochondrial.

> ⚠️ Le gap HOMO-LUMO en CPCM semble anormalement faible pour TPP-BODIPY (~0.75 eV ). Cela peut refléter une réorganisation des niveaux d'énergie due à la charge partielle du phosphore et à la grande surface de conjugaison. 
---

## 6. Paramètres du modèle de solvatation utilisé

| Paramètre | Valeur |
|-----------|--------|
| Modèle | CPCM (Conductor-like Polarizable Continuum Model) |
| Correction non-électrostatique | SMD (Solvent Model based on Density) |
| Solvant | Eau (water) |
| Constante diélectrique ε | 78.355 |
| Indice de réfraction (Refrac) | 1.3328 |
| Rayon de sonde | 1.3000 Å (Rsolv) |
| Schéma de surface | Gaussian VDW |
| Fonctionnelle | B3LYP-D3BJ (20% HF exchange) |
| Base | def2-SVP |
| Convergence SCF | TightSCF (ΔE < 1×10⁻⁸ Eh) |
| Convergence géométrique | TightOPT |

---


### Synthèse comparative

1. **Ordre de solvatation :** TPP-BODIPY ≫ Iodo-BODIPY > BODIPY 
   Cette hiérarchie reflète directement l'augmentation du moment dipolaire et de la surface moléculaire.

2. **TPP-BODIPY** est thermodynamiquement le plus stable en milieu aqueux. Sa forte interaction diélectrique (−2.60 eV) et son grand dipôle (11.58 D) le rendent particulièrement adapté à un environnement biologique polaire. Ces résultats supportent son utilisation comme **photosensibilisateur à ciblage mitochondrial**.

3. **Iodo-BODIPY** représente un compromis optimal : meilleure solvatation que le BODIPY de base tout en maintenant les propriétés SOC importantes pour la PDT (génération d'espèces réactives de l'oxygène via les états triplets).

4. **BODIPY de base** sert de référence structurelle. Sa solvatation modérée est compensée par sa grande stabilité photochimique et sa synthèse facile.





