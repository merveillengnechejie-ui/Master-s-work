# Concept 3 — PDT et PTT : Mécanismes et Synergie
## Deux armes photoniques complémentaires

---

## 1. Thérapie Photodynamique (PDT)

### Principe
La PDT utilise un **photosensibilisateur (PS)** + **lumière** + **oxygène** pour générer des espèces réactives de l'oxygène (ROS) qui tuent les cellules cancéreuses.

### Mécanisme détaillé

```
Étape 1 : Absorption
  PS(S₀) + hν → PS(S₁)
  [Le photosensibilisateur absorbe un photon et passe à l'état excité singulet]

Étape 2 : Intersystem Crossing (ISC)
  PS(S₁) → PS(T₁)
  [Transition vers l'état triplet — CRUCIAL pour la PDT]
  [Favorisée par : petit ΔE_ST, fort SOC, atomes lourds]

Étape 3a : PDT Type II (dépendante de l'O₂)
  PS(T₁) + ³O₂ → PS(S₀) + ¹O₂
  [Transfert d'énergie à l'oxygène → oxygène singulet ¹O₂]
  [¹O₂ oxyde les lipides, protéines, ADN → mort cellulaire]
  Condition : T₁ > 0.98 eV (énergie de ¹O₂)

Étape 3b : PDT Type I (indépendante de l'O₂)
  PS(T₁) + substrat → PS•⁻ + substrat•⁺
  [Transfert d'électron → radicaux libres (O₂•⁻, HO•)]
  [Fonctionne même en hypoxie !]
  Condition : ΔE_ST < 0.12 eV, caractère CT de S₁
```

### Avantages et limites de la PDT

| Avantage | Limite |
|----------|--------|
| Sélectivité spatiale (lumière focalisée) | Dépend de l'O₂ (Type II) |
| Pas de résistance croisée avec chimio | Pénétration limitée (< 1 cm) |
| Effets secondaires locaux seulement | Photosensibilisation cutanée |
| Imagerie simultanée (fluorescence) | Hypoxie tumorale réduit l'efficacité |

---

## 2. Thérapie Photothermique (PTT)

### Principe
La PTT convertit l'énergie lumineuse en **chaleur locale** via des processus non-radiatifs, détruisant les cellules cancéreuses par hyperthermie (> 42°C).

### Mécanisme détaillé

```
Étape 1 : Absorption
  PS(S₀) + hν → PS(S₁)

Étape 2 : Conversion interne (IC) — voie non-radiative
  PS(S₁) → PS(S₀) + chaleur
  [Relaxation vibrationnelle rapide → chaleur locale]
  [Favorisée par : faible Φ_f, grande flexibilité moléculaire, torsion]

Étape 3 : Hyperthermie locale
  T > 42°C → dénaturation protéines → mort cellulaire
  T > 50°C → nécrose directe
```

### Indicateurs computationnels de l'efficacité PTT

Nous ne pouvons pas calculer directement η (rendement photothermal). Nous utilisons des **proxies** :

| Proxy PTT | Signification | Comment le calculer |
|-----------|--------------|---------------------|
| Faible f_S1 | Faible probabilité de fluorescence | Force d'oscillateur TD-DFT |
| Grande flexibilité | Relaxation vibrationnelle facile | RMSD planéité xTB |
| Torsion S₀→S₁ | Changement de géométrie à l'excitation | Angle dièdre S₀ vs S₁ |
| Faible Φ_f | Peu de fluorescence → plus de chaleur | Proxy : 1 - f_S1/f_max |

> **Important** : Ces proxies sont des indicateurs qualitatifs, pas des prédictions quantitatives de η. Toujours les présenter comme "propension PTT" et non comme "rendement PTT".

---

## 3. Pourquoi la synergie PDT + PTT ?

### Le problème de l'hypoxie pour la PDT Type II

```
Tumeur TNBC hypoxique
  [O₂] < 20 μM  (vs 200 μM en tissu normal)
       │
       ▼
PDT Type II inefficace
  PS(T₁) + ³O₂ → ¹O₂  ← pas assez d'O₂ !
       │
       ▼
Résistance à la PDT
```

### La solution : combiner PDT Type I + PTT

```
Irradiation NIR-I
       │
       ├─→ PDT Type I (radical, indépendant O₂)
       │     → Fonctionne même en hypoxie
       │
       ├─→ PDT Type II (¹O₂, si O₂ disponible)
       │     → Efficace dans les zones oxygénées
       │
       └─→ PTT (chaleur)
             → Augmente le flux sanguin → ↑ O₂ local
             → Potentialise la PDT Type II
             → Tue directement par hyperthermie
```

**Effet synergique** : La PTT augmente la perfusion tumorale, ce qui augmente la disponibilité en O₂, ce qui potentialise la PDT Type II. Les deux mécanismes se renforcent mutuellement.

---

## 4. Scoring synergique PDT/PTT

Pour comparer nos molécules, nous utilisons un score composite :

```
PDT_Score = 0.30 × (propension ¹O₂)
           + 0.30 × (SOC / 100)
           + 0.25 × (E_T1 / 1.5)
           + 0.15 × f_S1

PTT_Score = 0.40 × (propension non-radiative)
           + 0.35 × (indice de flexibilité)
           + 0.25 × (facteur de torsion)

Synergy_Score = 0.35 × PDT_Score
              + 0.35 × PTT_Score
              + 0.30 × (PDT_Score × PTT_Score)
```

Le terme d'interaction `γ × (PDT × PTT)` récompense les molécules **équilibrées** — ni trop PDT ni trop PTT, mais les deux à la fois.

> **⚠️ Avertissement** : Les poids (0.35, 0.35, 0.30) sont **exploratoires**. Ils reflètent une importance égale accordée à PDT et PTT. Toujours effectuer une analyse de sensibilité ±20% pour vérifier que le classement des molécules est robuste.

---

## 5. Classification PDT Type I vs Type II

| Critère | Type I | Type II |
|---------|--------|---------|
| ΔE_ST | < 0.12 eV | > 0.3 eV |
| SOC (S₁↔T₁) | > 30 cm⁻¹ | < 10 cm⁻¹ |
| E(T₁) | Quelconque | > 0.98 eV |
| Caractère S₁ | CT (transfert de charge) | LE (excitation locale) |
| Dépendance O₂ | **Non** | **Oui** |
| Efficacité en hypoxie | **Haute** | Faible |

> **Pour le TNBC hypoxique** : Préférer les molécules avec **Type I propensity > 0.6** (score continu 0–1, pas binaire).

---

## 6. Résumé visuel

```
Notre molécule BODIPY-NTR idéale :

                    λ_max = 650–750 nm (NIR-I)
                           │
                    Absorption efficace
                           │
              ┌────────────┴────────────┐
              │                         │
         ISC rapide                  IC rapide
    (ΔE_ST < 0.05 eV)           (faible Φ_f)
    (SOC > 50 cm⁻¹)             (grande flexibilité)
              │                         │
              ▼                         ▼
         PDT Type I               PTT (chaleur)
    (radicaux libres)         (hyperthermie locale)
    (indépendant O₂)
              │                         │
              └────────────┬────────────┘
                           │
                    Synergie thérapeutique
                    contre TNBC hypoxique
```

---

## 📖 Références clés

- Overchuk et al., *ACS Nano* 2023, 17, 7979 — Synergie PDT/PTT
- Ma et al., *J. Mater. Chem. B* 2021, 9, 7318 — BODIPY PTT
- Baig et al., *J. Comput. Chem.* 2025, 46, 7 — I-BODIPY, ΦT = 0.85

---

*Suite → [`04_NTR_trigger_hypoxie.md`](04_NTR_trigger_hypoxie.md)*
