# Belgium documentary re-encoding queue

**Review metadata only. Do not merge as RuleSpec admission.** The queue at
`.axiom/be-documentary-reencoding-queue.v1.json` authorizes no generated
RuleSpec, `encode --apply`, signing dispatch, cleanup, merge, or admission. It
exists so the protected migration can be reviewed before the prerequisite
toolchain is frozen. Every candidate still requires fresh protected generation;
the review-head YAML is not an admissible output.

## Exact boundary

The queue binds RuleSpec-BE PR #127 at:

- lineage root `b105e2b3a3086ddd2de447d58a9b951346870dd1`, tree
  `4723792ae1752ffc33727ad8f34a280d526be59b`;
- review head `9aa9ee19d750fa0ac8aa7a02d9c1006c4240cb07`, tree
  `b08cfbf4b8c2b13a5298d0b5fb793c9c825e7fab`;
- 89 documentary candidates, 22 deletion groups, five excluded holds, and zero
  admissions, totaling the exact 116 base groups;
- candidate-set digest
  `141e8d261e3987634db0ca9d7ce8672bce0c962de4a52ab352ca0ca7887658d2`;
- deletion-set digest
  `4517f2f85075ee085e428ca1eef487546b1d0562a44b8f4cfd39a67befdad455`;
- hold-set digest
  `2af576c070365e580812917fbc39fd51d4d8a5837c19cc8811beaec71be80649`.

Set hashes use UTF-8 POSIX paths sorted byte-lexicographically, joined by one
NUL byte with no leading or trailing NUL, then SHA-256. Record-list hashes use
compact UTF-8 JSON with sorted object keys and no ASCII escaping. The invariant
tests independently reproduce both forms.

## Source readiness

The queue binds corpus release `be-rulespec-2026-07-10` at corpus commit
`644ee891c69b4632b0ce48d5432a6104df255571`, selector SHA-256
`6d451608c251bdbf85b6b94380399aeff55ad4df6bf6bcf415113b4c47dd2e16`,
and release content SHA-256
`c1436c9f99882a819773bc2ccddf8c2a67e41efd24b0d0a408493ba5da39964a`.
The release has 13 provision artifacts and 626 rows. All 89 candidate citations
resolve to exactly one nonempty row. There are 78 unique citations, each stored
with its corpus artifact, line, record ID, source path, and exact body SHA-256.

The current candidates contain zero `module.source_verification.source_sha256`
values. That is a readiness fact, not permission to hand-add hashes. Fresh
protected generation must let the corpus resolver stamp the expected body hash.

## Fail-closed sequence

The current cleanup planner correctly refuses the exact 22-group deletion:

```text
LegacyCleanupGitError: surviving base blob references a cleanup target: be-wal/statutes/family_benefits/amounts.yaml
```

Its contract-equivalent scan finds five surviving references:

- `be-wal/statutes/family_benefits/amounts.yaml`
- `data/coverage/euromod-be-coverage.json`
- `data/coverage/pilot-slice-coverage.json`
- `data/coverage/tax-benefit-source-map.json`
- `docs/ENCODING-GAPS.md`

Do not weaken the deletion-only receipt contract. The only safe sequence is:

1. Freeze and merge the compatible encoder and reusable-workflow prerequisite
   stack.
2. Land reviewed non-RuleSpec hygiene for the four data/documentation paths.
3. Freshly re-encode and sign
   `be-wal/statutes/family_benefits/amounts.yaml`. Its minimum write set is only
   that primary, companion, and deterministic manifest. Validate the direct
   eligibility dependent against the new target, and include the dependent
   group only if the trusted supervisor deterministically regenerates or
   rewrites it. Freeze the exact resulting write set as `F_cleanup`.
4. Re-run cleanup planning from `F_cleanup`. Continue only if it proves zero
   surviving references, then publish one signed atomic receipt covering the
   exact 22 groups. Freeze that result as `F1`.
5. Run the remaining 88 candidates in post-cleanup waves of
   `68 / 14 / 4 / 1 / 1`, freezing `F2` through `F6` between waves.

The transition graph combines desired documentary dependencies with three
required legacy disconnections. Employee contributions must be regenerated
before work bonus because the old employee-contributions module imported the
synthetic work bonus. Final tax and tax-liability pipeline must be regenerated
before movable withholding because both old consumers imported the withholding
module. The full transition layers, including the pre-cleanup Walloon amounts
candidate, are `69 / 14 / 4 / 1 / 1`.

Within a wave, the standard primary, companion test, and deterministic manifest
write sets are pairwise disjoint. A supplemental file, dependent rewrite,
waiver/toolchain change, or validation-expanded closure removes the affected
item from parallel dispatch and requires a new exact-base review.

## Earliest batches

No protected operation can run before the global prerequisites. Once they are
frozen, the first protected operation is the sequential Walloon family-benefit
amounts re-encoding above. After cleanup and the `F1` freeze, the first bounded
wave-one review tranche is:

- `be-vlg/regulations/employment/jobbonus.yaml`
- `be-vlg/statutes/education/school_allowance.yaml`
- `be-vlg/statutes/education/study_grant.yaml`
- `be/regulations/social_security/self_employed/contributions.yaml`
- `be/statutes/social_security/non_labour_income_contributions.yaml`

This tranche is a review unit, not a dispatch instruction.

## Item blockers

- `be-wal/statutes/education/study_allowance.yaml` waits for the
  French-Community-versus-Walloon namespace decision.
- `be-bru/statutes/family_benefits/selected_amount.yaml` waits for the Article
  7-plus-9 versus atomic-fold decision; Brussels eligibility waits on that
  result.
- `be-bru/statutes/disability/elderly_care_allowance.yaml` imports the federal
  disability module. The current protected `--required-import-rulespec-path`
  contract accepts only same-jurisdiction modules, so this item needs an
  explicit reviewed cross-jurisdiction composition contract.
- Guaranteed family benefits follows LGAF. The third-and-later BEF-to-EUR
  bridge must be omitted until Council Regulation 2866/98 is separately pinned.

The five human/source-boundary holds remain excluded from every queue step.

## Toolchain blockers and eventual command contract

The required final execution version is axiom-encode `0.2.1753`, but its exact
commit does not yet exist. PR #1566 (`0.2.1751`) is observed at
`410c81383826e9620ab969057631a9550d95e64b`; issues #1558 and #1557 must produce
the reviewed `0.2.1752` and `0.2.1753` commits. The compatible reusable workflow
commit for TheAxiomFoundation/.github PR #107 is also intentionally null; its
observed head `3e7976cc2aaab4e3e712285814e335493187a950` is not an execution pin.

The JSON records the cleanup CLI and re-encoding CLI skeleton. It is deliberately
non-executable while either final commit is null. For a candidate, the trusted
supervisor must:

- substitute the exact frozen corpus, rules-engine, clean wave-base, output,
  encoder, and workflow checkouts;
- supply the exact reviewed v3 `--review-contract-json` generated for that
  target;
- append one `--required-import-rulespec-path` for every entry in the
  candidate's same-jurisdiction required-import list;
- stop on any nonempty cross-jurisdiction dependency list;
- use an operation-scoped external apply signer; and
- reject `--apply-target-only` and `--skip-reviewers`.

No command in this review branch has been run with `--apply`; no signature or
receipt has been requested.

## Verification

From the exact review-head checkout:

```bash
python3 -m json.tool .axiom/be-documentary-reencoding-queue.v1.json >/dev/null
AXIOM_CORPUS_REPO=/exact/axiom-corpus/checkout \
  python3 -m pytest -q tests/test_documentary_reencoding_queue.py
AXIOM_CORPUS_REPO=/exact/axiom-corpus/checkout python3 -m pytest -q
```

The shared CI workflow supplies the pinned checkout at
`_axiom/axiom-corpus`. Local runs fail clearly unless that directory exists or
`AXIOM_CORPUS_REPO` names a checkout whose `HEAD` is the exact pinned commit.
The tests recompute every release-artifact hash, parse every recorded JSONL
line, and independently read every frozen RuleSpec primary and companion from
Git objects at the lineage root and review head.

Before any later execution, re-check the live PR and refs. If any base, head,
corpus artifact, encoder commit, workflow commit, waiver bytes, or candidate
record differs, regenerate and independently review the queue instead of
carrying signatures or readiness claims forward.

## Axiom concept boundary

Only concepts, events, statuses, rates, amounts, predicates, and relations
specifically present in public policy documents belong in atomic Axiom
RuleSpec. The queue authorizes no take-up mechanics, observed participation
flags, behavioral propensities, labor-supply elasticities, random assignment,
latent population variables, external-model/oracle outputs, or calibration
targets. A legal entitlement or payable amount is not observed receipt.
