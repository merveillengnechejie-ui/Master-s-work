# Master's Project - In Silico Design of Photodynamic Theranostic Agents for TNBC

**Optimization of BODIPY Nanoparticles for Combined PDT and PTT Therapy Targeting Breast Cancer Cells**

This project focuses on the *in silico* design, geometric optimization, and photophysical characterization of BODIPY-based molecules. These molecules act as key photosensitizers, aiming to improve their efficiency in photodynamic (PDT) and photothermal (PTT) therapies applied to targeted triple-negative breast cancer (TNBC) treatment.

> **Latest Update (March 2026):** Transitioned to ΔDFT+SOC methodology and local execution (16 GB RAM).

## 🎯 Goals

- **Structural Understanding:** Understand the importance of molecular geometry on the photophysical properties of BODIPY nanoparticles.
- **Computational Modeling:** Perform precise geometric optimization of BODIPY molecular prototypes (Base BODIPY, Iodo-BODIPY, and TPP-Iodo-BODIPY).
- **Excited-State Calculations:** Extend geometric optimizations to excited states (S1, T1) to better model photophysical transitions using advanced DFT, TD-DFT (ωB97X-D3), and ΔDFT+SOC methods.
- **Therapeutic Application:** Investigate their properties and function in phototherapies for the treatment of triple-negative breast cancer (TNBC).

## 📂 Repository Content

- **`Geometry_Optimization/`**: Results from initial semi-empirical (xTB, xTB-GFN2) methods, leading up to fine DFT optimizations and advanced OO-DFT/SOC (Spin-Orbit Coupling) calculations.
- **`Corine_codes/`**: Automated bash scripts and ORCA 6.1 input templates for local calculation execution.
- **`md files/`**: Comprehensive project documentation, methodology guidelines (`demarche_methodologique_stage_v3_260302.md`), troubleshooting guides, and execution plans.
- **`Revue_Bibliographique/`**: LaTeX sources for the literature review on TNBC, computational methods, and phototherapies.
- **`Planning_travail/`**: Interactive Gantt charts and operational work plans.

*For detailed navigation, please consult: [`md files/README_GUIDE_NAVIGATION_260304.md`](md%20files/README_GUIDE_NAVIGATION_260304.md).*

## 🚀 Methodology and Workflow

1. **Initial Modeling:** Fast geometry optimization (ground state) via semi-empirical methods (xTB, GFN2-xTB).
2. **DFT Optimization:** Ground state (S0) and implicit solvation (SMD mixed) modeling using robust Density Functional Theory methodologies.
3. **Excited-State Characterization:** Calculation of singlet (S1) and triplet (T1) excited states using ΔSCF and TD-DFT.
4. **Photophysical Properties:** Evaluation of Spin-Orbit Coupling (SOC) and singlet-triplet energy gaps (ΔE_ST) to determine intersystem crossing efficiency for optimal PDT/PTT performance.

## 🚀 Future Perspectives

- Enhanced solvation models (e.g., explicit water molecules, QM/MM).
- Advanced excited-state methods like ADC(3) for validation of key candidates.
- Explicit calculation of non-radiative decay rates (k_IC, k_ISC, k_r).
- Conical intersection search for photostability pathways.

---

## ✍️ Author
**Corine Merveille KENGNE NGNECHEJIE**

## 🎓 Master 2 Student in Atomic, Molecular Physics and Biophysics
## 📍 University of Yaoundé I, Cameroon

> *This repository represents the intersection of computational chemistry, quantum computing, and biomedical innovation, with a commitment to advancing healthcare solutions accessible to all.*
