#!/usr/bin/env python3
"""
generate_cover.py - Tạo ảnh PNG 512x512 làm ảnh gốc cho bài lab.
Script này chạy tự động khi container sender khởi động.
"""
import os
import sys
from PIL import Image
import numpy as np
import random

def generate_cover_image(output_path, width=512, height=512):
    random.seed(42)
    np.random.seed(42)

    img_array = np.zeros((height, width, 3), dtype=np.uint8)

    for y in range(height):
        for x in range(width):
            r = int((x / width) * 200 + 30)
            g = int((y / height) * 200 + 30)
            b = int(((x + y) / (width + height)) * 180 + 50)
            r = min(255, max(0, r + random.randint(-15, 15)))
            g = min(255, max(0, g + random.randint(-15, 15)))
            b = min(255, max(0, b + random.randint(-15, 15)))
            img_array[y, x] = [r, g, b]

    img = Image.fromarray(img_array, 'RGB')
    img.save(output_path, 'PNG')
    print("[+] Đã tạo ảnh: {}".format(output_path))
    print("    Kích thước : {}x{} pixels".format(width, height))
    print("    Mode       : RGB")
    print("    Dung lượng nhúng tối đa: {} bytes".format((width * height * 3) // 8))

if __name__ == "__main__":
    out = "/root/steg_lab/cover_image.png"
    if not os.path.exists(out):
        generate_cover_image(out)
    else:
        print("[*] Ảnh cover đã tồn tại: {}".format(out))
