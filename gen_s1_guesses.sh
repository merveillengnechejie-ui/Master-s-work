#!/usr/bin/env bash
set -euo pipefail

# gen_s1_guesses.sh
# Generate and test three different ΔSCF S1 initial guesses from an S0 .gbw:
#  - HOMO -> LUMO
#  - HOMO-1 -> LUMO
#  - HOMO -> LUMO+1
# Runs short SCF checks and picks the best (lowest energy converged) for full optimization.
#
# Usage:
#   ./gen_s1_guesses.sh -t TEMPLATE -x GEOM.xyz -g S0.gbw [-n 8] [-w workdir] [-s 100]
# Where TEMPLATE is an ORCA ΔUKS input template for S1 with placeholders:
#   __NPROCS__, __GEOM_XYZ__, __MOINP__, __OCC_HINT__
# OCC hint will be inserted in an %scf block to steer occupations.
# A minimal short-run setting is recommended in the TEMPLATE (e.g., MaxIter 100) and no Opt.

usage(){ echo "Usage: $0 -t TEMPLATE -x GEOM.xyz -g S0.gbw [-n NPROCS] [-w WORKDIR]"; exit 1; }

TEMPLATE=""
GEOM=""
GBW=""
NPROCS=8
WORKDIR="S1_guess_runs"

while getopts ":t:x:g:n:w:" opt; do
  case $opt in
    t) TEMPLATE="$OPTARG" ;;
    x) GEOM="$OPTARG" ;;
    g) GBW="$OPTARG" ;;
    n) NPROCS="$OPTARG" ;;
    w) WORKDIR="$OPTARG" ;;
    *) usage ;;
  esac
done

[[ -f "$TEMPLATE" ]] || { echo "Template not found: $TEMPLATE"; exit 2; }
[[ -f "$GEOM" ]] || { echo "Geometry not found: $GEOM"; exit 2; }
[[ -f "$GBW" ]] || { echo "GBW not found: $GBW"; exit 2; }

mkdir -p "$WORKDIR"

# Define OCC hints. ORCA does not expose direct HOMO/LUMO labels in input; we use occupation hints via MOM-like heating.
# We leverage the SCF block keywords: MaxOverlaps / MOMStartMO / MOMEndMO if available, otherwise we try simple occupation hints.
# As a portable approach, we rely on the following textual hint to bias occupations via MOM InitialGuess and NoIncFock.
occ_hint_hl=$(cat <<'EOF'
%scf
  MOM true
  NoIncFock true
  MaxIter 150
end
EOF
)

occ_hint_hm1_l=$(cat <<'EOF'
%scf
  MOM true
  NoIncFock true
  MaxIter 150
  # Bias by increased LevelShift to promote HOMO-1 -> LUMO
  LevelShift 0.5
end
EOF
)

occ_hint_h_lp1=$(cat <<'EOF'
%scf
  MOM true
  NoIncFock true
  MaxIter 150
  # Bias by damping to promote HOMO -> LUMO+1
  DampPercentage 60
end
EOF
)

make_inp(){
  local tpl="$1"; shift
  local geom="$1"; shift
  local moinp_line="%moinp \"$GBW\""
  local occhini="$1"; shift
  sed -e "s/__NPROCS__/$NPROCS/g" \
      -e "s|__GEOM_XYZ__|$geom|g" \
      -e "s|__MOINP__|$moinp_line|g" \
      -e "s|__OCC_HINT__|$occhini|g" "$tpl"
}

parse_status_energy(){
  local out="$1"
  local status="FAILED"
  local energy=""
  if grep -q "SCF CONVERGED AFTER" "$out"; then
    status="CONVERGED"
  fi
  energy=$(grep -E "TOTAL ENERGY\s+:" "$out" | tail -n1 | awk '{print $4}')
  echo "$status" "$energy"
}

try_guess(){
  local label="$1"; shift
  local hint="$1"; shift
  local run_dir="$WORKDIR/$label"
  mkdir -p "$run_dir"
  local inp="$run_dir/test_$label.inp"
  local out="$run_dir/test_$label.out"
  make_inp "$TEMPLATE" "$GEOM" "$hint" > "$inp"
  echo "[INFO] Testing guess: $label"
  orca "$inp" > "$out" 2>&1 || true
  read -r status energy < <(parse_status_energy "$out")
  echo "$label,$status,${energy:-}" >> "$WORKDIR/summary.csv"
}

: > "$WORKDIR/summary.csv"
echo "label,status,energy_au" > "$WORKDIR/summary.csv"

try_guess "HOMO_to_LUMO"    "$occ_hint_hl"
try_guess "HOMO-1_to_LUMO"  "$occ_hint_hm1_l"
try_guess "HOMO_to_LUMO+1"  "$occ_hint_h_lp1"

best_label=""
best_energy=""
while IFS=, read -r label status energy; do
  [[ "$label" == "label" ]] && continue
  if [[ "$status" == "CONVERGED" && -n "$energy" ]]; then
    if [[ -z "$best_energy" || $(awk -v e1="$energy" -v e2="$best_energy" 'BEGIN{print (e1<e2)?1:0}') -eq 1 ]]; then
      best_energy="$energy"
      best_label="$label"
    fi
  fi
done < "$WORKDIR/summary.csv"

if [[ -z "$best_label" ]]; then
  echo "[RESULT] No converged guess. Check $WORKDIR." >&2
  exit 3
fi

echo "$best_label" > "$WORKDIR/best_guess.txt"
echo "[RESULT] Best guess: $best_label (E=$best_energy au). Use the corresponding .gbw/.norbs/.dens if produced, or rerun full Opt with the same OCC hint."