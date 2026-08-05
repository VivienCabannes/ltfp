/-
Copyright (c) 2026 Vivien Cabannes. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Vivien Cabannes
-/
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.MeasureTheory.Function.ConvergenceInMeasure
import Mathlib.Probability.IdentDistrib
import Mathlib.Probability.Moments.Variance

/-!
# Sample means of pairwise independent identically distributed random variables

This file studies the empirical average `A n ω = (n : ℝ)⁻¹ * ∑ i ∈ Finset.range n, X i ω` of a
sequence `X : ℕ → Ω → ℝ` whose entries are pairwise independent and identically distributed with
`X 0`. Only square integrability of `X 0` is assumed: identical distribution transports it to every
sampled variable. We compute the variance of the sample mean, deduce the mean-square error identity
and Chebyshev's finite-sample deviation bound, and conclude convergence in probability to the common
expectation.

## Graph nodes

* `ProbabilityTheory.sampleMean`: the empirical average used by all four statements below; it is the
  quantity denoted `A_n` in the informal content files.
* `ProbabilityTheory.variance_sampleMean`: node `Variance of an iid sample mean`, transcribing
  `informal_content/variance-of-an-iid-sample-mean.md`.
* `ProbabilityTheory.integral_sampleMean_sub_integral_sq`: node
  `Mean-square error identity for an iid sample mean`, transcribing
  `informal_content/mean-square-error-identity-for-an-iid-sample-mean.md`.
* `ProbabilityTheory.measureReal_abs_sampleMean_sub_integral_gt_le`: node
  `Finite deviation bound for an iid sample mean`, transcribing
  `informal_content/finite-deviation-bound-for-an-iid-sample-mean.md`. The auxiliary lemma
  `ProbabilityTheory.measureReal_abs_sampleMean_sub_integral_ge_le` records the stronger
  closed-threshold bound that Mathlib's Chebyshev inequality supplies.
* `ProbabilityTheory.tendstoInMeasure_sampleMean`: node
  `Convergence in probability of iid sample means`, transcribing
  `informal_content/convergence-in-probability-of-iid-sample-means.md`.

The nodes `Variance of a finite sum of pairwise independent random variables` and
`Mean-square convergence of iid sample means` are already discharged by Mathlib
(`ProbabilityTheory.IndepFun.variance_sum` and `ProbabilityTheory.strong_law_Lp`) and are therefore
not restated here; the first one is used below.

## Source

Francis Bach, *Learning Theory from First Principles*, Chapter 1, Section 1.2, printed page 8
(the sample-mean variance display, equation (1.4), the finite deviation display, and the sentence
that follows it).
-/

open Filter MeasureTheory

open scoped Topology

namespace ProbabilityTheory

variable {Ω : Type*} [MeasurableSpace Ω] {μ : Measure Ω} {X : ℕ → Ω → ℝ} {n : ℕ} {ε : ℝ}

/-- The sample mean, or empirical average, of the first `n` terms of a sequence `X` of real random
variables: `sampleMean X n ω = (n : ℝ)⁻¹ * ∑ i ∈ Finset.range n, X i ω`. Lean's totalized inverse
makes `sampleMean X 0 = 0`. Every statement below that evaluates a moment of the sample mean
assumes `0 < n`; the square-integrability lemmas hold for every `n`, and the `atTop` limit is
insensitive to the value at `n = 0`. -/
noncomputable def sampleMean (X : ℕ → Ω → ℝ) (n : ℕ) (ω : Ω) : ℝ :=
  (n : ℝ)⁻¹ * ∑ i ∈ Finset.range n, X i ω

omit [MeasurableSpace Ω] in
/-- The sample mean is the scalar multiple `(n : ℝ)⁻¹ • ∑ i ∈ Finset.range n, X i` of the
`Finset`-sum of the sampled variables, seen as functions. -/
theorem sampleMean_eq_smul_sum (X : ℕ → Ω → ℝ) (n : ℕ) :
    sampleMean X n = (n : ℝ)⁻¹ • ∑ i ∈ Finset.range n, X i := by
  ext ω
  simp [sampleMean, Finset.sum_apply]

/-- If `X 0` is square integrable and identically distributed with every `X i` for `i < n`, then the
sample mean `sampleMean X n` is square integrable. -/
theorem memLp_sampleMean (hX : MemLp (X 0) 2 μ)
    (hident : ∀ i < n, IdentDistrib (X 0) (X i) μ μ) : MemLp (sampleMean X n) 2 μ := by
  rw [sampleMean_eq_smul_sum]
  exact (memLp_finsetSum' _ fun i hi => (hident i (Finset.mem_range.mp hi)).memLp_snd hX).const_smul
    ((n : ℝ)⁻¹)

/-- On a finite measure space, the sample mean of a positive number of square-integrable
identically distributed variables has the common expectation of the sample. -/
theorem integral_sampleMean [IsFiniteMeasure μ] (hn : 0 < n) (hX : MemLp (X 0) 2 μ)
    (hident : ∀ i < n, IdentDistrib (X 0) (X i) μ μ) : μ[sampleMean X n] = μ[X 0] := by
  have hn' : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hn.ne'
  have hint : ∀ i ∈ Finset.range n, Integrable (X i) μ := fun i hi =>
    ((hident i (Finset.mem_range.mp hi)).memLp_snd hX).integrable one_le_two
  have hsum : ∀ i ∈ Finset.range n, ∫ ω, X i ω ∂μ = ∫ ω, X 0 ω ∂μ := fun i hi =>
    ((hident i (Finset.mem_range.mp hi)).integral_eq).symm
  calc μ[sampleMean X n]
      = (n : ℝ)⁻¹ * ∫ ω, ∑ i ∈ Finset.range n, X i ω ∂μ := integral_const_mul _ _
    _ = (n : ℝ)⁻¹ * ∑ i ∈ Finset.range n, ∫ ω, X i ω ∂μ := by rw [integral_finsetSum _ hint]
    _ = (n : ℝ)⁻¹ * ((n : ℝ) * μ[X 0]) := by
        rw [Finset.sum_congr rfl hsum]
        simp [Finset.sum_const, nsmul_eq_mul]
    _ = μ[X 0] := by field_simp

/-- **Variance of an iid sample mean.** For an arbitrary measure `μ`, a positive sample size `n`, a
square-integrable `X 0`, pairwise independence on `Finset.range n` and identical distribution of
`X 0` with every `X i` for `i < n`, the variance of the sample mean is the common variance divided
by the sample size. -/
theorem variance_sampleMean (hn : 0 < n) (hX : MemLp (X 0) 2 μ)
    (hindep : Set.Pairwise (Finset.range n : Set ℕ) fun i j => IndepFun (X i) (X j) μ)
    (hident : ∀ i < n, IdentDistrib (X 0) (X i) μ μ) :
    Var[sampleMean X n; μ] = Var[X 0; μ] / n := by
  have hn' : (n : ℝ) ≠ 0 := Nat.cast_ne_zero.mpr hn.ne'
  have hvar : ∀ i ∈ Finset.range n, Var[X i; μ] = Var[X 0; μ] := fun i hi =>
    ((hident i (Finset.mem_range.mp hi)).variance_eq).symm
  calc Var[sampleMean X n; μ]
      = ((n : ℝ)⁻¹) ^ 2 * Var[∑ i ∈ Finset.range n, X i; μ] := by
        rw [sampleMean_eq_smul_sum, variance_smul]
    _ = ((n : ℝ)⁻¹) ^ 2 * ∑ i ∈ Finset.range n, Var[X i; μ] := by
        rw [IndepFun.variance_sum
          (fun i hi => (hident i (Finset.mem_range.mp hi)).memLp_snd hX) hindep]
    _ = ((n : ℝ)⁻¹) ^ 2 * ((n : ℝ) * Var[X 0; μ]) := by
        rw [Finset.sum_congr rfl hvar]
        simp [Finset.sum_const, nsmul_eq_mul]
    _ = Var[X 0; μ] / n := by field_simp

/-- **Mean-square error identity for an iid sample mean.** On a probability space, the expected
squared deviation of the sample mean from the common expectation is the common variance divided by
the positive sample size. -/
theorem integral_sampleMean_sub_integral_sq [IsProbabilityMeasure μ] (hn : 0 < n)
    (hX : MemLp (X 0) 2 μ)
    (hindep : Set.Pairwise (Finset.range n : Set ℕ) fun i j => IndepFun (X i) (X j) μ)
    (hident : ∀ i < n, IdentDistrib (X 0) (X i) μ μ) :
    ∫ ω, (sampleMean X n ω - μ[X 0]) ^ 2 ∂μ = Var[X 0; μ] / n := by
  rw [← integral_sampleMean hn hX hident,
    ← variance_eq_integral (memLp_sampleMean hX hident).aestronglyMeasurable.aemeasurable]
  exact variance_sampleMean hn hX hindep hident

/-- Chebyshev's bound for the sample mean at a closed threshold. This is the stronger form that
Mathlib's `ProbabilityTheory.meas_ge_le_variance_div_sq` supplies; the strict-event form recorded in
the source follows from it by inclusion. -/
theorem measureReal_abs_sampleMean_sub_integral_ge_le [IsProbabilityMeasure μ] (hn : 0 < n)
    (hε : 0 < ε) (hX : MemLp (X 0) 2 μ)
    (hindep : Set.Pairwise (Finset.range n : Set ℕ) fun i j => IndepFun (X i) (X j) μ)
    (hident : ∀ i < n, IdentDistrib (X 0) (X i) μ μ) :
    μ.real {ω | ε ≤ |sampleMean X n ω - μ[X 0]|} ≤ Var[X 0; μ] / (n * ε ^ 2) := by
  have hcheb := meas_ge_le_variance_div_sq (memLp_sampleMean hX hident) hε
  rw [integral_sampleMean hn hX hident, variance_sampleMean hn hX hindep hident, div_div] at hcheb
  have hnonneg : 0 ≤ Var[X 0; μ] / ((n : ℝ) * ε ^ 2) :=
    div_nonneg (variance_nonneg (X 0) μ) (by positivity)
  exact ENNReal.toReal_le_of_le_ofReal hnonneg hcheb

/-- **Finite deviation bound for an iid sample mean.** On a probability space, with a positive
sample size and a positive threshold, the probability that the sample mean deviates from the common
expectation by more than `ε` is at most `Var[X 0; μ] / (n * ε ^ 2)`. -/
theorem measureReal_abs_sampleMean_sub_integral_gt_le [IsProbabilityMeasure μ] (hn : 0 < n)
    (hε : 0 < ε) (hX : MemLp (X 0) 2 μ)
    (hindep : Set.Pairwise (Finset.range n : Set ℕ) fun i j => IndepFun (X i) (X j) μ)
    (hident : ∀ i < n, IdentDistrib (X 0) (X i) μ μ) :
    μ.real {ω | ε < |sampleMean X n ω - μ[X 0]|} ≤ Var[X 0; μ] / (n * ε ^ 2) := by
  refine le_trans (measureReal_mono ?_)
    (measureReal_abs_sampleMean_sub_integral_ge_le hn hε hX hindep hident)
  intro ω hω
  simp only [Set.mem_setOf_eq] at hω ⊢
  exact hω.le

/-- **Convergence in probability of iid sample means.** On a probability space, if `X 0` is square
integrable, the sequence `X` is pairwise independent and every `X i` is identically distributed with
`X 0`, then the sample means converge in probability to the common expectation. -/
theorem tendstoInMeasure_sampleMean [IsProbabilityMeasure μ] (hX : MemLp (X 0) 2 μ)
    (hindep : Pairwise fun i j => IndepFun (X i) (X j) μ)
    (hident : ∀ i, IdentDistrib (X 0) (X i) μ μ) :
    TendstoInMeasure μ (fun n => sampleMean X n) atTop fun _ => μ[X 0] := by
  rw [tendstoInMeasure_iff_measureReal_dist]
  intro ε hε
  have hε' : 0 < ε / 2 := by positivity
  have hg : Tendsto (fun n : ℕ => Var[X 0; μ] / ((n : ℝ) * (ε / 2) ^ 2)) atTop (𝓝 0) := by
    have hrw : (fun n : ℕ => Var[X 0; μ] / ((n : ℝ) * (ε / 2) ^ 2)) =
        fun n : ℕ => Var[X 0; μ] / (ε / 2) ^ 2 / (n : ℝ) := by
      ext n
      rw [div_div, mul_comm ((ε / 2) ^ 2) (n : ℝ)]
    rw [hrw]
    exact tendsto_const_div_atTop_nhds_zero_nat _
  refine squeeze_zero' (Eventually.of_forall fun n => measureReal_nonneg) ?_ hg
  filter_upwards [eventually_gt_atTop 0] with n hn
  refine le_trans (measureReal_mono ?_) (measureReal_abs_sampleMean_sub_integral_gt_le hn hε' hX
    (hindep.set_pairwise _) fun i _ => hident i)
  intro ω hω
  simp only [Set.mem_setOf_eq, Real.dist_eq] at hω ⊢
  linarith

end ProbabilityTheory
