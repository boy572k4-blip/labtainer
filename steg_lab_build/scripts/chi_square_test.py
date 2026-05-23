#!/usr/bin/env python3
"""
Chi-Square Attack for LSB Steganography Detection
T-STEG01: LSB Steganography in PNG Images

Theory (Westfeld & Pfitzmann 1999):
  LSB embedding EQUALIZES the frequency of value-pairs (2k, 2k+1).
  Natural images have unequal pair frequencies (high chi-sq statistic).
  After LSB embedding with random/text data, pairs equalize (lower chi-sq).

  Detection metric: chi-sq / degrees-of-freedom (normalized)
  - Natural image  : ratio >> 1  (pair frequencies are very unequal)
  - Stego image    : ratio closer to 1 (pairs are more equal)

  The RATIO between cover and stego chi-sq values is the key indicator.
"""
import argparse
import sys
import math
from PIL import Image


def chi_square_lsb(image_path: str):
    """
    Compute Chi-Square statistic testing whether LSB value-pairs are equal.

    H0: freq[2k] == freq[2k+1]  (steganography present: pairs are equalized)
    HA: freq[2k] != freq[2k+1]  (natural image: pairs are unequal)

    Returns: (chi_sq, p_value, df, normalized_ratio)
    """
    img = Image.open(image_path).convert("RGB")
    width, height = img.size

    # Count R-channel value frequencies
    freq = [0] * 256
    for y in range(height):
        for x in range(width):
            r, _, _ = img.getpixel((x, y))
            freq[r] += 1

    total = width * height
    chi_sq = 0.0
    df = 0

    for k in range(128):
        n_even = freq[2 * k]
        n_odd  = freq[2 * k + 1]
        pair_total = n_even + n_odd

        if pair_total < 5:
            continue

        expected = pair_total / 2.0
        chi_sq += ((n_even - expected) ** 2) / expected
        chi_sq += ((n_odd  - expected) ** 2) / expected
        df += 1

    # Normalized chi-sq (per degree of freedom)
    # Natural image: >> 1  |  After embedding: approaches 1
    normalized = chi_sq / df if df > 0 else 0.0

    # p-value (upper tail) using Wilson-Hilferty with log-scale for extreme values
    p_value = chi_square_p_value_robust(chi_sq, df)

    return chi_sq, p_value, df, normalized


def chi_square_p_value_robust(chi_sq: float, df: int) -> float:
    """
    Robust p-value calculation for Chi-Square using Wilson-Hilferty.
    Handles extreme values via log-normal approximation.
    """
    if df <= 0 or chi_sq <= 0:
        return 1.0

    k = float(df)
    x = float(chi_sq)

    # Wilson-Hilferty: transforms chi-sq to approximately standard normal
    mu    = 1.0 - 2.0 / (9.0 * k)
    sigma = math.sqrt(2.0 / (9.0 * k))
    z     = (math.pow(x / k, 1.0 / 3.0) - mu) / sigma

    # Upper tail: P(Z >= z)
    if z > 37.0:
        # Approximation for very large z: log(p) ≈ -z^2/2 - log(z) - log(2pi)/2
        log_p = -0.5 * z * z - math.log(z) - 0.5 * math.log(2 * math.pi)
        return max(1e-300, math.exp(log_p))
    elif z < -8.0:
        return 1.0

    return max(1e-300, 1.0 - normal_cdf(z))


def normal_cdf(z: float) -> float:
    """CDF of standard normal — Abramowitz & Stegun formula 26.2.17."""
    if z < 0:
        return 1.0 - normal_cdf(-z)
    if z > 8.5:
        return 1.0

    p  =  0.2316419
    b1 =  0.319381530
    b2 = -0.356563782
    b3 =  1.781477937
    b4 = -1.821255978
    b5 =  1.330274429

    t    = 1.0 / (1.0 + p * z)
    poly = t * (b1 + t * (b2 + t * (b3 + t * (b4 + t * b5))))
    pdf  = math.exp(-0.5 * z * z) / math.sqrt(2.0 * math.pi)
    return 1.0 - pdf * poly


def interpret_lsb_equalization(normalized: float) -> str:
    """Interpret the normalized chi-sq ratio for educational output."""
    if normalized > 500:
        return "VERY HIGH pair asymmetry — strongly suggests CLEAN (cover) image"
    elif normalized > 100:
        return "HIGH pair asymmetry — image is likely CLEAN or lightly embedded"
    elif normalized > 20:
        return "MODERATE equalization — partial LSB embedding detected"
    elif normalized > 5:
        return "SIGNIFICANT equalization — heavy LSB embedding strongly suspected"
    else:
        return "NEAR-PERFECT equalization — image almost certainly contains hidden data"


def main():
    parser = argparse.ArgumentParser(
        description="Chi-Square Attack — Detect LSB steganography in PNG images"
    )
    parser.add_argument("--image", required=True, help="Path to image to analyze")
    args = parser.parse_args()

    print("=" * 60)
    print("  CHI-SQUARE ATTACK - Steganography Detection")
    print("=" * 60)
    print(f"  Analyzing: {args.image}")
    print("-" * 60)

    try:
        chi_sq, p_value, df, normalized = chi_square_lsb(args.image)

        print(f"  Chi-Square statistic     : {chi_sq:.2f}")
        print(f"  Degrees of freedom       : {df}")
        print(f"  Chi-sq / df (normalized) : {normalized:.2f}")
        print(f"  p-value                  : {p_value:.2e}")
        print("-" * 60)
        print(f"  Interpretation: {interpret_lsb_equalization(normalized)}")
        print("=" * 60)
        print(f"\n  KEY METRIC: chi_sq/df = {normalized:.2f}")
        print(f"  (Cover image: large value | Stego image: smaller value)")
        print(f"\np-value={p_value:.2e}")
        print(f"chi_normalized={normalized:.2f}")

    except FileNotFoundError:
        print(f"[ERROR] File not found: {args.image}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback; traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
