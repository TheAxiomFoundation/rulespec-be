# Bulk encode (BE)

A durable queue → runner → PR loop for bulk RuleSpec encoding, independent of
any local session. It encodes already-ingested Belgian provisions with
`axiom-encode encode <citation> --apply`, pre-checks them with the same gate
battery the PR CI runs, opens one PR per module, and lets each PR auto-merge on
green.

This is the `rulespec-be` port of the `rulespec-us` dispatcher (structurally
following the `rulespec-uk` port). The encoder and the CI gates own
correctness. This system is **plumbing**: it never edits or invents generated
values. Its only judgement is *which* provisions to queue.

## Pieces

| File | Role |
| --- | --- |
| `bulk/worklist.yaml` | The durable queue. One entry per module. Committed. |
| `bulk/compute_matrix.py` | Turns the worklist into the CI job matrix; single source of truth for status selection. |
| `bulk/roots_for.py` | Maps an applied module path to `guard-generated --roots` (federal root `be`, plus a regional root `be-bru`/`be-dg`/`be-vlg`/`be-wal` when the module lives under one). |
| `.github/workflows/bulk-encode.yml` | The runner: dispatch → matrix → encode `--apply` → gate battery → PR + auto-merge. |

## Running it

Dispatch from the Actions tab (**Bulk encode → Run workflow**) or the CLI:

```bash
# Encode the pilot batch-A entries:
gh workflow run bulk-encode.yml -f batch=A -f limit=4 --repo TheAxiomFoundation/rulespec-be

# Encode up to 8 pending entries regardless of batch:
gh workflow run bulk-encode.yml -f limit=8 --repo TheAxiomFoundation/rulespec-be
```

The `schedule` trigger runs weekly and drains any remaining `pending` entries
with no human action. Parallelism is capped at 4 (`max-parallel`) to stay under
OpenAI rate limits; a top-level `concurrency` group serialises whole dispatches
so two runs never fight over the same `bulk/<slug>` branches.

### Secrets (repo Actions secrets on rulespec-be)

| Secret | Why |
| --- | --- |
| `OPENAI_API_KEY` | Headless `--backend openai` generation. |
| `AXIOM_ENCODE_APPLY_SIGNING_KEY` | Signs the apply manifest so `guard-generated` accepts the new files. Must match the key that signs manifests elsewhere. |
| `BULK_ENCODE_TOKEN` | A `repo`+`workflow`-scoped token used to push the branch and open the PR. **Required**: PRs opened by the default `GITHUB_TOKEN` do **not** trigger the `pull_request` event, so the required `validate / validate` check would never run and auto-merge would hang forever. This token makes the PR a real event that triggers CI. |

## Branch protection (required for the safety model)

Auto-merge is only safe when a required check gates the merge. Configure `main`
protection as: required check **`validate / validate`**, **`strict: false`**,
and enable repo-level "Allow auto-merge" — the same shape as `rulespec-uk`.
Without it, `gh pr merge --auto` can merge before or over a red validate. The
`validate / validate` roll-up already runs on every `rulespec-be` PR (federal
`be` + regional shards), so requiring it never deadlocks.

## What each job does

1. **dispatch** — installs PyYAML, runs `compute_matrix.py --status pending`
   (optionally `--batch`, `--limit`), and emits the matrix.
2. **encode** (one leg per module, ≤4 parallel):
   - Checks out the repo into a leaf dir named exactly `rulespec-be` (the
     `--apply` resolver requirement) using `BULK_ENCODE_TOKEN`.
   - Reads `.axiom/toolchain.toml` and checks out **the pinned** `axiom-encode`,
     `axiom-rules-engine`, and `axiom-corpus`, then builds the engine. Using the
     pinned encoder means generation and the downstream PR CI validate with the
     identical version — no version-skew surprises.
   - Runs `axiom-encode encode <citation> --apply`. The encoder resolves the
     citation's provision text from the pinned `axiom-corpus` checkout first
     (Supabase only as a fallback), so a committed-but-not-yet-published
     provision still resolves. `--apply` validates the main file, companion
     test, and direct dependents in a temporary overlay and writes nothing on
     failure (fail-closed), then installs the three artifacts:
     `be*/**/<sec>.yaml`, `<sec>.test.yaml`, and a signed
     `.axiom/encoding-manifests/**/<sec>.json` (root-level manifests, as in
     `rulespec-uk`).
   - Runs the gate battery in PR-CI order: `guard-generated` (manifest present),
     `validate --skip-reviewers`, `proof-validate`, then the companion `test`.
   - Opens `bulk/<slug>` with the manifest summary + gate output as the PR body,
     labels it `bulk-encode`, and runs `gh pr merge --auto --squash`.

The job **never** uses `--admin`, never bypasses a red check, and never merges
directly. The authoritative gate is the repository's required
`validate / validate` check on the PR.

### Difference from rulespec-us: no reverse index

`rulespec-us` maintains a committed provision → rules reverse index
(`tests/generate_reverse_index.py` → `.axiom/index/provisions_to_rules.json`)
and regenerates it per module. This repo carries no such artifact, so there is
**no index-regeneration step** here (same as `rulespec-uk`).

## Statuses

Set in `worklist.yaml`. The runner reads `pending`; humans/follow-ups own the rest.

| Status | Meaning |
| --- | --- |
| `pending` | Queued. The next dispatch may pick it up. |
| `in-progress` | A run is encoding it (transient). |
| `needs-fixtures` | Encoded + applied, but the companion fixtures hit the #1060 ceiling. The PR opens; auto-merge holds on the red required check until fixtures land. |
| `pr-open` | A PR exists and is set to auto-merge on green. |
| `merged` | The PR merged to main. Terminal success. |
| `failed` | Encode or a non-fixture gate failed. Needs human triage. Never auto-retried, never merged. |

Statuses are updated by committing to `worklist.yaml` (a reviewable diff), not by
silent CI mutation. `compute_matrix.py --set-status <citation> <status>` is a
local convenience.

## Readiness notes specific to rulespec-be

### 1. Corpus-publish lag — statute provisions not yet in `current_provisions`

Every worklist citation was verified to exist in the toolchain-pinned
`axiom-corpus` ref before listing (the encoder's local-first source), so the
runner will not invent numbers. However, the Belgian `be/statute/…` and
`be/regulation/…` provisions are **not yet published to the Supabase
`current_provisions` view** (0 rows there today; only `be/guidance/…` is
published). The bulk encoder resolves them locally from the pinned checkout, so
this does not block encoding, but a corpus publish should catch
`current_provisions` up before a full-scale drain. This is a corpus
(axiom-corpus) gap, not a dispatcher one.

### 2. Oracle-coverage pending lane — guarded, activates on toolchain bump

A freshly encoded output is `unmapped` until `axiom-oracles` gains a mapping.
The `oracle-coverage-pending` lane (`axiom-encode ≥ 0.2.1185`, encode#1076)
reclassifies a declared `unmapped` output to `pending_classification` so the
`validate / validate` oracle-coverage gate passes without a per-PR cross-repo
pin dance. The encoder pinned here **predates** that subcommand, so the
dispatcher **guards on its presence**: until `.axiom/toolchain.toml` is bumped
to include encode#1076, the sync step is skipped and a new output HOLDS at the
oracle-coverage gate — the expected, accountable held state, **never** a
weakened gate. The step activates automatically once the pin includes the
classification lane (encode#1076 + oracles#206, in flight). Do **not** hand-edit
`axiom-oracles` concept mappings to force a canary green.

## Extending the worklist

Append entries in the existing shape. `citation` is the corpus citation_path the
encoder resolves (`be/statute/<path>` or `be/regulation/<path>`, or a regional
`be-vlg/…`). Pick self-contained rate/duration/indemnity/definition sections;
**skip** cross-reference-heavy ones (encoder self-import, encode#1058) and any
known gate-held sections. Verify each candidate's exact citation_path resolves
in the pinned `axiom-corpus` ref (and, once the publish lag closes, in Supabase
`current_provisions`) before listing it.

## Full-scale bottlenecks and mitigations

When this dispatcher is promoted past the pilot, configure `main` protection as
above (`validate / validate`, `strict: false`, allow auto-merge). Turning
`strict` **off** avoids the rulespec-us merge-serialisation churn (each merge
re-queuing every other open PR's validation); bulk modules are independent
(disjoint files), so the up-to-date requirement buys nothing and costs a full
re-validation per merge. This repo has **no reverse index**, so the rulespec-us
per-PR index contention does not exist here.
