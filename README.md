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

- Atomic RuleSpec modules live only under
  `<jurisdiction>/{legislation,policies,regulations,statutes}/`, where the
  current jurisdictions are `be`, `be-bru`, `be-dg`, `be-vlg`, and `be-wal`.
- Declarative composition specs live only under
  `<jurisdiction>/programs/`. They are axiom-compose inputs, not atomic
  `rulespec/v1` modules, and are excluded from atomic companion-test and
  encoding-manifest workflows.
- Content files use the exact `.yaml` extension. Repository-root content trees,
  singular aliases, and compatibility symlinks are not supported.
- `data/corpus/`: source inventory, ingestion manifests, provision locators, and future promoted official extracts.
- `data/coverage/`: tax-benefit coverage backlog and official source map.
- `data/oracles/`: pinned household-level comparison references.

The first intake map is `data/coverage/tax-benefit-source-map.json`.

## Provenance contract

Every atomic module has exactly one non-empty
`module.source_verification.corpus_citation_path`. The only optional sibling is
a lowercase 64-character `source_sha256`. Independently operative secondary
sources belong on the rules they support as direct proof atoms with an exact
corpus citation and exact `excerpt`; plural module paths, mutable source
claims, and compatibility metadata are rejected.

Legacy `axiom-encode/applied-rulespec/v1` manifests are not retained. A future
manifest format may be introduced only through the trusted v5 signing path.

Durable ids should use `be:<path>#<rule>` for federal rules, `be-bru:<path>#<rule>` for Brussels rules, `be-vlg:<path>#<rule>` for Flemish rules, `be-wal:<path>#<rule>` for Walloon rules, and `be-dg:<path>#<rule>` for German-speaking Community rules.

## Money proof-atom coverage

Every policy-bearing monetary value — currency parameters, currency parameter-table cells, and currency literals in derived formulas — must carry a proof atom whose source cites a provision. The shared `validate-rulespec` workflow enforces this with `axiom-encode proof-validate --money-atoms-only` and no allowance file: the repository has 598 obligations and permits zero missing atoms.
