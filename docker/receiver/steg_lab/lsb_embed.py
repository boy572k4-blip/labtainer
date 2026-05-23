#!/usr/bin/env python3
"""LSB Steganography - Embed message into PNG"""
import sys, os, argparse
from PIL import Image

END_DELIMITER = '\x00' * 16

def text_to_bits(text):
    bits = []
    for char in text:
        byte = ord(char)
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)
    return bits

def embed_message(cover_path, stego_path, message):
    img = Image.open(cover_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    width, height = img.size
    pixels = list(img.getdata())
    max_bytes = (width * height * 3) // 8
    full_message = message + END_DELIMITER
    msg_bytes = len(full_message.encode('utf-8'))
    print(f"[INFO] Image: {cover_path} ({width}x{height})")
    print(f"[INFO] Max capacity: {max_bytes} bytes")
    print(f"[INFO] Message: '{message}' ({msg_bytes} bytes with delimiter)")
    if msg_bytes > max_bytes:
        print(f"[ERROR] Message too long!"); sys.exit(1)
    message_bits = text_to_bits(full_message)
    bit_index = 0
    new_pixels = []
    for pixel in pixels:
        r, g, b = pixel[0], pixel[1], pixel[2]
        if bit_index < len(message_bits):
            r = (r & 0xFE) | message_bits[bit_index]; bit_index += 1
        if bit_index < len(message_bits):
            g = (g & 0xFE) | message_bits[bit_index]; bit_index += 1
        if bit_index < len(message_bits):
            b = (b & 0xFE) | message_bits[bit_index]; bit_index += 1
        new_pixels.append((r, g, b))
    stego_img = Image.new('RGB', (width, height))
    stego_img.putdata(new_pixels)
    os.makedirs(os.path.dirname(os.path.abspath(stego_path)), exist_ok=True)
    stego_img.save(stego_path, 'PNG')
    changed = sum(1 for a, b2 in zip(list(Image.open(cover_path).convert('RGB').getdata()), new_pixels) if a != b2)
    print(f"[OK] Embedded {bit_index} bits into {stego_path}")
    print(f"[OK] Pixels changed: {changed}/{len(new_pixels)} ({100*changed/len(new_pixels):.2f}%)")

def main():
    parser = argparse.ArgumentParser(description='LSB Embed')
    parser.add_argument('--input',   '-i', required=True)
    parser.add_argument('--output',  '-o', required=True)
    parser.add_argument('--message', '-m', required=True)
    args = parser.parse_args()
    print("="*55); print("  LSB STEGANOGRAPHY - EMBED"); print("="*55)
    embed_message(args.input, args.output, args.message)
    print("="*55)

if __name__ == '__main__':
    main()
