# Taylor polynomial on a set

Let `E` be a normed real vector space, let `f : Real -> E`, let `s` be an arbitrary set of real numbers, let `x0 : Real`, and let `n` be a natural number. The order-`n` Taylor polynomial of `f` at `x0`, using totalized derivatives within `s`, has coefficient

`(k! : Real)^-1 smul iteratedDerivWithin k f s x0`

on the shifted power `(X - x0)^k`. It is a member of `PolynomialModule Real E`. Its value at `x` is

`sum k in range (n + 1), (((k! : Real)^-1 * (x - x0)^k) smul iteratedDerivWithin k f s x0)`.

No differentiability, convexity, openness, membership, or completeness hypothesis is needed for these definitions because `iteratedDerivWithin` is totalized. The polynomial definition alone asserts no approximation or remainder property.

## Mathlib

Declarations: `taylorCoeffWithin`, `taylorWithin`, `taylorWithinEval`, `taylor_within_apply`
File: `Mathlib/Analysis/Calculus/Taylor.lean`
