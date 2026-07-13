# rulespec-be Agent Notes

This repo stores Belgium RuleSpec source registry materials, oracle references,
encoded atomic policy rules, and declarative Axiom program composition specs.

## Scope

- `be/`, `be-bru/`, `be-dg/`, `be-vlg/`, and `be-wal/`: federal, regional,
  community, and Brussels-specific policy instruments.
- `<jurisdiction>/{legislation,policies,regulations,statutes}/`: the only atomic
  RuleSpec roots.
- `<jurisdiction>/programs/`: declarative axiom-compose specs only; never
  atomic `rulespec/v1` modules.
- `data/corpus/`: source inventory, ingestion notes, provision locators, and future promoted official-source extracts.
- `data/coverage/`: tax-benefit coverage backlog and source map.
- `data/oracles/`: executable or documentary comparison references. These are never legal authority.

## Do

- Treat the scope as a Belgium tax-benefit surface backed by federal Belgium upstream law, with Brussels-Capital Region as the first regional layer where family benefits, housing, or local social-assistance rules require regional law.
- Start from the furthest upstream available source: Moniteur belge/Belgisch Staatsblad original publication and ELI identifiers first, consolidated Justel only as a locator, then agency guidance or calculators.
- Add atomic RuleSpec under the canonical jurisdiction roots with companion
  `.test.yaml` files. Use exact `.yaml`; do not add aliases or symlinks.
- Give every atomic module exactly one
  `module.source_verification.corpus_citation_path`. Attach every other
  independently operative source directly to the supported rule as an exact
  corpus-backed proof atom.
- Keep exact oracle versions in `data/oracles/oracle-index.json` when executable comparison surfaces are pinned.
- Sync `axiom-encode` and `.axiom/toolchain.toml` before substantial encoding runs.

## Do Not

- Use Famiris, SPF Finance, ONEM/RVA, mutuality, CPAS, or calculator pages as the first legal source when a statute, ordinance, royal decree, or ministerial order governs the rule.
- Treat Justel consolidation as authentic legal text; use it to navigate to official Moniteur publications and version history.
- Migrate OpenFisca, EUROMOD, BELMOD, or agency calculator code mechanically as RuleSpec.
- Add generated source payload dumps, formula artifacts, `parameters.yaml`, or standalone YAML fixtures outside allowed RuleSpec roots.
- Hand-copy statute text into RuleSpec without a corpus `citation_path`.
- Reintroduce plural source paths, `module.source_claims`, proof `claim` refs,
  legacy v1 encoding manifests, root-level content trees, or compatibility
  symlinks.
