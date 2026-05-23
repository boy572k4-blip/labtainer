#!/usr/bin/env python3
import sys, os, math, random
from PIL import Image

def generate_cover_image(output_path, width=640, height=480, seed=42):
    random.seed(seed)
    img = Image.new('RGB', (width, height))
    pixels = []
    for y in range(height):
        for x in range(width):
            r = int(128 + 127 * math.sin(x/80.0) * math.cos(y/60.0))
            g = int(128 + 127 * math.sin(x/100.0 + 1.5) * math.cos(y/80.0 + 0.5))
            b = int(128 + 127 * math.sin(x/60.0 + 3.0) * math.cos(y/100.0 + 1.0))
            r = max(0, min(255, r + random.randint(-5, 5)))
            g = max(0, min(255, g + random.randint(-5, 5)))
            b = max(0, min(255, b + random.randint(-5, 5)))
            pixels.append((r, g, b))
    img.putdata(pixels)
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, 'PNG')
    print(f"[OK] Cover image: {output_path} ({width}x{height})")
    print(f"     Max embed capacity: {(width*height*3)//8} bytes")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "/home/ubuntu/steg_lab/cover_image.png"
    generate_cover_image(out)
