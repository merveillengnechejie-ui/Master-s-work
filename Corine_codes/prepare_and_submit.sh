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

  # Execute workflow sequentially on the local machine
  echo "  -> Running S0_gas_opt.inp..."
  nohup orca S0_gas_opt.inp > S0_gas_opt.out 2>&1
  
  if grep -q "TERMINATED NORMALLY" S0_gas_opt.out; then
    echo "  -> S0_gas converged. Running S0_water_opt.inp..."
    nohup orca S0_water_opt.inp > S0_water_opt.out 2>&1
  else
    echo "  -> Error in S0_gas. Stopping sequence for $p."
    continue
  fi

  if grep -q "TERMINATED NORMALLY" S0_water_opt.out; then
    echo "  -> S0_water converged. Running TDDFT_vertical.inp..."
    nohup orca TDDFT_vertical.inp > TDDFT_vertical.out 2>&1
    
    echo "  -> S0_water converged. Running T1_opt_UKS.inp..."
    nohup orca T1_opt_UKS.inp > T1_opt_UKS.out 2>&1
    
    echo "  -> S0_water converged. Note: S1_opt requires manual inspection and optional gen_s1_guesses.sh."
    echo "  -> Attempting default S1_opt_DeltaUKS.inp run..."
    nohup orca S1_opt_DeltaUKS.inp > S1_opt_DeltaUKS.out 2>&1 || true
    
    if grep -q "TERMINATED NORMALLY" S1_opt_DeltaUKS.out; then
      echo "  -> S1_opt converged. Running DeltaSCF_SOC.inp..."
      nohup orca DeltaSCF_SOC.inp > DeltaSCF_SOC.out 2>&1
    else
      echo "  -> Error in S1_opt. Please use run_troubleshoot_S1.sh."
      echo "  -> Running fallback TDDFT_SOC_quick.inp instead."
      nohup orca TDDFT_SOC_quick.inp > TDDFT_SOC_quick.out 2>&1
    fi
  else
    echo "  -> Error in S0_water. Stopping sequence for $p."
    continue
  fi

  echo "All sequential local jobs completed for $p."

done

echo "Sequential execution complete for all prototypes." 
