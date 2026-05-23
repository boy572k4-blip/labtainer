#!/usr/bin/env python3
"""Chi-Square Attack - Statistical detection of LSB steganography"""
import sys, os, argparse, math
from PIL import Image

def normal_cdf(x):
    t = 1.0/(1.0+0.2316419*abs(x))
    p = t*(0.319381530+t*(-0.356563782+t*(1.781477937+t*(-1.821255978+t*1.330274429))))
    cdf = 1.0-(1.0/math.sqrt(2*math.pi))*math.exp(-0.5*x*x)*p
    return (1.0-cdf) if x < 0 else cdf

def chi2_pvalue(chi2, df):
    if chi2 <= 0: return 1.0
    if df <= 0:   return 0.0
    h = 2.0/(9.0*df)
    z = (pow(chi2/df, 1.0/3.0) - (1-h)) / math.sqrt(max(h, 1e-10))
    return 1.0 - normal_cdf(z)

def chi_square_attack(image_path, ch=0):
    img = Image.open(image_path)
    if img.mode != 'RGB': img = img.convert('RGB')
    pixels = list(img.getdata())
    freq = [0]*256
    for px in pixels: freq[px[ch]] += 1
    chi2, df = 0.0, 0
    for k in range(128):
        n0, n1 = freq[2*k], freq[2*k+1]
        if n0+n1 == 0: continue
        exp = (n0+n1)/2.0
        chi2 += (n0-exp)**2/exp + (n1-exp)**2/exp
        df += 1
    return chi2, (chi2_pvalue(chi2, df) if df > 0 else 1.0), df

def analyze_image(image_path):
    print(f"\n{'='*60}\n  CHI-SQUARE ATTACK - LSB STEGANALYSIS\n{'='*60}")
    print(f"  File: {image_path}")
    img = Image.open(image_path); w, h = img.size
    print(f"  Size: {w}x{h} | File: {os.path.getsize(image_path):,} bytes")
    print(f"\n  {'Channel':<10} {'Chi2':>12} {'DF':>8} {'p-value':>12}  Verdict")
    print(f"  {'-'*55}")
    pvals = []
    for ci, cn in enumerate(['R (Red)', 'G (Green)', 'B (Blue)']):
        chi2, pv, df = chi_square_attack(image_path, ci)
        pvals.append(pv)
        v = "LIKELY HIDDEN DATA" if pv > 0.05 else ("UNCERTAIN" if pv > 0.01 else "CLEAN")
        print(f"  {cn:<10} {chi2:>12.2f} {df:>8d} {pv:>12.6f}  {v}")
    avg = sum(pvals)/len(pvals)
    print(f"  {'-'*55}")
    print(f"  {'Average':<10} {'':>12} {'':>8} {avg:>12.6f}  {'STEGO DETECTED' if avg > 0.05 else 'CLEAN'}")
    print(f"\n  avg_pvalue={avg:.6f}")
    for i, n in enumerate(['R','G','B']): print(f"  {n}_pvalue={pvals[i]:.6f}")
    print(f"{'='*60}\n")
    return avg, pvals

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image', '-i', required=True)
    args = parser.parse_args()
    analyze_image(args.image)

if __name__ == '__main__':
    main()
