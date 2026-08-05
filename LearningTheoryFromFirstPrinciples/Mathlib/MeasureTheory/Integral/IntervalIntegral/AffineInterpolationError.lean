/-
Copyright (c) 2026 Vivien Cabannes. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Vivien Cabannes
-/
import LearningTheoryFromFirstPrinciples.Mathlib.MeasureTheory.Integral.IntervalIntegral.AffineInterpolation
import Mathlib.Analysis.Calculus.IteratedDeriv.Defs
import Mathlib.Analysis.Calculus.LocalExtr.Rolle

/-!
# Local error of affine interpolation

For a function `f` that is twice differentiable on a closed interval `Set.Icc a b`, the difference
between `f` and its affine panel interpolant `affinePanelInterp f a b` is controlled pointwise by a
uniform bound on the second derivative:

`|f x - affinePanelInterp f a b x| ≤ L / 2 * (x - a) * (b - x)`.

The proof is the classical double application of Rolle's theorem. Fixing an interior point `x`, one
subtracts from the interpolation residual the unique multiple of `(t - a) * (t - b)` that also
vanishes at `x`; the resulting function has three roots, so its derivative has two, so its second
derivative has one, and the affine interpolant contributes nothing to that second derivative.

Only twice differentiability on the closed interval is assumed, exactly as in the source: no `C^2`
or continuity-of-the-second-derivative hypothesis is used.

## Graph nodes

* `abs_sub_affinePanelInterp_le`: node `Affine interpolation local error (Exercise 1.26)`,
  transcribing the statement of `informal_content/affine-interpolation-local-error-exercise-1-26.md`
  verbatim.
* `abs_sub_affinePanelInterp_le_unitInterval`: same node, the `[0, 1]` specialization recorded in
  the closing line of that file.
* `hasDerivAt_affinePanelInterp`, `exists_second_derivative_eq_zero` (private),
  `exists_sub_affinePanelInterp_eq`: same node, auxiliary steps of the proof written out in that
  file; `exists_sub_affinePanelInterp_eq` is the signed Cauchy remainder identity
  `e x = f'' ξ / 2 * (x - a) * (x - b)` from which the bound is read off.

## Source

Francis Bach, *Learning Theory from First Principles*, Chapter 1, Section 1.2.5 (printed page 19),
Exercise 1.26.
-/

/-- The affine panel interpolant of `f` through the nodes `a` and `b` is an affine function of its
argument, hence differentiable everywhere with the constant slope `(f b - f a) / (b - a)`. No
assumption on the nodes is needed: when `a = b` the interpolant is the constant `f a` and the
totalized slope is `0`. -/
theorem hasDerivAt_affinePanelInterp {a b : ℝ} (f : ℝ → ℝ) (t : ℝ) :
    HasDerivAt (affinePanelInterp f a b) ((f b - f a) / (b - a)) t := by
  have key : affinePanelInterp f a b
      = fun u : ℝ => ((f b - f a) / (b - a)) * u + (f a - a * ((f b - f a) / (b - a))) := by
    funext u
    rw [affinePanelInterp_apply]
    ring
  rw [key]
  exact (((hasDerivAt_id t).const_mul ((f b - f a) / (b - a))).add_const
    (f a - a * ((f b - f a) / (b - a)))).congr_deriv (by ring)

/-- Double Rolle: a function with three roots `a < x < b`, continuously differentiable enough that
`g'` is a derivative of `g` and `g''` a derivative of `g'` on `Set.Ioo a b`, has a point of
`Set.Ioo a b` at which `g''` vanishes. -/
private theorem exists_second_derivative_eq_zero (g g' g'' : ℝ → ℝ) {a x b : ℝ} (hax : a < x)
    (hxb : x < b) (hgc : ContinuousOn g (Set.Icc a b)) (hg'c : ContinuousOn g' (Set.Icc a b))
    (hgd : ∀ t ∈ Set.Ioo a b, HasDerivAt g (g' t) t)
    (hg'd : ∀ t ∈ Set.Ioo a b, HasDerivAt g' (g'' t) t)
    (ha : g a = 0) (hx : g x = 0) (hb : g b = 0) :
    ∃ ξ ∈ Set.Ioo a b, g'' ξ = 0 := by
  obtain ⟨u, hu, hu0⟩ := exists_hasDerivAt_eq_zero hax
    (hgc.mono (Set.Icc_subset_Icc le_rfl hxb.le)) (ha.trans hx.symm)
    fun t ht => hgd t ⟨ht.1, ht.2.trans hxb⟩
  obtain ⟨v, hv, hv0⟩ := exists_hasDerivAt_eq_zero hxb
    (hgc.mono (Set.Icc_subset_Icc hax.le le_rfl)) (hx.trans hb.symm)
    fun t ht => hgd t ⟨hax.trans ht.1, ht.2⟩
  have hIoo : Set.Ioo u v ⊆ Set.Ioo a b := Set.Ioo_subset_Ioo hu.1.le hv.2.le
  obtain ⟨ξ, hξ, hξ0⟩ := exists_hasDerivAt_eq_zero (hu.2.trans hv.1)
    (hg'c.mono (Set.Icc_subset_Icc hu.1.le hv.2.le)) (hu0.trans hv0.symm)
    fun t ht => hg'd t (hIoo ht)
  exact ⟨ξ, hIoo hξ, hξ0⟩

/-- **Cauchy's remainder formula for affine interpolation.** If `f` is twice differentiable on
`Set.Icc a b` and `x` is interior to that interval, then the interpolation residual is exactly
`f'' ξ / 2 * (x - a) * (x - b)` for some interior point `ξ`. The endpoint order hypothesis is kept
for symmetry with the main statement, although `x ∈ Set.Ioo a b` already forces `a < b`. -/
theorem exists_sub_affinePanelInterp_eq {f : ℝ → ℝ} {a b : ℝ} (_hab : a < b)
    (hf : DifferentiableOn ℝ f (Set.Icc a b))
    (hf' : DifferentiableOn ℝ (derivWithin f (Set.Icc a b)) (Set.Icc a b))
    {x : ℝ} (hx : x ∈ Set.Ioo a b) :
    ∃ ξ ∈ Set.Ioo a b, f x - affinePanelInterp f a b x
      = iteratedDerivWithin 2 f (Set.Icc a b) ξ / 2 * ((x - a) * (x - b)) := by
  obtain ⟨hax, hxb⟩ := hx
  -- The second iterated within derivative is the within derivative of the first one.
  have hiter : iteratedDerivWithin 2 f (Set.Icc a b)
      = derivWithin (derivWithin f (Set.Icc a b)) (Set.Icc a b) := by
    rw [show (2 : ℕ) = 1 + 1 from rfl, iteratedDerivWithin_succ, iteratedDerivWithin_one]
  -- At an interior point the closed interval is a neighbourhood, so within derivatives are
  -- genuine derivatives.
  have hsub : Set.Ioo a b ⊆ Set.Icc a b := Set.Ioo_subset_Icc_self
  have hnhds : ∀ t ∈ Set.Ioo a b, Set.Icc a b ∈ nhds t := fun t ht => Icc_mem_nhds ht.1 ht.2
  have hfd : ∀ t ∈ Set.Ioo a b, HasDerivAt f (derivWithin f (Set.Icc a b) t) t := fun t ht =>
    (hf t (hsub ht)).hasDerivWithinAt.hasDerivAt (hnhds t ht)
  have hf'd : ∀ t ∈ Set.Ioo a b,
      HasDerivAt (derivWithin f (Set.Icc a b)) (iteratedDerivWithin 2 f (Set.Icc a b) t) t := by
    intro t ht
    rw [hiter]
    exact (hf' t (hsub ht)).hasDerivWithinAt.hasDerivAt (hnhds t ht)
  have hA : ∀ t : ℝ, HasDerivAt (affinePanelInterp f a b) ((f b - f a) / (b - a)) t :=
    hasDerivAt_affinePanelInterp f
  -- The unique constant `c` making the corrected function vanish at `x` as well.
  have hxa0 : x - a ≠ 0 := sub_ne_zero.mpr hax.ne'
  have hxb0 : x - b ≠ 0 := sub_ne_zero.mpr hxb.ne
  obtain ⟨c, hcx⟩ : ∃ c : ℝ, f x - affinePanelInterp f a b x = c * ((x - a) * (x - b)) :=
    ⟨(f x - affinePanelInterp f a b x) / ((x - a) * (x - b)), by field_simp⟩
  -- The corrected function and its two derivatives.
  have hgc : ContinuousOn (fun t => f t - affinePanelInterp f a b t - c * ((t - a) * (t - b)))
      (Set.Icc a b) :=
    (hf.continuousOn.sub (continuous_affinePanelInterp f a b).continuousOn).sub (by fun_prop)
  have hg'c : ContinuousOn (fun t => derivWithin f (Set.Icc a b) t - (f b - f a) / (b - a)
      - c * (2 * t - a - b)) (Set.Icc a b) :=
    (hf'.continuousOn.sub continuousOn_const).sub (by fun_prop)
  have hgd : ∀ t ∈ Set.Ioo a b,
      HasDerivAt (fun u => f u - affinePanelInterp f a b u - c * ((u - a) * (u - b)))
        (derivWithin f (Set.Icc a b) t - (f b - f a) / (b - a) - c * (2 * t - a - b)) t := by
    intro t ht
    refine ((hfd t ht).sub (hA t)).sub ?_
    have h : HasDerivAt (fun u : ℝ => (u - a) * (u - b)) (1 * (t - b) + (t - a) * 1) t :=
      ((hasDerivAt_id t).sub_const a).mul ((hasDerivAt_id t).sub_const b)
    exact (h.const_mul c).congr_deriv (by ring)
  have hg'd : ∀ t ∈ Set.Ioo a b,
      HasDerivAt (fun u => derivWithin f (Set.Icc a b) u - (f b - f a) / (b - a)
        - c * (2 * u - a - b)) (iteratedDerivWithin 2 f (Set.Icc a b) t - 2 * c) t := by
    intro t ht
    refine ((hf'd t ht).sub_const ((f b - f a) / (b - a))).sub ?_
    have h : HasDerivAt (fun u : ℝ => 2 * u - a - b) (2 * 1) t :=
      (((hasDerivAt_id t).const_mul (2 : ℝ)).sub_const a).sub_const b
    exact (h.const_mul c).congr_deriv (by ring)
  -- Double Rolle produces the desired interior point.
  obtain ⟨ξ, hξ, hξ0⟩ := exists_second_derivative_eq_zero
    (fun t => f t - affinePanelInterp f a b t - c * ((t - a) * (t - b)))
    (fun t => derivWithin f (Set.Icc a b) t - (f b - f a) / (b - a) - c * (2 * t - a - b))
    (fun t => iteratedDerivWithin 2 f (Set.Icc a b) t - 2 * c) hax hxb hgc hg'c hgd hg'd
    (by simp) (by rw [hcx]; ring) (by simp)
  refine ⟨ξ, hξ, ?_⟩
  rw [hcx, show c = iteratedDerivWithin 2 f (Set.Icc a b) ξ / 2 by linarith]

/-- **Affine interpolation local error (Exercise 1.26).** If `f` is twice differentiable on
`Set.Icc a b` and its second derivative there is bounded in absolute value by `L`, then the affine
interpolant through the endpoint data approximates `f` to within `L / 2 * (x - a) * (b - x)`. -/
theorem abs_sub_affinePanelInterp_le {f : ℝ → ℝ} {a b L : ℝ} (hab : a < b)
    (hf : DifferentiableOn ℝ f (Set.Icc a b))
    (hf' : DifferentiableOn ℝ (derivWithin f (Set.Icc a b)) (Set.Icc a b)) (hL : 0 ≤ L)
    (hbound : ∀ y ∈ Set.Icc a b, |iteratedDerivWithin 2 f (Set.Icc a b) y| ≤ L) :
    ∀ x ∈ Set.Icc a b, |f x - affinePanelInterp f a b x| ≤ L / 2 * (x - a) * (b - x) := by
  have hrhs : ∀ y ∈ Set.Icc a b, (0 : ℝ) ≤ L / 2 * (y - a) * (b - y) := fun y hy =>
    mul_nonneg (mul_nonneg (div_nonneg hL zero_le_two) (sub_nonneg.mpr hy.1))
      (sub_nonneg.mpr hy.2)
  intro x hx
  rcases lt_or_eq_of_le hx.1 with hax | hxa
  · rcases lt_or_eq_of_le hx.2 with hxb | hxb
    · obtain ⟨ξ, hξ, hEq⟩ := exists_sub_affinePanelInterp_eq hab hf hf' ⟨hax, hxb⟩
      have hbξ : |iteratedDerivWithin 2 f (Set.Icc a b) ξ| ≤ L :=
        hbound ξ (Set.Ioo_subset_Icc_self hξ)
      have h1 : (0 : ℝ) ≤ x - a := by linarith
      have h2 : (0 : ℝ) ≤ b - x := by linarith
      have habs : |(x - a) * (x - b)| = (x - a) * (b - x) := by
        rw [abs_of_nonpos (by nlinarith : (x - a) * (x - b) ≤ 0)]
        ring
      rw [hEq, abs_mul, habs, abs_div, abs_two]
      nlinarith [mul_nonneg (sub_nonneg.mpr hbξ) (mul_nonneg h1 h2)]
    · subst hxb
      rw [affinePanelInterp_right, sub_self, abs_zero]
      exact hrhs _ hx
  · subst hxa
    rw [affinePanelInterp_left, sub_self, abs_zero]
    exact hrhs _ hx

/-- The unit-interval specialization of the affine interpolation local error bound: on `[0, 1]` the
right-hand side is `L / 2 * x * (1 - x)`. -/
theorem abs_sub_affinePanelInterp_le_unitInterval {f : ℝ → ℝ} {L : ℝ}
    (hf : DifferentiableOn ℝ f (Set.Icc 0 1))
    (hf' : DifferentiableOn ℝ (derivWithin f (Set.Icc 0 1)) (Set.Icc 0 1)) (hL : 0 ≤ L)
    (hbound : ∀ y ∈ Set.Icc (0 : ℝ) 1, |iteratedDerivWithin 2 f (Set.Icc 0 1) y| ≤ L) :
    ∀ x ∈ Set.Icc (0 : ℝ) 1, |f x - affinePanelInterp f 0 1 x| ≤ L / 2 * x * (1 - x) := by
  intro x hx
  simpa using abs_sub_affinePanelInterp_le zero_lt_one hf hf' hL hbound x hx
