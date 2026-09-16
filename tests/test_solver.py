import numpy as np
import pytest

from qho import exact_energies, exact_psi, solve

K = 12


@pytest.fixture(scope="module")
def sol():
    return solve(k=K, L=10.0, N=2000)


def test_eigenvalues_ascending_and_distinct(sol):
    assert np.all(np.diff(sol.energies) > 0.5)


def test_energies_match_n_plus_half(sol):
    err = np.abs(sol.energies - exact_energies(K))
    assert err.max() < 1e-3, err


def test_level_spacing_is_hbar_omega(sol):
    np.testing.assert_allclose(np.diff(sol.energies), 1.0, atol=2e-4)


def test_eigenfunctions_normalised(sol):
    norms = np.sum(sol.psi**2, axis=1) * sol.h
    np.testing.assert_allclose(norms, 1.0, atol=1e-10)


def test_eigenfunctions_orthogonal(sol):
    overlap = sol.psi @ sol.psi.T * sol.h
    np.testing.assert_allclose(overlap, np.eye(K), atol=1e-8)


def test_parity(sol):
    # psi_n(-x) = (-1)^n psi_n(x); the grid is symmetric so reversal is x -> -x.
    for n, psi in enumerate(sol.psi):
        np.testing.assert_allclose(psi[::-1], (-1) ** n * psi, atol=1e-6)


def test_node_count_equals_n(sol):
    for n, psi in enumerate(sol.psi):
        core = psi[np.abs(psi) > 1e-6 * np.abs(psi).max()]
        nodes = np.count_nonzero(np.diff(np.sign(core)) != 0)
        assert nodes == n


def test_matches_exact_wavefunctions(sol):
    ref = exact_psi(K, sol.x)
    fidelity = np.abs(np.sum(sol.psi * ref, axis=1) * sol.h)
    assert fidelity.min() > 0.9999
    assert np.abs(sol.psi - ref).max() < 1e-3


def test_exact_psi_is_orthonormal():
    x = np.linspace(-12, 12, 4001)
    psi = exact_psi(20, x)
    np.testing.assert_allclose(psi @ psi.T * (x[1] - x[0]), np.eye(20), atol=1e-10)


def test_second_order_convergence():
    # Halving h should cut the energy error by ~4x (central differences are O(h^2)).
    errs = []
    for N in (401, 801, 1601):
        s = solve(k=6, L=10.0, N=N)
        errs.append(np.abs(s.energies - exact_energies(6)).max())
    ratios = np.array(errs[:-1]) / np.array(errs[1:])
    np.testing.assert_allclose(ratios, 4.0, rtol=0.05)


def test_box_too_small_raises_energies():
    # Hard walls inside the classically-allowed region push levels up: a real limitation.
    s = solve(k=6, L=3.0, N=1000)
    assert s.energies[-1] > exact_energies(6)[-1] + 0.1
