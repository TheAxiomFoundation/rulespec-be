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

`child_benefit_composition_2025.yaml` is the new full surface. It imports all monetary cells; it contains no new money literal. Its `Child` output `belgium_child_benefit_composition_selected_annual_amount` composes the selected monthly base, frozen legacy rank where applicable, monthly age track, income-band social amount, separately exposed single-parent increment, orphan/disability/foster status amount, and annual school/age premium. The explicit `belgium_child_benefit_composition_beneficiary_child_of_household(Household, Child)` relation rolls those records into `belgium_child_benefit_composition_household_selected_annual_amount` with `sum_where`.

Brussels and DG protection is deliberately applied after child aggregation. The household inputs carry protection-active state and the frozen December-2019/December-2018 recipient amount; current annual premiums are added only after that protected monthly amount is selected. A separate `belgium_child_benefit_composition_household_euromod_comparator_annual_amount` reproduces EUROMOD's Brussels reconstructed-old-versus-ordinance maximum for diagnostics. It is not substituted for Article 39's historical-state rule.

The child inputs include beneficiary status, date of birth through the imported router, current age, age before 31 December, frozen legacy rank, beneficiary count, annual household income, single-parent status, higher-education status, and the cadastral gate. Orphan, full-orphan, disability/tier, foster, and Flemish mixed-cohort flags are explicit and are assigned `false` in ordinary companion fixtures. Existing regional status surfaces are imported where they exist; their amount verification is outside this lane as directed.

`applied_amounts_2025.yaml` fills only the absent applied schedule cells: Flemish legacy ranks 2/3, legacy social/high-age tracks and current social bands; Walloon legacy ranks 2/3, social/premium cells and current large-family, lone-parent, older-child and orphan cells. Its parameter companion case checks 35 outputs and passes. It deliberately does not redeclare the Brussels, Flemish, Walloon or DG values already present in `child_benefit_base_2025.yaml`.

The old `belgium_family_benefits_child_benefit_base_2025_annual_amount` remains unchanged and working for existing callers. The new full household output is the one-output oracle/population surface requested here; population-runner rewiring remains with the V5/ledger lane.

## EUROMOD `bch_be`

The installed `BE_2025` system has three active regional branches and no DG branch:

- Flanders (`drgn1=2`): `DefConst` F78; age-proxy cohort F81--82 (`2025-dag>=2019`); old base F91, social F97/F99, mixed-family legacy middle condition F101, age F104/F106, and premium F108; new base F116, social F118/F120/F122, premium F124; total F131.
- Wallonia (`drgn1=3`): `DefConst` F132; cohort F134--135 (`2025-dag>=2020`); old base F143, social F149/F151, age F154/F156, and premium F158/F160; new base F183, Article 13 F185/F193, annual age F204; total F207. F185/F193 has no old-child guard, so EUROMOD also adds the new Article 13 supplement to old children. In the official synthetic one-parent records, its direct `IsLoneParentOfDepChild#5` branch does not fire, so the new-scheme lone-parent increment is absent.
- Brussels (`drgn1=1`): `DefConst` F208; cohort F210--211 (`2025-dag>=2020`); old base/social/age and current premium F219/F225/F228/F231/F233/F239; pre-2020 ordinance F266/F273/F275/F277/F280; post-2020 F286/F290/F292/F294/F296; final household maximum F302. An employed couple needs the F226 unemployment/pension condition for old LGAF social support; the lone-parent path uses F224--225.
- Child disability tiers and foster supplements are absent from active `bch_be`; orphan flags exist. DG is absent and returns zero, consistent with the existing disposition.

Because EUROMOD has no date-of-birth input here, the requested cross-product contains logically inconsistent cells: in 2025 an age-8, age-14, or age-17 child cannot enter a post-2019/2020 age-proxy branch. Those cells will remain visible and be marked as an EUROMOD age-proxy limitation rather than silently relabelled.

The official axiom-oracles subprocess adapter runs successfully with the x86-64 connector. A known Flemish new-scheme age-0 case returned EUR2,184.80/year. The final calibrated 432-cell cross-product ran in one x64 worker and returned `bch_s`, `il_bch_means`, and `yem` for every case with zero errors. The independently derived EUROMOD branch formula matched the official result to the cent in all 432 rows. No more than one EUROMOD worker ran at a time.

Low/middle/high use nominal gross employment incomes of EUR30,000/EUR45,000/EUR90,000. The connector returned `il_bch_means` ranges EUR30,422.76--30,469.46, EUR40,961.44--41,146.95, and EUR81,797.92--82,202.78; these are the values the #508-style bridge must feed to the RuleSpec household-income input. The high gross was calibrated upward from EUR80,000 because the connector's means construct otherwise left a three-child Flemish household below the EUR75,593.05 ceiling.

## Case-grid verification

The grid is `region {bru,vlg,wal} x requested cohort {pre,post} x household child count/ranks {1,2,3} x age {3,8,14,17} x income {low,middle,high} x single parent {no,yes}`. An `rN` household has N same-age children with legacy ranks 1 through N. All status, cadastral-excess, childcare, and preschool flags are false. Monthly age components use current age; annual-premium bands use age on the preceding 31 December (`max(age-1,0)`).

Of 432 cells, 216 are temporally possible under the requested cohort and age. Among those, 174 match the statutory composition to the cent: Flanders 72/72 and Brussels 72/72, Wallonia 30/72. The 42 valid Walloon differences are fully dispositioned:

- Old-cohort Article 13 cumulation adds EUR57,747.60 in EUROMOD across valid rows (EUR38,944.80 low band and EUR18,802.80 middle band), contrary to Article 128 non-cumulation.
- New-cohort age-3 lone-parent increments are absent from the official synthetic runs, subtracting EUR2,685.60 from EUROMOD (EUR1,790.64 low and EUR894.96 middle).
- Net valid Walloon `EUROMOD - statute` is therefore +EUR55,062.00. High valid rows and post-cohort couple low/middle rows match.

The other 216 rows are preserved as requested but marked `EUROMOD age-proxy cohort routing`: age 3 necessarily routes post-reform in EUROMOD, while ages 8/14/17 necessarily route pre-reform. They are not counted as unexplained numeric failures. Brussels pre-reform rows instantiate a protection state consistent with the reconstructed LGAF/current comparison for the oracle fixture; the production statutory output still requires the explicit frozen recipient amount and protection-active input.

The full expected-versus-official-computed table follows below.

## Full case-grid table

The official x64 adapter returned 432/432 cases with zero errors. `EU actual` equals the independently derived EUROMOD formula to the cent in every row.

| case_id | reg | req | EU route | valid | n | age | band | SP | statute expected | EU actual | EU-statute | statute branch | mechanism |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| cb-bru-pre-r1-a3-low-sp0 | bru | pre | post | no | 1 | 3 | low | no | 2710.71 | 2859.87 | 149.16 | bru-pre-household-max-new | EUROMOD age-proxy cohort routing |
| cb-bru-pre-r1-a3-low-sp1 | bru | pre | post | no | 1 | 3 | low | yes | 2710.71 | 2859.87 | 149.16 | bru-pre-household-max-new | EUROMOD age-proxy cohort routing |
| cb-bru-pre-r1-a3-middle-sp0 | bru | pre | post | no | 1 | 3 | middle | no | 2113.83 | 2262.99 | 149.16 | bru-pre-household-max-new | EUROMOD age-proxy cohort routing |
| cb-bru-pre-r1-a3-middle-sp1 | bru | pre | post | no | 1 | 3 | middle | yes | 2113.83 | 2262.99 | 149.16 | bru-pre-household-max-new | EUROMOD age-proxy cohort routing |
| cb-bru-pre-r1-a3-high-sp0 | bru | pre | post | no | 1 | 3 | high | no | 2113.83 | 2262.99 | 149.16 | bru-pre-household-max-new | EUROMOD age-proxy cohort routing |
| cb-bru-pre-r1-a3-high-sp1 | bru | pre | post | no | 1 | 3 | high | yes | 2113.83 | 2262.99 | 149.16 | bru-pre-household-max-new | EUROMOD age-proxy cohort routing |
| cb-bru-pre-r1-a8-low-sp0 | bru | pre | pre | yes | 1 | 8 | low | no | 2723.14 | 2723.14 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance); Brussels employed couple is ineligible for old LGAF social supplement |
| cb-bru-pre-r1-a8-low-sp1 | bru | pre | pre | yes | 1 | 8 | low | yes | 2723.14 | 2723.14 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r1-a8-middle-sp0 | bru | pre | pre | yes | 1 | 8 | middle | no | 2126.26 | 2126.26 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r1-a8-middle-sp1 | bru | pre | pre | yes | 1 | 8 | middle | yes | 2126.26 | 2126.26 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r1-a8-high-sp0 | bru | pre | pre | yes | 1 | 8 | high | no | 2126.26 | 2126.26 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r1-a8-high-sp1 | bru | pre | pre | yes | 1 | 8 | high | yes | 2126.26 | 2126.26 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r1-a14-low-sp0 | bru | pre | pre | yes | 1 | 14 | low | no | 3046.33 | 3046.33 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance); Brussels employed couple is ineligible for old LGAF social supplement |
| cb-bru-pre-r1-a14-low-sp1 | bru | pre | pre | yes | 1 | 14 | low | yes | 3046.33 | 3046.33 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r1-a14-middle-sp0 | bru | pre | pre | yes | 1 | 14 | middle | no | 2151.13 | 2151.13 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r1-a14-middle-sp1 | bru | pre | pre | yes | 1 | 14 | middle | yes | 2151.13 | 2151.13 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r1-a14-high-sp0 | bru | pre | pre | yes | 1 | 14 | high | no | 2151.13 | 2151.13 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r1-a14-high-sp1 | bru | pre | pre | yes | 1 | 14 | high | yes | 2151.13 | 2151.13 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r1-a17-low-sp0 | bru | pre | pre | yes | 1 | 17 | low | no | 3046.33 | 3046.33 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance); Brussels employed couple is ineligible for old LGAF social supplement |
| cb-bru-pre-r1-a17-low-sp1 | bru | pre | pre | yes | 1 | 17 | low | yes | 3046.33 | 3046.33 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r1-a17-middle-sp0 | bru | pre | pre | yes | 1 | 17 | middle | no | 2151.13 | 2151.13 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r1-a17-middle-sp1 | bru | pre | pre | yes | 1 | 17 | middle | yes | 2151.13 | 2151.13 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r1-a17-high-sp0 | bru | pre | pre | yes | 1 | 17 | high | no | 2151.13 | 2151.13 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r1-a17-high-sp1 | bru | pre | pre | yes | 1 | 17 | high | yes | 2151.13 | 2151.13 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r2-a3-low-sp0 | bru | pre | post | no | 2 | 3 | low | no | 6316.62 | 6614.94 | 298.32 | bru-pre-household-max-new | EUROMOD age-proxy cohort routing |
| cb-bru-pre-r2-a3-low-sp1 | bru | pre | post | no | 2 | 3 | low | yes | 6614.94 | 6913.26 | 298.32 | bru-pre-household-max-new | EUROMOD age-proxy cohort routing |
| cb-bru-pre-r2-a3-middle-sp0 | bru | pre | post | no | 2 | 3 | middle | no | 4973.82 | 5272.14 | 298.32 | bru-pre-household-max-new | EUROMOD age-proxy cohort routing |
| cb-bru-pre-r2-a3-middle-sp1 | bru | pre | post | no | 2 | 3 | middle | yes | 4973.82 | 5272.14 | 298.32 | bru-pre-household-max-new | EUROMOD age-proxy cohort routing |
| cb-bru-pre-r2-a3-high-sp0 | bru | pre | post | no | 2 | 3 | high | no | 4227.66 | 4525.98 | 298.32 | bru-pre-household-max-new | EUROMOD age-proxy cohort routing |
| cb-bru-pre-r2-a3-high-sp1 | bru | pre | post | no | 2 | 3 | high | yes | 4227.66 | 4525.98 | 298.32 | bru-pre-household-max-new | EUROMOD age-proxy cohort routing |
| cb-bru-pre-r2-a8-low-sp0 | bru | pre | pre | yes | 2 | 8 | low | no | 6341.48 | 6341.48 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance); Brussels employed couple is ineligible for old LGAF social supplement |
| cb-bru-pre-r2-a8-low-sp1 | bru | pre | pre | yes | 2 | 8 | low | yes | 6639.80 | 6639.80 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r2-a8-middle-sp0 | bru | pre | pre | yes | 2 | 8 | middle | no | 4998.68 | 4998.68 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r2-a8-middle-sp1 | bru | pre | pre | yes | 2 | 8 | middle | yes | 4998.68 | 4998.68 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r2-a8-high-sp0 | bru | pre | pre | yes | 2 | 8 | high | no | 4894.52 | 4894.52 | 0.00 | bru-pre-household-max-old | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r2-a8-high-sp1 | bru | pre | pre | yes | 2 | 8 | high | yes | 4894.52 | 4894.52 | 0.00 | bru-pre-household-max-old | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r2-a14-low-sp0 | bru | pre | pre | yes | 2 | 14 | low | no | 6987.86 | 6987.86 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance); Brussels employed couple is ineligible for old LGAF social supplement |
| cb-bru-pre-r2-a14-low-sp1 | bru | pre | pre | yes | 2 | 14 | low | yes | 7286.18 | 7286.18 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r2-a14-middle-sp0 | bru | pre | pre | yes | 2 | 14 | middle | no | 5346.74 | 5346.74 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r2-a14-middle-sp1 | bru | pre | pre | yes | 2 | 14 | middle | yes | 5346.74 | 5346.74 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r2-a14-high-sp0 | bru | pre | pre | yes | 2 | 14 | high | no | 5336.66 | 5336.66 | 0.00 | bru-pre-household-max-old | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r2-a14-high-sp1 | bru | pre | pre | yes | 2 | 14 | high | yes | 5336.66 | 5336.66 | 0.00 | bru-pre-household-max-old | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r2-a17-low-sp0 | bru | pre | pre | yes | 2 | 17 | low | no | 6987.86 | 6987.86 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance); Brussels employed couple is ineligible for old LGAF social supplement |
| cb-bru-pre-r2-a17-low-sp1 | bru | pre | pre | yes | 2 | 17 | low | yes | 7286.18 | 7286.18 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r2-a17-middle-sp0 | bru | pre | pre | yes | 2 | 17 | middle | no | 5346.74 | 5346.74 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r2-a17-middle-sp1 | bru | pre | pre | yes | 2 | 17 | middle | yes | 5346.74 | 5346.74 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r2-a17-high-sp0 | bru | pre | pre | yes | 2 | 17 | high | no | 5336.66 | 5336.66 | 0.00 | bru-pre-household-max-old | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r2-a17-high-sp1 | bru | pre | pre | yes | 2 | 17 | high | yes | 5336.66 | 5336.66 | 0.00 | bru-pre-household-max-old | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r3-a3-low-sp0 | bru | pre | post | no | 3 | 3 | low | no | 11265.21 | 11712.69 | 447.48 | bru-pre-household-max-new | EUROMOD age-proxy cohort routing |
| cb-bru-pre-r3-a3-low-sp1 | bru | pre | post | no | 3 | 3 | low | yes | 12160.53 | 12608.01 | 447.48 | bru-pre-household-max-new | EUROMOD age-proxy cohort routing |
| cb-bru-pre-r3-a3-middle-sp0 | bru | pre | post | no | 3 | 3 | middle | no | 9564.21 | 10011.69 | 447.48 | bru-pre-household-max-new | EUROMOD age-proxy cohort routing |
| cb-bru-pre-r3-a3-middle-sp1 | bru | pre | post | no | 3 | 3 | middle | yes | 9564.21 | 10011.69 | 447.48 | bru-pre-household-max-new | EUROMOD age-proxy cohort routing |
| cb-bru-pre-r3-a3-high-sp0 | bru | pre | post | no | 3 | 3 | high | no | 8097.93 | 6788.97 | -1308.96 | bru-pre-household-max-old | EUROMOD age-proxy cohort routing |
| cb-bru-pre-r3-a3-high-sp1 | bru | pre | post | no | 3 | 3 | high | yes | 8097.93 | 6788.97 | -1308.96 | bru-pre-household-max-old | EUROMOD age-proxy cohort routing |
| cb-bru-pre-r3-a8-low-sp0 | bru | pre | pre | yes | 3 | 8 | low | no | 11302.50 | 11302.50 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance); Brussels employed couple is ineligible for old LGAF social supplement |
| cb-bru-pre-r3-a8-low-sp1 | bru | pre | pre | yes | 3 | 8 | low | yes | 12197.82 | 12197.82 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r3-a8-middle-sp0 | bru | pre | pre | yes | 3 | 8 | middle | no | 9601.50 | 9601.50 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r3-a8-middle-sp1 | bru | pre | pre | yes | 3 | 8 | middle | yes | 9601.50 | 9601.50 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r3-a8-high-sp0 | bru | pre | pre | yes | 3 | 8 | high | no | 9377.34 | 9377.34 | 0.00 | bru-pre-household-max-old | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r3-a8-high-sp1 | bru | pre | pre | yes | 3 | 8 | high | yes | 9377.34 | 9377.34 | 0.00 | bru-pre-household-max-old | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r3-a14-low-sp0 | bru | pre | pre | yes | 3 | 14 | low | no | 12272.43 | 12272.43 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance); Brussels employed couple is ineligible for old LGAF social supplement |
| cb-bru-pre-r3-a14-low-sp1 | bru | pre | pre | yes | 3 | 14 | low | yes | 13167.75 | 13167.75 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r3-a14-middle-sp0 | bru | pre | pre | yes | 3 | 14 | middle | no | 10123.59 | 10123.59 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r3-a14-middle-sp1 | bru | pre | pre | yes | 3 | 14 | middle | yes | 10123.59 | 10123.59 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r3-a14-high-sp0 | bru | pre | pre | yes | 3 | 14 | high | no | 10106.55 | 10106.55 | 0.00 | bru-pre-household-max-old | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r3-a14-high-sp1 | bru | pre | pre | yes | 3 | 14 | high | yes | 10106.55 | 10106.55 | 0.00 | bru-pre-household-max-old | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r3-a17-low-sp0 | bru | pre | pre | yes | 3 | 17 | low | no | 12272.43 | 12272.43 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance); Brussels employed couple is ineligible for old LGAF social supplement |
| cb-bru-pre-r3-a17-low-sp1 | bru | pre | pre | yes | 3 | 17 | low | yes | 13167.75 | 13167.75 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r3-a17-middle-sp0 | bru | pre | pre | yes | 3 | 17 | middle | no | 10123.59 | 10123.59 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r3-a17-middle-sp1 | bru | pre | pre | yes | 3 | 17 | middle | yes | 10123.59 | 10123.59 | 0.00 | bru-pre-household-max-new | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r3-a17-high-sp0 | bru | pre | pre | yes | 3 | 17 | high | no | 10106.55 | 10106.55 | 0.00 | bru-pre-household-max-old | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-pre-r3-a17-high-sp1 | bru | pre | pre | yes | 3 | 17 | high | yes | 10106.55 | 10106.55 | 0.00 | bru-pre-household-max-old | Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r1-a3-low-sp0 | bru | post | post | yes | 1 | 3 | low | no | 2859.87 | 2859.87 | 0.00 | bru-new-post | matched |
| cb-bru-post-r1-a3-low-sp1 | bru | post | post | yes | 1 | 3 | low | yes | 2859.87 | 2859.87 | 0.00 | bru-new-post | matched |
| cb-bru-post-r1-a3-middle-sp0 | bru | post | post | yes | 1 | 3 | middle | no | 2262.99 | 2262.99 | 0.00 | bru-new-post | matched |
| cb-bru-post-r1-a3-middle-sp1 | bru | post | post | yes | 1 | 3 | middle | yes | 2262.99 | 2262.99 | 0.00 | bru-new-post | matched |
| cb-bru-post-r1-a3-high-sp0 | bru | post | post | yes | 1 | 3 | high | no | 2262.99 | 2262.99 | 0.00 | bru-new-post | matched |
| cb-bru-post-r1-a3-high-sp1 | bru | post | post | yes | 1 | 3 | high | yes | 2262.99 | 2262.99 | 0.00 | bru-new-post | matched |
| cb-bru-post-r1-a8-low-sp0 | bru | post | pre | no | 1 | 8 | low | no | 2872.30 | 2723.14 | -149.16 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance); Brussels employed couple is ineligible for old LGAF social supplement |
| cb-bru-post-r1-a8-low-sp1 | bru | post | pre | no | 1 | 8 | low | yes | 2872.30 | 2723.14 | -149.16 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r1-a8-middle-sp0 | bru | post | pre | no | 1 | 8 | middle | no | 2275.42 | 2126.26 | -149.16 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r1-a8-middle-sp1 | bru | post | pre | no | 1 | 8 | middle | yes | 2275.42 | 2126.26 | -149.16 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r1-a8-high-sp0 | bru | post | pre | no | 1 | 8 | high | no | 2275.42 | 2126.26 | -149.16 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r1-a8-high-sp1 | bru | post | pre | no | 1 | 8 | high | yes | 2275.42 | 2126.26 | -149.16 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r1-a14-low-sp0 | bru | post | pre | no | 1 | 14 | low | no | 3195.49 | 3046.33 | -149.16 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance); Brussels employed couple is ineligible for old LGAF social supplement |
| cb-bru-post-r1-a14-low-sp1 | bru | post | pre | no | 1 | 14 | low | yes | 3195.49 | 3046.33 | -149.16 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r1-a14-middle-sp0 | bru | post | pre | no | 1 | 14 | middle | no | 2300.29 | 2151.13 | -149.16 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r1-a14-middle-sp1 | bru | post | pre | no | 1 | 14 | middle | yes | 2300.29 | 2151.13 | -149.16 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r1-a14-high-sp0 | bru | post | pre | no | 1 | 14 | high | no | 2300.29 | 2151.13 | -149.16 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r1-a14-high-sp1 | bru | post | pre | no | 1 | 14 | high | yes | 2300.29 | 2151.13 | -149.16 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r1-a17-low-sp0 | bru | post | pre | no | 1 | 17 | low | no | 3195.49 | 3046.33 | -149.16 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance); Brussels employed couple is ineligible for old LGAF social supplement |
| cb-bru-post-r1-a17-low-sp1 | bru | post | pre | no | 1 | 17 | low | yes | 3195.49 | 3046.33 | -149.16 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r1-a17-middle-sp0 | bru | post | pre | no | 1 | 17 | middle | no | 2300.29 | 2151.13 | -149.16 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r1-a17-middle-sp1 | bru | post | pre | no | 1 | 17 | middle | yes | 2300.29 | 2151.13 | -149.16 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r1-a17-high-sp0 | bru | post | pre | no | 1 | 17 | high | no | 2300.29 | 2151.13 | -149.16 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r1-a17-high-sp1 | bru | post | pre | no | 1 | 17 | high | yes | 2300.29 | 2151.13 | -149.16 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r2-a3-low-sp0 | bru | post | post | yes | 2 | 3 | low | no | 6614.94 | 6614.94 | 0.00 | bru-new-post | matched |
| cb-bru-post-r2-a3-low-sp1 | bru | post | post | yes | 2 | 3 | low | yes | 6913.26 | 6913.26 | 0.00 | bru-new-post | matched |
| cb-bru-post-r2-a3-middle-sp0 | bru | post | post | yes | 2 | 3 | middle | no | 5272.14 | 5272.14 | 0.00 | bru-new-post | matched |
| cb-bru-post-r2-a3-middle-sp1 | bru | post | post | yes | 2 | 3 | middle | yes | 5272.14 | 5272.14 | 0.00 | bru-new-post | matched |
| cb-bru-post-r2-a3-high-sp0 | bru | post | post | yes | 2 | 3 | high | no | 4525.98 | 4525.98 | 0.00 | bru-new-post | matched |
| cb-bru-post-r2-a3-high-sp1 | bru | post | post | yes | 2 | 3 | high | yes | 4525.98 | 4525.98 | 0.00 | bru-new-post | matched |
| cb-bru-post-r2-a8-low-sp0 | bru | post | pre | no | 2 | 8 | low | no | 6639.80 | 6341.48 | -298.32 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance); Brussels employed couple is ineligible for old LGAF social supplement |
| cb-bru-post-r2-a8-low-sp1 | bru | post | pre | no | 2 | 8 | low | yes | 6938.12 | 6639.80 | -298.32 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r2-a8-middle-sp0 | bru | post | pre | no | 2 | 8 | middle | no | 5297.00 | 4998.68 | -298.32 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r2-a8-middle-sp1 | bru | post | pre | no | 2 | 8 | middle | yes | 5297.00 | 4998.68 | -298.32 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r2-a8-high-sp0 | bru | post | pre | no | 2 | 8 | high | no | 4550.84 | 4894.52 | 343.68 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r2-a8-high-sp1 | bru | post | pre | no | 2 | 8 | high | yes | 4550.84 | 4894.52 | 343.68 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r2-a14-low-sp0 | bru | post | pre | no | 2 | 14 | low | no | 7286.18 | 6987.86 | -298.32 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance); Brussels employed couple is ineligible for old LGAF social supplement |
| cb-bru-post-r2-a14-low-sp1 | bru | post | pre | no | 2 | 14 | low | yes | 7584.50 | 7286.18 | -298.32 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r2-a14-middle-sp0 | bru | post | pre | no | 2 | 14 | middle | no | 5645.06 | 5346.74 | -298.32 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r2-a14-middle-sp1 | bru | post | pre | no | 2 | 14 | middle | yes | 5645.06 | 5346.74 | -298.32 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r2-a14-high-sp0 | bru | post | pre | no | 2 | 14 | high | no | 4898.90 | 5336.66 | 437.76 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r2-a14-high-sp1 | bru | post | pre | no | 2 | 14 | high | yes | 4898.90 | 5336.66 | 437.76 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r2-a17-low-sp0 | bru | post | pre | no | 2 | 17 | low | no | 7286.18 | 6987.86 | -298.32 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance); Brussels employed couple is ineligible for old LGAF social supplement |
| cb-bru-post-r2-a17-low-sp1 | bru | post | pre | no | 2 | 17 | low | yes | 7584.50 | 7286.18 | -298.32 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r2-a17-middle-sp0 | bru | post | pre | no | 2 | 17 | middle | no | 5645.06 | 5346.74 | -298.32 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r2-a17-middle-sp1 | bru | post | pre | no | 2 | 17 | middle | yes | 5645.06 | 5346.74 | -298.32 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r2-a17-high-sp0 | bru | post | pre | no | 2 | 17 | high | no | 4898.90 | 5336.66 | 437.76 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r2-a17-high-sp1 | bru | post | pre | no | 2 | 17 | high | yes | 4898.90 | 5336.66 | 437.76 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r3-a3-low-sp0 | bru | post | post | yes | 3 | 3 | low | no | 11712.69 | 11712.69 | 0.00 | bru-new-post | matched |
| cb-bru-post-r3-a3-low-sp1 | bru | post | post | yes | 3 | 3 | low | yes | 12608.01 | 12608.01 | 0.00 | bru-new-post | matched |
| cb-bru-post-r3-a3-middle-sp0 | bru | post | post | yes | 3 | 3 | middle | no | 10011.69 | 10011.69 | 0.00 | bru-new-post | matched |
| cb-bru-post-r3-a3-middle-sp1 | bru | post | post | yes | 3 | 3 | middle | yes | 10011.69 | 10011.69 | 0.00 | bru-new-post | matched |
| cb-bru-post-r3-a3-high-sp0 | bru | post | post | yes | 3 | 3 | high | no | 6788.97 | 6788.97 | 0.00 | bru-new-post | matched |
| cb-bru-post-r3-a3-high-sp1 | bru | post | post | yes | 3 | 3 | high | yes | 6788.97 | 6788.97 | 0.00 | bru-new-post | matched |
| cb-bru-post-r3-a8-low-sp0 | bru | post | pre | no | 3 | 8 | low | no | 11749.98 | 11302.50 | -447.48 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance); Brussels employed couple is ineligible for old LGAF social supplement |
| cb-bru-post-r3-a8-low-sp1 | bru | post | pre | no | 3 | 8 | low | yes | 12645.30 | 12197.82 | -447.48 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r3-a8-middle-sp0 | bru | post | pre | no | 3 | 8 | middle | no | 10048.98 | 9601.50 | -447.48 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r3-a8-middle-sp1 | bru | post | pre | no | 3 | 8 | middle | yes | 10048.98 | 9601.50 | -447.48 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r3-a8-high-sp0 | bru | post | pre | no | 3 | 8 | high | no | 6826.26 | 9377.34 | 2551.08 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r3-a8-high-sp1 | bru | post | pre | no | 3 | 8 | high | yes | 6826.26 | 9377.34 | 2551.08 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r3-a14-low-sp0 | bru | post | pre | no | 3 | 14 | low | no | 12719.91 | 12272.43 | -447.48 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance); Brussels employed couple is ineligible for old LGAF social supplement |
| cb-bru-post-r3-a14-low-sp1 | bru | post | pre | no | 3 | 14 | low | yes | 13615.23 | 13167.75 | -447.48 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r3-a14-middle-sp0 | bru | post | pre | no | 3 | 14 | middle | no | 10571.07 | 10123.59 | -447.48 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r3-a14-middle-sp1 | bru | post | pre | no | 3 | 14 | middle | yes | 10571.07 | 10123.59 | -447.48 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r3-a14-high-sp0 | bru | post | pre | no | 3 | 14 | high | no | 7348.35 | 10106.55 | 2758.20 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r3-a14-high-sp1 | bru | post | pre | no | 3 | 14 | high | yes | 7348.35 | 10106.55 | 2758.20 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r3-a17-low-sp0 | bru | post | pre | no | 3 | 17 | low | no | 12719.91 | 12272.43 | -447.48 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance); Brussels employed couple is ineligible for old LGAF social supplement |
| cb-bru-post-r3-a17-low-sp1 | bru | post | pre | no | 3 | 17 | low | yes | 13615.23 | 13167.75 | -447.48 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r3-a17-middle-sp0 | bru | post | pre | no | 3 | 17 | middle | no | 10571.07 | 10123.59 | -447.48 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r3-a17-middle-sp1 | bru | post | pre | no | 3 | 17 | middle | yes | 10571.07 | 10123.59 | -447.48 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r3-a17-high-sp0 | bru | post | pre | no | 3 | 17 | high | no | 7348.35 | 10106.55 | 2758.20 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-bru-post-r3-a17-high-sp1 | bru | post | pre | no | 3 | 17 | high | yes | 7348.35 | 10106.55 | 2758.20 | bru-new-post | EUROMOD age-proxy cohort routing; Brussels pre-2020 entitlement is household max(old LGAF,new ordinance) |
| cb-vlg-pre-r1-a3-low-sp0 | vlg | pre | post | no | 1 | 3 | low | no | 2088.08 | 3047.72 | 959.64 | vlg-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-vlg-pre-r1-a3-low-sp1 | vlg | pre | post | no | 1 | 3 | low | yes | 2088.08 | 3047.72 | 959.64 | vlg-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-vlg-pre-r1-a3-middle-sp0 | vlg | pre | post | no | 1 | 3 | middle | no | 1267.16 | 2621.72 | 1354.56 | vlg-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-vlg-pre-r1-a3-middle-sp1 | vlg | pre | post | no | 1 | 3 | middle | yes | 1267.16 | 2621.72 | 1354.56 | vlg-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-vlg-pre-r1-a3-high-sp0 | vlg | pre | post | no | 1 | 3 | high | no | 1267.16 | 2184.80 | 917.64 | vlg-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-vlg-pre-r1-a3-high-sp1 | vlg | pre | post | no | 1 | 3 | high | yes | 1267.16 | 2184.80 | 917.64 | vlg-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-vlg-pre-r1-a8-low-sp0 | vlg | pre | pre | yes | 1 | 8 | low | no | 2496.53 | 2496.53 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r1-a8-low-sp1 | vlg | pre | pre | yes | 1 | 8 | low | yes | 2496.53 | 2496.53 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r1-a8-middle-sp0 | vlg | pre | pre | yes | 1 | 8 | middle | no | 1480.37 | 1480.37 | 0.00 | vlg-old-lgaf | Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-pre-r1-a8-middle-sp1 | vlg | pre | pre | yes | 1 | 8 | middle | yes | 1480.37 | 1480.37 | 0.00 | vlg-old-lgaf | Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-pre-r1-a8-high-sp0 | vlg | pre | pre | yes | 1 | 8 | high | no | 1480.37 | 1480.37 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r1-a8-high-sp1 | vlg | pre | pre | yes | 1 | 8 | high | yes | 1480.37 | 1480.37 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r1-a14-low-sp0 | vlg | pre | pre | yes | 1 | 14 | low | no | 2720.18 | 2720.18 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r1-a14-low-sp1 | vlg | pre | pre | yes | 1 | 14 | low | yes | 2720.18 | 2720.18 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r1-a14-middle-sp0 | vlg | pre | pre | yes | 1 | 14 | middle | no | 1599.98 | 1599.98 | 0.00 | vlg-old-lgaf | Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-pre-r1-a14-middle-sp1 | vlg | pre | pre | yes | 1 | 14 | middle | yes | 1599.98 | 1599.98 | 0.00 | vlg-old-lgaf | Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-pre-r1-a14-high-sp0 | vlg | pre | pre | yes | 1 | 14 | high | no | 1599.98 | 1599.98 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r1-a14-high-sp1 | vlg | pre | pre | yes | 1 | 14 | high | yes | 1599.98 | 1599.98 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r1-a17-low-sp0 | vlg | pre | pre | yes | 1 | 17 | low | no | 2720.18 | 2720.18 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r1-a17-low-sp1 | vlg | pre | pre | yes | 1 | 17 | low | yes | 2720.18 | 2720.18 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r1-a17-middle-sp0 | vlg | pre | pre | yes | 1 | 17 | middle | no | 1599.98 | 1599.98 | 0.00 | vlg-old-lgaf | Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-pre-r1-a17-middle-sp1 | vlg | pre | pre | yes | 1 | 17 | middle | yes | 1599.98 | 1599.98 | 0.00 | vlg-old-lgaf | Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-pre-r1-a17-high-sp0 | vlg | pre | pre | yes | 1 | 17 | high | no | 1599.98 | 1599.98 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r1-a17-high-sp1 | vlg | pre | pre | yes | 1 | 17 | high | yes | 1599.98 | 1599.98 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r2-a3-low-sp0 | vlg | pre | post | no | 2 | 3 | low | no | 4993.60 | 6095.44 | 1101.84 | vlg-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-vlg-pre-r2-a3-low-sp1 | vlg | pre | post | no | 2 | 3 | low | yes | 4993.60 | 6095.44 | 1101.84 | vlg-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-vlg-pre-r2-a3-middle-sp0 | vlg | pre | post | no | 2 | 3 | middle | no | 3592.72 | 5243.44 | 1650.72 | vlg-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-vlg-pre-r2-a3-middle-sp1 | vlg | pre | post | no | 2 | 3 | middle | yes | 3592.72 | 5243.44 | 1650.72 | vlg-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-vlg-pre-r2-a3-high-sp0 | vlg | pre | post | no | 2 | 3 | high | no | 3592.72 | 4369.60 | 776.88 | vlg-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-vlg-pre-r2-a3-high-sp1 | vlg | pre | post | no | 2 | 3 | high | yes | 3592.72 | 4369.60 | 776.88 | vlg-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-vlg-pre-r2-a8-low-sp0 | vlg | pre | pre | yes | 2 | 8 | low | no | 5810.50 | 5810.50 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r2-a8-low-sp1 | vlg | pre | pre | yes | 2 | 8 | low | yes | 5810.50 | 5810.50 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r2-a8-middle-sp0 | vlg | pre | pre | yes | 2 | 8 | middle | no | 4214.38 | 4214.38 | 0.00 | vlg-old-lgaf | Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-pre-r2-a8-middle-sp1 | vlg | pre | pre | yes | 2 | 8 | middle | yes | 4214.38 | 4214.38 | 0.00 | vlg-old-lgaf | Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-pre-r2-a8-high-sp0 | vlg | pre | pre | yes | 2 | 8 | high | no | 4214.38 | 4214.38 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r2-a8-high-sp1 | vlg | pre | pre | yes | 2 | 8 | high | yes | 4214.38 | 4214.38 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r2-a14-low-sp0 | vlg | pre | pre | yes | 2 | 14 | low | no | 6257.80 | 6257.80 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r2-a14-low-sp1 | vlg | pre | pre | yes | 2 | 14 | low | yes | 6257.80 | 6257.80 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r2-a14-middle-sp0 | vlg | pre | pre | yes | 2 | 14 | middle | no | 4557.64 | 4557.64 | 0.00 | vlg-old-lgaf | Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-pre-r2-a14-middle-sp1 | vlg | pre | pre | yes | 2 | 14 | middle | yes | 4557.64 | 4557.64 | 0.00 | vlg-old-lgaf | Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-pre-r2-a14-high-sp0 | vlg | pre | pre | yes | 2 | 14 | high | no | 4557.64 | 4557.64 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r2-a14-high-sp1 | vlg | pre | pre | yes | 2 | 14 | high | yes | 4557.64 | 4557.64 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r2-a17-low-sp0 | vlg | pre | pre | yes | 2 | 17 | low | no | 6257.80 | 6257.80 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r2-a17-low-sp1 | vlg | pre | pre | yes | 2 | 17 | low | yes | 6257.80 | 6257.80 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r2-a17-middle-sp0 | vlg | pre | pre | yes | 2 | 17 | middle | no | 4557.64 | 4557.64 | 0.00 | vlg-old-lgaf | Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-pre-r2-a17-middle-sp1 | vlg | pre | pre | yes | 2 | 17 | middle | yes | 4557.64 | 4557.64 | 0.00 | vlg-old-lgaf | Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-pre-r2-a17-high-sp0 | vlg | pre | pre | yes | 2 | 17 | high | no | 4557.64 | 4557.64 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r2-a17-high-sp1 | vlg | pre | pre | yes | 2 | 17 | high | yes | 4557.64 | 4557.64 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r3-a3-low-sp0 | vlg | pre | post | no | 3 | 3 | low | no | 8386.20 | 10359.24 | 1973.04 | vlg-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-vlg-pre-r3-a3-low-sp1 | vlg | pre | post | no | 3 | 3 | low | yes | 8634.00 | 10359.24 | 1725.24 | vlg-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-vlg-pre-r3-a3-middle-sp0 | vlg | pre | post | no | 3 | 3 | middle | no | 6729.12 | 9548.52 | 2819.40 | vlg-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-vlg-pre-r3-a3-middle-sp1 | vlg | pre | post | no | 3 | 3 | middle | yes | 6729.12 | 9548.52 | 2819.40 | vlg-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-vlg-pre-r3-a3-high-sp0 | vlg | pre | post | no | 3 | 3 | high | no | 6729.12 | 6554.40 | -174.72 | vlg-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-vlg-pre-r3-a3-high-sp1 | vlg | pre | post | no | 3 | 3 | high | yes | 6729.12 | 6554.40 | -174.72 | vlg-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-vlg-pre-r3-a8-low-sp0 | vlg | pre | pre | yes | 3 | 8 | low | no | 9611.55 | 9611.55 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r3-a8-low-sp1 | vlg | pre | pre | yes | 3 | 8 | low | yes | 9859.35 | 9859.35 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r3-a8-middle-sp0 | vlg | pre | pre | yes | 3 | 8 | middle | no | 7759.23 | 7759.23 | 0.00 | vlg-old-lgaf | Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-pre-r3-a8-middle-sp1 | vlg | pre | pre | yes | 3 | 8 | middle | yes | 7759.23 | 7759.23 | 0.00 | vlg-old-lgaf | Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-pre-r3-a8-high-sp0 | vlg | pre | pre | yes | 3 | 8 | high | no | 7759.23 | 7759.23 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r3-a8-high-sp1 | vlg | pre | pre | yes | 3 | 8 | high | yes | 7759.23 | 7759.23 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r3-a14-low-sp0 | vlg | pre | pre | yes | 3 | 14 | low | no | 10282.50 | 10282.50 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r3-a14-low-sp1 | vlg | pre | pre | yes | 3 | 14 | low | yes | 10530.30 | 10530.30 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r3-a14-middle-sp0 | vlg | pre | pre | yes | 3 | 14 | middle | no | 8326.14 | 8326.14 | 0.00 | vlg-old-lgaf | Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-pre-r3-a14-middle-sp1 | vlg | pre | pre | yes | 3 | 14 | middle | yes | 8326.14 | 8326.14 | 0.00 | vlg-old-lgaf | Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-pre-r3-a14-high-sp0 | vlg | pre | pre | yes | 3 | 14 | high | no | 8326.14 | 8326.14 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r3-a14-high-sp1 | vlg | pre | pre | yes | 3 | 14 | high | yes | 8326.14 | 8326.14 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r3-a17-low-sp0 | vlg | pre | pre | yes | 3 | 17 | low | no | 10282.50 | 10282.50 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r3-a17-low-sp1 | vlg | pre | pre | yes | 3 | 17 | low | yes | 10530.30 | 10530.30 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r3-a17-middle-sp0 | vlg | pre | pre | yes | 3 | 17 | middle | no | 8326.14 | 8326.14 | 0.00 | vlg-old-lgaf | Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-pre-r3-a17-middle-sp1 | vlg | pre | pre | yes | 3 | 17 | middle | yes | 8326.14 | 8326.14 | 0.00 | vlg-old-lgaf | Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-pre-r3-a17-high-sp0 | vlg | pre | pre | yes | 3 | 17 | high | no | 8326.14 | 8326.14 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-pre-r3-a17-high-sp1 | vlg | pre | pre | yes | 3 | 17 | high | yes | 8326.14 | 8326.14 | 0.00 | vlg-old-lgaf | matched |
| cb-vlg-post-r1-a3-low-sp0 | vlg | post | post | yes | 1 | 3 | low | no | 3047.72 | 3047.72 | 0.00 | vlg-new | matched |
| cb-vlg-post-r1-a3-low-sp1 | vlg | post | post | yes | 1 | 3 | low | yes | 3047.72 | 3047.72 | 0.00 | vlg-new | matched |
| cb-vlg-post-r1-a3-middle-sp0 | vlg | post | post | yes | 1 | 3 | middle | no | 2621.72 | 2621.72 | 0.00 | vlg-new | matched |
| cb-vlg-post-r1-a3-middle-sp1 | vlg | post | post | yes | 1 | 3 | middle | yes | 2621.72 | 2621.72 | 0.00 | vlg-new | matched |
| cb-vlg-post-r1-a3-high-sp0 | vlg | post | post | yes | 1 | 3 | high | no | 2184.80 | 2184.80 | 0.00 | vlg-new | matched |
| cb-vlg-post-r1-a3-high-sp1 | vlg | post | post | yes | 1 | 3 | high | yes | 2184.80 | 2184.80 | 0.00 | vlg-new | matched |
| cb-vlg-post-r1-a8-low-sp0 | vlg | post | pre | no | 1 | 8 | low | no | 3064.61 | 2496.53 | -568.08 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r1-a8-low-sp1 | vlg | post | pre | no | 1 | 8 | low | yes | 3064.61 | 2496.53 | -568.08 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r1-a8-middle-sp0 | vlg | post | pre | no | 1 | 8 | middle | no | 2638.61 | 1480.37 | -1158.24 | vlg-new | EUROMOD age-proxy cohort routing; Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-post-r1-a8-middle-sp1 | vlg | post | pre | no | 1 | 8 | middle | yes | 2638.61 | 1480.37 | -1158.24 | vlg-new | EUROMOD age-proxy cohort routing; Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-post-r1-a8-high-sp0 | vlg | post | pre | no | 1 | 8 | high | no | 2201.69 | 1480.37 | -721.32 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r1-a8-high-sp1 | vlg | post | pre | no | 1 | 8 | high | yes | 2201.69 | 1480.37 | -721.32 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r1-a14-low-sp0 | vlg | post | pre | no | 1 | 14 | low | no | 3081.50 | 2720.18 | -361.32 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r1-a14-low-sp1 | vlg | post | pre | no | 1 | 14 | low | yes | 3081.50 | 2720.18 | -361.32 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r1-a14-middle-sp0 | vlg | post | pre | no | 1 | 14 | middle | no | 2655.50 | 1599.98 | -1055.52 | vlg-new | EUROMOD age-proxy cohort routing; Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-post-r1-a14-middle-sp1 | vlg | post | pre | no | 1 | 14 | middle | yes | 2655.50 | 1599.98 | -1055.52 | vlg-new | EUROMOD age-proxy cohort routing; Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-post-r1-a14-high-sp0 | vlg | post | pre | no | 1 | 14 | high | no | 2218.58 | 1599.98 | -618.60 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r1-a14-high-sp1 | vlg | post | pre | no | 1 | 14 | high | yes | 2218.58 | 1599.98 | -618.60 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r1-a17-low-sp0 | vlg | post | pre | no | 1 | 17 | low | no | 3081.50 | 2720.18 | -361.32 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r1-a17-low-sp1 | vlg | post | pre | no | 1 | 17 | low | yes | 3081.50 | 2720.18 | -361.32 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r1-a17-middle-sp0 | vlg | post | pre | no | 1 | 17 | middle | no | 2655.50 | 1599.98 | -1055.52 | vlg-new | EUROMOD age-proxy cohort routing; Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-post-r1-a17-middle-sp1 | vlg | post | pre | no | 1 | 17 | middle | yes | 2655.50 | 1599.98 | -1055.52 | vlg-new | EUROMOD age-proxy cohort routing; Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-post-r1-a17-high-sp0 | vlg | post | pre | no | 1 | 17 | high | no | 2218.58 | 1599.98 | -618.60 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r1-a17-high-sp1 | vlg | post | pre | no | 1 | 17 | high | yes | 2218.58 | 1599.98 | -618.60 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r2-a3-low-sp0 | vlg | post | post | yes | 2 | 3 | low | no | 6095.44 | 6095.44 | 0.00 | vlg-new | matched |
| cb-vlg-post-r2-a3-low-sp1 | vlg | post | post | yes | 2 | 3 | low | yes | 6095.44 | 6095.44 | 0.00 | vlg-new | matched |
| cb-vlg-post-r2-a3-middle-sp0 | vlg | post | post | yes | 2 | 3 | middle | no | 5243.44 | 5243.44 | 0.00 | vlg-new | matched |
| cb-vlg-post-r2-a3-middle-sp1 | vlg | post | post | yes | 2 | 3 | middle | yes | 5243.44 | 5243.44 | 0.00 | vlg-new | matched |
| cb-vlg-post-r2-a3-high-sp0 | vlg | post | post | yes | 2 | 3 | high | no | 4369.60 | 4369.60 | 0.00 | vlg-new | matched |
| cb-vlg-post-r2-a3-high-sp1 | vlg | post | post | yes | 2 | 3 | high | yes | 4369.60 | 4369.60 | 0.00 | vlg-new | matched |
| cb-vlg-post-r2-a8-low-sp0 | vlg | post | pre | no | 2 | 8 | low | no | 6129.22 | 5810.50 | -318.72 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r2-a8-low-sp1 | vlg | post | pre | no | 2 | 8 | low | yes | 6129.22 | 5810.50 | -318.72 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r2-a8-middle-sp0 | vlg | post | pre | no | 2 | 8 | middle | no | 5277.22 | 4214.38 | -1062.84 | vlg-new | EUROMOD age-proxy cohort routing; Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-post-r2-a8-middle-sp1 | vlg | post | pre | no | 2 | 8 | middle | yes | 5277.22 | 4214.38 | -1062.84 | vlg-new | EUROMOD age-proxy cohort routing; Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-post-r2-a8-high-sp0 | vlg | post | pre | no | 2 | 8 | high | no | 4403.38 | 4214.38 | -189.00 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r2-a8-high-sp1 | vlg | post | pre | no | 2 | 8 | high | yes | 4403.38 | 4214.38 | -189.00 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r2-a14-low-sp0 | vlg | post | pre | no | 2 | 14 | low | no | 6163.00 | 6257.80 | 94.80 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r2-a14-low-sp1 | vlg | post | pre | no | 2 | 14 | low | yes | 6163.00 | 6257.80 | 94.80 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r2-a14-middle-sp0 | vlg | post | pre | no | 2 | 14 | middle | no | 5311.00 | 4557.64 | -753.36 | vlg-new | EUROMOD age-proxy cohort routing; Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-post-r2-a14-middle-sp1 | vlg | post | pre | no | 2 | 14 | middle | yes | 5311.00 | 4557.64 | -753.36 | vlg-new | EUROMOD age-proxy cohort routing; Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-post-r2-a14-high-sp0 | vlg | post | pre | no | 2 | 14 | high | no | 4437.16 | 4557.64 | 120.48 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r2-a14-high-sp1 | vlg | post | pre | no | 2 | 14 | high | yes | 4437.16 | 4557.64 | 120.48 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r2-a17-low-sp0 | vlg | post | pre | no | 2 | 17 | low | no | 6163.00 | 6257.80 | 94.80 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r2-a17-low-sp1 | vlg | post | pre | no | 2 | 17 | low | yes | 6163.00 | 6257.80 | 94.80 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r2-a17-middle-sp0 | vlg | post | pre | no | 2 | 17 | middle | no | 5311.00 | 4557.64 | -753.36 | vlg-new | EUROMOD age-proxy cohort routing; Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-post-r2-a17-middle-sp1 | vlg | post | pre | no | 2 | 17 | middle | yes | 5311.00 | 4557.64 | -753.36 | vlg-new | EUROMOD age-proxy cohort routing; Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-post-r2-a17-high-sp0 | vlg | post | pre | no | 2 | 17 | high | no | 4437.16 | 4557.64 | 120.48 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r2-a17-high-sp1 | vlg | post | pre | no | 2 | 17 | high | yes | 4437.16 | 4557.64 | 120.48 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r3-a3-low-sp0 | vlg | post | post | yes | 3 | 3 | low | no | 10359.24 | 10359.24 | 0.00 | vlg-new | matched |
| cb-vlg-post-r3-a3-low-sp1 | vlg | post | post | yes | 3 | 3 | low | yes | 10359.24 | 10359.24 | 0.00 | vlg-new | matched |
| cb-vlg-post-r3-a3-middle-sp0 | vlg | post | post | yes | 3 | 3 | middle | no | 9548.52 | 9548.52 | 0.00 | vlg-new | matched |
| cb-vlg-post-r3-a3-middle-sp1 | vlg | post | post | yes | 3 | 3 | middle | yes | 9548.52 | 9548.52 | 0.00 | vlg-new | matched |
| cb-vlg-post-r3-a3-high-sp0 | vlg | post | post | yes | 3 | 3 | high | no | 6554.40 | 6554.40 | 0.00 | vlg-new | matched |
| cb-vlg-post-r3-a3-high-sp1 | vlg | post | post | yes | 3 | 3 | high | yes | 6554.40 | 6554.40 | 0.00 | vlg-new | matched |
| cb-vlg-post-r3-a8-low-sp0 | vlg | post | pre | no | 3 | 8 | low | no | 10409.91 | 9611.55 | -798.36 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r3-a8-low-sp1 | vlg | post | pre | no | 3 | 8 | low | yes | 10409.91 | 9859.35 | -550.56 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r3-a8-middle-sp0 | vlg | post | pre | no | 3 | 8 | middle | no | 9599.19 | 7759.23 | -1839.96 | vlg-new | EUROMOD age-proxy cohort routing; Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-post-r3-a8-middle-sp1 | vlg | post | pre | no | 3 | 8 | middle | yes | 9599.19 | 7759.23 | -1839.96 | vlg-new | EUROMOD age-proxy cohort routing; Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-post-r3-a8-high-sp0 | vlg | post | pre | no | 3 | 8 | high | no | 6605.07 | 7759.23 | 1154.16 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r3-a8-high-sp1 | vlg | post | pre | no | 3 | 8 | high | yes | 6605.07 | 7759.23 | 1154.16 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r3-a14-low-sp0 | vlg | post | pre | no | 3 | 14 | low | no | 10460.58 | 10282.50 | -178.08 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r3-a14-low-sp1 | vlg | post | pre | no | 3 | 14 | low | yes | 10460.58 | 10530.30 | 69.72 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r3-a14-middle-sp0 | vlg | post | pre | no | 3 | 14 | middle | no | 9649.86 | 8326.14 | -1323.72 | vlg-new | EUROMOD age-proxy cohort routing; Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-post-r3-a14-middle-sp1 | vlg | post | pre | no | 3 | 14 | middle | yes | 9649.86 | 8326.14 | -1323.72 | vlg-new | EUROMOD age-proxy cohort routing; Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-post-r3-a14-high-sp0 | vlg | post | pre | no | 3 | 14 | high | no | 6655.74 | 8326.14 | 1670.40 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r3-a14-high-sp1 | vlg | post | pre | no | 3 | 14 | high | yes | 6655.74 | 8326.14 | 1670.40 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r3-a17-low-sp0 | vlg | post | pre | no | 3 | 17 | low | no | 10460.58 | 10282.50 | -178.08 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r3-a17-low-sp1 | vlg | post | pre | no | 3 | 17 | low | yes | 10460.58 | 10530.30 | 69.72 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r3-a17-middle-sp0 | vlg | post | pre | no | 3 | 17 | middle | no | 9649.86 | 8326.14 | -1323.72 | vlg-new | EUROMOD age-proxy cohort routing; Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-post-r3-a17-middle-sp1 | vlg | post | pre | no | 3 | 17 | middle | yes | 9649.86 | 8326.14 | -1323.72 | vlg-new | EUROMOD age-proxy cohort routing; Flemish legacy middle supplement requires a mixed old/new family; all children here share a cohort |
| cb-vlg-post-r3-a17-high-sp0 | vlg | post | pre | no | 3 | 17 | high | no | 6655.74 | 8326.14 | 1670.40 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-vlg-post-r3-a17-high-sp1 | vlg | post | pre | no | 3 | 17 | high | yes | 6655.74 | 8326.14 | 1670.40 | vlg-new | EUROMOD age-proxy cohort routing |
| cb-wal-pre-r1-a3-low-sp0 | wal | pre | post | no | 1 | 3 | low | no | 2193.54 | 3158.31 | 964.77 | wal-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-wal-pre-r1-a3-low-sp1 | wal | pre | post | no | 1 | 3 | low | yes | 2193.54 | 3158.31 | 964.77 | wal-old-lgaf | EUROMOD age-proxy cohort routing; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r1-a3-middle-sp0 | wal | pre | post | no | 1 | 3 | middle | no | 1455.83 | 2710.71 | 1254.88 | wal-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-wal-pre-r1-a3-middle-sp1 | wal | pre | post | no | 1 | 3 | middle | yes | 1455.83 | 2710.71 | 1254.88 | wal-old-lgaf | EUROMOD age-proxy cohort routing; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r1-a3-high-sp0 | wal | pre | post | no | 1 | 3 | high | no | 1455.83 | 2337.63 | 881.80 | wal-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-wal-pre-r1-a3-high-sp1 | wal | pre | post | no | 1 | 3 | high | yes | 1455.83 | 2337.63 | 881.80 | wal-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-wal-pre-r1-a8-low-sp0 | wal | pre | pre | yes | 1 | 8 | low | no | 2730.98 | 3551.66 | 820.68 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-pre-r1-a8-low-sp1 | wal | pre | pre | yes | 1 | 8 | low | yes | 2730.98 | 3551.66 | 820.68 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r1-a8-middle-sp0 | wal | pre | pre | yes | 1 | 8 | middle | no | 1735.18 | 2108.26 | 373.08 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-pre-r1-a8-middle-sp1 | wal | pre | pre | yes | 1 | 8 | middle | yes | 1735.18 | 2108.26 | 373.08 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r1-a8-high-sp0 | wal | pre | pre | yes | 1 | 8 | high | no | 1735.18 | 1735.18 | 0.00 | wal-old-lgaf | matched |
| cb-wal-pre-r1-a8-high-sp1 | wal | pre | pre | yes | 1 | 8 | high | yes | 1735.18 | 1735.18 | 0.00 | wal-old-lgaf | matched |
| cb-wal-pre-r1-a14-low-sp0 | wal | pre | pre | yes | 1 | 14 | low | no | 3024.10 | 3844.78 | 820.68 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-pre-r1-a14-low-sp1 | wal | pre | pre | yes | 1 | 14 | low | yes | 3024.10 | 3844.78 | 820.68 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r1-a14-middle-sp0 | wal | pre | pre | yes | 1 | 14 | middle | no | 1887.80 | 2260.88 | 373.08 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-pre-r1-a14-middle-sp1 | wal | pre | pre | yes | 1 | 14 | middle | yes | 1887.80 | 2260.88 | 373.08 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r1-a14-high-sp0 | wal | pre | pre | yes | 1 | 14 | high | no | 1887.80 | 1887.80 | 0.00 | wal-old-lgaf | matched |
| cb-wal-pre-r1-a14-high-sp1 | wal | pre | pre | yes | 1 | 14 | high | yes | 1887.80 | 1887.80 | 0.00 | wal-old-lgaf | matched |
| cb-wal-pre-r1-a17-low-sp0 | wal | pre | pre | yes | 1 | 17 | low | no | 3024.10 | 3844.78 | 820.68 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-pre-r1-a17-low-sp1 | wal | pre | pre | yes | 1 | 17 | low | yes | 3024.10 | 3844.78 | 820.68 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r1-a17-middle-sp0 | wal | pre | pre | yes | 1 | 17 | middle | no | 1887.80 | 2260.88 | 373.08 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-pre-r1-a17-middle-sp1 | wal | pre | pre | yes | 1 | 17 | middle | yes | 1887.80 | 2260.88 | 373.08 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r1-a17-high-sp0 | wal | pre | pre | yes | 1 | 17 | high | no | 1887.80 | 1887.80 | 0.00 | wal-old-lgaf | matched |
| cb-wal-pre-r1-a17-high-sp1 | wal | pre | pre | yes | 1 | 17 | high | yes | 1887.80 | 1887.80 | 0.00 | wal-old-lgaf | matched |
| cb-wal-pre-r2-a3-low-sp0 | wal | pre | post | no | 2 | 3 | low | no | 5325.96 | 6316.62 | 990.66 | wal-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-wal-pre-r2-a3-low-sp1 | wal | pre | post | no | 2 | 3 | low | yes | 5325.96 | 6316.62 | 990.66 | wal-old-lgaf | EUROMOD age-proxy cohort routing; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r2-a3-middle-sp0 | wal | pre | post | no | 2 | 3 | middle | no | 4127.14 | 5421.42 | 1294.28 | wal-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-wal-pre-r2-a3-middle-sp1 | wal | pre | post | no | 2 | 3 | middle | yes | 4127.14 | 5421.42 | 1294.28 | wal-old-lgaf | EUROMOD age-proxy cohort routing; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r2-a3-high-sp0 | wal | pre | post | no | 2 | 3 | high | no | 4127.14 | 4675.26 | 548.12 | wal-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-wal-pre-r2-a3-high-sp1 | wal | pre | post | no | 2 | 3 | high | yes | 4127.14 | 4675.26 | 548.12 | wal-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-wal-pre-r2-a8-low-sp0 | wal | pre | pre | yes | 2 | 8 | low | no | 6400.84 | 8042.20 | 1641.36 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-pre-r2-a8-low-sp1 | wal | pre | pre | yes | 2 | 8 | low | yes | 6400.84 | 8042.20 | 1641.36 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r2-a8-middle-sp0 | wal | pre | pre | yes | 2 | 8 | middle | no | 4933.40 | 5679.56 | 746.16 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-pre-r2-a8-middle-sp1 | wal | pre | pre | yes | 2 | 8 | middle | yes | 4933.40 | 5679.56 | 746.16 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r2-a8-high-sp0 | wal | pre | pre | yes | 2 | 8 | high | no | 4933.40 | 4933.40 | 0.00 | wal-old-lgaf | matched |
| cb-wal-pre-r2-a8-high-sp1 | wal | pre | pre | yes | 2 | 8 | high | yes | 4933.40 | 4933.40 | 0.00 | wal-old-lgaf | matched |
| cb-wal-pre-r2-a14-low-sp0 | wal | pre | pre | yes | 2 | 14 | low | no | 6987.08 | 8628.44 | 1641.36 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-pre-r2-a14-low-sp1 | wal | pre | pre | yes | 2 | 14 | low | yes | 6987.08 | 8628.44 | 1641.36 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r2-a14-middle-sp0 | wal | pre | pre | yes | 2 | 14 | middle | no | 5370.64 | 6116.80 | 746.16 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-pre-r2-a14-middle-sp1 | wal | pre | pre | yes | 2 | 14 | middle | yes | 5370.64 | 6116.80 | 746.16 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r2-a14-high-sp0 | wal | pre | pre | yes | 2 | 14 | high | no | 5370.64 | 5370.64 | 0.00 | wal-old-lgaf | matched |
| cb-wal-pre-r2-a14-high-sp1 | wal | pre | pre | yes | 2 | 14 | high | yes | 5370.64 | 5370.64 | 0.00 | wal-old-lgaf | matched |
| cb-wal-pre-r2-a17-low-sp0 | wal | pre | pre | yes | 2 | 17 | low | no | 6987.08 | 8628.44 | 1641.36 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-pre-r2-a17-low-sp1 | wal | pre | pre | yes | 2 | 17 | low | yes | 6987.08 | 8628.44 | 1641.36 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r2-a17-middle-sp0 | wal | pre | pre | yes | 2 | 17 | middle | no | 5370.64 | 6116.80 | 746.16 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-pre-r2-a17-middle-sp1 | wal | pre | pre | yes | 2 | 17 | middle | yes | 5370.64 | 6116.80 | 746.16 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r2-a17-high-sp0 | wal | pre | pre | yes | 2 | 17 | high | no | 5370.64 | 5370.64 | 0.00 | wal-old-lgaf | matched |
| cb-wal-pre-r2-a17-high-sp1 | wal | pre | pre | yes | 2 | 17 | high | yes | 5370.64 | 5370.64 | 0.00 | wal-old-lgaf | matched |
| cb-wal-pre-r3-a3-low-sp0 | wal | pre | post | no | 3 | 3 | low | no | 9390.54 | 11041.65 | 1651.11 | wal-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-wal-pre-r3-a3-low-sp1 | wal | pre | post | no | 3 | 3 | low | yes | 9675.06 | 11041.65 | 1366.59 | wal-old-lgaf | EUROMOD age-proxy cohort routing; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r3-a3-middle-sp0 | wal | pre | post | no | 3 | 3 | middle | no | 8102.49 | 9027.45 | 924.96 | wal-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-wal-pre-r3-a3-middle-sp1 | wal | pre | post | no | 3 | 3 | middle | yes | 8102.49 | 9027.45 | 924.96 | wal-old-lgaf | EUROMOD age-proxy cohort routing; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r3-a3-high-sp0 | wal | pre | post | no | 3 | 3 | high | no | 8102.49 | 7012.89 | -1089.60 | wal-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-wal-pre-r3-a3-high-sp1 | wal | pre | post | no | 3 | 3 | high | yes | 8102.49 | 7012.89 | -1089.60 | wal-old-lgaf | EUROMOD age-proxy cohort routing |
| cb-wal-pre-r3-a8-low-sp0 | wal | pre | pre | yes | 3 | 8 | low | no | 11002.86 | 15031.62 | 4028.76 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-pre-r3-a8-low-sp1 | wal | pre | pre | yes | 3 | 8 | low | yes | 11287.38 | 15316.14 | 4028.76 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r3-a8-middle-sp0 | wal | pre | pre | yes | 3 | 8 | middle | no | 9435.66 | 11450.22 | 2014.56 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-pre-r3-a8-middle-sp1 | wal | pre | pre | yes | 3 | 8 | middle | yes | 9435.66 | 11450.22 | 2014.56 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r3-a8-high-sp0 | wal | pre | pre | yes | 3 | 8 | high | no | 9435.66 | 9435.66 | 0.00 | wal-old-lgaf | matched |
| cb-wal-pre-r3-a8-high-sp1 | wal | pre | pre | yes | 3 | 8 | high | yes | 9435.66 | 9435.66 | 0.00 | wal-old-lgaf | matched |
| cb-wal-pre-r3-a14-low-sp0 | wal | pre | pre | yes | 3 | 14 | low | no | 11882.22 | 15910.98 | 4028.76 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-pre-r3-a14-low-sp1 | wal | pre | pre | yes | 3 | 14 | low | yes | 12166.74 | 16195.50 | 4028.76 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r3-a14-middle-sp0 | wal | pre | pre | yes | 3 | 14 | middle | no | 10157.52 | 12172.08 | 2014.56 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-pre-r3-a14-middle-sp1 | wal | pre | pre | yes | 3 | 14 | middle | yes | 10157.52 | 12172.08 | 2014.56 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r3-a14-high-sp0 | wal | pre | pre | yes | 3 | 14 | high | no | 10157.52 | 10157.52 | 0.00 | wal-old-lgaf | matched |
| cb-wal-pre-r3-a14-high-sp1 | wal | pre | pre | yes | 3 | 14 | high | yes | 10157.52 | 10157.52 | 0.00 | wal-old-lgaf | matched |
| cb-wal-pre-r3-a17-low-sp0 | wal | pre | pre | yes | 3 | 17 | low | no | 11882.22 | 15910.98 | 4028.76 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-pre-r3-a17-low-sp1 | wal | pre | pre | yes | 3 | 17 | low | yes | 12166.74 | 16195.50 | 4028.76 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r3-a17-middle-sp0 | wal | pre | pre | yes | 3 | 17 | middle | no | 10157.52 | 12172.08 | 2014.56 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-pre-r3-a17-middle-sp1 | wal | pre | pre | yes | 3 | 17 | middle | yes | 10157.52 | 12172.08 | 2014.56 | wal-old-lgaf | EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-pre-r3-a17-high-sp0 | wal | pre | pre | yes | 3 | 17 | high | no | 10157.52 | 10157.52 | 0.00 | wal-old-lgaf | matched |
| cb-wal-pre-r3-a17-high-sp1 | wal | pre | pre | yes | 3 | 17 | high | yes | 10157.52 | 10157.52 | 0.00 | wal-old-lgaf | matched |
| cb-wal-post-r1-a3-low-sp0 | wal | post | post | yes | 1 | 3 | low | no | 3158.31 | 3158.31 | 0.00 | wal-new | matched |
| cb-wal-post-r1-a3-low-sp1 | wal | post | post | yes | 1 | 3 | low | yes | 3456.75 | 3158.31 | -298.44 | wal-new | EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r1-a3-middle-sp0 | wal | post | post | yes | 1 | 3 | middle | no | 2710.71 | 2710.71 | 0.00 | wal-new | matched |
| cb-wal-post-r1-a3-middle-sp1 | wal | post | post | yes | 1 | 3 | middle | yes | 2859.87 | 2710.71 | -149.16 | wal-new | EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r1-a3-high-sp0 | wal | post | post | yes | 1 | 3 | high | no | 2337.63 | 2337.63 | 0.00 | wal-new | matched |
| cb-wal-post-r1-a3-high-sp1 | wal | post | post | yes | 1 | 3 | high | yes | 2337.63 | 2337.63 | 0.00 | wal-new | matched |
| cb-wal-post-r1-a8-low-sp0 | wal | post | pre | no | 1 | 8 | low | no | 3170.74 | 3551.66 | 380.92 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-post-r1-a8-low-sp1 | wal | post | pre | no | 1 | 8 | low | yes | 3469.18 | 3551.66 | 82.48 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r1-a8-middle-sp0 | wal | post | pre | no | 1 | 8 | middle | no | 2723.14 | 2108.26 | -614.88 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-post-r1-a8-middle-sp1 | wal | post | pre | no | 1 | 8 | middle | yes | 2872.30 | 2108.26 | -764.04 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r1-a8-high-sp0 | wal | post | pre | no | 1 | 8 | high | no | 2350.06 | 1735.18 | -614.88 | wal-new | EUROMOD age-proxy cohort routing |
| cb-wal-post-r1-a8-high-sp1 | wal | post | pre | no | 1 | 8 | high | yes | 2350.06 | 1735.18 | -614.88 | wal-new | EUROMOD age-proxy cohort routing |
| cb-wal-post-r1-a14-low-sp0 | wal | post | pre | no | 1 | 14 | low | no | 3195.61 | 3844.78 | 649.17 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-post-r1-a14-low-sp1 | wal | post | pre | no | 1 | 14 | low | yes | 3494.05 | 3844.78 | 350.73 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r1-a14-middle-sp0 | wal | post | pre | no | 1 | 14 | middle | no | 2748.01 | 2260.88 | -487.13 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-post-r1-a14-middle-sp1 | wal | post | pre | no | 1 | 14 | middle | yes | 2897.17 | 2260.88 | -636.29 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r1-a14-high-sp0 | wal | post | pre | no | 1 | 14 | high | no | 2374.93 | 1887.80 | -487.13 | wal-new | EUROMOD age-proxy cohort routing |
| cb-wal-post-r1-a14-high-sp1 | wal | post | pre | no | 1 | 14 | high | yes | 2374.93 | 1887.80 | -487.13 | wal-new | EUROMOD age-proxy cohort routing |
| cb-wal-post-r1-a17-low-sp0 | wal | post | pre | no | 1 | 17 | low | no | 3195.61 | 3844.78 | 649.17 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-post-r1-a17-low-sp1 | wal | post | pre | no | 1 | 17 | low | yes | 3494.05 | 3844.78 | 350.73 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r1-a17-middle-sp0 | wal | post | pre | no | 1 | 17 | middle | no | 2748.01 | 2260.88 | -487.13 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-post-r1-a17-middle-sp1 | wal | post | pre | no | 1 | 17 | middle | yes | 2897.17 | 2260.88 | -636.29 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r1-a17-high-sp0 | wal | post | pre | no | 1 | 17 | high | no | 2374.93 | 1887.80 | -487.13 | wal-new | EUROMOD age-proxy cohort routing |
| cb-wal-post-r1-a17-high-sp1 | wal | post | pre | no | 1 | 17 | high | yes | 2374.93 | 1887.80 | -487.13 | wal-new | EUROMOD age-proxy cohort routing |
| cb-wal-post-r2-a3-low-sp0 | wal | post | post | yes | 2 | 3 | low | no | 6316.62 | 6316.62 | 0.00 | wal-new | matched |
| cb-wal-post-r2-a3-low-sp1 | wal | post | post | yes | 2 | 3 | low | yes | 6913.50 | 6316.62 | -596.88 | wal-new | EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r2-a3-middle-sp0 | wal | post | post | yes | 2 | 3 | middle | no | 5421.42 | 5421.42 | 0.00 | wal-new | matched |
| cb-wal-post-r2-a3-middle-sp1 | wal | post | post | yes | 2 | 3 | middle | yes | 5719.74 | 5421.42 | -298.32 | wal-new | EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r2-a3-high-sp0 | wal | post | post | yes | 2 | 3 | high | no | 4675.26 | 4675.26 | 0.00 | wal-new | matched |
| cb-wal-post-r2-a3-high-sp1 | wal | post | post | yes | 2 | 3 | high | yes | 4675.26 | 4675.26 | 0.00 | wal-new | matched |
| cb-wal-post-r2-a8-low-sp0 | wal | post | pre | no | 2 | 8 | low | no | 6341.48 | 8042.20 | 1700.72 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-post-r2-a8-low-sp1 | wal | post | pre | no | 2 | 8 | low | yes | 6938.36 | 8042.20 | 1103.84 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r2-a8-middle-sp0 | wal | post | pre | no | 2 | 8 | middle | no | 5446.28 | 5679.56 | 233.28 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-post-r2-a8-middle-sp1 | wal | post | pre | no | 2 | 8 | middle | yes | 5744.60 | 5679.56 | -65.04 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r2-a8-high-sp0 | wal | post | pre | no | 2 | 8 | high | no | 4700.12 | 4933.40 | 233.28 | wal-new | EUROMOD age-proxy cohort routing |
| cb-wal-post-r2-a8-high-sp1 | wal | post | pre | no | 2 | 8 | high | yes | 4700.12 | 4933.40 | 233.28 | wal-new | EUROMOD age-proxy cohort routing |
| cb-wal-post-r2-a14-low-sp0 | wal | post | pre | no | 2 | 14 | low | no | 6391.22 | 8628.44 | 2237.22 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-post-r2-a14-low-sp1 | wal | post | pre | no | 2 | 14 | low | yes | 6988.10 | 8628.44 | 1640.34 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r2-a14-middle-sp0 | wal | post | pre | no | 2 | 14 | middle | no | 5496.02 | 6116.80 | 620.78 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-post-r2-a14-middle-sp1 | wal | post | pre | no | 2 | 14 | middle | yes | 5794.34 | 6116.80 | 322.46 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r2-a14-high-sp0 | wal | post | pre | no | 2 | 14 | high | no | 4749.86 | 5370.64 | 620.78 | wal-new | EUROMOD age-proxy cohort routing |
| cb-wal-post-r2-a14-high-sp1 | wal | post | pre | no | 2 | 14 | high | yes | 4749.86 | 5370.64 | 620.78 | wal-new | EUROMOD age-proxy cohort routing |
| cb-wal-post-r2-a17-low-sp0 | wal | post | pre | no | 2 | 17 | low | no | 6391.22 | 8628.44 | 2237.22 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-post-r2-a17-low-sp1 | wal | post | pre | no | 2 | 17 | low | yes | 6988.10 | 8628.44 | 1640.34 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r2-a17-middle-sp0 | wal | post | pre | no | 2 | 17 | middle | no | 5496.02 | 6116.80 | 620.78 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-post-r2-a17-middle-sp1 | wal | post | pre | no | 2 | 17 | middle | yes | 5794.34 | 6116.80 | 322.46 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r2-a17-high-sp0 | wal | post | pre | no | 2 | 17 | high | no | 4749.86 | 5370.64 | 620.78 | wal-new | EUROMOD age-proxy cohort routing |
| cb-wal-post-r2-a17-high-sp1 | wal | post | pre | no | 2 | 17 | high | yes | 4749.86 | 5370.64 | 620.78 | wal-new | EUROMOD age-proxy cohort routing |
| cb-wal-post-r3-a3-low-sp0 | wal | post | post | yes | 3 | 3 | low | no | 11041.65 | 11041.65 | 0.00 | wal-new | matched |
| cb-wal-post-r3-a3-low-sp1 | wal | post | post | yes | 3 | 3 | low | yes | 11936.97 | 11041.65 | -895.32 | wal-new | EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r3-a3-middle-sp0 | wal | post | post | yes | 3 | 3 | middle | no | 9027.45 | 9027.45 | 0.00 | wal-new | matched |
| cb-wal-post-r3-a3-middle-sp1 | wal | post | post | yes | 3 | 3 | middle | yes | 9474.93 | 9027.45 | -447.48 | wal-new | EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r3-a3-high-sp0 | wal | post | post | yes | 3 | 3 | high | no | 7012.89 | 7012.89 | 0.00 | wal-new | matched |
| cb-wal-post-r3-a3-high-sp1 | wal | post | post | yes | 3 | 3 | high | yes | 7012.89 | 7012.89 | 0.00 | wal-new | matched |
| cb-wal-post-r3-a8-low-sp0 | wal | post | pre | no | 3 | 8 | low | no | 11078.94 | 15031.62 | 3952.68 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-post-r3-a8-low-sp1 | wal | post | pre | no | 3 | 8 | low | yes | 11974.26 | 15316.14 | 3341.88 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r3-a8-middle-sp0 | wal | post | pre | no | 3 | 8 | middle | no | 9064.74 | 11450.22 | 2385.48 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-post-r3-a8-middle-sp1 | wal | post | pre | no | 3 | 8 | middle | yes | 9512.22 | 11450.22 | 1938.00 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r3-a8-high-sp0 | wal | post | pre | no | 3 | 8 | high | no | 7050.18 | 9435.66 | 2385.48 | wal-new | EUROMOD age-proxy cohort routing |
| cb-wal-post-r3-a8-high-sp1 | wal | post | pre | no | 3 | 8 | high | yes | 7050.18 | 9435.66 | 2385.48 | wal-new | EUROMOD age-proxy cohort routing |
| cb-wal-post-r3-a14-low-sp0 | wal | post | pre | no | 3 | 14 | low | no | 11153.55 | 15910.98 | 4757.43 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-post-r3-a14-low-sp1 | wal | post | pre | no | 3 | 14 | low | yes | 12048.87 | 16195.50 | 4146.63 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r3-a14-middle-sp0 | wal | post | pre | no | 3 | 14 | middle | no | 9139.35 | 12172.08 | 3032.73 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-post-r3-a14-middle-sp1 | wal | post | pre | no | 3 | 14 | middle | yes | 9586.83 | 12172.08 | 2585.25 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r3-a14-high-sp0 | wal | post | pre | no | 3 | 14 | high | no | 7124.79 | 10157.52 | 3032.73 | wal-new | EUROMOD age-proxy cohort routing |
| cb-wal-post-r3-a14-high-sp1 | wal | post | pre | no | 3 | 14 | high | yes | 7124.79 | 10157.52 | 3032.73 | wal-new | EUROMOD age-proxy cohort routing |
| cb-wal-post-r3-a17-low-sp0 | wal | post | pre | no | 3 | 17 | low | no | 11153.55 | 15910.98 | 4757.43 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-post-r3-a17-low-sp1 | wal | post | pre | no | 3 | 17 | low | yes | 12048.87 | 16195.50 | 4146.63 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r3-a17-middle-sp0 | wal | post | pre | no | 3 | 17 | middle | no | 9139.35 | 12172.08 | 3032.73 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child |
| cb-wal-post-r3-a17-middle-sp1 | wal | post | pre | no | 3 | 17 | middle | yes | 9586.83 | 12172.08 | 2585.25 | wal-new | EUROMOD age-proxy cohort routing; EUROMOD Article 13 supplement cumulatively added to old Walloon child; EUROMOD Walloon BenCalc omits the decree lone-parent increment (direct IsLoneParentOfDepChild#5 branch does not fire) |
| cb-wal-post-r3-a17-high-sp0 | wal | post | pre | no | 3 | 17 | high | no | 7124.79 | 10157.52 | 3032.73 | wal-new | EUROMOD age-proxy cohort routing |
| cb-wal-post-r3-a17-high-sp1 | wal | post | pre | no | 3 | 17 | high | yes | 7124.79 | 10157.52 | 3032.73 | wal-new | EUROMOD age-proxy cohort routing |

## Release frontier

The signed-release manifest content SHA is `c1436c9f99882a819773bc2ccddf8c2a67e41efd24b0d0a408493ba5da39964a`.

Pinned but absent pages: Flemish Articles 222 and 228; Walloon Article 3; Brussels Articles 35, 39 and 40; DG article-specific Article 111. Article 228, Walloon Article 3 and DG article-specific Article 111 have promoted substitutes and are not used by the router. Flemish Article 222 is needed to connect legacy social supplements to Article 18 conditions. Brussels Article 39 has no promoted substitute for the comparison, cap, and permanent-loss mechanics, so rules whose proofs depend on those two pages are explicit release-frontier blocks. Iriscare blocks 3 and 15 prove the 2025 birth deduction and existence/cap of transitional old amounts, but not the complete Article 39 state machine.

There is also a release-projection collision for the Flemish guidance records `be-vlg/guidance/gpedia/family-benefits/amount-scale-2024-09/schedule-{1,3,4}`. The pinned official full-table records contain the verbatim €398.39 orphan, legacy social/high-age rows, and current social bands. The signed release resolves duplicate record IDs at those paths to later abbreviated records. The sibling-layout validator therefore stops at `Ungrounded generated numeric literal: 398.39` even though the parameter companion suite passes and the literal is verbatim in the pinned full-table record. This is recorded as a release-frontier failure, not waived or replaced with an uncited literal.

## Shortfall accounting and implied average

The temporally valid half-grid has 216 households and 432 actual child units. Its statutory total is EUR1,268,361.00, or EUR2,936.02 per actual child. Against the counterfactual narrow surface emitting one EUR2,070 amount per household:

| Term | Amount | Share of EUR821,241 shortfall |
|---|---:|---:|
| Missing child units: another 216 children x EUR2,070 | EUR447,120 | 54.44% |
| Missing composition on all child units: ranks, cohort schedules, age/social/single-parent components and premiums | EUR374,121 | 45.56% |

The composition term is EUR866.02 per child above EUR2,070. Across the deliberately balanced full 432-case cross-product, the corresponding split is 55.79% unit construction and 44.21% composition (EUR894,240 and EUR708,534.36 of EUR1,602,774.36).

For a separate back-of-envelope Belgian mix, I used explicit illustrative weights: regions 58% Flanders/31% Wallonia/11% Brussels; ages 3/8/14/17 at 22%/25%/28%/25% with the cohort implied by age; child ranks 1/2/3+ at 45%/35%/20%; incomes low/middle/high at 35%/25%/40%; and 20% single-parent. Marginalizing the cumulative rank households implies EUR2,901.80 per child: EUR831.80, or 40.2%, above the EUR2,070 bare-base figure. This is a transparent sensitivity estimate, not an administrative forecast.

## Suite registration

Fable should register one deterministic `be-family-child-benefit-full-composition` builder after merge, following #508's `Case` builders and generated-grid extraction:

```python
for region, cohort, rank, age, income_band, single_parent in product(
    ("bru", "vlg", "wal"), ("pre", "post"), (1, 2, 3),
    (3, 8, 14, 17), ("low", "middle", "high"), (False, True),
):
    case_id = (
        f"cb-{region}-{cohort}-r{rank}-a{age}-"
        f"{income_band}-sp{int(single_parent)}"
    )
```

Each `Case(period="2025")` should be Household-scoped, create N child entities and N relation records with ranks 1..N, assign every Boolean explicitly, use actual DOB facts for the requested cohort, and expose both composition household outputs. Compare the diagnostic comparator to `bch_s`; retain the statutory selected output in case metadata/results. The EUROMOD rows use gross EUR30k/EUR45k/EUR90k, and `EUROMOD_TO_AXIOM_INPUT_BRIDGE` maps `il_bch_means` to each child record's annual-household-income input. Add the builder to `axiom_oracles/suites/be_family_benefits.py`; add its import/name/dispatch to `axiom_oracles/suites/__init__.py`; add the new RuleSpec output-to-`bch_s` mapping, schema assertions, and the Walloon/age-proxy dispositions; then run `scripts/extract_grids.py` so `grids/be.yaml` contains the identical 432 IDs listed below. DG remains a separate statute-backed disposition because `bch_s` is zero there.

## Corrected `bch_s` ledger mechanism

Proposed ledger text: **`bch_s` is a mixed unit-construction and encoding-slice mechanism, not solely a population construct. On the temporally valid composition grid, 54.44% of the gap (EUR447,120 of EUR821,241; approximately EUR1.25--1.91B of the observed EUR2.3--3.5B population residual) is the missing-child-unit term caused by emitting one household amount where all beneficiary-child records must be summed. The other 45.56% (EUR374,121; approximately EUR1.05--1.59B) is the base-only encoding slice omitting cohort routing, legacy rank, age/social/single-parent components, and annual premiums; its grid effect is EUR866.02 per actual child above EUR2,070. EUROMOD's Walloon Article 13 cumulation and lone-parent omission are separately dispositioned oracle mechanisms, not silently copied into the statutory surface.**

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
