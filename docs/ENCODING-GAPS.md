# Encoding gaps

These findings record the modules that still fail path-anchored numeric
grounding after source-faithful citation and excerpt fixes. They do not change
encoded values or expected outputs.

## `be/policies/euromod_benefit_income_list.yaml`

- Failure: the Wallonia social-supplement selector uses the local enum value
  `4`.
- Finding: the pinned corpus contains the regional benefit rules but no
  EUROMOD `ils_ben` crosswalk assigning code `4`.
- Judgment: missing source for an internal interface tag, not evidence that a
  policy amount or household output is wrong.

## `be/regulations/career_break/parental_leave/allowance_amounts.yaml`

- Failure: the one-tenth leave-form denominator `10` is not recognized.
- Finding: the governing text states the exact supported phrase `d'un
  dixième`; the numeric parser sees the separate forty-month duration but does
  not interpret the French fractional ordinal as `10`.
- Judgment: source-present parser limitation; the encoded denominator is not
  judged wrong.

## `be/regulations/health_insurance/incapacity/indemnity_rates.yaml`

- Failure: the Article 226 invalidity rate `0.55` is not recognized.
- Finding: Article 213 contains the correct `55` rate, but Justel amendment
  markers split it from the shared `p.c.` unit. The parser therefore extracts
  the neighboring 40 percent rate but not 55 percent.
- Judgment: source-present parser limitation; the encoded rate is not judged
  wrong.

## `be/regulations/unemployment/benefit_amount.yaml`

- Failure: the AX wage-cap selector uses the local enum value `5`.
- Finding: Article 111 identifies AX as item `4°`; its item `5°` concerns a
  deleted different cap. The module's `5` is an internal routing code, not a
  source-stated legal number.
- Judgment: missing source for an internal interface tag. The sourced AX cap
  amount and resulting benefit are not judged wrong.

## `be/regulations/vat/rates.yaml`

- Failures: local consumption-category tags `4`, `5`, and `6`, plus raw rate
  selector values `6` and `12`.
- Finding: the pinned tables name the relevant medicine, restaurant, and
  periodical categories but do not assign those local category numbers.
  Article 1 states `6 p.c.` and `12 p.c.`; the parser correctly normalizes
  those percentages to `0.06` and `0.12`, so they cannot ground the module's
  separate raw selector codes.
- Judgment: missing source for internal enum tags and a parser/modeling
  mismatch for raw rate codes. The sourced VAT rates and mappings are not
  judged wrong.

## `be/statutes/family_benefits/birth_allowance.yaml`

- Failure: German-speaking Community routing uses the local region tag `4`.
- Finding: the pinned regional law supports the allowance but does not assign
  jurisdiction code `4`.
- Judgment: missing source for an internal routing enum, not evidence that the
  allowance output is wrong.

## `be/statutes/family_benefits/child_benefit_base_2025.yaml`

- Failures: German-speaking Community tag `4`, Flemish age boundary `4`, and
  the derived transition age `7`.
- Finding: no provision assigns the local region tag. Article 19 states the
  age boundary as Dutch `vier`, which the pinned parser misses. The age-seven
  transition is derived for 2025 from the source's pre-1-January-2019 birth
  cutoff rather than stated directly as `7`.
- Judgment: one missing-source internal enum, one parser limitation, and one
  derived-value grounding limitation. The tested benefit outputs are not
  judged wrong.

## `be/statutes/family_benefits/lgaf_amounts.yaml`

- Failure: the Article 42bis supplement `17.41` is not recognized.
- Finding: the exact supporting text says `17, 41 EUR`; the comma-space makes
  the parser read separate `17` and `41` values. Article 41's normalized
  `17,41` occurrence governs a different condition and cannot be substituted.
- Judgment: source-present parser limitation; the encoded supplement is not
  judged wrong.

## `be/statutes/income_tax/individual/pilot_worker_oracle_pipeline.yaml`

- Failure: the internal trailing-group helper value `46` is not recognized.
- Finding: the cited threshold is stated as `11.460 euros`; the source parser
  correctly reads `11460`, not the helper's internal decomposition fragment
  `46`. Slicing those digits alone would misrepresent the evidence.
- Judgment: parser/modeling mismatch in an internal reconstruction helper. The
  sourced EUR 11,460 threshold and downstream result are not judged wrong.

## `be/statutes/property_tax/immovable_withholding.yaml`

- Failure: the Article 258 professional-use threshold `0.25` is not
  recognized.
- Finding: the exact passage says `dépasse le quart du revenu cadastral`; the
  parser does not interpret `le quart` as `0.25`. A later `d'un quart` on the
  same page concerns a different reduction and cannot ground this rule.
- Judgment: source-present parser limitation; the encoded quarter threshold is
  not judged wrong.

## `be/statutes/social_integration/payable_amount.yaml`

- Failure: the euro-cent rounding denominator `100` is not grounded.
- Finding: the relevant pinned statute and implementing decree do not mandate
  this implementation rounding denominator; decimal historical amounts do not
  prove the algorithm.
- Judgment: missing source for an implementation constant, not evidence that
  the statutory entitlement amounts are wrong.

## `be-bru/regulations/housing/social_housing_rental.yaml`

- Failure: the income-coefficient rounding denominator `100` is not grounded.
- Provisions searched: the module's Article 2 source and the formula's Article
  58 proof. Article 58 requires rounding the coefficient to two decimal places
  but does not state an arithmetic denominator of `100`.
- Judgment: missing source for an implementation constant, not evidence that
  the rent coefficient or resulting rent is wrong.

## `be-bru/statutes/disability/elderly_care_allowance.yaml`

- Failures: transfer lookback `10`, household split factor `0.5`, and annual
  payment divisor `12`.
- Provisions searched: implementing-order Articles 5, 17, and 43. They state
  the values verbatim as `la moitié`, `dix années`, and `par douzièmes`; no
  distinct numeric rendering of those policy values appears in the promoted
  provisions.
- Judgment: source-present French-number-word limitations, not evidence that
  the encoded values or allowance outputs are wrong.

## `be-vlg/regulations/social_security/flemish_social_protection/premium.yaml`

- Failures: premium start age `26` and the Article 68 selector year `2025`.
- Provisions searched: Social Protection Decree Articles 45 and 46 and the
  2025 and current implementing-order Article 68 blocks. The promoted decree
  delegates the start age without stating `26`; the Article 68 validity date
  contains 2025 only as date metadata, which numeric grounding intentionally
  excludes.
- Judgment: missing source for the delegated age and a temporal-selector
  grounding limitation. The sourced premium amounts are not judged wrong.

## `be-vlg/statutes/family_benefits/amounts.yaml`

- Failures: internal disability-tier codes `6` and `7`, and universal
  participation age limits `11` and `17`.
- Provisions searched: Decree Articles 16 and 19 through 22, plus the promoted
  Groeipakket amount schedules. Article 16 lists seven amount bands but does
  not assign the module's internal selector codes. Articles 20 and 21 state
  the ages as Dutch `elf` and `zeventien`; the schedules describe operational
  age bands but do not provide a faithful numeric replacement for both exact
  statutory limit clauses.
- Judgment: missing source for internal enum tags and source-present Dutch
  number-word limitations. The benefit amounts and selections are not judged
  wrong.

## `be-wal/statutes/family_benefits/amounts.yaml`

- Failures: one-parent orphan supplement rate `0.5` and annual age-supplement
  limits `11` and `17`.
- Provisions searched: Decree Articles 15 and 17 and the promoted AVIQ amount
  scales. The decree states `cinquante pour cent`, `onze ans`, and `dix-sept
  ans`; the operational scales do not replace those exact statutory clauses.
- Judgment: source-present French-number-word limitations, not evidence that
  the encoded rates, age bands, or outputs are wrong.

## `be-wal/statutes/family_benefits/eligibility.yaml`

- Failures: eligibility age limits `18`, `21`, and `25`.
- Provisions searched: Decree Articles 5 and 6 and the promoted AVIQ amount
  scales. Article 5 states the limits as French `dix-huit`, `vingt et un`, and
  `vingt-cinq`; the amount scales cover only particular benefit bands and
  cannot substitute for the governing eligibility clauses.
- Judgment: source-present French-number-word limitations, not evidence that
  the eligibility windows or expected results are wrong.

## `be-wal/statutes/vehicle_tax/entry_into_service.yaml`

- Failure: the large-family reduction mass floor `1838` is not recognized.
- Provisions searched: the 2023 TMC decree, the 30 May 2025 adapting decree,
  and the current SPW passenger-car guidance. The adapting decree states the
  exact floor as `1 838 kilogrammes`; the pinned parser splits that
  space-grouped integer. The separate mass-coefficient denominator is now
  grounded by the guidance's verbatim `Y = 1838`, but that different use
  cannot be substituted for the reduction floor.
- Judgment: source-present grouped-integer parser limitation, not evidence
  that the mass floor or tax result is wrong.
