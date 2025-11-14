Corine_codes — Templates ORCA 6.1

But
----

Fournir des templates ORCA 6.1 prêts à l'usage pour le workflow décrit dans
`demarche_methodologique_stage_v2_integree.md`.

Contenu principal
-----------------

- `S0_gas_opt.inp`           : Optimisation S0 en phase gaz (B3LYP-D3BJ/def2-SVP)
- `S0_water_opt.inp`         : Optimisation S0 en solution (CPCM Water)
- `ADC2_vertical.inp`        : RI-ADC(2) calcul des excitations verticales
- `T1_opt_UKS.inp`           : Optimisation triplet T1 (ΔUKS / UKS)
- `S1_opt_DeltaUKS.inp`      : Optimisation S1 par ΔUKS (entry pour ΔSCF)
- `NEVPT2_SOC.inp`           : Calcul SOC via FIC-NEVPT2 (exemple)
- `TDDFT_SOC_quick.inp`      : Calcul SOC rapide via TD-DFT (dosoc)
- `run_examples.README.md`   : Instructions d'utilisation rapide et remarques

Fichiers XYZ prototypes
-----------------------

Le dossier contient désormais trois fichiers de coordonnées au format `.xyz`
utilisés comme prototypes/exemples dans les workflows :

- `Bodipy_Opt.xyz` : coordonnées optimisées du prototype BODIPY.
- `Iodo_Opt.xyz`  : coordonnées optimisées du prototype iodé.
- `TPP_Opt.xyz`   : coordonnées optimisées du prototype TPP-BODIPY.

Ces fichiers peuvent être insérés directement dans un input ORCA ou référencés
via la directive `* xyzfile` :

    * xyzfile 0 1 Bodipy_Opt.xyz

Remarques importantes
---------------------

1) Remplacez les placeholders `[COORDINATES]` ou utilisez la directive ci-dessus
   pour charger un fichier `.xyz`.
2) Ajustez `nprocs` dans les sections `%pal` selon vos ressources HPC.
3) Les champs `%casscf` (nel/norb) doivent être adaptés au système avant NEVPT2.
4) Ces templates sont des points de départ. Vérifiez chaque input avant
   exécution en production.

Utilisation rapide des scripts fournis
------------------------------------

- `copy_and_prepare.sh` : copie un fichier `.xyz` et un template `.inp` dans un
  répertoire de travail prêt à l'exécution. Exemple :

    ./copy_and_prepare.sh Bodipy_Opt.xyz S0_gas_opt.inp

  (le script peut accepter d'autres options — ouvrir le script pour détails)

- `prepare_and_submit.sh` : prépare l'input final et soumet le job via un
  script `submit_*.slurm`. Exemple :

    ./prepare_and_submit.sh Bodipy_Opt.xyz submit_S0.slurm

  Vérifiez la charge (`charge`) et la multiplicité (`multiplicity`) avant
  soumission.

Notes et prochaines étapes
-------------------------

- Si vous voulez que les scripts parcourent automatiquement tous les fichiers
  `.xyz` (exécution par lot), je peux proposer une version modifiée.
- Licence: usage académique
Corine_codes — Templates ORCA 6.1

But: fournir des templates ORCA 6.1 prêts à l'usage pour le workflow décrit dans
`demarche_methodologique_stage_v2_integree.md`.

Contenu
- S0_gas_opt.inp           : Optimisation S0 en phase gaz (B3LYP-D3BJ/def2-SVP)
- S0_water_opt.inp         : Optimisation S0 en solution (CPCM Water)
- ADC2_vertical.inp        : RI-ADC(2) calcul des excitations verticales
- T1_opt_UKS.inp           : Optimisation triplet T1 (ΔUKS / UKS)
- S1_opt_DeltaUKS.inp      : Optimisation S1 par ΔUKS (entry pour ΔSCF)
- NEVPT2_SOC.inp           : Calcul SOC via FIC-NEVPT2 (exemple)
- TDDFT_SOC_quick.inp      : Calcul SOC rapide via TD-DFT (dosoc)
- run_examples.README.md   : Instructions d'utilisation rapide et remarques

REMARQUES IMPORTANTES
1) Remplacez les placeholders [COORDINATES] ou utilisez `* xyzfile 0 1 S0_water_opt.xyz`
   pour charger un fichier .xyz.
2) Ajustez `nprocs` dans les sections %pal selon vos ressources HPC.
3) Les champs %casscf (nel/norb) doivent être adaptés au système avant NEVPT2.
4) Ces templates sont destinés à être des points de départ. Vérifiez chaque input
   avant exécution en production.

Licence: usage académique
