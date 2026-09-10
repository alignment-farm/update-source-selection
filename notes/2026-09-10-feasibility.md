# First audit and proposed pilot

10 September 2026. Status: literature and source-code inspection; no model
installation, training, inference experiment, or replication performed.

## Decision

Keep the study question, but begin with a **source-effect diagnostic before
building a selector**. First establish that updates affect later actions and
that the useful source varies within an episode. Otherwise selector development
would confound a weak learning mechanism with a weak selection policy.

A faithful aTTT replication is currently unavailable: this search did not locate
its implementation. The local 8 GB Apple M3 machine also argues for a much
smaller, sequential diagnostic. Native MLX is a plausible training fallback;
runtime feasibility remains untested. This would be a proposed extension using
some paper settings, not a replication of its reported results.

## Closest evidence

**aTTT, [2607.03441v1](https://arxiv.org/html/2607.03441v1), §§3–5 and Appendices A–E.**
Self and Env use the latest message and observation; Summary compresses the
prefix through a base-model call. Episode-persistent LoRA resets between
episodes. Defaults: rank 8, alpha 16, learning rate 5e-4, two gradient steps
every five agent steps. Repetition weighting uses token trigrams, floor 0.05,
and token-count normalization. Evaluation includes ALFWorld and SWE-bench Lite;
the smallest evaluated model is Qwen3.5-4B. Serving and training use separate
GPU resources. The paper leaves online source selection open and reports
model-dependent source rankings. Its summary-context control is narrower than
a general test of explicit memory. Section 4.5 and Appendix E give inconsistent
no-update values (50.7 versus 51.4).

No implementation link was found in the inspected HTML/abstract, title/ID web
searches, or GitHub repository search by exact arXiv ID. This is a search limit,
not proof of nonexistence. Unresolved implementation details include optimizer
configuration/state reset, target modules, token boundaries and truncation,
summary prompt, exact seeds, dataset revisions/instance IDs, and adapter-swap
timing. These prevent an exact reset/update/evaluation code audit.

**Self-Guided TTT, [2607.09415v1](https://arxiv.org/html/2607.09415v1), §2, §4.1, Appendix A.**
The model selects verbatim spans with the question already available, adapts,
then answers with the full context. Each instance starts fresh. Answer-aware
oracle annotations are diagnostic privileged information; the deployable
selector does not receive the answer. Query-projection LoRA uses rank 16,
alpha 32, AdamW and validation-selected learning rates. This already establishes
training-text selection as a meaningful research direction. Our possible
addition is sequential source choice, including abstention, under changing
experience. The [S-TTT repository](https://github.com/TianHongZXY/S-TTT) exists
but was empty at inspection: GitHub reports size zero and the commit endpoint
returns “Git Repository is empty.” No implementation commit can be recorded.

**VANE, [2608.09448v2](https://arxiv.org/html/2608.09448v2), §3.4.**
Shadow prompt updates are validated against the incumbent on matched future
visual evidence before deployment. This supplies a useful validation design,
but its predictive objective, modality, and timing differ from immediate text
source selection. Future feedback cannot be supplied early to our selector.
This audit inspected the method, not a robotics implementation.

**Beyond Perplexity, [2607.00368v1](https://arxiv.org/html/2607.00368v1), §§3, 5–6.**
Its sparse-fact diagnostic distinguishes improved losses from generated recall;
the evaluation framework motivates behavioral outcomes and explicit-memory
controls. It does not establish that all episode adaptation fails. Removing
support context would test a stronger memory claim than our initial question.

**Decision-theoretic TTT, [2606.15569v1](https://arxiv.org/html/2606.15569v1), §§3–8.**
Read beyond the abstract: the analysis uses local linearization, quadratic
objectives and Gaussian assumptions to relate query risk to update horizon
and subspace. It motivates adaptation choices but does not supply an evaluated
Self/Env/Summary episode selector. We have not independently checked its proofs
or established that its guarantees apply to the proposed language-model pilot.

This is a focused review, not an exhaustive novelty search. No claim of novelty
or independent confirmation of published gains follows.

## Local resources and reusable implementation

The [saved probe](../evidence/2026-09-10-audit/environment.json) records an M3
MacBook Air, 8 GB unified memory, 10 GPU cores, macOS 26.6.2, and roughly 72 GiB
available disk. `uv`, `docker`, `codex`, and `agent` executables exist. Docker
Model Runner client v1.2.6 is installed, but its configured daemon socket is
missing; models could not be listed. Do not interpret that as an empty model
inventory. No training libraries were found in the probed interpreter; other
environments were not exhaustively searched. No TeX compiler was found on PATH.
The directory is not currently a Git repository.

[Docker Model Runner documentation](https://docs.docker.com/ai/model-runner/)
describes a serving route; neither local CLI inspection nor this documentation
established mutable gradient access. Starting Docker would not itself resolve
the training requirement.

Inspected [MLX LM](https://github.com/ml-explore/mlx-lm/tree/86b48c461feebf87c58788655b7e57b5574b9e6d)
commit `86b48c461feebf87c58788655b7e57b5574b9e6d` as an alternative implementation:

- `tuner/trainer.py`: shifted next-token loss, masking, custom loss callback,
  gradient updates, and memory reporting are exposed.
- `tuner/utils.py`: target-module conversion and adapter loading/removal exist.
- `tuner/lora.py`: the low-rank delta is multiplied directly by `scale`.
  Under the conventional alpha/rank parameterization, alpha 16 and rank 8
  therefore map to MLX scale 2, not 16.
- `models/qwen3.py`: Qwen3 implementation exists. `setup.py` requires MLX
  >=0.32.2 on Darwin and Transformers >=5.7.0; a future `uv.lock` must resolve
  and pin the full environment. Nothing was installed or imported from it.

MLX is reusable training machinery, not an existing aTTT episode harness. We
would own repetition weighting, source construction, behavioral evaluation,
and snapshots of adapter, optimizer, random state and repetition history.
Generation caches must be rebuilt after adapter changes. Runtime tests must
verify that resets recover the initial policy and branch states cannot leak.

## Concrete exploratory pilot proposal

**Model and treatment.** Candidate:
[Qwen/Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B), revision
`c1899de289a04d12100db370d81485cdf75e47ca`. Use native MLX, one loaded base model,
sequential branches, short sequences, and explicit LoRA target modules. Start
with query projections, rank 8 and scale 2; these module choices are our own.
Begin with two gradient steps at 5e-4. Do not tune an unconstrained grid if
acquisition fails. Model competence at this scale is an open feasibility issue.

**Task.** Use a small deterministic text environment with inspect/move/take
actions and verifiable outcomes. First check that the model can act correctly
when the needed facts are supplied in context. Construct 12 exploratory
episodes with two update checkpoints each, deliberately including repeated
correct evidence and novel misleading assertions. Vary which source contains
useful evidence and its order. Keep actual model-produced Self text distinct
from researcher-authored diagnostic text. Record both; do not call injected
assertions self-generated experience.

At each checkpoint, snapshot a common prefix and branch into Self, Env,
Summary, and no update. Generate Summary once from the same prefix using a
frozen base model. Update each branch from identical pre-update state, then
score four subsequent environment actions. Only the scorer sees hidden state.
This measures a local intervention effect, not the value of an online policy
whose earlier choices change the trajectory. Any retrospective best-source
score is descriptive and may be optimistically biased.

**Go/no-go evidence.** Verify changed adapter tensors with unchanged base
weights, stable resets, finite gradients, and at least occasional downstream
behavioral differences. Report all 12 episodes, including failures. If source
rankings do not vary, report weak evidence for selection opportunity. If direct
context works but updates do not, diagnose acquisition before selector design.
These are exploratory decisions, not prospective statistical significance tests.

**Later prospective comparison.** Only after the diagnostic, freeze tasks,
splits, source formatting, selector, and update rules. Tune fixed sources,
fixed mixtures, cadence and abstention on development data with a disclosed
budget. Compare dynamic selection with those controls, matched random selection,
no update, and explicit context. The random control should separately test
source choice at the selector's realized update times and a matched-count
schedule; replaying adaptive times is a diagnostic, not an independent policy.
Keep evaluation episodes and scorer answers out of selector development.

Use identical observable prefixes and verification information. Summary
construction can use more history than latest-step sources, so expose that
history to every policy and include a development-tuned mixture with comparable
access. Charge every generated candidate summary, even when unselected.
Record losses, action success, invalid actions, tokens by purpose, optimizer
steps, update timing, latency and peak memory. Compare behavior/cost frontiers;
do not assert exact compute matching merely from equal update counts.

**Proposed resource envelope, not a measured requirement.** A 0.6B model needs
about 1.2 GB for 16-bit weights alone. Budget up to 3 GB of downloads and 5 GB
of study disk for one model/environment; begin with a 10-minute runtime probe,
then at most one local compute hour for the exploratory pilot. Target a
process peak below 5 GB and stop on sustained memory pressure. These are
conservative investigator-proposed limits, not user-specified caps or throughput
promises. The 24 checkpoints imply 72 adaptation branches (144 gradient steps),
24 summaries and 96 four-action continuations. Pilot throughput decides whether
that fits. No paid APIs, remote GPU jobs, or larger models are part of this
proposal. Revisit resources with the human if this envelope is inadequate.

**Human resource update, 10 September:** a second Apple M3 laptop with 48 GB
memory is available for larger models if needed. Its hardware and software
have not been independently inspected, and no remote access is established.
Use the current machine for a small implementation smoke test. Recommend moving
the substantive comparison to the 48 GB machine if the 0.6B model fails the
supplied-context competence check, adaptation hits memory pressure, or a useful
pilot warrants a model closer to aTTT's 4B minimum. A 4B model has roughly 8 GB
of 16-bit weights before activations and other overhead; 48 GB makes that route
plausible, not yet benchmarked. Tell the human when that transition is warranted;
do not interpret the extra memory as an unlimited experiment budget.

## Evidence and continuation

[Evidence index](../evidence/2026-09-10-audit/README.md) gives exact URLs,
saved source snapshots, failures and checksums. Re-run the read-only probe with
`UV_CACHE_DIR=/tmp/update-source-selection-uv uv run --no-project scripts/probe_environment.py`.
The current deliverable is this feasibility note. A results manuscript in
LaTeX/PDF should follow actual evidence; no empirical findings are claimed here.
