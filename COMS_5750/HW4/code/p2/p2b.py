import math
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.complex import Complex

def slow_idft(X):
    N = len(X)

    # Convert real inputs to Complex so arithmetic is uniform.
    # Use hasattr to handle Complex objects from other modules too.
    X_c = [v if hasattr(v, 'real') and hasattr(v, 'imag') and hasattr(v, 'mul')
           else Complex(float(v), 0.0) for v in X]

    x = []
    for n in range(N):
        acc = Complex(0.0, 0.0)
        for k in range(N):
            angle = 2.0 * math.pi * k * n / N   # positive exponent
            twiddle = Complex(math.cos(angle), math.sin(angle))
            acc = acc.add(X_c[k].mul(twiddle))
        # 1/N normalization
        x.append(Complex(acc.real / N, acc.imag / N))

    return x
