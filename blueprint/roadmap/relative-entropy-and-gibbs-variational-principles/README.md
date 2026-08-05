---
kind: roadmap
status: mapped
---

# Relative entropy and Gibbs variational principles

Kullback-Leibler divergence and the Donsker-Varadhan log-partition variational formula, including product rules, Gaussian shifts, and the Gibbs exponential tilt.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Elementary probability and convexity bounds](../elementary-probability-and-convexity-bounds/README.md)
- [Matrix algebra and Gaussian conditioning](../matrix-algebra-and-gaussian-conditioning/README.md)

## Candidate contents

- Kullback-Leibler divergence for discrete laws
- Kullback-Leibler divergence for densities
- Nonnegativity and equality case for KL divergence
- Joint convexity of KL divergence
- KL chain and product rules
- Gaussian-shift KL divergence
- Donsker-Varadhan log-partition variational formula
- Gibbs exponential-tilt optimizer
- Donsker-Varadhan variational inequality

## Sources

- `sources/ltfp_book.pdf` — Chapter 14, Section 14.4, printed pages 424-425
- `sources/ltfp_book.pdf` — Chapter 15, Sections 15.1.3-15.1.4, printed pages 433-435

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `klDiv`
- `klDiv_eq_zero_iff`
- `klDiv_compProd_left`
- `klDiv_compProd_eq_add`

Primary file: `Mathlib/InformationTheory/KullbackLeibler/Basic.lean`.

Pinned revision 905b958 provides measure-theoretic Kullback-Leibler divergence, its zero criterion, and composition-product chain rules. No Donsker-Varadhan/Gibbs variational theorem, general joint-convexity theorem matching the book, or Gaussian-shift KL identity was found; those remain project-local. The source states the Donsker-Varadhan equality but does not prove it.
