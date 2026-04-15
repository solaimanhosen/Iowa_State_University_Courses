import math
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from utils.complex import Complex

def slow_dft(x):
    N = len(x)

    # Convert real inputs to Complex so arithmetic is uniform
    x_c = [v if isinstance(v, Complex) else Complex(float(v), 0.0) for v in x]

    X = []
    for k in range(N):
        acc = Complex(0.0, 0.0)
        for n in range(N):
            angle = -2.0 * math.pi * k * n / N
            # Twiddle factor: e^{-j*angle}
            twiddle = Complex(math.cos(angle), math.sin(angle))
            acc = acc.add(x_c[n].mul(twiddle))
        X.append(acc)

    return X
