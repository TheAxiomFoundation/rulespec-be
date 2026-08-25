# Lane REFORM-ENC progress

Provenance: RuleSpec-BE branch `ledger/pit-reform-2026-2031`; starting commit `b105e2b3a3086ddd2de447d58a9b951346870dd1`; source image `reform-2026/sources/mb-2026-07-29_1.pdf`, SHA-256 `033bfdecb456d5b901bdf31e3a10b362a89bfdccc925d816d038a6e727d1c9d5`; prepared 2026-08-25.

## State

In progress. The bilingual statutory audit and existing-module map are complete. The Article 131 phase-in and the amended Article 132 one-/two-child branches are encoded and tested. The rules preserve raw bases separately from applied/indexed amounts, calculate the enacted Article 178 coefficient formulas from explicit CPI-average inputs, and use the direct post-Article-178 targets for AY2030/31. No scoring-only static translation is copied into RuleSpec.

## Done

- Confirmed branch `ledger/pit-reform-2026-2031` starts clean at `b105e2b3a3086ddd2de447d58a9b951346870dd1`.
- Read `LEDGER_CAMPAIGN.md`, `LANE_REFORM_PROMPT.md`, and `population-rerun/LANE_REFORM_REPORT.md` read-only.
- Read the scoring artifact and encoding-handoff boundaries read-only.
- Recorded the signed-release proof frontier: encode now against M.B. page/article locators; report corpus-backed validation failures without workaround.
- Verified all proposed numeric law values against the French text and Dutch cross-check.
- Corrected the handoff's systematic one-page citation offset: Articles 2–4 are on M.B. pp. 40196–40197; Articles 5–13 on pp. 40198–40199; Articles 27–34 on pp. 40202–40206; Articles 96–97 on p. 40218; Articles 104–105 on pp. 40219–40220.
- Identified the bilingual Article 28(s) discrepancy and adjudicated the coherent `5,860 -> 5,030` chain from French Article 27, Dutch Article 28(s), and both-language Article 30(B).
- Identified a separate unresolved defect in Article 41 section 4: both languages point to section 1, paragraphs 1 and 4, although the context appears to require section 2. The temporary child-credit floor will not be silently normalized.
- Confirmed no Article 133 or Article 81 module exists; confirmed the employee-SSC work-bonus schedule is not amended; confirmed the separate special-SSC module exists but the enacted brackets contain an unresolved EUR 41,630/EUR 41,360 overlap.
- Encoded Article 131 raw bases for AY2027–2031, the Article 178 general coefficient and rounding, and direct post-Article-178 targets EUR 14,450 (AY2030) and EUR 15,600 (AY2031).
- Encoded Article 132(1°–2°) raw one-/two-child supplements for AY2027–2031 and both branches of the new Article 178 section 2/1 CPI formula without inventing future CPI observations.
- Added eight companion cases (baseline plus one case per AY2027–2031); every case assigns all nine local inputs, including zero/neutral counts and every CPI input. Pinned compile and encoder test pass (8/8).
- Ran repository-layout tests: 28/29 pass. The sole failure is the expected source frontier—18 new monetary parameter atoms have exact M.B. excerpts but cannot yet name canonical corpus paths.
- Preserved Article 4/13 timing clauses verbatim in non-policy `effective_period_evidence`, because the repository's parameter proof gate permits only value-bearing atoms at `versions[N].formula`.
- Recorded a deliberate Article 132 boundary: Article 104(b) covers all first-paragraph supplements, but the pinned sources prove raw bases only for the amended one-/two-child branches. The remaining Article 132 applied branches and Article 133 coefficient application remain unencoded pending source-backed raw bases/module coverage.

## Next

- Encode the Article 87/88 age-gated cap chain and Article 126 linkage.
- Encode canonical Article 147/work-bonus surfaces and remove pilot duplicates.
- Encode the representable Article 134 structural change; record the unrepresentable remainder and Article 41 defect explicitly.
- Finalize the corpus ingestion worklist, run pinned compile/tests/layout/sibling validation, and cross-check every encoded value against the scoring bundle.
