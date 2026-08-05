/-
Copyright (c) 2026 Vivien Cabannes. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Vivien Cabannes
-/
import Mathlib.Analysis.Calculus.IteratedDeriv.Defs
import Mathlib.MeasureTheory.Integral.IntervalIntegral.IntegrationByParts
import Mathlib.MeasureTheory.Integral.IntervalIntegral.TrapezoidalRule
import Mathlib.NumberTheory.ZetaValues

/-!
# An exact Bernoulli-kernel representation of the trapezoidal error

For a function `f : ℝ → ℝ` of class `C^s` on `ℝ` whose derivatives of orders `1, …, s - 1` take
the same value at `0` and at `1`, the error of the `N`-panel trapezoidal rule on `[0, 1]` is
exactly an integral of `f⁽ˢ⁾` against the piecewise Bernoulli kernel
`x ↦ B_s (N * x - k) / (s ! * N ^ s)` on the `k`-th panel `[k / N, (k + 1) / N]`.

This is the Euler–Maclaurin style identity behind the `O(N⁻ˢ)` convergence rate of the
trapezoidal rule for periodic smooth integrands. Pinned Mathlib has the Bernoulli polynomials
(`bernoulliFun`) and the trapezoidal rule (`trapezoidal_error`) but nothing connecting them, so
the identity is built here from `hasDerivAt_bernoulliFun`, `bernoulliFun_endpoints_eq_of_ne_one`
and `intervalIntegral.integral_mul_deriv_eq_deriv_mul`.

The proof introduces the panel kernel `bernoulliPanel N k r x = B_r (N * x - k) / (r ! * N ^ r)`,
whose defining property is `(bernoulliPanel N k (r + 1))' = bernoulliPanel N k r`. Integration by
parts at order `1` turns the panel integral into the one-panel trapezoidal error, and each further
integration by parts flips a sign, the boundary terms telescoping to zero thanks to
`B_(r+1) (1) = B_(r+1) (0)` and the endpoint agreement hypothesis.

## Graph nodes

* `trapezoidal_error_eq_bernoulli_kernel` formalizes the tier-2 node
  `Periodic Bernoulli-kernel trapezoidal identity`, transcribing
  `informal_content/periodic-bernoulli-kernel-trapezoidal-identity.md`.

## Source

Francis Bach, *Learning Theory from First Principles*, Chapter 1, Section 1.2.5, printed page 19,
Exercise 1.28 (see also *Learning Theory from First Principles - Exercises*, Chapter 1,
Exercise 1.28, printed page 4).
-/

open Finset MeasureTheory intervalIntegral

open scoped Nat

/-- The Bernoulli quadrature kernel of order `r` on the `k`-th panel `[k / N, (k + 1) / N]`
of the uniform subdivision of `[0, 1]` into `N` panels, namely
`x ↦ B_r (N * x - k) / (r ! * N ^ r)`. -/
private noncomputable def bernoulliPanel (N k r : ℕ) (x : ℝ) : ℝ :=
  bernoulliFun r ((N : ℝ) * x - k) / (r ! * (N : ℝ) ^ r)

/-- The normalisation of `bernoulliPanel` is chosen so that the kernel of order `r + 1` is an
antiderivative of the kernel of order `r`: the factor `r + 1` coming from
`hasDerivAt_bernoulliFun` and the factor `N` coming from the chain rule cancel against
`(r + 1)! = (r + 1) * r !` and `N ^ (r + 1) = N ^ r * N`. -/
private lemma hasDerivAt_bernoulliPanel {N : ℕ} (hN : 0 < N) (k r : ℕ) (x : ℝ) :
    HasDerivAt (bernoulliPanel N k (r + 1)) (bernoulliPanel N k r x) x := by
  have hNR : (N : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hN.ne'
  have h1 : HasDerivAt (fun y : ℝ => (N : ℝ) * y - (k : ℝ)) (N : ℝ) x := by
    simpa using ((hasDerivAt_id x).const_mul (N : ℝ)).sub_const (k : ℝ)
  refine (((hasDerivAt_bernoulliFun (r + 1) ((N : ℝ) * x - k)).comp x h1).div_const
    (((r + 1)! : ℝ) * (N : ℝ) ^ (r + 1))).congr_deriv ?_
  simp only [bernoulliPanel, Nat.add_sub_cancel, Nat.factorial_succ, Nat.cast_mul,
    Nat.cast_add, Nat.cast_one, pow_succ]
  have hfac : ((r)! : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr (Nat.factorial_ne_zero r)
  have hr1 : ((r : ℝ) + 1) ≠ 0 := by positivity
  field_simp

/-- The panel kernels are continuous, being polynomials in `x`. -/
private lemma continuous_bernoulliPanel (N k r : ℕ) : Continuous (bernoulliPanel N k r) := by
  unfold bernoulliPanel
  fun_prop

/-- The value of the `k`-th panel kernel at the left endpoint `k / N` of its panel. -/
private lemma bernoulliPanel_left {N : ℕ} (hN : 0 < N) (k r : ℕ) :
    bernoulliPanel N k r ((k : ℝ) / N) = bernoulliFun r 0 / ((r ! : ℝ) * (N : ℝ) ^ r) := by
  have hNR : (N : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hN.ne'
  simp only [bernoulliPanel]
  rw [show (N : ℝ) * ((k : ℝ) / N) - k = 0 by field_simp; ring]

/-- The value of the `k`-th panel kernel at the right endpoint `(k + 1) / N` of its panel. -/
private lemma bernoulliPanel_right {N : ℕ} (hN : 0 < N) (k r : ℕ) :
    bernoulliPanel N k r (((k : ℝ) + 1) / N) = bernoulliFun r 1 / ((r ! : ℝ) * (N : ℝ) ^ r) := by
  have hNR : (N : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hN.ne'
  simp only [bernoulliPanel]
  rw [show (N : ℝ) * (((k : ℝ) + 1) / N) - k = 1 by field_simp; ring]

/-- The Bernoulli-panel representation of the trapezoidal error, at every intermediate order
`1 ≤ r ≤ s`. The case `r = 1` is integration by parts against the sawtooth
`x ↦ x - (k + 1 / 2) / N`, and the step from `r` to `r + 1` is one further integration by parts
whose boundary contributions telescope to zero. -/
private lemma trapezoidal_error_eq_bernoulliPanel_sum {f : ℝ → ℝ} {s N : ℕ}
    (hN : 0 < N) (hf : ContDiff ℝ s f)
    (hper : ∀ r : ℕ, 1 ≤ r → r < s → iteratedDeriv r f 1 = iteratedDeriv r f 0)
    (r : ℕ) (hr : 1 ≤ r) (hrs : r ≤ s) :
    trapezoidal_error f N 0 1
      = (-1) ^ (r - 1) * ∑ k ∈ range N,
          ∫ x in ((k : ℝ) / N)..(((k : ℝ) + 1) / N),
            bernoulliPanel N k r x * iteratedDeriv r f x := by
  have hNR : (N : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hN.ne'
  have hcont : ∀ m : ℕ, m ≤ s → Continuous (iteratedDeriv m f) := fun m hm =>
    hf.continuous_iteratedDeriv m (by exact_mod_cast hm)
  have hderiv : ∀ m : ℕ, m < s → ∀ x : ℝ,
      HasDerivAt (iteratedDeriv m f) (iteratedDeriv (m + 1) f x) x := by
    intro m hm x
    rw [iteratedDeriv_succ]
    exact ((hf.differentiable_iteratedDeriv m (by exact_mod_cast hm)) x).hasDerivAt
  revert hrs
  induction r, hr using Nat.le_induction with
  | base =>
    intro hrs
    -- Order one: the kernel is the displacement from the panel midpoint, and integrating by
    -- parts against `f'` produces exactly the one-panel trapezoidal error.
    have hpanel : ∀ k : ℕ,
        ∫ x in ((k : ℝ) / N)..(((k : ℝ) + 1) / N),
            bernoulliPanel N k 1 x * iteratedDeriv 1 f x
          = trapezoidal_error f 1 ((k : ℝ) / N) (((k : ℝ) + 1) / N) := by
      intro k
      rw [intervalIntegral.integral_mul_deriv_eq_deriv_mul
        (u := bernoulliPanel N k 1) (u' := bernoulliPanel N k 0) (v := f)
        (v' := iteratedDeriv 1 f) (fun x _ => hasDerivAt_bernoulliPanel hN k 0 x)
        (fun x _ => by simpa using hderiv 0 hrs x)
        ((continuous_bernoulliPanel N k 0).intervalIntegrable _ _)
        ((hcont 1 hrs).intervalIntegrable _ _)]
      have h0 : bernoulliPanel N k 0 = fun _ : ℝ => (1 : ℝ) := by
        funext x; simp [bernoulliPanel]
      rw [h0, bernoulliPanel_left hN, bernoulliPanel_right hN]
      simp only [one_mul, trapezoidal_error, trapezoidal_integral_one, bernoulliFun_one,
        Nat.factorial_one, Nat.cast_one, pow_one, one_mul]
      field_simp
      ring
    -- Summing the one-panel errors over the uniform subdivision of `[0, 1]`.
    have hsum : ∑ k ∈ range N, trapezoidal_error f 1 ((k : ℝ) / N) (((k : ℝ) + 1) / N)
        = trapezoidal_error f N 0 1 := by
      have he : (0 : ℝ) + (N : ℝ) * (1 / N) = 1 := by rw [zero_add, mul_one_div, div_self hNR]
      have hfc : Continuous f := by simpa using hcont 0 (Nat.zero_le s)
      have key := sum_trapezoidal_error_adjacent_intervals (f := f) (N := N) (a := 0)
        (h := (1 / N : ℝ)) hN (by rw [he]; exact hfc.intervalIntegrable _ _)
      rw [he] at key
      rw [← key]
      refine Finset.sum_congr rfl fun k _ => ?_
      rw [show (0 : ℝ) + (k : ℝ) * (1 / N) = (k : ℝ) / N by ring,
        show (0 : ℝ) + ((k : ℝ) + 1) * (1 / N) = ((k : ℝ) + 1) / N by ring]
    rw [← hsum]
    simp only [Nat.sub_self, pow_zero, one_mul]
    exact Finset.sum_congr rfl fun k _ => (hpanel k).symm
  | succ r hr ih =>
    intro hrs
    have hrs' : r ≤ s := le_of_lt (lt_of_lt_of_le (Nat.lt_succ_self r) hrs)
    have hrlt : r < s := lt_of_lt_of_le (Nat.lt_succ_self r) hrs
    set c : ℝ := bernoulliFun (r + 1) 0 / (((r + 1)! : ℝ) * (N : ℝ) ^ (r + 1)) with hc
    -- One further integration by parts. Since `r + 1 ≠ 1`, the kernel of order `r + 1` takes the
    -- same value `c` at both ends of every panel.
    have hpanel : ∀ k : ℕ,
        ∫ x in ((k : ℝ) / N)..(((k : ℝ) + 1) / N), bernoulliPanel N k r x * iteratedDeriv r f x
          = c * (iteratedDeriv r f (((k : ℝ) + 1) / N) - iteratedDeriv r f ((k : ℝ) / N))
            - ∫ x in ((k : ℝ) / N)..(((k : ℝ) + 1) / N),
                bernoulliPanel N k (r + 1) x * iteratedDeriv (r + 1) f x := by
      intro k
      have hibp := intervalIntegral.integral_mul_deriv_eq_deriv_mul
        (a := (k : ℝ) / N) (b := ((k : ℝ) + 1) / N)
        (u := bernoulliPanel N k (r + 1)) (u' := bernoulliPanel N k r)
        (v := iteratedDeriv r f) (v' := iteratedDeriv (r + 1) f)
        (fun x _ => hasDerivAt_bernoulliPanel hN k r x) (fun x _ => hderiv r hrlt x)
        ((continuous_bernoulliPanel N k r).intervalIntegrable _ _)
        ((hcont (r + 1) hrs).intervalIntegrable _ _)
      rw [bernoulliPanel_left hN, bernoulliPanel_right hN,
        bernoulliFun_endpoints_eq_of_ne_one (by omega : r + 1 ≠ 1)] at hibp
      rw [hc]
      linarith [hibp]
    rw [ih hrs']
    -- The boundary terms telescope to `c * (f⁽ʳ⁾ 1 - f⁽ʳ⁾ 0)`, which vanishes by hypothesis.
    have htel : ∑ k ∈ range N,
        c * (iteratedDeriv r f (((k : ℝ) + 1) / N) - iteratedDeriv r f ((k : ℝ) / N)) = 0 := by
      rw [← Finset.mul_sum]
      have hshift : ∀ k ∈ range N,
          iteratedDeriv r f (((k : ℝ) + 1) / N) - iteratedDeriv r f ((k : ℝ) / N)
            = (fun i : ℕ => iteratedDeriv r f ((i : ℝ) / N)) (k + 1)
              - (fun i : ℕ => iteratedDeriv r f ((i : ℝ) / N)) k := by
        intro k _
        push_cast
        ring_nf
      rw [Finset.sum_congr rfl hshift,
        Finset.sum_range_sub (fun i : ℕ => iteratedDeriv r f ((i : ℝ) / N)) N]
      simp only [Nat.cast_zero, zero_div, div_self hNR]
      rw [hper r hr hrlt, sub_self, mul_zero]
    have hsplit : ∑ k ∈ range N,
        ∫ x in ((k : ℝ) / N)..(((k : ℝ) + 1) / N), bernoulliPanel N k r x * iteratedDeriv r f x
        = -∑ k ∈ range N,
            ∫ x in ((k : ℝ) / N)..(((k : ℝ) + 1) / N),
              bernoulliPanel N k (r + 1) x * iteratedDeriv (r + 1) f x := by
      rw [Finset.sum_congr rfl fun k _ => hpanel k, Finset.sum_sub_distrib, htel, zero_sub]
    rw [hsplit, Nat.add_sub_cancel]
    have hpow : ((-1 : ℝ)) ^ r = -(-1 : ℝ) ^ (r - 1) := by
      conv_lhs => rw [show r = (r - 1) + 1 by omega]
      rw [pow_succ]
      ring
    rw [hpow]
    ring

/-- **Periodic Bernoulli-kernel trapezoidal identity.** Let `s ≥ 1`, let `N > 0`, and let
`f : ℝ → ℝ` be of class `C^s` with `f⁽ʳ⁾ 1 = f⁽ʳ⁾ 0` for every `1 ≤ r < s`. Then the error of the
`N`-panel trapezoidal rule on `[0, 1]`, that is `T_N(f; 0, 1) - ∫ x in 0..1, f x`, is exactly

`(-1) ^ (s - 1) * ∑ k ∈ range N, ∫ x in k / N..(k + 1) / N,`
`  (B_s (N * x - k) / (s ! * N ^ s)) * f⁽ˢ⁾ x`.

For `s = 1` the endpoint-matching hypothesis is vacuous. -/
theorem trapezoidal_error_eq_bernoulli_kernel {f : ℝ → ℝ} {s N : ℕ}
    (hs : 1 ≤ s) (hN : 0 < N) (hf : ContDiff ℝ s f)
    (hper : ∀ r : ℕ, 1 ≤ r → r < s → iteratedDeriv r f 1 = iteratedDeriv r f 0) :
    trapezoidal_error f N 0 1
      = (-1) ^ (s - 1) * ∑ k ∈ range N,
          ∫ x in (k / N : ℝ)..(((k : ℝ) + 1) / N),
            bernoulliFun s ((N : ℝ) * x - k) / (s ! * (N : ℝ) ^ s) * iteratedDeriv s f x := by
  simpa [bernoulliPanel] using
    trapezoidal_error_eq_bernoulliPanel_sum hN hf hper s hs le_rfl
