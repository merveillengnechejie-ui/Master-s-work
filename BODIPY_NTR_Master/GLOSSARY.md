# Glossary of technical terms

This glossary defines the key methodologies and parameters used in this Master's Thesis.

| Term | Definition |
| :--- | :--- |
| **Δ-DFT (ΔSCF)** | A method to calculate excited states by specifying a non-standard orbital occupancy. More robust than TD-DFT for certain Charge Transfer (CT) states. |
| **MOM (Maximum Overlap Method)** | A stabilization technique for Δ-DFT that prevents the excited-state calculation from collapsing back to the ground state ($S_0$) during optimization. |
| **SOC (Spin-Orbit Coupling)** | The relativistic interaction between an electron's spin and its orbital motion. Crucial for calculating the rate of Intersystem Crossing (ISC) in PDT. |
| **ISC (Intersystem Crossing)** | The non-radiative transition between states of different multiplicity (e.g., $S_1 \rightarrow T_1$). The primary pathway for triplet state generation. |
| **RSDH functional** | Range-Separated Double-Hybrid functional (e.g., $SOS-\omega B2GP-PLYP$). High-accuracy functionals used to benchmark spectral properties. |
| **OPI 2.0** | ORCA Property Interface (v2.0). A modernized extraction protocol using JSON-based data parsing to ensure 100% data integrity in the screening pipeline. |
| **SMD (Solvation Model based on Density)** | An implicit solvation model that accounts for the electronic density of the solute interacting with a continuum solvent (Water). |
| **Hirshfeld charges** | A method of partitioning electron density to determine the effective charge of molecular fragments (used here for TPP targeting validation). |
| **Logic gate** | A molecular system that provides a specific output (Fluorescence/PDT) only when a specific input (NTR enzyme/Hypoxia) is present. |
| **Pareto front** | In multi-objective optimization, the set of candidates where one property cannot be improved without degrading another. Used to find the lead Synergy candidates. |
