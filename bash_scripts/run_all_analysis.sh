#!/bin/bash


#!/bin/bash#!/bin/bash

echo "=========================================="
echo " START ANALYSIS PIPELINE (ROOT LEVEL)"
echo "=========================================="
echo ""

# =========================
# PARAMETRES
# =========================

ROOT_DIR=$(pwd)

LI_BASE="Conditions"
LI_DIRS=("Annealing")

ANALYSIS_SCRIPT="$ROOT_DIR/scripts/python_scripts/analysis.py"
AVERAGE_SCRIPT="$ROOT_DIR/scripts/python_scripts/average_analysis.py"

TRAJ_FILE_NAME="cool_dump.lammpstrj"
DESTINATION_DIR="ANALYSIS_COOL"

DATA_TYPES=(
"msd_Li"
"msd_Mn"
"msd_O"
"rdf_evolution"
"coord_Mn"
"distortion"
"volume"
"diffusion"
)


echo "[INFO] Root directory: $ROOT_DIR"
echo ""

# =========================
# LOOP PRINCIPALE
# =========================

for LI in "${LI_DIRS[@]}"; do

    SYSTEM_PATH="$ROOT_DIR/$LI_BASE/$LI"

    echo "------------------------------------------"
    echo "[SYSTEM] $LI"
    echo "[PATH] $SYSTEM_PATH"
    echo "------------------------------------------"

    if [ ! -d "$SYSTEM_PATH/TEMP" ]; then
        echo "[WARNING] TEMP folder not found → skipping"
        continue
    fi

    cd "$SYSTEM_PATH"
    mkdir -p $DESTINATION_DIR
    cd TEMP

    echo "[INFO] Working in $(pwd)"

    # =========================
    # 1. ANALYSES PAR STRUCTURE
    # =========================

    echo ""
    echo "[STEP 1] Per-structure analysis"
    echo ""

    for STRUCT in Structure_*; do
        [ -d "$STRUCT" ] || continue

        echo "  [STRUCTURE] $STRUCT"

        cp "$ANALYSIS_SCRIPT" "$STRUCT/"
        sed -i "s/XX_TRAJECTORY_XX/${TRAJ_FILE_NAME}/g" "${STRUCT}/analysis.py"
	echo "  [SETUP] Traj file has been set to $TRAJ_FILE_NAME"
	cd "$STRUCT"
	
        echo "  [RUN] analysis.py"
        python3 analysis.py > analysis.log 2>&1

        cd ..
    done

    # =========================
    # 2. MOYENNES
    # =========================

    echo ""
    echo "[STEP 2] Averaging"
    echo ""

    cp "$AVERAGE_SCRIPT" .

    for DATA in "${DATA_TYPES[@]}"; do

        echo "  [DATA] $DATA"

        COUNT=$(ls Structure_*/$DATA.dat 2>/dev/null | wc -l)

        if [ "$COUNT" -eq 0 ]; then
            echo "  [SKIP] No files"
            continue
        fi

        # STD logic
        case $DATA in
            msd_*|coord_Mn|disorder|distortion|volume)
                python3 average_analysis.py "$DATA" \
                    --std \
                    -o "avg_$DATA.dat" \
                    > avg_${DATA}.log 2>&1
                ;;
            *)
                python3 average_analysis.py "$DATA" \
                    -o "avg_$DATA.dat" \
                    > avg_${DATA}.log 2>&1
                ;;
        esac

        echo "  [OK]"
    done


    # =========================
    # 2.5 MERGE LARGE Mn DISPLACEMENTS
    # =========================

    echo ""
    echo "[STEP 2.5] Gathering large Mn displacements"
    
    OUTPUT_FILE="all_large_displacements_Mn.dat"
    echo "# Structure Index Type Displacement(Angstrom)" > $OUTPUT_FILE
    
    for STRUCT in Structure_*; do

        FILE="$STRUCT/large_displacements_Mn.dat"
    
        if [ ! -f "$FILE" ]; then
            echo "  [SKIP] $STRUCT (no file)"
            continue
        fi
    
        echo "  [MERGE] $STRUCT"

        # skip header + ajouter nom structure
        tail -n +2 "$FILE" | awk -v struct="$STRUCT" '{print struct, $0}' >> $OUTPUT_FILE

    done

    echo "[OK] All Mn displacements gathered in $OUTPUT_FILE"

    
    # =========================
    # 3. MOVE RESULTS
    # =========================

    echo ""
    echo "[STEP 3] Moving results"

    mv *.dat *.png ../$DESTINATION_DIR/ 2>/dev/null || echo "[INFO] Nothing to move"

    # =========================
    # 4. CLEAN
    # =========================

    echo ""
    echo "[STEP 4] Cleaning"

    for STRUCT in Structure_*; do
        rm -f "$STRUCT/analysis.py"
    done

    rm -f average_analysis.py

    echo "[OK] Clean complete"

    cd "$ROOT_DIR"

done  

echo "=========================================="
echo "  ALL SYSTEMS PROCESSED"
echo "=========================================="


