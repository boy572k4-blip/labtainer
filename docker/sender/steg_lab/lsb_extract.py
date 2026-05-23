#!/usr/bin/env python3
"""LSB Steganography - Extract message from PNG"""
import sys, os, argparse
from PIL import Image

def bits_to_text(bits):
    chars = []
    for i in range(0, len(bits)-7, 8):
        byte = 0
        for j in range(8): byte = (byte << 1) | bits[i+j]
        chars.append(chr(byte) if 32 <= byte <= 126 else ('\x00' if byte == 0 else '?'))
    return ''.join(chars)

def extract_message(stego_path, output_path=None):
    img = Image.open(stego_path)
    if img.mode != 'RGB': img = img.convert('RGB')
    width, height = img.size
    pixels = list(img.getdata())
    print(f"[INFO] Analyzing: {stego_path} ({width}x{height})")
    bits = []
    for pixel in pixels:
        bits.extend([pixel[0]&1, pixel[1]&1, pixel[2]&1])
    null_count = 0; result_bits = []; found_end = False
    for i in range(0, len(bits)-7, 8):
        bv = sum(bits[i+j] << (7-j) for j in range(8))
        result_bits.extend(bits[i:i+8])
        if bv == 0:
            null_count += 1
            if null_count >= 16:
                result_bits = result_bits[:-(null_count*8)]; found_end = True; break
        else:
            null_count = 0
    if not found_end:
        print("[WARNING] Delimiter not found")
    message = bits_to_text(result_bits)
    print(f"[OK] Extracted message: '{message}'")
    if output_path:
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, 'w') as f: f.write(message + '\n')
        print(f"[OK] Saved to: {output_path}")
    return message

def main():
    parser = argparse.ArgumentParser(description='LSB Extract')
    parser.add_argument('--input', '-i', required=True)
    parser.add_argument('--output', '-o', default=None)
    args = parser.parse_args()
    print("="*55); print("  LSB STEGANOGRAPHY - EXTRACT"); print("="*55)
    extract_message(args.input, args.output)
    print("="*55)

if __name__ == '__main__':
    main()
