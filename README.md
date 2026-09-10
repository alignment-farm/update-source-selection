# Update source selection

This study asks whether an agent can learn more usefully from an episode by
choosing what to train on as the episode develops. It begins with online
parameter adaptation, such as LoRA updates, and builds on existing test-time
training research. It is an independent investigation arising from
[Construct-2's S1 question](../../construct-2/sources/THEORIES_AND_QUESTIONS.md#s1-can-an-agent-choose-which-experience-to-train-on-during-an-episode).

## Question

**Does choosing between self-generated text, environmental observations,
summaries, and no update improve later decisions when the most useful source
changes during an episode?**

The comparison that matters is against the strongest fixed source or fixed
mixture selected on development data, with comparable resources and information
access. A selector might identify useful evidence as circumstances change. It
might instead gain only by making fewer updates, or by choosing the source that
is generally best for that model. Those are competing explanations to examine.

## Initial expectation

Begin with a focused investigation: understand the closest existing methods,
inspect whether their implementations can support the question, and develop a
small, informative empirical comparison where feasible. Start with existing
implementations where useful. The investigator owns the exact protocol and may
revise the question in light of prior work or early observations.

The intended first outcome is a short local research note explaining what is
already answered, what was investigated, what the evidence supports, and whether
a larger investigation is worthwhile. Finding that the question is already
answered, that dynamic selection offers no advantage, or that the available
setup cannot distinguish the explanations is useful progress. A positive result
is not required.

No numerical time, compute, or spending cap has been specified. This starting
brief does not imply an unlimited campaign: keep the initial work focused and
bring substantial expansion or new resource requirements back to the human.
Publication polish should fit the evidence and effort.

## Starting evidence and sources

- [aTTT, 2607.03441v1, §§3–5](https://arxiv.org/html/2607.03441v1)
  compares Self, Env, and Summary text for episode-specific adapter updates.
  It leaves online selection or combination of those sources open in that
  paper. Inspect its exact update, reset, and evaluation implementation first.
- [Self-Guided TTT, 2607.09415v1](https://arxiv.org/html/2607.09415v1)
  already selects training spans with a known question. Establish what an
  episode-level selector would add beyond that setting.
- [VANE, 2608.09448v2](https://arxiv.org/html/2608.09448v2)
  provides related adaptation-validation work in robotics; its modality and
  information access differ from textual agent experience.
- [Beyond Perplexity, 2607.00368v1](https://arxiv.org/html/2607.00368v1)
  distinguishes improved prediction loss from useful deployment memory.
- [Decision-theoretic TTT, 2606.15569v1](https://arxiv.org/abs/2606.15569v1)
  is a follow-up reading candidate; the parent project has reviewed only its
  abstract. Check its relevance before making novelty claims.

The parent's [B0 explanation and evidence map](../../construct-2/sources/THEORIES_AND_QUESTIONS.md)
provides mechanism background and links to Construct and Formation findings.
In particular, producing useful information and using it successfully can fail
separately. The map is a starting assessment, not an exhaustive novelty review.

## Possible first comparison

Hold the base model and adaptation mechanism fixed initially. Compare dynamic
selection with fixed sources, a fixed mixture, a matched random selector, and
no update. Include an explicit-context comparison using the same available
information. Common recorded episode prefixes could isolate the immediate
effect of selection before live trajectories introduce different subsequent
experiences. These are design suggestions, not a frozen protocol.

Measure later task behavior alongside training loss, update counts, and total
cost. Charge selection and summary generation as well as adaptation. Any source
verification information available to the selector must also be available to
its controls. Distinguish novel but incorrect text from repeated but useful
corrections; novelty alone does not establish training value. A gain that
disappears against a well-chosen fixed policy or after cost matching supports a
simpler explanation.

## Resources

- Open-weight models through `docker model` are preferred.
- OpenAI models through `codex` and SpaceXAI models through `agent` are available
  resource routes; their usable roles depend on the interfaces provided.
- Use `uv` for Python and Docker/Compose for model or supporting services where
  appropriate.

Inspect local model availability, hardware, and training support before sizing
experiments. Inference access alone does not provide the gradients or mutable
parameters required by the neural treatment.

On 10 September 2026, the human also offered a second Apple M3 laptop with
48 GB memory for larger models if needed. Notify the human when a move is
warranted. Access and training support on that machine remain unverified.

## Findings and publication

The [first paper/code audit and feasibility proposal](notes/2026-09-10-feasibility.md)
is available, with [saved supporting evidence](evidence/2026-09-10-audit/README.md).
The current laptop has 8 GB memory and an unreachable Docker model runner.
No aTTT implementation was located in the focused search; the S-TTT repository
was empty. Pinned MLX source provides a candidate training route. No model
experiments or empirical adaptation findings are recorded yet.
Keep methods, code, data, saved outputs, and reproduction instructions in this
project. Add links here as evidence and a manuscript become available. LaTeX
source, a bibliography, and a compiled PDF are the intended publication format,
scaled to the investigation; an early useful result need not wait for polish.

The [ancillary-study guidance](../../construct-2/notes/ANCILLARY_STUDY.md)
describes the relationship: this project investigates and publishes locally;
Construct-2 reads those publications and updates its broader theories.
# update-source-selection
