#!/bin/bash
#SBATCH --job-name=orc_SOC
#SBATCH --output=orca_SOC.%j.out
#SBATCH --error=orca_SOC.%j.err
#SBATCH --time=02:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G

module load orca/6.1
# Recommended: use the fast TD-DFT SOC for screening
orca TDDFT_SOC_quick.inp > TDDFT_SOC_quick.out 2>&1
