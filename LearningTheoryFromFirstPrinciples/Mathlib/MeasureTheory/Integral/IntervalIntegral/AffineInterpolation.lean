/-
Copyright (c) 2026 Vivien Cabannes. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Vivien Cabannes
-/
import Mathlib.LinearAlgebra.AffineSpace.AffineMap
import Mathlib.MeasureTheory.Integral.IntervalIntegral.TrapezoidalRule

/-!
# Affine panel interpolation and the exact trapezoidal error

This file introduces the normalized affine interpolant `affinePanelInterp f a b` of a real function
`f` through the endpoint data `(a, f a)` and `(b, f b)`, computes its oriented interval integral,
sums those panel integrals over a uniform grid to recover Mathlib's `trapezoidal_integral`, and
deduces the exact decomposition of the trapezoidal quadrature error as a sum of panelwise
interpolation residuals. The decomposition is an identity, not an estimate: its only hypotheses are
a positive panel count `0 < N` and interval integrability of `f`, no smoothness of `f` being
required.

Everything is stated for oriented interval integrals, so no order assumption on the endpoints is
ever required, and the degenerate case `a = b` is covered by Lean's totalized division.

## Graph nodes

* `affinePanelInterp`, `affinePanelInterp_apply`, `affinePanelInterp_eq_of_ne`,
  `affinePanelInterp_left`, `affinePanelInterp_right`, `affinePanelInterp_self`,
  `affinePanelInterp_self_eq_const`, `affinePanelInterp_zero_one`:
  node `Affine panel interpolant`, transcribing `informal_content/affine-panel-interpolant.md`.
* `continuous_affinePanelInterp`, `intervalIntegrable_affinePanelInterp`,
  `integral_affinePanelInterp`, `integral_affinePanelInterp_eq_trapezoidal_integral_one`,
  `integral_affinePanelInterp_zero_one`:
  node `Affine panel integral identity`, transcribing
  `informal_content/affine-panel-integral-identity.md`.
* `trapezoidal_uniform_grid_last_point`, `sum_integral_affinePanelInterp`:
  node `Piecewise-affine integral identity`, transcribing
  `informal_content/piecewise-affine-integral-identity.md`.
* `IntervalIntegrable.uniform_grid_panel`, `integral_sub_trapezoidal_integral_eq_sum_panel_error`,
  `integral_sub_trapezoidal_integral_eq_sum_integral_residual`,
  `trapezoidal_error_eq_neg_sum_integral_residual`,
  `abs_trapezoidal_error_eq_abs_sum_integral_residual`:
  node `Exact trapezoidal error decomposition`, transcribing
  `informal_content/exact-trapezoidal-error-decomposition.md`.

## Source

Francis Bach, *Learning Theory from First Principles*, Chapter 1, Section 1.2.5 (printed pages
18-19), including Exercise 1.26.
-/

open MeasureTheory

/-- The normalized affine panel function of `f` on the panel with endpoints `a` and `b`: the value
at `x` of the affine line map from `f a` to `f b` evaluated at the normalized coordinate
`(x - a) / (b - a)`. When `a ≠ b` this is the affine interpolant of the endpoint data `(a, f a)`
and `(b, f b)`; when `a = b` Lean's totalized division makes it the constant `f a`. -/
noncomputable def affinePanelInterp (f : ℝ → ℝ) (a b x : ℝ) : ℝ :=
  AffineMap.lineMap (f a) (f b) ((x - a) / (b - a))

/-- Barycentric expansion of the affine panel interpolant. -/
theorem affinePanelInterp_apply (f : ℝ → ℝ) (a b x : ℝ) :
    affinePanelInterp f a b x = (1 - (x - a) / (b - a)) * f a + ((x - a) / (b - a)) * f b :=
  AffineMap.lineMap_apply_ring _ _ _

/-- For distinct endpoints the interpolant has the familiar two-coefficient form. -/
theorem affinePanelInterp_eq_of_ne {a b : ℝ} (hab : a ≠ b) (f : ℝ → ℝ) (x : ℝ) :
    affinePanelInterp f a b x = ((b - x) / (b - a)) * f a + ((x - a) / (b - a)) * f b := by
  have hba : b - a ≠ 0 := sub_ne_zero.mpr hab.symm
  rw [affinePanelInterp_apply]
  congr 2
  field_simp
  ring

/-- The interpolant reproduces the left endpoint value, with no assumption on the endpoints. -/
@[simp]
theorem affinePanelInterp_left (f : ℝ → ℝ) (a b : ℝ) : affinePanelInterp f a b a = f a := by
  simp [affinePanelInterp]

/-- The interpolant reproduces the right endpoint value, with no assumption on the endpoints: when
`a = b` the totalized quotient is `0`, and the line map returns `f a`, which is then `f b`. -/
@[simp]
theorem affinePanelInterp_right (f : ℝ → ℝ) (a b : ℝ) : affinePanelInterp f a b b = f b := by
  rcases eq_or_ne a b with rfl | hab
  · simp [affinePanelInterp]
  · have hba : b - a ≠ 0 := sub_ne_zero.mpr hab.symm
    rw [affinePanelInterp, div_self hba, AffineMap.lineMap_apply_one]

/-- With coincident endpoints the interpolant is constantly `f a`. -/
@[simp]
theorem affinePanelInterp_self (f : ℝ → ℝ) (a x : ℝ) : affinePanelInterp f a a x = f a := by
  simp [affinePanelInterp]

/-- With coincident endpoints the interpolant is the constant function with value `f a`. -/
theorem affinePanelInterp_self_eq_const (f : ℝ → ℝ) (a : ℝ) :
    affinePanelInterp f a a = Function.const ℝ (f a) :=
  funext fun x => affinePanelInterp_self f a x

/-- The unit-interval specialization of the affine panel interpolant. -/
theorem affinePanelInterp_zero_one (f : ℝ → ℝ) (x : ℝ) :
    affinePanelInterp f 0 1 x = (1 - x) * f 0 + x * f 1 := by
  simp [affinePanelInterp_apply]

/-- The affine panel interpolant is continuous. -/
theorem continuous_affinePanelInterp (f : ℝ → ℝ) (a b : ℝ) :
    Continuous (affinePanelInterp f a b) := by
  simp only [funext (affinePanelInterp_apply f a b)]
  fun_prop

/-- The affine panel interpolant is interval integrable on its own panel. -/
theorem intervalIntegrable_affinePanelInterp (f : ℝ → ℝ) (a b : ℝ) :
    IntervalIntegrable (affinePanelInterp f a b) volume a b :=
  (continuous_affinePanelInterp f a b).intervalIntegrable a b

/-- The oriented integral of the affine panel interpolant is the signed trapezoid area. No order
assumption on the endpoints is needed, and both sides vanish when `a = b`. -/
theorem integral_affinePanelInterp (f : ℝ → ℝ) (a b : ℝ) :
    (∫ x in a..b, affinePanelInterp f a b x) = (b - a) * (f a + f b) / 2 := by
  rcases eq_or_ne a b with rfl | hab
  · simp
  · have hba : b - a ≠ 0 := sub_ne_zero.mpr hab.symm
    have key : ∀ x : ℝ, affinePanelInterp f a b x
        = ((f b - f a) / (b - a)) * x + (f a - a * ((f b - f a) / (b - a))) := by
      intro x
      rw [affinePanelInterp_apply]
      field_simp
      ring
    have h1 : IntervalIntegrable (fun x : ℝ => ((f b - f a) / (b - a)) * x) volume a b :=
      (by fun_prop : Continuous fun x : ℝ => ((f b - f a) / (b - a)) * x).intervalIntegrable a b
    have h2 : IntervalIntegrable (fun _ : ℝ => f a - a * ((f b - f a) / (b - a))) volume a b :=
      intervalIntegrable_const
    simp only [funext key]
    rw [intervalIntegral.integral_add h1 h2, intervalIntegral.integral_const_mul, integral_id,
      intervalIntegral.integral_const, smul_eq_mul]
    field_simp
    ring

/-- The integral of the affine panel interpolant is the one-panel trapezoidal approximation. -/
theorem integral_affinePanelInterp_eq_trapezoidal_integral_one (f : ℝ → ℝ) (a b : ℝ) :
    (∫ x in a..b, affinePanelInterp f a b x) = trapezoidal_integral f 1 a b := by
  rw [integral_affinePanelInterp, trapezoidal_integral_one]
  ring

/-- The unit-interval specialization of the affine panel integral identity. -/
theorem integral_affinePanelInterp_zero_one (f : ℝ → ℝ) :
    (∫ x in (0 : ℝ)..1, ((1 - x) * f 0 + x * f 1)) = (f 0 + f 1) / 2 := by
  have key : (∫ x in (0 : ℝ)..1, ((1 - x) * f 0 + x * f 1))
      = ∫ x in (0 : ℝ)..1, affinePanelInterp f 0 1 x := by
    simp only [funext (affinePanelInterp_zero_one f)]
  rw [key, integral_affinePanelInterp]
  ring

/-- On the uniform grid of `N` panels of signed width `h = (b - a) / N`, the last grid point is
`b`. Positivity of `N` is what makes the grid actually reach the right endpoint. -/
theorem trapezoidal_uniform_grid_last_point {N : ℕ} (hN : 0 < N) {a b h : ℝ}
    (hh : h = (b - a) / N) :
    a + (N : ℝ) * h = b := by
  have hN' : (N : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hN.ne'
  rw [hh]
  field_simp
  ring

/-- The sum of the affine panel integrals over the uniform grid of `N` panels is the trapezoidal
estimator `T_N(f; a, b)`. -/
theorem sum_integral_affinePanelInterp (f : ℝ → ℝ) {N : ℕ} (hN : 0 < N) {a b h : ℝ}
    (hh : h = (b - a) / N) :
    ∑ i ∈ Finset.range N,
        (∫ x in (a + i * h)..(a + (i + 1) * h), affinePanelInterp f (a + i * h) (a + (i + 1) * h) x)
      = trapezoidal_integral f N a b := by
  have hb : a + (N : ℝ) * h = b := trapezoidal_uniform_grid_last_point hN hh
  calc ∑ i ∈ Finset.range N,
        (∫ x in (a + i * h)..(a + (i + 1) * h), affinePanelInterp f (a + i * h) (a + (i + 1) * h) x)
      = ∑ i ∈ Finset.range N, trapezoidal_integral f 1 (a + i * h) (a + (i + 1) * h) :=
        Finset.sum_congr rfl fun i _ =>
          integral_affinePanelInterp_eq_trapezoidal_integral_one f _ _
    _ = trapezoidal_integral f N a (a + (N : ℝ) * h) :=
        sum_trapezoidal_integral_adjacent_intervals hN
    _ = trapezoidal_integral f N a b := by rw [hb]

/-- Interval integrability across the whole uniform grid restricts to every panel: if `f` is
interval integrable on the oriented interval from `a` to `a + N * h`, then for every `k < N` it is
interval integrable on the `k`-th panel, from `a + k * h` to `a + (k + 1) * h`. -/
theorem IntervalIntegrable.uniform_grid_panel {f : ℝ → ℝ} {N : ℕ} {a h : ℝ}
    (hf : IntervalIntegrable f volume a (a + (N : ℝ) * h)) {k : ℕ} (hk : k < N) :
    IntervalIntegrable f volume (a + k * h) (a + (k + 1) * h) := by
  have mem : ∀ {m : ℕ}, m ≤ N → a + (m : ℝ) * h ∈ Set.uIcc a (a + (N : ℝ) * h) := by
    rcases le_total h 0 with h_neg | h_pos <;> intro m hm <;> rw [← Nat.cast_le (α := ℝ)] at hm
    · simpa [Set.mem_uIcc] using .inr
        ⟨mul_le_mul_of_nonpos_right hm h_neg, mul_nonpos_of_nonneg_of_nonpos m.cast_nonneg h_neg⟩
    · exact Set.mem_uIcc_of_le (le_add_of_nonneg_right (by positivity)) (by grw [hm])
  have hright : a + ((k : ℝ) + 1) * h ∈ Set.uIcc a (a + (N : ℝ) * h) := by
    have := mem (Nat.succ_le_of_lt hk)
    push_cast at this
    exact this
  exact hf.mono (Set.uIcc_subset_uIcc (mem hk.le) hright) le_rfl

/-- Exact decomposition of the oriented quadrature error into panel errors: the integral minus the
trapezoidal estimator is the sum over panels of the panel integral minus the panel trapezoid. -/
theorem integral_sub_trapezoidal_integral_eq_sum_panel_error (f : ℝ → ℝ) {N : ℕ} (hN : 0 < N)
    {a b h : ℝ} (hh : h = (b - a) / N) (hf : IntervalIntegrable f volume a b) :
    (∫ x in a..b, f x) - trapezoidal_integral f N a b
      = ∑ i ∈ Finset.range N, ((∫ x in (a + i * h)..(a + (i + 1) * h), f x)
          - h * (f (a + i * h) + f (a + (i + 1) * h)) / 2) := by
  have hb : a + (N : ℝ) * h = b := trapezoidal_uniform_grid_last_point hN hh
  have key := sum_trapezoidal_error_adjacent_intervals (f := f) (N := N) (a := a) (h := h) hN
    (by rwa [hb])
  rw [hb] at key
  have hneg : (∫ x in a..b, f x) - trapezoidal_integral f N a b
      = -trapezoidal_error f N a b := by
    rw [trapezoidal_error]
    ring
  rw [hneg, ← key, ← Finset.sum_neg_distrib]
  refine Finset.sum_congr rfl fun i _ => ?_
  rw [trapezoidal_error, trapezoidal_integral_one]
  ring

/-- Exact decomposition of the oriented quadrature error into interpolation residuals: the integral
minus the trapezoidal estimator is the sum over panels of the integral of `f` minus its affine
panel interpolant. -/
theorem integral_sub_trapezoidal_integral_eq_sum_integral_residual (f : ℝ → ℝ) {N : ℕ} (hN : 0 < N)
    {a b h : ℝ} (hh : h = (b - a) / N) (hf : IntervalIntegrable f volume a b) :
    (∫ x in a..b, f x) - trapezoidal_integral f N a b
      = ∑ i ∈ Finset.range N, ∫ x in (a + i * h)..(a + (i + 1) * h),
          (f x - affinePanelInterp f (a + i * h) (a + (i + 1) * h) x) := by
  have hb : a + (N : ℝ) * h = b := trapezoidal_uniform_grid_last_point hN hh
  rw [integral_sub_trapezoidal_integral_eq_sum_panel_error f hN hh hf]
  refine Finset.sum_congr rfl fun i hi => ?_
  have hpanel : IntervalIntegrable f volume (a + i * h) (a + (i + 1) * h) :=
    IntervalIntegrable.uniform_grid_panel (by rwa [hb]) (Finset.mem_range.mp hi)
  rw [intervalIntegral.integral_sub hpanel (intervalIntegrable_affinePanelInterp _ _ _),
    integral_affinePanelInterp]
  ring

/-- Mathlib's signed `trapezoidal_error` is the negative of the residual decomposition, since it
subtracts the integral from the estimator rather than the other way round. -/
theorem trapezoidal_error_eq_neg_sum_integral_residual (f : ℝ → ℝ) {N : ℕ} (hN : 0 < N)
    {a b h : ℝ} (hh : h = (b - a) / N) (hf : IntervalIntegrable f volume a b) :
    trapezoidal_error f N a b
      = -∑ i ∈ Finset.range N, ∫ x in (a + i * h)..(a + (i + 1) * h),
          (f x - affinePanelInterp f (a + i * h) (a + (i + 1) * h) x) := by
  rw [← integral_sub_trapezoidal_integral_eq_sum_integral_residual f hN hh hf, trapezoidal_error]
  ring

/-- The absolute quadrature errors of the two sign conventions agree. -/
theorem abs_trapezoidal_error_eq_abs_sum_integral_residual (f : ℝ → ℝ) {N : ℕ} (hN : 0 < N)
    {a b h : ℝ} (hh : h = (b - a) / N) (hf : IntervalIntegrable f volume a b) :
    |trapezoidal_error f N a b|
      = |∑ i ∈ Finset.range N, ∫ x in (a + i * h)..(a + (i + 1) * h),
          (f x - affinePanelInterp f (a + i * h) (a + (i + 1) * h) x)| := by
  rw [trapezoidal_error_eq_neg_sum_integral_residual f hN hh hf, abs_neg]
