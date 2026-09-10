# Audit evidence, 10 September 2026

This directory contains public source snapshots and a read-only local probe.
It contains no model-generated trajectories or training results. The
[feasibility note](../../notes/2026-09-10-feasibility.md) owns the interpretation.

`sources.json` maps downloads to their exact URLs. `SHA256SUMS` records file
hashes. Paper `.txt` files are convenience extracts of the saved HTML using
Python's standard HTML parser; math can appear twice or lose layout. Consult
the original HTML for equations. Source code was read, not executed.

Paper snapshots: aTTT 2607.03441v1; Self-Guided TTT 2607.09415v1;
VANE 2608.09448v2; Beyond Perplexity 2607.00368v1; decision-theoretic TTT
2606.15569v1. MLX files are pinned to commit
`86b48c461feebf87c58788655b7e57b5574b9e6d`. Model metadata pins Qwen3-0.6B
to `c1899de289a04d12100db370d81485cdf75e47ca`; weights were not downloaded.

The implementation search checked paper HTML links, aTTT's abstract page,
GitHub's repository search for the exact aTTT identifier, and web searches:

- `"2607.03441" code github`
- `"Self-Guided Test-Time Training for Long-Context LLMs" github`
- `"No Time Like the Present" "Training" github`
- `"aTTT" "Yanbo" code`
- `"2607.03441" github aTTT implementation`
- `"agentic test-time training" code`
- `"test time training" "source selection" agent`

Web discovery results were used to locate primary sources; raw search-engine
responses were not archived. Queries are recorded for scope, not exact search
reproduction. GitHub's exact-ID search returned zero repositories; that does
not exclude repositories without the ID. S-TTT metadata and its commit API
response document an empty repository, so no source commit is available.

Observed failures: the first sandboxed curl could not resolve arxiv.org;
an approved network retry succeeded. S-TTT's commit request with curl `--fail`
returned HTTP 409; a subsequent request saved the response body. Direct `sysctl`
hardware access was denied; `system_profiler` supplied the hardware facts.
Docker's configured socket was missing. `git status` reported no repository.
No package installation, model pull, daemon start, paid model call, or remote
compute job was attempted.

Reproduce the local probe from the project root:

```sh
UV_CACHE_DIR=/tmp/update-source-selection-uv uv run --no-project --no-python-downloads --python /opt/homebrew/bin/python3 scripts/probe_environment.py
```

Adjust the Python path on another machine. It reports module availability only
in that interpreter. Device serial numbers and UUIDs are excluded. The offered
48 GB laptop is a human-reported resource, not part of this probe.

Verify saved snapshots from this directory:

```sh
shasum -a 256 -c SHA256SUMS
```
