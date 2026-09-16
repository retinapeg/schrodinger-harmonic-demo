"""Solve the oscillator and bake the results into a self-contained demo page.

    python -m qho.build            # writes demo/index.html

The page needs no server: the solution (at omega = 1) is embedded as JSON and the
browser rescales it to other frequencies exactly, using
    E_n(omega) = omega (n + 1/2),   psi_n(x; omega) = omega^(1/4) psi_n(sqrt(omega) x; 1).
"""
import json
import time
from pathlib import Path

import numpy as np

from .analytic import exact_energies, exact_psi
from .solver import solve

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "demo" / "template.html"
OUTPUT = ROOT / "demo" / "index.html"

K, L, N = 12, 12.0, 2401   # h = 0.01
STRIDE = 4                 # embed every 4th point (display step 0.04)


def convergence(ks=6, Ns=(101, 201, 401, 801, 1601, 3201)):
    rows = []
    for n_pts in Ns:
        s = solve(k=ks, L=10.0, N=n_pts)
        rows.append({"N": n_pts, "h": s.h, "maxErr": float(np.abs(s.energies - exact_energies(ks)).max())})
    return rows


def build_payload():
    t0 = time.perf_counter()
    s = solve(k=K, L=L, N=N)
    solve_ms = (time.perf_counter() - t0) * 1e3
    exact = exact_psi(K, s.x)
    idx = slice(None, None, STRIDE)
    r = lambda a: np.round(a, 6).tolist()
    return {
        "params": {"k": K, "L": L, "N": N, "h": s.h, "solveMs": round(solve_ms, 1)},
        "x": r(s.x[idx]),
        "E": s.energies.tolist(),
        "Eexact": exact_energies(K).tolist(),
        "norm": (np.sum(s.psi**2, axis=1) * s.h).tolist(),
        "fidelity": np.abs(np.sum(s.psi * exact, axis=1) * s.h).tolist(),
        "psi": [r(p) for p in s.psi[:, idx]],
        "psiExact": [r(p) for p in exact[:, idx]],
        "convergence": convergence(),
    }


def main():
    payload = build_payload()
    html = TEMPLATE.read_text().replace("/*__DATA__*/null", json.dumps(payload, separators=(",", ":")))
    OUTPUT.write_text(html)
    err = np.abs(np.array(payload["E"]) - np.array(payload["Eexact"])).max()
    print(f"wrote {OUTPUT.relative_to(ROOT)} ({OUTPUT.stat().st_size / 1e3:.0f} kB); "
          f"{K} states, N={N}, max |E_num - E_exact| = {err:.2e}")


if __name__ == "__main__":
    main()
