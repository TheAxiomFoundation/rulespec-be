# Belgium documentary-boundary hard cut

## State

Hard cut applied and repository validation complete on
`fix/documentary-concept-hard-cut`; self-review and remote handoff remain. The
worktree was clean at
the start of this review at `9f86c5eb9ab5471e8011d8bdf991863d8ec2ca73`.
The cached `origin/main` is
`b105e2b3a3086ddd2de447d58a9b951346870dd1`; network DNS currently prevents a
fresh fetch or live inspection of draft PR 127.

The audited immediate scope is exactly 12 retained protected replacements and
17 exact legacy deletion groups after deleting the two synthetic federal
family-benefit aggregates. This branch remains non-admitted: no encoder
manifest, receipt, signing dispatch, or merge is authorized.

## Done

- Read the applicable parent and repository instructions, README, layout
  contract, toolchain pin, and repository workflow.
- Confirmed the initial worktree and cached tracking branch were clean and
  aligned at `9f86c5e`.
- Inspected the five-commit diff from cached `origin/main`, including all
  changed-path inventory, retained replacement groups, deletion groups,
  coverage/docs/tests, and the two synthetic family-benefit modules.
- Verified that `birth_allowance.yaml` and
  `child_benefit_base_2025.yaml` combine citations from `be-bru`, `be-vlg`,
  `be-wal`, and `be-dg`, while the preserved regional modules remain separate
  jurisdiction surfaces.
- Located every exact stale path/id reference: four aggregate/companion files,
  two validation waivers, one encoding-gap section, three Walloon prose
  references, and the 15-group deletion guard that must become 17.
- Attempted a fresh origin fetch and live PR 127 query; both are blocked by DNS.
  No PR facts have been inferred from unavailable remote state.
- Committed the initial progress journal and its repository-layout allowance as
  `e41aa90` (`Start documentary hard-cut progress journal`).
- Deleted the two synthetic federal family-benefit modules and their companion
  tests, removed both obsolete validation waivers and all exact stale prose,
  and expanded the exact protected deletion inventory from 15 to 17 groups.
- Recomputed the waiver-set content hash after removing those two entries and
  updated the toolchain binding to
  `73dd1ac66619fc918e66d596a8b5ca8945072923c86482c6020a543404bb4514`.
- Added a regression check that family-benefit imports and citations stay
  within their federal, Brussels, Flemish, Walloon, or German-speaking
  Community documentary jurisdiction.
- Confirmed the branch diff now contains exactly 12 retained protected
  replacement modules and 17 deleted production-module/companion-test groups.
- Parsed all 203 remaining tracked YAML files, verified the waiver bytes match
  the updated toolchain hash, passed both new boundary tests, passed focused
  Ruff lint, and found no whitespace errors in the worktree diff.
- Passed the complete repository suite: 33 tests in 116.01 seconds. Full Ruff
  lint and the manual repository-layout diagnostic also pass; the latter
  checked 236 tracked paths with zero schema problems.
- Ran the local unsigned source-staleness diagnostic. It passed and reported
  that no module pins `source_sha256`, so there was no stale pin to compare.
- Ran local money-atom proof validation across all 99 remaining atomic modules:
  zero missing proof atoms across 540 monetary obligations, with no ratchet
  allowance.
- Ran the unsigned generated-file guard as a diagnostic. It failed with exactly
  52 missing legacy-manifest issues, as expected for the changed and deleted
  files. No manifest or receipt was created.
- Ran local standalone validation for all 12 retained replacements. Every file
  reached the same non-content failure because the available rules engine
  rejects this checkout's multi-root configuration. The local encoder, engine,
  and corpus revisions (`427edd81`, `8430cdea`, and `2794b544`) do not match the
  workflow pins (`b9d37668`, `05eac9d2`, and `644ee891`), so this is diagnostic
  only and cannot establish admission.
- Ran the local base proof-tree diagnostic across all 99 atomic modules. The
  older encoder rejected independently operative secondary proof sources in 61
  modules; this is likewise a known contract mismatch with the pinned protected
  path, not admission evidence. The money-only gate and repository source-path
  tests pass.
- Confirmed `.axiom/encoding-manifests` is absent and the branch introduces no
  manifest path; full `git diff --check origin/main...HEAD` passes.

## Next

- Self-review the full branch diff against the public-document boundary, write
  the final report file, commit each coherent step, then retry live PR
  verification, push, and PR-body update. Do not merge or dispatch signing.
