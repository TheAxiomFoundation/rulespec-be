# SOL adversarial review — rulespec-be #122 draft and merged #123

Reviewed as detached reviewer in the supplied integration worktree. No network
request or push was made. The only repository file created by this review is
this report.

## Disposition

#123 needs follow-up fixes. Its pensioner pipeline preserves the earlier
legal-pension and Article 466 ordering corrections, and the encoded Article
147/151/151-1/154 arithmetic otherwise tracks the pinned text in the cases
reviewed. It nevertheless executes provisions from pages outside the signed
source frontier without declaring those citation paths, and it exposes Article
154 section 3/1's fixed 90 percent coefficient as caller-controlled data.

#122 must not ship, even after its expected source release lands. Independently
reproduced blockers are:

1. a broad Article 134 paragraph 3 treaty-exclusion input is aliased to Article
   133's narrower Article 126 paragraph 2 item 4 exclusion;
2. both new final-liability paths calculate Article 466 additions after
   refundable family/work credits;
3. one Article 134 proof excerpt is stitched across two pages and is not
   verbatim under the required citation-path-keyed resolver; and
4. direct proof coverage collapses across newly operative composition rules;
   and
5. the changed companion set violates the campaign's every-local-input
   assignment rule.

The exact five #122 CIR 92 citation paths outside the promoted-page frontier
are listed below. Release promotion is necessary, but it cannot cure the five
independent blockers above.

## Scope, pins, and diff semantics

This command establishes every reviewed tip, the dependant branch base, and
the size of both the requested tip-to-tip diff and the actual merge payload:

    for rev in HEAD origin/main ledger/dependants 5312619 b105e2b3; do
      printf '%s ' "$rev"
      git rev-parse --short=12 "$rev"
    done
    printf 'merge-base '; git merge-base origin/main ledger/dependants
    printf '#123 '; git diff --shortstat 5312619..b105e2b3
    printf '#122-requested-two-dot '; git diff --shortstat origin/main..ledger/dependants
    printf '#122-payload-three-dot '; git diff --shortstat origin/main...ledger/dependants
    printf '#122-integrated '; git diff --shortstat origin/main..HEAD
    git diff --check 5312619..b105e2b3
    git diff --check origin/main..HEAD

Output:

    HEAD b9737c5df0e8
    origin/main b105e2b3a308
    ledger/dependants 3f2cf1e81e2a
    5312619 53126198acd6
    b105e2b3 b105e2b3a308
    merge-base 7c85808ae99f5731b21059e643e5e19b66438904
    #123  4 files changed, 982 insertions(+), 34 deletions(-)
    #122-requested-two-dot  41 files changed, 4169 insertions(+), 3471 deletions(-)
    #122-payload-three-dot  31 files changed, 4169 insertions(+), 681 deletions(-)
    #122-integrated  31 files changed, 4169 insertions(+), 681 deletions(-)

Both diff-check commands emitted nothing. The requested two-dot #122 diff was
inspected. Because ledger/dependants was cut from 7c85808 while origin/main
subsequently acquired #119, #120, and #123, that raw comparison also presents
those later-main files as removals. The three-dot payload and origin/main..HEAD
are byte-for-byte the same size above and are the correct attribution surface
for the dependant merge result. I used the requested two-dot comparison for
conflict review and the integrated/three-dot surface for #122 findings.

Pinned supporting repositories were:

    printf 'corpus '; git -C /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin rev-parse HEAD
    printf 'engine '; git -C /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine rev-parse HEAD
    printf 'encoder '; git -C /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned rev-parse HEAD
    rg -n '' .axiom/toolchain.toml

Output:

    corpus 8e48989c9e46faa6d85a9624b7a2ebda0880656d
    engine c6cc389a8f5e7238019e4fa06849325fad9acd46
    encoder 3869d66d009f52258be35901edbef370e65a399c
    5:axiom_corpus_release = "be-rulespec-2026-07-10"
    6:axiom_corpus_release_content_sha256 = "c1436c9f99882a819773bc2ccddf8c2a67e41efd24b0d0a408493ba5da39964a"
    7:validation_waiver_set_sha256 = "258a1b9eae033e2e3cff6982bccc596d755bc5e0094b6d51eba5841f532bed25"

## Findings on merged #123

### [BLOCKER][#123] Executable item 10 and Article 154 logic bypass the signed release and direct-proof contract

The repository contract requires each independently operative secondary source
to be attached directly to the supported rule as an exact atom:

    nl -ba CLAUDE.md | sed -n '22,28p'
    nl -ba README.md | sed -n '39,46p'

The new pipeline says in its own source fields that Article 147 item 10 is
encoded from page 254 and that Article 154 sections 2 through 3/1 are encoded
from page 257, while also labelling them unencoded_corpus_blocked:

    git show b105e2b3:be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml |
      nl -ba | sed -n '555,586p;619,637p;770,837p'

Those are executable formulas, not inert documentation. The following scanner
loads the immutable signed release, parses the exact #123 files from b105e2b3,
and reports both declared paths and missing page references in rule source
prose:

    PYTHONDONTWRITEBYTECODE=1 \
    /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
    import json,re,subprocess,yaml
    repo='/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin'
    release=subprocess.check_output([
      'git','-C',repo,'show',
      '04c77ce86bf16a6da19986aa8cbbd5d05a84b0af:data/corpus/provisions/be/statute/2026-07-10-be-rulespec-source-promotion.jsonl'
    ],text=True)
    promoted={json.loads(x)['citation_path'] for x in release.splitlines()}
    files=[
      'be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml',
      'be/statutes/income_tax/individual/replacement_income_complementary_reduction_parameters.yaml']
    docs={f:yaml.safe_load(subprocess.check_output(['git','show',f'b105e2b3:{f}'],text=True)) for f in files}
    paths=[]; atoms=[]
    def walk(x):
      if isinstance(x,dict):
        src=x.get('source')
        if isinstance(src,dict):
          p,e=src.get('corpus_citation_path'),src.get('excerpt')
          if p: paths.append(p)
          if p and isinstance(e,str): atoms.append((p,e))
        for v in x.values(): walk(v)
      elif isinstance(x,list):
        for v in x: walk(v)
    for d in docs.values():
      paths.append(d['module']['source_verification']['corpus_citation_path'])
      walk(d)
    print('cir92_rows',sum('fisconetplus/cir92/revenus-2025/page-' in p for p in promoted))
    for n in range(252,259):
      p=f'be/statute/fisconetplus/cir92/revenus-2025/page-{n}'
      print(f'page-{n}','PRESENT' if p in promoted else 'MISSING')
    print('declared_citation_paths',sorted(set(paths)))
    print('declared_outside_release',sorted(set(paths)-promoted))
    pipeline=docs[files[0]]
    for rule in pipeline['rules']:
      pages=sorted(set(map(int,re.findall(r'page[ -](\d+)',str(rule.get('source',''))))))
      missing=[n for n in pages if f'be/statute/fisconetplus/cir92/revenus-2025/page-{n}' not in promoted]
      count=len((((rule.get('metadata') or {}).get('proof') or {}).get('atoms') or []))
      if missing: print(rule['name'],'source_prose_missing_pages',missing,'proof_atoms',count)
    for name in {
      'belgium_pit_replacement_article_151_unemployment_base_reduction_factor',
      'belgium_pit_replacement_article_154_complementary_reduction'}:
      rule=next(r for r in pipeline['rules'] if r['name']==name)
      print(name,'proof_atoms',len((((rule.get('metadata') or {}).get('proof') or {}).get('atoms') or [])))
    PY

Selected output:

    cir92_rows 52
    page-252 MISSING
    page-253 PRESENT
    page-254 MISSING
    page-255 PRESENT
    page-256 PRESENT
    page-257 MISSING
    page-258 MISSING
    declared_citation_paths [
      'be/statute/fisconetplus/cir92/revenus-2025/page-253',
      'be/statute/fisconetplus/cir92/revenus-2025/page-256'
    ]
    declared_outside_release []
    belgium_pit_replacement_article_147_sickness_invalidity_ratio source_prose_missing_pages [254] proof_atoms 0
    belgium_pit_replacement_article_154_complementary_reduction source_prose_missing_pages [257] proof_atoms 0
    belgium_pit_replacement_article_154_section_3_1_pension_allocation source_prose_missing_pages [257] proof_atoms 0
    belgium_pit_replacement_article_154_section_3_1_unemployment_allocation source_prose_missing_pages [257] proof_atoms 0
    belgium_pit_replacement_article_154_section_3_1_sickness_invalidity_allocation source_prose_missing_pages [257] proof_atoms 0
    belgium_pit_replacement_article_151_unemployment_base_reduction_factor proof_atoms 0
    belgium_pit_replacement_article_154_complementary_reduction proof_atoms 0

Thus a naive declared-citation frontier scan reports a clean #123 only because
the missing citations were omitted. Page 255's new Article 151 phaseout and
page 256's Article 154 eligibility/cap structure are promoted, yet their
independently operative formulas also have no direct atoms. This repeats the
root-proof defect class set by SOL_REVIEW_119_120.

Required follow-up: hold/remove page-254/page-257 execution until those pages
are signed, then attach exact atoms directly to every independently operative
rule. Promoted Article 151 and the promoted portion of Article 154 can and
should receive direct atoms immediately.

### [MAJOR][#123] Article 154 section 3/1's statutory 90 percent coefficient is a free Person input

The code multiplies the statutory excess by
belgium_pit_replacement_article_154_mixed_replacement_excess_rate, and the
companion supplies that fact:

    CORPUS=/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/data/corpus/provisions/be/statute/2026-06-30-be-income-tax-consolidated.jsonl
    git show b105e2b3:be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml |
      nl -ba | sed -n '770,795p'
    git show b105e2b3:be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.test.yaml |
      nl -ba | sed -n '691,733p'
    jq -r 'select(.citation_path=="be/statute/fisconetplus/cir92/revenus-2025/page-257")|.body' "$CORPUS" |
      rg -o '2° 90 % de la différence[^.]*'

The last command emits:

    2° 90 % de la différence entre le montant des revenus de remplacement et, le cas échéant, des pensions et 19.630 euros (montant indexé)

This exact-tree live runner changes only that caller input:

    sol123_dir=$(mktemp -d /private/tmp/sol123-tree.XXXXXX)
    mkdir -p "$sol123_dir/rulespec-be"
    git archive b105e2b3 | tar -x -C "$sol123_dir/rulespec-be"
    cd "$sol123_dir/rulespec-be"
    AXIOM_RULESPEC_REPO_ROOTS="$PWD" \
      /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine/target/release/axiom-rules-engine \
      compile --program "$PWD/be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml" \
      --output /private/tmp/sol123-exact.compiled.json >/dev/null
    PYTHONDONTWRITEBYTECODE=1 \
    /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
    import json,subprocess,yaml
    from decimal import Decimal as D
    from pathlib import Path
    engine='/Users/maxghenis/TheAxiomFoundation/_cape-prep-engine/target/release/axiom-rules-engine'
    artifact='/private/tmp/sol123-exact.compiled.json'
    cases=yaml.safe_load(Path('be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.test.yaml').read_text())
    case=next(c for c in cases if c['name']=='mixed_unemployment_12k_pension_12k_article_154_section_3_1')
    names=['belgium_pit_replacement_tax_after_articles_147_to_153',
      'belgium_pit_replacement_article_154_complementary_reduction',
      'belgium_pit_pensioner_federal_and_local_tax_before_withholding']
    root='be:statutes/income_tax/individual/pensioner_pit_oracle_pipeline#'
    def scalar(v):
      if isinstance(v,bool): return {'kind':'bool','value':v}
      if isinstance(v,int): return {'kind':'integer','value':v}
      return {'kind':'decimal','value':str(v)}
    runs={}
    for rate in ('0.90','0'):
      values=dict(case['input'])
      key=next(k for k in values if k.endswith('#input.belgium_pit_replacement_article_154_mixed_replacement_excess_rate'))
      values[key]=rate
      period=case['period']; interval={'start':period['start'],'end':period['end']}
      request={'mode':'explain','dataset':{'inputs':[
        {'name':k,'entity':'Person','entity_id':'p1','interval':interval,'value':scalar(v)}
        for k,v in values.items()],'relations':[]},
        'queries':[{'entity_id':'p1','period':period,'outputs':[root+n for n in names]}]}
      cp=subprocess.run([engine,'run-compiled','--artifact',artifact],
        input=json.dumps(request),text=True,capture_output=True,check=True)
      out=json.loads(cp.stdout)['results'][0]['outputs']
      runs[rate]=[out[root+n]['value']['value'] for n in names]
      print('supplied_rate',rate)
      for n,v in zip(names,runs[rate]): print(n,v)
    law=D(runs['0.90'][2]); caller0=D(runs['0'][2]); complement=D(runs['0'][1])
    print('final_understatement_if_rate_zero',law-caller0)
    print('complement_times_autonomy',complement*D('0.75043'))
    PY

Output:

    supplied_rate 0.90
    belgium_pit_replacement_tax_after_articles_147_to_153 1966.3710491803278688524590164
    belgium_pit_replacement_article_154_complementary_reduction 0
    belgium_pit_pensioner_federal_and_local_tax_before_withholding 1475.6238264363934426229508197
    supplied_rate 0
    belgium_pit_replacement_tax_after_articles_147_to_153 1966.3710491803278688524590164
    belgium_pit_replacement_article_154_complementary_reduction 786.54841967213114754098360656
    belgium_pit_pensioner_federal_and_local_tax_before_withholding 885.3742958618360655737704918
    final_understatement_if_rate_zero 590.2495305745573770491803279
    complement_times_autonomy 590.2495305745573770491803279

The quantified mechanism is exactly the caller-suppressed complement times the
imported autonomy factor. A fixed statutory coefficient must be a page-scoped,
proven parameter, not a factual input that a caller can set to zero.

### #123 checks that passed the prior-review standard

The legal-pension input remains distinct from total pension, and local
additions are computed on reduced State tax before the refundable work credit:

    git show b105e2b3:be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml |
      nl -ba | rg -C 3 'annual_legal_pension|legal pension'
    git show b105e2b3:be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml |
      nl -ba | sed -n '838,902p'

The first command shows the Article 147 activity exclusion using
belgium_pit_pensioner_annual_legal_pension at lines 435, 438, and 439. The
second shows reduced State tax at line 859, local additions on that pre-credit
amount at line 891, and the work credit subtracted only in the final expression
at line 902. I reproduced no regression of the two #119 findings.

## Findings on draft #122

### [BLOCKER][#122] One broad exclusion input wrongly removes lawful Article 133 supplements

Pinned page 184 excludes the Article 133 isolated-taxpayer child supplement
only in Article 126 paragraph 2 item 4 cases. Pinned page 186 separately makes
Article 134 paragraph 3 inapplicable both to a direct treaty-exempt taxpayer
and to the separately taxed spouse described there. The draft collapses those
different predicates:

    CORPUS=/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/data/corpus/provisions/be/statute/2026-06-30-be-income-tax-consolidated.jsonl
    for p in 184 186; do
      jq -r --arg path "be/statute/fisconetplus/cir92/revenus-2025/page-$p" \
        'select(.citation_path==$path)|.body' "$CORPUS"
    done | rg -o '.{0,120}(article 126, § 2, alinéa 1er, 4°|revenus professionnels qui sont exonérés par convention).{0,350}'
    nl -ba be/statutes/income_tax/individual/pilot_worker_oracle_pipeline.yaml |
      sed -n '303,322p;430,439p'

Lines 313 through 322 map the broad supplied Article 134 paragraph 3 exclusion
directly to Article 133's item-4-only predicate; line 435 explicitly describes
the input as “treaty or Article 126 ... item 4”.

### [BLOCKER][#122] Refundable credits shrink the Article 466 base

The controlling order is directly visible in the pinned corpus:

    jq -r 'select(.citation_path=="be/statute/loi/1989/01/16/1989021010/article/5-3")|.body' \
      /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/data/corpus/provisions/be/statute/2026-07-02-be-pit-autonomy-factor.jsonl
    CORPUS=/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/data/corpus/provisions/be/statute/2026-06-30-be-income-tax-consolidated.jsonl
    for p in 518 526 687 688; do
      jq -r --arg path "be/statute/fisconetplus/cir92/revenus-2025/page-$p" \
        'select(.citation_path==$path)|.body' "$CORPUS" |
        rg -o '.{0,100}(crédits d.impôt visés aux articles 289bis|sur les taxes additionnelles|calculées sur l.impôt total|ne peut être l.objet d.aucune réduction).{0,150}'
    done
    nl -ba be/statutes/income_tax/individual/pilot_worker_oracle_pipeline.yaml |
      sed -n '526,594p;605,626p'
    nl -ba be/statutes/income_tax/individual/couple_pit_oracle_pipeline.yaml |
      sed -n '652,717p'

The corpus output says the credits are imputed on total tax, additions are
calculated on total tax, a credit surplus is only subsequently imputed against
additions, and an addition cannot itself receive a reduction. In contrast,
pilot line 594 and couple lines 706/717 use post-credit balances.

The next one-command live harness reproduces both this blocker and the Article
133 conflation above. It compiles the actual merged draft, uses complete
official companion inputs and relation conversion, and changes only the stated
adversarial fact:

    AXIOM_RULESPEC_REPO_ROOTS="$PWD" \
      /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine/target/release/axiom-rules-engine \
      compile --program "$PWD/be/statutes/income_tax/individual/pilot_worker_oracle_pipeline.yaml" \
      --output /private/tmp/sol-r7-report-pilot.compiled.json >/dev/null
    PYTHONDONTWRITEBYTECODE=1 \
    /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
    import copy,json,subprocess,yaml
    from decimal import Decimal as D
    from pathlib import Path
    from axiom_encode.harness.validator_pipeline import ValidatorPipeline,_rulespec_declared_relation_names
    root='be:statutes/income_tax/individual/pilot_worker_oracle_pipeline#'
    engine=Path('/Users/maxghenis/TheAxiomFoundation/_cape-prep-engine')
    artifact=Path('/private/tmp/sol-r7-report-pilot.compiled.json')
    p=ValidatorPipeline(Path('.').resolve(),engine,enable_oracles=False)
    a=json.loads(artifact.read_text())
    legal=p._rulespec_legal_ids_by_friendly_output_name(a)
    rels=_rulespec_declared_relation_names(a)
    cases={c['name']:c for c in yaml.safe_load(Path(
      'be/statutes/income_tax/individual/pilot_worker_oracle_pipeline.test.yaml').read_text())}
    def run(name,overrides,outputs):
      c=cases[name]; values=copy.deepcopy(c['input'])
      values.update({root+'input.'+k:v for k,v in overrides.items()})
      ds=p._build_rulespec_dataset(values,period=c['period'],query_entity='Person',
        query_entity_id='p1',require_legal_input_keys=True,
        legal_ids_by_friendly_name=legal,module_target=root[:-1],
        declared_relation_names=rels)
      request={'mode':'explain','dataset':ds,'queries':[{
        'entity_id':'p1','period':c['period'],
        'outputs':[legal[o][0] for o in outputs]}]}
      cp=subprocess.run([str(engine/'target/release/axiom-rules-engine'),
        'run-compiled','--artifact',str(artifact)],input=json.dumps(request),
        text=True,capture_output=True,check=True)
      raw=json.loads(cp.stdout)['results'][0]['outputs']
      return {o:(raw[legal[o][0]].get('outcome') or
        raw[legal[o][0]]['value']['value']) for o in outputs}
    art133=[
      'belgium_pit_article_133_article_126_paragraph_2_item_4_exclusion_applies',
      'belgium_pit_article_133_isolated_taxpayer_child_supplement',
      'belgium_pit_article_133_additional_isolated_parent_supplement',
      'belgium_pit_pilot_tax_free_amount',
      'belgium_pit_pilot_federal_and_local_tax_before_withholding']
    r=[]
    for flag in (False,True):
      got=run('single_parent_30k_with_one_dependent_child_gets_article_133_supplements',
        {'belgium_pit_pilot_article_134_paragraph_3_exclusion_applies':flag},art133)
      r.append(got); print('paragraph3_exclusion',flag)
      for k,v in got.items(): print(k,v)
    print('supplements_removed',D(str(r[0][art133[1]]))+D(str(r[0][art133[2]])))
    print('tax_overstatement',D(str(r[1][art133[4]]))-D(str(r[0][art133[4]])))
    art466=['belgium_pit_pilot_reduced_state_tax_after_autonomy_factor',
      'belgium_pit_pilot_article_289ter1_low_wage_work_bonus_credit',
      'belgium_pit_pilot_net_federal_tax_after_family_and_work_bonus_credits',
      'belgium_pit_pilot_local_additional_tax_base',
      'belgium_pit_pilot_local_additional_tax',
      'belgium_pit_pilot_federal_and_local_tax_before_withholding']
    got=run('computed_article_289ter1_work_bonus_credit_reduces_worker_pit',
      {'belgium_pit_communal_additional_tax_rate':'0.07',
       'belgium_pit_agglomeration_additional_tax_rate':0},art466)
    print('article466')
    for k,v in got.items(): print(k,v)
    state,credit,net,encoded=map(lambda k:D(str(got[k])),
      [art466[0],art466[1],art466[2],art466[5]])
    lawful=net+state*D('.07')
    print('article466_precredit_local_tax',state*D('.07'))
    print('corpus_order_total',lawful)
    print('encoded_understatement',lawful-encoded)
    print('credit_times_rate',credit*D('.07'))
    PY

Output:

    paragraph3_exclusion False
    belgium_pit_article_133_article_126_paragraph_2_item_4_exclusion_applies not_holds
    belgium_pit_article_133_isolated_taxpayer_child_supplement 1980
    belgium_pit_article_133_additional_isolated_parent_supplement 479.69678988326848249027237354
    belgium_pit_pilot_tax_free_amount 15349.696789883268482490272374
    belgium_pit_pilot_federal_and_local_tax_before_withholding 932.5100211903696498054474707
    paragraph3_exclusion True
    belgium_pit_article_133_article_126_paragraph_2_item_4_exclusion_applies holds
    belgium_pit_article_133_isolated_taxpayer_child_supplement 0
    belgium_pit_article_133_additional_isolated_parent_supplement 0
    belgium_pit_pilot_tax_free_amount 12890
    belgium_pit_pilot_federal_and_local_tax_before_withholding 1486.2590998
    supplements_removed 2459.696789883268482490272374
    tax_overstatement 553.7490786096303501945525293
    article466
    belgium_pit_pilot_reduced_state_tax_after_autonomy_factor 2863.6108628
    belgium_pit_pilot_article_289ter1_low_wage_work_bonus_credit 952.233168
    belgium_pit_pilot_net_federal_tax_after_family_and_work_bonus_credits 1911.3776948
    belgium_pit_pilot_local_additional_tax_base 1911.3776948
    belgium_pit_pilot_local_additional_tax 133.796438636
    belgium_pit_pilot_federal_and_local_tax_before_withholding 2045.174133436
    article466_precredit_local_tax 200.452760396
    corpus_order_total 2111.830455196
    encoded_understatement 66.656321760
    credit_times_rate 66.65632176

For Article 133, the quantified mechanism is removal of the two printed lawful
supplements by a treaty-only fact, producing exactly the printed tax
overstatement. For Article 466, the understatement is exactly the printed work
credit times the supplied communal rate. Neither mechanism depends on a
missing release page.

### [BLOCKER][#122] One proof atom is non-verbatim under the keyed resolver

I recursively resolved atoms across every JSONL under corpus-be-pin provisions,
keyed by citation_path, and required the excerpt to be a byte-for-byte
substring of one body at that exact key:

    PYTHONDONTWRITEBYTECODE=1 \
    /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
    import json,subprocess,yaml
    from pathlib import Path
    root=Path('/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/data/corpus/provisions')
    rows={}
    for corpus in root.rglob('*.jsonl'):
      for line in corpus.open():
        try: row=json.loads(line)
        except json.JSONDecodeError: continue
        if isinstance(row.get('citation_path'),str):
          rows.setdefault(row['citation_path'],[]).append(row.get('body',''))
    print('resolver_paths',len(rows))
    for label,range_ in [('#123','5312619..b105e2b3'),('#122','origin/main..HEAD')]:
      files=[Path(x) for x in subprocess.check_output(
        ['git','diff','--name-only',range_],text=True).splitlines()
        if x.endswith('.yaml') and not x.endswith('.test.yaml')]
      atoms=[]
      def walk(x,file,rule=None):
        if isinstance(x,dict):
          if isinstance(x.get('name'),str) and isinstance(x.get('versions'),list):
            rule=x['name']
          src=x.get('source')
          if isinstance(src,dict) and isinstance(src.get('corpus_citation_path'),str) and isinstance(src.get('excerpt'),str):
            atoms.append((str(file),rule,src['corpus_citation_path'],src['excerpt']))
          for v in x.values(): walk(v,file,rule)
        elif isinstance(x,list):
          for v in x: walk(v,file,rule)
      for f in files: walk(yaml.safe_load(f.read_text()),f)
      bad=[a for a in atoms if a[2] not in rows or not any(a[3] in b for b in rows[a[2]])]
      print(label,'files',len(files),'atoms',len(atoms),'failures',len(bad))
      for f,rule,path,excerpt in bad:
        print('BAD',f,rule,path,'excerpt_bytes',len(excerpt.encode()))
    PY

Output:

    resolver_paths 58821
    #123 files 2 atoms 8 failures 0
    #122 files 14 atoms 82 failures 1
    BAD be/statutes/income_tax/individual/article_134_additional_supplement_credit.yaml belgium_pit_article_134_refundable_article_133_additional_supplement_credit be/statute/fisconetplus/cir92/revenus-2025/page-186 excerpt_bytes 384

The reason is directly reproducible:

    PYTHONDONTWRITEBYTECODE=1 \
    /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
    import json,yaml
    from pathlib import Path
    f=Path('be/statutes/income_tax/individual/article_134_additional_supplement_credit.yaml')
    src=yaml.safe_load(f.read_text())['rules'][0]['metadata']['proof']['atoms'][0]['source']
    rows=[json.loads(x) for x in Path(
      '/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/data/corpus/provisions/be/statute/2026-06-30-be-income-tax-consolidated.jsonl'
    ).read_text().splitlines()]
    body=next(r['body'] for r in rows if r['citation_path']==src['corpus_citation_path'])
    previous=next(r['body'] for r in rows if r['citation_path'].endswith('/page-185'))
    print('citation_path',src['corpus_citation_path'])
    print('verbatim_substring',src['excerpt'] in body)
    print('body_starts',repr(body[:140]))
    print('excerpt_starts',repr(src['excerpt'][:140]))
    print('excerpt_prefix_in_page185',src['excerpt'][:160] in previous)
    PY

Output:

    citation_path be/statute/fisconetplus/cir92/revenus-2025/page-186
    verbatim_substring False
    body_starts "mesure où elle se rapporte au supplément additionnel visé à l'article 133, alinéa 2, est également convertie en un crédit d'impôt imputable "
    excerpt_starts "la partie de l'impôt sur la quotité du revenu exemptée d'impôt calculée conformément au paragraphe 2, alinéa 2, qui ne peut être portée en d"
    excerpt_prefix_in_page185 True

The atom starts on page 185 and is stitched to a page-186 continuation while
citing page 186 alone. It fails the resolver specified for this review.

### [BLOCKER][#122] Direct proof coverage collapses in the new composition roots

This command compares rule/atom/path counts at the two reviewed tips:

    PYTHONDONTWRITEBYTECODE=1 \
    /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
    import subprocess,yaml
    for ref,f in [
      ('origin/main','be/statutes/income_tax/individual/pilot_worker_oracle_pipeline.yaml'),
      ('ledger/dependants','be/statutes/income_tax/individual/pilot_worker_oracle_pipeline.yaml'),
      ('origin/main','be/statutes/income_tax/individual/couple_pit_oracle_pipeline.yaml'),
      ('ledger/dependants','be/statutes/income_tax/individual/couple_pit_oracle_pipeline.yaml'),
      ('origin/main','be/statutes/income_tax/individual/tax_free_amount_tax.yaml'),
      ('ledger/dependants','be/statutes/income_tax/individual/tax_free_amount_tax.yaml')]:
      d=yaml.safe_load(subprocess.check_output(['git','show',f'{ref}:{f}'],text=True)); atoms=[]
      def walk(x,rule=None):
        if isinstance(x,dict):
          if 'name' in x and 'versions' in x: rule=x['name']
          src=x.get('source')
          if isinstance(src,dict) and src.get('corpus_citation_path') and src.get('excerpt') is not None:
            atoms.append((rule,src['corpus_citation_path']))
          for v in x.values(): walk(v,rule)
        elif isinstance(x,list):
          for v in x: walk(v,rule)
      walk(d)
      print(ref,f.rsplit('/',1)[-1],'rules',len(d.get('rules',[])),
        'atoms',len(atoms),'atom_rules',len(set(x[0] for x in atoms)),
        'paths',len(set(x[1] for x in atoms)))
    PY

Output:

    origin/main pilot_worker_oracle_pipeline.yaml rules 72 atoms 32 atom_rules 29 paths 15
    ledger/dependants pilot_worker_oracle_pipeline.yaml rules 49 atoms 1 atom_rules 1 paths 1
    origin/main couple_pit_oracle_pipeline.yaml rules 34 atoms 2 atom_rules 2 paths 1
    ledger/dependants couple_pit_oracle_pipeline.yaml rules 55 atoms 2 atom_rules 2 paths 1
    origin/main tax_free_amount_tax.yaml rules 33 atoms 14 atom_rules 13 paths 4
    ledger/dependants tax_free_amount_tax.yaml rules 36 atoms 13 atom_rules 13 paths 1

Representative omissions are independently operative Article 23, 130, 132bis,
134, 289ter-1, 290/304, and 465-468 formulas in the pilot/couple roots, plus
the Article 134 paragraph 4 transfer formulas whose direct page-186/page-187
proofs disappear from tax_free_amount_tax. This is not cured by importing
numeric leaf parameters.

One especially clear provenance mismatch is that Article 132bis half-TFA
allocation reuses a parameter whose sole direct proof is Article 134's
half-credit cap:

    nl -ba be/statutes/income_tax/individual/pilot_worker_oracle_pipeline.yaml |
      sed -n '247,280p'
    nl -ba be/statutes/income_tax/individual/couple_pit_oracle_pipeline.yaml |
      sed -n '351,361p'
    nl -ba be/statutes/income_tax/individual/tax_free_amount_tax.yaml |
      sed -n '188,203p'

The value is numerically the same, but the page-185 Article 134 credit-cap atom
does not prove page-183 Article 132bis TFA allocation. A distinct page-scoped
Article 132bis parameter/direct atom is required when page 183 is promoted.

### [BLOCKER][#122] The changed companions do not assign every local input

The campaign rule is literal:

    sed -n '45,49p' /Users/maxghenis/TheAxiomFoundation/_cape-prep/LEDGER_CAMPAIGN.md

It requires companion tests to assign every local #input, including false. A
prefix-aware scan is required here: imported dependency facts must not create
false positives, while alternate local individual/joint/supplied-component
surfaces remain local inputs and cannot be omitted.

This command discovers all changed companions in both reviewed diffs, groups
facts by their own module prefix and relation context, and checks every case:

    PYTHONDONTWRITEBYTECODE=1 \
    /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
    from pathlib import Path
    from collections import Counter,defaultdict
    import subprocess,yaml
    names=set()
    for range_ in ('5312619..b105e2b3','origin/main..HEAD'):
      names.update(x for x in subprocess.check_output(
        ['git','diff','--name-only',range_],text=True).splitlines()
        if x.endswith('.test.yaml'))
    fail=[]; false_values=0
    for file in map(Path,sorted(names)):
      cases=yaml.safe_load(file.read_text())
      prefix=str(file).removesuffix('.test.yaml').replace('/',':',1)+'#input.'
      top=set(); relations={}
      for case in cases:
        for key,value in case.get('input',{}).items():
          if '#relation.' in key:
            for member in value:
              relations.setdefault(key,set()).update(
                x for x in member if x.startswith(prefix))
          elif key.startswith(prefix): top.add(key)
      for case in cases:
        supplied=case.get('input',{})
        have={k for k in supplied if k.startswith(prefix)}
        false_values+=sum(supplied[k] is False for k in have)
        if top-have:
          fail.append((file.name,case['name'],'top',sorted(top-have)))
        for relation,want in relations.items():
          for index,member in enumerate(supplied.get(relation,[]),1):
            local={k for k in member if k.startswith(prefix)}
            false_values+=sum(member[k] is False for k in local)
            if want-local:
              fail.append((file.name,case['name'],
                f'{relation}[{index}]',sorted(want-local)))
    by_file=Counter(x[0] for x in fail)
    missing=Counter(); counts=defaultdict(list)
    for file,case,context,keys in fail:
      missing[file]+=len(keys); counts[file].append(len(keys))
    case_count=sum(len(yaml.safe_load(Path(f).read_text())) for f in names)
    print('test_files',len(names),'cases',case_count,
      'local_false_values',false_values)
    print('full_assignment_failure_records',len(fail))
    print('failure_cases_by_file',dict(by_file))
    print('missing_local_assignments_by_file',dict(missing))
    print('missing_count_range_by_file',
      {f:(min(v),max(v)) for f,v in counts.items()})
    for file,case,context,keys in fail:
      if file=='euromod_tax_income_list.test.yaml':
        print('policy_failure',case,keys)
    PY

Output:

    test_files 18 cases 93 local_false_values 211
    full_assignment_failure_records 15
    failure_cases_by_file {'euromod_tax_income_list.test.yaml': 1, 'tax_free_amount_tax.test.yaml': 14}
    missing_local_assignments_by_file {'euromod_tax_income_list.test.yaml': 1, 'tax_free_amount_tax.test.yaml': 144}
    missing_count_range_by_file {'euromod_tax_income_list.test.yaml': (1, 1), 'tax_free_amount_tax.test.yaml': (3, 16)}
    policy_failure worker_pit_flows_to_ils_tax_worker_pit_pilot ['be:policies/euromod_tax_income_list#input.belgium_euromod_ils_tax_supplied_pit_annual_amount']

All failure records are in #122 files. The engine companions pass because the
unassigned facts are outside each selected output's live dependency branch;
that does not satisfy the campaign's explicit full-assignment rule. Every
tax_free_amount_tax case omits local facts present on another surface, and one
policy case omits the exact supplied-PIT fact printed above.

The fix is to split incompatible individual/joint fact surfaces into
separately testable modules or explicitly assign every local fact in every
companion case; branch non-reachability is not a campaign waiver.

### [RELEASE BLOCK][#122] Exact paths outside the promoted CIR-page frontier

This scanner compares all declared CIR paths in each production diff with the
immutable signed release:

    PYTHONDONTWRITEBYTECODE=1 \
    /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
    import json,subprocess,yaml
    from pathlib import Path
    release=subprocess.check_output([
      'git','-C','/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin','show',
      '04c77ce86bf16a6da19986aa8cbbd5d05a84b0af:data/corpus/provisions/be/statute/2026-07-10-be-rulespec-source-promotion.jsonl'
    ],text=True)
    promoted={json.loads(x)['citation_path'] for x in release.splitlines()}
    print('release_rows',len(release.splitlines()))
    print('cir92_rows',sum('fisconetplus/cir92/revenus-2025/page-' in p for p in promoted))
    for label,range_ in [('#123','5312619..b105e2b3'),('#122','origin/main..HEAD')]:
      files=[Path(x) for x in subprocess.check_output(
        ['git','diff','--name-only',range_],text=True).splitlines()
        if x.endswith('.yaml') and not x.endswith('.test.yaml')]
      paths=set()
      def walk(x):
        if isinstance(x,dict):
          p=x.get('corpus_citation_path')
          if isinstance(p,str): paths.add(p)
          for v in x.values(): walk(v)
        elif isinstance(x,list):
          for v in x: walk(v)
      for f in files: walk(yaml.safe_load(f.read_text()))
      cir=sorted(p for p in paths if 'fisconetplus/cir92/revenus-2025/page-' in p)
      print(label,'production_files',len(files),'declared_cir_paths',len(cir))
      print('declared_outside_52')
      for p in sorted(set(cir)-promoted): print(p)
    PY

Output:

    release_rows 169
    cir92_rows 52
    #123 production_files 2 declared_cir_paths 2
    declared_outside_52
    #122 production_files 14 declared_cir_paths 11
    declared_outside_52
    be/statute/fisconetplus/cir92/revenus-2025/page-183
    be/statute/fisconetplus/cir92/revenus-2025/page-188
    be/statute/fisconetplus/cir92/revenus-2025/page-189
    be/statute/fisconetplus/cir92/revenus-2025/page-190
    be/statute/fisconetplus/cir92/revenus-2025/page-192

Those five full strings are the exact answer to the release-frontier question.

## Independent verification gates

### Companion tests

The exact #123 command was:

    AXIOM_RULESPEC_REPO_ROOTS="$PWD" \
      /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode \
      test --root "$PWD" \
      --axiom-rules-engine-path /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine \
      be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.test.yaml \
      be/statutes/income_tax/individual/replacement_income_complementary_reduction_parameters.test.yaml \
      --json

Output:

    {"success":true,"test_files":2,"cases":26,"compiled_programs":2,"failures":[]}

The exact #122 command was:

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

Output:

    {"success":true,"test_files":16,"cases":67,"compiled_programs":16,"failures":[]}

Passing companions do not neutralize the adversarial fact flips above: neither
the Article 133 treaty-only state nor a nonzero communal rate combined with a
refundable credit is represented as a legal counterexample in the green
matrix.

### Full assignment

The controlling prefix-aware all-changed-companion command is in the #122
finding above. It reports no #123 failure, but it reports #122 failures in
tax_free_amount_tax and euromod_tax_income_list. The passing engine companions
are therefore not a green full-assignment gate.

### Person scope

I ran all four pinned scope/entity checks over the two #123 production modules
and all fourteen #122 production modules:

    PYTHONPATH=/Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/src \
    PYTHONDONTWRITEBYTECODE=1 \
    /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
    from pathlib import Path
    from axiom_encode.harness.validator_pipeline import (
      find_source_scope_consistency_issues as source_scope,
      find_person_scoped_rate_base_unit_issues as rate_base,
      find_person_scoped_definition_unit_issues as definition,
      find_imported_person_scoped_definition_unit_issues as imported)
    root=Path('.').resolve()
    files=[Path('be/statutes/income_tax/individual')/f for f in [
      'pensioner_pit_oracle_pipeline.yaml',
      'replacement_income_complementary_reduction_parameters.yaml',
      'dependant_net_resources.yaml','dependant_household_conditions.yaml',
      'dependant_article_145_exclusion.yaml','dependant_shared_custody.yaml',
      'dependants.yaml','dependant_article_132_counts.yaml',
      'article_133_isolated_taxpayer_supplement.yaml','article_133_supplements.yaml',
      'article_134_additional_supplement_credit.yaml','tax_free_amount_tax.yaml',
      'regional_autonomy_factor.yaml','pilot_worker_oracle_pipeline.yaml',
      'couple_pit_oracle_pipeline.yaml','final_tax.yaml']]
    total=0
    for file in files:
      content=file.read_text()
      issues=[source_scope(content),rate_base(content),definition(content),
        imported(content,rules_file=file.resolve(),policy_repo_path=root)]
      count=sum(map(len,issues)); total+=count
      print(file.name,'issues',count)
    print('modules',len(files),'person_scope_total_issues',total)
    PY

Every module line printed issues 0; the footer was:

    modules 16 person_scope_total_issues 0

### Built-in proof/money gate and independent exactness override

The pinned built-in command was run over the same sixteen production modules:

    AXIOM_CORPUS_REPO=/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin \
      /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode \
      proof-validate --require-money-atoms --money-atom-root "$PWD" --json \
      be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml \
      be/statutes/income_tax/individual/replacement_income_complementary_reduction_parameters.yaml \
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
      be/statutes/income_tax/individual/final_tax.yaml |
      jq 'if type=="array" then {reports:length,passed_all:all(.passed),
        issues_total:(map(.issues|length)|add),
        money_missing_total:(map(.money_atoms.missing // 0)|add)}
        else {passed,issues,money_atoms} end'

Output:

    {"reports":16,"passed_all":true,"issues_total":0,"money_missing_total":0}

That built-in gate does not detect the stitched page-185/page-186 excerpt. The
58,821-key independent resolver command above is therefore controlling for
the review's explicit verbatim requirement. The money-literal requirement
passed; the findings concern wrong/missing direct legal provenance.

### Repository and full-git-pin validation

    PYTHONDONTWRITEBYTECODE=1 \
      /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python \
      -m pytest -q -p no:cacheprovider tests/test_repository_layout.py

Output:

    29 passed in 21.44s

For strict validation I copied the worktree to a fresh sibling layout under
/private/tmp, symlinked the pinned engine, and supplied the pinned full corpus:

    sol_validate_dir="$(mktemp -d /private/tmp/sol-r7-validate.XXXXXX)"
    rsync -a --exclude .git "$PWD/" "$sol_validate_dir/rulespec-be/"
    ln -s /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine \
      "$sol_validate_dir/axiom-rules-engine"
    cd "$sol_validate_dir/rulespec-be"
    AXIOM_CORPUS_REPO=/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin \
      /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode \
      validate \
      be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml \
      be/statutes/income_tax/individual/replacement_income_complementary_reduction_parameters.yaml \
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
      --skip-reviewers --json |
      jq '[.[] | {file,ci_pass,all_passed,error_count:(.errors|length)}] |
        {modules:length,ci_pass_all:all(.ci_pass),
         all_passed_all:all(.all_passed),rows:.}'

Output summary:

    {"modules":16,"ci_pass_all":true,"all_passed_all":true}

Every row had error_count 0. This is a full-git-pin check, not a signed-release
check: exposing all corpus-be-pin JSONL records is exactly why it can pass
while the five declared #122 paths and #123's hidden page-254/page-257 sources
remain outside the signed frontier.

### Diff hygiene

    { git diff --name-only 5312619..b105e2b3
      git diff --name-only origin/main..HEAD
    } | sort -u |
      rg '(^|/)(\.axiom|\.github|known-validation-gaps|oracle-coverage-pending|toolchain|scoreboard|waiver)' || true

The command emitted nothing. Neither PR changes toolchain, workflow, waiver,
known-gap, oracle-pending, or scoreboard surfaces.

## Independent EUROMOD reruns

### Execution and artifact identity

I extracted and executed the lane drivers verbatim, sequentially in separate
x86-64 processes:

    awk '/^    #!\/usr\/bin\/env python3$/{emit=1}
         /^LANE U DONE$/{emit=0}
         emit{sub(/^    /,""); print}' \
      /Users/maxghenis/TheAxiomFoundation/_cape-prep/beU/rulespec-be/LANE_U_REPORT.md |
      arch -x86_64 env PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
        DOTNET_ROOT=/Users/maxghenis/.dotnet-x64 \
        PYTHONNET_RUNTIME=coreclr POLARS_SKIP_CPU_CHECK=1 \
        /Users/maxghenis/.venvs/axiom-euromod-x64/bin/python \
        - /private/tmp/sol-r7-euromod-123.json

    sed -n '188,377p' LANE_F_REPORT.md |
      arch -x86_64 env PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
        DOTNET_ROOT=/Users/maxghenis/.dotnet-x64 \
        PYTHONNET_RUNTIME=coreclr POLARS_SKIP_CPU_CHECK=1 \
        /Users/maxghenis/.venvs/axiom-euromod-x64/bin/python \
        - /private/tmp/sol-r7-euromod-122.json

Both processes exited 0. Artifact identity was checked with:

    shasum -a 256 \
      /private/tmp/sol-r7-euromod-123.json \
      /private/tmp/lane-u-validate.38uNxC/validate-layout/rulespec-be/euromod_replacement_cases.json \
      /private/tmp/sol-r7-euromod-122.json \
      /private/tmp/lane-f-engine-matrix-final.MobyCj/rulespec-be/scratch_lane_f_euromod_cases.json
    cmp -s /private/tmp/sol-r7-euromod-123.json \
      /private/tmp/lane-u-validate.38uNxC/validate-layout/rulespec-be/euromod_replacement_cases.json
    printf 'U_CMP_EXIT=%s\n' "$?"
    cmp -s /private/tmp/sol-r7-euromod-122.json \
      /private/tmp/lane-f-engine-matrix-final.MobyCj/rulespec-be/scratch_lane_f_euromod_cases.json
    printf 'F_CMP_EXIT=%s\n' "$?"

Output:

    aab2f22c663783b74f5337fbe0a6035bfe408d52ac67823e2b44b24495cbc9da  /private/tmp/sol-r7-euromod-123.json
    aab2f22c663783b74f5337fbe0a6035bfe408d52ac67823e2b44b24495cbc9da  /private/tmp/lane-u-validate.38uNxC/validate-layout/rulespec-be/euromod_replacement_cases.json
    5959a40cb2d455672fcc4060ebb0c1af467ec4fedf9c17e28a7e275638503242  /private/tmp/sol-r7-euromod-122.json
    5959a40cb2d455672fcc4060ebb0c1af467ec4fedf9c17e28a7e275638503242  /private/tmp/lane-f-engine-matrix-final.MobyCj/rulespec-be/scratch_lane_f_euromod_cases.json
    U_CMP_EXIT=0
    F_CMP_EXIT=0

Both reruns retained, rather than suppressed, connector diagnostics:

    jq '{probe_errors,errors,missing_columns,case_count:(.cases|length)}' \
      /private/tmp/sol-r7-euromod-123.json
    jq '{probe_errors,errors,missing_columns,case_count:(.cases|length)}' \
      /private/tmp/sol-r7-euromod-122.json

Output for both files reports case_count 7 and the same two messages:

    Variable(s) yds, lindi, yptmp, tad, tis not found in user-provided lists (zero is used as default)
    2.1 uprate_be/Uprate (43a9959d-ec21-446c-9223-8d69af445b1b): variable(s) bunpe01, bunpe02, xcc, yempv, yiyitdp is/are uprated with default factor (1.050524934383202)

#123 has missing_columns []; #122 has missing_columns ["tintadch_s"].

### #123: five direct comparison cases and residual mechanisms

The green companion command above live-evaluates the Axiom expectations. This
command reads those exact outputs and the fresh EUROMOD JSON:

    PYTHONDONTWRITEBYTECODE=1 \
    /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
    import json,yaml
    from decimal import Decimal as D
    cs={c['name']:c for c in yaml.safe_load(open(
      'be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.test.yaml'))}
    eu={c['label']:c for c in json.load(open(
      '/private/tmp/sol-r7-euromod-123.json'))['cases']}
    rows=[
      ('unemployment_12k','unemployment_12k_euromod_input_bun_zero_tax'),
      ('unemployment_18k','unemployment_18k_euromod_input_bun_zero_tax'),
      ('unemployment_24k','unemployment_24k_euromod_articles_147_to_153'),
      ('unemployment_15k_wage_15k','unemployment_15k_plus_wage_15k_no_activity_exclusion'),
      ('sickness_bhl_18k','sickness_18k_euromod_bhl_article_153_cap')]
    for label,name in rows:
      ax=next(v for k,v in cs[name]['output'].items()
        if k.endswith('belgium_pit_pensioner_federal_and_local_tax_before_withholding'))
      ev=eu[label]['tin_s_annual']
      print(label,'axiom',ax,'euromod',ev,
        'euromod_minus_axiom',D(str(ev))-D(str(ax)))
    PY

Output:

    unemployment_12k axiom 0 euromod 0.0 euromod_minus_axiom 0.0
    unemployment_18k axiom 0 euromod 0.0 euromod_minus_axiom 0.0
    unemployment_24k axiom 1475.6238264363934426229508197 euromod 1475.6238264363938 euromod_minus_axiom 3.573770491803E-13
    unemployment_15k_wage_15k axiom 1690.2437254013500482160077145 euromod 1163.0377081352365 euromod_minus_axiom -527.2060172661135482160077145
    sickness_bhl_18k axiom 0 euromod 0.0 euromod_minus_axiom 0.0

The U24 remainder is only decimal-versus-binary output serialization and is
far below one cent; it is not labelled as a substantive tax mechanism. The
mixed-case residual has exactly two named, quantified mechanisms, reproduced
from the fresh outputs:

    python3 - <<'PY'
    from decimal import Decimal as D, getcontext
    getcontext().prec=50
    ax_extra=D('96.4136547733847637415621986577')
    eu_extra=D('163.90321311475395')
    autonomy=D('.75043')
    ax_credit=D('1028.28906')
    eu_credit=D('1504.8488879999998')
    ax_final=D('1690.2437254013500482160077145')
    eu_final=D('1163.0377081352365')
    share=-(eu_extra-ax_extra)*autonomy
    work=-(eu_credit-ax_credit)
    observed=eu_final-ax_final
    print('item8_share_proration_effect',share)
    print('work_credit_effect',work)
    print('mechanism_sum',share+work)
    print('observed_euromod_minus_axiom',observed)
    print('remainder',observed-share-work)
    PY

Output:

    item8_share_proration_effect -50.646189266113678443919479261302189
    work_credit_effect -476.5598279999998
    mechanism_sum -527.206017266113478443919479261302189
    observed_euromod_minus_axiom -527.2060172661135482160077145
    remainder -6.9772088235238697811E-14

Mechanism one is EUROMOD's additional unemployment reduction omitting the
Article 147 item-8 unemployment share before autonomy. Mechanism two is
EUROMOD's larger uncapped work-credit result. Their printed sum closes to the
observed residual with only the printed floating remainder.

### #122: seven direct comparison cases and residual ledger

The Axiom final amounts below are extracted from the companions that the
sixteen-file command live-evaluated:

    PYTHONDONTWRITEBYTECODE=1 \
    /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/python - <<'PY'
    import yaml
    files=['be/statutes/income_tax/individual/couple_pit_oracle_pipeline.test.yaml',
      'be/statutes/income_tax/individual/pilot_worker_oracle_pipeline.test.yaml']
    cases={c['name']:c for f in files for c in yaml.safe_load(open(f))}
    rows=[
      ('single_earner_couple_30k_1_child','single_earner_30k_one_child_refundable_credit_binds_at_joint_cap'),
      ('single_earner_couple_30k_2_children','lane_f_single_earner_30k_two_children'),
      ('single_earner_couple_45k_1_child','lane_f_single_earner_45k_one_child'),
      ('single_earner_couple_45k_2_children','lane_f_single_earner_45k_two_children'),
      ('two_earner_couple_45k_30k_2_children','two_earner_45k_and_30k_with_two_eligible_children_feeds_joint_article_132'),
      ('single_parent_30k_1_child','single_parent_30k_with_one_dependent_child_gets_article_133_supplements'),
      ('low_single_parent_18k_2_children','low_earner_18k_with_two_dependent_children_gets_capped_refundable_child_credit')]
    for label,name in rows:
      values=[v for k,v in cases[name]['output'].items() if k.endswith(
        ('belgium_pit_couple_federal_and_local_tax_before_withholding',
         'belgium_pit_pilot_federal_and_local_tax_before_withholding'))]
      print(label,values[-1])
    PY

Output:

    single_earner_couple_30k_1_child -1522.233168
    single_earner_couple_30k_2_children -2092.233168
    single_earner_couple_45k_1_child 2449.96259035
    single_earner_couple_45k_2_children 1696.271972
    two_earner_couple_45k_30k_2_children 7024.67638955
    single_parent_30k_1_child 932.5100211903696498054474707
    low_single_parent_18k_2_children -2814.231

This command joins those values to the fresh EUROMOD JSON and partitions each
residual at observable output-stage boundaries:

    jq -n --slurpfile oracle /private/tmp/sol-r7-euromod-122.json '
      def eu($label): $oracle[0].cases[] | select(.label == $label);
      def row($label;$axiom_final;$axiom_work;$axiom_child;$axiom_article133):
        (eu($label)) as $e
        | ($axiom_final+$axiom_work+$axiom_child+$axiom_article133) as $pre
        | [{mechanism:"pre_family_reduced_state_tax_stage",
             amount:($pre-$e.tinna_s_annual_sum)},
           {mechanism:"work_bonus_credit",
             amount:($e.tintcly_s_annual_sum-$axiom_work)},
           {mechanism:"article_134_child_credit",
             amount:($e.tintcch_s_annual_sum-$axiom_child)},
           {mechanism:"article_133_additional_refundable_credit",
             amount:(0-$axiom_article133)}] as $parts
        | {case:$label,axiom:$axiom_final,euromod:$e.tin_s_annual_sum,
           delta:($axiom_final-$e.tin_s_annual_sum),parts:$parts,
           closure_error:(($axiom_final-$e.tin_s_annual_sum)
             -($parts|map(.amount)|add))};
      [row("single_earner_couple_30k_1_child";-1522.233168;952.233168;570;0),
       row("single_earner_couple_30k_2_children";-2092.233168;952.233168;1140;0),
       row("single_earner_couple_45k_1_child";2449.96259035;0;0;0),
       row("single_earner_couple_45k_2_children";1696.271972;0;0;0),
       row("two_earner_couple_45k_30k_2_children";7024.67638955;952.233168;0;0),
       row("single_parent_30k_1_child";932.5100211903696498054474707;952.233168;0;0),
       row("low_single_parent_18k_2_children";-2814.231;1158.231;1140;516)]' |
      jq -r '.[] | [.case,.axiom,.euromod,.delta,
        ([.parts[]|select(.amount!=0)|
          (.mechanism+"="+(.amount|tostring))]|join(";")),
        .closure_error]|@tsv'

Output:

    single_earner_couple_30k_1_child  -1522.233168  -1605.8388879999973  83.60571999999729  work_bonus_credit=552.6157199999998;article_134_child_credit=-469.0100000000025  0
    single_earner_couple_30k_2_children  -2092.233168  -2644.8488879999995  552.6157199999993  pre_family_reduced_state_tax_stage=-2.2737367544323206E-13;work_bonus_credit=552.6157199999998  -2.2737367544323206E-13
    single_earner_couple_45k_1_child  2449.96259035  2443.8398177719537  6.1227725780463516  pre_family_reduced_state_tax_stage=-31.64263353709839;work_bonus_credit=37.765406115144614  1.2789769243681803E-13
    single_earner_couple_45k_2_children  1696.271972  1692.714818357394  3.557153642605954  pre_family_reduced_state_tax_stage=-34.20825247253856;work_bonus_credit=37.765406115144614  -9.947598300641403E-14
    two_earner_couple_45k_30k_2_children  7024.67638955  6793.625893966462  231.05049558353767  pre_family_reduced_state_tax_stage=-359.3306305316073;work_bonus_credit=590.3811261151443  6.821210263296962E-13
    single_parent_30k_1_child  932.5100211903696498054474707  761.1334181648349  171.3766030255348  pre_family_reduced_state_tax_stage=-381.2391169744651;work_bonus_credit=552.6157199999998  1.1368683772161603E-13
    low_single_parent_18k_2_children  -2814.231  -2644.8488879999995  -169.3821120000007  pre_family_reduced_state_tax_stage=-2.2737367544323206E-13;work_bonus_credit=346.61788799999977;article_133_additional_refundable_credit=-516  -2.2737367544323206E-13

The recurring work-credit component is the named Axiom encoded ONSS
full-year/equal-month construction versus EUROMOD's uprated monthly
tintcly result. The child-credit component is the named Article 134 allocation
and cap difference. The Article 133 component is explicitly absent from the
connector because tintadch_s is the missing column printed above. The
pre-family component is only a localization boundary, not a causal legal
mechanism. I therefore do not call the four rows with a material pre-family
component explained; they remain quantified gaps. The required three-case
minimum is met by the two 30k single-earner-couple rows and the low-income
single-parent row: their material residuals close to the named work-credit,
child-credit, and absent-Article-133-output mechanisms, with only the printed
binary-serialization remainders. These EU residuals neither cause nor excuse
the live legal blockers.

## Legal surfaces with no additional reproduced liability finding

Against the pinned pages, the Article 132 child ladder, disability doubling,
under-three exclusion, Article 132bis half-share eligibility, Articles 136
through 143 household/resource gates, Article 145 supplied exclusion gate,
Article 133 amount/phaseout arithmetic, and the Article 134 paragraph 3
child/additional ordering produced no additional liability finding in the
official and adversarial cases run here. This statement does not waive the
five missing release paths, the wrong Article 132bis proof source, or the
composition-root proof omissions.

## Flat failure and diagnostic ledger

No failed attempt was used as evidence:

1. The GitNexus PR-review skill was invoked, but the read-only status command
   returned:

       gitnexus status
       Repository not indexed.
       Run: gitnexus analyze

   Running analyze would write index state outside the sole permitted report
   edit, so I used read-only git diffs, import closure, corpus resolution, and
   direct engine execution.

2. The first relative path used for the prior sol report resolved under the
   current beR7 directory and failed with “No such file or directory”. I reran
   it against the explicit
   /Users/maxghenis/TheAxiomFoundation/_cape-prep/beI/rulespec-be/SOL_REVIEW_119_120.md
   path before applying its standard.

3. A first multi-revision git rev-parse --short invocation failed with
   “Needed a single revision”. The per-revision loop in the scope section is
   the successful rerun and is the only pin output used.

4. A first proof one-liner contained a literal escaped newline and failed with
   SyntaxError. A later proof-validate jq projection also assumed an object
   while the multi-file command returned an array. The raw rerun and the
   successful type-aware projection are reported above.

5. The first atom scanner loaded only the consolidated CIR JSONL and therefore
   reported the separate regional-autonomy regulation atoms as false
   negatives. The controlling scanner recursively loads every provisions
   JSONL and leaves exactly the keyed Article 134 failure printed above.

6. The first direct multi-case harness accepted the Article 466 case but then
   aborted because an unqualified relation name was rejected. A second
   diagnostic requested imported outputs under the pilot namespace and also
   failed. Neither partial run was used. The complete legal-ID/relation-aware
   harness reported above exited successfully for both adversarial cases.

7. An early all-dependency assignment heuristic mixed imported facts with
   local facts and therefore could not decide the campaign gate. I initially
   rejected its apparent misses. The corrected prefix-aware rerun excludes
   imports, preserves relation context, and confirms the #122 full-assignment
   blocker reported above; it is the controlling result.

8. One single-module validation jq expression indexed an object as an array
   and failed with “Cannot index object with number”. The corrected
   multi-module validation summary above succeeded.

9. A combined git diff command incorrectly supplied two ranges to one
   invocation and printed usage. It was rerun as two commands inside braces;
   the successful forbidden-surface scan above emitted nothing.

10. The first #123 artifact comparison named a non-existent report-worktree
    JSON path and returned a missing-file diagnostic with U_CMP_EXIT=2. A
    read-only find located the retained Lane-U validation artifact; the
    corrected hash/cmp command above returned U_CMP_EXIT=0.

11. Two convenience extraction scripts initially used the wrong companion
    field name and one wrong case name, raising KeyError. The corrected
    extraction commands and their complete outputs are printed in the
    EUROMOD sections.

12. A jq search for Article 304 applied contains to a null body and stopped
    on that row. The final citation-path-keyed page lookup in the Article 466
    finding succeeded and is the only corpus output used.

13. EUROMOD's two non-fatal missing/default-uprating diagnostics were retained
    verbatim above. The #122 connector also lacked tintadch_s; the residual
    ledger treats its Article 133 component as absent rather than inventing a
    value.

## Final worktree check

Immediately before finalizing:

    git status --short
    git diff --check 5312619..b105e2b3
    git diff --check origin/main..HEAD

The status command printed only:

    ?? SOL_REVIEW_122_123.md

Both diff-check commands emitted nothing. No source, test, configuration,
ledger, or generated artifact in the repository was modified.

VERDICT #123: NEEDS-FIX

VERDICT #122: DO-NOT-SHIP

SOL REVIEW DONE
