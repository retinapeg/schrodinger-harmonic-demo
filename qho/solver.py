"""Finite-difference solver for the 1D time-independent Schrödinger equation.

    H = -1/2 d^2/dx^2 + V(x),   V(x) = 1/2 x^2      (hbar = m = omega = 1)

On a uniform grid x_i in [-L, L] with spacing h and hard walls (psi = 0 just
outside the box) the second derivative becomes the tridiagonal stencil
(psi_{i-1} - 2 psi_i + psi_{i+1}) / h^2, so H is a symmetric tridiagonal matrix:

    diagonal     1/h^2 + V(x_i)
    off-diagonal -1/(2 h^2)

Its lowest eigenpairs are found with LAPACK via scipy.linalg.eigh_tridiagonal.
Discretisation error in E_n is O(h^2).
"""
from dataclasses import dataclass

import numpy as np
from scipy.linalg import eigh_tridiagonal

from .analytic import exact_psi


def harmonic_potential(x: np.ndarray) -> np.ndarray:
    return 0.5 * np.asarray(x) ** 2


@dataclass
class Solution:
    x: np.ndarray        # grid, shape (N,)
    V: np.ndarray        # potential on the grid, shape (N,)
    energies: np.ndarray # shape (k,), ascending
    psi: np.ndarray      # shape (k, N), each row normalised: sum(psi^2) h = 1

    @property
    def h(self) -> float:
        return float(self.x[1] - self.x[0])


def solve(k: int = 10, L: float = 10.0, N: int = 2000, potential=harmonic_potential) -> Solution:
    """Lowest k eigenpairs of H on N grid points spanning [-L, L]."""
    x = np.linspace(-L, L, N)
    h = x[1] - x[0]
    V = potential(x)
    diag = 1.0 / h**2 + V
    off = np.full(N - 1, -0.5 / h**2)
    E, vecs = eigh_tridiagonal(diag, off, select="i", select_range=(0, k - 1))
    psi = vecs.T / np.sqrt(h)  # eigenvectors have unit 2-norm -> unit L2 norm on the grid

    # Eigenvectors have arbitrary sign; align each with the exact Hermite
    # function so numerical and analytical curves can be overlaid directly.
    ref = exact_psi(k, x)
    signs = np.sign(np.sum(psi * ref, axis=1))
    signs[signs == 0] = 1.0
    psi *= signs[:, None]
    return Solution(x=x, V=V, energies=E, psi=psi)
