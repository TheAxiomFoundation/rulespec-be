# Lane REFORM-ENC progress

Provenance: RuleSpec-BE branch `ledger/pit-reform-2026-2031`; starting commit `b105e2b3a3086ddd2de447d58a9b951346870dd1`; source image `reform-2026/sources/mb-2026-07-29_1.pdf`, SHA-256 `033bfdecb456d5b901bdf31e3a10b362a89bfdccc925d816d038a6e727d1c9d5`; prepared 2026-08-25.

## State

In progress. The bilingual statutory audit and existing-module map are complete. The encoding will preserve law-fixed raw bases separately from applied/indexed amounts, use explicit supplied index-coefficient dependencies where the law does not fix a nominal amount, and use the two direct post-Article-178 targets for AY2030/31. No scoring-only static translation will be copied into RuleSpec.

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

## Next

- Encode Article 131/132 raw/applied surfaces and per-AY companions.
- Encode the Article 87/88 age-gated cap chain and Article 126 linkage.
- Encode canonical Article 147/work-bonus surfaces and remove pilot duplicates.
- Encode the representable Article 134 structural change; record the unrepresentable remainder and Article 41 defect explicitly.
- Finalize the corpus ingestion worklist, run pinned compile/tests/layout/sibling validation, and cross-check every encoded value against the scoring bundle.
