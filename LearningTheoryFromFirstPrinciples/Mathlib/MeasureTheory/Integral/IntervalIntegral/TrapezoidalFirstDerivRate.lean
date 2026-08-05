/-
Copyright (c) 2026 Vivien Cabannes. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Vivien Cabannes
-/
import Mathlib.Analysis.Asymptotics.Defs
import Mathlib.MeasureTheory.Function.Jacobian
import Mathlib.MeasureTheory.Integral.IntervalIntegral.IntegrationByParts
import Mathlib.MeasureTheory.Integral.IntervalIntegral.TrapezoidalRule

/-!
# First-derivative error rate for the trapezoidal rule

Mathlib's `trapezoidal_error_le` bounds the trapezoidal quadrature error by a second-derivative
quantity, which is `O(1 / N ^ 2)` but requires twice-differentiability. This file records the
weaker regularity regime: for a function that is merely differentiable on `Set.Icc a b` with
derivative bounded in absolute value by `L`, the trapezoidal error is at most
`L * (b - a) ^ 2 / (4 * N)`, hence `O(1 / N)`.

The proof is the classical one. On the panel `[c, d]` with midpoint `m`, integration by parts
against the kernel `x ↦ x - m` turns `∫ x in c..d, (x - m) * f' x` into the exact one-panel
trapezoidal error; bounding `|f'|` by `L` and integrating `|x - m|` exactly gives the panel bound
`L * (d - c) ^ 2 / 4`. Summing the panels with `sum_trapezoidal_error_adjacent_intervals` yields
the global bound. No integrability hypothesis is imposed on `f'`: almost-everywhere measurability
of a within-derivative on a measurable set (`MeasureTheory.aemeasurable_fderivWithin`) together
with the uniform bound already gives interval integrability.

## Graph nodes

* `abs_trapezoidal_error_le_of_deriv_bound` formalizes the tier-2 node
  `First-derivative error rate (Exercise 1.27)`, transcribing
  `informal_content/first-derivative-error-rate-exercise-1-27.md`, phrased with Mathlib's
  `trapezoidal_error`.
* `abs_trapezoidal_integral_sub_integral_le_of_deriv_bound` is the same statement with
  `trapezoidal_error` unfolded, matching the display of that informal file, for the same node.
* `abs_trapezoidal_integral_sub_integral_unitInterval_le_of_deriv_bound` is the `[0, 1]`
  specialization mentioned
  in the last paragraph of that same informal file, for the same node.
* `isBigO_trapezoidal_error_of_deriv_bound` is the `O(1 / N)` consequence asserted by the closing
  sentence of that same informal file, for the same node.

## Source

Francis Bach, *Learning Theory from First Principles*, Chapter 1, Section 1.2.5, printed page 19,
Exercise 1.27 (also Exercise 1.27 of the companion exercise collection, printed page 4).
-/

open MeasureTheory Set

open scoped Interval

/-- The derivative of a differentiable function whose within-derivative is uniformly bounded on
`Set.Icc c d` is interval integrable on `c..d`. Only almost-everywhere measurability of the
within-derivative is available, so the argument goes through
`MeasureTheory.aemeasurable_fderivWithin` and domination by the constant `L`. -/
private lemma intervalIntegrable_derivWithin_Icc {f : ℝ → ℝ} {c d L : ℝ} (hcd : c ≤ d)
    (hf : DifferentiableOn ℝ f (Icc c d))
    (hbound : ∀ x ∈ Icc c d, |derivWithin f (Icc c d) x| ≤ L) :
    IntervalIntegrable (derivWithin f (Icc c d)) volume c d := by
  have hmeas : AEMeasurable (derivWithin f (Icc c d)) (volume.restrict (Icc c d)) := by
    have h := (MeasureTheory.aemeasurable_fderivWithin (f := f) (f' := fderivWithin ℝ f (Icc c d))
      volume measurableSet_Icc
      fun x hx ↦ (hf x hx).hasFDerivWithinAt).apply_continuousLinearMap 1
    simpa [fderivWithin_derivWithin] using h
  rw [intervalIntegrable_iff_integrableOn_Ioc_of_le hcd]
  refine Integrable.mono' (g := fun _ ↦ L) (integrableOn_const (C := L) (by simp)) ?_ ?_
  · exact (hmeas.mono_measure
      (Measure.restrict_mono Ioc_subset_Icc_self le_rfl)).aestronglyMeasurable
  · filter_upwards [ae_restrict_mem measurableSet_Ioc] with x hx
    exact hbound x (Ioc_subset_Icc_self hx)

/-- The exact value `(d - c) ^ 2 / 4` of the integral of the distance to the midpoint of the
interval of integration. -/
private lemma integral_abs_sub_midpoint {c d : ℝ} (hcd : c ≤ d) :
    ∫ x in c..d, |x - (c + d) / 2| = (d - c) ^ 2 / 4 := by
  set m := (c + d) / 2 with hm
  have hm1 : c ≤ m := by rw [hm]; linarith
  have hm2 : m ≤ d := by rw [hm]; linarith
  have hint : ∀ u v : ℝ, IntervalIntegrable (fun x ↦ |x - m|) volume u v := fun u v ↦
    Continuous.intervalIntegrable (by fun_prop) _ _
  have h1 : (∫ x in c..m, |x - m|) = (m - c) ^ 2 / 2 := by
    have key : (∫ x in c..m, |x - m|) = ∫ x in c..m, (m - x) := by
      refine intervalIntegral.integral_congr fun x hx ↦ ?_
      rw [uIcc_of_le hm1] at hx
      rw [abs_of_nonpos (by linarith [hx.2])]
      ring
    rw [key, intervalIntegral.integral_sub intervalIntegrable_const
      intervalIntegral.intervalIntegrable_id, intervalIntegral.integral_const, integral_id,
      smul_eq_mul]
    ring
  have h2 : (∫ x in m..d, |x - m|) = (d - m) ^ 2 / 2 := by
    have key : (∫ x in m..d, |x - m|) = ∫ x in m..d, (x - m) := by
      refine intervalIntegral.integral_congr fun x hx ↦ ?_
      rw [uIcc_of_le hm2] at hx
      rw [abs_of_nonneg (by linarith [hx.1])]
    rw [key, intervalIntegral.integral_sub intervalIntegral.intervalIntegrable_id
      intervalIntegrable_const, intervalIntegral.integral_const, integral_id, smul_eq_mul]
    ring
  rw [← intervalIntegral.integral_add_adjacent_intervals (hint c m) (hint m d), h1, h2, hm]
  ring

/-- Integration by parts against the kernel `x ↦ x - (c + d) / 2` produces exactly the signed
one-panel trapezoidal error. -/
private lemma integral_sub_midpoint_mul_derivWithin {f : ℝ → ℝ} {c d : ℝ} (hcd : c ≤ d)
    (hf : DifferentiableOn ℝ f (Icc c d))
    (hf' : IntervalIntegrable (derivWithin f (Icc c d)) volume c d) :
    ∫ x in c..d, (x - (c + d) / 2) * derivWithin f (Icc c d) x = trapezoidal_error f 1 c d := by
  have huIcc : [[c, d]] = Icc c d := uIcc_of_le hcd
  have hu : ∀ x ∈ [[c, d]], HasDerivWithinAt (fun y ↦ y - (c + d) / 2) 1 [[c, d]] x := fun x _ ↦ by
    simpa using (hasDerivWithinAt_id x [[c, d]]).sub_const ((c + d) / 2)
  have hv : ∀ x ∈ [[c, d]], HasDerivWithinAt f (derivWithin f (Icc c d) x) [[c, d]] x := by
    intro x hx
    rw [huIcc] at hx ⊢
    exact (hf x hx).hasDerivWithinAt
  rw [intervalIntegral.integral_mul_deriv_eq_deriv_mul_of_hasDerivWithinAt (u' := fun _ ↦ (1 : ℝ))
    hu hv intervalIntegrable_const hf']
  simp only [one_mul, trapezoidal_error, trapezoidal_integral_one]
  ring

/-- The one-panel first-derivative error bound: on `[c, d]` the trapezoidal error is at most
`L * (d - c) ^ 2 / 4`. -/
private lemma abs_trapezoidal_error_one_le_of_deriv_bound {f : ℝ → ℝ} {c d L : ℝ} (hcd : c ≤ d)
    (hf : DifferentiableOn ℝ f (Icc c d))
    (hbound : ∀ x ∈ Icc c d, |derivWithin f (Icc c d) x| ≤ L) :
    |trapezoidal_error f 1 c d| ≤ L * (d - c) ^ 2 / 4 := by
  have hf' := intervalIntegrable_derivWithin_Icc hcd hf hbound
  rw [← integral_sub_midpoint_mul_derivWithin hcd hf hf', ← Real.norm_eq_abs]
  have hle : ‖∫ x in c..d, (x - (c + d) / 2) * derivWithin f (Icc c d) x‖
      ≤ ∫ x in c..d, L * |x - (c + d) / 2| := by
    refine intervalIntegral.norm_integral_le_of_norm_le hcd
      (Filter.Eventually.of_forall fun t ht ↦ ?_)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
    rw [Real.norm_eq_abs, abs_mul, mul_comm L]
    exact mul_le_mul_of_nonneg_left (hbound t (Ioc_subset_Icc_self ht)) (abs_nonneg _)
  refine hle.trans ?_
  rw [intervalIntegral.integral_const_mul, integral_abs_sub_midpoint hcd, mul_div_assoc]

/-- **First-derivative error rate for the trapezoidal rule** (Exercise 1.27), phrased with
Mathlib's `trapezoidal_error`. If `f` is differentiable on `Set.Icc a b` with `|f'| ≤ L` there,
then the `N`-panel trapezoidal error on `[a, b]` is at most `L * (b - a) ^ 2 / (4 * N)`. -/
theorem abs_trapezoidal_error_le_of_deriv_bound {f : ℝ → ℝ} {a b L : ℝ} {N : ℕ} (hab : a < b)
    (hN : 0 < N) (hf : DifferentiableOn ℝ f (Icc a b))
    (hbound : ∀ x ∈ Icc a b, |derivWithin f (Icc a b) x| ≤ L) :
    |trapezoidal_error f N a b| ≤ L * (b - a) ^ 2 / (4 * N) := by
  set h := (b - a) / N with hh
  have hNR : (0 : ℝ) < N := by exact_mod_cast hN
  have hba : (0 : ℝ) < b - a := sub_pos.mpr hab
  have hpos : 0 < h := by rw [hh]; positivity
  have hb : b = a + N * h := by rw [hh]; field_simp; ring
  have hstep : ∀ k : ℕ, a + ((k : ℝ) + 1) * h - (a + (k : ℝ) * h) = h := by
    intro k; ring
  rw [hb, ← sum_trapezoidal_error_adjacent_intervals hN
    (hb ▸ hf.continuousOn.intervalIntegrable_of_Icc hab.le)]
  have hpanel : ∀ k ∈ Finset.range N,
      |trapezoidal_error f 1 (a + (k : ℝ) * h) (a + ((k : ℝ) + 1) * h)| ≤ L * h ^ 2 / 4 := by
    intro k hk
    rw [Finset.mem_range] at hk
    have h1 : a ≤ a + (k : ℝ) * h := by
      simp only [le_add_iff_nonneg_right]; positivity
    have h2 : a + ((k : ℝ) + 1) * h ≤ b := by
      rw [hb]
      have : (k : ℝ) + 1 ≤ (N : ℝ) := by exact_mod_cast hk
      nlinarith
    have h3 : Icc (a + (k : ℝ) * h) (a + ((k : ℝ) + 1) * h) ⊆ Icc a b := Icc_subset_Icc h1 h2
    have h4 : a + (k : ℝ) * h < a + ((k : ℝ) + 1) * h := by nlinarith
    have h5 : ∀ x ∈ Icc (a + (k : ℝ) * h) (a + ((k : ℝ) + 1) * h),
        |derivWithin f (Icc (a + (k : ℝ) * h) (a + ((k : ℝ) + 1) * h)) x| ≤ L := by
      intro x hx
      rw [derivWithin_subset h3 (uniqueDiffOn_Icc h4 x hx) (hf x (h3 hx))]
      exact hbound x (h3 hx)
    refine (abs_trapezoidal_error_one_le_of_deriv_bound h4.le (hf.mono h3) h5).trans_eq ?_
    rw [hstep k]
  calc |∑ k ∈ Finset.range N, trapezoidal_error f 1 (a + (k : ℝ) * h) (a + ((k : ℝ) + 1) * h)|
      ≤ ∑ k ∈ Finset.range N, |trapezoidal_error f 1 (a + (k : ℝ) * h) (a + ((k : ℝ) + 1) * h)| :=
        Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ _k ∈ Finset.range N, L * h ^ 2 / 4 := Finset.sum_le_sum hpanel
    _ = N * (L * h ^ 2 / 4) := by rw [Finset.sum_const, Finset.card_range, nsmul_eq_mul]
    _ = L * (a + N * h - a) ^ 2 / (4 * N) := by field_simp; ring

/-- **First-derivative error rate for the trapezoidal rule** (Exercise 1.27). If `f` is
differentiable on `Set.Icc a b` and its within-derivative is bounded in absolute value by `L`
there, then the `N`-panel trapezoidal estimator differs from the integral by at most
`L * (b - a) ^ 2 / (4 * N)`. -/
theorem abs_trapezoidal_integral_sub_integral_le_of_deriv_bound {f : ℝ → ℝ} {a b L : ℝ} {N : ℕ}
    (hab : a < b) (hN : 0 < N) (hf : DifferentiableOn ℝ f (Icc a b))
    (hbound : ∀ x ∈ Icc a b, |derivWithin f (Icc a b) x| ≤ L) :
    |trapezoidal_integral f N a b - ∫ x in a..b, f x| ≤ L * (b - a) ^ 2 / (4 * N) :=
  abs_trapezoidal_error_le_of_deriv_bound hab hN hf hbound

/-- The unit-interval specialization of
`abs_trapezoidal_integral_sub_integral_le_of_deriv_bound`: on `[0, 1]` a derivative bounded by `L`
forces a trapezoidal error of at most `L / (4 * N)`. -/
theorem abs_trapezoidal_integral_sub_integral_unitInterval_le_of_deriv_bound {f : ℝ → ℝ} {L : ℝ}
    {N : ℕ}
    (hN : 0 < N) (hf : DifferentiableOn ℝ f (Icc 0 1))
    (hbound : ∀ x ∈ Icc (0 : ℝ) 1, |derivWithin f (Icc 0 1) x| ≤ L) :
    |trapezoidal_integral f N 0 1 - ∫ x in (0 : ℝ)..1, f x| ≤ L / (4 * N) := by
  simpa using abs_trapezoidal_integral_sub_integral_le_of_deriv_bound (a := 0) (b := 1)
    zero_lt_one hN hf hbound

/-- **Asymptotic form of the first-derivative trapezoidal rate.** Under the hypotheses of
`abs_trapezoidal_error_le_of_deriv_bound`, the trapezoidal error on `[a, b]` is `O(1 / N)` as the
number of panels tends to infinity. -/
theorem isBigO_trapezoidal_error_of_deriv_bound {f : ℝ → ℝ} {a b L : ℝ} (hab : a < b)
    (hf : DifferentiableOn ℝ f (Icc a b))
    (hbound : ∀ x ∈ Icc a b, |derivWithin f (Icc a b) x| ≤ L) :
    (fun N : ℕ => trapezoidal_error f N a b) =O[Filter.atTop]
      fun N : ℕ => (N : ℝ) ^ (-1 : ℤ) := by
  refine Asymptotics.IsBigO.of_bound (L * (b - a) ^ 2 / 4) ?_
  filter_upwards [Filter.eventually_gt_atTop 0] with N hN
  have h := abs_trapezoidal_error_le_of_deriv_bound hab hN hf hbound
  have hNpos : (0 : ℝ) < N := Nat.cast_pos.mpr hN
  rw [Real.norm_eq_abs, Real.norm_eq_abs, zpow_neg_one,
    abs_of_nonneg (inv_pos.mpr hNpos).le, ← div_eq_mul_inv, div_div]
  exact h
