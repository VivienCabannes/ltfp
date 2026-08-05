---
kind: node
declaration: theorem
statement: formalized
proof: formalized
lean: trapezoidalPeriodicConst, trapezoidalPeriodicConst_one, abs_trapezoidal_error_le_of_periodic, isBigO_trapezoidal_error_of_periodic
---

# Periodic smooth-function error rate (Exercise 1.28)

Let `s : Nat` satisfy `1 <= s`, let `f : Real -> Real` satisfy `ContDiff Real s f`, and suppose `f` is one-periodic:

`f(x + 1) = f(x)` for every `x : Real`.

Let `0 <= M`, and suppose

`abs (iteratedDeriv s f x) <= M`

for every `x` in `[0, 1]`. Define the constant depending only on `s` by

`C_s = (Nat.factorial s : Real)^(-1)`

`      * integral u in 0..1, abs (bernoulliFun s u)`.

Then, for every positive natural number `N`,

`abs (T_N(f; 0, 1) - integral x in 0..1, f x) <= C_s * M / N^s`.

Consequently,

`(fun N : Nat => T_N(f; 0, 1) - integral x in 0..1, f x)`

`  =O[atTop] (fun N => ((N : Real)^s)^(-1))`.

## Proof

First, every iterated derivative is one-periodic. Apply `iteratedDeriv r` to the function equality expressing periodicity and use the rule for the iterated derivative of composition with a translation. Hence

`iteratedDeriv r f (x + 1) = iteratedDeriv r f x`.

In particular, the endpoint values agree for every order `r` with `1 <= r < s`. The periodic Bernoulli-kernel identity therefore applies. Taking absolute values, using the triangle inequality for the finite sum and the integral, and applying the bound on `iteratedDeriv s f` gives

`abs (T_N(f; 0, 1) - integral x in 0..1, f x)`

`<= (M / (s! * N^s)) * sum k in {0, ..., N - 1},`

`     integral x in k/N..(k+1)/N, abs (B_s(N*x - k))`.

On each panel use the substitution `u = N*x - k`. Its contribution becomes

`(1 / N) * integral u in 0..1, abs (B_s(u))`.

There are `N` panels, so the sum of these contributions is simply the integral over `[0, 1]`. The result is

`C_s * M / N^s`,

as claimed. The constant is finite because `B_s` is a polynomial and hence continuous on the compact unit interval. Continuous differentiability also implies all interval-integrability conditions used in the argument.

For `s = 1`, `B_1(u) = u - 1/2`, so `C_1 = 1/4`; this recovers the first-derivative estimate on the unit interval. The explicit bound immediately gives the displayed `atTop` Big-O statement.


## Roadmap and coverage

- [Deterministic quadrature error](../README.md)
- [Project coverage](../../../coverage/README.md)

## Source locations

- `sources/ltfp_book.pdf` — Chapter 1, Section 1.2.5, printed page 19, Exercise 1.28
- `sources/ltfp_exercises.pdf` — Chapter 1, Exercise 1.28, printed page 4

## Planning record

Legacy Mathlib assessment: `missing`.

No matching periodic trapezoidal-rate theorem exists in pinned Mathlib. Compiled checks verify periodicity of every iteratedDeriv from Function.Periodic.funext and iteratedDeriv_comp_add_const, the exact panel substitution via intervalIntegral.integral_comp_mul_sub, and the resulting atTop Big-O corollary. The raw panel polynomial bernoulliFun is appropriate for every s >= 1; periodizedBernoulli.continuous excludes s = 1.

## Depends on

- [Periodic Bernoulli-kernel trapezoidal identity](periodic-bernoulli-kernel-trapezoidal-identity.md)
- [Iterated Frechet derivative](../../differential-and-integral-calculus/definitions/iterated-frechet-derivative.md)
