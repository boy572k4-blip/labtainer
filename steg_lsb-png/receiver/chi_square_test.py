#!/usr/bin/env python3
"""
chi_square_test.py - Chi-Square Attack để phát hiện dữ liệu ẩn trong ảnh PNG.

Sử dụng:
    python3 chi_square_test.py --image stego_image.png
"""
import argparse
import sys
import numpy as np
from PIL import Image

try:
    from scipy.stats import chisquare
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False

def chi_square_attack(image_path):
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print("[!] Lỗi: Không tìm thấy file '{}'".format(image_path))
        sys.exit(1)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    data = np.array(img)
    channel = data[:, :, 0].flatten()
    freq = np.bincount(channel, minlength=256)

    observed = []
    expected = []
    for i in range(0, 255, 2):
        total = freq[i] + freq[i+1]
        exp = total / 2.0
        if exp > 0:
            observed.append(float(freq[i]))
            expected.append(exp)

    observed = np.array(observed)
    expected = np.array(expected)

    if HAS_SCIPY:
        chi2, pval = chisquare(observed, f_exp=expected)
    else:
        chi2 = float(np.sum((observed - expected)**2 / (expected + 1e-10)))
        df = max(len(observed) - 1, 1)
        pval = float(np.exp(-chi2 / (2.0 * df)))

    return chi2, pval

def interpret(pval):
    if pval < 0.001:
        return ">>> RẤT CÓ KHẢ NĂNG chứa dữ liệu ẩn (p < 0.001)"
    elif pval < 0.05:
        return ">>> CÓ KHẢ NĂNG chứa dữ liệu ẩn (p < 0.05)"
    elif pval < 0.1:
        return ">>> NGHI NGỜ - cần phân tích thêm (p < 0.1)"
    else:
        return ">>> KHÔNG phát hiện dữ liệu ẩn (p >= 0.1)"

def main():
    parser = argparse.ArgumentParser(description='Chi-Square Attack - Phát hiện steganography')
    parser.add_argument('--image', required=True, help='Ảnh cần phân tích')
    args = parser.parse_args()

    print("=" * 54)
    print("  CHI-SQUARE ATTACK - PHAT HIEN STEGANOGRAPHY")
    print("=" * 54)
    print("[*] Phan tich: {}".format(args.image))

    chi2, pval = chi_square_attack(args.image)

    print("\n  Chi2 statistic : {:.4f}".format(chi2))
    print("  p-value        : {:.6f}".format(pval))
    print("\n  {}".format(interpret(pval)))
    print("\n  Giai thich:")
    print("  - p-value THAP -> phan phoi LSB bat thuong -> CO du lieu an")
    print("  - p-value CAO  -> phan phoi LSB tu nhien   -> KHONG co du lieu an")
    print("=" * 54)

if __name__ == "__main__":
    main()
