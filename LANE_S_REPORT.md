# Lane S — self-employment PIT and separately taxed income

## Outcome

Lane S adds a Person-scoped self-employment PIT composition and an Article 171
tin-side composition. The self-employment path imports the existing
self-employed social-contribution, Article 51 forfait, worker, ordinary-rate,
tax-free-amount, autonomy, and local-tax surfaces. The Article 171 path imports
the conformant movable-income rules and six page-scoped fixed-rate modules.
Every new module returns `ci_pass: true`; the final integrated regression run
passes 46 cases in 13 suites with no failures. [V1] [V4]

The pinned corpus is clean at
`8e48989c9e46faa6d85a9624b7a2ebda0880656d`; the consolidated CIR92 PDF SHA-256
is `2cfa02443064f4f4714211a2d6570c5f9f46c360af715f9ffb6c7a0e8f582ffc`.
[S1]

## Corpus and legal resolution

### Self-employment

Article 51 pages 121–122 state that the forfait base is gross professional
income after personal social contributions and, for the business-profit
(`bénéfices`) branch, purchase costs. The imported
profit schedule is 28.7% through EUR 7,540, 10% through EUR 14,970, 5% through
EUR 24,920, and 3% above that, capped at EUR 5,210. Business profits use 30%,
capped at EUR 5,930. [S2]

Article 49 on page 120 supplies the actual-cost boundary; page 123 identifies
personal social contributions as professional expenses. The pipeline therefore
orders gross self-employment income → imported self-employed contribution →
business-profit-only purchase costs → actual-or-forfait selection → net professional income → the
imported Articles 130/131/134 chain → regional and local additions. [S3]

The existing integration point is
`belgium_self_employed_selected_annual_social_contribution`. For the tested
income year its imported first rate is 20.5%; the base secondary-activity
exemption is EUR 405.60 and the imported Article 14 index factor is supplied at
runtime. [S2] [R1]

A bare EUROMOD `yse` does not distinguish business profits from liberal-
profession/other profits and is already net of non-SSC business expenses in the
oracle cases. The pipeline therefore exposes both the category and the
Article 49 actual-cost choice as named boundaries. [E1] [R1]

### Article 171

The fixed-rate table is split by the singular pinned page that grounds it, as
required by this repository's provenance contract. [A1] [V3]

| Article 171 row | Encoded rate | Corpus page | Status |
|---|---:|---:|---|
| item 1 | 33% | 268 | encoded |
| item 1bis | 8% | 269 | encoded |
| item 2 | 10% | 269 | encoded |
| item 2bis | 15% | 270 | encoded |
| item 2quater | 18% | 270 | encoded |
| item 3 | 30% | 271 | encoded, with movable income imported |
| item 3bis | 20% | 271 | encoded |
| item 3quater | 15% | 271 | encoded |
| item 3sexies | 20% / 15% | 272 | encoded as two source-class bases |
| item 3septies | 5% / 20% | 272 | encoded by at-least-five / under-five-year bases |
| item 4 | 16.5% | 272 | encoded |
| item 7 | 10.38% | 275 | encoded |
| item 8 | 0% | 275 | encoded |

All values and page numbers in this table are emitted by [A1].

The Article 171 boundaries are explicit rather than silently generalized:

- Item 3quinquies uses the imported regulated-savings 15% surface; general
  movable income uses the imported 30% capital-income surface. [A2] [R1]
- Item 3ter's inherited movable rate, item 5's prior-full-year average rate,
  and item 6's other-income rate are dynamic supplied rates. Their statutory
  bases remain named supplied row scopes. [S4]
- Item 2ter is an ellipsis in the pinned consolidation and is a supplied-tax
  boundary: `unencoded_corpus_blocked`. [S4]
- Item 4bis prints `12, 5 %` in the pinned extracted page. Because the numeric
  grounding gate does not recognize that split decimal as 12.5%, its rate is a
  named supplied boundary: `unencoded_corpus_blocked`. The tax multiplication
  and class scope are encoded. [F2] [S4]
- Every row/subitem aggregate base is supplied after all applicable Articles
  171/1 and 172–174/1 classification, limitation, holding-period, write-down,
  and prorating rules: `input_carrying`. [S4]
- The Article 171 opening comparison is a supplied **State-tax** comparison,
  not a final-tax comparison. Its alternative is a consistent incremental
  ordinary State-tax amount. [S4]
- Private-pricaf item 3sexies dividends are not forced into 15%. The caller
  assigns them to the 20% or 15% source-class base according to the underlying
  Article 269 class. [S4]
- Article 466's nonprofessional-movable exclusion share and the resulting local
  additional-tax base increment are both exposed. [S5] [R1]

## EUROMOD verification

The oracle is `BE_2025` with dataset `BE_2024_c1_2015_03_e2`. Annual labour
inputs were divided by `12 × 1.055022392834293`; `yiy` was divided by
`12 × 1.0710267229254573`, so EUROMOD uprating returns the same annual gross.
[E1]

| Case | EUROMOD annual result | RuleSpec annual result | Disposition |
|---|---:|---:|---|
| `yse=25000` | SSC 5125; taxable 19875; tax 2030.3371518803276 | SSC 5125; taxable 19875; tax 2030.337151880326415 | MATCHED to the cent; EUR 880 self-activity credit is `input_carrying` |
| `yse=45000` | SSC 9225; taxable 35775; tax 10163.204158431827 | SSC 9225; taxable 35775; tax 10163.2041584318275275 | MATCHED to the cent |
| `yse=70000` | SSC 14350; taxable 55650; tax 20059.554882076052 | SSC 14350; taxable 55650; tax 20059.554882076053225 | MATCHED to the cent |
| `yem=30000, yse=20000` | taxable 39833.2858; tax 10507.62779506539 | taxable 38378.65; tax 10398.345773764672415475 | EXPLAINED `engine_semantics`; EUROMOD minus RuleSpec = 109.28202130071870734370 |
| `yiy=10000` | `tin_s=0`; `tinkt_s=3000`; total tax 3000 | imported movable tax 3000; Article 466 increment 0; tin total 3000 | MATCHED to the cent |

EUROMOD values and inputs in this table are emitted by [E1]; RuleSpec values are
emitted by [R1] and execution equality is established by [V1]. The mixed-case
residual is emitted and decomposed by [D1].

### Mixed-income residual decomposition

The residual is explained, not fitted:

- The existing RuleSpec secondary-activity contribution is EUR 4,100. EUROMOD
  applies an excess-only schedule, `(20000 - 1881.76) × 20.5%`, yielding
  EUR 3,714.2392. RuleSpec self-employment net income is therefore lower by
  EUR 385.7608. [D2]
- The existing RuleSpec worker net is EUR 22,478.65 versus EUROMOD
  EUR 23,547.525. EUROMOD employee SSC net of its reduction is
  `3921 - 3398.52 = 522.48`; RuleSpec employee SSC is EUR 1,591.35, a
  EUR 1,068.87 difference. RuleSpec's worker forfait is EUR 5,930 versus
  EUROMOD EUR 5,929.995, another EUR 0.005. Together these lower RuleSpec
  worker net by EUR 1,068.875. [E1] [D2] [R1]
- Those mechanisms sum to a RuleSpec taxable-base difference of
  `-385.7608 + -1068.875 = -1454.6358`. [D1]
- Holding the RuleSpec credit fixed and moving to EUROMOD's taxable base adds
  EUR 701.52028842471870734370 of tax. Moving from the RuleSpec activity credit
  of EUR 952.233168 to EUROMOD's EUR 1,504.848888 then removes
  EUR 592.238267124, including its effect on the communal base. Net:
  `701.52028842471870734370 - 592.238267124 = 109.28202130071870734370`.
  [D1]

## Verification results

- Both root modules compile. The self-employment root has 261 transitive rules;
  the Article 171 root has 50. [V2]
- The final integrated run covers 13 suites and 46 cases, with no failures.
  [V1]
- Proof validation passes all 8 new modules, checking 19 atoms with no issues.
  [V3]
- Repository layout and provenance tests pass 29 tests. [V3]
- Full sibling-layout validation returns `ci_pass: true`, `all_passed: true`,
  and an empty error list for every one of the 8 new modules. [V4]
- `git diff --check` exits successfully. [V5]

## Failures encountered

- A connector import without `PYTHONNET_RUNTIME=coreclr` failed with
  `Could not find libmono`; all oracle runs used the pinned x64/coreclr command
  in [E1]. [F1]
- The first exact-decimal fixture run failed because expected values had been
  seeded from binary-float display. Expected strings were replaced by the
  engine's canonical decimal outputs; the final execution gate is [V1]. [F1]
- The first proof-validation run failed because cross-page proof atoms were
  paired with a single page locator. The rates were split into singular,
  page-scoped modules and the integration roots now contain only same-page proof
  atoms. The repaired proof gate is [V3]. [F1]
- The first full validation returned `ci_pass: false` for Article 171 because
  `0.125` was not recognized in source text printed as `12, 5 %`. Item 4bis is
  now the explicit corpus-blocked boundary described above; [V4] is the clean
  rerun. [F2]
- Treating virtual corpus citation paths as physical files initially produced
  `No such file or directory`. Resolution used the pinned JSONL provision file
  and its `citation_path` field. [F3]

## Lane W wiring notes

1. Keep all new computations Person-scoped. Aggregate only through an explicit
   relation plus `sum_where`; do not connect Person outputs directly to a tax
   unit or household.
2. Neutralize EUROMOD input uprating with the factors in [E1]. Feed annual
   `yse` to `belgium_self_employed_gross_professional_income` and set the
   existing contribution-category flags explicitly.
3. For EUROMOD-parity `yse`, set the Article 49 actual-expense selector true and
   additional actual expenses and business purchase costs to zero. For genuine
   gross business-profit inputs, supply applicable purchase costs or select the Article 51 forfait and
   the business-profit-versus-profit category boundary. Populate the imported
   SSC module's professional-expense, loss, and reference-year netting inputs
   according to its own contribution-base semantics; they are not inferred
   from the PIT actual-cost boundary.
4. Feed `yem` to the imported worker surface and its work-bonus reference input.
   The mixed-case residual above must remain classified `engine_semantics`; do
   not alter either imported contribution module to erase it.
5. The EUR 880 low-activity credit in the low `yse` oracle is not encoded here.
   Carry the corresponding EUROMOD credit into
   `belgium_pit_self_employment_supplied_low_activity_income_refundable_credit`:
   `input_carrying`. [E1] [R1]
6. Feed `yiy` to the existing
   `belgium_capital_income_taxable_movable_income` input. EUROMOD exposes this
   liability in `tinkt_s`, not `tin_s`; ledger total tax is the sum, as shown by
   the EUR 3,000 oracle. [E1] [R1]
7. Supply every Article 171 row base only after its named eligibility and
   limitation scope. Keep item 2ter and item 4bis classified
   `unencoded_corpus_blocked`; keep the three dynamic rates and the State-tax
   comparison classified `input_carrying`.
8. For communal integration, feed
   `belgium_pit_article_171_selected_separate_or_globalised_tax` to the
   self-employment pipeline's Article 466 separately-taxed amount and feed the
   nonprofessional-movable share to its exclusion input. Then feed the
   self-employment federal/regional/local output into the Article 171 supplied
   ordinary-tax input and add the selected Article 171 liability exactly once.
   The movable-only oracle has an Article 466 increment of zero. [R1]

## Command ledger

### [S1] Corpus pin and PDF digest

```bash
git -C /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin rev-parse HEAD
git -C /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin status --short
shasum -a 256 /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/data/corpus/sources/be/statute/2026-06-30-be-income-tax-consolidated/official-documents/be-cir92-fisconetplus-current-code-2025-income.pdf
```

### [S2] Existing SSC and Article 51 parameters

```bash
/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
import json, yaml
from pathlib import Path
for rel in (
    "be/regulations/social_security/self_employed/contributions.yaml",
    "be/statutes/income_tax/professional_expenses/article_51_forfaits.yaml",
):
    payload = yaml.safe_load(Path(rel).read_text())
    for rule in payload["rules"]:
        if any(token in rule["name"] for token in (
            "article_12_first_rate", "secondary_exemption_threshold_base",
            "article_14_index_base", "article_51_profit_",
            "article_51_employee_forfait_rate",
            "article_51_employee_and_business_profit_cap",
            "article_51_assisting_spouse_and_profit_cap",
        )):
            print(json.dumps({"file": rel, "rule": rule["name"],
                              "formula": rule["versions"][0]["formula"].strip()},
                             sort_keys=True))
PY
```

### [S3] Article 49/51/52 corpus pages

```bash
jq -r 'select(.citation_path | test("/page-(120|121|122|123)$")) |
  [.citation_path, .body] | @tsv' \
  /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/data/corpus/provisions/be/statute/2026-06-30-be-income-tax-consolidated.jsonl
```

### [S4] Article 171 and follow-on corpus pages

```bash
jq -r 'select(.citation_path | test("/page-(268|269|270|271|272|273|274|275|276|277|463)$")) |
  [.citation_path, .body] | @tsv' \
  /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/data/corpus/provisions/be/statute/2026-06-30-be-income-tax-consolidated.jsonl
```

### [S5] Article 466 corpus pages

```bash
jq -r 'select(.citation_path | test("/page-(686|687|688)$")) |
  [.citation_path, .body] | @tsv' \
  /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/data/corpus/provisions/be/statute/2026-06-30-be-income-tax-consolidated.jsonl
```

### [A1] Encoded fixed-rate inventory

```bash
/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
import json, yaml
from pathlib import Path
base = Path("be/statutes/income_tax/individual/article_171_rates")
for path in sorted(p for p in base.glob("page_*.yaml")
                   if not p.name.endswith(".test.yaml")):
    payload = yaml.safe_load(path.read_text())
    citation = payload["module"]["source_verification"]["corpus_citation_path"]
    for rule in payload["rules"]:
        print(json.dumps({"citation": citation,
                          "rate": rule["versions"][0]["formula"].strip(),
                          "rule": rule["name"]}, sort_keys=True))
PY
```

### [A2] Existing movable-income surfaces

```bash
/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode test \
  --root "$PWD" \
  --axiom-rules-engine-path /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine \
  be/statutes/income_tax/movable_withholding/rates.test.yaml \
  be/statutes/income_tax/individual/movable_income.test.yaml --json
```

### [E1] EUROMOD five-case oracle

```bash
arch -x86_64 env \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  DOTNET_ROOT=/Users/maxghenis/.dotnet-x64 \
  PYTHONNET_RUNTIME=coreclr \
  POLARS_SKIP_CPU_CHECK=1 \
  /Users/maxghenis/.venvs/axiom-euromod-x64/bin/python - <<'PY' 2>&1 | rg '^\{"annual_outputs"'
import json
from pathlib import Path
import numpy as np
import pandas as pd
from euromod import Model

ROOT = Path("/Users/maxghenis/Downloads/EUROMOD_J2.0/EUROMOD_RELEASES_J2.0+")
DATASET = "BE_2024_c1_2015_03_e2"
SYSTEM = "BE_2025"
TEMPLATE = ROOT / "Input/BE_training_data.txt"
LABOUR_FACTOR = 1.055022392834293
CAPITAL_FACTOR = 1.0710267229254573
with TEMPLATE.open(encoding="utf-8") as stream:
    header = [name.strip() for name in stream.readline().rstrip("\n").split("\t") if name.strip()]
model = Model(str(ROOT))
country = next(country for country in model.countries if country.name == "BE")
system = next(system for system in country.systems if system.name == SYSTEM)
base = {
    "idhh": 1, "idperson": 101, "idpartner": 0, "idmother": 0, "idfather": 0,
    "dag": 35, "dgn": 1, "dms": 1, "drgn1": 2, "dwt": 1, "les": 0,
    "lfs": 0, "lhw": 0, "liwmy": 0, "liwwh": 0, "loc": 5, "poa": 0,
    "yem": 0, "yemmy": 0, "yse": 0, "yiy": 0,
}
cases = [
    ("yse_25000", {"yse": 25000 / 12 / LABOUR_FACTOR}),
    ("yse_45000", {"yse": 45000 / 12 / LABOUR_FACTOR}),
    ("yse_70000", {"yse": 70000 / 12 / LABOUR_FACTOR}),
    ("mixed_yem_30000_yse_20000", {
        "les": 3, "lfs": 15, "lhw": 38, "liwmy": 12, "liwwh": 120,
        "yem": 30000 / 12 / LABOUR_FACTOR, "yemmy": 12,
        "yse": 20000 / 12 / LABOUR_FACTOR,
    }),
    ("yiy_10000", {"yiy": 10000 / 12 / CAPITAL_FACTOR}),
]
outputs = [
    "yem", "yse", "yiy_s", "tscee_s", "tsceerd_s", "tscse_s", "tintace_s",
    "il_taxabley", "tinna_s", "tinrg_s", "tintcly_s", "tinkt_s", "tinmu_s",
    "tin_s", "ils_tax",
]
for case_id, overrides in cases:
    row = dict(base)
    row.update(overrides)
    frame = pd.DataFrame(np.zeros((1, len(header)), dtype=np.float64), columns=header)
    for name, value in row.items():
        frame.loc[0, name] = float(value)
    result = system.run(
        frame, DATASET, verbose=False, nowarnings=True, requested_vars=[],
        requested_incomelists=[], requested_vargroups=[], requested_ilgroups=[],
        suppress_other_output=False,
    ).outputs[0].iloc[0]
    annual = {name: float(result[name]) * 12 for name in outputs if name in result.index}
    monthly_inputs = {name: row[name] for name in ("yem", "yse", "yiy") if row[name]}
    print(json.dumps({"annual_outputs": annual, "case_id": case_id,
                      "monthly_inputs": monthly_inputs}, sort_keys=True))
PY
```

### [R1] RuleSpec fixture outputs and execution

```bash
/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode test \
  --root "$PWD" \
  --axiom-rules-engine-path /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine \
  be/statutes/income_tax/individual/self_employed_oracle_pipeline.test.yaml \
  be/statutes/income_tax/individual/separately_taxed_income.test.yaml --json

/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
import json, yaml
from pathlib import Path
root = Path("be/statutes/income_tax/individual")
for filename in ("self_employed_oracle_pipeline.test.yaml",
                 "separately_taxed_income.test.yaml"):
    for case in yaml.safe_load((root / filename).read_text()):
        if case["name"].startswith("euromod_") or case["name"].startswith("mixed_"):
            print(json.dumps({"case": case["name"], "output": case["output"]},
                             sort_keys=True, default=str))
PY
```

### [D1] Mixed-case downstream decomposition

```bash
/usr/bin/python3 - <<'PY'
from decimal import Decimal as D, getcontext
getcontext().prec = 40
T1,T2,T3 = map(D, ("16320","28800","49840"))
R1,R2,R3,R4 = map(D, (".25",".40",".45",".50"))
TFA_TAX = D("2727.5")
STATE_SHARE, REGION, LOCAL = map(D, (".75043",".33257",".0717"))
def tax(taxable, credit):
    x, c = D(taxable), D(credit)
    if x <= T1: gross=x*R1
    elif x <= T2: gross=T1*R1+(x-T1)*R2
    elif x <= T3: gross=T1*R1+(T2-T1)*R2+(x-T2)*R3
    else: gross=T1*R1+(T2-T1)*R2+(T3-T2)*R3+(x-T3)*R4
    state=max(D(0),gross-TFA_TAX)*STATE_SHARE
    after=state+state*REGION-c
    return after+max(D(0),after)*LOCAL
a=tax("38378.65","952.233168")
b=tax("39833.2858","952.233168")
c=tax("39833.2858","1504.848888")
print("rulespec_tax",a)
print("counterfactual_eu_taxable_rulespec_credit",b)
print("counterfactual_eu_taxable_eu_credit",c)
print("taxable_base_mechanism_eu_minus_rulespec",b-a)
print("credit_mechanism_eu_minus_rulespec",c-b)
print("total_eu_minus_rulespec",c-a)
print("taxable_delta_rulespec_minus_eu",D("38378.65")-D("39833.2858"))
print("credit_delta_rulespec_minus_eu",D("952.233168")-D("1504.848888"))
PY
```

### [D2] Imported schedule components

```bash
/usr/bin/python3 - <<'PY'
from decimal import Decimal as D
print(D("405.60")*D("4.639439281617473"))
print((D("20000")-D("1881.76"))*D(".205"))
print(D("3921")-D("3398.52"))
print(D("1591.35")-(D("3921")-D("3398.52")))
print(D("5930")-D("5929.995"))
PY
```

### [V1] Final integrated tests

```bash
/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode test \
  --root "$PWD" \
  --axiom-rules-engine-path /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine \
  be/regulations/social_security/self_employed/contributions.test.yaml \
  be/statutes/income_tax/professional_expenses/article_51_forfaits.test.yaml \
  be/statutes/income_tax/individual/pilot_worker_oracle_pipeline.test.yaml \
  be/statutes/income_tax/movable_withholding/rates.test.yaml \
  be/statutes/income_tax/individual/movable_income.test.yaml \
  be/statutes/income_tax/individual/article_171_rates/page_268.test.yaml \
  be/statutes/income_tax/individual/article_171_rates/page_269.test.yaml \
  be/statutes/income_tax/individual/article_171_rates/page_270.test.yaml \
  be/statutes/income_tax/individual/article_171_rates/page_271.test.yaml \
  be/statutes/income_tax/individual/article_171_rates/page_272.test.yaml \
  be/statutes/income_tax/individual/article_171_rates/page_275.test.yaml \
  be/statutes/income_tax/individual/self_employed_oracle_pipeline.test.yaml \
  be/statutes/income_tax/individual/separately_taxed_income.test.yaml --json
```

### [V2] Root compiles

```bash
AXIOM_RULESPEC_REPO_ROOTS="$PWD" \
  /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode compile \
  --as-of 2025-01-01 --json \
  --axiom-rules-engine-path /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine \
  "$PWD/be/statutes/income_tax/individual/self_employed_oracle_pipeline.yaml"
AXIOM_RULESPEC_REPO_ROOTS="$PWD" \
  /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode compile \
  --as-of 2025-01-01 --json \
  --axiom-rules-engine-path /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine \
  "$PWD/be/statutes/income_tax/individual/separately_taxed_income.yaml"
```

### [V3] Proof and repository gates

```bash
AXIOM_CORPUS_REPO=/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin \
  /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode \
  proof-validate --require-money-atoms --money-atom-root "$PWD" --json \
  be/statutes/income_tax/individual/article_171_rates/page_{268,269,270,271,272,275}.yaml \
  be/statutes/income_tax/individual/self_employed_oracle_pipeline.yaml \
  be/statutes/income_tax/individual/separately_taxed_income.yaml
PYTHONDONTWRITEBYTECODE=1 pytest -q -p no:cacheprovider tests/test_repository_layout.py
```

### [V4] Full sibling-layout validation

```bash
lane_s_validate_dir="$(mktemp -d /private/tmp/lane-s-validate-final.XXXXXX)"
rsync -a --exclude .git "$PWD/" "$lane_s_validate_dir/rulespec-be/"
ln -s /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine "$lane_s_validate_dir/axiom-rules-engine"
ln -s /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin "$lane_s_validate_dir/corpus-be-pin"
cd "$lane_s_validate_dir/rulespec-be"
AXIOM_CORPUS_REPO="$lane_s_validate_dir/corpus-be-pin" \
  /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode validate \
  be/statutes/income_tax/individual/article_171_rates/page_{268,269,270,271,272,275}.yaml \
  be/statutes/income_tax/individual/self_employed_oracle_pipeline.yaml \
  be/statutes/income_tax/individual/separately_taxed_income.yaml \
  --skip-reviewers --json
```

### [V5] Worktree check

```bash
git diff --check
git status --short --branch
rg -n "self_employed_oracle_pipeline|separately_taxed_income|article_171_rates" \
  --glob '*.yaml' --glob '*.md' .
```

### [F1] Early connector, fixture, and proof failures

```bash
# Failed without coreclr: Could not find libmono.
arch -x86_64 /Users/maxghenis/.venvs/axiom-euromod-x64/bin/python -c 'from euromod import Model'

# First exact-decimal fixture run; failed assertions were replaced by canonical engine decimals.
/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode test \
  --root "$PWD" \
  --axiom-rules-engine-path /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine \
  be/statutes/income_tax/individual/self_employed_oracle_pipeline.test.yaml \
  be/statutes/income_tax/individual/separately_taxed_income.test.yaml --json

# First proof run; failed on proof atoms outside single-page module locators.
AXIOM_CORPUS_REPO=/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin \
  /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode \
  proof-validate --require-money-atoms --money-atom-root "$PWD" --json \
  be/statutes/income_tax/individual/self_employed_oracle_pipeline.yaml \
  be/statutes/income_tax/individual/separately_taxed_income.yaml
```

### [F2] First full-validation failure

```bash
# Earlier source returned:
# ci: Ungrounded generated numeric literal: 0.125 does not appear as a substantive numeric value in the source text.
AXIOM_CORPUS_REPO=/private/tmp/lane-s-validate.8BO1wT/corpus-be-pin \
  /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode validate \
  be/statutes/income_tax/individual/self_employed_oracle_pipeline.yaml \
  be/statutes/income_tax/individual/separately_taxed_income.yaml \
  --skip-reviewers --json
```

### [F3] Virtual-path lookup failure and JSONL resolution

```bash
ls /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/be/statute/fisconetplus/cir92/revenus-2025/page-121
rg -n "page-121" /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/be/statute/fisconetplus/cir92/revenus-2025
jq -r 'select(.citation_path == "be/statute/fisconetplus/cir92/revenus-2025/page-121") |
  [.citation_path, .body] | @tsv' \
  /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/data/corpus/provisions/be/statute/2026-06-30-be-income-tax-consolidated.jsonl
```

LANE S DONE
