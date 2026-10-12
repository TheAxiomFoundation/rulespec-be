# Lane F — dependants and family tax-free amount

## 1. Outcome

Lane F started from `ledger/dependants` at main `7c85808` and encodes the
Person-to-taxpayer/tax-unit dependant ledger, Article 133 supplements, and the
Article 134 §3 refundable credits for income year 2025 / assessment year 2026.
The existing Articles 131–132 amount module remains the only owner of the base,
child ladder, under-three, elderly, and other-dependant monetary amounts.

The local pinned-corpus result is complete and green. The EUROMOD matrix is not
cent-identical, but every residual is decomposed below with named and quantified
mechanisms. The configured signed corpus release is a separate promotion
blocker: it omits pages 183 and 188–192; encoded modules cite five of those keys
(all except page 191). Under the campaign convention, the affected rows remain
`unencoded_corpus_blocked` until those already-encoded sources are promoted; no
toolchain or waiver file was changed.

Pin evidence:

```sh
git show -s --format='%H%n%P%n%s' 30f979b10cf381acd5a3f78618e6b5b831f0b671
# 30f979b10cf381acd5a3f78618e6b5b831f0b671
# 7c85808ae99f5731b21059e643e5e19b66438904
# Encode dependants machinery, article 133 supplements, article 134 §3 credit
git -C /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin rev-parse HEAD
# 8e48989c9e46faa6d85a9624b7a2ebda0880656d
git -C /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned rev-parse HEAD
# 3869d66d009f52258be35901edbef370e65a399c
git -C /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine rev-parse HEAD
# c6cc389a8f5e7238019e4fa06849325fad9acd46
```

## 2. Pinned-law resolution

Every provision and amount below came from this command, against the campaign
pin rather than a web source:

```sh
jq -r 'select(.citation_path | test("page-(182|183|184|185|186|187|188|189|190|191|192)$")) | "### " + .citation_path + "\n" + .heading + "\n" + .body' \
  /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/data/corpus/provisions/be/statute/2026-06-30-be-income-tax-consolidated.jsonl
```

The citation key is one lower than the visible PDF page heading in this slice.

| Citation key | Operative text resolved | Encoded mechanism |
|---|---|---|
| page-182 | Article 132 | Existing child ladder and amounts; disabled child/other dependant counts twice; under-three childcare exclusion; certified dependent person aged 66+; other dependants. |
| page-183 | Article 132bis; Article 133 item 1 begins | Separate-household equal custody, maintenance duty, qualifying/timely instrument, no deducted maintenance payment, child `à charge`; €1,980 isolated-taxpayer child branch. |
| page-184 | Article 133 continuation; Article 134 §1 | Shared-custody Article 133 branch; Article 126 exclusions; marriage-year €1,980 branch; extra €1,290 at taxable income ≤€19,250, phased to zero at €24,390; qualifying professional income ≥€4,100. |
| page-185 | Article 134 §§2–3 | Tax-free-amount tax scale, statutory ordering, unused child-TFA conversion, €570 per equivalent child ceiling, half ceiling under Article 132bis, disabled child double count. |
| page-186 | Article 134 §3 continuation and §4 start | Refund of unused tax value attributable to the additional Article 133 supplement; paragraph-3 treaty exclusions; joint allocator starts. |
| page-187 | Article 134 §4 continuation; Article 135 | Joint spouse cap/allocation; supplied disability status is the upstream Article 135 adjudication result. |
| page-188 | Articles 136–138 start | Permitted roles, actual 1-January household membership, €4,100 general net-resources ceiling, Article 137 cumulation override. |
| page-189 | Articles 138–141 start | Deemed household cases and Article 140 factual household direction. |
| page-190 | Articles 141–143 start | €5,930 isolated-child and €7,520 isolated-disabled-child ceilings; justified/default expenses, 20% default, €570 worker/profit minimum; Article 143 disregard begins. |
| page-191 | Articles 143–145 start | Article 143 disregard categories and indexed category ceilings; Article 144 public interventions ignored in custody-support assessment; Article 145 starts. |
| page-192 | Article 145 | Remuneration/professional-expense and student-company-director exclusions. |

The proof excerpts in the RuleSpec files are verbatim substrings from those
records. To satisfy the repository's singular-provenance contract, adjacent
pages are separate atomic modules and imported into the composed predicates.

Three deliberately supplied legal-result facts are not presented as fully
derived population constructs:

- Article 138/139 exceptional deemed-household outcomes are explicit booleans;
  ordinary actual membership on 1 January is a separate explicit fact.
- Article 143 category-specific disregards are supplied as one aggregate amount;
  Article 142 expense selection and the resulting net means test are encoded.
- Article 145's remuneration/control outcome is an explicit exclusion boolean.

Article 144 changes how an upstream custody-support fact is constructed (public
interventions are ignored); it creates no separate monetary amount in this
pipeline. These boundaries are named so a population adapter cannot silently
treat absent evidence as a positive legal conclusion.

## 3. Encoding and scope

The Person-scope path is:

```text
related Person facts
  -> Articles 136–145 eligibility and Article 132bis gate
  -> Article 132 equivalent counts on each Person
  -> sum_where over taxpayer/tax-unit relation
  -> existing Article 131–132 TFA amounts
  -> Article 133 supplements
  -> Article 134 tax reduction and refundable credits
  -> pilot/couple/final-tax outputs
```

New atomic modules:

- `dependant_net_resources.yaml`: Article 141 ceilings and Article 142–143 net
  resources, including the 20% default and €570 minimum.
- `dependant_household_conditions.yaml`: Articles 138–140 deemed membership and
  household direction.
- `dependant_article_145_exclusion.yaml`: Article 145 exclusion gate.
- `dependant_shared_custody.yaml`: Article 132bis, including an explicit
  child-is-dependent-of-one-taxpayer fact.
- `dependants.yaml`: ordinary Article 136/137 eligibility.
- `dependant_article_132_counts.yaml`: child, shared child, under-three,
  certified elderly, other-dependant, and disabled equivalent counts.
- `article_133_isolated_taxpayer_supplement.yaml` and
  `article_133_supplements.yaml`: page-split Article 133 branches and phaseout.
- `article_134_additional_supplement_credit.yaml`: the additional Article 133
  refundable component and total paragraph-3 credit.
- `regional_autonomy_factor.yaml`: a single-source canonical home for the
  pre-existing 24.957% factor, allowing the worker compositions to import it
  instead of duplicating literals.

Pipeline relations and direction:

| Pipeline | Relation | Arity / direction |
|---|---|---|
| Individual worker | `belgium_pit_pilot_dependent_of_taxpayer` | `[Person, Person]`, taxpayer → potential dependant |
| Couple | `belgium_pit_couple_dependent_of_tax_unit` | `[TaxUnit, Person]`, tax unit → potential dependant |
| Existing spouse rollup | `belgium_pit_couple_spouse_of_tax_unit` | `[TaxUnit, Person]`, tax unit → spouse |

The relations feed the existing count inputs without duplicating their amounts:

- ordinary and Article 132bis child equivalents, with disabled children doubled;
- ordinary and shared under-three equivalents, excluding a childcare claim;
- certified dependent elderly persons; and
- other dependants, doubled when disabled.

The couple companion includes a positive nonchild relation case: one certified
elderly dependant plus one disabled other dependant yields equivalent counts
`1 + 2` and an Article 132 supplement of `€5,950 + 2×€1,980 = €9,910`.
That number is generated and verified by the companion command in §6.

### Article 133

The final isolated-taxpayer supplement is €1,980 when the taxpayer is assessed
separately and has an ordinary dependent child or receives an Article 132bis
half allocation, subject to the Article 126 §2 item 4 exclusion. The additional
isolated-parent amount is €1,290 through €19,250 and then:

```text
1290 × (24390 − taxable income) / (24390 − 19250)
```

until it reaches zero at €24,390. The household-members restriction and at
least €4,100 of qualifying net professional income are explicit inputs/bridges.
The separate marriage/legal-cohabitation-year branch uses the same €1,980 only
when spouse net resources are at most €4,100 and its Article 126 exception does
not apply.

### Article 134 §3 and EUROMOD columns

`tax_free_amount_tax.yaml` now implements the statutory component order and
converts only the unused tax value attributable to Article 132 items 1–6 into
the refundable child credit, capped at €570 per equivalent child (half under
Article 132bis). Disabled children contribute two equivalents. The page-186
module separately converts unused tax value attributable to the additional
Article 133 supplement and adds both paragraph-3 components.

EUROMOD `tintcch_s` maps to:

- individual: `belgium_pit_pilot_article_134_refundable_child_tax_credit`;
- couple: the sum of `belgium_pit_couple_spouse_{a,b}_refundable_child_tax_credit`.

The requested connector output did not contain `tintadch_s`; the Article 133
additional refundable component therefore has no emitted EUROMOD counterpart
in this run. It remains separate in Axiom as
`belgium_pit_pilot_article_134_refundable_article_133_additional_supplement_credit`.

## 4. EUROMOD BE_2025 oracle

Exact invocation:

```sh
arch -x86_64 env PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
  DOTNET_ROOT=/Users/maxghenis/.dotnet-x64 PYTHONNET_RUNTIME=coreclr \
  POLARS_SKIP_CPU_CHECK=1 \
  /Users/maxghenis/.venvs/axiom-euromod-x64/bin/python \
  scratch_lane_f_euromod_cases.py scratch_lane_f_euromod_cases.json
```

<details>
<summary>Verbatim EUROMOD driver</summary>

Save this block as `scratch_lane_f_euromod_cases.py` before running the
invocation above:

```python
#!/usr/bin/env python3
"""Lane F scratch driver: BE_2025 dependant/TFA cases."""
import json
import platform
import sys
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import numpy as np
import pandas as pd
from euromod import Model


MODEL_ROOT = Path("/Users/maxghenis/Downloads/EUROMOD_J2.0/EUROMOD_RELEASES_J2.0+")
TEMPLATE = MODEL_ROOT / "Input/BE_training_data.txt"
DATASET = "BE_2024_c1_2015_03_e2"
SYSTEM = "BE_2025"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("scratch_lane_f_euromod_cases.json")


def header_columns():
    with TEMPLATE.open(encoding="utf-8") as stream:
        return [name.strip() for name in stream.readline().rstrip("\n").split("\t") if name.strip()]


def blank_frame(rows, header):
    return pd.DataFrame(np.zeros((rows, len(header)), dtype=np.float64), columns=header)


def assign(frame, row, values):
    for name, value in values.items():
        if name not in frame.columns:
            raise RuntimeError(f"template missing {name!r}")
        frame.loc[row, name] = float(value)


def engine_run(system, frame):
    chatter = StringIO()
    with redirect_stdout(chatter):
        simulation = system.run(
            frame,
            DATASET,
            verbose=False,
            nowarnings=True,
            requested_vars=[],
            requested_incomelists=[],
            requested_vargroups=[],
            requested_ilgroups=[],
            suppress_other_output=False,
        )
    return simulation.outputs[0], [str(error) for error in list(getattr(simulation, "errors", []))]


def person_base(frame, row, household_id, person_id, age, marital_status, labour_status):
    assign(frame, row, {
        "idhh": household_id,
        "idperson": person_id,
        "idpartner": 0,
        "idmother": 0,
        "idfather": 0,
        "dag": age,
        "dgn": 1,
        "dms": marital_status,
        "dwt": 1,
        "les": labour_status,
        "lfs": 15 if labour_status in (3, 6, 7) else 0,
        "lhw": 0,
        "liwmy": 0,
        "liwwh": 540,
        "loc": 5,
        "drgn1": 0,
        "yemmy": 0,
    })


def add_worker(frame, row, household_id, person_id, wage, factor, marital_status=1, partner_id=0):
    person_base(frame, row, household_id, person_id, 35, marital_status, 3)
    assign(frame, row, {
        "idpartner": partner_id,
        "lhw": 38,
        "liwmy": 12,
        "yemmy": 12,
        "yem": wage / 12.0 / factor,
    })


def add_nonworker_partner(frame, row, household_id, person_id, partner_id):
    person_base(frame, row, household_id, person_id, 35, 2, 7)
    assign(frame, row, {"idpartner": partner_id})


def add_child(frame, row, household_id, person_id, mother_id, father_id, age=10):
    person_base(frame, row, household_id, person_id, age, 1, 6)
    assign(frame, row, {
        "idmother": mother_id,
        "idfather": father_id,
        "dec": 0,
        "xed00": 1,
    })


def main():
    if platform.machine() != "x86_64":
        raise RuntimeError(f"needs x86_64, got {platform.machine()}")
    header = header_columns()
    model = Model(str(MODEL_ROOT))
    country = next(country for country in model.countries if country.name == "BE")
    system = next(system for system in country.systems if system.name == SYSTEM)

    probe = blank_frame(1, header)
    person_base(probe, 0, 1, 101, 35, 1, 3)
    assign(probe, 0, {"lhw": 38, "liwmy": 12, "yemmy": 12, "yem": 1000})
    probe_out, probe_errors = engine_run(system, probe)
    wage_factor = float(probe_out.loc[0, "yem"]) / 1000.0

    cases = [
        {"label": "single_earner_couple_30k_1_child", "kind": "couple", "wages": [30000, 0], "children": 1},
        {"label": "single_earner_couple_30k_2_children", "kind": "couple", "wages": [30000, 0], "children": 2},
        {"label": "single_earner_couple_45k_1_child", "kind": "couple", "wages": [45000, 0], "children": 1},
        {"label": "single_earner_couple_45k_2_children", "kind": "couple", "wages": [45000, 0], "children": 2},
        {"label": "two_earner_couple_45k_30k_2_children", "kind": "couple", "wages": [45000, 30000], "children": 2},
        {"label": "single_parent_30k_1_child", "kind": "single", "wages": [30000], "children": 1},
        {"label": "low_single_parent_18k_2_children", "kind": "single", "wages": [18000], "children": 2},
    ]
    row_count = sum(len(case["wages"]) + case["children"] for case in cases)
    frame = blank_frame(row_count, header)
    row = 0
    membership = []
    for household_id, case in enumerate(cases, start=1):
        member_rows = []
        mother_id = household_id * 100 + 1
        if case["kind"] == "couple":
            father_id = household_id * 100 + 3
            add_worker(frame, row, household_id, mother_id, case["wages"][0], wage_factor, 2, father_id)
            member_rows.append(row)
            row += 1
            if case["wages"][1] > 0:
                add_worker(frame, row, household_id, father_id, case["wages"][1], wage_factor, 2, mother_id)
            else:
                add_nonworker_partner(frame, row, household_id, father_id, mother_id)
            member_rows.append(row)
            row += 1
        else:
            father_id = 0
            add_worker(frame, row, household_id, mother_id, case["wages"][0], wage_factor)
            member_rows.append(row)
            row += 1
        for child_index in range(case["children"]):
            child_id = household_id * 100 + 2 + child_index * 2
            add_child(frame, row, household_id, child_id, mother_id, father_id)
            member_rows.append(row)
            row += 1
        membership.append((case, member_rows))

    out, errors = engine_run(system, frame)
    want = [
        "idhh", "idperson", "yem", "tscee_s", "tsceerd_s", "tints_s", "tintatb_s",
        "tintatc_s", "tintatc01_s", "tintadch_s", "tintcly_s", "tintcch_s", "tinna_s",
        "tin_s", "tinrg_s", "tinmu_s", "ils_tax", "ils_taxsim",
    ]
    present = [name for name in want if name in out.columns]
    results = {
        "wage_uprating_factor": wage_factor,
        "probe_errors": probe_errors,
        "errors": errors,
        "missing_columns": [name for name in want if name not in out.columns],
        "cases": [],
    }
    for case, member_rows in membership:
        household = {"label": case["label"], "members": []}
        for member_row in member_rows:
            person_id = int(frame.loc[member_row, "idperson"])
            output_row = out.index[out["idperson"] == person_id][0]
            person = {"idperson": person_id}
            for column in present:
                value = float(out.loc[output_row, column])
                person[f"{column}_annual"] = value if column in ("idhh", "idperson") else value * 12.0
            household["members"].append(person)
        for column in present:
            if column in ("idhh", "idperson"):
                continue
            household[f"{column}_annual_sum"] = sum(member.get(f"{column}_annual", 0.0) for member in household["members"])
        results["cases"].append(household)
    OUT.write_text(json.dumps(results, indent=1) + "\n")
    print(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
```

</details>

The original output was recovered from the pre-cleanup sibling-layout copy and
the driver was rerun once after the final legal hardening. These commands prove
that the rerun is byte-identical:

```sh
shasum -a 256 \
  /private/tmp/lane-f-engine-matrix-final.MobyCj/rulespec-be/scratch_lane_f_euromod_cases.py \
  /private/tmp/lane-f-engine-matrix-final.MobyCj/rulespec-be/scratch_lane_f_euromod_cases.json \
  /private/tmp/lane-f-euromod-final-rerun.json
cmp -s \
  /private/tmp/lane-f-engine-matrix-final.MobyCj/rulespec-be/scratch_lane_f_euromod_cases.json \
  /private/tmp/lane-f-euromod-final-rerun.json
printf 'CMP_EXIT=%s\n' "$?"
# 13c414d5270115bd64af5eb16b8a721e2910b612417a9513918f37f66ec00143  .../scratch_lane_f_euromod_cases.py
# 5959a40cb2d455672fcc4060ebb0c1af467ec4fedf9c17e28a7e275638503242  .../scratch_lane_f_euromod_cases.json
# 5959a40cb2d455672fcc4060ebb0c1af467ec4fedf9c17e28a7e275638503242  /private/tmp/lane-f-euromod-final-rerun.json
# CMP_EXIT=0
```

The driver used model
`/Users/maxghenis/Downloads/EUROMOD_J2.0/EUROMOD_RELEASES_J2.0+`, system
`BE_2025`, dataset/configuration `BE_2024_c1_2015_03_e2`, and the
`BE_training_data` header. A probe produced the wage uprating factor
`1.055022392834293`; intended annual wages were assigned as
`annual / 12 / factor`.

Workers use `les=3`, `lhw=38`, `liwmy=yemmy=12`. Children are separate
household rows aged 10 with `idmother`/`idfather` populated, `les=6`, `lfs=15`,
`dec=0`, and `xed00=1`. A zero-earning partner uses `les=7`. `drgn1=0` keeps
regional and municipal components zero for this federal comparison.

The connector status came directly from:

```sh
jq '{wage_uprating_factor,probe_errors,errors,missing_columns,case_count:(.cases|length)}' \
  scratch_lane_f_euromod_cases.json
# wage_uprating_factor: 1.055022392834293
# probe_errors/errors, on both runs:
#   Variable(s) yds, lindi, yptmp, tad, tis not found ... (zero is used as default)
#   bunpe01, bunpe02, xcc, yempv, yiyitdp ... default factor (1.050524934383202)
# missing_columns: ["tintadch_s"]
# case_count: 7
```

Thus both the probe and the seven-case simulation returned the same two
warnings, retained rather than suppressed from the failure ledger. Requested
`tintadch_s` was absent; that is a missing output column, not a third warning.

The output table was produced by:

```sh
jq -r '["case","tints","tintatb","tintatc","tintatc01","tintcly","tintcch","tinna","tin"],
  (.cases[] | [.label,.tints_s_annual_sum,
    .tintatb_s_annual_sum,.tintatc_s_annual_sum,.tintatc01_s_annual_sum,
    .tintcly_s_annual_sum,.tintcch_s_annual_sum,.tinna_s_annual_sum,
    .tin_s_annual_sum]) | @tsv' scratch_lane_f_euromod_cases.json
```

| Case | `tints` | `tintatb` | `tintatc` | `tintatc01` | `tintcly` | `tintcch` | `tinna` | `tin` |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 30k+0, one child | 5,911.371375 | 23,547.525000 | 6,154.371375 | 6,255.361375 | 1,504.848888 | 100.990000 | 0 | -1,605.838888 |
| 30k+0, two children | 5,911.371375 | 23,547.525000 | 6,154.371375 | 7,507.361375 | 1,504.848888 | 1,140.000000 | 0 | -2,644.848888 |
| 45k+0, one child | 9,374.374070 | 23,800.000000 | 6,067.463067 | 6,067.463067 | 37.765406 | 0 | 2,481.605224 | 2,443.839818 |
| 45k+0, two children | 9,374.374070 | 26,930.000000 | 7,068.389202 | 7,068.389202 | 37.765406 | 0 | 1,730.480224 | 1,692.714818 |
| 45k+30k, two children | 18,069.117976 | 26,930.000000 | 6,960.500000 | 6,960.500000 | 1,542.614294 | 0 | 8,336.240188 | 6,793.625894 |
| Single parent 30k, one child | 6,971.010000 | 15,081.438278 | 3,951.431483 | 3,951.431483 | 1,504.848888 | 0 | 2,265.982306 | 761.133418 |
| Single parent 18k, two children | 3,150.000000 | 12,600.000000 | 3,207.000000 | 4,879.000000 | 1,504.848888 | 1,140.000000 | 0 | -2,644.848888 |

## 5. Identical-or-explained residual ledger

Sign convention is `Δ = Axiom − EUROMOD`: positive means more Axiom tax (or a
smaller refund). Axiom final-tax and credit components are exact expectations in
`couple_pit_oracle_pipeline.test.yaml` and
`pilot_worker_oracle_pipeline.test.yaml`, both executed by the 16-file command
in §6. EU values are read from the raw §4 JSON rather than copied into the
arithmetic. This command generated every delta, names every component, and
reports a closure error for each row:

```sh
jq -n --slurpfile oracle scratch_lane_f_euromod_cases.json '
  def eu($label): $oracle[0].cases[] | select(.label == $label);
  def row($label;$axiom_final;$axiom_work;$axiom_child;$axiom_article133):
    (eu($label)) as $e
    | ($axiom_final + $axiom_work + $axiom_child + $axiom_article133)
      as $axiom_pre_family
    | [
        {mechanism:"pre_family_reduced_state_tax_stage",
         amount:($axiom_pre_family - $e.tinna_s_annual_sum)},
        {mechanism:"work_bonus_credit",
         amount:($e.tintcly_s_annual_sum - $axiom_work)},
        {mechanism:"article_134_child_credit",
         amount:($e.tintcch_s_annual_sum - $axiom_child)},
        {mechanism:"article_133_additional_refundable_credit",
         amount:(0 - $axiom_article133)}
      ] as $parts
    | {case:$label, axiom:$axiom_final, euromod:$e.tin_s_annual_sum,
       delta_axiom_minus_euromod:($axiom_final - $e.tin_s_annual_sum),
       axiom_pre_family_reduced_state_tax:$axiom_pre_family,
       euromod_pre_family_reduced_state_tax:$e.tinna_s_annual_sum,
       parts:$parts, parts_sum:($parts | map(.amount) | add),
       closure_error:(($axiom_final - $e.tin_s_annual_sum)
         - ($parts | map(.amount) | add))};
  [
    row("single_earner_couple_30k_1_child";-1522.233168;952.233168;570;0),
    row("single_earner_couple_30k_2_children";-2092.233168;952.233168;1140;0),
    row("single_earner_couple_45k_1_child";2449.96259035;0;0;0),
    row("single_earner_couple_45k_2_children";1696.271972;0;0;0),
    row("two_earner_couple_45k_30k_2_children";7024.67638955;952.233168;0;0),
    row("single_parent_30k_1_child";932.5100211903696498054474707;952.233168;0;0),
    row("low_single_parent_18k_2_children";-2814.231;1158.231;1140;516)
  ]'
```

All seven absolute closure errors are below `7e-13`; that bound is the maximum
printed by the command, not a tax tolerance.

| Case | Axiom | EUROMOD | Δ | Exact decomposition |
|---|---:|---:|---:|---|
| 30k+0, one child | -1,522.233168 | -1,605.838888 | +83.605720 | +552.615720 work-bonus credit −469.010000 Article 134 child credit. Axiom's Article 134 §4 allocation produces €667.6405 unused child-TFA tax value and binds at €570; EU's `tintatc01−tintatc` and `tintcch` are €100.99. |
| 30k+0, two children | -2,092.233168 | -2,644.848888 | +552.615720 | Work-credit gap only; both child credits are €1,140. |
| 45k+0, one child | 2,449.962590 | 2,443.839818 | +6.122773 | −31.642633537 pre-family reduced-State-tax stage +37.765406115 work-bonus credit. |
| 45k+0, two children | 1,696.271972 | 1,692.714818 | +3.557154 | −34.208252473 pre-family reduced-State-tax stage +37.765406115 work-bonus credit. |
| 45k+30k, two children | 7,024.676390 | 6,793.625894 | +231.050496 | −359.330630532 pre-family reduced-State-tax stage +590.381126115 work-bonus credit. |
| Single parent 30k, one child | 932.510021 | 761.133418 | +171.376603 | −381.239116974 pre-family reduced-State-tax stage +552.615720 work-bonus credit. |
| Single parent 18k, two children | -2,814.231000 | -2,644.848888 | −169.382112 | +346.617888 work-credit gap −516.000000 Axiom Article 133-additional refundable credit; child credit is €1,140 in both. |

The recurring work-credit residual is the already-named worker-pipeline
mechanism: Axiom uses the encoded ONSS full-year equal-month A/B construction
and contribution cap, while EUROMOD's `tintcly_s` follows its own uprated
monthly work-bonus variables. The remaining `pre_family_reduced_state_tax_stage`
rows are dispositioned as the campaign's `engine_semantics` class: they compare
the exact stage immediately before the three family/work credit components and
are not mislabeled as family-column rounding. The single-parent row is further
decomposed below because Article 133's phaseout responds to that upstream base.

For the single-parent phaseout, this command isolates the mechanism:

```sh
jq -n --slurpfile oracle scratch_lane_f_euromod_cases.json '
  ($oracle[0].cases[] | select(.label == "single_parent_30k_1_child")) as $e
  | 22478.65 as $axiom_taxable
  | (16320 + ($e.tints_s_annual_sum - 16320 * 0.25) / 0.40)
    as $eu_taxable
  | (30000 - $e.tscee_s_annual_sum - $eu_taxable)
    as $eu_professional_expense
  | (932.5100211903696498054474707 + 952.233168)
    as $axiom_pre_family_state_tax
  | (6543.46 - $axiom_pre_family_state_tax / 0.75043)
    as $axiom_tfa_tax_reduction
  | {
      axiom_employee_ssc_deduction:1591.35,
      euromod_employee_ssc_deduction:$e.tscee_s_annual_sum,
      axiom_professional_expense_deduction:5930,
      euromod_inferred_professional_expense_deduction:$eu_professional_expense,
      taxable_effect_axiom_minus_euromod_from_ssc:
        ($e.tscee_s_annual_sum - 1591.35),
      taxable_effect_axiom_minus_euromod_from_professional_expense:
        (0 - (5930 - $eu_professional_expense)),
      axiom_taxable_income:$axiom_taxable,
      euromod_implied_taxable_income:$eu_taxable,
      net_taxable_income_difference:($axiom_taxable - $eu_taxable),
      axiom_article_133_additional:479.69678988326848249027237354,
      euromod_article_133_additional:
        ($e.tintatb_s_annual_sum - 10910 - 1980 - 1980),
      article_133_difference:
        (479.69678988326848249027237354
          - ($e.tintatb_s_annual_sum - 10910 - 1980 - 1980)),
      axiom_article_130_base_tax:6543.46,
      euromod_article_130_base_tax:$e.tints_s_annual_sum,
      base_tax_difference:(6543.46 - $e.tints_s_annual_sum),
      axiom_tfa_tax_reduction:$axiom_tfa_tax_reduction,
      euromod_tfa_tax_reduction:$e.tintatc_s_annual_sum,
      tfa_tax_reduction_difference:
        ($axiom_tfa_tax_reduction - $e.tintatc_s_annual_sum),
      reduced_state_tax_difference:
        ((6543.46 - $e.tints_s_annual_sum
          - ($axiom_tfa_tax_reduction - $e.tintatc_s_annual_sum)) * 0.75043)
    }'
```

It yields the complete causal chain. Axiom deducts €1,591.35 employee SSC
versus EUROMOD's €3,921, a +€2,329.65 effect on Axiom taxable income; Axiom
then deducts €5,930 of professional expenses versus EUROMOD's inferred
€2,531.475, a −€3,398.525 effect. Net: Axiom taxable income is
€22,478.65 versus €23,547.525, or −€1,068.875. That produces Article 133
additions of €479.696789883 versus €211.438278210 (difference
+€268.258511673). At the tax stage, the Article 130 base-tax difference is
−€427.55 and the TFA-tax-reduction difference is +€80.477553502; applying
the 0.75043 State share closes exactly to the −€381.239116974 stage component
in the residual table.

No residual is labeled “explained” merely because it is small: the €6.12 and
€3.56 cases are explicitly decomposed above.

## 6. Verification gates

Final companion, repository, and sibling-layout results are recorded here after
the last legal-hardening edit.

Companion tests, including the pilot and couple oracle matrices and explicit
false assignments for every local input:

```sh
AXIOM_RULESPEC_REPO_ROOTS="$PWD" \
  /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode \
  test --root "$PWD" \
  --axiom-rules-engine-path /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine \
  be/statutes/income_tax/individual/dependant_net_resources.test.yaml \
  be/statutes/income_tax/individual/dependant_household_conditions.test.yaml \
  be/statutes/income_tax/individual/dependant_article_145_exclusion.test.yaml \
  be/statutes/income_tax/individual/dependant_shared_custody.test.yaml \
  be/statutes/income_tax/individual/dependants.test.yaml \
  be/statutes/income_tax/individual/dependant_article_132_counts.test.yaml \
  be/statutes/income_tax/individual/article_133_isolated_taxpayer_supplement.test.yaml \
  be/statutes/income_tax/individual/article_133_supplements.test.yaml \
  be/statutes/income_tax/individual/article_134_additional_supplement_credit.test.yaml \
  be/statutes/income_tax/individual/tax_free_amount_tax.test.yaml \
  be/statutes/income_tax/individual/regional_autonomy_factor.test.yaml \
  be/statutes/income_tax/individual/pilot_worker_oracle_pipeline.test.yaml \
  be/statutes/income_tax/individual/couple_pit_oracle_pipeline.test.yaml \
  be/statutes/income_tax/individual/final_tax.test.yaml \
  be/policies/euromod_disposable_income_list.test.yaml \
  be/policies/euromod_tax_income_list.test.yaml --json
# {"success":true,"test_files":16,"cases":67,
#  "compiled_programs":16,"failures":[]}
```

Repository layout/provenance suite:

```sh
PYTHONDONTWRITEBYTECODE=1 \
  /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python \
  -m pytest -q -p no:cacheprovider tests/
# ............................. [100%]
# 29 passed in 11.24s
```

Full sibling-layout strict validation:

```sh
lane_f_validate_dir="$(mktemp -d /private/tmp/lane-f-final-validate.XXXXXX)"
rsync -a --exclude .git "$PWD/" "$lane_f_validate_dir/rulespec-be/"
ln -s /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine \
  "$lane_f_validate_dir/axiom-rules-engine"
ln -s /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin \
  "$lane_f_validate_dir/corpus-be-pin"
cd "$lane_f_validate_dir/rulespec-be"
AXIOM_CORPUS_REPO="$lane_f_validate_dir/corpus-be-pin" \
  /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode \
  validate \
  be/statutes/income_tax/individual/dependant_net_resources.yaml \
  be/statutes/income_tax/individual/dependant_household_conditions.yaml \
  be/statutes/income_tax/individual/dependant_article_145_exclusion.yaml \
  be/statutes/income_tax/individual/dependant_shared_custody.yaml \
  be/statutes/income_tax/individual/dependants.yaml \
  be/statutes/income_tax/individual/dependant_article_132_counts.yaml \
  be/statutes/income_tax/individual/article_133_isolated_taxpayer_supplement.yaml \
  be/statutes/income_tax/individual/article_133_supplements.yaml \
  be/statutes/income_tax/individual/article_134_additional_supplement_credit.yaml \
  be/statutes/income_tax/individual/tax_free_amount_tax.yaml \
  be/statutes/income_tax/individual/regional_autonomy_factor.yaml \
  be/statutes/income_tax/individual/pilot_worker_oracle_pipeline.yaml \
  be/statutes/income_tax/individual/couple_pit_oracle_pipeline.yaml \
  be/statutes/income_tax/individual/final_tax.yaml \
  --skip-reviewers --json
```

The fresh directory was
`/private/tmp/lane-f-final-validate.8lygtC/rulespec-be`. All 14 returned rows
had `ci_pass: true`, `all_passed: true`, and `errors: []`; the process exited 0.

## 7. Flat failure ledger

All failed attempts are listed rather than folded into the final green result:

1. GitNexus exploration was unavailable in this detached sandbox; repository
   exploration continued with read-only `rg`/`sed` commands.
2. Early Article 133 compilation exposed a Decimal/Money mismatch; the phase
   formula was typed as Money throughout before any expected value was accepted.
3. Initial new companions failed on missing explicit inputs and placeholder
   expectations. Every local input, including false judgments and empty
   relations, is now assigned.
4. Extending the worker graph caused existing `final_tax` and two policy
   companions to fail for newly inferred inputs; their full assignments were
   updated rather than defaulted.
5. An early couple composition collided with duplicate Article 134/base-TFA
   rules; duplicate local literals/rules were removed and canonical imports used.
6. A scratch matrix test placed at repository root failed because it had no
   adjacent module, and its placeholders failed by design. Its verified cases
   were promoted into the official companion; all scratch files were removed.
7. Early strict validations reported cross-source Article 133 proof atoms,
   ungrounded `11460`, pilot literal `46`, then autonomy forms `0.24957` and
   `24.957`, unused imports, and missing positive/zero-branch coverage. The
   resolution was page-scoped modules, canonical imports, the autonomy leaf,
   and explicit branch assertions—not waivers.
8. The first combined dependant validation missed derived-rule and zero-branch
   assertions; the companions now cover those branches.
9. The first repository suite after implementation failed four checks: two
   modules used plural `corpus_citation_paths`, root scratch YAML was stray, and
   singular source locators were consequently missing. Atomic page splitting
   and scratch removal fixed all four.
10. The first final repository rerun was `28 passed, 1 failed`: the complementary
    State-share parameter lacked its own formula proof atom. Adding the pinned
    decree atom produced the final green repository result in §6.
11. EUROMOD completed but reported the two defaulting/uprating warnings and
    missing `tintadch_s` described in §4. They are not represented as a clean,
    warning-free connector run.
12. The first legal-hardening validation summary tried to index the validator's
    top-level array as an object and failed with `Cannot index array with string
    "all_passed"`; the raw JSON rerun showed all six focused modules green.
13. A diagnostic checksum-grouping command used GNU `uniq -w` on the BSD tool
    and failed with `uniq: invalid option -- w`; the rerun grouped SHA-1 values
    with `awk` and found every recovered driver copy identical.
14. One documentation patch missed its context because the displayed `printf`
    newline had been escaped twice; a narrower `apply_patch` corrected the
    report without touching executable RuleSpec files.

One diagnostic shell query also failed on unmatched quoting; it produced no
data and changed no file. No network call, push, destructive git command,
workflow/toolchain edit, waiver, or oracle-coverage-pending edit was made.

## 8. Lane W population wiring

Lane W must preserve children and other dependants as Person records; counts
must not be precomputed on the tax unit. Emit one of these directed relations:

- individual/single-parent run:
  `pilot_worker_oracle_pipeline#relation.belgium_pit_pilot_dependent_of_taxpayer`;
- joint run:
  `couple_pit_oracle_pipeline#relation.belgium_pit_couple_dependent_of_tax_unit`.

For each related Person, emit all of the following, explicitly assigning false
when the population carries no positive evidence:

```text
dependant_net_resources:
  belgium_pit_dependent_gross_resources
  belgium_pit_article_143_disregarded_resources
  belgium_pit_dependent_has_probative_resource_expense_evidence
  belgium_pit_dependent_justified_resource_expenses
  belgium_pit_dependent_resources_are_worker_remuneration_or_profits
  belgium_pit_taxpayer_is_taxed_separately
  belgium_pit_dependent_is_child
  belgium_pit_dependent_is_disabled

dependants:
  belgium_pit_dependent_is_ascendant
  belgium_pit_dependent_is_collateral_within_second_degree
  belgium_pit_dependent_assumed_exclusive_or_main_support_of_taxpayer_during_childhood
  belgium_pit_dependent_is_part_of_taxpayer_household_on_assessment_year_january_1
  belgium_pit_dependent_child_all_taxable_income_is_cumulated_with_parents

dependant_household_conditions:
  belgium_pit_article_138_child_is_deemed_part_of_taxpayer_household
  belgium_pit_article_139_nonchild_is_deemed_part_of_taxpayer_household
  belgium_pit_multiple_separately_taxed_taxpayers_are_in_same_household
  belgium_pit_taxpayer_actually_directs_household

dependant_article_145_exclusion:
  belgium_pit_dependent_is_excluded_under_article_145

dependant_shared_custody:
  belgium_pit_article_132bis_child_is_dependent_of_one_taxpayer
  belgium_pit_article_132bis_taxpayers_do_not_form_same_household
  belgium_pit_article_132bis_both_taxpayers_meet_civil_code_maintenance_obligation
  belgium_pit_article_132bis_child_accommodation_is_equally_divided
  belgium_pit_article_132bis_qualifying_agreement_or_judicial_decision_exists
  belgium_pit_article_132bis_instrument_was_timely_registered_approved_or_rendered
  belgium_pit_article_132bis_no_maintenance_payment_is_deducted_for_child

dependant_article_132_counts:
  belgium_pit_dependent_child_is_under_age_three_on_assessment_year_january_1
  belgium_pit_taxpayer_claims_childcare_reduction_for_dependent_child
  belgium_pit_dependent_has_reached_age_66
  belgium_pit_dependent_has_at_least_nine_autonomy_points
  belgium_pit_dependent_dependency_is_certified_by_competent_body
```

At the individual pipeline root also emit:

```text
tax_free_amount#belgium_pit_taxpayer_disability_count
pilot_worker_oracle_pipeline#belgium_pit_pilot_taxpayer_assessed_separately
pilot_worker_oracle_pipeline#belgium_pit_pilot_only_article_133_permitted_household_members_on_january_1
pilot_worker_oracle_pipeline#belgium_pit_pilot_article_134_paragraph_3_exclusion_applies
```

For ordinary EUROMOD-style children, derive relation membership from household
`idhh` plus `idmother`/`idfather`; retain the child row even with zero income.
Map `dag` to under-three, `dec`/`les` and parent identifiers to the population's
dependency/household convention, disability evidence to the disability fact,
and all resource columns to gross resources and Article 143 disregard inputs.
Ordinary co-resident children have actual 1-January membership true; shared-
custody legal facts must not be inferred merely from two parent identifiers.
Concretely, a zero-resource ordinary co-resident child emits `is_child=true`,
all three nonchild-role facts false, actual 1-January membership true, both
Article 138/139 deeming facts false, Article 145 exclusion false, all seven
Article 132bis facts false, and zero gross/disregarded/justified resources with
both expense-selector facts false. Set the separately-taxed-taxpayer fact from
the enclosing single/joint pipeline; set under-three from `dag`; absent
evidence, childcare claim, disability, Article 137 cumulation, Article 140
multiple-separately-taxed-household, direction, elderly, autonomy, and
certification facts are false.
Where the transport lacks custody instruments, disability, deemed-household,
Article 145, or Article 143 detail, emit explicit false/zero facts and record the
population limitation.

## 9. Signed-release promotion blocker

The configured release is evidenced by:

```sh
rg -n 'axiom_corpus_release' .axiom/toolchain.toml
# axiom_corpus_release = "be-rulespec-2026-07-10"
# axiom_corpus_release_content_sha256 = "c1436c9f99882a819773bc2ccddf8c2a67e41efd24b0d0a408493ba5da39964a"
```

Per the campaign's authoritative release inventory, the affected missing
sources are:

- page-183: isolated Article 133 leaf and Article 132bis;
- page-188: Articles 136–137;
- page-189: Articles 138–140;
- page-190: Articles 141–143 leaf; and
- page-192: Article 145.

Pages 182 and 184–187 are present. Local sibling validation succeeds because it
uses the full pinned corpus checkout. CI against the signed release will remain
blocked until a newly signed promotion release includes the five missing page
keys and the rulespec toolchain is intentionally repinned by the authorized
release workflow.

## 10. Commit handoff

The RuleSpec implementation is commit
`30f979b10cf381acd5a3f78618e6b5b831f0b671`, whose parent and subject are
reproduced by the §1 command. This evidence report is added as the lane's final
local handoff commit with:

```sh
git add LANE_F_REPORT.md
git commit -m "Document Lane F verification and population wiring"
```

No push was made from this lane session.

LANE F DONE
