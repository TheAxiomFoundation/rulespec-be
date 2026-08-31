# Belgium documentary migration boundary

**DO NOT MERGE.** This document specifies a non-admitted review boundary. It
does not authorize protected generation, signing dispatch, an applied manifest,
a cleanup receipt, or an admission claim.

## Frozen census

The census is frozen to exact `main`
`b105e2b3a3086ddd2de447d58a9b951346870dd1`:

| Classification | Primary-plus-adjacent-companion groups |
| --- | ---: |
| Documentary-core candidates requiring protected v5 re-encoding | 89 |
| Clearly synthetic or derived; delete with atomic cleanup receipts | 22 |
| Human/source-boundary holds; do not queue | 5 |
| Admitted | 0 |
| **Total** | **116** |

“Documentary-core candidate” means only that a path contains a documentary core
suitable for protected regeneration. It does not approve every current rule,
helper, selector, supplied override, import, or companion expectation. After the
22 deletions, the review tree contains 94 groups: the 89 candidates and five
holds. All current RuleSpec remains unadmitted.

## Complete deletion boundary

Each of these 22 primaries and its exact adjacent `<stem>.test.yaml` companion
is deleted. No surviving primary imports one of them.

1. `be/policies/euromod_benefit_income_list.yaml`
2. `be/policies/euromod_disposable_income_list.yaml`
3. `be/policies/euromod_tax_income_list.yaml`
4. `be/regulations/unemployment/pilot_oracle_pipeline.yaml`
5. `be/statutes/income_tax/individual/couple_pit_oracle_pipeline.yaml`
6. `be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml`
7. `be/statutes/income_tax/individual/pilot_worker_oracle_pipeline.yaml`
8. `be/statutes/income_tax/individual/self_employed_oracle_pipeline.yaml`
9. `be/statutes/education/study_allowance_routing.yaml`
10. `be/statutes/family_benefits/regional_routing.yaml`
11. `be/statutes/gift_tax/regional_routing.yaml`
12. `be/statutes/inheritance_tax/regional_routing.yaml`
13. `be/statutes/property_tax/regional_routing.yaml`
14. `be/statutes/vehicle_tax/regional_routing.yaml`
15. `be/statutes/family_benefits/birth_allowance.yaml`
16. `be/statutes/family_benefits/child_benefit_base_2025.yaml`
17. `be/statutes/property_tax/gross_withholding_and_supplied_centimes.yaml`
18. `be/regulations/unemployment/payable_amount.yaml`
19. `be/statutes/income_guarantee_for_elderly/payable_amount.yaml`
20. `be/statutes/social_integration/payable_amount.yaml`
21. `be/statutes/social_security/pension_health_insurance_article_191.yaml`
22. `be/statutes/social_security/pension_solidarity_article_68.yaml`

The first 17 were already in the reviewed deletion set. The superseding audit
moved unemployment `payable_amount` from replacement to deletion because it has
zero documentary proof atoms and only fed the deleted pilot. The last four are
additional whole-tree deletions: two unsourced/duplicative payable aggregates
and two redundant compatibility adapters.

## Immediate reviewed subset

The immediate 29-group review footprint is 11 protected-replacement candidates
plus the first 18 deletion groups above. The 11 candidates are:

- `be-vlg/regulations/employment/jobbonus.yaml`
- `be-vlg/statutes/education/school_allowance.yaml`
- `be-vlg/statutes/education/study_grant.yaml`
- `be-wal/statutes/education/study_allowance.yaml`
- `be-wal/statutes/family_benefits/amounts.yaml`
- `be/regulations/social_security/self_employed/contributions.yaml`
- `be/regulations/social_security/workers/employee_contributions.yaml`
- `be/regulations/social_security/workers/work_bonus.yaml`
- `be/statutes/income_tax/individual/final_tax.yaml`
- `be/statutes/income_tax/individual/tax_liability_pipeline.yaml`
- `be/statutes/social_security/non_labour_income_contributions.yaml`

Only the Flemish school-allowance and Walloon study-allowance files retain
post-review hand edits. Those edits remove exported internal selector-code
pseudo-concepts while preserving tested numeric branches. They are explicitly
non-admitted expected-output cleanup and still require protected regeneration.
No equivalent repair is expanded across the other 78 documentary candidates.

## Human/source-boundary holds

These five paths must not enter an encoder queue until a human decides the
documentary subset or split:

- `be/regulations/vat/rates.yaml` — public VAT rates are mixed with local enum
  tags, household mapping, and exemption-as-zero behavior.
- `be/statutes/property_tax/additional_centimes.yaml` — public authorization is
  mixed with an unproved supplied three-tier aggregation and denominator.
- `be/statutes/income_tax/individual/regional_surcharge.yaml` — supplied
  rates/totals and a synthetic work-bonus/childcare helper exceed the cited
  authority.
- `be/statutes/social_security/chapter_10_special_contributions.yaml` — the
  module bundles unrelated schemes, duplicates ordinary rates, annualizes
  generically, and passes through an unsupported amount.
- `be/statutes/social_security/workers/contribution_rates.yaml` — historical
  components are projected into 2026 without current-law proof, and composites
  collapse source-specific bases and caps.

## Admission prerequisites

This branch is not an admission path. Before any candidate can be admitted, all
of the following remain prerequisites:

- `axiom-encode#1557` must provide atomic cleanup receipts for deletion groups.
- `axiom-encode#1558` must establish the waiver/toolchain transition contract;
  this review binds the final waiver bytes directly and does not use a pending
  waiver.
- Any optional retired-inventory cleanup must occur before the relevant base is
  frozen.
- The generated-change guard must be enabled and required; it is disabled in
  the current workflow.
- The protected v5 apply/sign path and manifest location must be established.
- Exact corpus release, content hash, source objects, and per-source hashes must
  be pinned. Source-discovery run IDs alone are not immutable source pins.
- Coverage-registry toolchain references must be reconciled with the workflow
  pins.
- Each target must be regenerated and signed from its dependency layer’s frozen
  base with disjoint write sets. Wave 1 uses `F0`; integrated Wave 1 freezes
  `F1` for Wave 2, and later layers repeat that sequence. A base-changing merge
  invalidates outstanding signatures unless the protected tooling proves
  portability.

The repository currently binds corpus release `be-rulespec-2026-07-10`, corpus
content SHA-256
`c1436c9f99882a819773bc2ccddf8c2a67e41efd24b0d0a408493ba5da39964a`,
and final waiver-byte SHA-256
`904514a87f353e22767a3de186257675eacd99a496b71ca35052b9e9aa14543f`.
The workflow pins encoder `b9d376684cfb5e86202daa3451b8fc716703ed19`,
rules engine `05eac9d2f89dabe5c6673176260762cef3a58f47`, and corpus
repository `644ee891c69b4632b0ce48d5432a6104df255571`. Those pins do not
substitute for missing target-specific source pins or signed v5 manifests.

## Unresolved documentary decisions

Beyond the five holds, protected work must still resolve at least these source
boundaries:

- Decide whether the French-Community study-allowance surface belongs under the
  Walloon namespace.
- Admit LGAF before guaranteed family benefits; omit the third-and-later
  BEF-to-EUR bridge until Council Regulation 2866/98 is pinned.
- Decide whether Brussels `selected_amount.yaml` remains a directly proved
  Article 7-plus-9 path or is folded atomically into the Article 9 replacement.
- Resolve sparse proof coverage, parser gaps, mutable guidance/rate sources,
  supplied thresholds and overrides, and exact operative versions during
  protected regeneration—not through further hand-authored repairs here.
