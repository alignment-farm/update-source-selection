# Update source selection

Read [README.md](README.md) first. It owns the starting question, initial
expectation, background, and links to this study's eventual findings.

This ancillary study investigates whether an agent can improve later decisions
by choosing which experience to use for parameter updates during an episode:
self-generated text, environmental observations, summaries, or no update.

The study owns its methods, implementation, experiments, analysis, and local
publication. Revise the question when evidence warrants it and explain material
changes. Keep work within the human's stated resources and expectation; return
to the human when those boundaries need to change. The parent project's study
map supplies background, not a mandatory experimental protocol.

### Research practice

- Start with the closest papers and available implementations. Distinguish
  existing conclusions, replications, and proposed extensions; record exact
  paper and implementation versions.
- Separate exploratory observations from prospective tests of a developed
  claim. Preserve inputs, outputs, configurations, failures, and the evidence
  needed to reproduce reported comparisons.
- Judge useful adaptation through later behavior, not training loss alone.
  Keep information access and costs explicit across comparisons, including
  selection, summaries, verification, and skipped updates.
- Keep working documentation proportional to the investigation. Publish a
  local research note or paper with supporting evidence and reproduction
  instructions; link it from the README. Negative and inconclusive results
  are valid outcomes. External submission is a separate human decision.

### Model resources

- Open weight models with `docker model` (preferred)
- OpenAI models with `codex`
- SpaceXAI models with `agent`

### Dependency management

- Use `uv` for Python package and project management.
- Use `docker` for local models and `compose`/Dockerfile(s) for complex resources, if/when needed.
