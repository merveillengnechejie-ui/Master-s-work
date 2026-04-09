# Protocole P5 — Protocole Dual-State NTR : ON vs OFF
## Semaines 5–6 — Quantifier le switch photophysique

---

## Objectif

Pour chaque molécule NTR, calculer les propriétés photophysiques dans les **deux états** (nitro = OFF, amine = ON) et quantifier le switch d'activation.

---

## 1. Les paires de molécules à calculer

| Paire | Forme OFF (—NO₂) | Forme ON (—NH₂) |
|-------|-----------------|----------------|
| 1 | BODIPY-Ph-NO₂ | BODIPY-Ph-NH₂ |
| 2 | Iodo-BODIPY-Ph-NO₂ | Iodo-BODIPY-Ph-NH₂ |
| 3 | aza-BODIPY-NO₂ | aza-BODIPY-NH₂ |

---

## 2. Workflow complet pour une paire

```
Forme OFF (—NO₂)              Forme ON (—NH₂)
      │                              │
      ▼                              ▼
  xTB opt                        xTB opt
  (--alpb water)                 (--alpb water)
      │                              │
      ▼                              ▼
  S₀ opt ORCA                    S₀ opt ORCA
  (B3LYP-D3/def2-SVP)           (B3LYP-D3/def2-SVP)
      │                              │
      ▼                              ▼
  TD-DFT vertical                TD-DFT vertical
  (meilleure fonctionnelle)      (meilleure fonctionnelle)
  + ptSS-PCM                     + ptSS-PCM
  → λ_max(OFF), f(OFF)           → λ_max(ON), f(ON)
      │                              │
      ▼                              ▼
  T₁ opt (UKS)                   T₁ opt (UKS)
      │                              │
      ▼                              ▼
  Δ-DFT ΔE_ST(OFF)               Δ-DFT ΔE_ST(ON)
      │                              │
      ▼                              ▼
  SOC(OFF)                       SOC(ON)
      │                              │
      └──────────────┬───────────────┘
                     │
                     ▼
             Calcul des deltas :
             Δλ_max = λ_max(ON) - λ_max(OFF)
             ΔΔE_ST = ΔE_ST(ON) - ΔE_ST(OFF)
             ΔSOC   = SOC(ON) - SOC(OFF)
             Δf     = f(ON) - f(OFF)
```

---

## 3. Input S₀ optimisation (commun OFF et ON)

```orca
# BODIPY_Ph_NO2_S0_opt.inp  (changer NO2 en NH2 pour la forme ON)

! Opt RKS B3LYP D3BJ def2-SVP AutoAux RIJCOSX TightSCF TIGHTOPT
! CPCM(water)
%pal nprocs 4 end
%maxcore 7000
%cpcm
  SMD true
  SMDSolvent "water"
end
%geom
  MaxStep 0.2
  Trust 0.3
end
* xyzfile 0 1 ../tier0_xtb/BODIPY_Ph_NO2_S0_T0_opt.xyz
```

---

## 4. Input TD-DFT vertical (avec ptSS-PCM)

```orca
# BODIPY_Ph_NO2_T2_wB97XD.inp

! RKS wB97X-D def2-SVP AutoAux RIJCOSX TightSCF
! CPCM(water)
%pal nprocs 4 end
%maxcore 7000
%cpcm
  SMD true
  SMDSolvent "water"
  StateSpecificSolvation true
end
%tddft
  n_roots 10
  DoNTOs true
  PrintNTOs true
end
* xyzfile 0 1 ../S0_opt/BODIPY_Ph_NO2_S0_opt.xyz
```

---

## 5. Input T₁ optimisation (ΔUKS)

```orca
# BODIPY_Ph_NO2_T1_opt.inp

! Opt UKS PBE0 D3BJ def2-SVP AutoAux RIJCOSX TightSCF TIGHTOPT
! CPCM(water)
%pal nprocs 4 end
%maxcore 7000
%cpcm
  SMD true
  SMDSolvent "water"
end
%scf
  HFTyp UKS
  SCF_ALGORITHM DIIS_TRAH
  MaxIter 500
  ConvForce 1e-6
end
%geom
  MaxStep 0.2
  Trust 0.3
end
* xyz 0 3
[Copier les coordonnées de S0_opt.xyz ici]
*
```

**Vérification après T₁ opt** : Dans le `.out`, chercher :
```
<S**2> =  2.0xxx   ← doit être entre 2.00 et 2.10
```
Si `<S²>` > 2.1 → contamination de spin → utiliser ΔROKS à la place.

---

## 6. Tableau de collecte des résultats

Remplir `results/NTR_activation.csv` :

| Molécule | État | λ_max (nm) | f_S1 | ΔE_ST (eV) | SOC (cm⁻¹) | E_ad (eV) |
|----------|------|-----------|------|-----------|-----------|---------|
| BODIPY-Ph-NO₂ | OFF | | | | | |
| BODIPY-Ph-NH₂ | ON | | | | | |
| Δ (ON−OFF) | | | | | | |
| Iodo-BODIPY-NO₂ | OFF | | | | | |
| Iodo-BODIPY-NH₂ | ON | | | | | |
| Δ (ON−OFF) | | | | | | |

---

## 7. Critères de succès du switch NTR

| Critère | Valeur cible | Interprétation |
|---------|-------------|----------------|
| Δλ_max | > 20 nm | Décalage spectral détectable |
| ΔΔE_ST | < −0.05 eV | ΔE_ST diminue → ISC s'améliore |
| ΔSOC | > +10 cm⁻¹ | SOC augmente → ISC s'accélère |
| Δf | > +0.2 | Absorption plus forte à l'activation |

**Si Δλ_max < 10 nm** : Le trigger NTR n'est pas efficace pour cette molécule. Discuter dans le mémoire comme limitation de design.

---

## 8. Classification PDT Type I vs Type II

Pour chaque molécule en forme ON, calculer le score Type I :

```python
def type_I_score(delta_E_ST, SOC, E_T1, NTO_overlap):
    """
    Score continu 0-1 pour la propension PDT Type I.
    0 = pur Type II, 1 = pur Type I
    """
    score = 0.0
    # ΔE_ST < 0.12 eV → Type I favorisé
    if delta_E_ST < 0.12:
        score += 0.4 * (0.12 - delta_E_ST) / 0.12
    # SOC élevé → ISC rapide → Type I possible
    if SOC > 10:
        score += 0.3 * min(SOC / 100, 1.0)
    # Faible chevauchement NTO → caractère CT → Type I
    score += 0.3 * (1 - NTO_overlap)
    return min(score, 1.0)
```

**Interprétation** :
- Score > 0.6 → Type I dominant → efficace en hypoxie ✓
- Score 0.3–0.6 → mécanisme mixte
- Score < 0.3 → Type II dominant → moins efficace en hypoxie

---

## 9. Livrable

- `results/NTR_activation.csv` — propriétés ON/OFF pour toutes les paires
- `results/PDT_mechanism.csv` — scores Type I/II
- Figure : overlay spectres ON/OFF pour les 3 meilleures molécules
