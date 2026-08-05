/-
Copyright (c) 2026 Vivien Cabannes. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Vivien Cabannes
-/
import LearningTheoryFromFirstPrinciples.Mathlib.MeasureTheory.Integral.IntervalIntegral.TrapezoidalBernoulliKernel
import Mathlib.Algebra.Ring.Periodic
import Mathlib.Analysis.Asymptotics.Defs
import Mathlib.Analysis.Calculus.IteratedDeriv.Lemmas

/-!
# Spectral accuracy of the trapezoidal rule for periodic smooth functions

The `N`-panel trapezoidal rule on `[0, 1]` converges at the rate `N⁻ˢ` for every one-periodic
function of class `C^s`, with a constant that only involves `s` and a bound on the `s`-th
derivative. This is the phenomenon that makes the trapezoidal rule the method of choice for
periodic integrands: unlike the generic `C²` estimate, the rate improves with the smoothness of
the integrand.

The proof rests on the exact Bernoulli-kernel representation of the trapezoidal error, that is on
`trapezoidal_error_eq_bernoulli_kernel` from the `TrapezoidalBernoulliKernel` file of this folder.
Periodicity of `f` propagates to every iterated derivative, so the endpoint-matching hypothesis of
that identity holds at every order; taking absolute values through the finite sum and each panel
integral, bounding `f⁽ˢ⁾` by `M`, and rescaling each panel by `u = N * x - k` turns the estimate
into `N` copies of `∫ u in 0..1, |B_s u|`, each weighted by `1 / N`.

## Graph nodes

* `trapezoidalPeriodicConst`, `trapezoidalPeriodicConst_one`,
  `abs_trapezoidal_error_le_of_periodic` and `isBigO_trapezoidal_error_of_periodic` together
  formalize the tier-2 node `Periodic smooth-function error rate (Exercise 1.28)`, transcribing
  `informal_content/periodic-smooth-function-error-rate-exercise-1-28.md`: the definition of the
  constant `C_s`, its value `C_1 = 1 / 4`, the explicit bound `C_s * M / N ^ s`, and the `atTop`
  Big-O consequence.

## Source

Francis Bach, *Learning Theory from First Principles*, Chapter 1, Section 1.2.5, printed page 19,
Exercise 1.28 (see also *Learning Theory from First Principles - Exercises*, Chapter 1,
Exercise 1.28, printed page 4).
-/

open Finset MeasureTheory intervalIntegral

open scoped Nat

/-- The constant `C_s = (s !)⁻¹ * ∫ u in 0..1, |B_s u|` governing the trapezoidal error of a
one-periodic `C^s` function. It depends only on the order `s`, and `C_1 = 1 / 4`. -/
noncomputable def trapezoidalPeriodicConst (s : ℕ) : ℝ :=
  ((s ! : ℝ))⁻¹ * ∫ u in (0 : ℝ)..1, |bernoulliFun s u|

/-- **The first-order constant is `1 / 4`.** Since `B₁ u = u - 1 / 2`, the integral defining
`trapezoidalPeriodicConst 1` is the integral of the distance to the midpoint of `[0, 1]`, so
`C_1 = 1 / 4`; this recovers the first-derivative estimate on the unit interval. -/
theorem trapezoidalPeriodicConst_one : trapezoidalPeriodicConst 1 = 1 / 4 := by
  have hint : ∀ u v : ℝ, IntervalIntegrable (fun x : ℝ => |x - 1 / 2|) volume u v := fun u v =>
    Continuous.intervalIntegrable (by fun_prop) _ _
  -- Below the midpoint the integrand is `1 / 2 - x`, above it is `x - 1 / 2`.
  have hlow : ∫ x in (0 : ℝ)..(1 / 2 : ℝ), |x - 1 / 2| = 1 / 8 := by
    have key : ∫ x in (0 : ℝ)..(1 / 2 : ℝ), |x - 1 / 2|
        = ∫ x in (0 : ℝ)..(1 / 2 : ℝ), (1 / 2 - x) := by
      refine intervalIntegral.integral_congr fun x hx => ?_
      rw [Set.uIcc_of_le (by norm_num : (0 : ℝ) ≤ 1 / 2)] at hx
      rw [abs_of_nonpos (by linarith [hx.2])]
      ring
    rw [key, intervalIntegral.integral_sub intervalIntegrable_const
      intervalIntegral.intervalIntegrable_id, intervalIntegral.integral_const, integral_id,
      smul_eq_mul]
    norm_num
  have hhigh : ∫ x in (1 / 2 : ℝ)..(1 : ℝ), |x - 1 / 2| = 1 / 8 := by
    have key : ∫ x in (1 / 2 : ℝ)..(1 : ℝ), |x - 1 / 2|
        = ∫ x in (1 / 2 : ℝ)..(1 : ℝ), (x - 1 / 2) := by
      refine intervalIntegral.integral_congr fun x hx => ?_
      rw [Set.uIcc_of_le (by norm_num : (1 / 2 : ℝ) ≤ 1)] at hx
      rw [abs_of_nonneg (by linarith [hx.1])]
    rw [key, intervalIntegral.integral_sub intervalIntegral.intervalIntegrable_id
      intervalIntegrable_const, intervalIntegral.integral_const, integral_id, smul_eq_mul]
    norm_num
  rw [trapezoidalPeriodicConst]
  simp only [bernoulliFun_one, Nat.factorial_one, Nat.cast_one, inv_one, one_mul]
  rw [← intervalIntegral.integral_add_adjacent_intervals (hint 0 (1 / 2)) (hint (1 / 2) 1),
    hlow, hhigh]
  norm_num

/-- Every iterated derivative of a periodic function is periodic with the same period: apply
`iteratedDeriv r` to the identity `(fun x ↦ f (x + c)) = f` and use that iterated derivatives
commute with translations. -/
private lemma periodic_iteratedDeriv {f : ℝ → ℝ} {c : ℝ} (hf : Function.Periodic f c) (r : ℕ) :
    Function.Periodic (iteratedDeriv r f) c := by
  intro x
  have h := congrFun (iteratedDeriv_comp_add_const r f c) x
  rw [hf.funext] at h
  exact h.symm

/-- **Trapezoidal error rate for periodic smooth functions.** Let `s ≥ 1`, let `f : ℝ → ℝ` be of
class `C^s` and one-periodic, and let `M ≥ 0` bound `|f⁽ˢ⁾|` on `[0, 1]`. Then for every `N > 0`
the `N`-panel trapezoidal rule on `[0, 1]` satisfies

`|T_N(f; 0, 1) - ∫ x in 0..1, f x| ≤ C_s * M / N ^ s`,

with `C_s = trapezoidalPeriodicConst s`. -/
theorem abs_trapezoidal_error_le_of_periodic {f : ℝ → ℝ} {s N : ℕ} {M : ℝ}
    (hs : 1 ≤ s) (hf : ContDiff ℝ s f) (hfper : Function.Periodic f 1) (_hM : 0 ≤ M)
    (hbound : ∀ x ∈ Set.Icc (0 : ℝ) 1, |iteratedDeriv s f x| ≤ M) (hN : 0 < N) :
    |trapezoidal_integral f N 0 1 - ∫ x in (0 : ℝ)..1, f x|
      ≤ trapezoidalPeriodicConst s * M / (N : ℝ) ^ s := by
  -- `0 ≤ M` is part of the source statement but forced by `hbound` at `x = 0`, hence unused here.
  have hNpos : (0 : ℝ) < N := Nat.cast_pos.mpr hN
  have hNne : (N : ℝ) ≠ 0 := ne_of_gt hNpos
  have hden : (0 : ℝ) < (s ! : ℝ) * (N : ℝ) ^ s := by positivity
  have hcont : Continuous (iteratedDeriv s f) := hf.continuous_iteratedDeriv' s
  -- Periodicity of `f` transfers to every order, so all endpoint values agree.
  have hend : ∀ r : ℕ, 1 ≤ r → r < s → iteratedDeriv r f 1 = iteratedDeriv r f 0 := by
    intro r _ _
    simpa using periodic_iteratedDeriv hfper r 0
  -- The substitution `u = N * x - k` on the `k`-th panel.
  have hsubst : ∀ k : ℕ,
      ∫ x in ((k : ℝ) / N)..(((k : ℝ) + 1) / N), |bernoulliFun s ((N : ℝ) * x - k)|
        = (N : ℝ)⁻¹ * ∫ u in (0 : ℝ)..1, |bernoulliFun s u| := by
    intro k
    have h := intervalIntegral.integral_comp_mul_sub (a := (k : ℝ) / N) (b := ((k : ℝ) + 1) / N)
      (fun u : ℝ => |bernoulliFun s u|) hNne (k : ℝ)
    simp only [smul_eq_mul] at h
    rw [show (N : ℝ) * ((k : ℝ) / N) - k = 0 by field_simp; ring,
      show (N : ℝ) * (((k : ℝ) + 1) / N) - k = 1 by field_simp; ring] at h
    exact h
  -- Panelwise bound: absolute values through the integral, then `|f⁽ˢ⁾| ≤ M` and the rescaling.
  have hpanel : ∀ k ∈ range N,
      |∫ x in ((k : ℝ) / N)..(((k : ℝ) + 1) / N),
          bernoulliFun s ((N : ℝ) * x - k) / ((s ! : ℝ) * (N : ℝ) ^ s) * iteratedDeriv s f x|
        ≤ M / ((s ! : ℝ) * (N : ℝ) ^ s) * ((N : ℝ)⁻¹ * ∫ u in (0 : ℝ)..1, |bernoulliFun s u|) := by
    intro k hk
    have hkN : (k : ℝ) + 1 ≤ (N : ℝ) := by exact_mod_cast Nat.succ_le_of_lt (mem_range.mp hk)
    have hab : (k : ℝ) / N ≤ ((k : ℝ) + 1) / N := by
      have h : ((k : ℝ) + 1) / N - (k : ℝ) / N = 1 / N := by
        field_simp
        ring
      have hpos := one_div_pos.mpr hNpos
      linarith
    have hsub : Set.Icc ((k : ℝ) / N) (((k : ℝ) + 1) / N) ⊆ Set.Icc (0 : ℝ) 1 := by
      intro x hx
      refine ⟨le_trans (by positivity) hx.1, le_trans hx.2 ?_⟩
      rw [div_le_one hNpos]
      exact hkN
    have hcB : Continuous fun x : ℝ => |bernoulliFun s ((N : ℝ) * x - k)| := by fun_prop
    have hcG : Continuous fun x : ℝ =>
        |bernoulliFun s ((N : ℝ) * x - k) / ((s ! : ℝ) * (N : ℝ) ^ s) * iteratedDeriv s f x| := by
      fun_prop
    calc |∫ x in ((k : ℝ) / N)..(((k : ℝ) + 1) / N),
            bernoulliFun s ((N : ℝ) * x - k) / ((s ! : ℝ) * (N : ℝ) ^ s) * iteratedDeriv s f x|
        ≤ ∫ x in ((k : ℝ) / N)..(((k : ℝ) + 1) / N),
            |bernoulliFun s ((N : ℝ) * x - k) / ((s ! : ℝ) * (N : ℝ) ^ s)
              * iteratedDeriv s f x| := intervalIntegral.abs_integral_le_integral_abs hab
      _ ≤ ∫ x in ((k : ℝ) / N)..(((k : ℝ) + 1) / N),
            M / ((s ! : ℝ) * (N : ℝ) ^ s) * |bernoulliFun s ((N : ℝ) * x - k)| := by
          refine intervalIntegral.integral_mono_on hab (hcG.intervalIntegrable _ _)
            ((continuous_const.mul hcB).intervalIntegrable _ _) fun x hx => ?_
          have hD : |iteratedDeriv s f x| ≤ M := hbound x (hsub hx)
          have hBnn : (0 : ℝ) ≤ |bernoulliFun s ((N : ℝ) * x - k)| := abs_nonneg _
          have hkey : |bernoulliFun s ((N : ℝ) * x - k)| * |iteratedDeriv s f x|
              ≤ |bernoulliFun s ((N : ℝ) * x - k)| * M := mul_le_mul_of_nonneg_left hD hBnn
          have hdinv : (0 : ℝ) ≤ ((s ! : ℝ) * (N : ℝ) ^ s)⁻¹ := le_of_lt (inv_pos.mpr hden)
          rw [abs_mul, abs_div, abs_of_pos hden]
          calc |bernoulliFun s ((N : ℝ) * x - k)| / ((s ! : ℝ) * (N : ℝ) ^ s)
                * |iteratedDeriv s f x|
              = ((s ! : ℝ) * (N : ℝ) ^ s)⁻¹
                  * (|bernoulliFun s ((N : ℝ) * x - k)| * |iteratedDeriv s f x|) := by
                field_simp
            _ ≤ ((s ! : ℝ) * (N : ℝ) ^ s)⁻¹
                  * (|bernoulliFun s ((N : ℝ) * x - k)| * M) :=
                mul_le_mul_of_nonneg_left hkey hdinv
            _ = M / ((s ! : ℝ) * (N : ℝ) ^ s) * |bernoulliFun s ((N : ℝ) * x - k)| := by
                field_simp
      _ = M / ((s ! : ℝ) * (N : ℝ) ^ s)
            * ∫ x in ((k : ℝ) / N)..(((k : ℝ) + 1) / N), |bernoulliFun s ((N : ℝ) * x - k)| :=
          intervalIntegral.integral_const_mul _ _
      _ = M / ((s ! : ℝ) * (N : ℝ) ^ s)
            * ((N : ℝ)⁻¹ * ∫ u in (0 : ℝ)..1, |bernoulliFun s u|) := by rw [hsubst k]
  -- Assemble: the Bernoulli-kernel identity, the triangle inequality, and the `N` panels.
  have hrw : trapezoidal_integral f N 0 1 - ∫ x in (0 : ℝ)..1, f x
      = trapezoidal_error f N 0 1 := rfl
  rw [hrw, trapezoidal_error_eq_bernoulli_kernel hs hN hf hend, abs_mul,
    show |(-1 : ℝ) ^ (s - 1)| = 1 by simp, one_mul]
  calc |∑ k ∈ range N, ∫ x in ((k : ℝ) / N)..(((k : ℝ) + 1) / N),
          bernoulliFun s ((N : ℝ) * x - k) / ((s ! : ℝ) * (N : ℝ) ^ s) * iteratedDeriv s f x|
      ≤ ∑ k ∈ range N, |∫ x in ((k : ℝ) / N)..(((k : ℝ) + 1) / N),
          bernoulliFun s ((N : ℝ) * x - k) / ((s ! : ℝ) * (N : ℝ) ^ s)
            * iteratedDeriv s f x| := Finset.abs_sum_le_sum_abs _ _
    _ ≤ ∑ _k ∈ range N, M / ((s ! : ℝ) * (N : ℝ) ^ s)
          * ((N : ℝ)⁻¹ * ∫ u in (0 : ℝ)..1, |bernoulliFun s u|) := Finset.sum_le_sum hpanel
    _ = trapezoidalPeriodicConst s * M / (N : ℝ) ^ s := by
        rw [Finset.sum_const, card_range, nsmul_eq_mul, trapezoidalPeriodicConst]
        have hfac : ((s ! : ℝ)) ≠ 0 := by positivity
        field_simp

/-- **Asymptotic form of the periodic trapezoidal rate.** Under the hypotheses of
`abs_trapezoidal_error_le_of_periodic`, the trapezoidal error on `[0, 1]` is `O(N⁻ˢ)` as the
number of panels tends to infinity. -/
theorem isBigO_trapezoidal_error_of_periodic {f : ℝ → ℝ} {s : ℕ} {M : ℝ}
    (hs : 1 ≤ s) (hf : ContDiff ℝ s f) (hfper : Function.Periodic f 1) (hM : 0 ≤ M)
    (hbound : ∀ x ∈ Set.Icc (0 : ℝ) 1, |iteratedDeriv s f x| ≤ M) :
    (fun N : ℕ => trapezoidal_error f N 0 1) =O[Filter.atTop]
      fun N : ℕ => ((N : ℝ) ^ s)⁻¹ := by
  refine Asymptotics.IsBigO.of_bound (trapezoidalPeriodicConst s * M) ?_
  filter_upwards [Filter.eventually_gt_atTop 0] with N hN
  have h := abs_trapezoidal_error_le_of_periodic hs hf hfper hM hbound hN
  have hnn : (0 : ℝ) ≤ ((N : ℝ) ^ s)⁻¹ := by positivity
  rw [Real.norm_eq_abs, Real.norm_eq_abs, abs_of_nonneg hnn, ← div_eq_mul_inv]
  exact h
