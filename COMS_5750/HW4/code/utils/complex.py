"""
Custom Complex number class for Problems 2 and 3.
No library arithmetic is used — only +, -, * are implemented manually,
as required by the problem statement.
"""


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
