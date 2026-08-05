---
kind: roadmap
status: mapped
---

# Minimax reduction and packing

Reduction of statistical minimax estimation to finite testing problems and construction of separated hypotheses by volumetric and coding arguments.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Consistency, minimax limits, and adaptivity](../consistency-minimax-limits-and-adaptivity/README.md)
- [Entropy, data processing, and Fano inequalities](../entropy-data-processing-and-fano-inequalities/README.md)
- [Relative entropy and Gibbs variational principles](../relative-entropy-and-gibbs-variational-principles/README.md)
- [Metric and measure-theoretic geometry](../metric-and-measure-theoretic-geometry/README.md)
- [Elementary probability and convexity bounds](../elementary-probability-and-convexity-bounds/README.md)
- [Hoeffding and sub-Gaussian concentration](../hoeffding-and-sub-gaussian-concentration/README.md)

## Candidate contents

- Minimax excess risk
- Restriction to a finite hard family
- Separation condition for estimators
- Estimator-to-test reduction
- Testing-error lower bound for minimax risk
- Pairwise KL control of mutual information
- Fano minimax lower-bound template
- Euclidean packing number
- Volumetric packing of l2 balls (Lemma 15.1)
- Hamming distance and binary codes
- Varshamov-Gilbert lemma (Lemma 15.2)
- Hypercube packing construction
- Choice of separation and information radii

## Sources

- `sources/ltfp_book.pdf` — Chapter 15, Sections 15.1.1-15.1.4 and Lemmas 15.1-15.2, printed pages 428-436

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `ProbabilityTheory.minimaxRisk`
- `Metric.packingNumber`
- `Metric.exists_set_encard_eq_packingNumber`
- `Metric.IsSeparated.encard_le_packingNumber`
- `hammingDist`
- `Hamming`

Primary file: `Mathlib/Topology/MetricSpace/CoveringNumbers.lean`.

Pinned Mathlib 905b95818eb32af7874a58b427f50c1711a5e96c. Direct or narrowly matched members: ProbabilityTheory.minimaxRisk defines generic minimax risk; Metric.packingNumber defines packing numbers and the listed lemmas realize finite maximal separated sets and their cardinality bound; hammingDist and Hamming provide finite-product Hamming geometry. The minimax definition is in Mathlib/Probability/Decision/Risk/Defs.lean and Hamming geometry is in Mathlib/InformationTheory/Hamming.lean. Searches found no estimator-to-test reduction, mutual-information/Fano minimax template, Euclidean volumetric ball-packing lemma, coding-theoretic Varshamov-Gilbert lemma, or hypercube hard-family construction. Materially uncovered members: Minimax excess-risk specialization; Restriction to a finite hard family; Separation condition for estimators; Estimator-to-test reduction; Testing-error lower bound for minimax risk; Pairwise KL control of mutual information; Fano minimax lower-bound template; Volumetric packing of l2 balls (Lemma 15.1); Binary-code existence and size bounds beyond Hamming distance; Varshamov-Gilbert lemma (Lemma 15.2); Hypercube packing construction; Choice of separation and information radii.
