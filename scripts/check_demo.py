"""Breaker check for the demo page.

    python scripts/check_demo.py

1. demo/index.html is template.html plus embedded data (no stale markup).
2. The embedded data matches a fresh solve (energies, norms, fidelity, psi).
3. The embedded physics is right: E_n = n + 1/2, normalised, high fidelity.
4. The page actually runs: headless Chrome renders it and the DOM contains the
   KPI tiles, all 12 table rows and drawn Plotly SVGs (needs the Plotly CDN).
Exits non-zero with a reason on the first failure.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import NoReturn

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from qho import build  # noqa: E402

CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
DATA_RE = re.compile(r"const D = (\{.*?\});\n")


def fail(msg) -> NoReturn:
    print(f"FAIL: {msg}")
    sys.exit(1)


def render_dom(url, timeout=45):
    """Dump the DOM with headless Chrome. Chrome can linger after dumping, so poll and kill it."""
    with tempfile.TemporaryDirectory() as tmp:
        dump = Path(tmp) / "dom.html"
        with dump.open("w") as fh:
            proc = subprocess.Popen(
                [CHROME, "--headless", "--disable-gpu", "--no-first-run", f"--user-data-dir={tmp}/profile",
                 "--window-size=1400,1400", "--virtual-time-budget=8000", "--dump-dom", url],
                stdout=fh, stderr=subprocess.DEVNULL)
            deadline = time.monotonic() + timeout
            try:
                while time.monotonic() < deadline and "</html>" not in dump.read_text():
                    if proc.poll() is not None:
                        break
                    time.sleep(0.5)
            finally:
                proc.kill()
                proc.wait()
        return dump.read_text()


def main():
    page = (ROOT / "demo" / "index.html").read_text()
    template = (ROOT / "demo" / "template.html").read_text()
    m = DATA_RE.search(page)
    if not m:
        fail("no embedded data in demo/index.html")
    if page[: m.start(1)] + "/*__DATA__*/null" + page[m.end(1):] != template:
        fail("demo/index.html is stale: rerun python -m qho.build")
    D = json.loads(m.group(1))

    fresh = build.build_payload()
    for key in ("E", "Eexact", "norm", "fidelity", "x"):
        if not np.allclose(D[key], fresh[key], rtol=0, atol=1e-9):
            fail(f"embedded {key} differs from a fresh solve")
    if not np.allclose(D["psi"], fresh["psi"], atol=1e-6):
        fail("embedded psi differs from a fresh solve")

    E, Ex = np.array(D["E"]), np.array(D["Eexact"])
    if not np.array_equal(Ex, np.arange(len(E)) + 0.5):
        fail("exact energies are not n + 1/2")
    if np.abs(E - Ex).max() > 1e-3:
        fail(f"max |dE| = {np.abs(E - Ex).max():.2e} > 1e-3")
    if np.abs(np.array(D["norm"]) - 1).max() > 1e-9:
        fail("eigenfunctions not normalised")
    if min(D["fidelity"]) < 0.9999:
        fail("fidelity below 0.9999")
    print(f"data ok: {len(E)} states, max |dE| = {np.abs(E - Ex).max():.2e}")

    if not Path(CHROME).exists():
        fail(f"Chrome not found at {CHROME} (set CHROME=...)")
    out = render_dom((ROOT / "demo" / "index.html").as_uri() + "?n=5&omega=1.5&view=prob")
    rows = len(re.findall(r'<tr data-n="\d+"', out))
    svgs = out.count('class="main-svg"')
    checks = {
        "table rows": rows == len(E),
        "plots drawn (>= 4 main-svg)": svgs >= 4,
        "KPI tiles": "eigenstates solved" in out,
        "URL preset n=5 applied": "State n = 5" in out,
        "omega preset applied": ">1.50<" in out,
        "exponents fully superscripted": not re.search("[⁰¹²³⁴⁵⁶⁷⁸⁹][0-9]", out),
        "no load-error banner": 'id="loadError"' not in out or 'id="loadError" hidden' in out,
    }
    bad = [k for k, ok in checks.items() if not ok]
    if bad:
        fail(f"rendered page: {', '.join(bad)} (rows={rows}, svgs={svgs})")
    print(f"render ok: {rows} table rows, {svgs} plot SVGs, presets applied")

    # Simulated CDN outage: numbers must still render and the banner must explain why.
    with tempfile.TemporaryDirectory() as tmp:
        offline = Path(tmp) / "offline.html"
        offline.write_text(page.replace("https://cdn.jsdelivr.net/npm/plotly.js-dist-min", "file:///nonexistent/plotly"))
        out = render_dom(offline.as_uri())
    rows = len(re.findall(r'<tr data-n="\d+"', out))
    if 'id="loadError" hidden' in out or "Charts unavailable" not in out or rows != len(E):
        fail(f"offline fallback: banner not shown or table missing (rows={rows})")
    print(f"offline fallback ok: banner shown, {rows} table rows still rendered")
    print("PASS")


if __name__ == "__main__":
    main()
