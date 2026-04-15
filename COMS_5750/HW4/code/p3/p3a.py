import math
import sys
import os

def fft(x):
    N = len(x)

    if N == 0 or (N & (N - 1)) != 0:
        raise ValueError(f"Input length must be a power of 2, got {N}")

    # Base case
    if N == 1:
        return [complex(x[0])]

    # Split into even and odd
    even = fft(x[0::2])
    odd  = fft(x[1::2])

    # Combine with butterfly
    X = [0] * N
    half = N // 2
    for k in range(half):
        twiddle = complex(math.cos(-2 * math.pi * k / N),
                          math.sin(-2 * math.pi * k / N))
        t = twiddle * odd[k]
        X[k]        = even[k] + t
        X[k + half] = even[k] - t

    return X
