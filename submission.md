# Submission: Quantum Harmonic Oscillator, solved numerically and checked exactly

**One-liner:** A finite-difference Schrödinger solver whose every eigenvalue and
eigenstate is checked live against the exact ℏω(n + ½) solution, in an
interactive visualisation.

## What it does
- Builds the Hamiltonian H = −½ d²/dx² + ½x² as a symmetric tridiagonal matrix and
  solves for the lowest 12 eigenpairs with LAPACK (`scipy.linalg.eigh_tridiagonal`).
- Compares the results with the exact Hermite-function solution:
  - max |ΔE| = 8.3 × 10⁻⁴
  - worst infidelity ≈ 8 × 10⁻⁸
  - measured O(h²) convergence (× 4.0 per halving of h)
- Provides a single-file interactive page:
  - eigenstates drawn at their energies in the well
  - ψ and |ψ|² views, with an overlay of the exact solution
  - a per-state residual panel
  - an ω slider using the exact scaling law
  - a table comparing numerical and exact energies, and a convergence plot
  - URL presets, keyboard navigation, and light and dark themes

## How we verified it
- **18 pytest tests** check:
  - normalisation, orthogonality, parity (−1)ⁿ and node count
  - the exact wavefunction match and second-order convergence
  - that ω rescaling equals a re-solve on the scaled grid
  - direct solves at ω = 0.5 and ω = 2
  - the known small-box failure mode
  - the build output
- **`scripts/check_demo.py`** checks that:
  - the embedded data matches a fresh solve
  - the page renders in headless Chrome, with the plots, 12 table rows and URL presets
  - a simulated CDN outage shows the fallback banner
- **`scripts/check_slides.py`** checks that:
  - the deck has 7 slides and all shapes fit on the slide
  - every image decodes and every slide has speaker notes
  - the slide text matches a regeneration from a fresh solve

## Run it
```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m pytest -q && .venv/bin/python -m qho.build && open demo/index.html
```

## Links
- **Public demo URL:** not deployed. The repository has no git remote or
  authorised hosting destination, so the demo runs locally.
- **Slides:** `slides/qho-demo.pptx` (7 slides)
- **Screenshots:** `docs/demo-light.png`, `docs/demo-dark.png`, `docs/demo-probability.png`

## Limitations
- The solver is 1D and time-independent, and only the harmonic potential is validated.
- A hard-wall box is used, so the box must enclose the turning points.
- The O(h²) error grows with n.
- The ω slider reuses the ω = 1 solve on a rescaled grid.
- The charts need the Plotly CDN; the numbers still work offline.
- Full details are in README.md.

## Built with
Python, NumPy, SciPy, Plotly.js, python-pptx and matplotlib.
