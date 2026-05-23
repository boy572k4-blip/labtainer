#!/bin/bash
# ============================================================
# T-STEG01: Build Docker images and push to DockerHub
# Run this on a machine WITH Docker and internet access.
# ============================================================
set -e

DOCKERHUB_USERNAME="r3xonx"
DOCKERHUB_TOKEN="dckr_pat_0GZ-Z_l_0BPiLTozPoSXlWHSRs8"
LAB_NAME="steg_lsb-png"
SENDER_IMAGE="${DOCKERHUB_USERNAME}/${LAB_NAME}.sender:latest"
RECEIVER_IMAGE="${DOCKERHUB_USERNAME}/${LAB_NAME}.receiver:latest"

# Resolve script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "============================================"
echo "  T-STEG01 Build & Push to DockerHub"
echo "============================================"
echo "  Working dir: ${SCRIPT_DIR}"
echo ""

# ── 1. Login ─────────────────────────────────────────────
echo "[1/4] Logging in to DockerHub..."
echo "${DOCKERHUB_TOKEN}" | docker login \
    --username "${DOCKERHUB_USERNAME}" \
    --password-stdin
echo "      Login OK"

# ── 2. Build sender ───────────────────────────────────────
echo ""
echo "[2/4] Building SENDER image..."
docker build \
    --no-cache \
    -t "${SENDER_IMAGE}" \
    -f "${SCRIPT_DIR}/sender/Dockerfile" \
    "${SCRIPT_DIR}"          # <-- build context = project root (has scripts/)
echo "      OK: ${SENDER_IMAGE}"

# ── 3. Build receiver ─────────────────────────────────────
echo ""
echo "[3/4] Building RECEIVER image..."
docker build \
    --no-cache \
    -t "${RECEIVER_IMAGE}" \
    -f "${SCRIPT_DIR}/receiver/Dockerfile" \
    "${SCRIPT_DIR}"          # <-- build context = project root (has scripts/)
echo "      OK: ${RECEIVER_IMAGE}"

# ── 4. Push both images ───────────────────────────────────
echo ""
echo "[4/4] Pushing to DockerHub..."
docker push "${SENDER_IMAGE}"
echo "      Pushed: ${SENDER_IMAGE}"
docker push "${RECEIVER_IMAGE}"
echo "      Pushed: ${RECEIVER_IMAGE}"

echo ""
echo "============================================"
echo "  DONE! Images available:"
echo "    ${SENDER_IMAGE}"
echo "    ${RECEIVER_IMAGE}"
echo ""
echo "  On Labtainer VM, run:"
echo "    imodule https://github.com/boy572k4-blip/labtainer/raw/main/imodule_steg_lsb-png.tar"
echo "    labtainer steg_lsb-png"
echo ""
echo "  OR use standalone runner:"
echo "    chmod +x run_lab.sh && ./run_lab.sh start"
echo "============================================"
