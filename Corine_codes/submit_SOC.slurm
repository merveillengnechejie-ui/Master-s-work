#!/bin/bash
#SBATCH --job-name=orc_SOC
#SBATCH --output=orca_SOC.%j.out
#SBATCH --error=orca_SOC.%j.err
#SBATCH --time=01:00:00  # Reduced time (30-60 min vs 2+ hours for NEVPT2)
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G

module load orca/6.1
# Recommended: use ΔDFT+SOC for screening (10× faster than NEVPT2)
# This method is consistent with ΔDFT workflow (S1/T1) and provides reliable SOC values
orca DeltaSCF_SOC.inp > DeltaSCF_SOC.out 2>&1

# For comparison: TD-DFT SOC (TDDFT_SOC_quick.inp) can be used as alternative
# For validation: FIC-NEVPT2 can be used for final candidates if resources available
