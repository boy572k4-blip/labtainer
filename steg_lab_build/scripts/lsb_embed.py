#!/usr/bin/env python3
"""
LSB Steganography - Embed secret message into PNG image
T-STEG01: LSB Steganography in PNG Images
"""
import argparse
import sys
from PIL import Image


def text_to_bits(text: str) -> str:
    """Convert text string to binary bit string with EOF marker."""
    bits = ""
    for char in text:
        bits += format(ord(char), '08b')
    # Append EOF marker: 8 null bytes = 64 zero bits
    bits += '00000000' * 8
    return bits


def embed_message(cover_path: str, stego_path: str, message: str) -> None:
    """Embed message into image using LSB of R, G, B channels."""
    img = Image.open(cover_path).convert("RGB")
    width, height = img.size

    bits = text_to_bits(message)
    max_capacity = width * height * 3

    if len(bits) > max_capacity:
        print(f"[ERROR] Message too long! Max capacity: {max_capacity // 8 - 8} characters")
        sys.exit(1)

    print(f"[INFO] Image size: {width}x{height} pixels")
    print(f"[INFO] Max capacity: {(max_capacity // 8) - 8} characters")
    print(f"[INFO] Message length: {len(message)} characters ({len(bits)} bits)")

    bit_index = 0
    new_pixels = []

    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            new_rgb = [r, g, b]

            for channel in range(3):
                if bit_index < len(bits):
                    new_rgb[channel] = (new_rgb[channel] & 0xFE) | int(bits[bit_index])
                    bit_index += 1

            new_pixels.append(tuple(new_rgb))

    stego_img = Image.new("RGB", img.size)
    stego_img.putdata(new_pixels)
    stego_img.save(stego_path, "PNG")

    print(f"[SUCCESS] Stego image saved to: {stego_path}")
    print(f"[INFO] Total bits embedded: {bit_index}")


def main():
    parser = argparse.ArgumentParser(
        description="LSB Steganography - Embed message into PNG image"
    )
    parser.add_argument("--input",   required=True, help="Path to cover image (PNG)")
    parser.add_argument("--output",  required=True, help="Path to save stego image (PNG)")
    parser.add_argument("--message", required=True, help="Secret message to embed")
    args = parser.parse_args()

    print("=" * 50)
    print("  LSB STEGANOGRAPHY - EMBED")
    print("=" * 50)
    embed_message(args.input, args.output, args.message)
    print("=" * 50)


if __name__ == "__main__":
    main()
