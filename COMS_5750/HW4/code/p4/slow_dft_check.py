"""
Question 4a: Slow DFT Check
Computes the DFT of CheckVectorA using the slow O(N^2) implementation
from Part 2a and writes the result to outputs/p4/DFTout.txt.
"""

import sys
import os

# Resolve paths relative to this file's location
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'code', 'p2'))

from p2a import slow_dft

# ---------------------------------------------------------------------------
# Load input vector
# ---------------------------------------------------------------------------

INPUT_FILE  = os.path.join(BASE_DIR, 'inputs',  'p4', 'CheckVectorA.txt')
OUTPUT_FILE = os.path.join(BASE_DIR, 'outputs', 'p4', 'DFTout.txt')

with open(INPUT_FILE, 'r') as f:
    raw = f.read().strip()

# Parse "[ v0, v1, ..., vN ]" format
raw = raw.strip().lstrip('[').rstrip(']')
x = [float(v.strip()) for v in raw.split(',') if v.strip()]

print(f"Input vector ({len(x)} samples): {x}")

# ---------------------------------------------------------------------------
# Compute Slow DFT
# ---------------------------------------------------------------------------

X = slow_dft(x)

# ---------------------------------------------------------------------------
# Write output
# ---------------------------------------------------------------------------

lines = []
for k, val in enumerate(X):
    sign = '+' if val.imag >= 0 else '-'
    lines.append(f"X[{k:2d}] = {val.real: .6f} {sign} {abs(val.imag):.6f}j")

output_text = '\n'.join(lines) + '\n'

with open(OUTPUT_FILE, 'w') as f:
    f.write(output_text)

print(f"\nSlow DFT output written to: {OUTPUT_FILE}")
print(output_text)
