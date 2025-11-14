#!/bin/bash
#SBATCH --job-name=orc_S1
#SBATCH --output=orca_S1.%j.out
#SBATCH --error=orca_S1.%j.err
#SBATCH --time=06:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=32G

module load orca/6.1
orca S1_water_opt.inp > S1_water_opt.out 2>&1
