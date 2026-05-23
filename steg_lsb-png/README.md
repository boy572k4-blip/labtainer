# T-STEG01: LSB Steganography in PNG Images

Bài lab thực hành kỹ thuật **giấu tin LSB** trong ảnh PNG, dùng nền tảng Labtainer.

## Cấu trúc (theo chuẩn Labtainer IModule)

```
steg_lsb-png/
├── config/
│   ├── start.config          ← Cấu hình container, mạng, IP (QUAN TRỌNG NHẤT)
│   ├── results.config        ← Định nghĩa artifact chấm điểm
│   ├── goals.config          ← Tiêu chí chấm điểm tự động
│   └── receiver.results.config
├── dockerfiles/
│   ├── Dockerfile.steg_lsb-png.sender.student
│   └── Dockerfile.steg_lsb-png.receiver.student
├── sender/                   ← Files copy vào /root/steg_lab/ của sender
│   ├── fixlocal.sh           ← Chạy tự động khi container khởi động
│   ├── generate_cover.py
│   ├── lsb_embed.py
│   └── chi_square_test.py
├── receiver/                 ← Files copy vào /root/steg_lab/ của receiver
│   ├── fixlocal.sh
│   ├── lsb_extract.py
│   └── chi_square_test.py
└── README.md
```

## Cách dùng trên LabtainerVM

```bash
# 1. Tải imodule
imodule https://github.com/boy572k4-blip/labtainer/raw/main/imodule_steg_lsb-png.tar

# 2. Chạy lab
cd ~/labtainers/labtainer-student
labtainer steg_lsb-png
```

## Thông tin kỹ thuật

| | |
|---|---|
| Kỹ thuật | LSB Insertion, kênh R/G/B |
| Dung lượng tối đa | (512 × 512 × 3) / 8 = 98,304 bytes |
| Phát hiện | Chi-Square Attack |
| Sender IP | 172.21.0.20 |
| Receiver IP | 172.21.0.30 |
| SSH password | password |
