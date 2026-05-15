#!/usr/bin/env python3
"""
opi_master_workflow.py
Workflow OPI pour l'automatisation des calculs BODIPY (S0, S1, T1, SOC).
Remplace et améliore prepare_and_submit.sh.
"""

import os
import shutil
from pathlib import Path
from opi.core import Calculator
from opi.input.blocks import BlockScf, BlockCpcm, BlockGeom, BlockTddft, Shift, Damp
from opi.input.simple_keywords import BasisSet, Method, Functional, Scf, Opt, Wft
from opi.input.structures import Structure

# Configuration globale
NPROCS = 8
MAXCORE = 3500
PROJECT_ROOT = Path("/home/taamangtchu/Documents/Github/Master-s-work/BODIPY_NTR_Master")
TEMPLATES_DIR = PROJECT_ROOT / "Corine_codes"

def setup_calculator(name, structure, working_dir):
    calc = Calculator(basename=name, working_dir=working_dir)
    calc.structure = structure
    calc.input.ncores = NPROCS
    calc.input.set_maxcore(MAXCORE)
    return calc

def run_workflow(proto_name, xyz_file):
    print(f"\n=== Démarrage du workflow pour {proto_name} ===")
    working_dir = PROJECT_ROOT / "calculations" / proto_name
    working_dir.mkdir(parents=True, exist_ok=True)
    
    structure = Structure.from_xyz(xyz_file)
    
    # ---------------------------------------------------------
    # Étape 1 : Optimisation S0 (Gaz)
    # ---------------------------------------------------------
    print(f"  -> Étape 1 : Optimisation S0 (Gaz)")
    calc_s0_gas = setup_calculator("S0_gas_opt", structure, working_dir)
    calc_s0_gas.input.add_simple_keywords(Opt.OPT, Functional.B3LYP, BasisSet.DEF2_SVP, "D3BJ", Scf.TIGHTSCF, "TIGHTOPT")
    calc_s0_gas.input.add_blocks(BlockScf(maxiter=500))
    calc_s0_gas.write_input()
    calc_s0_gas.run()
    
    out_s0_gas = calc_s0_gas.get_output()
    if not out_s0_gas.terminated_normally():
        print(f"  [!] Erreur S0 Gaz pour {proto_name}. Arrêt.")
        return

    # ---------------------------------------------------------
    # Étape 2 : Optimisation S0 (Eau / CPCM)
    # ---------------------------------------------------------
    print(f"  -> Étape 2 : Optimisation S0 (Eau / CPCM)")
    # On repart de la géométrie optimisée en phase gazeuse
    struct_s0_gas = out_s0_gas.get_structure() 
    calc_s0_water = setup_calculator("S0_water_opt", struct_s0_gas, working_dir)
    calc_s0_water.input.add_simple_keywords(Opt.OPT, Functional.B3LYP, BasisSet.DEF2_SVP, "D3BJ", Scf.TIGHTSCF)
    calc_s0_water.input.add_blocks(BlockCpcm(smdsolvent="water"))
    calc_s0_water.write_input()
    calc_s0_water.run()
    
    out_s0_water = calc_s0_water.get_output()
    if not out_s0_water.terminated_normally():
        print(f"  [!] Erreur S0 Eau pour {proto_name}. Arrêt.")
        return

    # ---------------------------------------------------------
    # Étape 3 : TD-DFT Vertical & T1 Opt
    # ---------------------------------------------------------
    struct_s0_water = out_s0_water.get_structure()
    
    # TD-DFT
    print(f"  -> Étape 3a : TD-DFT Vertical")
    calc_tddft = setup_calculator("TDDFT_vertical", struct_s0_water, working_dir)
    calc_tddft.input.add_simple_keywords(Functional.PBE0, BasisSet.DEF2_SVP, "TD-DFT")
    calc_tddft.input.add_blocks(BlockTddft(nroots=10))
    calc_tddft.write_input()
    calc_tddft.run()
    
    # T1 Opt
    print(f"  -> Étape 3b : Optimisation T1 (UKS)")
    calc_t1 = setup_calculator("T1_opt_UKS", struct_s0_water, working_dir)
    calc_t1.input.add_simple_keywords(Opt.OPT, "UKS", Functional.PBE0, BasisSet.DEF2_SVP, "D3BJ")
    calc_t1.structure.multiplicity = 3 # Triplet
    calc_t1.write_input()
    calc_t1.run()

    # ---------------------------------------------------------
    # Étape 4 : Optimisation S1 (Delta-UKS) avec Escalade
    # ---------------------------------------------------------
    print(f"  -> Étape 4 : Optimisation S1 (Delta-UKS)")
    calc_s1 = setup_calculator("S1_opt_DeltaUKS", struct_s0_water, working_dir)
    calc_s1.input.add_simple_keywords(Opt.OPT, "UKS", Functional.PBE0, BasisSet.DEF2_SVP, "D3BJ", "SlowConv")
    
    # Bloc SCF avec MOM pour la stabilité de l'état excité
    scf_block = BlockScf(maxiter=500, mom=True)
    scf_block.shift = Shift(0.2)
    scf_block.damp = Damp(40)
    calc_s1.input.add_blocks(scf_block, BlockCpcm(smdsolvent="water"))
    
    # Utiliser le guess de S0
    calc_s1.input.add_keyword("MORead")
    # Note: OPI handles file paths. Here we manually ensure the GBW is reachable if needed.
    
    calc_s1.write_input()
    calc_s1.run()
    
    out_s1 = calc_s1.get_output()
    if not out_s1.terminated_normally():
        print(f"  [!] Échec S1 standard. Tentative d'ESCALADE (LevelShift 0.5)...")
        calc_s1_esc = setup_calculator("S1_opt_Escalate", struct_s0_water, working_dir)
        calc_s1_esc.input.add_simple_keywords(Opt.OPT, "UKS", Functional.PBE0, BasisSet.DEF2_SVP, "D3BJ")
        scf_esc = BlockScf(maxiter=500, mom=True)
        scf_esc.shift = Shift(0.5)
        scf_esc.damp = Damp(70)
        calc_s1_esc.input.add_blocks(scf_esc, BlockCpcm(smdsolvent="water"))
        calc_s1_esc.write_input()
        calc_s1_esc.run()
        out_s1 = calc_s1_esc.get_output()

    # ---------------------------------------------------------
    # Étape 5 : Propriétés Finales (SOC)
    # ---------------------------------------------------------
    if out_s1.terminated_normally():
        print(f"  -> Étape 5 : Calcul SOC (DeltaSCF_SOC)")
        struct_s1 = out_s1.get_structure()
        calc_soc = setup_calculator("DeltaSCF_SOC", struct_s1, working_dir)
        # Keywords pour SOC (à adapter selon vos besoins exacts)
        calc_soc.input.add_simple_keywords(Functional.PBE0, BasisSet.DEF2_SVP, "EPRNMR")
        calc_soc.input.add_keyword("SOC") 
        calc_soc.write_input()
        calc_soc.run()
    else:
        print(f"  [!] S1 n'a pas pu converger même avec escalade. Passage au Plan B (TD-DFT SOC).")
        # Pattern pour calcul SOC rapide en TD-DFT
        calc_soc_q = setup_calculator("TDDFT_SOC_quick", struct_s0_water, working_dir)
        calc_soc_q.input.add_simple_keywords(Functional.PBE0, BasisSet.DEF2_SVP, "TD-DFT")
        calc_soc_q.input.add_blocks(BlockTddft(nroots=5, soc=True))
        calc_soc_q.write_input()
        calc_soc_q.run()

if __name__ == "__main__":
    # Découverte automatique des molécules (.xyz) dans le répertoire racine du projet
    # ou spécification manuelle
    molecules = [
        ("BODIPY-Ph", PROJECT_ROOT / "BODIPY_Ph.xyz"), # Exemple
        # Ajoutez vos molécules ici ou automatisez la boucle
    ]
    
    # Pour le test, on cherche les fichiers .xyz dans Corine_codes
    for f in TEMPLATES_DIR.glob("*.xyz"):
        run_workflow(f.stem, f)

    print("\nWorkflow OPI Master terminé.")
