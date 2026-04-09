# Concept 2 — Le BODIPY : Structure et Propriétés Photophysiques
## Comprendre le "moteur photonique" de notre thérapie

---

## 1. Qu'est-ce qu'un BODIPY ?

**BODIPY** = **BO**ron-**DI**pyromethene = colorant à base de bore et de dipyrrométhène.

### Structure de base

```
        R₁    R₂
         \   /
    R₇    C=C    R₃
     \   / \ \  / \
      N     B     N
     / \   / \   / \
    R₈  C=C   C=C  R₄
        |       |
        R₅     R₆
              F F
```

Plus précisément, le squelette BODIPY numéroté :

```
         8    1
          \  /
    7      \/      2
     \    /  \    /
      N--B--N
     /    \  /    \
    6      /\      3
          /  \
         5    4
              |
             BF₂
```

**Positions clés pour la modification** :
- **meso (8)** : position centrale, très influente sur λ_max et le trigger NTR
- **2,6** : positions pour atomes lourds (Br, I) → augmente SOC → améliore PDT
- **3,5** : positions pour groupes donneurs/accepteurs → décale λ_max vers NIR
- **1,7** : positions pour groupes encombrants (tBu) → augmente PTT

---

## 2. Pourquoi les BODIPY sont-ils si intéressants ?

| Propriété | BODIPY | Avantage thérapeutique |
|-----------|--------|----------------------|
| Coefficient d'extinction ε | 50 000–100 000 M⁻¹cm⁻¹ | Absorption très efficace de la lumière |
| Rendement quantique Φ_f | 0.5–0.9 (sans atome lourd) | Fluorescence pour imagerie |
| Photostabilité | Excellente | Résiste à la dégradation sous irradiation |
| Modularité | Très haute | Facile à modifier chimiquement |
| Solubilité | Ajustable | Peut être rendu hydrosoluble |
| Toxicité intrinsèque | Faible | Sûr en l'absence de lumière |

---

## 3. Les propriétés photophysiques clés

### 3.1 L'absorption (λ_max)

La longueur d'onde d'absorption maximale dépend du **gap HOMO-LUMO** :

```
E_photon = hc/λ = E_LUMO - E_HOMO

Plus le gap est petit → λ_max plus grand (rouge/NIR)
Plus le gap est grand → λ_max plus petit (bleu/vert)
```

**BODIPY non substitué** : λ_max ≈ 500–520 nm (vert) — trop court pour la thérapie  
**Notre cible** : λ_max = 650–750 nm (NIR-I)

### 3.2 Le diagramme de Jablonski

```
                    S₁ ─────────────────────────────
                   /│\                              │
                  / │ \  Conversion interne (IC)    │ Fluorescence
                 /  │  \  (chaleur → PTT)           │ (imagerie)
                /   │   \                           │
               /    │    ▼                          │
              /     │    T₁ ──────────────────────  │
             /      │   /│\                    │    │
            /       │  / │ \  Phosphorescence  │    │
           /        │ /  │  \                  │    │
          /         │/   │   ▼                 │    │
         S₀ ────────────────────────────────────────
                    │
                    │ Absorption (hν)
                    │ λ = 650–750 nm
```

**Transitions importantes** :
- **S₀ → S₁** : absorption de photon (notre λ_max)
- **S₁ → S₀** : fluorescence (imagerie diagnostique)
- **S₁ → T₁** : ISC (intersystem crossing) → crucial pour PDT
- **T₁ → ³O₂** : transfert d'énergie → génération ¹O₂ (PDT Type II)
- **S₁ → S₀** via IC : chaleur (PTT)

### 3.3 L'écart singulet-triplet ΔE_ST

```
ΔE_ST = E(S₁) - E(T₁)
```

C'est l'une des propriétés les plus importantes pour la PDT :

| ΔE_ST | Conséquence | Thérapie |
|-------|-------------|---------|
| < 0.05 eV | ISC très efficace | PDT excellente |
| 0.05–0.15 eV | ISC modérée | PDT bonne |
| > 0.3 eV | ISC lente | PDT faible |

> **Règle pratique** : Plus ΔE_ST est petit, plus la molécule passe facilement de S₁ à T₁, et plus la PDT est efficace.

---

## 4. Règles de design pour décaler λ_max vers le NIR

### 4.1 Groupes donneurs d'électrons (EDG) aux positions 3,5

Les groupes donneurs (—NMe₂, —Ph, —thienyl) augmentent la densité électronique sur le BODIPY, réduisant le gap HOMO-LUMO :

```
BODIPY-H          : λ_max ≈ 505 nm
BODIPY-3,5-Ph     : λ_max ≈ 540 nm  (+35 nm)
BODIPY-3,5-NMe₂   : λ_max ≈ 580 nm  (+75 nm)
BODIPY-distyryl   : λ_max ≈ 650 nm  (+145 nm)
```

### 4.2 Atomes lourds aux positions 2,6 (effet d'atome lourd)

L'iode et le brome augmentent le **couplage spin-orbite (SOC)** par interaction relativiste :

```
BODIPY-H          : SOC ≈ 1–5 cm⁻¹   → ISC lente
BODIPY-2,6-Br₂    : SOC ≈ 30–60 cm⁻¹ → ISC modérée
BODIPY-2,6-I₂     : SOC ≈ 80–150 cm⁻¹ → ISC rapide ← NOTRE CHOIX
```

### 4.3 aza-BODIPY (substitution N à la position meso)

Remplacer le carbone meso par un azote crée un **aza-BODIPY** avec un fort décalage vers le rouge :

```
BODIPY standard   : λ_max ≈ 500–520 nm
aza-BODIPY        : λ_max ≈ 650–750 nm  (+150–230 nm)
```

---

## 5. L'effet du trigger NTR sur les propriétés optiques

C'est le cœur de notre projet. Voici ce qui se passe quand NTR réduit —NO₂ en —NH₂ :

### Forme OFF (—NO₂, prodrug)

```
—NO₂ est un groupe ACCEPTEUR d'électrons (EWG)
→ Quench la fluorescence par PET (Photoinduced Electron Transfer)
→ λ_max décalé vers le bleu (hypsochrome)
→ Φ_f très faible (< 0.05)
→ Pas de génération ¹O₂ efficace
→ INACTIF thérapeutiquement
```

### Forme ON (—NH₂, activée)

```
—NH₂ est un groupe DONNEUR d'électrons (EDG)
→ PET supprimé → fluorescence restaurée
→ λ_max décalé vers le rouge (bathochrome) : Δλ_max = +20 à +60 nm
→ Φ_f augmente (0.3–0.7)
→ ΔE_ST diminue → ISC plus efficace
→ ACTIF thérapeutiquement
```

**Ce que nous calculons** :
```
Δλ_max = λ_max(ON) - λ_max(OFF)  → cible : > 20 nm
ΔΔE_ST = ΔE_ST(ON) - ΔE_ST(OFF)  → cible : négatif (ΔE_ST diminue)
ΔSOC   = SOC(ON) - SOC(OFF)       → cible : positif (SOC augmente)
```

---

## 6. Résumé des propriétés cibles pour notre projet

| Propriété | Valeur cible | Méthode de calcul |
|-----------|-------------|-------------------|
| λ_max (forme ON) | 650–750 nm | TD-DFT/ωB97X-D/def2-SVP |
| ΔE_ST (forme ON) | < 0.05 eV | Δ-DFT (ΔROKS/PBE0) |
| SOC (forme ON) | > 50 cm⁻¹ (avec I) | ΔDFT+SOC (ZORA) |
| Δλ_max ON/OFF | > 20 nm | TD-DFT comparatif |
| E_ad (S₁→S₀) | < 1.0 eV | ΔUKS |
| SA Score | < 5.0 | RDKit |

---

## 📖 Références clés

- Bartusik-Aebisher et al., *Pharmaceuticals* 2025, 18, 53
- Baig et al., *J. Comput. Chem.* 2025, 46, 7 — I-BODIPY TSH-MD
- Alkhatib et al., *RSC Adv.* 2022, 12, 1704 — benchmark 36 fonctionnelles

---

*Suite → [`03_PDT_PTT_mecanismes.md`](03_PDT_PTT_mecanismes.md)*
