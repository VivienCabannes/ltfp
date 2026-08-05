---
kind: blueprint
status: active
---

# Learning Theory from First Principles in Lean

This blueprint presents the formalization roadmap for Francis Bach's
*Learning Theory from First Principles* and its separate exercise collection.
It preserves the approved project scope while using Autoform's Markdown-native,
leanblueprint-style presentation.

- [Roadmap](roadmap/README.md)
- [Coverage](coverage/README.md)
- [Source map](sources/README.md)
- [Dependency maps](dependencies.md) (generated locally and on GitHub Pages)

## Current state

The roadmap contains 116 coarse milestones spanning all fifteen chapters and
111 theorem-sized nodes in the seven milestones whose detailed content review
is complete. Of those detailed nodes, 97 are supplied by pinned Mathlib and 14
are proved in this repository.

Only links under a node's `## Depends on` or `## Proof depends on` heading are
Autoform DAG edges. Other links are ordinary navigation for Obsidian and the
rendered site.
