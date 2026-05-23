#!/usr/bin/env python3
"""
LSB Steganography - Extract secret message from PNG image
T-STEG01: LSB Steganography in PNG Images
"""
import argparse
import sys
from PIL import Image


def bits_to_text(bits: str) -> str:
    """Convert binary bit string back to text, stopping at EOF marker."""
    chars = []
    i = 0
    while i + 7 < len(bits):
        byte = bits[i:i + 8]
        value = int(byte, 2)
        if value == 0:
            break
        chars.append(chr(value))
        i += 8
    return "".join(chars)


def extract_message(stego_path: str, output_path: str) -> str:
    """Extract hidden message from stego image using LSB."""
    img = Image.open(stego_path).convert("RGB")
    width, height = img.size

    print(f"[INFO] Image size: {width}x{height} pixels")
    print(f"[INFO] Max extractable: {(width * height * 3 // 8) - 8} characters")

    bits = ""
    max_chars = 10000  # Safety limit
    max_bits = max_chars * 8 + 64  # message bits + EOF marker bits

    collected = 0
    done = False

    for y in range(height):
        if done:
            break
        for x in range(width):
            if done:
                break
            r, g, b = img.getpixel((x, y))
            for channel_val in [r, g, b]:
                bits += str(channel_val & 1)
                collected += 1

                # Check for EOF every 8 bits
                if collected % 8 == 0 and collected >= 64:
                    # Look for 8 consecutive null bytes
                    recent = bits[-64:]
                    if all(c == '0' for c in recent):
                        done = True
                        break

                if collected >= max_bits:
                    done = True
                    break

    message = bits_to_text(bits)

    if not message:
        print("[WARNING] No hidden message found or image is not a stego image.")
        message = ""
    else:
        print(f"[SUCCESS] Message extracted: {len(message)} characters")

    # Save to output file
    with open(output_path, 'w') as f:
        f.write(message + "\n")

    print(f"[INFO] Message saved to: {output_path}")
    return message


def main():
    parser = argparse.ArgumentParser(
        description="LSB Steganography - Extract message from PNG image"
    )
    parser.add_argument("--input",  required=True, help="Path to stego image (PNG)")
    parser.add_argument("--output", required=True, help="Path to save extracted message")
    args = parser.parse_args()

    print("=" * 50)
    print("  LSB STEGANOGRAPHY - EXTRACT")
    print("=" * 50)
    message = extract_message(args.input, args.output)
    print(f"\n  Extracted message: {message}")
    print("=" * 50)


if __name__ == "__main__":
    main()
