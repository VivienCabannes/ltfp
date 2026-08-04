# Supremum tail union bound

Let `mu` be a probability measure, let `I` be a countable nonempty index type, and let `Z i : Omega -> Real` be measurable for every `i`. Suppose that, for every `omega`, the set

`Set.range (fun i => Z i omega)`

is bounded above. Then, for every `t : Real`,

`mu {omega | t < sSup (Set.range (fun i => Z i omega))}`

`<= sum' i, mu {omega | t < Z i omega}`.

Both tail events are strict. Nonemptiness and pointwise boundedness make the real supremum meaningful and are exactly the conditions needed for the event identity used below.

## Proof

Fix `omega`. Because the range is nonempty and bounded above, the defining properties of the real supremum give

`t < sSup (Set.range (fun i => Z i omega))`

if and only if there exists an index `i` such that `t < Z i omega`. In one direction, a strict lower bound on the supremum must be exceeded by a member of the range. In the other direction, every member of the bounded range is at most its supremum.

Consequently,

`{omega | t < sSup (Set.range (fun i => Z i omega))}`

`= union i, {omega | t < Z i omega}`.

Apply the countable union bound to this equality.

The source states this for measurable random variables on a probability space. The compiled inequality itself is stronger: because measure is defined on arbitrary sets, it needs only a countable nonempty index type and the pointwise bounded-above hypothesis under an arbitrary measure.

### Mathlib support

Declarations: `MeasureTheory.measure_iUnion_le`, `lt_csSup_iff`
Files: `Mathlib/MeasureTheory/OuterMeasure/Basic.lean`, `Mathlib/Order/ConditionallyCompleteLattice/Basic.lean`
