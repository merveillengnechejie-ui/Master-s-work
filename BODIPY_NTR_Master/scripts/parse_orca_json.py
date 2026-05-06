#!/usr/bin/env python3
"""
parse_orca_json.py
Extraction robuste des résultats ORCA via les fichiers .property.json.
Nécessite ORCA 6.1.1+ et le module orca-pi (OPI 2.0).

Usage : python scripts/parse_orca_json.py
"""

import json
import os
import pandas as pd
from pathlib import Path

try:
    from opi.drivers import OrcaCalculator
    from opi.structure import Structure
    HAS_OPI = True
except ImportError:
    HAS_OPI = False
    print("⚠️  Module 'orca-pi' non trouvé. Utilisation de la méthode JSON directe.")


def extract_from_json(json_file):
    """Extrait les données d'un fichier .property.json d'ORCA."""
    with open(json_file, 'r') as f:
        data = json.load(f)
    
    results = {
        "molecule": Path(json_file).stem,
        "energy_Eh": data.get("ORCA_JSON_Data", {}).get("Energies", {}).get("Total_Energy"),
        "homo_ev": None,
        "lumo_ev": None,
        "lambda_max_nm": None,
        "f_osc": None
    }
    
    # Extraction des orbitales (pour HOMO-LUMO)
    orbitals = data.get("ORCA_JSON_Data", {}).get("Orbitals", [])
    if orbitals:
        # Trouver l'indice HOMO (dernière occupée)
        homos = [o for o in orbitals if o.get("Occupation") > 0]
        lumos = [o for o in orbitals if o.get("Occupation") == 0]
        if homos and lumos:
            results["homo_ev"] = homos[-1].get("Energy")
            results["lumo_ev"] = lumos[0].get("Energy")
            results["gap_ev"] = results["lumo_ev"] - results["homo_ev"]

    # Extraction des excitations TD-DFT
    excitations = data.get("ORCA_JSON_Data", {}).get("Excitation_Energies", [])
    if excitations:
        # Filtrer pour le premier état avec f > 0.01
        bright_states = [e for e in excitations if e.get("Oscillator_Strength", 0) > 0.01]
        if bright_states:
            first_bright = bright_states[0]
            results["lambda_max_nm"] = 1240.0 / (first_bright.get("Energy_eV"))
            results["f_osc"] = first_bright.get("Oscillator_Strength")

    return results


def main():
    base_dir = Path("calculations")
    all_results = []
    
    # Parcourir tous les fichiers .json générés par ORCA
    for json_path in base_dir.rglob("*.property.json"):
        print(f"Analyse de {json_path.name}...")
        try:
            res = extract_from_json(json_path)
            all_results.append(res)
        except Exception as e:
            print(f"❌ Erreur sur {json_path.name}: {e}")

    if all_results:
        df = pd.DataFrame(all_results)
        os.makedirs("results", exist_ok=True)
        df.to_csv("results/ORCA_structured_results.csv", index=False)
        print(f"\n✅ {len(all_results)} résultats extraits dans results/ORCA_structured_results.csv")
    else:
        print("\n❌ Aucun fichier .property.json trouvé. Vérifiez vos calculs ORCA.")


if __name__ == "__main__":
    main()
