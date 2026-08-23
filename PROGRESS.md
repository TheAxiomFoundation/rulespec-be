# Lane CB progress

## State

- Branch: `ledger/child-benefits-full` at the `origin/main` baseline.
- Campaign rules loaded from `../../LEDGER_CAMPAIGN.md`.
- Status: transition routing implementation in progress.

## Done

- Confirmed the worktree is clean and on the requested branch.
- Recorded the binding constraints: pinned-corpus verbatim proofs, exhaustive local-input tests, imported money amounts, person/child scope, pinned-engine tests, sibling-layout validation, per-case EUROMOD comparison, local commits only, and no toolchain/workflow/waiver edits.
- Inventoried the LGAF and four regional amount surfaces, their child-scoped inputs, annual components, and the narrow household-scoped 2025 oracle consumer.
- Resolved the pinned transition law: Flanders has a birth-date plus 2018-entitlement test and frozen ranks; Wallonia has a 2020 birth cutoff; Brussels and DG instead protect frozen recipient-level totals.
- Checked the signed-release frontier. Promoted evidence suffices for Flanders, Wallonia, and DG; Brussels Article 39 is pinned but absent from `be-rulespec-2026-07-10`.
- Traced EUROMOD `BE_2025/bch_be`: its cohort proxy is age-derived, its Brussels branch uses a household maximum, it includes annual premiums, and it has no DG branch.
- Ran the existing 35-case base-only companion suite successfully and probed its module through the sibling layout. The existing module has one pre-existing ungrounded age-4 literal.

## Next

1. Encode and test the child-level transition indicators and recipient-level protection-state inputs.
2. Add applied-2025 component selectors by importing existing amount parameters and adding only corpus-proven missing applied values.
3. Add the explicit Household-to-Child relation, per-child annual output, household sum, and backward-compatible oracle output.
4. Run the EUROMOD case-grid harness, classify the age-proxy and statutory residuals, and quantify the composition/unit split.
5. Run all companion tests and full sibling-layout validation, then finish `LANE_CB_REPORT.md`.
