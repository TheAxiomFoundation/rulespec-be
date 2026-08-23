# Lane CB — Belgian child benefits, full composition

## State

Implementation is in progress on `ledger/child-benefits-full` from `origin/main` (`b105e2b`). The worktree began clean. No pushes, stashes, workflow edits, toolchain edits, waiver edits, or population-runner changes have been made.

## Binding basis

The lane is using the corpus checkout at `~/TheAxiomFoundation/_cape-prep/corpus-be-pin` and the signed release selected by the untouched `.axiom/toolchain.toml`, `be-rulespec-2026-07-10`. Proof excerpts in new RuleSpec modules will be literal substrings from that pinned corpus. Each companion case will assign every local input, including every false Boolean.

## Cohort routing

The pinned law does not define four parallel child-cohort switches:

| Region | Statutory 2025 route | Pinned evidence | Signed-release status |
|---|---|---|---|
| Flanders | Legacy LGAF amounts only when the child was born before 1 January 2019 **and** the entitlement conditions were satisfied on 31 December 2018. Otherwise the child uses the new schedule. The legacy rank is the rank assigned in the 2018 group and remains attached to the child; it is not recomputed from the current household. | Flemish Decree of 27 April 2018, Articles 210 §§1, 2 and 4 and 13: `be-vlg/statute/decreet/2018/04/27/2018040369/article/{210,13}`. Article 210 begins: “Een rechtgevend kind dat geboren is vóór 1 januari 2019 en voor wie het recht op kinderbijslag overeenkomstig de kinderbijslagreglementering is geopend op 31 december 2018, blijft recht geven op kinderbijslag overeenkomstig de kinderbijslagreglementering”. | Both required pages promoted. Article 228 is pinned but absent and is not needed. |
| Wallonia | Legacy LGAF amounts for a child born before 1 January 2020; the new Walloon schedule for a child born from that date. A newly filed claim does not change the legacy amount route. | Walloon Decree of 8 February 2018, Article 120, `be-wal/statute/decret/2018/02/08/2018201006/article/120`, plus AVIQ 2025 scale pages 1 and 4, `be-wal/guidance/aviq/family-benefits/amount-scale-2025-02/page-{1,4}`: “Les enfants nés avant 2020” / “Les enfants nés à partir de 2020”. | Required pages promoted. Article 3 is pinned but absent and is not needed. |
| Brussels | There is no per-child old/new cohort route. Article 39 compares the December-2019 LGAF total and ordinance total **per recipient**, caps the legacy total at its December-2019 level, prevents it from increasing, and permanently ends protection once the ordinance total catches up. Annual premiums are excluded from that comparison and Article 15 premiums are paid. Separately, through 2025, the ordinance schedule deducts €12.43 for a child born before 1 December 2019. | Brussels Ordinance of 25 April 2019, Article 39, `be-bru/statute/ordonnance/2019/04/25/2019012118/article/39`; promoted Iriscare scale blocks 3 and 15, `be-bru/guidance/iriscare/family-benefits/amount-scale-2025-02/block-{3,15}`. | Article 39 is pinned but absent from the signed release. Blocks 3 and 15 are promoted. |
| German-speaking Community | There is no child birth-cohort split. Article 111 protects a frozen December-2018 total for the same recipient group until the new aggregate is more favorable or the group/recipient changes. | Decree of 23 April 2018, Article 111 in `be-dg/statute/moniteur/decret-2018-04-23/2018202523/family-benefits/block-1`: “Dieser Betrag wird ... gezahlt, bis ... die Summe ... vorteilhafter ... [ist]” or the recipient grouping changes. | Promoted whole-law block is sufficient; the article-specific page is absent but unnecessary. |

The implementation therefore takes actual child date of birth, a Flemish 31-December-2018 entitlement fact, a frozen Flemish legacy rank, and explicit Brussels/DG household protection state. It does not manufacture a Brussels or DG child-cohort selector.

## Composition surface

The existing inventory contains federal LGAF rank, single-parent, social, age, annual-premium and indexation surfaces; current regional amount selectors; and the narrow household-level `child_benefit_base_2025` oracle slice. The latter duplicates selected 2025 parameters, treats one age as an age-derived cohort, assumes legacy rank 1, and has no heterogeneous-child relation. Its output `belgium_family_benefits_child_benefit_base_2025_annual_amount` is consumed by `be/policies/euromod_benefit_income_list.yaml`.

The new child-scoped composition and explicit household relation rollup are in progress. Monetary values already encoded in LGAF, regional, or applied-2025 rules will be imported; only missing applied values will receive new corpus proofs.

`applied_amounts_2025.yaml` now fills only the absent applied schedule cells: Flemish legacy ranks 2/3, legacy social/high-age tracks and current social bands; Walloon legacy ranks 2/3, social/premium cells and current large-family, lone-parent, older-child and orphan cells. Its parameter companion case checks 35 outputs and passes. It deliberately does not redeclare the Brussels, Flemish, Walloon or DG values already present in `child_benefit_base_2025.yaml`.

## EUROMOD `bch_be`

The installed `BE_2025` system has three active regional branches and no DG branch:

- Flanders (`drgn1=2`) pays old rank bases, old social and age supplements, or the new flat base and income/child-count social supplement. Both paths include the universal annual participation premium. The new-child flag is the age proxy `(2025 - dag) >= 2019`.
- Wallonia (`drgn1=3`) pays old rank, social, age and annual-premium components, or new base, income/child-count/lone-parent supplements and annual age component. Its new-child proxy is `(2025 - dag) >= 2020`.
- Brussels (`drgn1=1`) calculates an old and a new-equivalent household amount for pre-2020 children and pays their maximum; post-2020 children use the new schedule. It also derives the cohort from age, not date of birth.
- Child disability tiers and foster supplements are absent from active `bch_be`; orphan flags exist. DG is absent and returns zero, consistent with the existing disposition.

Because EUROMOD has no date-of-birth input here, the requested cross-product contains logically inconsistent cells: in 2025 an age-8, age-14, or age-17 child cannot enter a post-2019/2020 age-proxy branch. Those cells will remain visible and be marked as an EUROMOD age-proxy limitation rather than silently relabelled.

The official axiom-oracles subprocess adapter now runs successfully with the x86-64 connector. A known Flemish new-scheme age-0 case returned EUR2,184.80/year. The complete 432-cell cross-product then ran in one x64 worker and returned `bch_s`, `il_bch_means`, and `yem` for every case with zero errors. No more than one EUROMOD worker ran at a time. The final grid below will therefore distinguish connector results from the statutory RuleSpec computation, rather than treating XML inspection as oracle output.

## Release frontier

The signed-release manifest content SHA is `c1436c9f99882a819773bc2ccddf8c2a67e41efd24b0d0a408493ba5da39964a`.

Pinned but absent pages: Flemish Articles 222 and 228; Walloon Article 3; Brussels Articles 35, 39 and 40; DG article-specific Article 111. Article 228, Walloon Article 3 and DG article-specific Article 111 have promoted substitutes and are not used by the router. Flemish Article 222 is needed to connect legacy social supplements to Article 18 conditions. Brussels Article 39 has no promoted substitute for the comparison, cap, and permanent-loss mechanics, so rules whose proofs depend on those two pages are explicit release-frontier blocks. Iriscare blocks 3 and 15 prove the 2025 birth deduction and existence/cap of transitional old amounts, but not the complete Article 39 state machine.

There is also a release-projection collision for the Flemish guidance records `be-vlg/guidance/gpedia/family-benefits/amount-scale-2024-09/schedule-{1,3,4}`. The pinned official full-table records contain the verbatim €398.39 orphan, legacy social/high-age rows, and current social bands. The signed release resolves duplicate record IDs at those paths to later abbreviated records. The sibling-layout validator therefore stops at `Ungrounded generated numeric literal: 398.39` even though the parameter companion suite passes and the literal is verbatim in the pinned full-table record. This is recorded as a release-frontier failure, not waived or replaced with an uncited literal.

## Shortfall accounting and implied average

Pending the reconciled case grid.

## Suite registration

Pending; the final section will use the local axiom-oracles format associated with #508.

## Corrected `bch_s` ledger mechanism

Pending the composition-versus-unit-construction decomposition.

## Commands (verbatim)

```sh
sed -n '1,260p' ../../LEDGER_CAMPAIGN.md
wc -l ../../LEDGER_CAMPAIGN.md
sed -n '261,520p' ../../LEDGER_CAMPAIGN.md
git status --short --branch
git log -5 --oneline --decorate
gitnexus list
gitnexus status
gitnexus analyze .
rg --files be/statutes/family_benefits be-vlg be-wal be-bru be-dg | sort
rg -n "kind: data_relation|sum_where\\(" --glob '*.yaml' .
/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode test --root "$PWD" --axiom-rules-engine-path /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine be/statutes/family_benefits/child_benefit_base_2025.test.yaml --json
/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode test --root "$PWD" --axiom-rules-engine-path /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine be/statutes/family_benefits/cohort_routing_2025.test.yaml --json
/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode test --root "$PWD" --axiom-rules-engine-path /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine be/statutes/family_benefits/applied_amounts_2025.test.yaml --json
AXIOM_CORPUS_REPO=/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode validate /private/tmp/lane-cb-applied.jtSiUR/layout/rulespec-be/be/statutes/family_benefits/cohort_routing_2025.yaml --skip-reviewers --json
AXIOM_CORPUS_REPO=/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode validate /private/tmp/lane-cb-applied.jtSiUR/layout/rulespec-be/be/statutes/family_benefits/applied_amounts_2025.yaml --skip-reviewers --json
DOTNET_ROOT=/Users/maxghenis/.dotnet-x64 PYTHONNET_RUNTIME=coreclr .venv/bin/python - <<'PY'
from axiom_oracles.suites import load_suite
from axiom_oracles.adapters.euromod.runner import EuromodPlatformRunner
cases = load_suite('be-family-child-benefit-base')
case = next(c for c in cases if c.case_id == 'be-family-child-benefit-base-flanders-age-0')
runner = EuromodPlatformRunner(model_root='/Users/maxghenis/Downloads/EUROMOD_J2.0/EUROMOD_RELEASES_J2.0+', country='BE', system='BE_2025', dataset='BE_2024_c1_2015_03_e2', template_dataset='BE_training_data', python_executable='/Users/maxghenis/.venvs/axiom-euromod-x64/bin/python', dotnet_root='/Users/maxghenis/.dotnet-x64', timeout=900)
print(runner.run_cases([case], variables=['bch_s']))
PY
```

`gitnexus analyze .` could not register its index because the sandbox denied writing `~/.gitnexus/registry.json`; direct `rg`, source reading, and import/caller tracing are being used as the read-only fallback.

The early sibling-layout validation of the unchanged base-only module returned `ci_pass: false` solely for its pre-existing ungrounded numeric age-4 literal. All transition source paths already used by that module resolved in the signed release.

LANE CB IN PROGRESS
