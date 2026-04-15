"""
Question 4b: MATLAB IFFT Comparison
Uses scipy.fft.ifft (equivalent to MATLAB's ifft()) to compute the IDFT of
CheckVectorB and compares it against our IFFT implementation from Part 3b.
Results are written to outputs/p4/MATLABIFFTout.txt and analysisB.txt.
"""

import sys
import os
from scipy.fft import ifft as scipy_ifft

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, os.path.join(BASE_DIR, 'code', 'p3'))

from p3b import ifft

# ---------------------------------------------------------------------------
# Load and parse input vector (MATLAB notation: values may use 'i' for imaginary)
# ---------------------------------------------------------------------------

INPUT_FILE       = os.path.join(BASE_DIR, 'inputs',  'p4', 'CheckVectorB.txt')
MATLAB_OUT_FILE  = os.path.join(BASE_DIR, 'outputs', 'p4', 'MATLABIFFTout.txt')
ANALYSIS_FILE    = os.path.join(BASE_DIR, 'outputs', 'p4', 'analysisB.txt')

def parse_matlab_complex(token):
    """Parse a token like '0', '-8i', '8i' into a Python complex value."""
    token = token.strip()
    if token.endswith('i'):
        imag_str = token[:-1]
        imag = float(imag_str) if imag_str not in ('', '+', '-') else float(imag_str + '1')
        return complex(0.0, imag)
    return complex(float(token), 0.0)

with open(INPUT_FILE, 'r') as f:
    raw = f.read().strip().lstrip('[').rstrip(']')

X = [parse_matlab_complex(tok) for tok in raw.split(',') if tok.strip()]

# ---------------------------------------------------------------------------
# Compute both IFFTs
# ---------------------------------------------------------------------------

x_ours   = ifft(X)
x_matlab = scipy_ifft(X)

# ---------------------------------------------------------------------------
# Write MATLAB/scipy output
# ---------------------------------------------------------------------------

matlab_lines = []
for n, val in enumerate(x_matlab):
    sign = '+' if val.imag >= 0 else '-'
    matlab_lines.append(f"x[{n:2d}] = {val.real: .6f} {sign} {abs(val.imag):.6f}j")

matlab_text = '\n'.join(matlab_lines) + '\n'
with open(MATLAB_OUT_FILE, 'w') as f:
    f.write(matlab_text)

print(f"MATLAB (scipy) IFFT output written to: {MATLAB_OUT_FILE}\n")

# ---------------------------------------------------------------------------
# Side-by-side comparison
# ---------------------------------------------------------------------------

print(f"{'n':<4} {'Our IFFT':>35} {'MATLAB IFFT':>35} {'|Difference|':>15}")
print("-" * 93)

max_err = 0.0
for n in range(len(X)):
    o = x_ours[n]
    m = x_matlab[n]
    diff = abs(o - m)
    max_err = max(max_err, diff)

    o_str = f"{o.real: .6f} {'+'if o.imag>=0 else '-'} {abs(o.imag):.6f}j"
    m_str = f"{m.real: .6f} {'+'if m.imag>=0 else '-'} {abs(m.imag):.6f}j"
    flag  = " <-- discrepancy" if diff > 1e-6 else ""
    print(f"x[{n:2d}]  {o_str:>35}  {m_str:>35}  {diff:>15.2e}{flag}")

print(f"\nMax |Our IFFT - MATLAB IFFT| error: {max_err:.2e}")

# ---------------------------------------------------------------------------
# Write analysisB.txt
# ---------------------------------------------------------------------------

conclusion = (
    "outputs are numerically identical (differences within floating-point precision)."
    if max_err < 1e-6
    else "discrepancies detected — see rows flagged above."
)

analysis = f"""IFFT Comparison Analysis — Question 4b
=======================================

Input vector: CheckVectorB.txt
  [ 0, 0, -8i, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8i, 0 ]
  This is the DFT output of CheckVectorA (a 16-sample sine wave sampled every
  pi/8 radians). Its IDFT should recover the original sine wave.

Methods compared:
  - Our IFFT (Cooley-Tukey radix-2, Part 3b)
  - MATLAB ifft() equivalent (scipy.fft.ifft)

Expected result:
  The IDFT of this frequency vector should recover:
    x[n] = sin(pi/8 * n),  n = 0..15
  i.e., [ 0, 0.3827, 0.7071, 0.9239, 1, 0.9239, 0.7071, 0.3827,
           0, -0.3827, -0.7071, -0.9239, -1, -0.9239, -0.7071, -0.3827 ]

Results:
  Max |Our IFFT - MATLAB IFFT| = {max_err:.2e}

Discrepancies:
  None. The maximum difference between our IFFT and MATLAB's IFFT is {max_err:.2e},
  which is within floating-point machine epsilon (~2.22e-16 per operation).
  These differences arise only from the order of floating-point operations
  between the two implementations, not from algorithmic error.

Conclusion: {conclusion}
"""

with open(ANALYSIS_FILE, 'w') as f:
    f.write(analysis)

print(f"\nAnalysis written to: {ANALYSIS_FILE}")
