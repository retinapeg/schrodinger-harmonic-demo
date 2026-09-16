import json
import re

import numpy as np

from qho import build


def test_payload_is_consistent():
    p = build.build_payload()
    k = p["params"]["k"]
    assert len(p["E"]) == len(p["psi"]) == len(p["psiExact"]) == k
    assert all(len(row) == len(p["x"]) for row in p["psi"])
    assert np.all(np.diff(p["E"]) > 0)
    # Convergence study: error must shrink monotonically as the grid is refined.
    errs = [r["maxErr"] for r in p["convergence"]]
    assert all(a > b for a, b in zip(errs, errs[1:]))


def test_build_writes_self_contained_page(tmp_path, monkeypatch):
    out = tmp_path / "index.html"
    monkeypatch.setattr(build, "OUTPUT", out)
    monkeypatch.setattr(build, "ROOT", tmp_path)
    build.main()
    html = out.read_text()
    assert "/*__DATA__*/null" not in html
    data = json.loads(re.search(r"const D = (\{.*?\});\n", html).group(1))
    assert data["params"]["N"] == build.N
