/-
Copyright (c) 2026 Vivien Cabannes. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Vivien Cabannes
-/
import Mathlib.MeasureTheory.Constructions.BorelSpace.Basic
import Mathlib.MeasureTheory.Measure.Typeclasses.Probability

/-!
# Elementary tail bounds

Two elementary ingredients of the tail estimates of Chapter 1: the pointwise indicator bound that
Markov's inequality is obtained from by integration, and the union bound for the strict upper tail
of a pointwise bounded countable supremum.

Both statements are recorded twice, because in both cases the source-facing hypotheses are stronger
than what the argument consumes: a general auxiliary lemma, stated with the hypotheses the informal
content identifies as sufficient, and then the exact source-facing statement, derived from it.

## Graph nodes

* `MeasureTheory.ae_mul_indicator_lt_le_of_ae_nonneg` formalizes the tier-2 node
  `Threshold indicator bound for Markov's inequality`, transcribing
  `informal_content/threshold-indicator-bound-for-markovs-inequality.md`. The auxiliary
  `MeasureTheory.ae_mul_indicator_le_of_ae_nonneg` is the stronger closed-threshold version that the
  same argument proves, as the informal content observes: it holds for an arbitrary measure, an
  arbitrary threshold, and without measurability of `Y`.
* `MeasureTheory.measure_lt_sSup_range_le_tsum'` formalizes the tier-2 node
  `Supremum tail union bound`, transcribing `informal_content/supremum-tail-union-bound.md`. The
  auxiliary `MeasureTheory.measure_lt_sSup_range_le_tsum` is the general version that the same
  argument proves, as the informal content observes: it holds for an arbitrary measure and without
  measurability of the `Z i`, needing only a countable nonempty index type and pointwise
  boundedness above.

## Implementation notes

The informal content states both nodes for measurable random variables on a probability space and
explicitly records that the compiled arguments are more general. The auxiliary lemmas take that
observation literally and drop every hypothesis the argument does not consume: an arbitrary measure
in both cases, no measurability in either, and no positivity of the threshold in the indicator
bound. In particular the supremum tail bound needs no measurability because the measure of an
arbitrary set is defined, so the pointwise event identity and the countable union bound suffice.

The source-facing statements reinstate exactly the hypotheses the source lists. The binders they do
not consume, namely the measurability assumptions, are underscore-prefixed to record that they are
part of the transcribed statement rather than of the proof.

## Source

Francis Bach, *Learning Theory from First Principles*, Chapter 1, Section 1.2: Exercise 1.9 on
printed page 9 (indicator bound behind Markov's inequality) and the supremum-tail union-bound
display on printed page 9.
-/

namespace MeasureTheory

variable {Ω : Type*} {m : MeasurableSpace Ω}

/-- **Closed-threshold indicator bound.** If `Y` is nonnegative almost everywhere, then almost
everywhere `ε * 1_{Y ≥ ε} ≤ Y`. No measurability of `Y`, no positivity of `ε` and no normalization
of `μ` are needed; this is the general form of the bound behind Markov's inequality. -/
theorem ae_mul_indicator_le_of_ae_nonneg (μ : Measure Ω) {Y : Ω → ℝ} (hY : 0 ≤ᵐ[μ] Y) (ε : ℝ) :
    ∀ᵐ ω ∂μ, ε * Set.indicator {ω | ε ≤ Y ω} (fun _ ↦ (1 : ℝ)) ω ≤ Y ω := by
  filter_upwards [hY] with ω hω
  by_cases h : ω ∈ {ω | ε ≤ Y ω}
  · rw [Set.indicator_of_mem h, mul_one]
    exact h
  · rw [Set.indicator_of_notMem h, mul_zero]
    exact hω

/-- **Threshold indicator bound for Markov's inequality.** For a probability measure `μ`, a
measurable `Y : Ω → ℝ` that is nonnegative almost everywhere and a threshold `ε > 0`, almost
everywhere `ε * 1_{Y > ε} ≤ Y`. Integrating this inequality and dividing by `ε` yields Markov's
inequality. The measurability hypothesis and the probability-measure instance belong to the
source-facing statement and are deliberately kept although the pointwise argument does not use
them; see `MeasureTheory.ae_mul_indicator_le_of_ae_nonneg` for the general form. -/
theorem ae_mul_indicator_lt_le_of_ae_nonneg (μ : Measure Ω) [IsProbabilityMeasure μ] {Y : Ω → ℝ}
    (_hmeas : Measurable Y) (hY : 0 ≤ᵐ[μ] Y) {ε : ℝ} (hε : 0 < ε) :
    ∀ᵐ ω ∂μ, ε * Set.indicator {ω | ε < Y ω} (fun _ ↦ (1 : ℝ)) ω ≤ Y ω := by
  filter_upwards [ae_mul_indicator_le_of_ae_nonneg μ hY ε] with ω hω
  refine le_trans (mul_le_mul_of_nonneg_left ?_ hε.le) hω
  have hsub : {ω | ε < Y ω} ⊆ {ω | ε ≤ Y ω} :=
    Set.setOf_subset_setOf.mpr fun _ hx ↦ hx.le
  exact Set.indicator_le_indicator_of_subset hsub (fun _ ↦ zero_le_one) ω

/-- **Union bound for a countable supremum, general form.** For an arbitrary measure and a countable
nonempty family of real-valued functions whose pointwise range is bounded above, the measure of the
strict upper tail of the pointwise supremum is at most the sum of the measures of the strict upper
tails of the members. No measurability and no normalization of `μ` are needed: the measure of an
arbitrary set is defined, and the event is a countable union of the individual tail events. -/
theorem measure_lt_sSup_range_le_tsum (μ : Measure Ω) {I : Type*} [Countable I] [Nonempty I]
    {Z : I → Ω → ℝ} (hbdd : ∀ ω, BddAbove (Set.range fun i ↦ Z i ω)) (t : ℝ) :
    μ {ω | t < sSup (Set.range fun i ↦ Z i ω)} ≤ ∑' i, μ {ω | t < Z i ω} := by
  have hevent : {ω | t < sSup (Set.range fun i ↦ Z i ω)} = ⋃ i, {ω | t < Z i ω} := by
    ext ω
    simp only [Set.mem_setOf_eq, Set.mem_iUnion,
      lt_csSup_iff (hbdd ω) (Set.range_nonempty _), Set.exists_range_iff]
  rw [hevent]
  exact measure_iUnion_le _

/-- **Supremum tail union bound.** For a probability measure `μ` and a countable nonempty family of
measurable real-valued random variables whose pointwise range is bounded above, the probability that
the pointwise supremum exceeds `t` is at most the sum of the probabilities that the individual
members exceed `t`. The measurability hypothesis and the probability-measure instance belong to the
source-facing statement and are deliberately kept although the argument does not use them; see
`MeasureTheory.measure_lt_sSup_range_le_tsum` for the general form. -/
theorem measure_lt_sSup_range_le_tsum' (μ : Measure Ω) [IsProbabilityMeasure μ]
    {I : Type*} [Countable I] [Nonempty I] {Z : I → Ω → ℝ} (_hZ : ∀ i, Measurable (Z i))
    (hbdd : ∀ ω, BddAbove (Set.range fun i ↦ Z i ω)) (t : ℝ) :
    μ {ω | t < sSup (Set.range fun i ↦ Z i ω)} ≤ ∑' i, μ {ω | t < Z i ω} :=
  measure_lt_sSup_range_le_tsum μ hbdd t

end MeasureTheory
