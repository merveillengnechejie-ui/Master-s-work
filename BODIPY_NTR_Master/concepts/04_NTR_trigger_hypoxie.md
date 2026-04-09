# Concept 4 — La Nitroreductase (NTR) : L'Interrupteur Moléculaire
## Comment transformer un prodrug inactif en agent thérapeutique actif

---

## 1. Qu'est-ce qu'un prodrug ?

Un **prodrug** est une molécule inactive qui se transforme en médicament actif sous l'action d'une enzyme ou d'une condition biologique spécifique.

```
Prodrug (inactif)  →  Enzyme/Condition  →  Médicament actif
BODIPY-NO₂ (OFF)  →  NTR + NADPH       →  BODIPY-NH₂ (ON)
```

**Avantage** : La molécule ne cause pas d'effets secondaires dans les tissus normaux. Elle n'est activée que là où l'enzyme est présente (tumeur hypoxique).

---

## 2. Réaction de réduction NTR

### Réaction chimique

```
Ar—NO₂  +  3 NADPH  +  3 H⁺  →  Ar—NH₂  +  3 NADP⁺  +  2 H₂O
  (nitro)    (cofacteur)              (amine)

Ar = squelette aromatique (ici : phényle lié au BODIPY en position meso)
```

### Conditions requises

| Condition | Valeur | Signification |
|-----------|--------|---------------|
| Enzyme | NTR (nfsA/nfsB homologs) | Nitroreductase bactérienne/mammifère |
| Cofacteur | NADPH | Nicotinamide adénine dinucléotide phosphate |
| O₂ | < 20 μM (hypoxique) | La réaction est inhibée par l'O₂ |
| pH | 6.5–7.4 | Compatible avec le TME |

> **Clé de la sélectivité** : En présence d'O₂ (tissu normal), NADPH est réoxydé avant de réduire le nitro. En hypoxie (tumeur), NADPH est disponible pour la réduction. C'est ce qui rend le trigger NTR hypoxie-sélectif.

---

## 3. Les trois types de triggers NTR

| Trigger | Forme réduite | Sélectivité | Avantage | Inconvénient |
|---------|--------------|-------------|----------|--------------|
| **—Ph-NO₂ (meso)** | —Ph-NH₂ | **Haute** | Bien caractérisé, stable | Δλ_max modéré |
| **—NO₂ direct (meso)** | —NH₂ direct | **Haute** | Perturbation électronique forte | Synthèse plus difficile |
| **—N=N— (azo)** | —NH₂ + aldéhyde | **Modérée** | Clivage irréversible | Azoreductase active en normoxie |

**Notre choix principal** : —Ph-NO₂ en position meso (meilleur compromis sélectivité/synthèse).

---

## 4. Effet du trigger sur les propriétés photophysiques

### Pourquoi —NO₂ éteint la fluorescence (PET)

Le mécanisme d'extinction est le **PET (Photoinduced Electron Transfer)** :

```
État excité S₁ du BODIPY
        │
        │  Transfert d'électron
        ▼
    Orbitale du groupe —NO₂
    (accepteur d'électrons)
        │
        ▼
    Retour non-radiatif vers S₀
    → Pas de fluorescence
    → Pas de génération ¹O₂
    → INACTIF
```

### Pourquoi —NH₂ restaure l'activité

```
—NH₂ est un DONNEUR d'électrons
→ Pas de PET (le groupe NH₂ donne des électrons au BODIPY)
→ S₁ se désexcite normalement
→ Fluorescence restaurée
→ ISC possible → T₁ → ¹O₂
→ ACTIF
```

### Changements quantitatifs attendus

```
Propriété          OFF (—NO₂)    ON (—NH₂)    Δ
─────────────────────────────────────────────────
λ_max              ~620 nm       ~660 nm      +40 nm
Φ_f                < 0.05        ~0.4         +0.35
ΔE_ST              ~0.3 eV       ~0.05 eV     -0.25 eV
SOC                ~5 cm⁻¹       ~60 cm⁻¹     +55 cm⁻¹
f_S1               ~0.1          ~0.8         +0.7
```

> **Note** : Ces valeurs sont des estimations basées sur la littérature. Vos calculs produiront les valeurs réelles pour vos molécules spécifiques.

---

## 5. Ce que nous calculons pour caractériser l'activation NTR

Pour chaque molécule NTR, nous effectuons les calculs dans les **deux états** :

```
Molécule-NO₂ (OFF)          Molécule-NH₂ (ON)
      │                            │
      ▼                            ▼
  S₀ optimisé               S₀ optimisé
      │                            │
      ▼                            ▼
  TD-DFT vertical            TD-DFT vertical
  → λ_max(OFF)               → λ_max(ON)
      │                            │
      ▼                            ▼
  T₁ optimisé                T₁ optimisé
      │                            │
      ▼                            ▼
  Δ-DFT → ΔE_ST(OFF)         Δ-DFT → ΔE_ST(ON)
      │                            │
      ▼                            ▼
  SOC(OFF)                   SOC(ON)
      │                            │
      └──────────┬─────────────────┘
                 │
                 ▼
         Δλ_max, ΔΔE_ST, ΔSOC
         → Quantification du switch ON/OFF
```

---

## 6. Critères de succès pour le trigger NTR

| Critère | Valeur cible | Signification |
|---------|-------------|---------------|
| Δλ_max (ON − OFF) | > 20 nm | Décalage spectral détectable |
| ΔΔE_ST (ON − OFF) | < −0.1 eV | ΔE_ST diminue à l'activation |
| ΔSOC (ON − OFF) | > +20 cm⁻¹ | SOC augmente à l'activation |
| Φ_f(ON) / Φ_f(OFF) | > 10 | Rapport signal/bruit pour imagerie |

---

## 7. Contrôle négatif : le trigger azo

Le trigger azo (—N=N—) est inclus dans notre bibliothèque comme **contrôle négatif de sélectivité** :

```
—N=N—  →  azoreductase  →  —NH₂ + aldéhyde

Problème : l'azoreductase est active en normoxie ET en hypoxie
→ Activation non sélective
→ Effets secondaires dans les tissus normaux
→ Sert à démontrer que notre trigger Ph-NO₂ est MEILLEUR
```

---

## 📖 Références clés

- Bartusik-Aebisher et al., *Pharmaceuticals* 2025, 18, 53
- Kong et al., *Prog. Mater. Sci.* 2023, 134, 101070

---

*Suite → [`05_DFT_pour_debutants.md`](05_DFT_pour_debutants.md)*
