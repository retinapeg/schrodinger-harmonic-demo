"""Exact harmonic-oscillator eigenpairs in units hbar = m = omega = 1.

    E_n     = n + 1/2
    psi_n(x) = (2^n n!)^(-1/2) pi^(-1/4) H_n(x) exp(-x^2/2)

The Hermite functions are evaluated with the normalised three-term recurrence,
which stays finite for large n (no n! or H_n overflow).
"""
import numpy as np


def exact_energies(k: int) -> np.ndarray:
    """First k exact energies E_n = n + 1/2."""
    return np.arange(k) + 0.5


def exact_psi(k: int, x: np.ndarray) -> np.ndarray:
    """Array of shape (k, len(x)) holding psi_0 .. psi_{k-1} evaluated at x."""
    x = np.asarray(x, dtype=float)
    out = np.empty((k, x.size))
    out[0] = np.pi ** -0.25 * np.exp(-x**2 / 2)
    if k > 1:
        out[1] = np.sqrt(2.0) * x * out[0]
    for n in range(1, k - 1):
        out[n + 1] = np.sqrt(2.0 / (n + 1)) * x * out[n] - np.sqrt(n / (n + 1)) * out[n - 1]
    return out
