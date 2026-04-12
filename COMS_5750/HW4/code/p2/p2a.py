"""
Question 2a: Slow DFT
Implements the Discrete Fourier Transform (DFT) in O(N^2) time by
multiplying the DFT transform matrix by the input vector.
Complex number arithmetic (+, -, *) is implemented manually without
using any complex number library.
"""

import math


# ---------------------------------------------------------------------------
# Custom Complex Number Class (no library arithmetic allowed)
# ---------------------------------------------------------------------------

class Complex:
    """Represents a complex number a + bj with manual +, -, * operations."""

    def __init__(self, real=0.0, imag=0.0):
        self.real = real
        self.imag = imag

    def add(self, other):
        """Return self + other."""
        return Complex(self.real + other.real, self.imag + other.imag)

    def sub(self, other):
        """Return self - other."""
        return Complex(self.real - other.real, self.imag - other.imag)

    def mul(self, other):
        """Return self * other using (a+bj)(c+dj) = (ac-bd) + (ad+bc)j."""
        real = self.real * other.real - self.imag * other.imag
        imag = self.real * other.imag + self.imag * other.real
        return Complex(real, imag)

    def __repr__(self):
        if self.imag >= 0:
            return f"{self.real:.6f} + {self.imag:.6f}j"
        else:
            return f"{self.real:.6f} - {abs(self.imag):.6f}j"


# ---------------------------------------------------------------------------
# Slow DFT  —  O(N^2)
# ---------------------------------------------------------------------------

def slow_dft(x):
    """
    Compute the DFT of input vector x using the O(N^2) matrix-vector product.

    The DFT is defined as:
        X[k] = sum_{n=0}^{N-1} x[n] * W_N^{kn}
    where W_N^{kn} = e^{-j * 2*pi * k * n / N}
                   = cos(2*pi*k*n/N)  -  j * sin(2*pi*k*n/N)

    Parameters
    ----------
    x : list of real or Complex values (up to length 1024)

    Returns
    -------
    X : list of Complex, the DFT coefficients
    """
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


# ---------------------------------------------------------------------------
# Main: demonstration
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Test vector: sine wave sampled at pi/8 radians (16 samples, period = 16)
    # x[n] = sin(2*pi*n/16)  =>  should show a spike at k=1 and k=15
    N = 16
    x = [math.sin(2 * math.pi * n / N) for n in range(N)]

    print(f"Input vector (N={N}):")
    for n, v in enumerate(x):
        print(f"  x[{n:2d}] = {v: .6f}")

    print("\nDFT output X[k]:")
    X = slow_dft(x)
    for k, val in enumerate(X):
        print(f"  X[{k:2d}] = {val}")
