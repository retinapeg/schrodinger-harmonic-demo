"""Quantum harmonic oscillator: numerical (finite differences) and exact solutions.

Units: hbar = m = omega = 1 unless stated otherwise.
"""
from .analytic import exact_energies, exact_psi
from .solver import Solution, solve

__all__ = ["exact_energies", "exact_psi", "Solution", "solve"]
