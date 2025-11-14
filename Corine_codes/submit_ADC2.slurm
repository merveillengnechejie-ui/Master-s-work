#!/bin/bash
#SBATCH --job-name=orc_ADC2
#SBATCH --output=orca_ADC2.%j.out
#SBATCH --error=orca_ADC2.%j.err
#SBATCH --time=04:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=24G

module load orca/6.1
orca ADC2_vertical.inp > ADC2_vertical.out 2>&1
