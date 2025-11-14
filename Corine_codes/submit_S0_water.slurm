#!/bin/bash
#SBATCH --job-name=orc_S0_water
#SBATCH --output=orca_S0_water.%j.out
#SBATCH --error=orca_S0_water.%j.err
#SBATCH --time=03:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=12G

module load orca/6.1
orca S0_water_opt.inp > S0_water_opt.out 2>&1
