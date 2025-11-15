#!/usr/bin/env bash
set -euo pipefail

# run_troubleshoot_S1.sh
# Automated ΔSCF S1 troubleshooting for ORCA: iterates LevelShift/Damp/DIIS_TRAH settings
# Detects oscillatory SCF or non-convergence, escalates settings, and keeps the best result.
#
# Requirements:
# - ORCA available in PATH (orca, orca_jobname conventions)
# - Input template for S1 ΔSCF (UKS) with placeholders for parameters and geometry/gbw
# - Geometry .xyz and (optional) S0 .gbw as initial guess
#
# Usage:
#   ./run_troubleshoot_S1.sh -i S1_template.inp -x S0_water_opt.xyz [-g S0_water_opt.gbw] \
#       [-n 8] [-w workdir]
#
# Placeholders expected in template (exact tokens):
#   __NPROCS__   -> replaced by integer nprocs
#   __LEVELSHIFT__ -> SCF LevelShift value (e.g., 0.0, 0.2, 0.5)
#   __DAMP__     -> DampPercentage (e.g., 0, 40, 60)
#   __ALGO__     -> SCF_ALGORITHM value (e.g., DIIS, DIIS_TRAH)
#   __GEOM_XYZ__ -> xyz file path
#   __MOINP__    -> optional %moinp line or empty
#
# Output:
#  - workdir/ contains run_* subfolders per attempt with .inp/.out
#  - best_attempt.txt with the selected attempt
#  - summary.csv with energies and statuses

usage() {
  echo "Usage: $0 -i TEMPLATE -x GEOM.xyz [-g S0.gbw] [-n NPROCS] [-w WORKDIR]" >&2
  exit 1
}

TEMPLATE=""
GEOM=""
GBW=""
NPROCS=8
WORKDIR="S1_troubleshoot_runs"

while getopts ":i:x:g:n:w:" opt; do
  case $opt in
    i) TEMPLATE="$OPTARG" ;;
    x) GEOM="$OPTARG" ;;
    g) GBW="$OPTARG" ;;
    n) NPROCS="$OPTARG" ;;
    w) WORKDIR="$OPTARG" ;;
    *) usage ;;
  esac
done

[[ -f "$TEMPLATE" ]] || { echo "Template not found: $TEMPLATE"; exit 2; }
[[ -f "$GEOM" ]] || { echo "Geometry not found: $GEOM"; exit 2; }

mkdir -p "$WORKDIR"
SUMMARY="$WORKDIR/summary.csv"
echo "attempt,levelshift,damp,algo,status,energy_au,cycles" > "$SUMMARY"

# Escalation matrix of settings
LEVELSHIFTS=(0.0 0.2 0.5)
DAMPS=(0 40 60)
ALGOS=(DIIS DIIS_TRAH)

attempt=0

make_inp() {
  local tpl="$1"; shift
  local levelshift="$1"; shift
  local damp="$1"; shift
  local algo="$1"; shift
  local geom="$1"; shift
  local moinp_line=""
  if [[ -n "$GBW" ]]; then
    moinp_line="%moinp \"$GBW\""
  fi
  sed -e "s/__NPROCS__/$NPROCS/g" \
      -e "s/__LEVELSHIFT__/$levelshift/g" \
      -e "s/__DAMP__/$damp/g" \
      -e "s/__ALGO__/$algo/g" \
      -e "s|__GEOM_XYZ__|$geom|g" \
      -e "s|__MOINP__|$moinp_line|g" "$tpl"
}

parse_status_energy() {
  local out="$1"
  local status="UNKNOWN"
  local energy=""
  local cycles=""
  # Detect SCF convergence and oscillations
  if grep -q "SCF CONVERGED AFTER" "$out"; then
    status="CONVERGED"
    cycles=$(grep -m1 "SCF CONVERGED AFTER" "$out" | awk '{print $(NF-1)}')
  else
    status="FAILED"
  fi
  # Detect typical oscillation messages
  if grep -Eqi "oscillat|trah|not converged|max\.? number of iterations" "$out"; then
    if [[ "$status" != "CONVERGED" ]]; then
      status="OSCILLATION"
    fi
  fi
  # Final single point energy (Total Energy) for UKS
  energy=$(grep -E "TOTAL ENERGY\s+:" "$out" | tail -n1 | awk '{print $4}')
  echo "$status" "$energy" "$cycles"
}

best_energy=""
best_attempt=""

for ls in "${LEVELSHIFTS[@]}"; do
  for dp in "${DAMPS[@]}"; do
    for algo in "${ALGOS[@]}"; do
      attempt=$((attempt+1))
      run_dir="$WORKDIR/run_${attempt}_LS${ls}_D${dp}_${algo}"
      mkdir -p "$run_dir"
      inp="$run_dir/S1_opt.inp"
      out="$run_dir/S1_opt.out"
      make_inp "$TEMPLATE" "$ls" "$dp" "$algo" "$GEOM" > "$inp"
      echo "[INFO] Attempt #$attempt -> LevelShift=$ls Damp=$dp Algo=$algo"
      orca "$inp" > "$out" 2>&1 || true
      read -r status energy cycles < <(parse_status_energy "$out")
      echo "$attempt,$ls,$dp,$algo,$status,${energy:-},${cycles:-}" >> "$SUMMARY"
      if [[ "$status" == "CONVERGED" && -n "$energy" ]]; then
        if [[ -z "$best_energy" || $(awk -v e1="$energy" -v e2="$best_energy" 'BEGIN{print (e1<e2)?1:0}') -eq 1 ]]; then
          best_energy="$energy"
          best_attempt="$run_dir"
        fi
      fi
    done
  done
done

if [[ -n "$best_attempt" ]]; then
  echo "$best_attempt" > "$WORKDIR/best_attempt.txt"
  echo "[RESULT] Best converged attempt: $best_attempt (E = $best_energy au)"
else
  echo "[RESULT] No converged attempt found. Check $SUMMARY and outputs in $WORKDIR." >&2
  exit 3
fi
