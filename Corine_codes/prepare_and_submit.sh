#!/usr/bin/env bash
# prepare_and_submit.sh
# Prepare inputs (via copy_and_prepare.sh) and submit SLURM jobs for each prototype

set -euo pipefail
PROJECT_ROOT="${1:-$(pwd)}"
NPROCS="${2:-8}"
VERBOSE=${3:-1}
TEMPLATES_DIR="$PROJECT_ROOT/Corine_codes"

if [ ! -d "$TEMPLATES_DIR" ]; then
  echo "Templates dir not found: $TEMPLATES_DIR"
  exit 1
fi

# Ensure templates and prototype directories are prepared
bash "$TEMPLATES_DIR/copy_and_prepare.sh" "$PROJECT_ROOT"

# Discover prototype directories: any subdirectory of PROJECT_ROOT (not Corine_codes)
# that contains at least one .xyz file will be considered a prototype.
PROTOS=()
for d in "$PROJECT_ROOT"/*/; do
  [ -d "$d" ] || continue
  base=$(basename "$d")
  # skip templates dir and hidden dirs
  if [ "$base" = "Corine_codes" ] || [[ "$base" == .* ]]; then
    continue
  fi
  if compgen -G "$d"*.xyz >/dev/null; then
    PROTOS+=("$base")
  fi
done

if [ ${#PROTOS[@]} -eq 0 ]; then
  # fallback to legacy names if nothing detected
  PROTOS=("proto-A" "proto-B" "proto-C")
fi

for p in "${PROTOS[@]}"; do
  echo -e "\n=== Preparing and submitting for $p ==="
  TARGET="$PROJECT_ROOT/$p"
  if [ ! -d "$TARGET" ]; then
    echo "Target dir $TARGET not found; creating"
    mkdir -p "$TARGET"
  fi

  cd "$TARGET"

  # Optional: set %pal nprocs in all .inp files
  if [ "$NPROCS" != "" ]; then
    for f in *.inp; do
      if [ -f "$f" ]; then
        if grep -q "%pal" "$f"; then
          if grep -q "nprocs" "$f"; then
            sed -i "s/nprocs [0-9]\+/nprocs $NPROCS/" "$f" || true
          else
            sed -i "/%pal/ a\  nprocs $NPROCS" "$f" || true
          fi
        else
          printf "\n%%pal\n  nprocs %s\nend\n" "$NPROCS" >> "$f"
        fi
      fi
    done
  fi

  # Submit workflow with dependencies; similar logic as before but robust to missing templates
  # Helper to submit either via provided slurm script or a simple sbatch --wrap
  submit_or_wrap() {
    local script="$1"; shift
    local cmd="$1"; shift
    if [ -f "$script" ]; then
      echo "  -> Submitting $script"
      sbatch "$script" | awk '{print $4}'
    else
      echo "  -> Submitting wrapped command: $cmd"
      sbatch --wrap="$cmd" | awk '{print $4}'
    fi
  }

  jid_s0=$(submit_or_wrap submit_S0.slurm "orca S0_gas_opt.inp > S0_gas_opt.out 2>&1")
  echo "Submitted S0_gas job id: $jid_s0"

  jid_s0w=$(sbatch --dependency=afterok:$jid_s0 ${PWD}/submit_S0_water.slurm 2>/dev/null | awk '{print $4}' || true)
  if [ -z "$jid_s0w" ]; then
    jid_s0w=$(sbatch --dependency=afterok:$jid_s0 --wrap="orca S0_water_opt.inp > S0_water_opt.out 2>&1" | awk '{print $4}')
  fi
  echo "Submitted S0_water job id: $jid_s0w"

  jid_adc=$(sbatch --dependency=afterok:$jid_s0w ${PWD}/submit_ADC2.slurm 2>/dev/null | awk '{print $4}' || true)
  if [ -z "$jid_adc" ]; then
    jid_adc=$(sbatch --dependency=afterok:$jid_s0w --wrap="orca ADC2_vertical.inp > ADC2_vertical.out 2>&1" | awk '{print $4}')
  fi
  echo "Submitted ADC2 job id: $jid_adc"

  jid_t1=$(sbatch --dependency=afterok:$jid_s0w ${PWD}/submit_T1.slurm 2>/dev/null | awk '{print $4}' || true)
  if [ -z "$jid_t1" ]; then
    jid_t1=$(sbatch --dependency=afterok:$jid_s0w --wrap="orca T1_water_opt.inp > T1_water_opt.out 2>&1" | awk '{print $4}')
  fi
  echo "Submitted T1 job id: $jid_t1"

  jid_s1=$(sbatch --dependency=afterok:$jid_adc ${PWD}/submit_S1.slurm 2>/dev/null | awk '{print $4}' || true)
  if [ -z "$jid_s1" ]; then
    jid_s1=$(sbatch --dependency=afterok:$jid_adc --wrap="orca S1_water_opt.inp > S1_water_opt.out 2>&1" | awk '{print $4}')
  fi
  echo "Submitted S1 job id: $jid_s1"

  jid_soc=$(sbatch --dependency=afterok:$jid_s1 ${PWD}/submit_SOC.slurm 2>/dev/null | awk '{print $4}' || true)
  if [ -z "$jid_soc" ]; then
    jid_soc=$(sbatch --dependency=afterok:$jid_s1 --wrap="orca TDDFT_SOC_quick.inp > TDDFT_SOC_quick.out 2>&1" | awk '{print $4}')
  fi
  echo "Submitted SOC job id: $jid_soc"

  echo "All jobs submitted for $p (S0:$jid_s0 S0w:$jid_s0w ADC:$jid_adc T1:$jid_t1 S1:$jid_s1 SOC:$jid_soc)"

done

echo "Submission complete for all prototypes. Monitor with squeue -u $USER" 
