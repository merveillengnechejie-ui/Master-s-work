# Synthèse : Intégration des recommandations méthodologiques

Cette synthèse (1 page) rassemble les recommandations pratiques issues de l'audit et
intègre les choix méthodologiques à appliquer systématiquement pour les calculs
BODIPY décrits dans `demarche_methodologique_stage_v2_integree.md`.

Thématique du stage : Optimisation de nanoparticules de BODIPY pour une thérapie combinée photodynamique et photothermique ciblée sur les cellules de cancer du sein triple négatif.

Points-clés

- Méthodes recommandées :
  - ΔUKS / ΔROKS pour ΔE_ST et E_em (privilégier ΔROKS pour émissions CT en solution).
  - ADC(2) pour les excitations verticales (λ_max) sur géométrie S0.
  - FIC-NEVPT2 / CASSCF (ZORA) pour SOC (gold standard) ; TD-DFT/dosoc comme alternative de screening.

- Solvatation : utiliser ptSS-PCM (état-spécifique non-équilibre) pour les énergies d'émission des états CT lorsque c'est possible.

- Fonctionnelles conseillées : OT-ωB97M-V (pour ΔUKS/ΔROKS en émission), PBE0 (ΔUKS rapide/robuste), PBE38-D4 (robuste pour E_em).

- ICT / dimères : utiliser la stratégie IMOM (Initial Maximum Overlap Method) pour la stabilité de convergence et de bonnes prédictions d'états ICT.

- Benchmarks & cibles :
  - ΔE_ST : viser MAE < 0,05 eV (précision chimique)
  - λ_max / E_em : viser MAE ≤ 0,1 eV (≈10 nm autour de 700 nm)

- Coûts & stratégie pragmatic :
  - Réserver NEVPT2/CASSCF aux candidats retenus (goulet d'étranglement CPU).
  - Utiliser TD-DFT/dosoc pour screening SOC rapide.
  - Conserver les fichiers `.gbw` et utiliser des scripts de reprise (damping, LevelShift, TRAH).

Utilisation

- Lire en priorité `demarche_methodologique_stage_v2_integree.md` puis utiliser les templates dans
  `/home/taamangtchu/Documents/UY1Master_2025/Corine/Corine_codes/`.

Cette fiche peut être jointe au rapport comme annexe méthodologique.
