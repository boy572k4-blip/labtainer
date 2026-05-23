#!/usr/bin/env python3
"""
lsb_extract.py - Trích xuất thông điệp ẩn từ ảnh PNG (LSB steganography).

Sử dụng:
    python3 lsb_extract.py --input stego_image.png --output extracted_message.txt
"""
import argparse
import sys
from PIL import Image

DELIMITER = "<<<END>>>"

def extract_message(input_path, output_path):
    try:
        img = Image.open(input_path)
    except FileNotFoundError:
        print("[!] Lỗi: Không tìm thấy file '{}'".format(input_path))
        sys.exit(1)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    pixels = list(img.getdata())
    width, height = img.size
    print("[+] Đang phân tích: {} ({}x{})".format(input_path, width, height))

    bits = ""
    for pixel in pixels:
        for val in pixel[:3]:
            bits += str(val & 1)

    message = ""
    i = 0
    while i + 8 <= len(bits):
        byte = bits[i:i+8]
        code = int(byte, 2)
        if 0 < code < 128:
            ch = chr(code)
            message += ch
            if message.endswith(DELIMITER):
                message = message[:-len(DELIMITER)]
                break
        i += 8

    if not message:
        print("[!] Không tìm thấy thông điệp ẩn trong ảnh này.")
        sys.exit(1)

    print("[+] Thông điệp trích xuất: '{}'".format(message))
    print("[+] Độ dài: {} ký tự".format(len(message)))

    with open(output_path, 'w') as f:
        f.write(message + "\n")
    print("[+] Đã lưu vào: {}".format(output_path))

    return message

def main():
    parser = argparse.ArgumentParser(description='LSB Extract - Trích xuất thông điệp từ ảnh PNG')
    parser.add_argument('--input',  required=True, help='Ảnh stego cần trích xuất')
    parser.add_argument('--output', required=True, help='File lưu thông điệp')
    args = parser.parse_args()
    extract_message(args.input, args.output)

if __name__ == "__main__":
    main()
