"""
Question 2b: Slow IDFT
Implements the Inverse Discrete Fourier Transform (IDFT) in O(N^2) time by
multiplying the IDFT transform matrix by the input vector.
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
# Slow IDFT  —  O(N^2)
# ---------------------------------------------------------------------------

def slow_idft(X):
    """
    Compute the IDFT of frequency-domain vector X using the O(N^2)
    matrix-vector product.

    The IDFT is defined as:
        x[n] = (1/N) * sum_{k=0}^{N-1} X[k] * W_N^{-kn}
    where W_N^{-kn} = e^{+j * 2*pi * k * n / N}
                    = cos(2*pi*k*n/N)  +  j * sin(2*pi*k*n/N)

    Note: this differs from the DFT by:
      1. A positive exponent (conjugate twiddle factor)
      2. A 1/N normalization applied after summing

    Parameters
    ----------
    X : list of real or Complex values (up to length 1024)

    Returns
    -------
    x : list of Complex, the recovered time-domain samples
    """
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


# ---------------------------------------------------------------------------
# Main: demonstration — round-trip DFT → IDFT should recover the original signal
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Import slow_dft from p2a for the round-trip verification
    import sys, os
    sys.path.insert(0, os.path.dirname(__file__))
    from p2a import slow_dft

    # Test vector: sine wave sampled at pi/8 radians (16 samples)
    N = 16
    original = [math.sin(2 * math.pi * n / N) for n in range(N)]

    print(f"Original signal (N={N}):")
    for n, v in enumerate(original):
        print(f"  x[{n:2d}] = {v: .6f}")

    # Forward DFT
    X = slow_dft(original)

    print("\nIDFT output x[n] (should match original):")
    recovered = slow_idft(X)
    for n, val in enumerate(recovered):
        print(f"  x[{n:2d}] = {val}")

    # Verify round-trip accuracy
    max_err = max(
        math.sqrt((recovered[n].real - original[n])**2 + recovered[n].imag**2)
        for n in range(N)
    )
    print(f"\nMax round-trip error: {max_err:.2e}  (should be ~0)")
