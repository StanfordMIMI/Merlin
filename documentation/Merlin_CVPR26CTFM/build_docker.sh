#!/bin/bash
set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

IMAGE_NAME=${IMAGE_NAME:-merlin_lp}
docker build -t ${IMAGE_NAME}:latest .
docker save ${IMAGE_NAME}:latest | gzip > ${IMAGE_NAME}.tar.gz
echo "Built and saved: ${SCRIPT_DIR}/${IMAGE_NAME}.tar.gz"
