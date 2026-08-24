# LANE XP — Belgian computable-core experiment

## State

Lane XP is in progress on `experiment/computable-core-penal-contract`, based on
`origin/main` commit `b105e2b`. This lane is Axiom-only. It uses no EUROMOD code,
data, commands, or comparison results.

The experiment encodes two non-tax-benefit statutory computations:

1. the Belgian additional-decimes multiplier for penal fines, including the
   1 February 2026 amendment boundary and the Article 2 exclusions; and
2. the civil/commercial legal-interest formula and the Article 2 §2 fiscal 7%
   default, including explicit derogation scope.

## Binding campaign constraints

`../LEDGER_CAMPAIGN.md` was read before repository work. The lane uses the pinned
encoder and engine, assigns every local companion-test input (including every
false boolean), validates through the required sibling layout, changes neither
`.axiom/toolchain.toml` nor workflows/waivers/known-gap/oracle-pending files,
commits locally after coherent steps, does not push, and performs no stash
operation.

## Saved-source register

All hashes are SHA-256 over the exact saved bytes. The HTML statute files are
ISO-8859-1; quotations below are decoded to UTF-8 without altering their text.

| Saved file | SHA-256 | Use |
|---|---|---|
| `decimes_1952.html` | `2804d91abd1b35ac4c1be59f6b04a883fe4f0b5bde83e1e7cf955d118e663b65` | Consolidated 1952 law, current text, version notes, exclusions, repeal/procedure inventory |
| `amending_law_2025009854.html` | `bfc100bc23b93a4b8620c57a7e06eec2c52fb0cc659c882be9a7c4b754380a8f` | Authentic 2025 amendment text, publication evidence, entry-into-force formula |
| `interet_1865.html` | `487dbdf2619e4b2478987178895e2c257fe4a61c7480898d450ed094b3955a0b` | Additional saved consolidated view, cross-check only |
| `interet_1865_texte.html` | `6c4516e695f23f89f03e3740e8b7c1a6126f4662ed567268b95fbfebc760c01b` | Consolidated Article 2 text and version notes used for encoding |
| `euribor_1y_monthly.csv` | `ede1ff74f9d96b80f23352bed4391309ae8ec202e5381baca1e3e7d49ac1a3e1` | ECB-series observations used only as companion/oracle inputs |
| `taux_2026_mediation.html` | `67bbd508234cb8376d527bad9bafba1af03fee5bda6c7ab13cb4005777ecc0cd` | Cross-source documentary oracle for published 2025/2026 rates |

Hash command:

```sh
shasum -a 256 ../experiment-penal-contract/sources/*
```

## Penal law: 5 March 1952, numac 1952030505

### Source locators and operative text

The consolidated Justel locator embedded at `decimes_1952.html:279` is
`https://www.ejustice.just.fgov.be/eli/loi/1952/03/05/1952030505/justel`.
The amending-law Justel locator embedded at
`amending_law_2025009854.html:184` is
`https://www.ejustice.just.fgov.be/eli/loi/2025/12/19/2025009854/justel`; its
Moniteur ELI at line 173 is
`https://www.ejustice.just.fgov.be/eli/loi/2025/12/19/2025009854/moniteur`.

Article 1 (`decimes_1952.html:192`) says:

> Le montant des amendes pénales prononcées par les cours et tribunaux en vertu du Code pénal et des lois et règlements particuliers, même postérieurs à la présente loi, est majoré de (nonante décimes), sans que cette majoration modifie le caractère juridique de ces peines.

The 2025 amendment supplies the immediately prior word and the replacement
(`amending_law_2025009854.html:166`):

> Art. 2. Dans l'article 1er, alinéas 1er et 2, de la loi du 5 mars 1952 relative aux décimes additionnels sur les amendes pénales, modifiés en dernier lieu par la loi du 25 décembre 2016, le mot "septante" est chaque fois remplacé par le mot "nonante".

The consolidated version notes on `decimes_1952.html:192` state:

> (1)\<L 2016-12-25/01, art. 59, 010; En vigueur : 01-01-2017\>

> (2)\<L 2025-12-19/18, art. 2, 011; En vigueur : 01-02-2026\>

The saved-source-only windows are therefore `septante` = 70 additional decimes
from 1 January 2017 through 31 January 2026, and `nonante` = 90 from 1 February
2026. A fine increased by N decimes is multiplied by `(10 + N) / 10`, giving
`(10 + 70) / 10 = 8` before the boundary and `(10 + 90) / 10 = 10` on and
after it. The version note supplies the prior start date; the amending law's
Article 2 supplies the prior word. Neither is silently filled from outside
knowledge.

### Entry into force

The saved Moniteur page and consolidation identify publication on 30 December
2025 (`amending_law_2025009854.html:126,179` and
`decimes_1952.html:214-216`). Article 6 says
(`amending_law_2025009854.html:166`):

> Art. 6. La présente loi entre en vigueur le premier jour du mois qui suit l'expiration d'un délai de dix jours prenant cours le jour après sa publication au Moniteur belge.

Derivation: publication is 30 December; the period starts the next day,
31 December 2025 (day 1); day 10 is 9 January 2026; the ten-day period expires
in January; the first day of the following month is **1 February 2026**. This
independently agrees with consolidated footnote (2). The module effective-date
field will state `2026-02-01` explicitly.

### Scope and non-computable text

Article 2 (`decimes_1952.html:192`) provides two computable exclusions:

> La majoration prévue à l'article 1er n'est applicable ni aux amendes prononcées en vertu de la loi du 29 août 1919 concernant les débits de boissons fermentées, modifiée par l'arrêté-loi du 14 novembre 1939 relatif à la répression du débit illicite de boissons fermentées, ni dans les cas où cette majoration est exclue par une loi particulière.

Both exclusions will be explicit boolean inputs. An excluded fine retains a
multiplier of 1 and its unmultiplied amount; it does not become a zero fine.

The second paragraph of Article 1 requires the judgment to record the increased
amount. The third paragraph requires joint recovery with the principal. Those
are procedural consequences, not separate numeric rules. Article 1bis is
`[abrogé]`, with the note
`<L 2010-06-06/06, art. 109, 13°, 008; En vigueur : 01-07-2011>`, so it creates
no current output. Article 3 repeals predecessor enactments and creates no
current per-case computation. Amendment Articles 3–5 contain potentially
computable Social Penal Code minimum-fine rules, but their Article 101 maximums
and operative parent provisions are not among the saved sources; they are
cross-provision-dependent and outside this decimes module, not mislabeled as
procedure.

The consolidation's amendment list also mentions a law of 16 March 2026,
published 1 April 2026, affecting Article 1, while the saved displayed text is
labeled updated through 30 December 2025. The requested January/February cases
are unaffected, but this capture does not prove an open-ended post-April-2026
consolidation. The encoded experiment is accordingly bounded to the evidenced
case horizon rather than presented as perpetual legal completeness.

### Penal oracle grid

These saved-law values are engine-exercised by the pinned companion. Every row
cites Article 1 of the 1952 law, as amended by Article 2 of the 2025 law; the
Article 1 scope input is true and both exclusion inputs are explicitly false.

| Judgment date | Statutory fine | Additional decimes | Multiplier | Fine after decimes | Provision |
|---|---:|---:|---:|---:|---|
| 2026-01-15 | €26 | 70 | ×8 | €208 | 1952 Art. 1 + pre-amendment version note |
| 2026-01-15 | €50 | 70 | ×8 | €400 | 1952 Art. 1 + pre-amendment version note |
| 2026-01-15 | €200 | 70 | ×8 | €1,600 | 1952 Art. 1 + pre-amendment version note |
| 2026-01-15 | €500 | 70 | ×8 | €4,000 | 1952 Art. 1 + pre-amendment version note |
| 2026-02-15 | €26 | 90 | ×10 | €260 | 1952 Art. 1 + 2025 Art. 2 |
| 2026-02-15 | €50 | 90 | ×10 | €500 | 1952 Art. 1 + 2025 Art. 2 |
| 2026-02-15 | €200 | 90 | ×10 | €2,000 | 1952 Art. 1 + 2025 Art. 2 |
| 2026-02-15 | €500 | 90 | ×10 | €5,000 | 1952 Art. 1 + 2025 Art. 2 |

The pre/post-February pair is the fresh amendment caught by the encoded
effective windows.

## Civil/contract law: 5 May 1865 Article 2, numac 1865050550

### Source locator, formula, and scope

The embedded consolidated Justel locator at `interet_1865_texte.html:243` is
`https://www.ejustice.just.fgov.be/eli/loi/1865/05/05/1865050550/justel`.
Article 2 is marked
`<L 2006-12-27/30, art. 87, 002; En vigueur : 01-01-2007>` at line 192.

Article 2 §1 states (`interet_1865_texte.html:192`):

> § 1er. Chaque année calendrier, le taux de l'intérêt légal en matière civile et en matière commerciale est fixé comme suit : la moyenne du taux d'intérêt EURIBOR à 1 an pendant le mois de décembre de l'année précédente est arrondie vers le haut au quart de pourcent; le taux d'intérêt ainsi obtenu est augmenté de 2 pour cent.

Thus the formula in percentage points is `ceil(EURIBOR / 0.25) * 0.25 + 2`.
The preceding-December EURIBOR average remains a test/oracle input; it is never
a statute-module literal.

The statutory publication sentence is:

> L'administration générale de la Trésorerie du Service public fédéral Finances publie, dans le courant du mois de janvier, le taux de l'intérêt légal applicable pendant l'année calendrier en cours, au Moniteur belge.

Article 2 §2 states:

> § 2. Le taux d'intérêt légal en matière fiscale est fixé à 7 pour cent, même si les dispositions fiscales renvoient au taux d'intérêt légal en matière civile et pour autant qu'il n'y soit pas explicitement dérogé dans les dispositions fiscales.

The next sentence is a necessary authority boundary:

> Ce taux peut être modifié par arrêté royal délibéré en Conseil des ministres.

The current Article 2 provision will conservatively begin on `2007-01-01`.
Although its history notes 7% from 1 September 1996 (`<AR 4 août 1996, MB 15
août 1996>`), extending the current statutory formulation backward would rely
on that separate decree.

From 1 January 2023, §2/1 begins “Par dérogation au paragraphe 2” for specified
SPF-Finances-collected or refunded fiscal and non-fiscal claims, subject to its
regional-tax exception. Because its J-index data and referenced implementing
order are not supplied, this experiment encodes an explicit `§2 applies`
predicate and the 7% default, not an invented §2/1 rate. Any other explicit
fiscal derogation also turns that predicate off.

### EURIBOR and published-rate oracle

The data input is ECB series
`FM.M.U2.EUR.RT.MM.EURIBOR1YD_.HSTA`, titled “Euribor 1-year - Historical close,
average of observations through period,” unit `PCPA`. The exact relevant CSV
observations are 2.43605 for `2024-12` and 2.2671429 for `2025-12`.

The saved mediation page (`taux_2026_mediation.html:479-484`) says:

> Le taux d’intérêt légal pour 2026 a été publié :

> Le taux d’intérêt légal applicable pour les transactions entre particuliers ou entre particuliers et commerçants est fixé à 4,5 % pour l’année 2026. Il s’agit du même taux qu’en 2025.

The separate 10.5% late-commercial-payment bullet is a different legal rate and
is not used as this Article 2 oracle.

| Rate year | Prior December input | Upward-quarter result | Statutory addition | Computed rate | Published rate | Residual |
|---|---:|---:|---:|---:|---:|---:|
| 2025 | 2.43605% = 243.605 bp | 2.50% = 250 bp (+6.395 bp) | +2.00 pp = 200 bp | 4.50% = 450 bp | 4.50% = 450 bp | 0 bp |
| 2026 | 2.2671429% = 226.71429 bp | 2.50% = 250 bp (+23.28571 bp) | +2.00 pp = 200 bp | 4.50% = 450 bp | 4.50% = 450 bp | 0 bp |

The saved mediation HTML contains no specific 2025/2026 Moniteur issue, notice
number, notice date, or direct Moniteur link. It links only to an SPF Finances
rate page. Accordingly, the saved evidence supports the published values and
the statute supports the general Moniteur publication duty, but the prompt's
claimed saved specific Moniteur reference is not present. No missing notice
reference is invented.

## Corpus-ingestion worklist

The pinned corpus does not yet hold either governing document. Following the
dependants-lane “encode now, promote later” precedent, the modules will identify
the Justel numac locators and exact saved-byte hashes now, while certification-
frontier validation remains blocked until ingestion, legal-source slicing, and
promotion:

| Work item | Numac | Locator | Saved evidence |
|---|---:|---|---|
| Ingest and promote the 1952 consolidated law plus its 2025 amendment source | 1952030505 / 2025009854 | 1952 and 2025 ELI links above | `decimes_1952.html` + `amending_law_2025009854.html` hashes above |
| Ingest and promote the 1865 Article 2 consolidation | 1865050550 | 1865 ELI link above | `interet_1865_texte.html` hash above |

## Verification commands and results

Commands executed so far:

```sh
sed -n '1,260p' ../LEDGER_CAMPAIGN.md
sed -n '1,280p' CLAUDE.md
git status --short --branch
shasum -a 256 ../experiment-penal-contract/sources/*
file ../experiment-penal-contract/sources/*.html ../experiment-penal-contract/sources/*.csv
```

Penal compile:

```sh
AXIOM_RULESPEC_REPO_ROOTS="$PWD" /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine/target/release/axiom-rules-engine compile --program "$PWD/be/statutes/penal/additional_decimes.yaml" --output /private/tmp/lane-xp-penal.compiled.json
```

Result: exit 0; artifact format 1; engine `0.1.0`; four derived outputs;
evaluation order `decimes_apply` → `multiplier` → `amount_after` →
`additional_amount`; `fast_path_compatible: true`.

Penal companion:

```sh
AXIOM_RULESPEC_REPO_ROOTS="$PWD" /Users/maxghenis/TheAxiomFoundation/axiom-encode-pinned/.venv/bin/axiom-encode test --root "$PWD" --axiom-rules-engine-path /Users/maxghenis/TheAxiomFoundation/_cape-prep-engine be/statutes/penal/additional_decimes.test.yaml --json
```

Result: exit 0 and `success: true`; one test file, 11 cases, one compiled
program, zero failures. All four local inputs are assigned in every case,
including explicit `false` values. The eight requested grid rows, both Article
2 exclusions, and a false Article 1 scope case all pass.

Civil compile/companion and sibling-layout validation commands and exact results
remain pending.

## Commits

| Commit | Coherent step |
|---|---|
| `5f97c22` | Start and commit the required `PROGRESS.md` ledger |

## What this proves / what it does not

If the pending pinned-engine runs succeed, this exhibit will prove that the
Axiom pipeline can compile and exercise dated statutory computations outside
tax-benefit law, including amendment selection, legal-scope carve-outs,
rounding, and a cross-source oracle that owes nothing to EUROMOD. It will be an
executable, exercised artifact on the certification ladder; it will **not** be
certified law. Corpus ingestion/promotion and legal review remain pending. The
scoping document's pilot recipe remains one quarter, one reviewer, and one
oracle; this experiment does not enlarge that recipe or claim national legal
coverage.

## Next

- Finish RuleSpec-shape investigation against the pinned engine and repository
  contracts.
- Implement the two atomic modules and exhaustive companion cases.
- Compile and execute with the pinned engine, then run sibling-layout validate
  and classify the corpus/release frontier exactly.

LANE XP IN PROGRESS
