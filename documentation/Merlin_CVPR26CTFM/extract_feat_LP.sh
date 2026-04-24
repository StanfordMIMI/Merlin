#!/bin/bash
set -e

INPUT_DIR=${INPUT_DIR:-/workspace/inputs}
OUTPUT_DIR=${OUTPUT_DIR:-/workspace/outputs}
MASKS_DIR=${MASKS_DIR:-""}

CMD="python extract_feat_LP.py -i $INPUT_DIR -o $OUTPUT_DIR --batch_size 1 --num_workers 0"
if [ -n "$MASKS_DIR" ]; then
    CMD="$CMD --masks_path $MASKS_DIR"
fi

echo "Running: $CMD"
eval $CMD
