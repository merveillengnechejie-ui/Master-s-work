#!/usr/bin/env python3
"""
scoring_PDT_PTT.py
Calcule les scores PDT, PTT et synergique pour toutes les molécules ON.
Effectue l'analyse de sensibilité sur les poids.

Usage : python scripts/scoring_PDT_PTT.py
Prérequis : results/NTR_activation.csv et results/SOC_results.csv doivent exister.
"""

import pandas as pd
import numpy as np
import os


# ─── Configuration du Scoring (Audit #753) ───────────────────────────────────

CONFIG = {
    "SOC_NORM": 150.0,      # Constante SOC cible (cm-1)
    "T1_NORM": 1.5,         # Énergie T1 cible (eV)
    "T1_THRESHOLD": 0.98,   # Seuil pour sensibilisation 1O2 (eV)
    "DE_ST_THRESHOLD": 0.20,# Seuil pour ISC efficace (eV)
    "SR_TARGET": 10.0,      # Ratio de sélectivité cible (ON/OFF)
    "LAMBDA_NORM": 0.4,     # Énergie de réorganisation cible (eV)
    "WEIGHTS_DEFAULT": (0.35, 0.35, 0.30), # Alpha, Beta, Gamma
}


# ─── Fonctions de scoring ────────────────────────────────────────────────────

def o2_propensity(delta_E_ST_eV, soc_cm, E_T1_eV):
    """
    Propension à générer des espèces réactives de l'oxygène (0–1).
    Combine les critères PDT Type I et Type II.
    """
    score = 0.0
    # T1 > Seuil : énergie suffisante pour sensibiliser ¹O₂ (Type II)
    if E_T1_eV is not None and E_T1_eV > CONFIG["T1_THRESHOLD"]:
        score += 0.40
    # SOC élevé → ISC rapide → peuplement T1 efficace
    if soc_cm is not None and soc_cm > 0:
        score += 0.30 * min(soc_cm / CONFIG["SOC_NORM"], 1.0)
    # ΔE_ST petit → ISC thermiquement accessible
    if delta_E_ST_eV is not None and delta_E_ST_eV < CONFIG["DE_ST_THRESHOLD"]:
        score += 0.30 * (CONFIG["DE_ST_THRESHOLD"] - delta_E_ST_eV) / CONFIG["DE_ST_THRESHOLD"]
    return min(score, 1.0)


def pdt_score(o2_prop, soc_cm, E_T1_eV, f_S1, selectivity_ratio=1.0):
    """
    Score PDT (0–1).
    selectivity_ratio : Φ_Δ(ON) / Φ_Δ(OFF). Target > SR_TARGET.
    """
    soc_norm = min((soc_cm or 0) / CONFIG["SOC_NORM"], 1.0)
    E_T1_norm = min((E_T1_eV or 0) / CONFIG["T1_NORM"], 1.0)
    f_norm = min((f_S1 or 0), 1.0)
    sr_norm = min(selectivity_ratio / CONFIG["SR_TARGET"], 1.0)
    
    return (0.25 * o2_prop +
            0.20 * soc_norm +
            0.20 * E_T1_norm +
            0.15 * f_norm +
            0.20 * sr_norm)


def ptt_score(reorganization_energy_ev, flexibility, twist):
    """
    Score PTT (0–1).
    reorganization_energy_ev (λ) : Proxy primaire (Audit #753).
    """
    lambda_norm = min((reorganization_energy_ev or 0) / CONFIG["LAMBDA_NORM"], 1.0)
    
    return (0.40 * lambda_norm +
            0.35 * min(flexibility, 1.0) +
            0.25 * min(twist, 1.0))


def synergy_score(pdt, ptt, alpha=None, beta=None, gamma=None):
    """
    Score synergique PDT/PTT avec terme d'interaction.
    """
    a, b, g = CONFIG["WEIGHTS_DEFAULT"]
    alpha = alpha if alpha is not None else a
    beta  = beta  if beta  is not None else b
    gamma = gamma if gamma is not None else g
    
    return alpha * pdt + beta * ptt + gamma * (pdt * ptt)


# ─── Analyse de sensibilité ──────────────────────────────────────────────────

WEIGHT_SETS = [
    (0.35, 0.35, 0.30, "Nominal"),
    (0.42, 0.28, 0.30, "PDT +20%"),
    (0.28, 0.42, 0.30, "PTT +20%"),
    (0.35, 0.35, 0.36, "γ +20%"),
    (0.35, 0.35, 0.24, "γ -20%"),
    (0.40, 0.40, 0.20, "Synergie réduite"),
]


def sensitivity_analysis(df_on):
    """Vérifie la stabilité du classement sous variation des poids."""
    print("\n" + "=" * 65)
    print("ANALYSE DE SENSIBILITÉ — Stabilité du classement")
    print("=" * 65)
    print(f"{'Scénario':<22} {'Top 1':<25} {'Top 2':<25} {'Top 3'}")
    print("-" * 65)

    rankings = {}
    for alpha, beta, gamma, label in WEIGHT_SETS:
        df_on["S_test"] = df_on.apply(
            lambda r: synergy_score(r["PDT_Score"], r["PTT_Score"],
                                    alpha, beta, gamma), axis=1)
        top3 = df_on.nlargest(3, "S_test")["molecule"].tolist()
        rankings[label] = top3
        t1 = top3[0] if len(top3) > 0 else "—"
        t2 = top3[1] if len(top3) > 1 else "—"
        t3 = top3[2] if len(top3) > 2 else "—"
        print(f"{label:<22} {t1:<25} {t2:<25} {t3}")

    # Vérifier la stabilité
    all_top1 = set(r[0] for r in rankings.values() if r)
    if len(all_top1) == 1:
        print(f"\n✅ Classement STABLE : '{list(all_top1)[0]}' reste #1 pour tous les scénarios.")
    else:
        print(f"\n⚠️  Classement INSTABLE : le #1 change selon les poids → mentionner comme limitation.")

    return rankings


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    # Vérifier les fichiers d'entrée
    required = ["results/NTR_activation.csv", "results/SOC_results.csv"]
    for f in required:
        if not os.path.exists(f):
            print(f"❌ Fichier manquant : {f}")
            print("   Lancer d'abord parse_orca_results.py et compléter NTR_activation.csv")
            return

    # Charger les données
    ntr = pd.read_csv("results/NTR_activation.csv")
    soc = pd.read_csv("results/SOC_results.csv")

    # Calcul du Selectivity Ratio (SR) : ON / OFF
    # On compare la propension PDT (proxy de Φ_Δ)
    # ⚠️ Nécessite les deux formes pour chaque molécule
    sr_data = []
    for mol in ntr["molecule"].unique():
        m_data = ntr[ntr["molecule"] == mol]
        on_state = m_data[m_data["state"] == "ON"]
        off_state = m_data[m_data["state"] == "OFF"]
        
        if not on_state.empty and not off_state.empty:
            # On utilise f_S1 comme proxy de Φ_f pour le ratio de sélectivité
            f_on = on_state["f_S1"].values[0]
            f_off = off_state["f_S1"].values[0]
            sr = f_on / max(f_off, 1e-3)
            sr_data.append({"molecule": mol, "selectivity_ratio": sr})
    
    df_sr = pd.DataFrame(sr_data)

    # Fusionner et filtrer forme ON uniquement pour le scoring final
    df = ntr.merge(soc, on="molecule", how="left")
    df = df.merge(df_sr, on="molecule", how="left")
    df_on = df[df["state"] == "ON"].copy()

    if df_on.empty:
        print("❌ Aucune molécule en état 'ON' trouvée dans NTR_activation.csv")
        return

    # Remplir les valeurs manquantes
    df_on["selectivity_ratio"] = df_on["selectivity_ratio"].fillna(1.0)

    # Proxies PTT (Audit #753)
    # λ (reorganization energy) : E(S1@S0) - E(S1@S1)
    # À défaut de géométrie S1 optimisée, on utilise le Stokes Shift normalisé
    if "reorganization_energy_ev" not in df_on.columns:
        # Proxy : λ ≈ 0.5 * Stokes_Shift (eV)
        df_on["reorganization_energy_ev"] = df_on.get("stokes_shift_ev", 0.2) * 0.5
    
    df_on["flexibility"] = df_on.get("flexibility_index", 0.5)
    df_on["twist"]       = df_on.get("twist_factor", 0.5)

    # Calculer les scores
    df_on["o2_prop"]   = df_on.apply(
        lambda r: o2_propensity(r.get("delta_E_ST_deltaDFT"),
                                r.get("SOC_cm"),
                                r.get("E_T1_eV")), axis=1)
    
    df_on["PDT_Score"] = df_on.apply(
        lambda r: pdt_score(r["o2_prop"], r.get("SOC_cm"),
                            r.get("E_T1_eV"), r.get("f_S1"),
                            r.get("selectivity_ratio")), axis=1)
    
    df_on["PTT_Score"] = df_on.apply(
        lambda r: ptt_score(r["reorganization_energy_ev"],
                            r["flexibility"], r["twist"]), axis=1)
    
    df_on["Synergy_Score"] = df_on.apply(
        lambda r: synergy_score(r["PDT_Score"], r["PTT_Score"]), axis=1)
    
    df_on["GoNoGo"] = df_on["Synergy_Score"].apply(
        lambda s: "Go ✓" if s >= 0.70 else "No-Go ✗")


    # Afficher le classement
    print("\n" + "=" * 65)
    print("CLASSEMENT PDT/PTT — Molécules activées (forme ON)")
    print("=" * 65)
    cols = ["molecule", "PDT_Score", "PTT_Score", "Synergy_Score", "GoNoGo"]
    print(df_on[cols].sort_values("Synergy_Score", ascending=False)
          .to_string(index=False, float_format="{:.3f}".format))

    # Analyse de sensibilité
    sensitivity_analysis(df_on.copy())

    # Sauvegarder
    os.makedirs("results", exist_ok=True)
    df_on.to_csv("results/PDT_PTT_synergy.csv", index=False)
    print(f"\n✅ Résultats sauvegardés : results/PDT_PTT_synergy.csv")


if __name__ == "__main__":
    main()
