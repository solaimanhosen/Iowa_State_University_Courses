import math
import sys
import os

def _ifft_unscaled(X):
    N = len(X)

    # Base case
    if N == 1:
        return [complex(X[0])]

    # Split into even and odd
    even = _ifft_unscaled(X[0::2])
    odd  = _ifft_unscaled(X[1::2])

    # Combine with butterfly using +j exponent twiddle factors
    result = [0] * N
    half = N // 2
    for k in range(half):
        twiddle = complex(math.cos(2 * math.pi * k / N),   # positive exponent
                          math.sin(2 * math.pi * k / N))
        t = twiddle * odd[k]
        result[k]        = even[k] + t
        result[k + half] = even[k] - t

    return result

def ifft(X):
    N = len(X)

    if N == 0 or (N & (N - 1)) != 0:
        raise ValueError(f"Input length must be a power of 2, got {N}")

    unscaled = _ifft_unscaled(X)
    return [v / N for v in unscaled]
