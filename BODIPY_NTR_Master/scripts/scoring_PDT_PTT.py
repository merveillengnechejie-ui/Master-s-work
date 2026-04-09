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


# ─── Fonctions de scoring ────────────────────────────────────────────────────

def o2_propensity(delta_E_ST_eV, soc_cm, E_T1_eV):
    """
    Propension à générer des espèces réactives de l'oxygène (0–1).
    Combine les critères PDT Type I et Type II.
    """
    score = 0.0
    # T1 > 0.98 eV : énergie suffisante pour sensibiliser ¹O₂ (Type II)
    if E_T1_eV is not None and E_T1_eV > 0.98:
        score += 0.40
    # SOC élevé → ISC rapide → peuplement T1 efficace
    if soc_cm is not None and soc_cm > 0:
        score += 0.30 * min(soc_cm / 100.0, 1.0)
    # ΔE_ST petit → ISC thermiquement accessible
    if delta_E_ST_eV is not None and delta_E_ST_eV < 0.30:
        score += 0.30 * (0.30 - delta_E_ST_eV) / 0.30
    return min(score, 1.0)


def pdt_score(o2_prop, soc_cm, E_T1_eV, f_S1):
    """Score PDT (0–1)."""
    soc_norm = min((soc_cm or 0) / 100.0, 1.0)
    E_T1_norm = min((E_T1_eV or 0) / 1.5, 1.0)
    f_norm = min((f_S1 or 0), 1.0)
    return (0.30 * o2_prop +
            0.30 * soc_norm +
            0.25 * E_T1_norm +
            0.15 * f_norm)


def ptt_score(nr_propensity, flexibility, twist):
    """
    Score PTT (0–1).
    Ces proxies sont qualitatifs — les présenter comme 'propension PTT'.
    nr_propensity : 1 - f_S1 normalisé (faible fluorescence → plus de chaleur)
    flexibility   : indice de flexibilité xTB (rotatable bonds normalisé)
    twist         : changement d'angle dièdre S0→T1 normalisé
    """
    return (0.40 * min(nr_propensity, 1.0) +
            0.35 * min(flexibility, 1.0) +
            0.25 * min(twist, 1.0))


def synergy_score(pdt, ptt, alpha=0.35, beta=0.35, gamma=0.30):
    """
    Score synergique PDT/PTT avec terme d'interaction.
    Le terme gamma*(pdt*ptt) récompense les molécules équilibrées.
    ⚠️ Les poids sont exploratoires — toujours effectuer l'analyse de sensibilité.
    """
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

    # Fusionner et filtrer forme ON uniquement
    df = ntr.merge(soc, on="molecule", how="left")
    df_on = df[df["state"] == "ON"].copy()

    if df_on.empty:
        print("❌ Aucune molécule en état 'ON' trouvée dans NTR_activation.csv")
        return

    # Calculer les proxies PTT (à partir des données disponibles)
    # nr_propensity : 1 - f_S1 normalisé (faible f → plus de chaleur)
    f_max = df_on["f_S1"].max() if "f_S1" in df_on.columns else 1.0
    df_on["nr_propensity"] = 1.0 - df_on.get("f_S1", 0) / max(f_max, 1e-6)
    # flexibility et twist : à remplir depuis xTB_screening.csv si disponible
    df_on["flexibility"] = df_on.get("flexibility_index", 0.5)
    df_on["twist"]       = df_on.get("twist_factor", 0.5)

    # Calculer les scores
    df_on["o2_prop"]   = df_on.apply(
        lambda r: o2_propensity(r.get("delta_E_ST_deltaDFT"),
                                r.get("SOC_cm"),
                                r.get("E_T1_eV")), axis=1)
    df_on["PDT_Score"] = df_on.apply(
        lambda r: pdt_score(r["o2_prop"], r.get("SOC_cm"),
                            r.get("E_T1_eV"), r.get("f_S1")), axis=1)
    df_on["PTT_Score"] = df_on.apply(
        lambda r: ptt_score(r["nr_propensity"],
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
