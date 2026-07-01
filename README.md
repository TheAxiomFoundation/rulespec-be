# rulespec-be

Belgium RuleSpec source registry.

This repository targets a Belgium tax-benefit surface comparable in ambition to `rulespec-nz`: federal/national policy plus the Flanders, Wallonia, Brussels, and community-layer programs needed for household-level calculations. The surface includes income tax, social contributions, family benefits, minimum income, unemployment, sickness/disability, pensions, housing support, indirect tax, student support, regional property and transfer taxes, vehicle taxes, care insurance, and cross-cutting residency predicates.

Brussels-Capital Region is the first encoded regional slice because family benefits, housing, and local social-assistance interfaces require regional law. It is not the final regional scope: full Belgium coverage means the same source-first treatment for Flanders, Wallonia, and community competences.

## Source Priority

Policy must come from the furthest upstream available source.

1. Moniteur belge / Belgisch Staatsblad original publications and ELI identifiers, including the official publication image/PDF when legal value matters.
2. Justel consolidated legislation as a non-authentic locator for current text, amendment history, and ELI navigation.
3. Agency rate tables, manuals, calculators, and guidance only after the governing statute, ordinance, decree, royal decree, order, or regulation is identified.
4. Oracles only for household-level parity tests against an external source that can calculate the same household case, never as law.

## Oracle Scope

An oracle is an executable, pinned external calculator that accepts household-level inputs and returns household-level tax-benefit outputs comparable to Axiom outputs. Aggregate simulators, distributional reports, parameter documentation, and public model summaries are not oracles for RuleSpec parity, even when they are useful as background references.

## Layout

- `be/statutes/`: federal Belgium primary law encoded as RuleSpec.
- `be/regulations/`: federal royal decrees, ministerial orders, and delegated instruments.
- `be/policies/`: federal agency guidance or rate surfaces when statute/regulation decomposition is not yet complete.
- `be-bru/statutes/`: Brussels-Capital Region and Common Community Commission ordinances and primary law.
- `be-bru/regulations/`: Brussels regional and COCOM delegated instruments.
- `be-bru/policies/`: Brussels agency guidance or rate surfaces after upstream legal source discovery.
- `be-vlg/statutes/`: Flemish Region and Flemish Community decrees and primary law where competence is integrated in Flemish institutions.
- `be-vlg/regulations/`: Flemish delegated instruments.
- `be-vlg/policies/`: Flemish agency guidance or rate surfaces after upstream legal source discovery.
- `be-wal/statutes/`: Walloon Region decrees and primary law.
- `be-wal/regulations/`: Walloon delegated instruments.
- `be-wal/policies/`: Walloon agency guidance or rate surfaces after upstream legal source discovery.
- `be-dg/statutes/`: German-speaking Community decrees and primary law for promoted community competences.
- `be-dg/regulations/`: German-speaking Community delegated instruments.
- `be-dg/policies/`: German-speaking Community agency guidance or rate surfaces after upstream legal source discovery.
- Other community-specific namespaces beyond `be-vlg` and `be-dg` are added when source manifests promote those competences.
- `data/corpus/`: source inventory, ingestion manifests, provision locators, and future promoted official extracts.
- `data/coverage/`: tax-benefit coverage backlog and official source map.
- `data/oracles/`: pinned household-level comparison references.

The first intake map is `data/coverage/tax-benefit-source-map.json`.

## Initial Build Strategy

This first pass is a source-first repo scaffold, not a formula port. The Belgium ELI/Moniteur adapter now exists in `axiom-corpus`, with the first tax-benefit manifest run at `2026-06-30-be-tax-benefit`. RuleSpec modules should cite those corpus artifacts before encoding formulas.

Durable ids should use `be:<path>#<rule>` for federal rules, `be-bru:<path>#<rule>` for Brussels rules, `be-vlg:<path>#<rule>` for Flemish rules, `be-wal:<path>#<rule>` for Walloon rules, and `be-dg:<path>#<rule>` for German-speaking Community rules.
