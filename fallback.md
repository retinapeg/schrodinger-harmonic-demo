# Fallback demo plan

The live demo is a local file. It needs no server or accounts, but it fetches
Plotly.js and web fonts from a CDN. Use the first option below that works.

1. **Live page:** open `demo/index.html` in a browser. If the plots appear,
   follow `pitch.md`.
2. **Offline, with numbers only:** if the page shows the **"Charts unavailable"**
   banner, Plotly could not be loaded. The KPI tiles, the energy table
   (click a row), the state facts and the ω slider still work. Narrate from the
   table: E_num against E_exact and 1 − fidelity. Show the plots from the
   screenshots instead (option 3).
3. **Screenshots:** `docs/demo-light.png` shows the full page at n = 4.
   `docs/demo-dark.png` is the hero view. `docs/demo-probability.png` shows the
   |ψ|² view with 10 states.
4. **Slides:** `slides/qho-demo.pptx` covers the physics, the method, the
   visualisation, the validation numbers and the limitations. Speaker notes are
   on every slide.
5. **Terminal proof:** these commands need no browser.
   ```bash
   .venv/bin/python -m pytest -q          # 18 passed
   .venv/bin/python -m qho.build          # prints max |E_num - E_exact| = 8.28e-04
   ```

## What the fallbacks do not show
- The screenshots and slides are static; they show no interaction.
- The screenshots were captured from this build with Google Chrome.
- The offline mode shows no plots.
- No public URL exists. Do not describe the demo as deployed.
