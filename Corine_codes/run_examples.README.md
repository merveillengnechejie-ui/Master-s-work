Run examples and quick notes

Quick use-case:
1) Copy S0_gas_opt.inp into a proto folder (e.g. proto-A/)
2) Replace "[COORDINATES]" or use your .xyz and name it S0_gas_opt.xyz
3) Submit S0_gas_opt.inp to ORCA (or use the submit script in your Guide)
4) After S0 optimization, copy/rename the output geometry to S0_water_opt.xyz if you want
   to run the water-phase optimizations and ADC2.

Recommended parameters to adapt before running:
- %pal nprocs: number of CPU cores to use
- Basis set: def2-SVP is default here; change to def2-TZVP for production
- %casscf nel/norb: must be set appropriate for NEVPT2 runs

Notes on ΔSCF/ΔUKS and S1 optimizations:
- S1 optimizations can fail (collapse to S0). Use the convergence strategies in the
  main Guide (damping, LevelShift, TRAH algorithm, smaller MaxStep).
- Keep gbw files (checkpoint) to restart or generate excited guesses.

Contact & provenance: templates derived from `demarche_methodologique_stage_v2_integree.md`.
