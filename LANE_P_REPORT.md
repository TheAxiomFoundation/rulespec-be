# Lane P — pensions & replacement-income PIT

Run date: 2026-08-22. Branch `ledger/pensions`, worktree
`~/TheAxiomFoundation/_cape-prep/beP/rulespec-be`, off main `7c85808`.
Local commit: **`2c84eb9`** ("Encode pensioner PIT pipeline with arts. 146-154
reduction machinery"). Nothing pushed.

## 1. Executive summary

- New module `be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml`
  (+ companion `.test.yaml`, 10 cases): Person-scoped path gross art. 34 pension →
  art. 191 AMI + art. 68 solidarity withholdings → art. 23 §2 netting → art. 6
  taxable income (+ worker pilot net professional income for working pensioners) →
  arts. 130/131/134 → **arts. 147/151-1/152/153 reduction machinery** (incl. the
  art. 147 al. 1 2° b/c activity-income exclusions) → art. 5/2 autonomy factor →
  work-bonus credit → supplied communal/agglomeration additions.
- **EUROMOD BE_2025 single-pensioner cases match to the cent** (three of three);
  `tscpe_s` (pensioner SSC) matches exactly on all four cases. The mixed
  pension+wage case's −352.30 residual **decomposes to the cent into two named
  EUROMOD-side mechanisms** (§4).
- Art. 154 is **correctly absent for pensioners**: the AY2026 statutory text
  grants the complementary reduction only when unemployment benefits are present
  (verified against corpus pages 256–258); EUROMOD BE_2025 has the corresponding
  function blocks switched off. The lane's original framing ("the 154 additional
  reduction floor") does not bind for pension-only cases at this vintage.
- Gates: companion tests 10/10; repository layout tests 29/29; pinned-corpus
  sibling-layout validate **`ci_pass: true`** (same bar as the merged couple
  pipeline; the merged pilot-worker, tax_reductions, and non_labour modules do
  NOT pass that validator at this pin — baseline evidence in §6).

## 2. Corpus resolution (pin 8e48989c, `AXIOM_CORPUS_REPO=corpus-be-pin`)

Resolver learned from the pinned encoder: provisions live in
`corpus-be-pin/data/corpus/provisions/<jur>/<class>/*.jsonl`, records keyed by
`citation_path`; the CIR92 consolidation is one document,
`be/statute/fisconetplus/cir92/revenus-2025/page-N`, in
`be/statute/2026-06-30-be-income-tax-consolidated.jsonl` (744 records).

Command that located the reduction sub-section (every page below re-read in full):

```sh
python3 - <<'PY'
import json
F='corpus-be-pin/data/corpus/provisions/be/statute/2026-06-30-be-income-tax-consolidated.jsonl'
for line in open(F):
    r = json.loads(line)
    body = r.get('body') or ''
    for art in ['Art. 146','Art. 147','Art. 148','Art. 150','Art. 151','Art. 152','Art. 153','Art. 154']:
        if art in body: print(art, r['citation_path'])
PY
```

| Provision | Page | Content used |
|---|---|---|
| Art. 146 (definitions) | page-252 | pensions = art. 34 pensions/rentes/allocations en tenant lieu |
| Art. 147 al. 1 1°/2° | page-253 | base 2 219,27 + additional 457,23; proration to net-pension share; 2° a/b/c exclusions |
| Art. 147 al. 2–4 | page-254 | "revenus d'activités" definition; c) proration formula; King's top-up clause |
| Arts. 148/149 | page-254 | abrogés |
| Art. 150 | page-255 | joint assessment → per-taxpayer computation |
| Art. 151 | page-255 | unemployment phase-out (28 780→35 930) — out of slice |
| Art. 151/1 | page-255 | additional-reduction phase-out 19 630→28 780, zero at/above |
| Art. 152 | page-256 | 1/3 floor at/above 57 560; linear majoration from 28 780 |
| Art. 153 | page-256 | per-category cap at the attributable share of the arts. 130-145 tax |
| Art. 154 §§1–4 | page-256..258 | complementary reduction **requires unemployment benefits** (both §1 branches) |
| Art. 23 §2 / art. 52 7° | page-73 / page-123 | per-category netting of personal social-legislation withholdings |
| Art. 51 | page-121..122 | forfait applies to rémunérations/bénéfices/profits net of *their own* contributions — not pensions |
| Pension withholding 2025 guidance | `be/guidance/sfp/pension-withholding/2025/ami-and-solidarity-contribution/block-4/5/11/12` | SFP AMI + solidarity tables (already proven inside `non_labour_income_contributions`) |

Self-consistency check at the pin: 2 219,27 + 457,23 = **2 676,50** = the
arts. 130-134 tax at taxable 19 630 (25 %×16 320 + 40 %×3 310 − 2 727,50), i.e.
the art. 147 al. 4 zero-tax calibration holds and no King's top-up applies for
AY2026. (Computed by hand from page-181/185 amounts; reproduced by the engine:
the 15k case's remaining tax is fully consumed.)

## 3. Module map

`pensioner_pit_oracle_pipeline.yaml` — all rules Person-scoped, `belgium_pit_pensioner_*`:

| Stage | Rules | Grounding |
|---|---|---|
| Monthly bridge | `monthly_gross_pension` = annual input / 12 | months param imported from non_labour |
| Art. 191 AMI | `article_191_protected_floor_limit_monthly`, `article_191_full_rate_threshold_monthly` (isolated/charge-de-famille selectors), `article_191_monthly_withholding` (0 / excess-over-floor / 3.55 %) | all money values imported from `non_labour_income_contributions`; canonical proofs live there |
| Art. 68 solidarity | `article_68_{first..fourth}_threshold`, `article_68_transition_base_amount`, `article_68_monthly_withholding` (0 / 50 % phase-in / 1.5 % / transition / 2 %) | same |
| Annual + netting | `annual_social_withholding` (faces EUROMOD `tscpe_s`), `net_pension` | art. 23 §2 1° + art. 52 7° |
| Taxable | `taxable_income` = net pension + `belgium_pit_pilot_worker_net_professional_income` (import) | art. 6 |
| 130–134 | `article_130_base_tax`, `tax_free_amount`, `article_134_tax_on_tax_free_amount`, `tax_after_tax_free_amount` | thresholds/rates imported from `rate_scale`, `tax_free_amount`, `tax_free_amount_tax` |
| Art. 147 | `activity_income`, `article_147_excluded_activity_income` (2° b/c machinery driven by `has_reached_legal_retirement_age`, `receives_survivor_pension_or_transition_allowance`; c-band proration reuses the imported 19 630/28 780 amounts), `article_147_net_income_for_ratio`, `article_147_replacement_ratio` (min(1, net pension / denominator)), `article_147_{base,additional}_reduction_before_limits` | amounts imported from `tax_reductions_and_credits`; page-253/254 proof atoms |
| Art. 151/1 & 152 | `article_1511_additional_reduction_factor`, `article_152_base_reduction_factor` | bounds imported; page-255/256 excerpts in report (atoms carry page-253 only — see §6) |
| Art. 153 | `article_153_pension_tax_share_cap` = min(1, net pension / taxable) × tax after TFA | page-256 |
| Combine | `replacement_reduction_after_limits` = min(base×f152 + additional×f1511, cap); `net_federal_tax_after_replacement_reductions` | — |
| Post-federal | `reduced_state_tax_after_autonomy_factor` (imported art. 5/2 share), `net_federal_tax_after_work_bonus_credit` (imported pilot 289ter/1 credit, refundable), `agglomeration_additional_tax_rate_after_cap` (imported 468 cap), `local_additional_tax`, `federal_and_local_tax_before_withholding` | mirrors pilot worker architecture |

Inputs (all Person; the engine namespaces them per owning module):

```
pensioner_pit_oracle_pipeline#input.belgium_pit_pensioner_annual_gross_pension                                   Money
pensioner_pit_oracle_pipeline#input.belgium_pit_pensioner_beneficiary_has_family_charge                          bool
pensioner_pit_oracle_pipeline#input.belgium_pit_pensioner_has_reached_legal_retirement_age                       bool
pensioner_pit_oracle_pipeline#input.belgium_pit_pensioner_receives_survivor_pension_or_transition_allowance      bool
pensioner_pit_oracle_pipeline#input.belgium_pit_pensioner_communal_additional_tax_rate                           Rate
pensioner_pit_oracle_pipeline#input.belgium_pit_pensioner_agglomeration_additional_tax_rate                      Rate
pilot_worker_oracle_pipeline#input.belgium_pit_article_23_worker_remuneration                                    Money (0 for pure pensioners)
work_bonus#input.belgium_worker_work_bonus_supplied_reference_annual_remuneration                                Money (wage × 12/13.92; 0 for pure pensioners)
```

Integration note ("integrate, do not duplicate"): the SSC stage imports every
parameter of `non_labour_income_contributions` and re-applies them at Person
scope, exactly the pilot/couple pattern for canonical-module reuse (the couple
pipeline imports rate_scale/tax_free_amount parameters the same way). The
Family-scoped originals stay untouched and canonical for their own suites; the
per-beneficiary scope matches art. 68/191's per-pensioner text and the
person-scope lint. The alternative (relation-bridged import of the Family
rules) was rejected: it would force every dataset row to carry a singleton
Family entity plus relation for no numeric difference.

## 4. Per-case verification vs EUROMOD BE_2025

EUROMOD side generated by me with the x64 connector (model
`EUROMOD_RELEASES_J2.0+`, system BE_2025, dataset config `BE_2024_c1_2015_03_e2`,
template `BE_training_data`, 273 columns). Case rows: `les=4, lfs=15, lhw=0,
liwmy=0, liwwh=540, loc=5, yemmy=0, dms=1, dag=70, dwt=1, drgn1=0` (drgn1=0
switches off EUROMOD's regional+municipal layers — the Lane D "communal 0"
configuration); mixed case adds `yem>0, yemmy=12, lhw=38, liwmy=12`.
**Uprating factors probed in-run: yem 1.055022392834293, poa exactly 1.0** (no
pre-divide needed for pensions; `poa` input = annual/12). Driver script and
raw results: scratchpad `euromod_pension_cases.py` /
`euromod_pension_cases.json` (script reproduced in §8). Run command:

```sh
arch -x86_64 env PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
  DOTNET_ROOT=/Users/maxghenis/.dotnet-x64 PYTHONNET_RUNTIME=coreclr \
  POLARS_SKIP_CPU_CHECK=1 /Users/maxghenis/.venvs/axiom-euromod-x64/bin/python \
  euromod_pension_cases.py euromod_pension_cases.json
```

Axiom side: pinned engine `_cape-prep-engine/target/release/axiom-rules-engine`
(source c6cc389a), compile + run-compiled in-tree:

```sh
AXIOM_RULESPEC_REPO_ROOTS=$PWD \
  .../axiom-rules-engine compile \
  --program $PWD/be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml \
  --output pensioner.compiled.json
.../axiom-rules-engine run-compiled --artifact pensioner.compiled.json < request.json
# request: {"mode":"explain","dataset":{"inputs":[{name:"<module>#<rule>",entity:"Person",
#   entity_id:"p1",interval:{start,end},value:{kind,value}},...],"relations":[]},
#   "queries":[{"entity_id":"p1","period":{"period_kind":"tax_year",...},"outputs":[...]}]}
```

All values annual EUR. EUROMOD columns ×12 from its monthly output.

### 4.1 Single pensioners — MATCHED to the cent

| Case | Column | EUROMOD | Axiom | Δ |
|---|---|---:|---:|---:|
| 15k | tscpe_s vs `annual_social_withholding` | 0.00 | 0.00 | 0 |
| 15k | tints_s vs `article_130_base_tax` | 3 750.00 | 3 750.00 | 0 |
| 15k | tintcri_s vs `replacement_reduction_after_limits` | 1 022.50 | 1 022.50 | 0 |
| 15k | **tin_s** vs `federal_and_local_tax_before_withholding` | **0.00** | **0.00** | **0** |
| 25k | tscpe_s vs withholding | 547.2400000000016 | 547.24 (exact 547.2399…96) | <1e-12 |
| 25k | tintcri_s vs reduction | 2 435.5043109508197 | 2 435.5043109508197 | 0 |
| 25k | **tin_s** vs final | **1 628.5079096531776** | **1 628.5079096531764** | **1.2e-12** |
| 40k | tscpe_s vs withholding | 2 020.00 | 2 020.00 | 0 |
| 40k | tintcri_s vs reduction | 1 746.319247162381 | 1 746.3192471623813 | <1e-12 |
| 40k | **tin_s** vs final | **6 550.639112351934** | **6 550.639112351934** | **0** |

Mechanism identity per stage (both engines): 25k monthly pension 2 083,33 sits
in the AMI phase-in band (withholding = excess over 2 037,73 → 547,24/yr);
taxable 24 452,76; art. 151/1 factor (28 780−24 452,76)/9 150 = 0,472922…;
reduction = 2 219,27 + 457,23×0,472922 = 2 435,50; federal ×(1−0,24957).
40k: AMI 3,55 % (1 420) + solidarity mid band 1,5 % (600); taxable 37 980;
art. 152 factor 1/3 + 2/3×(57 560−37 980)/28 780 = 0,786889; additional = 0
(taxable ≥ 28 780).

### 4.2 Mixed 30k pension + 15k wage — EXPLAINED (two named mechanisms, exact)

EUROMOD tin_s **6 051.513079980725**; Axiom **6 403.8118471069212**.
Residual (EUROMOD − Axiom) = **−352.30**, decomposed to the cent:

1. **`engine_semantics` — EUROMOD il_netYem forfait-base construction (+124.26
   EUROMOD-side).** EUROMOD's forfait base `il_netYem` subtracts *all* personal
   SIC including the pension withholding `tscpe_s` (its DefIl lists
   `tscpe_s = -`), so its art. 51 forfait is 30 %×(15 000 − 1 065) = 4 180,50
   (= its `tintace_s` output) and its taxable income is 39 754,50. Art. 51
   (page-121: "diminués desdites cotisations", scoped by art. 23 §2 1° "qui
   grèvent ces revenus") nets each category by its own contributions: the wage
   forfait base is 15 000 (wage SSC nets to zero after the work bonus), forfait
   4 500, taxable 39 435. Effects: tax scale +319,50×45 % = +143,78; art. 147
   ratio/152-factor shift −21,81 −... net federal-after-autonomy difference
   7 556,36 − 7 432,10 = **+124.26** (observed on both engines' own numbers:
   EUROMOD tints_s 14 001,525, tintcri_s 1 204,6488 vs Axiom 13 857,75 /
   1 226,4603).
2. **`upstream_engine_gap` (already dispositioned in the be-work-bonus-credit
   suite) — work-bonus credit bases (−476.56).** EUROMOD credits the uncapped
   volet schedule: `tintcly_s = 120,59×12×33,14 % + 162,62×12×52,54 % =
   1 504,85`. Art. 289ter/1 credits the reduction "réellement accordée" — the
   volets capped at contributions actually due (163,375/mo at this wage) with
   the statutory B-then-A ordering → encoded credit 1 028,29.
   1 504,8489 reproduces EUROMOD's constants exactly:
   (1447,08×0,3314)+(1951,44×0,5254) = 479,5623+1025,2866.

Check: +124.26 − 476.56 = **−352.30** = observed residual. ✓
(Both engines agree the wage-side employee SSC nets to zero:
tscee_s = tsceerd_s = 1 960,50.)

### 4.3 Additional companion-pinned cases (engine-internal regressions)

family-charge 40k (charge-de-famille scales: solidarity 0, AMI 1 420 → final
6 776,40); survivor 20k+10k wage (full activity-income exclusion → ratio 1);
under-age 18k+12k wage (no exclusion → ratio 18 000/26 400); art. 147 2° c band
24k+8k wage (excluded activity = 5 600×(28 780−24 000)/9 150 = 2 925,46);
communal 7 % + agglomeration 1,5 %→capped 1 % (local = 8 %×6 550,64 = 524,05);
zero-income degenerate case (zero-denominator branches). These have no direct
single-column EUROMOD counterparts at drgn1=0 (family charge requires
dependent children in EUROMOD, which changes the TFA supplements too) and are
pinned as exact-decimal engine regressions.

## 5. EUROMOD BE_2025 mechanics (read from the model XML, BE_2025 system spine)

Extraction: `extract_be2025.py` (scratchpad) parses
`XMLParam/Countries/BE/BE.xml` → per-system policy→function→parameter spine.
Facts my encoding decisions rest on, all observed in that spine:

- `tscpe_be`: AMI bands (2 037,73/2 112,71 isolated; 2 414,98/2 503,85 with
  dependent children at `tu_family` level) + solidarity bands (3 225,74… /
  3 729,35…), all on monthly `il_pension = poa + psu` per individual.
- `tinna_be`: schedule on `il_taxabley` → tints_s; base allowance 10 910 →
  tintatc_s via the 134 schedule; **FUN 46** horizontal reduction
  2 219,27×(il_netpension+byr+bwkmcse01_s)/il_taxabley_bf_mq + 2 977,93×share
  for sickness; **FUN 47** vertical (art. 152 shape); **FUN 48/49**
  unemployment (art. 151 shape, denominator 7 150); **FUN 52** cap
  (il_netrepY/il_taxableY)×max(0,tints−tintatc) (art. 153 shape); **FUN 62-64**
  additional reduction 457,23 with the 19 630→28 780 taper, *not* prorated by
  the pension share, capped at remaining tax; **FUN 54-61 (art. 154 extra
  reductions) all switch=n/a — not simulated**; ×(1−24,957 %); tin_s.
- `tinrg_be`/`tinmu_be`: keyed on drgn1 (1/2/3); drgn1=0 → both zero.
- `tintace_be`: 30 % SchedCalc on `il_netYem` capped 5 930 — pensions excluded
  from the base *except* the il_netYem tscpe subtraction quirk (§4.2).
- `tinfe_be` FUN 97/102: work-bonus credit from **uncapped** `i_tsceerdA/B_s`
  (les-independent; requires lhw>0, yemmy>0), subtracted from tin_s.
- les=4 = pensioner (all 1 680 les=4 training rows have poa>0; no les condition
  in the tscpe/tin chains — poa alone drives them).

## 6. Gates and their evidence

```sh
# companion tests (pinned encoder + pinned engine)
~/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode test --root $PWD \
  --axiom-rules-engine-path ~/TheAxiomFoundation/_cape-prep-engine \
  be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.test.yaml
# -> RuleSpec companion tests passed: 1 file(s), 10 case(s)

# repository layout tests
~/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python -m pytest tests/ -q
# -> 29 passed in 11.82s

# sibling-layout full validate at the corpus pin
rsync -a --exclude target --exclude .venv $PWD/ /tmp/.../validate-layout/rulespec-be/
ln -s ~/TheAxiomFoundation/_cape-prep-engine /tmp/.../validate-layout/axiom-rules-engine
cd /tmp/.../validate-layout/rulespec-be && AXIOM_CORPUS_REPO=~/TheAxiomFoundation/_cape-prep/corpus-be-pin \
  ~/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode validate \
  be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml --skip-reviewers --json
# -> "ci_pass": true
```

Validator baseline at the same pin, same command (for fable's calibration):
couple_pit_oracle_pipeline **true**; pilot_worker_oracle_pipeline **false**
("Ungrounded generated numeric literal: 46"); tax_reductions_and_credits
**false** ("…1050…"); non_labour_income_contributions **false** ("…3325.48…").
I.e. the merged baseline does not uniformly pass this validator; the new module
meets the strictest recent bar (couple).

What the validator forced, and the costs accepted:
- **Rule-level proof atoms may only cite the module's single
  `source_verification` path** (exact string match). Cross-page atoms
  (page-73/123/254/255/256/686 and the SFP guidance blocks) were therefore
  removed; page-253 atoms retained on four art. 147 rules. The removed
  grounding lives in this report (§2) and in the canonical imported modules.
  This mirrors the couple module (no cross-path atoms). Repo guidance
  ("attach every other independently operative source … as a proof atom")
  conflicts with this validator rule at this pin — flagged for fable.
- Scope lint reads the module summary; "Family-scoped"/"family-charge"
  vocabulary classified the module as unit-scoped → reworded to
  charge-de-famille phrasing.
- "Flattened thresholded imported rate" lint requires threshold/limit/cap
  vocabulary or `min(` in banded-rate formulas → the art. 191 selector rules
  are named `…protected_floor_limit_monthly` / `…full_rate_threshold_monthly`.
- Zero-branch coverage: every 0-returning branch asserted (15k SSC zeros; a
  zero-income degenerate case for the ratio/cap denominators).

Machine-load note (honesty): one layout-pytest run appeared hung and was
killed; the cause was concurrent heavy jobs from other lanes (load avg >13
earlier in the session) plus background-QoS throttling after a foreground
timeout — the same suite completed 29/29 in 11.82s once contention cleared.
One run of the full suite in contention took 148.06s, also green.

## 7. Population-wiring notes for Lane W

- **Entity shape**: everything Person. No relations needed for single-pensioner
  rows. Working pensioners: assign both the pension input and the pilot worker
  remuneration input on the same Person.
- **Column facing**:
  - `tscpe_s` ↔ `pensioner_pit_oracle_pipeline#belgium_pit_pensioner_annual_social_withholding`
    (÷12 for the monthly template convention; EUROMOD cumulates `poa+psu` per
    individual — feed the summed pension).
  - `tin_s` (at drgn1=0) ↔ `…#belgium_pit_pensioner_federal_and_local_tax_before_withholding`
    with communal and agglomeration rates 0. For regionful `tin_s` the
    regional_surcharge module must be composed in (out of Lane P scope), and
    EUROMOD's `tinmu_be` applies its regional average communal rates
    (BXL 6,2 % / FL 7,17 % / WAL 7,92 %) to tin_s *after* refundable credits.
- **Input wiring from EUROMOD-style columns**:
  - `belgium_pit_pensioner_annual_gross_pension` ← 12×(poa+psu). poa uprating
    factor is exactly 1.0 (probed) — no pre-divide.
  - `beneficiary_has_family_charge` ← EUROMOD proxies the charge-de-famille
    scale with `nDepChildrenOfCouple >= 1` (couple-level dependent children).
    The SFP definition is broader (spouse without benefit/income, ménage-rate
    pension). For EUROMOD-matching runs wire it to the children proxy;
    dispositions should note the semantic gap.
  - `has_reached_legal_retirement_age` ← dag ≥ 66 (legal retirement age from
    1 Feb 2025). EUROMOD does not model the art. 147 2° b/c exclusions at all,
    so this input only matters for law-faithful runs; wire dag-based.
  - `receives_survivor_pension_or_transition_allowance` ← psu > 0.
  - Worker inputs for working pensioners: as in the worker recipe
    (remuneration = gross wage; work-bonus reference = wage×12/13.92).
- **Known EUROMOD-side divergences to expect in population columns**
  (all mechanisms named and quantified here):
  1. il_netYem forfait-base quirk — biases EUROMOD taxable upward by
     30 %×tscpe_s for every working pensioner with tscpe_s>0 (§4.2 #1).
  2. Work-bonus credit uncapped-volet gap — low-wage workers incl. working
     pensioners (§4.2 #2; existing disposition).
  3. Art. 154 complementary reduction (unemployment-bearing incomes) is in the
     law but off in EUROMOD BE_2025 — will surface in unemployment-carrying
     rows, not pension-only rows.
  4. EUROMOD FUN 47 boundary bug: at il_taxabley exactly 28 780 or 57 560 its
     strict inequalities match no branch → tintcri_s = 0; the statute (and the
     encoding) is continuous there. Measure-zero unless a row lands exactly on
     a boundary after netting.
- **EUROMOD run recipe deltas vs the worker recipe**: pensioner rows use
  les=4, lfs=15, liwwh=540, lhw=liwmy=yemmy=0, poa set; everything else as in
  `microcosm_be_v02_euromod.py`. `bsa_be` (income support) is on in BE_2025 but
  paid €0 for all four cases here (single, dag=70; bsa targets <65 per its
  eligibility) — watch it for low-income pensioner rows only via `bsaoa`
  (GRAPA), which stays off without the manual switch.

## 8. EUROMOD driver (verbatim)

The exact script that produced every EUROMOD number in §4 (also at scratchpad
`euromod_pension_cases.py`; results JSON `euromod_pension_cases.json`):

```python
#!/usr/bin/env python3
"""Lane P: single-pensioner and mixed pension+wage EUROMOD BE_2025 cases."""
import json, math, platform, sys, time
from io import StringIO
from contextlib import redirect_stdout
from pathlib import Path
import numpy as np
import pandas as pd
from euromod import Model

MODEL_ROOT = Path("/Users/maxghenis/Downloads/EUROMOD_J2.0/EUROMOD_RELEASES_J2.0+")
TEMPLATE = MODEL_ROOT / "Input/BE_training_data.txt"
DATASET = "BE_2024_c1_2015_03_e2"
SYSTEM = "BE_2025"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("euromod_pension_cases.json")

def header_columns():
    with TEMPLATE.open(encoding="utf-8") as stream:
        return [n.strip() for n in stream.readline().rstrip("\n").split("\t") if n.strip()]

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
        sim = system.run(frame, DATASET, verbose=False, nowarnings=True,
                         requested_vars=[], requested_incomelists=[],
                         requested_vargroups=[], requested_ilgroups=[],
                         suppress_other_output=False)
    out = sim.outputs[0]
    return out, [str(e) for e in list(getattr(sim, "errors", []))]

def base_person(frame, row, idhh, idperson, dag=70, les=4):
    assign(frame, row, {
        "idhh": idhh, "idperson": idperson, "idpartner": 0, "idmother": 0,
        "idfather": 0, "dag": dag, "dgn": 1, "dms": 1, "dwt": 1,
        "les": les, "lfs": 15, "lhw": 0, "liwmy": 0, "liwwh": 540,
        "loc": 5, "yemmy": 0,
    })

def main():
    if platform.machine() != "x86_64":
        raise RuntimeError(f"needs x86_64, got {platform.machine()}")
    header = header_columns()
    model = Model(str(MODEL_ROOT))
    country = next(c for c in model.countries if c.name == "BE")
    system = next(s for s in country.systems if s.name == SYSTEM)

    probe = blank_frame(2, header)
    base_person(probe, 0, idhh=1, idperson=101, dag=35, les=3)
    assign(probe, 0, {"lhw": 38, "liwmy": 12, "liwwh": 120, "yemmy": 12, "yem": 1000})
    base_person(probe, 1, idhh=2, idperson=201)
    assign(probe, 1, {"poa": 1000})
    out, errs = engine_run(system, probe)
    out = out.sort_values("idperson").reset_index(drop=True)
    yem_factor = float(out.loc[0, "yem"]) / 1000.0
    poa_factor = float(out.loc[1, "poa"]) / 1000.0
    print(f"yem_factor={yem_factor!r} poa_factor={poa_factor!r} probe_errors={errs}")

    cases = [
        {"label": "pension_15k", "pension": 15000.0, "wage": 0.0},
        {"label": "pension_25k", "pension": 25000.0, "wage": 0.0},
        {"label": "pension_40k", "pension": 40000.0, "wage": 0.0},
        {"label": "mixed_30k_pension_15k_wage", "pension": 30000.0, "wage": 15000.0},
    ]
    frame = blank_frame(len(cases), header)
    for i, case in enumerate(cases):
        base_person(frame, i, idhh=i + 1, idperson=(i + 1) * 100 + 1)
        assign(frame, i, {"poa": case["pension"] / 12.0 / poa_factor})
        if case["wage"] > 0:
            assign(frame, i, {"yem": case["wage"] / 12.0 / yem_factor,
                              "yemmy": 12, "lhw": 38, "liwmy": 12})
    out, errs = engine_run(system, frame)
    out = out.sort_values("idperson").reset_index(drop=True)

    want = ["poa", "yem", "tscpe_s", "tscee_s", "tsceerd_s", "tin_s", "tints_s",
            "tintatb_s", "tintatc_s", "tintcri_s", "tinna_s", "tinrg_s",
            "tinmu_s", "tintcly_s", "tintcch_s", "tintace_s", "tsceesp_s",
            "bsa_s", "ils_dispy", "ils_tax", "ils_taxsim"]
    present = [c for c in want if c in out.columns]
    results = {"yem_uprating_factor": yem_factor, "poa_uprating_factor": poa_factor,
               "probe_errors": errs,
               "missing_columns": [c for c in want if c not in out.columns],
               "cases": []}
    for i, case in enumerate(cases):
        row = {"label": case["label"], "intended_annual_pension": case["pension"],
               "intended_annual_wage": case["wage"]}
        for col in present:
            row[f"{col}_annual"] = float(out.loc[i, col]) * 12.0
        results["cases"].append(row)
    OUT.write_text(json.dumps(results, indent=1) + "\n")
    print(json.dumps(results, indent=1))

if __name__ == "__main__":
    main()
```

Both runs (probe + 4 cases) completed with empty EUROMOD error arrays; total
≤2 concurrent EUROMOD processes throughout (one process, two sequential runs).

## 9. Open questions

1. **"pension légale" in art. 147 2° b/c — gross or net?** Encoded as the gross
   annual pension (the benefit as granted). EUROMOD doesn't model b/c at all,
   so no oracle discriminates. All lane cases keep it dormant (mixed case
   pension > 28 780) except the dedicated companion cases.
2. **Charge-de-famille wiring** (§7): EUROMOD's children proxy vs the SFP
   definition — needs a disposition class when population rows with a
   low-income spouse appear.
3. **Validator-vs-CLAUDE.md tension on cross-provision proof atoms** (§6):
   the pinned validator rejects atoms citing any path other than the module's
   single source_verification path; repo guidance asks for exactly such atoms.
   The couple precedent (and now this module) resolves toward the validator.
   Fable may want a corpus-side fix (multi-page provision units) or a validator
   fix before this pattern hardens.
4. **Extending the pipeline to the other art. 147 categories**: unemployment
   (items 7/8 + art. 151 + art. 154 §§2-3) and sickness/invalidity (items 9/10,
   2 977,93) reuse the same skeleton; the parameters are already imported by
   `tax_reductions_and_credits`. The art. 154 §3/1 machinery (mixed
   unemployment + pension) is encodable from page-257 but has no EUROMOD
   counterpart to match (off in BE_2025) — it would land as law-ahead-of-oracle
   EXPLAINED rows.
5. **EUROMOD `il_earnedY_bf_mq`/`il_bch_means` also embed poa** — child-benefit
   means tests and lone-parent supplements see pension income; irrelevant for
   this slice but will matter when Lane F's dependants meet pensioner
   households.

LANE P DONE
