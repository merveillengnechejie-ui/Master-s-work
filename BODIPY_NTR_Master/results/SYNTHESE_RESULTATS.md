# Synthèse des Résultats
## Tableau de bord du projet — À remplir au fur et à mesure

---

## 1. Benchmark TD-DFT

**Meilleure fonctionnelle** : _____________ (MAE = _____ eV)

| Fonctionnelle | MAE (eV) | RMSE (eV) | R² | Recommandée |
|---|---|---|---|---|
| ωB97X-D | | | | |
| CAM-B3LYP | | | | |
| PBE0 | | | | |
| B3LYP | | | | |
| M06-2X | | | | |
| MN15 | | | | |

---

## 2. Propriétés photophysiques — Toutes les molécules

| Molécule | État | λ_max (nm) | f_S1 | ΔE_ST TD-DFT (eV) | ΔE_ST Δ-DFT (eV) | SOC (cm⁻¹) | E_ad (eV) |
|----------|------|-----------|------|-----------------|-----------------|-----------|---------|
| BODIPY-Ph | S₀ | | | | | N/A | N/A |
| BODIPY-Ph-NO₂ | OFF | | | | | | |
| BODIPY-Ph-NH₂ | ON | | | | | | |
| Iodo-BODIPY | S₀ | | | | | N/A | N/A |
| Iodo-BODIPY-NO₂ | OFF | | | | | | |
| Iodo-BODIPY-NH₂ | ON | | | | | | |
| TPP-Iodo-BODIPY | S₀ | | | | | | |
| aza-BODIPY-NO₂ | OFF | | | | | | |
| aza-BODIPY-NH₂ | ON | | | | | | |

> **Note** : E_ad = énergie adiabatique S₁→S₀ (proxy PTT). N/A pour les molécules sans trigger NTR calculées en état fondamental uniquement.

---

## 3. Activation NTR — Switch ON/OFF

| Paire | Δλ_max (nm) | ΔΔE_ST (eV) | ΔSOC (cm⁻¹) | Δf | Switch efficace ? |
|-------|-----------|-----------|-----------|-----|-----------------|
| BODIPY-Ph | | | | | ☐ |
| Iodo-BODIPY | | | | | ☐ |
| aza-BODIPY | | | | | ☐ |

**Critères de succès** : Δλ_max > 20 nm **ET** ΔΔE_ST < −0.05 eV **ET** ΔSOC > +10 cm⁻¹

> **Rappel** : ΔX = X(ON) − X(OFF). Un ΔΔE_ST négatif signifie que l'activation NTR réduit l'écart singulet-triplet → ISC plus efficace → meilleure PDT.

---

## 4. Classification PDT Type I / Type II

| Molécule (ON) | ΔE_ST (eV) | SOC (cm⁻¹) | E(T₁) (eV) | Type I score | Classification |
|---|---|---|---|---|---|
| BODIPY-Ph-NH₂ | | | | | |
| Iodo-BODIPY-NH₂ | | | | | |
| aza-BODIPY-NH₂ | | | | | |

---

## 5. Scoring PDT/PTT

| Molécule | PDT_Score | PTT_Score | Synergy_Score | Rang | Go/No-Go |
|----------|----------|----------|--------------|------|---------|
| BODIPY-Ph-NH₂ | | | | | |
| Iodo-BODIPY-NH₂ | | | | | |
| aza-BODIPY-NH₂ | | | | | |
| TPP-Iodo-BODIPY | | | | | |

**Seuil Go** : Synergy_Score ≥ 0.70

---

## 6. Top 3 candidats recommandés

| Rang | Molécule | Synergy_Score | Points forts | Points faibles |
|------|----------|--------------|-------------|----------------|
| 1 | | | | |
| 2 | | | | |
| 3 | | | | |

---

## 7. Validation de la méthode Δ-DFT

| Molécule | ΔE_ST TD-DFT | ΔE_ST Δ-DFT | Différence | Δ-DFT nécessaire ? |
|----------|-------------|------------|-----------|-------------------|
| BODIPY-Ph | | | | |
| Iodo-BODIPY | | | | |

**Conclusion** : La différence TD-DFT vs Δ-DFT est de _____ eV en moyenne, ce qui confirme / infirme la nécessité d'utiliser Δ-DFT pour les BODIPY.

---

## 8. Fichiers de calcul archivés

| Calcul | Fichier .out | Fichier .gbw | Statut |
|--------|------------|------------|--------|
| S₀ BODIPY-Ph | | | ☐ |
| S₀ Iodo-BODIPY | | | ☐ |
| T₁ Iodo-BODIPY-NH₂ | | | ☐ |
| TD-DFT PBE0 BODIPY-Ph | | | ☐ |
| Δ-DFT Iodo-BODIPY-NH₂ | | | ☐ |
| SOC Iodo-BODIPY-NH₂ | | | ☐ |
