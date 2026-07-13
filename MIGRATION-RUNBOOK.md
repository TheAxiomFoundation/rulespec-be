# Canonical-provenance migration gauntlet — runbook from nz#83

Every failure the first migration (rulespec-nz #83) hit, in order, with the
fix that landed. Future country migrations (SOUTHMOD et/zm/ug/gh/ng, us, uk,
be, ca) pre-flight ALL of these instead of rediscovering them serially.

## The wiring (per country repo)

1. `.axiom/toolchain.toml` → strict 3-key:
   - `axiom_corpus_release = "<cc>-rulespec-2026-07-10"` (immutable name; never "current")
   - `axiom_corpus_release_content_sha256` — from `corpus.release_objects` (Supabase), cross-verified by anonymous R2 fetch + canonical-JSON sha256 recompute. Verified table: ops/1101-migration/southmod-release-pins.md
   - `validation_waiver_set_sha256` — sha256 of the repo's `known-validation-gaps.yaml` AT HEAD
2. `repository-checks.yml` validate job → `TheAxiomFoundation/.github/.github/workflows/validate-rulespec.yml@<current main SHA>` with 4 dep-refs:
   - `axiom-encode-ref: 6cc3f8a59539e5abacbf351b913db98877cf6579`
   - `axiom-rules-engine-ref: de0efdc73b469132ee268e1c832e8f7148b91431` (pre-#103; post-#103 needs a coordinated workflow-flag change — see below)
   - `axiom-corpus-ref: <corpus main SHA carrying the release cut plan>`
   - `rulespec-us-ref: 0f291b367bf7e15555f9973112278c5cbf221653`
   - `validate-roots: auto`, `run-generated-guard: true`
3. If the repo has a hardening manifest recording the workflow pin
   (nz: `data/coverage/repo-hardening-source-readiness.json`,
   `ci_readiness.reusable_validation_workflow`), sync it — a test asserts
   manifest == workflow `uses:` pin.

## Pre-flight checklist (each bites as a distinct CI death otherwise)

- [ ] **Waiver schema (hard cut)**: `known-validation-gaps.yaml` document
      root must contain EXACTLY `validate_failures` (supervised audit
      strict-parses HEAD *and* PROTECTED BASE). If main still carries legacy
      keys (`missing_companion_tests`, `shape_issues`,
      `uncovered_derived_rules` — empty lists), land the deletion **on main
      first** (old pinned workflow ignores extras), then adopt in the
      migration PR + re-pin `validation_waiver_set_sha256`. (nz: #84.)
- [ ] **Waiver entries canonical**: every entry `active`/`pending` with
      fingerprint (`sha256:<64hex>`), owner (`@login`), issue (org issue
      URL), expires (future date); waived module paths must EXIST as regular
      files in the tree (`require_paths`).
- [ ] **Base toolchain**: first-migration PRs pass only on
      .github ≥ #26 (soft base parse). Any repo pinned < 4db0e754 will
      reject its own migration PR at the toolchain step.
- [ ] **Runner disk**: .github ≥ #27 frees ~20 GB at validate-job start.
- [ ] **sudo python trap**: .github ≥ #28 — provisioning must pass the
      resolved interpreter (`sudo "$(command -v python)"`), else the
      provision script copytrees /usr until the runner dies (annotation-only
      failure, no logs).
- [ ] **/opt trusted path**: .github ≥ #29 — supervisor refuses
      group-writable ancestors; hosted runners ship /opt g+w.
      → **Pin b62057d55345f739b71e3fd68616c09e0428c48f or later** (has all four).
- [ ] **Corpus main green**: ingest-manifest ancestry guard fails everywhere
      if any manifest on main records a squash-orphaned commit. RULE: PRs
      carrying signed ingest manifests must land via MERGE COMMIT (as #300),
      never squash (#303 broke main; fixed by #306 re-sign).
- [ ] **Ingest manifests in the PR** (if the migration carries any): must be
      signed from a clean root checkout (root=".", dirty_tracked=false,
      commit = ancestor of head) by the current signer. Re-sign procedure
      proven in corpus #301 (b5955d1c + f7c4a63f): surgical re-provenance +
      re-sign, applied-file sha256 set asserted unchanged. The guard reports
      ONE bad manifest per run — enumerate and fix ALL manifests locally
      (`find .axiom/ingest-manifests -name '*.json'` + root/dirty check).

## Verification gotchas

- r2.dev blocks python-urllib's default User-Agent (403). Use curl or set a
  UA when hand-verifying public fetches. CI's fetch step is unaffected.
- The release object URL: `https://pub-a8952f8657fc49fda358146ac001366c.r2.dev/releases/<name>/<content_sha256>.json`;
  hash = sha256 over canonical JSON (`sort_keys, separators=(",",":")`) of `.content`.
- GitHub kills runners silently on disk exhaustion: no step conclusions, no
  log blob, `BlobNotFound` on the logs API. The ONLY evidence is
  `gh api /repos/<r>/check-runs/<job-id>/annotations`.

## Endgame lessons (added 7/13 from nz#83's final rounds)

- **Test-input-assignment check masks its full scope.** CI reports the FIRST
  failing case per module; nz "4 failures" was really 32 cases across 9
  modules. Reproduce locally with the exact pure function
  (`find_test_input_assignment_issues(module_content, test_cases)`) — see
  scratchpad `nz-testinput-harness.py` — and iterate to zero before pushing.
  Same pattern works for any pure validate-pipeline check
  (`find_ungrounded_numeric_issues_scoped`, etc.).
- **Completing test inputs ripples into the waiver ratchet**: a waived module
  may start passing (stale-waiver hard error → remove, decrement) and another
  may re-fingerprint (combined outcome changed → pending-on-main → consume).
- **Waiver consumption needs a fresh PR base.** `pull_request` runs pin
  `base.sha` at trigger time; a waiver-only PR merged to main afterwards is
  invisible to a plain re-push (ratchet sees old base → "changed record").
  Fix: merge origin/main into the branch (refreshes the PR baseRefOid), keep
  `--ours` on known-validation-gaps.yaml + .axiom/toolchain.toml.
- **Promote ALL of main's pendings when consuming, not just yours** — main
  accumulates pendings from every waiver-only PR; a branch waiver file with
  any `pending` left violates the branch-side invariant (every entry exactly
  `{active}`), and rebuilding from main without re-applying branch-side
  removals resurrects deleted waivers.
- **Keep an explicit branch-side-removals ledger.** This trap bit twice on
  nz#83 even after being documented: any rebuild-from-main resurrects every
  waiver the branch had removed (main still carries them). Before ANY
  rebuild, `git log -p known-validation-gaps.yaml` on the branch and list the
  removed module paths; re-apply every removal after the rebuild. The
  supervised audit enumerates all stale waivers per run, so each missed
  removal costs a full ~35-min CI round.
- **Sub-paragraph coverage failures** ("has no rule citing it and no entry in
  module.deferred_outputs"): the honest fix is a `deferred_outputs` entry
  naming the uncovered sub-paragraph with an out-of-scope reason (et: 4 VAT
  categories), or encode it. Never a waiver.
- **Fabricated excerpts surface as "proof source evidence not found"** — fix
  by finding a VERBATIM supporting passage in the resolved provision text
  (ug: the ×12 annualization grounded by the handbook's own
  monthly-vs-annual-payment Q&A line), never by inventing text.
- **Main-first PRs must not touch `<cc>/` under an old pin with the
  generated guard on** ("Manual RuleSpec changes are not allowed") — and the
  manifest route is closed by design (the hard cut asserts
  `.axiom/encoding-manifests` empty). Keep main-first to the waiver file +
  tests/ (pin any known gap explicitly with a pointer to the migration PR,
  which carries the content change under `run-generated-guard: false`).
- **Rebuilding a branch from a worker's commit: `git checkout <sha> -- .`
  does NOT delete files the commit removed** (uk: resurrected 386 legacy
  manifests + a `programs/` root). Use empty-then-restore
  (`git rm -rq . && git checkout <sha> -- .`) and assert
  `git write-tree == <sha>^{tree}` before committing. Gate pushes on the
  full pytest exit code, not just the waiver-sha check.

## Engine coordination (post-#103, NOT yet merged)

Engine PR #103 (loader hard cut) REMOVES `--exclusive-rulespec-roots`
(hard-fails as unknown) and introduces required `--rulespec-root`. Merging it
requires, in one coordinated change: shared-workflow invocation update +
engine re-pin + revalidation of every migrated repo. Sol gate verdict
2026-07-12: DO-NOT-SHIP until its input-tamper claim is implemented or
descoped (see sol-audit-engine103.* and the PR comment). encode #1110 (E2E
non-skippable in CI) is queued behind it.

## Publish path (per country, after corpus cut plan merges)

Post-#304 (idempotent staging) the publisher converges pre-staged rows
safely; publish → copy to public bucket → activate → verify (200 + hash
recompute + shipped verifier). et/zm/ug/gh/ng/nz published and verified
2026-07-12. BE publish pends #301 merge; UK pends the #297-immutable port
(prompt ready: codex-uk-port-prompt.txt).

## Publish-side rules (added 7/12 after the SOUTHMOD provenance rejection)

- **Publish only from corpus default-branch commits.** The signed release
  object records `content.git.commit`; the workflow's provenance
  authentication hard-fails unless it is an ancestor of corpus main. The
  chip's et/zm/ug/gh objects were published from the #304 PR branch and were
  orphaned by its squash-merge → rejected in every consumer CI.
- **Release names are forever.** `activate_corpus_release` raises
  "immutable corpus release name already exists with another digest" on any
  same-name re-publish. Recovery from a bad publish = a NEW name (re-cut
  plan PR, e.g. *-rulespec-2026-07-12), never a rebind. Cut-plan-only PRs
  are squash-safe.
- **api.supabase.com bans python-urllib's TLS signature (CF 1010)** —
  activation must go through curl when the ban is hot; shim:
  scratchpad publish_via_curl.py (monkeypatches activate_corpus_release,
  preserves verify + response validation). Consider porting a curl/httpx
  fallback into publish_corpus.py.
- Verified provenance state 7/12: ng ad294991 ✓ / nz 66dcb07c ✓ /
  be 04c77ce8 ✓ on main; et/zm/ug/gh 7422c6ab orphaned → re-cut as 07-12
  (corpus #308).
