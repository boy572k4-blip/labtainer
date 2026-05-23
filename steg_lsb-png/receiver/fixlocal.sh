#!/bin/bash
# fixlocal.sh - Chạy tự động bởi Labtainer framework khi container receiver khởi động.

# Tạo thư mục lab
mkdir -p /root/steg_lab

# Cấu hình SSH server
mkdir -p /var/run/sshd
echo 'root:password' | chpasswd 2>/dev/null || true
sed -i 's/#PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config 2>/dev/null || true
sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config 2>/dev/null || true
echo "PermitRootLogin yes" >> /etc/ssh/sshd_config 2>/dev/null || true
echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config 2>/dev/null || true
service ssh restart 2>/dev/null || /usr/sbin/sshd 2>/dev/null || true

echo ""
echo "=========================================="
echo "  LAB T-STEG01: LSB Steganography"
echo "  MAY: RECEIVER  IP: 172.21.0.30"
echo "=========================================="
echo "  Thu muc lab : ~/steg_lab/"
echo "  Cho nhan anh stego tu sender..."
echo ""
echo "  Sau khi nhan anh, chay:"
echo "    python3 ~/steg_lab/lsb_extract.py \\"
echo "        --input  ~/steg_lab/stego_image.png \\"
echo "        --output ~/steg_lab/extracted_message.txt"
echo "=========================================="
