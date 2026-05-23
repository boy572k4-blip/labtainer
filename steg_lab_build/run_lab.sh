#!/bin/bash
# ============================================================
# T-STEG01: Standalone Lab Runner (without Labtainer)
# Use this if Labtainer cannot reach DockerHub
# Requirements: Docker + docker-compose installed
# ============================================================

DOCKERHUB_USERNAME="r3xonx"
LAB_NAME="steg_lsb-png"
SENDER_IMAGE="${DOCKERHUB_USERNAME}/${LAB_NAME}.sender:latest"
RECEIVER_IMAGE="${DOCKERHUB_USERNAME}/${LAB_NAME}.receiver:latest"

ACTION="${1:-start}"

case "$ACTION" in
    start)
        echo "============================================"
        echo "  T-STEG01 LSB Steganography Lab - START"
        echo "============================================"

        # Pull latest images
        echo "[*] Pulling Docker images..."
        docker pull "${SENDER_IMAGE}"
        docker pull "${RECEIVER_IMAGE}"

        # Create network if not exists
        docker network inspect steg_network >/dev/null 2>&1 || \
            docker network create \
                --driver bridge \
                --subnet 172.21.0.0/24 \
                steg_network

        # Remove old containers if exist
        docker rm -f steg_sender steg_receiver 2>/dev/null || true

        # Start sender
        echo "[*] Starting sender container (172.21.0.20)..."
        docker run -d \
            --name steg_sender \
            --hostname sender \
            --network steg_network \
            --ip 172.21.0.20 \
            -it \
            "${SENDER_IMAGE}" \
            /bin/bash -c "service ssh start && tail -f /dev/null"

        # Start receiver
        echo "[*] Starting receiver container (172.21.0.30)..."
        docker run -d \
            --name steg_receiver \
            --hostname receiver \
            --network steg_network \
            --ip 172.21.0.30 \
            -it \
            "${RECEIVER_IMAGE}" \
            /bin/bash -c "service ssh start && tail -f /dev/null"

        echo ""
        echo "============================================"
        echo "  Lab is RUNNING!"
        echo "============================================"
        echo ""
        echo "  Connect to SENDER:"
        echo "    docker exec -it steg_sender /bin/bash"
        echo ""
        echo "  Connect to RECEIVER:"
        echo "    docker exec -it steg_receiver /bin/bash"
        echo ""
        echo "  Or open two terminal tabs and run both."
        echo "============================================"
        ;;

    stop)
        echo "[*] Stopping and removing lab containers..."
        docker rm -f steg_sender steg_receiver 2>/dev/null || true
        docker network rm steg_network 2>/dev/null || true
        echo "[*] Lab stopped."
        ;;

    sender)
        echo "[*] Opening SENDER terminal..."
        docker exec -it steg_sender /bin/bash
        ;;

    receiver)
        echo "[*] Opening RECEIVER terminal..."
        docker exec -it steg_receiver /bin/bash
        ;;

    status)
        echo "=== Lab Container Status ==="
        docker ps --filter name=steg_sender --filter name=steg_receiver \
            --format "table {{.Names}}\t{{.Status}}\t{{.Networks}}"
        ;;

    *)
        echo "Usage: $0 {start|stop|sender|receiver|status}"
        echo ""
        echo "  start    - Pull images and start both containers"
        echo "  stop     - Stop and remove containers"
        echo "  sender   - Open sender terminal"
        echo "  receiver - Open receiver terminal"
        echo "  status   - Show container status"
        ;;
esac
