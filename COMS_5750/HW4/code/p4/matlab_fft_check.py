"""
Question 4a: MATLAB FFT Comparison
Uses scipy.fft (equivalent to MATLAB's fft()) to compute the DFT of
CheckVectorA and compares it against our FFT implementation from Part 3a.
Results are written to outputs/p4/MATLABFFTout.txt.
"""

import sys
import os
from scipy.fft import fft as scipy_fft

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'code', 'p3'))

from p3a import fft

# ---------------------------------------------------------------------------
# Load input vector
# ---------------------------------------------------------------------------

INPUT_FILE  = os.path.join(BASE_DIR, 'inputs',  'p4', 'CheckVectorA.txt')
OUTPUT_FILE = os.path.join(BASE_DIR, 'outputs', 'p4', 'MATLABFFTout.txt')

with open(INPUT_FILE, 'r') as f:
    raw = f.read().strip()

raw = raw.strip().lstrip('[').rstrip(']')
x = [float(v.strip()) for v in raw.split(',') if v.strip()]

# ---------------------------------------------------------------------------
# Compute both FFTs
# ---------------------------------------------------------------------------

X_ours   = fft(x)
X_matlab = scipy_fft(x)

# ---------------------------------------------------------------------------
# Write MATLAB/scipy output to file
# ---------------------------------------------------------------------------

lines = []
for k, val in enumerate(X_matlab):
    sign = '+' if val.imag >= 0 else '-'
    lines.append(f"X[{k:2d}] = {val.real: .6f} {sign} {abs(val.imag):.6f}j")

output_text = '\n'.join(lines) + '\n'

with open(OUTPUT_FILE, 'w') as f:
    f.write(output_text)

print(f"MATLAB (scipy) FFT output written to: {OUTPUT_FILE}\n")

# ---------------------------------------------------------------------------
# Side-by-side comparison
# ---------------------------------------------------------------------------

print(f"{'k':<4} {'Our FFT':>35} {'MATLAB FFT':>35} {'|Difference|':>15}")
print("-" * 93)

max_err = 0.0
for k in range(len(x)):
    o = X_ours[k]
    m = X_matlab[k]
    diff = abs(o - m)
    max_err = max(max_err, diff)

    o_str = f"{o.real: .6f} {'+'if o.imag>=0 else '-'} {abs(o.imag):.6f}j"
    m_str = f"{m.real: .6f} {'+'if m.imag>=0 else '-'} {abs(m.imag):.6f}j"
    flag  = " <-- discrepancy" if diff > 1e-6 else ""
    print(f"X[{k:2d}]  {o_str:>35}  {m_str:>35}  {diff:>15.2e}{flag}")

print(f"\nMax |Our FFT - MATLAB FFT| error: {max_err:.2e}")
if max_err < 1e-6:
    print("Conclusion: outputs are numerically identical (differences within floating-point precision).")
else:
    print("Conclusion: discrepancies detected — see rows flagged above.")
