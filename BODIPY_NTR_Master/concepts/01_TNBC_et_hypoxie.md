# Concept 1 — Le TNBC et l'Hypoxie Tumorale
## Pourquoi cibler ce cancer avec cette approche ?

---

## 1. Qu'est-ce que le TNBC ?

Le **cancer du sein triple négatif (TNBC)** est défini par l'absence de trois récepteurs :

| Récepteur | Rôle normal | Statut TNBC |
|-----------|-------------|-------------|
| ER (Œstrogène) | Régulation hormonale | **Négatif** |
| PR (Progestérone) | Régulation hormonale | **Négatif** |
| HER2 | Facteur de croissance | **Négatif** |

### Pourquoi cette triple négativité est-elle un problème ?

Les thérapies hormonales (tamoxifène, aromatase inhibitors) ciblent ER et PR. Les thérapies anti-HER2 (trastuzumab/Herceptin) ciblent HER2. Le TNBC n'ayant **aucune de ces cibles**, il est **résistant à ces traitements**.

**Données épidémiologiques** :
- 15–20% de tous les cancers du sein
- Taux de survie à 5 ans : ~77% (localisé) → ~12% (métastatique) (SEER 2023)
- Prévalence plus élevée chez les femmes jeunes et d'Afrique subsaharienne
- Seule option actuelle : chimiothérapie cytotoxique (effets secondaires sévères)

> **Pourquoi le TNBC est un bon modèle d'étude** : Sa résistance aux thérapies conventionnelles en fait un cas d'étude paradigmatique pour les approches alternatives comme la PDT/PTT.

---

## 2. L'hypoxie tumorale : une vulnérabilité à exploiter

### Définition
L'**hypoxie** désigne un manque d'oxygène dans les tissus. Dans les tumeurs solides, la croissance rapide des cellules cancéreuses dépasse la capacité des vaisseaux sanguins à les alimenter en O₂.

```
Tumeur normale : pO₂ ≈ 40–60 mmHg
Tumeur hypoxique : pO₂ < 10 mmHg  ← TNBC typique
```

### Conséquences biologiques de l'hypoxie

```
Hypoxie
  │
  ├─→ Activation HIF-1α (Hypoxia-Inducible Factor)
  │     └─→ Surexpression de NTR (nitroreductase) × 3–8
  │
  ├─→ Résistance à la chimiothérapie (moins d'O₂ = moins de radicaux libres)
  │
  └─→ Métastases plus fréquentes (cellules plus agressives)
```

### La nitroreductase (NTR) : notre cible

La **nitroreductase** est une enzyme qui réduit les groupements nitro (—NO₂) en amine (—NH₂) en utilisant NADPH comme cofacteur :

```
—NO₂  +  NADPH  →  —NH₂  +  NAD⁺  +  H₂O
  (OFF)    NTR      (ON)
```

**Pourquoi c'est parfait pour notre projet** :
- NTR est surexprimée **3–8×** dans les tumeurs hypoxiques vs tissu normal
- La réaction nécessite un environnement pauvre en O₂ (hypoxique)
- Elle est **sélective** : peu active dans les tissus normaux oxygénés
- Elle transforme notre molécule d'un état inactif (prodrug) à un état actif

---

## 3. Le microenvironnement tumoral (TME) du TNBC

Le TME du TNBC présente plusieurs caractéristiques exploitables :

| Paramètre | Tissu normal | TME TNBC | Exploitation |
|-----------|-------------|----------|--------------|
| pO₂ | 40–60 mmHg | < 10 mmHg | Activation NTR sélective |
| pH | 7.4 | 6.5–6.8 | Activation pH-sensible |
| [GSH] | 2–20 μM | 1–10 mM | Clivage disulfure |
| NTR | Faible | × 3–8 | **Notre trigger principal** |
| Potentiel mitochondrial | −120 mV | −180 mV | Accumulation TPP⁺ |

---

## 4. Stratégie thérapeutique : le "cheval de Troie" moléculaire

Notre molécule BODIPY-NTR fonctionne comme un **prodrug activé** :

```
Injection systémique
        │
        ▼
Tissu normal (normoxique)
  NTR faible → molécule reste en forme NO₂ (OFF)
  → Pas de phototoxicité → Pas d'effets secondaires
        │
        ▼
Tumeur TNBC (hypoxique)
  NTR élevée → NO₂ → NH₂ (ON)
  → Irradiation lumineuse (NIR-I, 650–750 nm)
  → PDT : génération ¹O₂ → mort cellulaire
  → PTT : chaleur locale → mort cellulaire
```

---

## 5. Pourquoi la fenêtre NIR-I (650–750 nm) ?

La lumière doit traverser les tissus pour atteindre la tumeur. L'absorption par les tissus biologiques varie avec la longueur d'onde :

```
UV/Visible (< 600 nm) : forte absorption par l'hémoglobine et la mélanine
                         → pénétration < 1 mm

NIR-I (650–900 nm)    : absorption minimale des tissus
                         → pénétration 5–10 mm  ← NOTRE CIBLE

NIR-II (1000–1700 nm) : encore moins d'absorption
                         → pénétration > 1 cm (perspective future)
```

**Conclusion** : Notre BODIPY doit absorber dans la fenêtre NIR-I (λ_max = 650–750 nm) pour être efficace sur des tumeurs profondes.

---

## 6. Résumé : pourquoi ce projet est pertinent

```
Problème clinique          Solution computationnelle
─────────────────          ─────────────────────────
TNBC résistant             → Design de novo in silico
Hypoxie tumorale           → Trigger NTR sélectif
Effets secondaires         → Activation sélective (prodrug)
Tumeurs profondes          → Absorption NIR-I (650–750 nm)
PDT limitée par hypoxie    → Synergie PDT + PTT
```

---

## 📖 Références clés

- Kong et al., *Prog. Mater. Sci.* 2023, 134, 101070 — TNBC microenvironnement
- Bartusik-Aebisher et al., *Pharmaceuticals* 2025, 18, 53 — BODIPY pour PDT/PTT
- Overchuk et al., *ACS Nano* 2023, 17, 7979 — Synergie PDT/PTT

---

*Suite → [`02_BODIPY_photophysique.md`](02_BODIPY_photophysique.md)*
´