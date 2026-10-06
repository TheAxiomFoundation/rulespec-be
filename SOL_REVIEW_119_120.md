# SOL adversarial review — PRs #119 and #120

Reviewed combined tree: `origin/main` `7c85808ae99f5731b21059e643e5e19b66438904` plus PR #119 commit `2c84eb9b5bcd853e430fbfbb0c7c31a22b0a3887` and PR #120 commit `26c6b9763aed688105a24e763aeac91b86a3a9c4`, at integration HEAD `7d05517c55541008e9f4202908292ff8dd5b4156`.

Review surface: `git diff origin/main...HEAD` — 18 added YAML files, 2,384 insertions (nine modules and nine companions). I read both lane reports and the campaign law, but independently reran the gates, source checks, EUROMOD cases, direct engine executions, scope lint, and adversarial counterexamples. No source or test file was modified.

## Result

Neither PR is merge-safe.

- #119 has a material Article 147 input-model error, repeats an Article 466/304 ordering error in its final-liability path, and violates the direct-secondary-source proof contract.
- #120 erases Article 23 professional losses, repeats the Article 466/304 ordering error, violates the proof contract, and its Article 171 half cannot pass the canonical signed-release CI frontier. The self-employment-only portion would still be blocked by the first three issues.
- The requested cent-level oracle claims are real. They do not cure the legal errors: in particular, EUROMOD shares the disputed local-tax ordering used by the new fixtures.

## Findings

### [BLOCKER][#120] Article 171 cites pages absent from the canonical signed release; the git-corpus override does not test the shared-CI source frontier

Files: `.axiom/toolchain.toml:1-6`; `be/statutes/income_tax/individual/article_171_rates/page_268.yaml:8`; corresponding anchors in `page_269.yaml`, `page_270.yaml`, `page_271.yaml`, `page_272.yaml`, `page_275.yaml`; and `be/statutes/income_tax/individual/separately_taxed_income.yaml:35-44`.

The repository is bound to immutable release `be-rulespec-2026-07-10`. Its signed content selects 52 CIR92 pages, but none of pages 268, 269, 270, 271, 272, or 275. The PR is forbidden to alter the toolchain pin. The campaign explicitly records this CI frontier at `../../LEDGER_CAMPAIGN.md:72-84` and says these modules are held pending a Max-gated source promotion and re-pin.

Reproducer (offline, against the release commit embedded in the immutable release object):

```bash
rg -n 'axiom_corpus_release = ' .axiom/toolchain.toml
git -C /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin \
  show 04c77ce86bf16a6da19986aa8cbbd5d05a84b0af:data/corpus/provisions/be/statute/2026-07-10-be-rulespec-source-promotion.jsonl |
python3 -c 'import json,sys
rows=[json.loads(x) for x in sys.stdin]
ps=[r["citation_path"] for r in rows if "fisconetplus/cir92/revenus-2025/page-" in r.get("citation_path","")]
print("cir92_rows",len(ps))
for p in (268,269,270,271,272,275): print(f"page-{p}", "PRESENT" if any(x.endswith(f"page-{p}") for x in ps) else "MISSING")'
git show -s --format='%h %s%n%b' f9557bc
```

Selected output:

```text
5:axiom_corpus_release = "be-rulespec-2026-07-10"
cir92_rows 52
page-268 MISSING
page-269 MISSING
page-270 MISSING
page-271 MISSING
page-272 MISSING
page-275 MISSING
f9557bc Hold article 171 modules pending a corpus promotion release
... the validator cannot isolate their provisions in CI although the git-pinned corpus carries them.
```

The mandatory local sibling validation below passes because `AXIOM_CORPUS_REPO=.../corpus-be-pin` exposes all 744 git-pinned records. Under the binding campaign record at lines 72-84, that is not the signed source frontier consumed by shared CI, which previously rejected these absent pages. I cannot execute the remote shared workflow in this sandbox: the predicted main failure is an inference from the immutable release membership plus that recorded CI behavior, not a locally observed failed `validate`. A later local branch commit, `f9557bc`, already removes exactly these 14 Article 171 files for this reason.

### [BLOCKER][#119] Article 147 tests total Article 34 pension instead of the taxpayer's legal pension

File: `be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml:49-51,96,353-380` (and the assumption pinned at `pensioner_pit_oracle_pipeline.test.yaml:291-310`).

The only pension input is described as broad gross Article 34 pension. Article 34 includes complementary pensions, while Article 147 item 2(b)/(c) tests the amount of the taxpayer's **legal pension**. The same total Article 34 amount must be used for the reduction numerator, but it cannot be reused for this threshold. A separate legal-pension amount is required.

Pinned text:

- page 92: `pensions, pensions complémentaires et rentes`;
- page 253: `d'une pension légale qui ne dépasse pas 19.630 euros`;
- page 254: `la différence entre 28.780 euros ... et la pension légale`.

Reproducer:

```bash
nl -ba be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml |
  sed -n '49,51p;94,97p;353,380p'
python3 - <<'PY'
legal_pension, complementary_pension, activity = 15000, 9000, 5600
article34_total = legal_pension + complementary_pension
law = activity if legal_pension <= 19630 else activity * (28780-legal_pension)/(28780-19630)
encoded = activity if article34_total <= 19630 else activity * (28780-article34_total)/(28780-19630)
print(f"law_excluded_activity={law:.2f}")
print(f"encoded_excluded_activity={encoded:.2f}")
PY
```

Output:

```text
374 ... annual_gross_pension <= ...phaseout_start
377 ... annual_gross_pension <= ...phaseout_end
378 activity_income * (... - annual_gross_pension) / ...
law_excluded_activity=5600.00
encoded_excluded_activity=2925.46
```

The same supplied Article 34 total can represent €15k legal plus €9k complementary pension, for which page 253 requires the full €5,600 exclusion. The displayed source formula instead returns €2,925.46, so the module cannot distinguish the two legally different cases.

### [BLOCKER][#120] Article 23 professional losses are clipped away before cross-activity netting, and prior-period losses are absent

File: `be/statutes/income_tax/individual/self_employed_oracle_pipeline.yaml:73-76,132-153`.

The first `max(0, ...)` clips the category before expenses, the second clips the resulting self-employment loss, and the combined worker/self-employment rule therefore never receives a negative amount. There is also no PIT input for deductible prior-period professional losses.

Pinned page 73 states:

> `les pertes professionnelles éprouvées pendant la période imposable ... sont déduites des revenus des autres activités professionnelles`

and then:

> `sont déduites les pertes professionnelles des périodes imposables antérieures`.

Reproducer (the direct CLI request was the companion mixed fixture with only gross self-employment, wage, reference wage, and justified-expense values changed):

```bash
nl -ba be/statutes/income_tax/individual/self_employed_oracle_pipeline.yaml |
  sed -n '70,77p;132,154p'
if rg -n -i 'prior.{0,30}(professional_)?loss|loss.{0,30}prior|antérieur.{0,30}perte|perte.{0,30}antérieur' \
  be/statutes/income_tax/individual/self_employed_oracle_pipeline.yaml; then
  :
else
  echo 'no prior-period PIT professional-loss input or rule'
fi
AXIOM_RULESPEC_REPO_ROOTS="$PWD" \
  /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine/target/release/axiom-rules-engine compile \
  --program "$PWD/be/statutes/income_tax/individual/self_employed_oracle_pipeline.yaml" \
  --output /private/tmp/sol120-selfemp.compiled.json
PYTHONDONTWRITEBYTECODE=1 \
  /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
import json, subprocess, yaml
from pathlib import Path
cases=yaml.safe_load(Path('be/statutes/income_tax/individual/self_employed_oracle_pipeline.test.yaml').read_text())
c=next(x for x in cases if x['name']=='mixed_yem_30000_yse_20000_exposes_imported_semantics')
values=dict(c['input'])
def setv(suffix, value):
    key=next(k for k in values if k.endswith('#input.'+suffix)); values[key]=value
setv('belgium_self_employed_gross_professional_income',1000)
setv('belgium_pit_article_23_worker_remuneration',10000)
setv('belgium_worker_work_bonus_supplied_reference_annual_remuneration',8620.689655172413)
setv('belgium_pit_self_employment_actual_professional_expenses_are_justified',True)
setv('belgium_pit_self_employment_justified_professional_expenses_excluding_social_contribution_and_purchase_costs',2000)
setv('belgium_pit_self_employment_article_51_business_purchase_costs',0)
def scalar(v):
    if isinstance(v,bool): return {'kind':'bool','value':v}
    if isinstance(v,int): return {'kind':'integer','value':v}
    return {'kind':'decimal','value':str(v)}
p=c['period']; interval={'start':p['start'],'end':p['end']}
inputs=[{'name':k,'entity':'Person','entity_id':'p1','interval':interval,'value':scalar(v)} for k,v in values.items()]
root='be:statutes/income_tax/individual/self_employed_oracle_pipeline#'
outputs=['be:regulations/social_security/self_employed/contributions#belgium_self_employed_selected_annual_social_contribution',
 'be:statutes/income_tax/individual/pilot_worker_oracle_pipeline#belgium_pit_pilot_worker_net_professional_income',
 *[root+n for n in ('belgium_pit_self_employment_income_after_social_contribution_and_business_purchase_costs',
 'belgium_pit_self_employment_selected_professional_expenses_excluding_social_contribution_and_purchase_costs',
 'belgium_pit_self_employment_net_professional_income',
 'belgium_pit_self_employment_combined_worker_and_self_employment_taxable_income')]]
request={'mode':'explain','dataset':{'inputs':inputs,'relations':[]},
 'queries':[{'entity_id':'p1','period':p,'outputs':outputs}]}
run=subprocess.run(['/Users/maxghenis/TheAxiomFoundation/_cape-prep-engine/target/release/axiom-rules-engine',
 'run-compiled','--artifact','/private/tmp/sol120-selfemp.compiled.json'],
 input=json.dumps(request),text=True,capture_output=True,check=True)
got=json.loads(run.stdout)['results'][0]['outputs']
for name in outputs: print(name.rsplit('#',1)[-1],got[name]['value']['value'])
print('statutory_current_loss_combined',7000+(1000-2000))
PY
```

Selected output from the request:

```text
no prior-period PIT professional-loss input or rule
belgium_self_employed_selected_annual_social_contribution 0
belgium_pit_pilot_worker_net_professional_income 7000
belgium_pit_self_employment_income_after_social_contribution_and_business_purchase_costs 1000
belgium_pit_self_employment_selected_professional_expenses_excluding_social_contribution_and_purchase_costs 2000
belgium_pit_self_employment_net_professional_income 0
belgium_pit_self_employment_combined_worker_and_self_employment_taxable_income 7000
statutory_current_loss_combined 6000
```

The request JSON was mechanically generated from `mixed_yem_30000_yse_20000_exposes_imported_semantics`, so all transitive inputs remained assigned. This is a live engine result, not only hand arithmetic.

### [BLOCKER][#119/#120] Both final-liability paths shrink the Article 466 local-tax base with refundable credits

Files: `be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml:522-553`; `be/statutes/income_tax/individual/self_employed_oracle_pipeline.yaml:241-294`.

Both pipelines subtract refundable activity credits—the pension path's imported Article 289ter/1 work-bonus credit and #120's supplied Article 289ter low-activity credit—and then calculate local additions on the post-credit balance. The pinned corpus establishes the opposite ordering:

- Special Financing Law Article 5/3: after federal and regional tax form `l'impôt total`, it is successively `diminué des crédits d'impôt fédéraux et régionaux remboursables` and only then `majoré de la taxe communale additionnelle ... et de la taxe d'agglomération additionnelle`;
- page 518, Article 290: `les crédits d'impôt visés aux articles 289bis, § 1er, 289ter et 289ter/1, sont imputés intégralement sur l'impôt`, with that tax defined as `l'impôt total`;
- page 687, Article 466: additions are `calculées sur l'impôt total`;
- page 688, Article 468: `La taxe additionnelle ... ne peut être l'objet d'aucune réduction`;
- page 526, Article 304: only a credit **surplus** is subsequently `imputé ... sur les taxes additionnelles`.

Thus a refundable credit is imputed after the local addition has been calculated; it does not reduce that addition's calculation base.

Reproducer for #120, using values pinned by the first passing companion case:

```bash
jq -r 'select(.citation_path=="be/statute/loi/1989/01/16/1989021010/article/5-3")|.body' \
  /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/data/corpus/provisions/be/statute/2026-07-02-be-pit-autonomy-factor.jsonl
CORPUS=/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/data/corpus/provisions/be/statute/2026-06-30-be-income-tax-consolidated.jsonl
for p in 518 526 687 688; do
  jq -r --arg path "be/statute/fisconetplus/cir92/revenus-2025/page-$p" \
    'select(.citation_path==$path)|.body' "$CORPUS" |
    rg -o '.{0,100}(crédits d.impôt visés aux articles 289bis|sur les taxes additionnelles|calculées sur l.impôt total|ne peut être l.objet d.aucune réduction).{0,150}'
done
/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode test \
  --root "$PWD" --axiom-rules-engine-path /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine \
  be/statutes/income_tax/individual/self_employed_oracle_pipeline.test.yaml --json
/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
from decimal import Decimal as D
precredit = D("2082.068035") + D("692.43336639995")
credit, rate, engine = D("880"), D(".0717"), D("2030.337151880326415")
lawful = precredit + precredit * rate - credit
print("article466_precredit_base", precredit)
print("article466_local_tax", precredit * rate)
print("corpus_order_total", lawful)
print("engine_understatement", engine - lawful)
PY
```

Selected output:

```text
... les crédits d'impôt visés aux articles 289bis, § 1er, 289ter et 289ter/1, sont imputés intégralement sur l'impôt. Pour l'application de l'alinéa 1er, il faut entendre par impôt l'impôt total ...
... est imputé, s'il y a lieu, sur les taxes additionnelles à l'impôt des personnes physiques ...
... la taxe d'agglomération additionnelle à l'impôt des personnes physiques sont calculées sur l'impôt total ...
La taxe additionnelle à l'impôt des personnes physiques ne peut être l'objet d'aucune réduction, exemption ou exception.
{"success":true,...,"cases":6,...,"failures":[]}
article466_precredit_base 2774.50140139995
article466_local_tax 198.931750480376415
corpus_order_total 2093.433151880326415
engine_understatement -63.096000000000000
```

The passing fixture instead pins a post-credit base of `1894.50140139995`, local tax `135.835750480376415`, and total `2030.337151880326415`; the understatement is exactly `880 × 7.17%`.

For #119, lines 532 and 553 establish the same algebra. The mixed €30k pension/€15k wage companion pins pre-credit tax at `7432.1009071069212379904370213` and post-credit tax at `6403.8118471069212379904370213`. At a 7% communal rate, the encoded formula and corpus-order counterfactual are:

```text
precredit_tax 7432.1009071069212379904370213
credit 1028.28906
encoded_postcredit_local_tax 448.266829297484486659330591491
encoded_total 6852.078676404405724649767612791
corpus_order_total 6924.058910604405724649767612791
understatement -71.980234200000000000000000000
```

Reproduction arithmetic:

```bash
nl -ba be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml | sed -n '522,553p'
nl -ba be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.test.yaml | sed -n '179,181p'
/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
from decimal import Decimal as D, getcontext
getcontext().prec = 60
pre, credit, rate = D("7432.1009071069212379904370213"), D("1028.28906"), D(".07")
encoded = (pre-credit) + (pre-credit)*rate
lawful = pre + pre*rate - credit
print("precredit_tax",pre); print("credit",credit)
print("encoded_postcredit_local_tax",(pre-credit)*rate)
print("encoded_total",encoded); print("corpus_order_total",lawful)
print("understatement",encoded-lawful)
PY
```

The older worker oracle also uses this ordering, but both PRs newly reproduce it in their own final-liability surfaces. An inherited implementation is not legal authority.

### [BLOCKER][#119/#120] The root modules omit direct proof atoms for independently operative secondary provisions

Files: `be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml:443-499,522-553`; `be/statutes/income_tax/individual/self_employed_oracle_pipeline.yaml:104-153,263-294`; `be/statutes/income_tax/individual/separately_taxed_income.yaml:338-359`.

`CLAUDE.md:24-27` and `README.md:39-46` require every independently operative secondary source to be attached directly to the supported rule as an exact corpus-backed proof atom. Lexically, every atom that exists is exact. Completeness fails; representative omissions (not an exhaustive inventory) are:

- the pension root has four atoms, all page 253, despite newly implementing Articles 23, 151/1, 152, 153, 290/304, and 465-468;
- the self-employment root has three atoms, all page 121, despite newly implementing Articles 23, 49, 290/304, and 465-468;
- the separate-tax root has one atom, page 268, despite newly implementing Article 466.

Reproducer:

```bash
nl -ba CLAUDE.md | sed -n '22,28p'
nl -ba README.md | sed -n '39,46p'
PYTHONDONTWRITEBYTECODE=1 \
  /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
from pathlib import Path
import yaml
for f in map(Path, (
  'be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml',
  'be/statutes/income_tax/individual/self_employed_oracle_pipeline.yaml',
  'be/statutes/income_tax/individual/separately_taxed_income.yaml')):
    d=yaml.safe_load(f.read_text()); paths=[]
    for r in d['rules']:
        for a in (((r.get('metadata') or {}).get('proof') or {}).get('atoms') or []):
            paths.append(a['source']['corpus_citation_path'])
    print(f"{f} atoms={len(paths)} unique={sorted(set(paths))}")
PY
```

Selected output for the three composition roots:

```text
be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml atoms=4 unique=['be/statute/fisconetplus/cir92/revenus-2025/page-253']
be/statutes/income_tax/individual/self_employed_oracle_pipeline.yaml atoms=3 unique=['be/statute/fisconetplus/cir92/revenus-2025/page-121']
be/statutes/income_tax/individual/separately_taxed_income.yaml atoms=1 unique=['be/statute/fisconetplus/cir92/revenus-2025/page-268']
```

Lane P's report at lines 466-471 confirms that cross-page atoms were removed because the current validator rejects a sibling provision under a single module anchor. That validator limitation does not waive the repository contract; the operative provisions need page-scoped modules/imports or an approved contract/tooling resolution.

### [MAJOR][#119] Article 153's exact proportional allocation formula has an unresolved provenance boundary

File: `be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml:475-488`.

The code defines attributable tax as `(net pension / total taxable income) × tax after TFA`. Page 256 says only that no reduction can exceed the Article 130-145 tax share `qui est afférente aux revenus à raison desquels elle est accordée`; it does not state this pro-rata arithmetic. EUROMOD uses the same arithmetic, but `data/oracles` is expressly not legal authority (`CLAUDE.md:16`). I do not conclude from this record that the ratio is substantively wrong; I conclude that the module has not sourced this independently operative allocation choice. It needs an upstream legal source or an explicit supplied allocation boundary.

Reproducer:

```bash
nl -ba be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml | sed -n '475,489p'
CORPUS=/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/data/corpus/provisions/be/statute/2026-06-30-be-income-tax-consolidated.jsonl
jq -r 'select(.citation_path=="be/statute/fisconetplus/cir92/revenus-2025/page-256")|.body' "$CORPUS" |
  sed 's/Article 154.*//' | rg -o 'Article 153.*'
```

The output juxtaposes line 488's exact ratio with the quoted sentence above; the cited provision text contains no allocation equation.

### [MAJOR][#120] Article 171 item 4bis is a fixed 12.5% law rate but remains caller-controlled

File: `be/statutes/income_tax/individual/separately_taxed_income.yaml:217-227`; companion input at `separately_taxed_income.test.yaml:27-28`.

Pinned page 274 says `4°bis au taux de 12, 5 %`. Line 227 nevertheless multiplies by a free `...12_5_percent_rate_boundary`; a caller can legally misprice the row or leave it zero. The spaced extraction is a validator/parser limitation, not missing law; leaving a statutory constant caller-controlled is not a valid encoding.

Reproducer:

```bash
nl -ba be/statutes/income_tax/individual/separately_taxed_income.yaml | sed -n '217,228p'
nl -ba be/statutes/income_tax/individual/separately_taxed_income.test.yaml | sed -n '25,30p'
CORPUS=/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/data/corpus/provisions/be/statute/2026-06-30-be-income-tax-consolidated.jsonl
jq -r 'select(.citation_path=="be/statute/fisconetplus/cir92/revenus-2025/page-274")|.body' "$CORPUS" |
  rg -o '4°bis au taux de 12, 5 %'
```

Output shows the fixed corpus phrase, the free multiplier, and the fixture manually injecting `0.125`.

### [MAJOR][#119/#120] Required population classifications are unavailable or hard-coded, and overlapping new incomes have no combined progressive base

Files: `be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml:353-380`; `self_employed_oracle_pipeline.yaml:73-76,104-153,241-273`; `separately_taxed_income.yaml:62-271,316-370`. Wiring evidence: `../../population-rerun/out/v03/microcosm_be_v03_axiom_components.py:340-354,372-431,445-478,728-743` and `../../population-rerun/LANE_V_REPORT.md:318-323,395-420`.

These are MAJOR, rather than blockers, under the review brief's explicit treatment of population inputs:

- v0.3 carries combined old-age/survivor pension entirely as `poa`; survivor status is unavailable and is hard-coded false even though that classification selects an Article 147 branch.
- v0.3 exposes undifferentiated `yse`; wiring forces actual expenses justified with zero expenses and forces the profit (not business-profit) branch, although those choices select different Article 51 calculations.
- the self-employment parity path depends on an unencoded supplied low-activity credit. Lane W notes that EUROMOD's exposed `tintcly_s` conflates worker and self-employment credits, so mixed cases cannot split this input exactly.
- Article 171 eligibility bases, globalisation selector, dynamic rates, and 4bis rate are caller inputs; v0.3 wires only generic movable income at 30% and cannot populate the other rows.
- most importantly, the pension root combines only pension+wage (`pensioner...yaml:267-268`) and the self-employment root combines only self-employment+wage (`self_employed...yaml:151-153`). Lane W therefore adds separate marginal outputs for overlapping persons rather than calculating one progressive base.

Reproducer for the overlap surface:

```bash
PYTHONDONTWRITEBYTECODE=1 \
  /Users/maxghenis/TheAxiomFoundation/_cape-prep/population-rerun/.venv/bin/python - <<'PY'
import numpy as np
x=np.load('/Users/maxghenis/TheAxiomFoundation/_cape-prep/population-rerun/out/v03/microcosm_be_v03_h5_sidecar.npz')
p=x['belgium_pension_gross_2026']>0; s=x['belgium_self_employment_gross_2026']>0
c=x['belgium_movable_capital_gross_2026']>0; w=x['person_weight']
for label,m in [('pension+selfemp',p&s),('pension+capital',p&c),('selfemp+capital',s&c),('all_three',p&s&c)]:
    print(label,'rows',int(m.sum()),'weighted_people',round(float(w[m].sum()),3))
PY
nl -ba ../../population-rerun/out/v03/microcosm_be_v03_axiom_components.py | sed -n '340,354p;372,431p;445,478p;728,743p'
```

Output:

```text
pension+selfemp rows 936 weighted_people 178555.111
pension+capital rows 12662 weighted_people 832308.498
selfemp+capital rows 4283 weighted_people 261445.959
all_three rows 602 weighted_people 56750.293
733 ... 936 pension+yse overlap records therefore use an additive marginal composition because no combined pension+self-employment pipeline exists.
```

The nonlinear scale, pension-reduction ratios/phaseouts, credits, and local bases do not generally make two separately computed marginal pipelines additive.

### [NIT][#119 evidence] The lane report's “empty error arrays” assertion is false

File: `../../beP/rulespec-be/LANE_P_REPORT.md:455`.

This does not affect the reproduced values, but the verbatim driver emitted two nonfatal EUROMOD warnings.

Reproducer after the driver run:

```bash
jq '.probe_errors' /private/tmp/sol_euromod_pension_cases.json
```

Output:

```text
[
  "Variable(s) yds, lindi, yptmp, tad, tis not found ... (zero is used as default)",
  "... variable(s) bunpe01, bunpe02, xcc, yempv, yiyitdp is/are uprated with default factor (1.050524934383202)"
]
```

## Independent gate results

### Pins and diff hygiene

```bash
git rev-parse HEAD origin/main ledger/pensions 26c6b97 ledger/art171-held
git -C /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin rev-parse HEAD
git -C /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine rev-parse HEAD
git -C /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned rev-parse HEAD
git diff --check origin/main...HEAD
git status --short
```

Observed pins: integration `7d05517`, main `7c85808`, pension `2c84eb9`, PR #120 payload `26c6b97`, corpus `8e48989c`, engine `c6cc389a`, local pinned encoder `3869d66`. `git diff --check` passed. Initial status was clean; final status contains only this untracked report. The diff contains no `.axiom`, workflow, waiver, `known-*`, `oracle-coverage-pending`, toolchain, or scoreboard edit.

### Companion tests

```bash
/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode test \
  --root "$PWD" \
  --axiom-rules-engine-path /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine \
  be/statutes/income_tax/individual/article_171_rates/page_{268,269,270,271,272,275}.test.yaml \
  be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.test.yaml \
  be/statutes/income_tax/individual/self_employed_oracle_pipeline.test.yaml \
  be/statutes/income_tax/individual/separately_taxed_income.test.yaml --json
```

Output:

```json
{"success":true,"test_files":9,"cases":25,"compiled_programs":9,"failures":[]}
```

A separate scanner confirmed every direct factual reference and every companion `#input` key is assigned in every case, including false booleans:

```bash
/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
import re, subprocess, yaml
from pathlib import Path
reserved={'if','else','min','max','true','false','and','or','not'}
mods=[Path(x) for x in subprocess.check_output(
 ['git','diff','--name-only','origin/main...HEAD'],text=True).splitlines()
 if x.endswith('.yaml') and not x.endswith('.test.yaml')]
fail=[]
for file in mods:
    doc=yaml.safe_load(file.read_text())
    cases=yaml.safe_load(file.with_suffix('.test.yaml').read_text())
    defined={r['name'] for r in doc.get('rules',[])}
    imported={x.rsplit('#',1)[-1] for x in doc.get('imports',[])}
    refs={tok for rule in doc.get('rules',[]) for v in rule.get('versions',[])
          for tok in re.findall(r'\b[A-Za-z_][A-Za-z0-9_]*\b',str(v.get('formula','')))}
    direct=refs-defined-imported-reserved
    keys=set().union(*(set(c.get('input',{})) for c in cases))
    prefix=str(file.with_suffix('')).replace('/',':',1)+'#input.'
    local={k for k in keys if k.startswith(prefix)}
    for case in cases:
        supplied=case.get('input',{})
        suffixes={k.rsplit('#input.',1)[-1] for k in supplied if '#input.' in k}
        if direct-suffixes or keys-set(supplied):
            fail.append((file.name,case['name'],sorted(direct-suffixes),sorted(keys-set(supplied))))
    false_count=sum(v is False for case in cases for v in case.get('input',{}).values())
    print(file.name,'local_keys',len(local),'all_input_keys',len(keys),
          'cases',len(cases),'false_values',false_count)
print('failures',len(fail))
PY
```

Output: each rate page `local_keys 0 ... cases 1`; pension `local_keys 6 all_input_keys 8 cases 10 false_values 21`; self-employment `local_keys 10 all_input_keys 28 cases 6 false_values 59`; separate-tax `local_keys 28 all_input_keys 31 cases 3 false_values 2`; `failures 0`.

### Repository layout

```bash
PYTHONDONTWRITEBYTECODE=1 \
  /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python \
  -m pytest -q -p no:cacheprovider tests/test_repository_layout.py
```

Output: `29 passed in 23.82s`.

### Full sibling-layout validation against the requested git pin

```bash
sol_validate_dir="$(mktemp -d /private/tmp/sol-review-119-120-validate.XXXXXX)"
rsync -a --exclude .git "$PWD/" "$sol_validate_dir/rulespec-be/"
ln -s /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine "$sol_validate_dir/axiom-rules-engine"
cd "$sol_validate_dir/rulespec-be"
AXIOM_CORPUS_REPO=/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin \
  /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode validate \
  be/statutes/income_tax/individual/article_171_rates/page_{268,269,270,271,272,275}.yaml \
  be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml \
  be/statutes/income_tax/individual/self_employed_oracle_pipeline.yaml \
  be/statutes/income_tax/individual/separately_taxed_income.yaml \
  --skip-reviewers --json
```

Every requested module returned `ci_pass: true`, `all_passed: true`, and `errors: []`:

| Module | `ci_pass` |
|---|---:|
| `article_171_rates/page_268.yaml` | true |
| `article_171_rates/page_269.yaml` | true |
| `article_171_rates/page_270.yaml` | true |
| `article_171_rates/page_271.yaml` | true |
| `article_171_rates/page_272.yaml` | true |
| `article_171_rates/page_275.yaml` | true |
| `pensioner_pit_oracle_pipeline.yaml` | true |
| `self_employed_oracle_pipeline.yaml` | true |
| `separately_taxed_income.yaml` | true |

This establishes the requested full-git-pin gate, while the first blocker explains why it is not equivalent to the signed-release source frontier recorded for shared CI.

### Proof atoms

I recursively resolved every new proof atom by its `citation_path` key in `2026-06-30-be-income-tax-consolidated.jsonl` and tested `excerpt in body` byte-for-byte:

```bash
PYTHONDONTWRITEBYTECODE=1 \
  /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
import json, subprocess, yaml
from pathlib import Path
corpus=Path('/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/data/corpus/provisions/be/statute/2026-06-30-be-income-tax-consolidated.jsonl')
rows={r['citation_path']:r.get('body','') for r in map(json.loads,corpus.open())}
files=[Path(x) for x in subprocess.check_output(['git','diff','--name-only','origin/main...HEAD'],text=True).splitlines()
       if x.endswith('.yaml') and not x.endswith('.test.yaml')]
atoms=[]
def walk(x,file):
    if isinstance(x,dict):
        src=x.get('source')
        if isinstance(src,dict) and isinstance(src.get('corpus_citation_path'),str) and isinstance(src.get('excerpt'),str):
            atoms.append((file,src['corpus_citation_path'],src['excerpt']))
        for value in x.values(): walk(value,file)
    elif isinstance(x,list):
        for value in x: walk(value,file)
for file in files: walk(yaml.safe_load(file.read_text()),file)
bad=[a for a in atoms if a[1] not in rows or a[2] not in rows[a[1]]]
print('files',len(files),'atoms',len(atoms),'failures',len(bad))
for file in files: print(file,sum(a[0]==file for a in atoms))
PY
```

Summarized output:

```text
files 9 atoms 23 failures 0
page_268 1; page_269 2; page_270 2; page_271 3; page_272 5; page_275 2;
pension 4; self-employment 3; separate-tax 1
```

The pinned money-atom gate and an independent nontrivial-Money-literal scan were also clean:

```bash
AXIOM_CORPUS_REPO=/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin \
  /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode \
  proof-validate --require-money-atoms --money-atom-root "$PWD" --json \
  be/statutes/income_tax/individual/article_171_rates/page_{268,269,270,271,272,275}.yaml \
  be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml \
  be/statutes/income_tax/individual/self_employed_oracle_pipeline.yaml \
  be/statutes/income_tax/individual/separately_taxed_income.yaml
/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
import re, subprocess, yaml
from pathlib import Path
files=[Path(x) for x in subprocess.check_output(
 ['git','diff','--name-only','origin/main...HEAD'],text=True).splitlines()
 if x.endswith('.yaml') and not x.endswith('.test.yaml')]
for file in files:
    for rule in yaml.safe_load(file.read_text()).get('rules',[]):
        if rule.get('dtype')!='Money': continue
        payload=' '.join(str(v.get(k,'')) for v in rule.get('versions',[])
                         for k in ('formula','value','values'))
        nums=re.findall(r'(?<![A-Za-z0-9_])(?:\d+(?:\.\d+)?)(?![A-Za-z0-9_])',payload)
        material=sorted({x for x in nums if x not in {'0','1'}})
        if material: print(file,rule['name'],material)
PY
```

All nine proof reports returned `passed: true`, `issues: []`, and `money_atoms.missing: 0`; the literal scanner printed nothing. Thus the composed Money formulas reuse imported amounts instead of duplicating nontrivial monetary literals. There is no paraphrase or money-literal finding. The proof blocker above concerns missing independently operative secondary proofs, not the exactness of atoms that exist.

### Person scope and entity shape

I ran `find_source_scope_consistency_issues`, `find_person_scoped_rate_base_unit_issues`, `find_person_scoped_definition_unit_issues`, and `find_imported_person_scoped_definition_unit_issues` from the pinned encoder over all nine new modules. Every result was `[]`.

```bash
PYTHONPATH=/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/src \
PYTHONDONTWRITEBYTECODE=1 \
  /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
import subprocess
from pathlib import Path
from axiom_encode.harness.validator_pipeline import (
 find_source_scope_consistency_issues as source_scope,
 find_person_scoped_rate_base_unit_issues as rate_base,
 find_person_scoped_definition_unit_issues as definition,
 find_imported_person_scoped_definition_unit_issues as imported)
root=Path('.').resolve()
files=[Path(x) for x in subprocess.check_output(['git','diff','--name-only','origin/main...HEAD'],text=True).splitlines()
       if x.endswith('.yaml') and not x.endswith('.test.yaml')]
for file in files:
    content=file.read_text()
    print(file, source_scope(content), rate_base(content), definition(content),
          imported(content,rules_file=file.resolve(),policy_repo_path=root))
PY
```

Output: each of the nine files printed four empty lists.

All newly derived rules are Person-scoped (pension 33/33, self-employment 18/18, separate-tax 28/28); Article 171 rate modules are scalar parameters. Relevant compiled dependency closures contain only Person and Scalar definitions. There is no unit-scoped rate×base or relation/entity-shape finding.

## Legal checks that did pass

- Article 147's base/additional amounts, ratio structure, and b/c interpolation are correct apart from the wrong legal-pension threshold input identified above.
- Article 151/1 is correctly 1 through €19,630, linear to zero at €28,780. Article 152 is correctly 1 through €28,780, linear to one-third at €57,560, and one-third thereafter.
- Article 154 is correctly absent for the pension-only AY2026 slice. Page 256 §1 requires unemployment benefits, alone or mixed with pension/replacement income.
- Article 51 matches pages 121-122: profits 28.7%/10%/5%/3% at €7,540/€14,970/€24,920 with €5,210 cap; business profits 30% with €5,930 cap; contributions and the applicable purchase price are removed before the forfait.
- Article 23's category-specific deduction of the pension's own social contribution is supported; the disputed point is loss netting in #120.
- Encoded Article 171 fixed rates match pages 268-275: 33%; 8%; 10%; 15%; 18%; 30%; 20%; 15%; 20/15%; 5/20%; 16.5%; 10.38%; 0%. Item 3quinquies's 15% path is imported; items 3ter, 5, and 6 are genuinely dynamic; item 2ter is literally `(...)`. Item 4bis is legally fixed at 12.5%, as discussed above.

## EUROMOD and direct-engine verification

### EUROMOD reruns

Pension driver, verbatim from Lane P report lines 351-452:

```bash
sed -n '351,452p' ../../beP/rulespec-be/LANE_P_REPORT.md |
arch -x86_64 env PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
  DOTNET_ROOT=/Users/maxghenis/.dotnet-x64 PYTHONNET_RUNTIME=coreclr \
  POLARS_SKIP_CPU_CHECK=1 /Users/maxghenis/.venvs/axiom-euromod-x64/bin/python \
  - /private/tmp/sol_euromod_pension_cases.json
```

Self-employment/capital driver, verbatim from Lane S report lines 297-358:

```bash
sed -n '297,358p' ../../beS/rulespec-be/LANE_S_REPORT.md | zsh
```

Selected annual results:

| Case | EUROMOD result |
|---|---:|
| pension €25k | `tscpe=547.2400000000016`; `tintcri=2435.5043109508197`; `tin=1628.5079096531776` |
| pension €40k | `tscpe=2019.9999999999998`; `tintcri=1746.319247162381`; `tin=6550.639112351934` |
| self-employment `yse=€45k` | `tscse=9225`; taxable `35775`; `tin=10163.204158431827` |
| movable `yiy=€10k` | ordinary `tin=0`; `tinkt=3000`; total `ils_tax=3000` |

### Direct pinned engine CLI

```bash
ENGINE=/Users/maxghenis/TheAxiomFoundation/_cape-prep-engine/target/release/axiom-rules-engine
AXIOM_RULESPEC_REPO_ROOTS="$PWD" "$ENGINE" compile \
  --program "$PWD/be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml" \
  --output /private/tmp/sol119-pension.compiled.json
AXIOM_RULESPEC_REPO_ROOTS="$PWD" "$ENGINE" compile \
  --program "$PWD/be/statutes/income_tax/individual/self_employed_oracle_pipeline.yaml" \
  --output /private/tmp/sol120-selfemp.compiled.json
AXIOM_RULESPEC_REPO_ROOTS="$PWD" "$ENGINE" compile \
  --program "$PWD/be/statutes/income_tax/individual/separately_taxed_income.yaml" \
  --output /private/tmp/sol120-separate.compiled.json
```

I then ran the four named companion cases directly against those artifacts. This converts every explicit case input to a one-Person engine dataset; it does not use the encoder test runner for evaluation:

```bash
/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
import json, subprocess, yaml
from pathlib import Path
engine='/Users/maxghenis/TheAxiomFoundation/_cape-prep-engine/target/release/axiom-rules-engine'
jobs=[
 ('be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.test.yaml',
  'pension_25k_article_191_band_and_partial_additional_reduction',
  '/private/tmp/sol119-pension.compiled.json',
  'be:statutes/income_tax/individual/pensioner_pit_oracle_pipeline#belgium_pit_pensioner_federal_and_local_tax_before_withholding'),
 ('be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.test.yaml',
  'pension_40k_solidarity_band_and_article_152_phaseout',
  '/private/tmp/sol119-pension.compiled.json',
  'be:statutes/income_tax/individual/pensioner_pit_oracle_pipeline#belgium_pit_pensioner_federal_and_local_tax_before_withholding'),
 ('be/statutes/income_tax/individual/self_employed_oracle_pipeline.test.yaml',
  'euromod_exact_gross_yse_45000_matches_to_machine_precision',
  '/private/tmp/sol120-selfemp.compiled.json',
  'be:statutes/income_tax/individual/self_employed_oracle_pipeline#belgium_pit_self_employment_federal_regional_and_local_tax_before_withholding'),
 ('be/statutes/income_tax/individual/separately_taxed_income.test.yaml',
  'euromod_exact_gross_yiy_10000_imports_general_capital_tax_and_keeps_tin_total_explicit',
  '/private/tmp/sol120-separate.compiled.json',
  'be:statutes/income_tax/individual/separately_taxed_income#belgium_pit_article_171_tin_total_tax_before_withholding')]
def scalar(v):
    if isinstance(v,bool): return {'kind':'bool','value':v}
    if isinstance(v,int): return {'kind':'integer','value':v}
    return {'kind':'decimal','value':str(v)}
for path,name,artifact,out in jobs:
    case=next(c for c in yaml.safe_load(Path(path).read_text()) if c['name']==name)
    p=case['period']; interval={'start':p['start'],'end':p['end']}
    inputs=[{'name':k,'entity':'Person','entity_id':'p1','interval':interval,
             'value':scalar(v)} for k,v in case['input'].items()]
    request={'mode':'explain','dataset':{'inputs':inputs,'relations':[]},
             'queries':[{'entity_id':'p1','period':p,'outputs':[out]}]}
    run=subprocess.run([engine,'run-compiled','--artifact',artifact],
        input=json.dumps(request),text=True,capture_output=True,check=True)
    got=json.loads(run.stdout)['results'][0]['outputs'][out]['value']['value']
    print(name,got)
PY
```

Output:

```text
pension_25k_article_191_band_and_partial_additional_reduction 1628.5079096531763934426229508
pension_40k_solidarity_band_and_article_152_phaseout 6550.6391123519342135742413711
euromod_exact_gross_yse_45000_matches_to_machine_precision 10163.2041584318275275
euromod_exact_gross_yiy_10000_imports_general_capital_tax_and_keeps_tin_total_explicit 3000
```

Each request used one Person, no relations, the 2025 calendar-year interval, and every explicit companion input. Comparison:

| Case | Engine | EUROMOD minus engine | Cent-equal |
|---|---:|---:|---|
| pension €25k | `1628.5079096531763934426229508` | `1.21e-12` | yes |
| pension €40k | `6550.6391123519342135742413711` | `-2.14e-13` | yes |
| `yse=€45k` | `10163.2041584318275275` | `-5.28e-13` | yes |
| `yiy=€10k` | `3000` | `0` | yes |

### Mixed-case decompositions

Both named decompositions genuinely close; neither is fabricated by rounding.

Pension €30k + wage €15k:

```bash
python3 - <<'PY'
from decimal import Decimal as D
eu_pre,rs_pre=D('7556.361967980724'),D('7432.1009071069212379904370213')
eu_credit,rs_credit=D('1504.848888'),D('1028.28906')
eu_final,rs_final=D('6051.513079980725'),D('6403.8118471069212379904370213')
base=(eu_pre-rs_pre); credit=(rs_credit-eu_credit)
print('forfait_tax_mechanism',base)
print('work_credit_mechanism',credit)
print('mechanism_sum',base+credit)
print('observed_eu_minus_rulespec',eu_final-rs_final)
print('floating_residual',(base+credit)-(eu_final-rs_final))
PY
```

```text
forfait_tax_mechanism 124.2610608738027620095629787
work_credit_mechanism -476.559828
mechanism_sum -352.2987671261972379904370213
observed_eu_minus_rulespec -352.2987671261962379904370213
floating_residual -1.0000000000000E-12
```

The €0.000000000001 closure residue is only the displayed EUROMOD float precision. The first mechanism is visible in EUROMOD's `tintace=4180.5` (30% of wage after it also subtracts the pension withholding) versus RuleSpec's category-specific wage forfait. The second is EUROMOD `tintcly=1504.848888` versus RuleSpec's contribution-capped `1028.28906` credit.

Self-employment €20k + wage €30k, rerunning Lane S's `[D1]` decimal script:

```bash
sed -n '386,413p' ../../beS/rulespec-be/LANE_S_REPORT.md | zsh
```

```text
rulespec_tax 10398.345773764672415475
counterfactual_eu_taxable_rulespec_credit 11099.86606218939112281870
counterfactual_eu_taxable_eu_credit 10507.62779506539112281870
taxable_base_mechanism_eu_minus_rulespec 701.52028842471870734370
credit_mechanism_eu_minus_rulespec -592.23826712400000000000
total_eu_minus_rulespec 109.28202130071870734370
taxable_delta_rulespec_minus_eu -1454.6358
credit_delta_rulespec_minus_eu -552.615720
```

EUROMOD's component outputs independently support the labels: self-employed contribution `3714.2392`, employee contribution/reduction `3921/3398.52`, worker forfait `5929.995`, and activity credit `1504.848888`. The claimed `-352.30` and `+109.28` explanations are arithmetically real even though the pipelines still have the legal blockers above.

VERDICT #119: DO-NOT-SHIP (blockers: Article 147 legal-pension input; Article 466/304 credit/local-tax order; missing direct secondary-source proof atoms)
VERDICT #120: DO-NOT-SHIP (blockers: canonical release lacks Article 171 pages; Article 23 loss netting; Article 466/304 credit/local-tax order; missing direct secondary-source proof atoms)
SOL REVIEW DONE
