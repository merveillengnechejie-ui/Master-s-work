#!/usr/bin/env bash
# copy_and_prepare.sh
# Copies ORCA templates into prototype directories and installs .xyz files
# Usage: ./copy_and_prepare.sh [project_root]

set -euo pipefail
PROJECT_ROOT="${1:-$(pwd)}"
TEMPLATES_DIR="$PROJECT_ROOT/Corine_codes"

echo "Preparing prototypes in $PROJECT_ROOT"

# Prefer .xyz files placed in the Corine_codes directory (prototypes there).
# If none found, fall back to proto-A/proto-B/proto-C behaviour.
XYZ_LIST=("" )
shopt -s nullglob
XYZ_FILES=("$TEMPLATES_DIR"/*.xyz)
shopt -u nullglob

if [ ${#XYZ_FILES[@]} -gt 0 ]; then
  for xyz in "${XYZ_FILES[@]}"; do
    name=$(basename "$xyz" .xyz)
    TARGET="$PROJECT_ROOT/$name"
    mkdir -p "$TARGET"
    echo "- Creating $TARGET for prototype $name"
    # Copy templates
    cp "$TEMPLATES_DIR"/*.inp "$TARGET/" 2>/dev/null || true
    cp "$TEMPLATES_DIR"/*.md "$TARGET/" 2>/dev/null || true

    # Install xyz into target and create standard S0 filenames if missing
    echo "  -> Installing $xyz"
    cp "$xyz" "$TARGET/$name.xyz"
    # create common names used by the templates if they don't already exist
    if [ ! -f "$TARGET/S0_gas_opt.xyz" ]; then
      cp "$xyz" "$TARGET/S0_gas_opt.xyz"
    fi
    if [ ! -f "$TARGET/S0_water_opt.xyz" ]; then
      cp "$xyz" "$TARGET/S0_water_opt.xyz"
    fi

    chmod +x "$TARGET"/*.inp 2>/dev/null || true
  done
else
  # fallback: keep legacy proto names
  PROTOS=("proto-A" "proto-B" "proto-C")
  for p in "${PROTOS[@]}"; do
    TARGET="$PROJECT_ROOT/$p"
    mkdir -p "$TARGET"
    echo "- Creating $TARGET (legacy proto)"
    cp "$TEMPLATES_DIR"/*.inp "$TARGET/" 2>/dev/null || true
    cp "$TEMPLATES_DIR"/*.md "$TARGET/" 2>/dev/null || true

    XYZ_SRC="$PROJECT_ROOT/${p}.xyz"
    if [ -f "$XYZ_SRC" ]; then
      echo "  -> Found $XYZ_SRC, installing as S0_gas_opt.xyz and S0_water_opt.xyz"
      cp "$XYZ_SRC" "$TARGET/S0_gas_opt.xyz"
      cp "$XYZ_SRC" "$TARGET/S0_water_opt.xyz"
    else
      echo "  -> No ${p}.xyz found. Please place coordinates as ${p}.xyz or edit inputs in $TARGET"
    fi

    chmod +x "$TARGET"/*.inp 2>/dev/null || true
  done
fi

echo "Done. Templates copied. Edit XYZ files and adapt %pal nprocs and casscf active space before running." 
