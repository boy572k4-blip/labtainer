#!/usr/bin/env python3
"""
Generate a realistic cover image for LSB steganography lab.
Creates a 512x512 PNG that mimics real JPEG-decoded image statistics:
 - Pixel pair (2k, 2k+1) frequencies are UNEQUAL (natural characteristic)
 - This gives low p-value in chi-square test for clean cover image
 - After LSB embedding with random data, pairs equalize -> HIGH p-value
"""
import random
import math
from PIL import Image


def generate_cover_image(width=512, height=512, output_path="/root/steg_lab/cover_image.png"):
    """
    Generate a cover image with realistic image statistics.
    Uses biased even-value distribution to mimic JPEG artifacts.
    """
    random.seed(42)
    img = Image.new("RGB", (width, height))
    pixels = []

    for y in range(height):
        for x in range(width):
            # Vertical gradient: sky-blue (top) to green-earth (bottom)
            t = y / height

            if t < 0.55:
                sky_t  = t / 0.55
                base_r = int(130 + 70 * (1 - sky_t))
                base_g = int(170 + 50 * (1 - sky_t))
                base_b = int(220 - 30 * sky_t)
            else:
                gnd_t  = (t - 0.55) / 0.45
                base_r = int(75  + 70  * gnd_t)
                base_g = int(110 + 50  * gnd_t)
                base_b = int(55  + 25  * gnd_t)

            # Add natural-looking wave texture
            wave = int(18 * math.sin(x * 0.04 + 0.3) * math.cos(y * 0.035))
            fine = int(7  * math.sin(x * 0.18 + y * 0.13))

            # Smooth Gaussian noise
            nr = int(random.gauss(0, 9))
            ng = int(random.gauss(0, 7))
            nb = int(random.gauss(0, 11))

            r_raw = base_r + wave + fine + nr
            g_raw = base_g + wave + fine + ng
            b_raw = base_b + wave + fine + nb

            # Key: force R values toward EVEN to create natural pair asymmetry
            # This mimics real camera/JPEG-decoded images where even values are
            # more frequent due to DCT rounding in the original source
            # We round to nearest even with probability 0.7 (subtle, not absolute)
            def bias_even(v):
                v = max(0, min(255, v))
                if (v % 2 == 1) and (random.random() < 0.70):
                    # Flip to neighbor with slight preference for even
                    v = v - 1 if v > 0 else v + 1
                return v

            r = bias_even(r_raw)
            g = max(0, min(255, g_raw))   # G and B are natural
            b = max(0, min(255, b_raw))

            pixels.append((r, g, b))

    img.putdata(pixels)
    img.save(output_path, "PNG")
    print(f"[INFO] Cover image created : {output_path}")
    print(f"[INFO] Size                : {width}x{height} | Mode: RGB")
    print(f"[INFO] Max embed capacity  : {(width * height * 3 // 8) - 8} characters")


if __name__ == "__main__":
    generate_cover_image()
