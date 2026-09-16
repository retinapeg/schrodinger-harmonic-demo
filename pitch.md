# Demo script (about 75 seconds)

**[0:00, the page loads at `demo/index.html`]**
The quantum harmonic oscillator is the benchmark every physics student meets, and
one of the few systems with an exact answer. We solved it numerically and then
checked every number against that exact answer.

**[0:10, point at the main plot]**
The method is to turn the Schrödinger equation into a matrix using finite
differences and let LAPACK diagonalise it. That takes a few milliseconds. Here
each eigenstate sits at its own energy inside the parabola. The levels are
evenly spaced and start at one half ℏω, not zero: that is the zero-point energy.
Blue states are even, orange states are odd, and state n has n nodes.

**[0:25, click n = 3, then point at the dotted line and the residual]**
The dotted line is the exact Hermite function. It lies on top of our curve, and
the residual panel shows that the difference is only about 3 × 10⁻⁵. The tails also
extend past the classical turning points.

**[0:38, toggle |ψ|², drag the ω slider]**
This shows the probability density. When I change the frequency, the levels
spread out as ℏω. We tested that this rescaling equals a genuine re-solve on the
scaled grid.

**[0:48, scroll to the table and convergence plot]**
All twelve energies match n + ½ to within 8 × 10⁻⁴. When we halve the grid
spacing the error falls by a factor of four, which is textbook second-order
convergence.

**[0:58, close]**
Eighteen physics tests, plus automated checks that render this page and verify
the slide numbers. The limits are stated honestly: it is 1D, uses a hard-wall
box, and the error grows with n. It is a small solver that you can trust because
it is checked against the exact answer.

**[~1:10, end]**
