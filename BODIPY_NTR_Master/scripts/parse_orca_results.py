#!/usr/bin/env python3
"""
parse_orca_results.py
Extrait les propriétés clés de tous les fichiers .out ORCA du projet.
Usage : python scripts/parse_orca_results.py
"""

import re
import os
import csv
from pathlib import Path


def extract_tddft(outfile):
    """Extrait λ_max (nm) et f_S1 du premier état excité avec f > 0.01."""
    with open(outfile) as f:
        content = f.read()
    # Tableau d'absorption ORCA
    pattern = r'(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)'
    for state, energy_cm, wavelength, fosc in re.findall(pattern, content):
        if float(fosc) > 0.01:
            return float(wavelength), float(fosc)
    return None, None


def extract_final_energy(outfile):
    """Extrait l'énergie SCF finale en Hartree."""
    with open(outfile) as f:
        content = f.read()
    matches = re.findall(r'FINAL SINGLE POINT ENERGY\s+([-\d.]+)', content)
    return float(matches[-1]) if matches else None


def extract_soc(outfile):
    """Extrait la constante SOC S1<->T1 en cm-1."""
    with open(outfile) as f:
        content = f.read()
    # Chercher "S( 0)-> T( 0)" ou "S1 <-> T1"
    patterns = [
        r'S\(\s*0\)\s*->\s*T\(\s*0\).*?([\d.]+)\s*cm',
        r'S1\s*<->\s*T1\s*:\s*([\d.]+)\s*cm',
    ]
    for pat in patterns:
        m = re.search(pat, content, re.IGNORECASE)
        if m:
            return float(m.group(1))
    return None


def extract_homo_lumo(outfile):
    """Extrait le gap HOMO-LUMO en eV depuis un calcul xTB ou DFT."""
    with open(outfile) as f:
        content = f.read()
    # xTB format
    m = re.search(r'HOMO-LUMO GAP\s+([\d.]+)\s+eV', content)
    if m:
        return float(m.group(1))
    # ORCA format : chercher les énergies orbitales
    homo_matches = re.findall(r'(\d+)\s+([\d.]+)\s+[-\d.]+\s+[-\d.]+\s+2\.0000', content)
    lumo_matches = re.findall(r'(\d+)\s+([\d.]+)\s+[-\d.]+\s+[-\d.]+\s+0\.0000', content)
    if homo_matches and lumo_matches:
        homo_ev = float(homo_matches[-1][1]) * 27.2114
        lumo_ev = float(lumo_matches[0][1]) * 27.2114
        return lumo_ev - homo_ev
    return None


def compute_delta_E_ST(e_s0_Eh, e_t1_Eh):
    """Calcule ΔE_ST en eV depuis les énergies en Hartree."""
    if e_s0_Eh is None or e_t1_Eh is None:
        return None
    return (e_t1_Eh - e_s0_Eh) * 27.2114


def scan_results():
    """Parcourt tous les répertoires de calcul et collecte les résultats."""
    results = {}
    base = Path("calculations")

    # TD-DFT
    for func_dir in (base / "tier2_tddft").iterdir():
        if not func_dir.is_dir():
            continue
        func = func_dir.name
        for outfile in func_dir.glob("*.out"):
            mol = outfile.stem.replace(f"_T2_{func}", "")
            lmax, fosc = extract_tddft(outfile)
            key = (mol, func)
            results[key] = {"molecule": mol, "functional": func,
                            "lambda_max_nm": lmax, "f_S1": fosc}

    # Δ-DFT ΔE_ST
    delta_energies = {}
    for outfile in (base / "tier25_deltadft").glob("*.out"):
        name = outfile.stem
        e = extract_final_energy(outfile)
        delta_energies[name] = e

    # SOC
    soc_results = {}
    for outfile in (base / "soc").glob("*.out"):
        mol = outfile.stem.replace("_SOC", "")
        soc_results[mol] = extract_soc(outfile)

    return results, delta_energies, soc_results


def write_tddft_csv(results):
    if not results:
        print("Aucun résultat TD-DFT trouvé.")
        return
    os.makedirs("results", exist_ok=True)
    with open("results/TDDFT_benchmark.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["molecule", "functional",
                                               "lambda_max_nm", "f_S1"])
        writer.writeheader()
        writer.writerows(results.values())
    print(f"Écrit : results/TDDFT_benchmark.csv ({len(results)} entrées)")


def write_soc_csv(soc_results):
    if not soc_results:
        print("Aucun résultat SOC trouvé.")
        return
    with open("results/SOC_results.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["molecule", "SOC_cm"])
        writer.writeheader()
        for mol, soc in soc_results.items():
            writer.writerow({"molecule": mol, "SOC_cm": soc})
    print(f"Écrit : results/SOC_results.csv ({len(soc_results)} entrées)")


if __name__ == "__main__":
    print("Parsing des résultats ORCA...")
    tddft, delta, soc = scan_results()
    write_tddft_csv(tddft)
    write_soc_csv(soc)
    print("Terminé.")
