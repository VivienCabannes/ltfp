---
kind: roadmap
status: mapped
---

# Entropy, data processing, and Fano inequalities

Finite entropy, mutual information, data processing, and Fano inequalities that convert indistinguishable hypotheses into lower bounds for testing error.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Relative entropy and Gibbs variational principles](../relative-entropy-and-gibbs-variational-principles/README.md)
- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)
- [Elementary probability and convexity bounds](../elementary-probability-and-convexity-bounds/README.md)

## Candidate contents

- Entropy of a finite random variable
- Conditional entropy
- Chain rule for entropy
- Conditioning reduces entropy
- Binary entropy bound
- Mutual information
- Mutual information as expected KL divergence
- Data-processing inequality
- Basic Fano inequality
- Full Fano inequality
- Tensorization and samplewise mutual-information bound
- Fano inequality for multiple-hypothesis testing

## Sources

- `sources/ltfp_book.pdf` — Chapter 15, Sections 15.1.3-15.1.4, Propositions 15.1-15.2 and Corollary 15.1, printed pages 431-435

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `Real.binEntropy`
- `Real.qaryEntropy`

Primary file: `Mathlib/Analysis/SpecialFunctions/BinaryEntropy.lean`.

Pinned Mathlib provides scalar binary and q-ary entropy functions. No random-variable Shannon or conditional entropy, mutual information, data-processing inequality, or Fano inequality was found; those remain project-local. The book's continuous-variable extension of the multiple-testing argument is stated by reference rather than proved in this section.
