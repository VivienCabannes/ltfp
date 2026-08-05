---
kind: roadmap
status: mapped
---

# Supervised learning setup and evaluation

The independent train-test framework, practical evaluation protocol, design conventions, and neighboring learning paradigms.

## Planning status

This milestone is mapped at coarse granularity. Its candidate contents have not yet been expanded into theorem-sized Autoform nodes.

## Milestone dependencies

- [Measure-theoretic probability and conditional expectation](../measure-theoretic-probability-and-conditional-expectation/README.md)

## Candidate contents

- Input and output spaces
- Training and testing data
- Independent identically distributed train-test assumption
- Learning algorithm as a dataset-to-predictor map
- Training-validation-testing split
- Cross-validation
- Hyperparameter and model selection
- Random-design and fixed-design settings
- In-sample evaluation
- Unsupervised learning
- Semisupervised learning
- Active learning
- Online learning
- Reinforcement learning
- Generative modeling

## Sources

- `sources/ltfp_book.pdf` — Chapter 2, Sections 2.1 and 2.7, printed pages 22-25 and 40-41

## Mathlib assessment

Legacy assessment: `partial`.

Relevant declarations:

- `ProbabilityTheory.iIndepFun`
- `ProbabilityTheory.IndepFun`
- `ProbabilityTheory.IdentDistrib`
- `MeasureTheory.ProbabilityMeasure.pi`

Primary file: `Mathlib/Probability/Independence/Basic.lean`.

Pinned Mathlib supplies independence of indexed random variables, identical distribution through equal pushforward laws, and finite product probability measures, which are enough to state i.i.d. train/test samples. Searches found no unified dataset, learner, training/validation/test split, cross-validation, hyperparameter-selection, or neighboring-learning-paradigm API. Those definitions are project-local; their measurable interfaces must be built explicitly on the probability substrate.
