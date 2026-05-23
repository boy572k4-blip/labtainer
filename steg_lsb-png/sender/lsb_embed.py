#!/usr/bin/env python3
"""
lsb_embed.py - Nhúng thông điệp bí mật vào ảnh PNG bằng kỹ thuật LSB.

Sử dụng:
    python3 lsb_embed.py --input cover_image.png \\
                         --output stego_image.png \\
                         --message "BIET_TEN_TOI_KHONG"
"""
import argparse
import sys
from PIL import Image

DELIMITER = "<<<END>>>"

def text_to_bits(text):
    bits = ""
    for ch in text:
        bits += format(ord(ch), '08b')
    return bits

def embed_message(input_path, output_path, message):
    try:
        img = Image.open(input_path)
    except FileNotFoundError:
        print("[!] Lỗi: Không tìm thấy file '{}'".format(input_path))
        sys.exit(1)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    pixels = list(img.getdata())
    width, height = img.size

    full_message = message + DELIMITER
    bits = text_to_bits(full_message)
    max_bits = width * height * 3

    if len(bits) > max_bits:
        print("[!] Lỗi: Thông điệp quá dài! Tối đa {} ký tự.".format(max_bits // 8))
        sys.exit(1)

    print("[+] Ảnh gốc  : {} ({}x{})".format(input_path, width, height))
    print("[+] Thông điệp: '{}' ({} ký tự)".format(message, len(message)))
    print("[+] Bits cần nhúng: {} / {} bits".format(len(bits), max_bits))

    new_pixels = []
    bit_index = 0

    for pixel in pixels:
        r, g, b = pixel
        new_ch = []
        for val in (r, g, b):
            if bit_index < len(bits):
                val = (val & 0xFE) | int(bits[bit_index])
                bit_index += 1
            new_ch.append(val)
        new_pixels.append(tuple(new_ch))

    out_img = Image.new('RGB', (width, height))
    out_img.putdata(new_pixels)
    out_img.save(output_path, 'PNG')

    print("[+] Đã lưu ảnh stego: {}".format(output_path))
    print("[+] Tỉ lệ sử dụng   : {:.2f}%".format(len(bits) / max_bits * 100))

def main():
    parser = argparse.ArgumentParser(description='LSB Embed - Nhúng thông điệp vào ảnh PNG')
    parser.add_argument('--input',   required=True, help='Ảnh gốc (cover image)')
    parser.add_argument('--output',  required=True, help='Ảnh đầu ra (stego image)')
    parser.add_argument('--message', required=True, help='Thông điệp bí mật')
    args = parser.parse_args()
    embed_message(args.input, args.output, args.message)

if __name__ == "__main__":
    main()
