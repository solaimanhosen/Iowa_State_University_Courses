"""
Question 4b: Slow IDFT Check
Computes the IDFT of CheckVectorB using the slow O(N^2) implementation
from Part 2b and writes the result to outputs/p4/IDFTout.txt.
"""

import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'code', 'p2'))

from p2b import slow_idft, Complex

# ---------------------------------------------------------------------------
# Load and parse input vector (MATLAB notation: values may use 'i' for imaginary)
# ---------------------------------------------------------------------------

INPUT_FILE  = os.path.join(BASE_DIR, 'inputs',  'p4', 'CheckVectorB.txt')
OUTPUT_FILE = os.path.join(BASE_DIR, 'outputs', 'p4', 'IDFTout.txt')

def parse_matlab_complex(token):
    """Parse a token like '0', '-8i', '8i' into a Complex value."""
    token = token.strip()
    if token.endswith('i'):
        imag_str = token[:-1]
        imag = float(imag_str) if imag_str not in ('', '+', '-') else float(imag_str + '1')
        return Complex(0.0, imag)
    return Complex(float(token), 0.0)

with open(INPUT_FILE, 'r') as f:
    raw = f.read().strip().lstrip('[').rstrip(']')

X = [parse_matlab_complex(tok) for tok in raw.split(',') if tok.strip()]

print(f"Input vector ({len(X)} samples):")
for k, v in enumerate(X):
    print(f"  X[{k:2d}] = {v}")

# ---------------------------------------------------------------------------
# Compute Slow IDFT
# ---------------------------------------------------------------------------

x = slow_idft(X)

# ---------------------------------------------------------------------------
# Write output
# ---------------------------------------------------------------------------

lines = []
for n, val in enumerate(x):
    sign = '+' if val.imag >= 0 else '-'
    lines.append(f"x[{n:2d}] = {val.real: .6f} {sign} {abs(val.imag):.6f}j")

output_text = '\n'.join(lines) + '\n'

with open(OUTPUT_FILE, 'w') as f:
    f.write(output_text)

print(f"\nSlow IDFT output written to: {OUTPUT_FILE}")
print(output_text)
