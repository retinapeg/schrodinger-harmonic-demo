"""The demo's omega slider rescales the omega = 1 solution instead of re-solving.

On a grid scaled by x' = x / sqrt(omega) the finite-difference Hamiltonian for
V = 1/2 omega^2 x^2 is exactly omega times the omega = 1 matrix, so the rescaled
numbers are the finite-difference solution on that grid, not an approximation.
"""
import numpy as np
import pytest

from qho import exact_energies, exact_psi, solve

K, L, N = 8, 10.0, 1601


@pytest.mark.parametrize("omega", [0.5, 1.5, 2.0])
def test_rescaling_equals_resolve_on_scaled_grid(omega):
    base = solve(k=K, L=L, N=N)
    s = np.sqrt(omega)
    direct = solve(k=K, L=L / s, N=N, potential=lambda x: 0.5 * omega**2 * np.asarray(x) ** 2)
    np.testing.assert_allclose(direct.x, base.x / s, atol=1e-12)
    np.testing.assert_allclose(direct.energies, omega * base.energies, rtol=1e-10)
    # solve() fixes signs against the omega = 1 Hermite functions, which is ambiguous for
    # other potentials, so compare each eigenvector up to an overall sign.
    signs = np.sign(np.sum(direct.psi * base.psi, axis=1))[:, None]
    np.testing.assert_allclose(signs * direct.psi, omega**0.25 * base.psi, atol=1e-8)


@pytest.mark.parametrize("omega", [0.5, 2.0])
def test_resolve_matches_exact_hbar_omega(omega):
    # Fixed physical grid: E_n = omega (n + 1/2) and psi_n(x) = omega^(1/4) psi_n(sqrt(omega) x).
    x_half = 10.0 / np.sqrt(min(omega, 1.0))
    sol = solve(k=K, L=x_half, N=4001, potential=lambda x: 0.5 * omega**2 * np.asarray(x) ** 2)
    np.testing.assert_allclose(sol.energies, omega * exact_energies(K), atol=2e-3 * omega)
    ref = omega**0.25 * exact_psi(K, np.sqrt(omega) * sol.x)
    fidelity = np.abs(np.sum(sol.psi * ref, axis=1) * sol.h)
    assert fidelity.min() > 0.9999
