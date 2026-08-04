# Law of total expectation

Let `E` be a complete real normed space, let `mu` be an arbitrary measure, let `m <= m0`, and suppose that the corresponding trimmed measure is sigma-finite. Then the Bochner integral of a conditional expectation equals the integral of the original function:

`integral x, mu[f | m] x dmu = integral x, f x dmu`.

No probability or finite-measure assumption is required. The equality also covers nonintegrable `f` through the totalized conventions for conditional expectation and the Bochner integral.

## Mathlib

Declarations: `MeasureTheory.integral_condExp`
File: `Mathlib/MeasureTheory/Function/ConditionalExpectation/Basic.lean`
