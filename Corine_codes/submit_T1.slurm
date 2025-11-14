#!/bin/bash
#SBATCH --job-name=orc_T1
#SBATCH --output=orca_T1.%j.out
#SBATCH --error=orca_T1.%j.err
#SBATCH --time=04:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G

module load orca/6.1
orca T1_water_opt.inp > T1_water_opt.out 2>&1
