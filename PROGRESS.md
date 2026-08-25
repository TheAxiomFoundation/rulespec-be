# Lane REFORM-ENC progress

Provenance: RuleSpec-BE branch `ledger/pit-reform-2026-2031`; starting commit `b105e2b3a3086ddd2de447d58a9b951346870dd1`; source image `reform-2026/sources/mb-2026-07-29_1.pdf`, SHA-256 `033bfdecb456d5b901bdf31e3a10b362a89bfdccc925d816d038a6e727d1c9d5`; prepared 2026-08-25.

## State

In progress. The bilingual statutory audit and existing-module map are complete. The Article 131 phase-in, amended Article 132 one-/two-child branches, Article 126 threshold/scholarship amendment, Article 87/88 quotient transition, and representable Article 134 changes are encoded and tested. The rules preserve raw bases separately from applied/indexed amounts, calculate the enacted Article 178 coefficient formulas from explicit CPI-average inputs, and use direct post-Article-178 targets where the law supplies them. No scoring-only static translation is copied into RuleSpec.

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
- Encoded the Article 126 item 4 threshold as the applied Article 131 amount from AY2027 and added the qualifying untaxed scholarship/social-security-rights branch with a strict `>` comparison.
- Encoded the Article 87/88 ordinary and both-spouses-age statutory cap chains, the age threshold change from 66 to 67, the special Article 178 fixed coefficient, and nearest-EUR-10 applied cap for AY2027 onward. The full both-old phase-out through AY2045 and the replacement Article 87 age gate from AY2046 are retained rather than truncated at the scoring horizon.
- Preserved the French Article 28(s) `5.680` defect verbatim and used the coherent EUR 5,860 predecessor proved by French Article 27, Dutch Article 28(s), and French Article 30(B)(1°).
- Added 20 core-horizon reform companions (four each for AY2027–AY2031): ordinary one-earner, both-spouses-age, no-tax-increase guard, and scholarship-threshold cases. Added a companion for every AY2032–AY2045 both-old cap step, two AY2046 replacement-Article-87 cases, both scholarship boundary directions, and a non-unity CPI case that detects ratio inversion plus average/coefficient/cap rounding. Every assessment-year case explicitly assigns all 40 reachable local/imported inputs. Pinned encoder testing passes all 52 module cases.
- Pinned engine compilation of the joint module closure passes with 37 derived outputs and `generic_bulk` fast-path compatibility.
- Re-ran repository-layout tests: 28/29 pass. The sole failure contains exactly 41 missing canonical corpus paths: 23 joint-assessment M.B. monetary atoms plus the previously recorded 18 tax-free-amount atoms. No additional repository-contract failure is present.
- Recorded every Article 34 assessment-year transition through AY2046 and the replacement Article 87 mechanisms as exact evidence. The AY2046 formula versions now carry verbatim paragraph 1–4 proof atoms. Timing clauses are not mislabeled as value-bearing parameter proof atoms.
- Encoded the Article 134 scholarship exclusion from AY2027, including the taxpayer branch and the spouse-plus-separate-assessment branch, with an explicit AY2026 pre-effective regression.
- Replaced Article 134's separate five-band tax-free-amount scale with imported Article 130 brackets and rates from AY2030. The AY2030 and AY2031 cases use the enacted Article 131 post-indexation amounts EUR 14,450 and EUR 15,600, so the companions do not present 2025 bracket snapshots as future indexed observations.
- Corrected the Article 134 module's baseline review anchor from CIR page 181 to the operative Article 134 text on page 185; the untouched HEAD module's sibling validation had otherwise stopped at an existing ungrounded EUR 11,460 diagnostic.
- Narrowed Article 10(k)-(l) after independent audit: the law removes the per-spouse wording and replaces the proportional-allocation paragraph, so the obsolete spouse-allocation outputs return zero from AY2030 and a new household output applies the single EUR 1,140 cap to the supplied aggregate uncapped credit. The AY2030/31 tests cross that cap boundary.
- Recorded Article 10(l)'s transferred-tax-free-amount composition priority as an upstream component-attribution obligation. Aggregate inputs cannot prove which portion arose from Article 131, Article 132(7°-8°), or child supplements, so no allocation formula was invented.
- Added six complete reform companions covering AY2026 through AY2031; each assigns all 18 local inputs plus the imported taxable-income input. Pinned encoder testing passes all 18 module cases, and pinned compilation passes with 25 derived outputs and `generic_bulk` compatibility.
- Ran sibling-layout validation for Article 134. It reaches the expected signed-release frontier and reports `ci_pass: false` solely because the new Moniteur proof source lacks an authorized canonical `corpus_citation_path`; no waiver, pseudo-path, corpus edit, or toolchain change was made.
- Re-ran repository-layout tests against the stable combined worktree: 28/29 pass. The sole failure lists 58 pending Moniteur parameter atoms (23 joint-assessment, 18 tax-free-amount, and 17 Article 147/work-bonus); this Article 134 structural slice adds no unrelated repository-contract failure.

## Next

- Encode canonical Article 147/work-bonus surfaces and remove pilot duplicates.
- Propagate the reform boundaries through the couple oracle pipeline without duplicating canonical parameters.
- Finalize the corpus ingestion worklist, run pinned compile/tests/layout/sibling validation, and cross-check every encoded value against the scoring bundle.
