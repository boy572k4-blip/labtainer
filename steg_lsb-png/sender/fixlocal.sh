#!/bin/bash
# fixlocal.sh - Chạy tự động bởi Labtainer framework khi container sender khởi động.
# Đây là cơ chế chuẩn của Labtainer để setup môi trường.

# Tạo thư mục lab nếu chưa có
mkdir -p /root/steg_lab

# Tạo ảnh cover nếu chưa tồn tại
if [ ! -f /root/steg_lab/cover_image.png ]; then
    python3 /root/steg_lab/generate_cover.py
fi

# Cấu hình SSH client để không hỏi host key
mkdir -p /root/.ssh
cat > /root/.ssh/config << 'SSHEOF'
Host *
    StrictHostKeyChecking no
    UserKnownHostsFile /dev/null
    LogLevel ERROR
SSHEOF
chmod 700 /root/.ssh
chmod 600 /root/.ssh/config

echo ""
echo "=========================================="
echo "  LAB T-STEG01: LSB Steganography"
echo "  MAY: SENDER  IP: 172.21.0.20"
echo "=========================================="
echo "  Thu muc lab : ~/steg_lab/"
echo "  Anh goc     : ~/steg_lab/cover_image.png"
echo ""
echo "  Bat dau bang lenh:"
echo "    ls ~/steg_lab/"
echo "=========================================="
