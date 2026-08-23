# Lane CB progress

## State

- Branch: `ledger/child-benefits-full` at the `origin/main` baseline.
- Campaign rules loaded from `../../LEDGER_CAMPAIGN.md`.
- Status: per-child and household composition implementation in progress.

## Done

- Confirmed the worktree is clean and on the requested branch.
- Recorded the binding constraints: pinned-corpus verbatim proofs, exhaustive local-input tests, imported money amounts, person/child scope, pinned-engine tests, sibling-layout validation, per-case EUROMOD comparison, local commits only, and no toolchain/workflow/waiver edits.
- Inventoried the LGAF and four regional amount surfaces, their child-scoped inputs, annual components, and the narrow household-scoped 2025 oracle consumer.
- Resolved the pinned transition law: Flanders has a birth-date plus 2018-entitlement test and frozen ranks; Wallonia has a 2020 birth cutoff; Brussels and DG instead protect frozen recipient-level totals.
- Checked the signed-release frontier. Promoted evidence suffices for Flanders, Wallonia, and DG; Brussels Article 39 is pinned but absent from `be-rulespec-2026-07-10`.
- Traced EUROMOD `BE_2025/bch_be`: its cohort proxy is age-derived, its Brussels branch uses a household maximum, it includes annual premiums, and it has no DG branch.
- Ran the existing 35-case base-only companion suite successfully and probed its module through the sibling layout. The existing module has one pre-existing ungrounded age-4 literal.
- Added and verified the Date-based transition router: 12 companion cases pass and its sibling-layout validation reports `ci_pass: true`.
- Added a parameter-only applied-2025 layer for the missing Flemish and Walloon ranks, social bands, age tracks, and annual amounts. Its 35-output companion case passes.
- Confirmed a signed-release projection collision on the Flemish amount schedule: pinned full schedule rows are verbatim evidence, while the release resolves duplicate schedule IDs to abbreviated records that omit some old-system/social values.
- Re-established the official x64 EUROMOD connector through the axiom-oracles subprocess adapter: a known Flemish case returned EUR2,184.80/year with no error.
- Ran the full requested 432-cell regional/cohort/rank/age/income/single-parent cross-product through one x64 EUROMOD worker. Every cell returned `bch_s`, `il_bch_means`, and `yem`; there were zero connector errors.

## Next

1. Finish and test the imported applied-2025 component selectors.
2. Finish the explicit Household-to-Child relation, per-child annual output, household sum, and backward-compatible oracle output.
3. Reconcile all 432 successful EUROMOD results against the RuleSpec output, classify every residual, and quantify the composition/unit split.
4. Run all companion tests and full sibling-layout validation, then finish `LANE_CB_REPORT.md`.
