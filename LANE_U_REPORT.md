# Lane U — unemployment and sickness/invalidity replacement-income PIT

Run date: 2026-08-22. Branch ledger/unemployment, branched from Lane P at
2c84eb9. The canonical RuleSpec changes are committed locally as 9baafa8
("Encode unemployment and sickness PIT reductions"). Nothing was pushed.
This report is a worktree-root handoff artifact and is intentionally not part
of that code commit, matching Lane P's handoff layout.

Baseline/commit command:

    git branch --show-current
    git merge-base HEAD 2c84eb9
    git rev-parse HEAD
    git show --stat --oneline --summary HEAD

Observed:

    ledger/unemployment
    2c84eb9b5bcd853e430fbfbb0c7c31a22b0a3887
    9baafa8bd557c04049035ca38e4bcb57af495db1
    9baafa8 Encode unemployment and sickness PIT reductions
     .../pensioner_pit_oracle_pipeline.test.yaml        | 522 +++++++++++++++++++++
     .../individual/pensioner_pit_oracle_pipeline.yaml  | 380 ++++++++++++++-
     ...me_complementary_reduction_parameters.test.yaml |   9 +
     ..._income_complementary_reduction_parameters.yaml |  26 +
     4 files changed, 918 insertions(+), 19 deletions(-)

## 1. Outcome

I chose the smaller extension: Lane P's Person-scoped pensioner pipeline is
generalized in place by replacement-income category while its filename and
legacy pension outputs remain stable. It now covers:

- gross unemployment benefit, with no personal SSC in the observed BE_2025
  INPUT-bun path;
- gross sickness indemnity and gross invalidity indemnity, with a supplied
  invalidity social-withholding boundary before Article 23 paragraph 2 netting;
- ordinary Articles 130, 131 and 134 tax;
- Article 147 items 7–10, Article 151 and 151/1 phase-outs, Article 152,
  Article 153 category caps, and the Article 154 sections 1–3/1 structure;
- the imported autonomy factor, imported actual-work-bonus credit, and supplied
  communal/agglomeration additions.

The required pure unemployment 12k/18k cases, U24 under the explicitly
EU-comparable supplied M=20k, and sickness bhl 18k case match EUROMOD BE_2025
to the cent. Articles 147–153 at U24 match independently; Article 154 itself
is euromod_non_simulated. The required unemployment 15k plus wage 15k case has
a fully quantified EUROMOD-minus-Axiom residual of
-527.2060172661135 EUR: -50.6461892661138 EUR from EUROMOD function 63 omitting
the Article 147 unemployment-share proration on the additional amount after
autonomy, and -476.559828 EUR from EUROMOD's uncapped work-bonus credit. The
floating remainder is about 2.42e-13 EUR. Both mechanisms are
engine_semantics; nothing is left unexplained.

Article 154 functions 54–61 are n/a in the BE_2025 baseline and are therefore
euromod_non_simulated. The Axiom branches are encoded and regression-tested,
but their page-257/page-258 legal details are explicitly classified at the
signed-release frontier rather than treated as released proofs.

## 2. Corpus resolution and encodability frontier

The resolver source is the pinned provisions JSONL, keyed by citation_path.
This command establishes the corpus pin and prints every relevant record in
full:

    git -C /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin rev-parse HEAD
    python3 - <<'PY'
    import json
    path = (
        "/Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin/"
        "data/corpus/provisions/be/statute/"
        "2026-06-30-be-income-tax-consolidated.jsonl"
    )
    wanted = {
        f"be/statute/fisconetplus/cir92/revenus-2025/page-{page}"
        for page in range(252, 259)
    }
    with open(path) as stream:
        for line_number, line in enumerate(stream, 1):
            record = json.loads(line)
            if record.get("citation_path") in wanted:
                print(line_number, record["citation_path"])
                print(record["body"])
    PY

Observed corpus commit:

    8e48989c9e46faa6d85a9624b7a2ebda0880656d

Resolver map emitted by that command:

| Provision | JSONL line | citation_path page | Branch treatment |
|---|---:|---:|---|
| Article 146 definitions | 253 | 252 | resolved as input contract; unencoded_corpus_blocked (release lacks page 252) |
| Article 147 items 7–9 | 254 | 253 | promoted and encoded |
| Article 147 item 10 and activity definition | 255 | 254 | encoded on branch; release lacks page 254 |
| Articles 150, 151, 151/1 | 256 | 255 | promoted and encoded |
| Articles 152, 153, Article 154 §1/start of §2 | 257 | 256 | promoted and encoded |
| Article 154 remainder §2, §3, §3/1 | 258 | 257 | encoded on branch; release lacks page 257 |
| Article 154 §4 vintage rule | 259 | 258 | release lacks page 258; numeric M remains input_carrying |

The governing signed-release command is:

    sed -n '1,12p' .axiom/toolchain.toml
    sed -n '73,84p' /Users/maxghenis/TheAxiomFoundation/_cape-prep/LEDGER_CAMPAIGN.md

It identifies release be-rulespec-2026-07-10 and the campaign's promoted CIR
set. Of the pages above, only 253, 255 and 256 are promoted. Thus
unencoded_corpus_blocked means exactly: "encoded on branch; release lacks page
N." It does not mean that the pinned git corpus was ignored. The module
accepts already classified unemployment and statutory sickness/invalidity
gross inputs; it does not implement Article 146's source
eligibility/exclusion screening.

### 2.1 Verbatim resolved law

The preceding resolver command produced these exact substrings.

Article 146 items 3 and 4, page 252:

> 3° allocations de chômage: les allocations légales et extra-légales de toute nature, obtenues en réparation totale ou partielle d'une perte temporaire de rémunérations résultant d'un chômage involontaire complet ou partiel mais à l'exclusion des allocations visées à l'article 31bis, alinéa 2, 1°, ainsi que le revenu obtenu pour des prestations fournies dans le cadre d'un contrat de travail ALE, à concurrence du solde restant après application de l'article 38, § 1er, alinéa 1er, 13°;

> 4° indemnités légales d'assurance en cas de maladie ou d'invalidité: les indemnités octroyées en exécution de la législation relative à l'assurance en cas de maladie ou d'invalidité;

Article 147 items 7–9, promoted page 253:

> 7° lorsque le revenu net se compose exclusivement d'allocations de chômage: une réduction de base de 2.219,27 euros (montant indexé) et une réduction additionnelle de 457,23 euros (montant indexé);

> 8° lorsque le revenu net se compose partiellement d'allocations de chômage: une quotité des montants visés au 7°, proportionnelle au rapport entre, d'une part, le montant net des allocations de chômage et, d'autre part, le montant du revenu net;

> 9° lorsque le revenu net se compose exclusivement d'indemnités légales d'assurance en cas de maladie ou d'invalidité: 2.977,93 euros (montant indexé);

Article 147 item 10, pinned-only page 254:

> 10° lorsque le revenu net se compose partiellement d'indemnités légales d'assurance en cas de maladie ou d'invalidité: une quotité du montant visé au 9°, proportionnelle au rapport entre, d'une part, le montant net des indemnités légales d'assurance en cas de maladie ou d'invalidité et, d'autre part, le montant du revenu net.

This resolves Lane P's activity-income question: the special activity-income
exclusions occur in Article 147 item 2 for pensions and other replacement
income. Item 8 and item 10 instead name the full net-income denominator.
Consequently, the mixed unemployment+wage case excludes no activity income.

Article 150, promoted page 255:

> Lorsqu'une imposition commune est établie, les réductions et les limites prévues par la présente sous- section sont calculées par contribuable.

The module is Person-scoped for that per-taxpayer calculation. It does not
claim to implement spouse aggregation or the joint-assessment clauses later in
Article 154.

Article 151, promoted page 255:

> Lorsque le revenu imposable atteint ou dépasse 35.930 euros (montant indexé), les réductions pour allocations de chômage autres que celles qui sont attribuées aux chômeurs âgés de 58 ans ou plus au 1er janvier de l'exercice d'imposition et comprenant un complément d'ancienneté, n'est pas accordée.

> Lorsque le revenu imposable est compris entre 28.780 euros (montant indexé) et 35.930 euros (montant indexé), ces réductions ne sont accordées qu'à concurrence d'une quotité déterminée par le rapport qu'il y a entre, d'une part, la différence entre 35.930 euros (montant indexé) et le revenu imposable et, d'autre part, la différence entre 35.930 euros (montant indexé) et 28.780 euros (montant indexé).

Article 153, promoted page 256:

> Aucune des réductions prévues à la présente sous-section ne peut excéder la quotité de l'impôt déterminé conformément aux articles 130 à 145 qui est afférente aux revenus à raison desquels elle est accordée.

Article 154 §1 and the start of §2, promoted page 256:

> § 1. Une réduction complémentaire est accordée lorsque le revenu net total est exclusivement composé: 1° d'allocations de chômage; 2° d'allocations de chômage d'une part, et de pensions, indemnités légales d'assurance en cas de maladie ou d'invalidité ou d'autres revenus de remplacement d'autre part.

> La réduction supplémentaire est égale à 40 % de l'impôt qui subsiste après application des articles 147 à 153, lorsque l'ensemble des revenus nets se compose exclusivement:

Article 154 remainder §2, §3 and §3/1, pinned-only page 257:

> 1° d'allocations de chômage et que le montant de ces allocations n'excède pas le montant maximum de l'allocation légale de chômage qui peut être attribuée pendant les douze premiers mois de chômage complet; 2° d'allocations de chômage d'une part, et de pensions, indemnités légales d'assurance en cas de maladie ou d'invalidité ou d'autres revenus de remplacement d'autre part et que le montant total de ces revenus n'excède pas 19.630 euros (montant indexé).

> § 3. Dans les autres cas que ceux visés au § 2 et lorsque l'ensemble des revenus nets se compose exclusivement d'allocations de chômage, la réduction supplémentaire est égale à 40 % de la différence positive entre: 1° le montant de l'impôt qui subsiste après application des articles 147 à 153 et 2° la différence entre ces allocations de chômage et le montant maximum applicable conformément au § 2, alinéa 1er, 1°.

> § 3/1. Dans les autres cas que ceux visés aux paragraphe 2 et lorsque l'ensemble des revenus nets se compose exclusivement d'allocations de chômage d'une part et de pensions, d'indemnités légales d'assurance en cas de maladie ou d'invalidité ou d'autres revenus de remplacement d'autre part, la réduction supplémentaire est égale à 40 % de la différence positive entre: 1° le montant de l'impôt qui subsiste après application des articles 147 à 153 et 2° 90 % de la différence entre le montant des revenus de remplacement et, le cas échéant, des pensions et 19.630 euros (montant indexé).

The same page requires proportional allocation over the category-specific tax
remaining after Articles 147–153. Section 4 on page 258 fixes the vintage basis
for the maximum unemployment amount but supplies no numeric M in this
subsection.

### 2.2 Encoded formulas

Let Y be taxable/net income in this slice, U net unemployment, S net statutory
sickness/invalidity, P net pension, T the tax after the tax-free amount, and M
the supplied first-twelve-month maximum unemployment benefit.

- Item 8 unemployment ratio: min(1, U / Y), with a zero-denominator guard.
- Item 10 sickness/invalidity ratio: min(1, S / Y), with the same guard.
- Unemployment base: 2,219.27 × U/Y; additional: 457.23 × U/Y.
- Article 151 base factor: one through 28,780; then
  (35,930 − Y)/(35,930 − 28,780); zero at/above 35,930, except when the supplied
  older-unemployed-with-seniority condition is true.
- Article 151/1 additional factor: one through 19,630; then
  (28,780 − Y)/(28,780 − 19,630); zero at/above 28,780.
- Sickness/invalidity amount: 2,977.93 × S/Y, followed by Article 152.
- Article 153: each category reduction is capped by its category income share
  times T.
- Pure unemployment Article 154: 40% × T-rem when U ≤ M; otherwise
  40% × max(0, T-rem − (U − M)).
- Mixed unemployment plus replacement income: 40% × T-rem through 19,630;
  otherwise 40% × max(0, T-rem − q × (U+P+S−19,630)), with q supplied as
  90%, followed by the §3/1 category allocation.

The values and thresholds are imported where already canonical:

    rg -n \
      'article_147_(basic|additional|sickness)|article_151_|article_1511_|article_152_' \
      be/statutes/income_tax/individual/tax_reductions_and_credits.yaml
    rg -n \
      'article_154_complementary_reduction_rate|0.40' \
      be/statutes/income_tax/individual/replacement_income_complementary_reduction_parameters.yaml

No numeric M was invented. M is input_carrying. The 90% q is a supplied input;
its legal mechanism is unencoded_corpus_blocked because its proof page is not
promoted. Only the 40% rate is a new canonical parameter, imported from the
small companion module and proven verbatim at the start of §2 on promoted page
256. That proof does not promote the §3/§3/1 mechanics on page 257.

## 3. Module map

Changed canonical files:

- be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml
- be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.test.yaml
- be/statutes/income_tax/individual/replacement_income_complementary_reduction_parameters.yaml
- be/statutes/income_tax/individual/replacement_income_complementary_reduction_parameters.test.yaml

The generalized pipeline remains entirely Person-scoped:

| Stage | Principal outputs/mechanics |
|---|---|
| Gross to net | pension AMI/solidarity; U passes gross to net in BE_2025; S/I deducts supplied invalidity withholding |
| Article 23 §2 | per-category net pension, U and S/I |
| Taxable income | P + U + S/I + imported worker net professional income |
| Articles 130/131/134 | imported brackets/rates, base TFA and tax on TFA |
| Article 147 | separate P, U and S/I shares and raw reductions |
| Articles 151/151-1/152 | category-appropriate phase-outs |
| Article 153 | separate attributable-tax caps |
| Article 154 | eligibility, pure-U and mixed formulas, §3/1 allocation |
| Post-federal | imported autonomy factor, imported actual work-bonus credit, supplied local additions |

Lane U adds these seven inputs:

    belgium_pit_replacement_annual_gross_unemployment_benefit
    belgium_pit_replacement_annual_gross_sickness_benefit
    belgium_pit_replacement_annual_gross_invalidity_benefit
    belgium_pit_replacement_annual_invalidity_social_withholding
    belgium_pit_replacement_article_151_older_unemployed_with_seniority_supplement
    belgium_pit_replacement_article_154_first_twelve_month_maximum_unemployment_benefit
    belgium_pit_replacement_article_154_mixed_replacement_excess_rate

Every companion case assigns every reachable input, including false booleans.
This command verifies full assignment:

    python3 - <<'PY'
    import yaml
    path = (
        "be/statutes/income_tax/individual/"
        "pensioner_pit_oracle_pipeline.test.yaml"
    )
    cases = yaml.safe_load(open(path))
    counts = [len(case["input"]) for case in cases]
    print("cases=", len(cases), sep="")
    print("input_counts=", sorted(set(counts)), sep="")
    print("all_full_assignment=", all(count == 15 for count in counts), sep="")
    PY

Observed:

    cases=23
    input_counts=[15]
    all_full_assignment=True

The separate atomic-parameter companion adds one case; the combined runner
count is in §7.

The compile command:

    git -C /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine rev-parse HEAD
    lane_u_compiled=$(mktemp /private/tmp/lane-u-compiled.XXXXXX)
    AXIOM_RULESPEC_REPO_ROOTS="$PWD" \
      /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine/target/release/axiom-rules-engine \
      compile \
      --program "$PWD/be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml" \
      --output "$lane_u_compiled"

reported the pinned engine commit and artifact properties:

    c6cc389a8f5e7238019e4fa06849325fad9acd46
    derived_outputs: 192
    fast_path_compatible: true
    fast_path_strategy: generic_bulk

## 4. EUROMOD BE_2025 mechanics

The model source read was:

    /Users/maxghenis/Downloads/EUROMOD_J2.0/EUROMOD_RELEASES_J2.0+/XMLParam/Countries/BE/BE.xml

This namespaced XML extraction command produced the policy/function evidence:

    python3 - <<'PY'
    from lxml import etree
    path = (
        "/Users/maxghenis/Downloads/EUROMOD_J2.0/"
        "EUROMOD_RELEASES_J2.0+/XMLParam/Countries/BE/BE.xml"
    )
    root = etree.parse(path)
    ns = {"e": "http://euromod.com/CountryConfig.xsd"}
    ids = [
        "a3b45d8e-c974-4ff7-964d-44ccc628736a",
        "306ebcc9-91db-4d98-a2b3-c69640e3f141",
        "fa5a00d1-2cf3-4528-be03-2ec06a0737b9",
    ]
    for policy_id in ids:
        policy = root.xpath(
            f'.//e:Policy[e:ID="{policy_id}"]', namespaces=ns
        )[0]
        get = lambda node, name: node.findtext("e:" + name, namespaces=ns)
        print("POLICY", policy_id, get(policy, "Name"), get(policy, "Switch"))
        for function in policy.findall("e:Function", ns):
            order = int(get(function, "Order"))
            if policy_id == ids[0] and not 46 <= order <= 63:
                continue
            print(
                "FUNCTION", order, get(function, "ID"),
                get(function, "Comment"), get(function, "Switch")
            )
            for parameter in function.findall("e:Parameter", ns):
                name = get(parameter, "Name")
                if name in {
                    "Formula", "Output_Var", "Elig_Cond", "Comp_Cond",
                    "Comp_perElig", "UpLim", "Base", "name", "pdi"
                }:
                    print(name, "=", get(parameter, "Value"))
    PY

Resolved mechanics:

| Block | XML identity | Baseline state and meaning |
|---|---|---|
| Federal PIT | policy a3b45d8e-c974-4ff7-964d-44ccc628736a, tinna_be | on |
| Unemployment benefit simulation | policy 306ebcc9-91db-4d98-a2b3-c69640e3f141, bun_be | off; euromod_non_simulated; use INPUT bun, not bun_s |
| Horizontal P/S reduction | function 46, ffd87b0d-3de5-4219-86ff-0ae5ee414abb | on; sickness uses il_netsickY/il_taxableY_bf_mq |
| Vertical P/S limit | function 47, de37aa7a-e383-4e8f-91e8-08b923ce1328 | on |
| Horizontal U reduction | function 48, b2cc0e9c-36cb-4195-93af-9c5d1ea04e99 | on; bun share of il_taxableY_bf_mq |
| Vertical U limit | function 49, fc3886c8-965e-48ee-98a9-74bcb4d1861b | on |
| Attributable-tax cap | function 52, 3ed9810e-0dec-41a2-92f5-93f4d94563d5 | on |
| Article 154-like extra-reduction blocks | functions 54–61 | every block n/a; euromod_non_simulated |
| Article 147 additional amount/taper | functions 62/63, 433e0878... / bbfc5ff3... | on; these are not the Article 154 blocks |
| Disability SSC income list | tscee_be function 1, c5e8cb4d-99b9-4c00-bcbe-ab28e861914b | il_disabY contains pdi only |

The XML and observed outputs jointly resolve the SSC question. In each pure
bun case, annual bun equals annual il_netrepY and taxable income; tscdb_s,
tscee_s and tscpe_s are zero. The active employee-contribution policy applies
its ordinary components to yem, and its disability contribution consumes
il_disabY, whose defining function contains pdi only. There is no bun term.
The required sickness bhl 18k case also has zero tscdb_s. Invalidity remains a
separate supplied-withholding composition boundary in Axiom rather than being
conflated with this bhl oracle.

## 5. Exact EUROMOD comparison

The exact driver is reproduced verbatim in §8. It was run once for probes and
once for cases in one x64 process:

    arch -x86_64 env PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
      DOTNET_ROOT=/Users/maxghenis/.dotnet-x64 \
      PYTHONNET_RUNTIME=coreclr \
      POLARS_SKIP_CPU_CHECK=1 \
      /Users/maxghenis/.venvs/axiom-euromod-x64/bin/python \
      euromod_replacement_cases.py euromod_replacement_cases.json

The driver uses model EUROMOD_RELEASES_J2.0+, system BE_2025, dataset
BE_2024_c1_2015_03_e2 and template BE_training_data. It probes and neutralizes
these observed uprating factors:

| Input | Probed factor |
|---|---:|
| yem | 1.055022392834293 |
| bun | 1.0793082886106142 |
| pdi | 1.1096513390601312 |
| phl | 1.1096513390601312 |
| bhl | 1.1096513390601312 |

It returned two output frames, no missing requested columns, and these
non-fatal diagnostics verbatim:

    Variable(s) yds, lindi, yptmp, tad, tis not found in user-provided lists (zero is used as default)
    2.1 uprate_be/Uprate (43a9959d-ec21-446c-9223-8d69af445b1b): variable(s) bunpe01, bunpe02, xcc, yempv, yiyitdp is/are uprated with default factor (1.050524934383202)

The Axiom side is the passing companion suite:

    /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode \
      test --root "$PWD" \
      --axiom-rules-engine-path /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine \
      be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.test.yaml \
      be/statutes/income_tax/individual/replacement_income_complementary_reduction_parameters.test.yaml

All values below are annual EUR. EUROMOD monthly columns are multiplied by 12
in the driver. Local additions are supplied as zero.

| Case | Taxable income both | EU tintcri_s | Axiom Articles 147–153 reduction | EU tin_s | Axiom final | Classification |
|---|---:|---:|---:|---:|---:|---|
| INPUT bun 12k | 12,000 | 272.5000000000001 | 272.5 | 0 | 0 | MATCHED |
| INPUT bun 18k | 18,000 | 2,024.5 | 2,024.5 | 0 | 0 | MATCHED |
| INPUT bun 24k | 24,000 | 2,458.128950819672 | 2,458.1289508196721311475409836 | 1,475.6238264363938 | 1,475.6238264363934426229508197 | MATCHED under supplied M=20k; Article 154 euromod_non_simulated, M input_carrying |
| INPUT bun 15k + yem 15k | 25,500 | 1,469.3561542912246 | 1,401.8665959498553519768563164 | 1,163.0377081352365 | 1,690.2437254013500482160077145 | EXPLAINED |
| INPUT bhl 18k | 18,000 | 2,024.5 | 2,024.5 | 0 | 0 | MATCHED |

For the pure-U stages, the same EU output gives:

| Case | tints_s | tintatc_s | tax after TFA | bun_s | personal SSC columns |
|---|---:|---:|---:|---:|---:|
| U12 | 3,000 | 2,727.5 | 272.5 | 0 | 0 |
| U18 | 4,752 | 2,727.5 | 2,024.5 | 0 | 0 |
| U24 | 7,152 | 2,727.5 | 4,424.5 | 0 | 0 |

At U24 the Axiom Article 151/1 factor is
0.5224043715846994535519125683, its reduction is
2,458.1289508196721311475409836, and the tax remaining after Articles 147–153
is 1,966.3710491803278688524590164. The EU-comparable test supplies M=20,000,
which makes the Article 154 branch zero; that value is illustrative and is
not asserted as Belgium's statutory M. Applying the imported autonomy factor
then produces the cent-exact final result.

For bhl 18k, the raw Article 147 item-9 amount is 2,977.93 and Article 153 caps
it at the full 2,024.5 tax after TFA. EUROMOD returns the same tintcri_s and
zero tin_s.

Additional item-10 and invalidity composition regressions are carried by:

    sed -n '498,528p;828,875p' \
      be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.test.yaml

The sickness 9k plus pension 9k case has taxable income 18,000, an item-10
sickness share of 0.5, raw sickness reduction 1,488.965, Article 153
sickness-tax cap 1,012.25, and zero tax after both category reductions. It is
encoded on branch but unencoded_corpus_blocked because item 10 is on page 254.
The invalidity 20k less supplied 500 withholding case nets to 19,500 under
Article 23 paragraph 2; its 2,624.5 tax is fully consumed by the item-9
reduction after the cap. This is an Axiom composition regression, not a claim
that EUROMOD pdi is the same input as the required bhl sickness oracle.

### 5.1 Mixed unemployment+wage residual

The companion expectations and EU JSON above provide the observed endpoints.
This Decimal command reproduces the decomposition:

    python3 - <<'PY'
    from decimal import Decimal as D, getcontext
    getcontext().prec = 50
    ax_extra = D("96.41365477338476374156219864995178399228")
    eu_extra = D("163.9032131147540983606557377049180327869")
    autonomy = D("0.75043")
    ax_credit = D("1028.28906")
    eu_credit = D("1504.8488879999998")
    ax_final = D("1690.2437254013500482160077145")
    eu_final = D("1163.0377081352365")
    reduction_effect = -(eu_extra - ax_extra) * autonomy
    credit_effect = -(eu_credit - ax_credit)
    mechanism_sum = reduction_effect + credit_effect
    observed = eu_final - ax_final
    print("axiom_additional_reduction=", ax_extra, sep="")
    print("euromod_additional_reduction=", eu_extra, sep="")
    print("raw_reduction_gap=", eu_extra - ax_extra, sep="")
    print("tin_effect_after_autonomy=", reduction_effect, sep="")
    print("work_credit_effect=", credit_effect, sep="")
    print("mechanism_sum=", mechanism_sum, sep="")
    print("observed_euromod_minus_axiom=", observed, sep="")
    print("floating_remainder=", observed - mechanism_sum, sep="")
    PY

Output:

    axiom_additional_reduction=96.41365477338476374156219864995178399228
    euromod_additional_reduction=163.9032131147540983606557377049180327869
    raw_reduction_gap=67.48955834136933461909353905496624879462
    tin_effect_after_autonomy=-50.64618926611378977820636451301832208295
    work_credit_effect=-476.559828
    mechanism_sum=-527.2060172661137897782063645130183220830
    observed_euromod_minus_axiom=-527.2060172661135482160077145
    floating_remainder=2.415621986500130183220830E-13

Named mechanism 1 — engine_semantics: EU function 48 correctly prorates the
base U reduction by 15,000/25,500, but function 63 applies the tapered
additional 457.23 amount without the same U share. Axiom applies item 8 to both
amounts. The excess EU reduction lowers tax by 50.6461892661138 after
autonomy.

Named mechanism 2 — engine_semantics, already dispositioned in the work-bonus
suite: EU tintcly_s is 1,504.848888, while the statutory actual reduction
imported by Axiom is capped at 1,028.28906. The difference lowers EU tax by
476.559828.

The two mechanisms sum to the observed residual with only the displayed
floating remainder.

### 5.2 Article 151 branch tests

The linear, zero and exception branches are pinned by:

    sed -n '469,497p;529,588p' \
      be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.test.yaml

At U32 the Article 151 factor is
0.5496503496503496503496503497 and the basic unemployment reduction is
1,219.8225314685314685314685316. At U40 without the exception, the factor and
reduction are zero. With the supplied older-unemployed/seniority exception,
the U40 factor is one and the base reduction remains 2,219.27; Article 151/1's
additional factor is still zero.

### 5.3 Article 154 branch tests

These values are emitted by the same companion-test command; the relevant
cases can be inspected with:

    rg -n \
      'unemployment_24k_article_154|mixed_unemployment_12k_pension_12k' \
      be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.test.yaml
    sed -n '589,628p;770,827p' \
      be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.test.yaml

| Axiom case | Supplied boundary | Complement | Final after autonomy | Meaning |
|---|---:|---:|---:|---|
| U24, §2 | M=24,000 | 786.54841967213114754098360656 | 885.3742958618360655737704918 | 40% of positive tax remaining |
| U24, §3 | M=23,000 | 386.54841967213114754098360656 | 1,185.5462958618360655737704918 | subtract 1,000 benefit excess, then 40% |
| U24, EU-comparable | M=20,000 | 0 | 1,475.6238264363934426229508197 | excess exhausts complement |
| U12 + pension 12, §3/1 | q=90% | 0 | 1,475.6238264363934426229508197 | positive allocation denominator, but 3,933 excess charge exhausts complement |

The mixed §3/1 case exercises the allocation denominators and guarded
division, but does not claim positive allocation: both category allocations
are zero because the complement is zero. EUROMOD functions 54–61 are n/a, so
all positive-complement comparisons remain euromod_non_simulated, not matches.
The suite does not claim a positive S/I allocation case; S/I category
proration/capping is covered separately, and the shared §3/1 formula exposes
the S/I allocation output with a zero expectation in the mixed regression.
At the illustrative M=24,000 branch, EU baseline tin_s minus Axiom is
590.2495305745573770491803279 ≈
786.54841967213114754098360656 × 0.75043. The named mechanism is the switched-
off EU functions 54–61, classified euromod_non_simulated.

The classifications stay separate: M is input_carrying; q=90% is supplied, and
its page-257 legal mechanism is unencoded_corpus_blocked. The 40% §2 rate is
release-proven on page 256, while the §3/§3/1 structures remain blocked as
described in §2.

## 6. Lane-W population wiring notes

This command audits the exact v0.2 transport column and population basis:

    python3 - <<'PY'
    import pandas as pd
    path = (
        "/Users/maxghenis/TheAxiomFoundation/_cape-prep/population-rerun/"
        "out/microcosm_be_v02_2026.h5"
    )
    person = pd.read_hdf(path, "/person")
    unemployment = person["unemployment_compensation_2026"].fillna(0)
    weight = person["person_weight"].fillna(0)
    positive = unemployment > 0
    print("column=unemployment_compensation_2026")
    print("positive_records=", int(positive.sum()), sep="")
    print("weighted_recipients=", float(weight[positive].sum()), sep="")
    print("unweighted_compensation=", float(unemployment.sum()), sep="")
    print(
        "weighted_compensation=",
        float((unemployment * weight).sum()),
        sep=""
    )
    print(
        "replacement_columns=",
        [
            column for column in person.columns
            if any(
                token in column.lower()
                for token in (
                    "unemployment", "sickness", "invalidity", "incapacity"
                )
            )
        ]
    )
    PY

Output:

    column=unemployment_compensation_2026
    positive_records=2986
    weighted_recipients=325331.6458282976
    unweighted_compensation=26584847.338184953
    weighted_compensation=2504425259.097485
    replacement_columns=['unemployment_compensation_2026']

Lane W should map the annual EUR column directly, without monthly conversion or
uprating inside Axiom, to:

    be:statutes/income_tax/individual/pensioner_pit_oracle_pipeline#input.belgium_pit_replacement_annual_gross_unemployment_benefit

Set the absent sickness and invalidity inputs and invalidity withholding to
zero. The transport has no sickness/invalidity/incapacity column, so that
population ledger class is input_absent_in_population; it is not a numeric
match. Set the Article 151 seniority exception false unless an actual
seniority-supplement flag is supplied. Do not infer Article 154 M or q from
the population. If the blocked mixed branch is deliberately evaluated, pass
q=0.90 as explicit pinned-corpus configuration and retain the
unencoded_corpus_blocked label; M still requires an authoritative supplied
value. For strict BE_2025 parity, compare the pre-Article-154 surface or
explicitly label orchestration-side suppression as euromod_non_simulated.

The existing EUROMOD population adapter is confirmed by:

    sed -n '404,420p' \
      /Users/maxghenis/TheAxiomFoundation/_cape-prep/population-rerun/out/microcosm_be_v02_euromod.py

It uses:

    lunmy = recipient * 12
    bun = annual_unemployment / 12 / probed_bun_factor
    bunmy = recipient * 12
    yempv = annual_unemployment / 12 / 0.65 / probed_yempv_factor

The yempv reverse-imputation is carried for the adapter contract, but the
BE_2025 bun simulation policy is off; the tax comparison consumes INPUT bun.
Use bhl for the current sickness-income oracle. The legacy phl variable is not
in the resolved current income lists, and pdi changes disability/TFA semantics,
so neither should replace bhl for the required sickness case.

## 7. Verification gates and flat failure ledger

### 7.1 Gates

Companion tests:

    /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode \
      test --root "$PWD" \
      --axiom-rules-engine-path /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine \
      be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.test.yaml \
      be/statutes/income_tax/individual/replacement_income_complementary_reduction_parameters.test.yaml

Observed:

    RuleSpec companion tests passed: 2 file(s), 24 case(s)

Repository tests:

    pytest -q

Observed:

    .............................                                            [100%]
    29 passed in 15.89s

Sibling-layout validation:

    lane_u_tmp=$(mktemp -d /private/tmp/lane-u-report-validate.XXXXXX)
    mkdir -p "$lane_u_tmp/validate-layout"
    rsync -a --exclude .git "$PWD/" \
      "$lane_u_tmp/validate-layout/rulespec-be/"
    ln -s /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine \
      "$lane_u_tmp/validate-layout/axiom-rules-engine"
    ln -s /Users/maxghenis/TheAxiomFoundation/_cape-prep/corpus-be-pin \
      "$lane_u_tmp/validate-layout/corpus-be-pin"
    cd "$lane_u_tmp/validate-layout/rulespec-be"
    AXIOM_CORPUS_REPO=corpus-be-pin \
      /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode \
      validate \
      be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml \
      --skip-reviewers --json |
      jq '{ci_pass,all_passed,duration_ms}'
    AXIOM_CORPUS_REPO=corpus-be-pin \
      /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode \
      validate \
      be/statutes/income_tax/individual/replacement_income_complementary_reduction_parameters.yaml \
      --skip-reviewers --json |
      jq '{ci_pass,all_passed,duration_ms}'

Observed:

    {
      "ci_pass": true,
      "all_passed": true,
      "duration_ms": 5813
    }
    {
      "ci_pass": true,
      "all_passed": true,
      "duration_ms": 966
    }

Committed-diff check:

    git diff --check 2c84eb9..HEAD

Observed: no output.

### 7.2 Failures, flat

1. Two initial broad repository-search tool calls were rejected by the command
   hook before execution. I narrowed both searches to explicit roots and reran
   them successfully.
2. The first EUROMOD system.run request used the wrong boolean/request variant;
   the connector reported that it expected a bool. The driver now passes the
   documented boolean flags and explicit requested variable lists.
3. A fast-path engine request evaluated an unused imported division and hit a
   division-by-zero error. Explain mode succeeds and is what the population
   adapter uses for this composed oracle; the companion suite covers the
   guarded lane outputs.
4. The first expanded companion run reported missing newly introduced inputs
   in ten inherited Lane-P cases. Every case was updated to assign every input,
   including false booleans.
5. One manual request queried an output under the input namespace. The request
   was corrected to the owning module namespace and rerun.
6. Bare axiom-encode was not on PATH. All recorded runs use the pinned absolute
   executable.
7. A pinned test invocation omitted the engine path and resolved an invalid
   root configuration. It was rerun with
   --axiom-rules-engine-path /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine.
8. The first repository-layout run reported seven newly derived outputs absent
   from the companion coverage inventory. Exact expectations were added.
9. The first full validation found an uncovered zero cap branch for U. A
   zero-income/U-degenerate case was added and validation rerun.
10. The first Article 154 parameter draft cited page 257. That proof was
    removed: 40% is now proven on promoted page 256 and 90% is supplied.
11. A proof atom spanning content on page 255 failed the single-anchor
    validator. The invalid cross-page atom was removed; promoted formulas keep
    valid local proof anchors and source descriptions.
12. The first HDF aggregation requested household_id and raised KeyError
    because the relevant table is /person. The audit was rerun with
    person_weight.
13. The first attempt to add this report had one patch line without its leading
    plus marker; apply_patch rejected the whole patch atomically and no partial
    file was created. This retry is the complete file.
14. The first XML XPath omitted the document namespace and raised IndexError.
    The successful extraction above binds the EUROMOD namespace explicitly.
15. A diagnostic jq selector assumed different compiled-artifact keys and
    printed zero/null values. The compiler's own stdout is the authoritative
    192/true/generic_bulk evidence reported in §3.
16. The first report draft carried a stale expanded base hash and an incorrect
    per-file split of the otherwise correct 918/19 diff totals. A direct
    git rev-parse plus git show --stat audit caught both; the command and
    corrected outputs are now at the top of this report.
17. One compound report-correction patch used a context line with the wrong
    wrap and failed atomically. I reread the exact ranges and applied the same
    classification corrections with narrower contexts.

## 8. Verbatim EUROMOD driver

The following is the exact 282-line driver used for the results in §5.

    #!/usr/bin/env python3
    """Lane U scratch oracle: BE_2025 unemployment and sickness/invalidity PIT."""

    import json
    import math
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
    OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("euromod_replacement_cases.json")


    def header_columns():
        with TEMPLATE.open(encoding="utf-8") as stream:
            header = [
                name.strip()
                for name in stream.readline().rstrip("\n").split("\t")
                if name.strip()
            ]
        # BE_training_data is a legacy template and carries phl, whereas the
        # resolved BE_2025 income lists consume current-variable bhl. EUROMOD's
        # in-memory connector accepts any globally defined input variable.
        if "bhl" not in header:
            header.append("bhl")
        return header


    def blank_frame(rows, header):
        return pd.DataFrame(
            np.zeros((rows, len(header)), dtype=np.float64), columns=header
        )


    def assign(frame, row, values):
        for name, value in values.items():
            if name not in frame.columns:
                raise RuntimeError(f"template missing {name!r}")
            frame.loc[row, name] = float(value)


    def engine_run(system, frame, request_private=False):
        chatter = StringIO()
        kwargs = {}
        if request_private:
            kwargs = {
                "requested_vars": [
                    "tmp_reduc_gen",
                    "tmp_reduc_bun",
                    "tmp_tinna",
                    "tmp_tintcri_extra",
                ],
                "requested_incomelists": [
                    "il_gross_taxableY",
                    "il_taxableY_bf_mq",
                    "il_taxableY",
                    "il_netrepY",
                    "il_netsickY",
                    "il_sickY",
                    "il_netYem",
                ],
            }
        with redirect_stdout(chatter):
            sim = system.run(
                frame,
                DATASET,
                verbose=False,
                nowarnings=True,
                requested_vargroups=[],
                requested_ilgroups=[],
                suppress_other_output=False,
                **kwargs,
            )
        outputs = [item.copy() for item in sim.outputs]
        return (
            outputs,
            [str(error) for error in list(getattr(sim, "errors", []))],
            chatter.getvalue(),
        )


    def base_person(frame, row, idhh, idperson, dag=45, les=5):
        assign(
            frame,
            row,
            {
                "idhh": idhh,
                "idperson": idperson,
                "idpartner": 0,
                "idmother": 0,
                "idfather": 0,
                "dag": dag,
                "dgn": 1,
                "ddi": 0,
                "dms": 1,
                "drgn1": 0,
                "dwt": 1,
                "les": les,
                "lfs": 0,
                "lhw": 0,
                "liwmy": 0,
                "liwwh": 0,
                "loc": 5,
                "lunmy": 0,
                "yemmy": 0,
            },
        )


    def merge_outputs(outputs):
        frames = []
        for index, frame in enumerate(outputs):
            frame = frame.sort_values("idperson").reset_index(drop=True)
            frames.append(frame)
            print(f"output[{index}] shape={frame.shape} columns={list(frame.columns)}")
        merged = frames[0]
        for frame in frames[1:]:
            new_columns = [
                name for name in frame.columns if name == "idperson" or name not in merged
            ]
            merged = merged.merge(frame[new_columns], how="left", on="idperson")
        return merged


    def main():
        if platform.machine() != "x86_64":
            raise RuntimeError(f"needs x86_64, got {platform.machine()}")

        header = header_columns()
        model = Model(str(MODEL_ROOT))
        country = next(country for country in model.countries if country.name == "BE")
        system = next(system for system in country.systems if system.name == SYSTEM)

        probe_specs = [
            ("yem", {"yem": 1000, "yemmy": 12, "lhw": 38, "liwmy": 12}),
            ("bun", {"bun": 1000, "bunmy": 12, "lunmy": 12}),
            ("pdi", {"pdi": 1000, "pdimy": 12, "ddi": 1}),
            ("phl", {"phl": 1000}),
            ("bhl", {"bhl": 1000}),
        ]
        probe = blank_frame(len(probe_specs), header)
        for row, (_, values) in enumerate(probe_specs):
            base_person(probe, row, row + 1, (row + 1) * 100 + 1)
            assign(probe, row, values)
        probe_outputs, probe_errors, probe_chatter = engine_run(system, probe)
        probe_out = probe_outputs[0].sort_values("idperson").reset_index(drop=True)
        factors = {}
        for row, (name, _) in enumerate(probe_specs):
            factor = float(probe_out.loc[row, name]) / 1000.0
            if not math.isfinite(factor) or factor <= 0:
                raise RuntimeError(f"invalid probed {name} uprating factor {factor}")
            factors[name] = factor
        print(f"factors={factors!r} probe_errors={probe_errors}")

        cases = [
            {"label": "unemployment_12k", "bun": 12000.0},
            {"label": "unemployment_18k", "bun": 18000.0},
            {"label": "unemployment_24k", "bun": 24000.0},
            {"label": "unemployment_15k_wage_15k", "bun": 15000.0, "yem": 15000.0},
            {"label": "sickness_bhl_18k", "bhl": 18000.0},
            {"label": "invalidity_pdi_18k", "pdi": 18000.0},
            {"label": "legacy_phl_18k", "phl": 18000.0},
        ]
        frame = blank_frame(len(cases), header)
        for row, case in enumerate(cases):
            is_unemployment = case.get("bun", 0) > 0
            is_disability = case.get("pdi", 0) > 0
            base_person(
                frame,
                row,
                row + 101,
                (row + 101) * 100 + 1,
                les=5 if is_unemployment else 6,
            )
            if is_unemployment:
                assign(
                    frame,
                    row,
                    {
                        "bun": case["bun"] / 12.0 / factors["bun"],
                        "bunmy": 12,
                        "lunmy": 12,
                    },
                )
            if case.get("yem", 0) > 0:
                assign(
                    frame,
                    row,
                    {
                        "yem": case["yem"] / 12.0 / factors["yem"],
                        "yemmy": 12,
                        "lfs": 15,
                        "lhw": 38,
                        "liwmy": 12,
                        "liwwh": 120,
                    },
                )
            for name in ("bhl", "pdi", "phl"):
                if case.get(name, 0) > 0:
                    assign(
                        frame,
                        row,
                        {name: case[name] / 12.0 / factors[name]},
                    )
            if is_disability:
                assign(frame, row, {"ddi": 1, "pdimy": 12})

        outputs, errors, chatter = engine_run(system, frame, request_private=True)
        out = merge_outputs(outputs)

        want = [
            "bun",
            "bun_s",
            "yem",
            "bhl",
            "phl",
            "pdi",
            "tscdb_s",
            "tscee_s",
            "tsceerd_s",
            "tscpe_s",
            "tintace_s",
            "tints_s",
            "tintatb_s",
            "tintatc_s",
            "tintcri_s",
            "tinna_s",
            "tin_s",
            "tinrg_s",
            "tinmu_s",
            "tintcly_s",
            "bsa_s",
            "ils_dispy",
            "ils_tax",
            "ils_taxsim",
            "tmp_reduc_gen",
            "tmp_reduc_bun",
            "tmp_tinna",
            "tmp_tintcri_extra",
            "il_gross_taxableY",
            "il_taxableY_bf_mq",
            "il_taxableY",
            "il_netrepY",
            "il_netsickY",
            "il_sickY",
            "il_netYem",
        ]
        present = [name for name in want if name in out.columns]
        results = {
            "model_root": str(MODEL_ROOT),
            "dataset": DATASET,
            "system": SYSTEM,
            "uprating_factors": factors,
            "probe_errors": probe_errors,
            "probe_chatter": probe_chatter,
            "errors": errors,
            "chatter": chatter,
            "output_frame_count": len(outputs),
            "missing_columns": [name for name in want if name not in out.columns],
            "cases": [],
        }
        for row, case in enumerate(cases):
            item = dict(case)
            for name in present:
                item[f"{name}_annual"] = float(out.loc[row, name]) * 12.0
            results["cases"].append(item)
        OUT.write_text(json.dumps(results, indent=1) + "\n")
        print(json.dumps(results, indent=1))


    if __name__ == "__main__":
        main()

LANE U DONE
