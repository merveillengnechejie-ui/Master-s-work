#!/bin/bash
#SBATCH --job-name=orc_S0
#SBATCH --output=orca_S0.%j.out
#SBATCH --error=orca_S0.%j.err
#SBATCH --time=02:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=8G

module load orca/6.1
orca S0_gas_opt.inp > S0_gas_opt.out 2>&1
