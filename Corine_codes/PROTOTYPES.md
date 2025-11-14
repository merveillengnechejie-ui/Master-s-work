PROTOTYPES
=========

Ce fichier décrit les prototypes présents dans `Corine_codes` et le comportement
des scripts `copy_and_prepare.sh` et `prepare_and_submit.sh`.

Fichiers prototype
-------------------

- `Bodipy_Opt.xyz` : prototype BODIPY (coordonnées au format .xyz)
- `Iodo_Opt.xyz`  : prototype iodé
- `TPP_Opt.xyz`   : prototype TPP-BODIPY

Comportement de `copy_and_prepare.sh`
-------------------------------------

- Par défaut, le script recherche tous les fichiers `*.xyz` dans `Corine_codes`.
- Pour chaque fichier trouvé (ex. `Bodipy_Opt.xyz`) :
  - crée un répertoire `../Bodipy_Opt` (dans le répertoire projet passé en
    argument — par défaut le répertoire courant)
  - copie les templates `.inp` et `.md` depuis `Corine_codes/` dans ce répertoire
  - installe le fichier `.xyz` dans le répertoire cible sous son nom original
    (ex. `Bodipy_Opt.xyz`) et crée également `S0_gas_opt.xyz` et
    `S0_water_opt.xyz` si ces fichiers n'existent pas encore

- Si aucun `.xyz` n'est trouvé, le script retombe sur le comportement legacy
  (création de `proto-A`, `proto-B`, `proto-C`).

Comportement de `prepare_and_submit.sh`
---------------------------------------

- Appelle d'abord `copy_and_prepare.sh` pour préparer les prototypes.
- Recherche ensuite tous les sous-répertoires du projet (sauf
  `Corine_codes`) contenant au moins un fichier `*.xyz`. Ces répertoires
  sont traités comme des prototypes.
- Pour chaque prototype, le script :
  - met à jour les blocs `%pal` dans tous les fichiers `.inp` pour définir
    `nprocs` (paramètre passé en 2ème argument, défaut 8)
  - soumet une chaîne de jobs SLURM : S0_gas -> S0_water -> ADC2 -> T1 -> S1 -> SOC
    (si les scripts `submit_*.slurm` sont présents, ils sont utilisés, sinon
    on soumet des commandes `sbatch --wrap="orca ..."`)

Utilisation rapide
------------------

Préparer les prototypes dans le répertoire courant :

    ./Corine_codes/copy_and_prepare.sh

Préparer et soumettre avec 12 coeurs par job :

    ./Corine_codes/prepare_and_submit.sh . 12

Remarques
--------

- Vérifiez les entrées `%pal`, `charge`, `multiplicity` et l'espace actif `%casscf`
  dans chaque `.inp` avant de lancer des calculs en production.
- Si vous voulez un mode "dry-run" (prévisualiser sans soumettre), je peux
  ajouter une option `--dry-run` aux scripts.
