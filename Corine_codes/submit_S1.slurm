#!/bin/bash
#SBATCH --job-name=orc_S1
#SBATCH --output=orca_S1.%j.out
#SBATCH --error=orca_S1.%j.err
#SBATCH --time=12:00:00  # Extended time to account for multiple attempts (+200-300% buffer)
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12
#SBATCH --mem=32G

module load orca/6.1

# S₁ optimization is critical and may require multiple attempts due to convergence issues
# Expected times per attempt: 120-180 min
# Buffer +200-300% recommended (3-5 tentatives) → Total time: up to 8-10 hours
# Use gen_s1_guesses.sh and run_troubleshoot_S1.sh for automated attempts

# For improved success rate, use automated troubleshooting:
# ./run_troubleshoot_S1.sh -i S1_water_opt.inp -x S0_water_opt.xyz -g S0_water_opt.gbw -n 12

# Or run directly with multiple attempt protocol:
orca S1_water_opt.inp > S1_water_opt.out 2>&1
