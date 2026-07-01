# rulespec-be Agent Notes

This repo stores Belgium and Brussels-Capital Region RuleSpec source registry materials, oracle references, and encoded policy rules.

## Scope

- `be/`: federal Belgium statutes, royal decrees, regulations, and federal administrative policy needed for tax-benefit modeling.
- `be-bru/`: Brussels-Capital Region, Common Community Commission, and Brussels-specific policy instruments.
- `data/corpus/`: source inventory, ingestion notes, provision locators, and future promoted official-source extracts.
- `data/coverage/`: tax-benefit coverage backlog and source map.
- `data/oracles/`: executable or documentary comparison references. These are never legal authority.

## Do

- Treat the scope as a Belgium tax-benefit surface backed by federal Belgium upstream law, with Brussels-Capital Region as the first regional layer where family benefits, housing, or local social-assistance rules require regional law.
- Start from the furthest upstream available source: Moniteur belge/Belgisch Staatsblad original publication and ELI identifiers first, consolidated Justel only as a locator, then agency guidance or calculators.
- Add RuleSpec under `be/statutes/`, `be/regulations/`, `be/policies/`, `be-bru/statutes/`, `be-bru/regulations/`, or `be-bru/policies/` with companion `.test.yaml` files.
- Keep source law provenance in corpus artifacts and cite those corpus paths from RuleSpec modules.
- Keep exact oracle versions in `data/oracles/oracle-index.json` when executable comparison surfaces are pinned.
- Sync `axiom-encode` and `.axiom/toolchain.toml` before substantial encoding runs.

## Do Not

- Use Famiris, SPF Finance, ONEM/RVA, mutuality, CPAS, or calculator pages as the first legal source when a statute, ordinance, royal decree, or ministerial order governs the rule.
- Treat Justel consolidation as authentic legal text; use it to navigate to official Moniteur publications and version history.
- Migrate OpenFisca, EUROMOD, BELMOD, or agency calculator code mechanically as RuleSpec.
- Add generated source payload dumps, formula artifacts, `parameters.yaml`, or standalone YAML fixtures outside allowed RuleSpec roots.
- Hand-copy statute text into RuleSpec without a corpus `citation_path`.
