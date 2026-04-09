# Protocole P7 — Scoring PDT/PTT et Grille Go/No-Go
## Semaine 8

---

## 1. Script de scoring complet

```python
#!/usr/bin/env python3
# scripts/scoring_PDT_PTT.py

import pandas as pd
import numpy as np

def pdt_score(o2_propensity, soc_cm, E_T1_eV, f_S1):
    """Score PDT (0-1). Tous les paramètres normalisés."""
    return (0.30 * o2_propensity +
            0.30 * min(soc_cm / 100, 1.0) +
            0.25 * min(E_T1_eV / 1.5, 1.0) +
            0.15 * min(f_S1, 1.0))

def ptt_score(nr_propensity, flexibility, twist):
    """Score PTT (0-1). Proxies qualitatifs."""
    return (0.40 * nr_propensity +
            0.35 * flexibility +
            0.25 * twist)

def synergy_score(pdt, ptt, alpha=0.35, beta=0.35, gamma=0.30):
    """Score synergique avec terme d'interaction."""
    return alpha * pdt + beta * ptt + gamma * (pdt * ptt)

def o2_propensity(delta_E_ST, soc_cm, E_T1_eV):
    """Propension à générer ¹O₂ (Type II) ou radicaux (Type I)."""
    score = 0.0
    if E_T1_eV > 0.98:   # Seuil énergie ¹O₂
        score += 0.4
    if soc_cm > 10:
        score += 0.3 * min(soc_cm / 100, 1.0)
    if delta_E_ST < 0.3:
        score += 0.3 * (0.3 - delta_E_ST) / 0.3
    return min(score, 1.0)

# Charger les données
data = pd.read_csv("results/NTR_activation.csv")
soc  = pd.read_csv("results/SOC_results.csv")
df   = data.merge(soc, on="molecule")

# Calculer les scores (forme ON uniquement)
df_on = df[df["state"] == "ON"].copy()

df_on["o2_prop"]   = df_on.apply(
    lambda r: o2_propensity(r["delta_E_ST_deltaDFT"],
                             r["SOC_cm"], r["E_T1_eV"]), axis=1)
df_on["PDT_Score"] = df_on.apply(
    lambda r: pdt_score(r["o2_prop"], r["SOC_cm"],
                        r["E_T1_eV"], r["f_S1"]), axis=1)
df_on["PTT_Score"] = df_on.apply(
    lambda r: ptt_score(r["nr_propensity"],
                        r["flexibility"], r["twist"]), axis=1)
df_on["Synergy"]   = df_on.apply(
    lambda r: synergy_score(r["PDT_Score"], r["PTT_Score"]), axis=1)

df_on["GoNoGo"] = df_on["Synergy"].apply(
    lambda s: "Go ✓" if s >= 0.70 else "No-Go ✗")

# Afficher le classement
print(df_on[["molecule","PDT_Score","PTT_Score","Synergy","GoNoGo"]]
      .sort_values("Synergy", ascending=False)
      .to_string(index=False))

df_on.to_csv("results/PDT_PTT_synergy.csv", index=False)
```

---

## 2. Analyse de sensibilité (obligatoire)

```python
# scripts/sensitivity_analysis.py

import numpy as np
import pandas as pd

df = pd.read_csv("results/PDT_PTT_synergy.csv")

# Varier les poids ±20%
weight_sets = [
    (0.35, 0.35, 0.30),  # Nominal
    (0.42, 0.28, 0.30),  # PDT +20%
    (0.28, 0.42, 0.30),  # PTT +20%
    (0.35, 0.35, 0.36),  # γ +20%
    (0.35, 0.35, 0.24),  # γ -20%
]

print("Analyse de sensibilité — Classement des molécules")
print("=" * 60)

for alpha, beta, gamma in weight_sets:
    df["S_test"] = alpha*df["PDT_Score"] + beta*df["PTT_Score"] \
                 + gamma*(df["PDT_Score"]*df["PTT_Score"])
    ranking = df.sort_values("S_test", ascending=False)["molecule"].tolist()
    print(f"α={alpha}, β={beta}, γ={gamma}: {ranking[:3]}")
```

**Interprétation** : Si le top 3 reste stable pour tous les jeux de poids → le classement est robuste. Si le top 3 change → mentionner comme limitation dans le mémoire.

---

## 3. Grille Go/No-Go détaillée

| Critère | Iodo-BODIPY-NH₂ | aza-BODIPY-NH₂ | Poids |
|---------|----------------|----------------|-------|
| λ_max ∈ [650–750 nm] | ___/1 | ___/1 | 25% |
| ΔE_ST < 0.05 eV | ___/1 | ___/1 | 25% |
| SOC > 50 cm⁻¹ | ___/1 | ___/1 | 20% |
| Δλ_max ON/OFF > 20 nm | ___/1 | ___/1 | 15% |
| E_ad < 1.0 eV | ___/1 | ___/1 | 15% |
| **Score total** | **___/100%** | **___/100%** | |
| **Décision** | Go/No-Go | Go/No-Go | |

---

## 4. Livrable

- `results/PDT_PTT_synergy.csv`
- `results/sensitivity_analysis.md`
- Feuille de scoring complète (tableau ci-dessus rempli)
- Recommandation finale : top 3 candidats avec justification
