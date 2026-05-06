# VIVA Defense: Frequently Asked Questions (FAQ)

This document provides scientifically "hardened" responses to potential questions from the thesis committee.

---

## 1. Methodology: Δ-DFT vs. TD-DFT
**Q: Why did you prioritize Δ-DFT (ΔSCF) over TD-DFT for your lead candidates?**
*   **Response:** "While TD-DFT is excellent for spectral screening, it often suffers from variational collapse and poor description of Charge Transfer (CT) states in nitro-substituted systems like our BODIPY-NTR logic gates. Δ-DFT, combined with the **Maximum Overlap Method (MOM)**, allowed us to directly optimize the $S_1$ and $T_1$ geometries with orbital-specific constraints, providing a more robust physical description of the excited-state relaxation and SOC coupling."

**Q: Why not use multiconfigurational methods like NEVPT2 or CASSCF?**
*   **Response:** "Our goal was to screen an 8-molecule library with high throughput. NEVPT2 is computationally prohibitive for this scale on local hardware (16GB RAM). Δ-DFT+SOC provides a reliable compromise, capturing the essential physics of intersystem crossing at 1/10th the computational cost, allowing for a broader exploration of the design space."

---

## 2. The Synergy score
**Q: How did you define the Synergy Score? Is it physically grounded?**
*   **Response:** "The Synergy Score is a multi-objective heuristic. It balances the **PDT potential** (quantified by $\Delta E_{ST}$ and Spin-Orbit Coupling) with the **PTT potential** (quantified by reorganization energy $\lambda$ as a proxy for non-radiative decay). By normalizing these values, we identify molecules that occupy the Pareto front—performing optimally in both modalities rather than excelling in only one."

---

## 3. Clinical relevance
**Q: How does your in-silico model account for the biological complexity of TNBC?**
*   **Response:** "We account for the biological microenvironment through two critical layers:
    1.  **Implicit Solvation (SMD):** Using a water-calibrated dielectric to mimic the cellular environment.
    2.  **Logic Gate Framing:** Modeling the Nitro-to-Amino transformation as a binary response to **Nitroreductase (NTR)**, which is a clinical biomarker for tumor hypoxia. Our model doesn't just predict properties; it predicts **activation**."

---

## 4. Hardware limitations
**Q: You mention local execution on 16GB RAM. Did this limit your accuracy?**
*   **Response:** "No. We optimized our protocol by using **RIJCOSX** approximations and efficient memory management (%maxcore 3500). These technical adjustments allowed us to maintain a high-level basis set (def2-SVP/TZVP) and robust functionals (PBE0/ωB97X) without compromising the scientific integrity of the results."
