from __future__ import annotations

import json
import re
from decimal import Decimal, InvalidOperation
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
JURISDICTION_DIR_RE = re.compile(r"^[a-z]{2}(-[a-z0-9-]+)*$")
CONTENT_DIRS = ("statutes", "regulations", "policies", "legislation")
IGNORED_DIRS = {".git", ".pytest_cache", ".venv", "__pycache__", "_axiom"}
DISALLOWED_GENERIC_RULE_NAMES = {
    "amount",
    "base",
    "excess",
    "excess_wages",
    "rate",
    "threshold",
    "value",
}
POLICY_BEARING_PARAMETER_DTYPES = {"Money", "Rate"}
POLICY_BEARING_PARAMETER_NAME_TOKENS = (
    "amount",
    "rate",
    "threshold",
    "cap",
    "ceiling",
    "floor",
    "minimum",
    "maximum",
    "premium",
    "allowance",
    "reduction",
    "credit",
    "disregard",
    "exemption",
    "income",
    "wage",
    "remuneration",
    "coefficient",
    "index",
    "bracket",
    "tax",
    "contribution",
    "withholding",
    "forfait",
    "supplement",
    "grant",
    "benefit",
)
STRUCTURAL_PARAMETER_NAME_TOKENS = (
    "selector",
    "category",
    "status",
    "code",
    "count",
    "months",
    "days",
    "years",
    "age",
    "number",
    "id",
    "region",
    "reference_year",
    "relationship",
    "source",
    "denominator",
)
NUMERIC_TEXT_RE = re.compile(
    r"(?<![\w.,])[-+]?(?:\d+(?:[ .\u00a0]\d{3})+|\d+)(?:\s*[,.]\d+)?\s*(?:%|p\.c\.|pc|pour cent)?(?![\w.,])"
)
SIMPLE_NUMERIC_FORMULA_RE = re.compile(r"^[+-]?\d+(?:\.\d+)?$")
FRENCH_NUMBER_WORD_VALUES = {
    "un": Decimal("1"),
    "une": Decimal("1"),
    "deux": Decimal("2"),
    "trois": Decimal("3"),
    "quatre": Decimal("4"),
    "cinq": Decimal("5"),
    "six": Decimal("6"),
    "sept": Decimal("7"),
    "huit": Decimal("8"),
    "neuf": Decimal("9"),
    "dix": Decimal("10"),
    "onze": Decimal("11"),
    "douze": Decimal("12"),
    "treize": Decimal("13"),
    "quatorze": Decimal("14"),
    "quinze": Decimal("15"),
    "seize": Decimal("16"),
    "dix-sept": Decimal("17"),
    "dix sept": Decimal("17"),
    "dix-huit": Decimal("18"),
    "dix huit": Decimal("18"),
    "dix-neuf": Decimal("19"),
    "dix neuf": Decimal("19"),
    "vingt": Decimal("20"),
    "trente": Decimal("30"),
    "quarante": Decimal("40"),
    "cinquante": Decimal("50"),
    "soixante": Decimal("60"),
    "moitié": Decimal("0.5"),
}


def jurisdiction_dirs() -> list[Path]:
    return sorted(
        child
        for child in ROOT.iterdir()
        if child.is_dir()
        and JURISDICTION_DIR_RE.match(child.name)
        and any((child / marker).is_dir() for marker in CONTENT_DIRS)
    )


def rulespec_content_roots() -> list[Path]:
    return [
        jurisdiction / marker
        for jurisdiction in jurisdiction_dirs()
        for marker in CONTENT_DIRS
        if (jurisdiction / marker).is_dir()
    ]


def allowed_yaml_roots() -> set[str]:
    return {
        ".axiom",
        ".github",
        "data",
        "known-dangling.yaml",
        "known-missing-money-atoms.yaml",
        "known-validation-gaps.yaml",
        *(d.name for d in jurisdiction_dirs()),
    }


def _validation_gaps(section: str) -> set[str]:
    path = ROOT / "known-validation-gaps.yaml"
    if not path.exists():
        return set()
    payload = yaml.safe_load(path.read_text()) or {}
    return set(payload.get(section) or [])


def apply_gap_ratchet(section: str, found: list[str]) -> list[str]:
    allowlisted = _validation_gaps(section)
    found_set = set(found)
    problems = [item for item in found if item not in allowlisted]
    problems.extend(
        f"known-validation-gaps.yaml {section} entry is fixed - remove it: {stale}"
        for stale in sorted(allowlisted - found_set)
    )
    return problems


def iter_repo_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.relative_to(ROOT).parts):
            continue
        if path.is_file():
            files.append(path)
    return sorted(files)


def iter_rulespec_files() -> list[Path]:
    files: list[Path] = []
    for root in rulespec_content_roots():
        files.extend(
            path for path in root.rglob("*.yaml") if not path.name.endswith(".test.yaml")
        )
    return sorted(files)


def canonical_rule_id(path: Path, rule_name: str) -> str:
    relative = path.relative_to(ROOT)
    prefix = relative.parts[0]
    target = Path(*relative.parts[1:]).with_suffix("").as_posix()
    return f"{prefix}:{target}#{rule_name}"


def proof_atoms(rule: dict) -> list[dict]:
    metadata = rule.get("metadata")
    if not isinstance(metadata, dict):
        return []
    proof = metadata.get("proof")
    if not isinstance(proof, dict):
        return []
    atoms = proof.get("atoms")
    return atoms if isinstance(atoms, list) else []


def is_policy_bearing_parameter(rule: dict) -> bool:
    if rule.get("kind") != "parameter":
        return False
    dtype = rule.get("dtype")
    name = str(rule.get("name", "")).lower()
    policy_bearing = dtype in POLICY_BEARING_PARAMETER_DTYPES or any(
        token in name for token in POLICY_BEARING_PARAMETER_NAME_TOKENS
    ) or "scalar_limit" in name
    structural = any(token in name for token in STRUCTURAL_PARAMETER_NAME_TOKENS)
    return policy_bearing and (
        not structural
        or dtype in POLICY_BEARING_PARAMETER_DTYPES
        or "scalar_limit" in name
    )


def parameter_formula_values(rule: dict) -> list[Decimal]:
    versions = rule.get("versions")
    if not isinstance(versions, list) or not versions:
        return []
    version = versions[0]
    if not isinstance(version, dict):
        return []
    formula = version.get("formula")
    if isinstance(formula, int | float):
        formula = str(formula)
    if not isinstance(formula, str):
        return []
    formula = formula.strip()
    if not SIMPLE_NUMERIC_FORMULA_RE.fullmatch(formula):
        return []
    return [Decimal(formula)]


def text_number_values(text: str) -> list[Decimal]:
    values: list[Decimal] = []
    for match in NUMERIC_TEXT_RE.finditer(text):
        token = match.group().strip().replace("\u00a0", " ")
        is_percent = (
            token.endswith("%")
            or token.endswith("p.c.")
            or token.endswith("pc")
            or token.endswith("pour cent")
        )
        token = (
            token.removesuffix("%")
            .removesuffix("p.c.")
            .removesuffix("pc")
            .removesuffix("pour cent")
            .strip()
            .replace(" ", "")
        )
        if "," in token and "." in token:
            if token.rfind(",") > token.rfind("."):
                token = token.replace(".", "").replace(",", ".")
            else:
                token = token.replace(",", "")
        elif "," in token:
            token = token.replace(",", ".")
        elif re.fullmatch(r"[-+]?\d{1,3}(?:\.\d{3})+", token):
            token = token.replace(".", "")
        try:
            value = Decimal(token)
        except InvalidOperation:
            continue
        values.append(value)
        if is_percent:
            values.append(value / Decimal("100"))
    lower_text = text.lower()
    for word, value in FRENCH_NUMBER_WORD_VALUES.items():
        if re.search(rf"\b{re.escape(word)}\b", lower_text):
            values.append(value)
    return values


def span_contains_formula_value(
    formula_values: list[Decimal], span_values: list[Decimal], span: str
) -> bool:
    if any(
        formula_value == span_value
        for formula_value in formula_values
        for span_value in span_values
    ):
        return True
    if "%" not in span and "p.c." not in span and "pour cent" not in span:
        return False
    return any(
        Decimal("0") < formula_value < Decimal("1")
        and formula_value * Decimal("100") == span_value
        for formula_value in formula_values
        for span_value in span_values
    )


def module_has_source_locator(payload: object) -> bool:
    if not isinstance(payload, dict):
        return False
    module = payload.get("module")
    if not isinstance(module, dict):
        return False
    source_verification = module.get("source_verification")
    if not isinstance(source_verification, dict):
        return False
    if source_verification.get("corpus_citation_path"):
        return True
    citation_paths = source_verification.get("corpus_citation_paths")
    return isinstance(citation_paths, list) and any(citation_paths)


def source_spine() -> dict:
    return json.loads((ROOT / "data/corpus/inventory/be/source-spine.json").read_text())


def source_map() -> dict:
    return json.loads((ROOT / "data/coverage/tax-benefit-source-map.json").read_text())


def backlog() -> dict:
    return json.loads((ROOT / "data/coverage/full-country-backlog.json").read_text())


def oracle_index() -> dict:
    return json.loads((ROOT / "data/oracles/oracle-index.json").read_text())


def euromod_coverage() -> dict:
    return json.loads((ROOT / "data/coverage/euromod-be-coverage.json").read_text())


def test_has_full_belgium_jurisdiction_namespaces() -> None:
    assert [path.name for path in jurisdiction_dirs()] == [
        "be",
        "be-bru",
        "be-dg",
        "be-vlg",
        "be-wal",
    ]


def test_oracle_index_requires_household_level_executable_comparisons() -> None:
    index = oracle_index()
    oracle_scope = index["oracle_scope"]
    oracle_ids = {oracle["id"] for oracle in index["oracles"]}
    source_map_oracle_ids = {
        surface["oracle_id"]
        for track in source_map()["tracks"]
        for surface in track["oracle_surfaces"]
    }

    assert "household-level inputs" in oracle_scope
    assert "household-level tax-benefit outputs" in oracle_scope
    assert "public model summaries" in oracle_scope
    assert "not oracles" in oracle_scope
    assert source_map_oracle_ids <= oracle_ids


def test_euromod_inventory_tracks_current_pilot_oracle_scope() -> None:
    coverage = euromod_coverage()
    euromod_oracle = next(
        oracle
        for oracle in oracle_index()["oracles"]
        if oracle["id"] == "euromod-belgium"
    )
    denominator = coverage["denominator"]
    policies = coverage["euromod_policies"]
    outputs = {
        target["euromod_variable"]: target
        for target in coverage["oracle_output_coverage"]
    }

    assert euromod_oracle["coverage_inventory"] == (
        "data/coverage/euromod-be-coverage.json"
    )
    assert euromod_oracle["authority"] == "oracle_pinned_for_pilot_outputs"
    assert denominator["policy_count"] == len(policies) == 43
    assert denominator["function_count"] == 1171
    assert denominator["parameter_count"] == 8211
    assert denominator["policy_switch_counts"] == {
        "on": 32,
        "off": 7,
        "switch": 3,
        "n/a": 1,
    }
    assert coverage["coverage_summary"]["rule_percentage"] is None
    assert coverage["coverage_summary"]["full_household_disposable_income_parity"] is False
    assert coverage["coverage_summary"]["live_verified_oracle_output_targets"] == 1
    assert outputs["tscee_s"]["status"] == (
        "live_oracle_verified_for_regular_worker_statutory_slice"
    )
    assert outputs["tin_s"]["status"] == "prepared_worker_pilot_not_full_household_parity"
    assert outputs["ils_dispy"]["status"] == "not_mapped"


def test_euromod_inventory_references_existing_rulespec_modules() -> None:
    coverage = euromod_coverage()
    module_paths = [
        output["rulespec_module"]
        for output in coverage["oracle_output_coverage"]
        if output["rulespec_module"]
    ]
    module_paths.extend(
        module
        for domain in coverage["domain_coverage"]
        for module in domain["rulespec_modules"]
    )

    missing = [
        module for module in sorted(set(module_paths)) if not (ROOT / module).exists()
    ]

    assert missing == []


def test_euromod_domain_policy_codes_are_known() -> None:
    coverage = euromod_coverage()
    policy_codes = {policy["code"] for policy in coverage["euromod_policies"]}
    unknown = [
        f"{domain['domain']}:{code}"
        for domain in coverage["domain_coverage"]
        for code in domain["euromod_policies"]
        if code not in policy_codes
    ]

    assert unknown == []


def test_json_manifests_parse() -> None:
    for path in sorted((ROOT / "data").rglob("*.json")):
        json.loads(path.read_text())


def test_tax_benefit_source_map_references_known_ids() -> None:
    track_ids = {track["id"] for track in backlog()["tracks"]}
    source_ids = {source["id"] for source in source_spine()["sources"]}
    oracle_ids = {oracle["id"] for oracle in oracle_index()["oracles"]}

    unknown_tracks = [
        track["track_id"]
        for track in source_map()["tracks"]
        if track["track_id"] not in track_ids
    ]
    unknown_sources = [
        f"{track['track_id']}:{source['source_id']}"
        for track in source_map()["tracks"]
        for source in track["official_source_refs"]
        if source["source_id"] not in source_ids
    ]
    unknown_oracles = [
        f"{track['track_id']}:{oracle['oracle_id']}"
        for track in source_map()["tracks"]
        for oracle in track["oracle_surfaces"]
        if oracle["oracle_id"] not in oracle_ids
    ]

    assert unknown_tracks == []
    assert unknown_sources == []
    assert unknown_oracles == []


def test_source_map_covers_every_backlog_track() -> None:
    backlog_tracks = {track["id"] for track in backlog()["tracks"]}
    mapped_tracks = {track["track_id"] for track in source_map()["tracks"]}

    assert mapped_tracks == backlog_tracks


def test_source_priority_starts_from_upstream_law() -> None:
    sources = {source["id"]: source for source in source_spine()["sources"]}

    for track in source_map()["tracks"]:
        refs = track["official_source_refs"]
        assert refs, f"{track['track_id']} has no official source refs"
        first_source = sources[refs[0]["source_id"]]
        assert first_source["source_tier"] == 1, track["track_id"]
        assert refs[0]["source_priority_role"] == "primary_law_or_original_publication"


def test_justel_is_only_a_non_authentic_locator() -> None:
    justel = next(source for source in source_spine()["sources"] if source["id"] == "justel-eli")

    assert justel["canonical"] is False
    assert justel["source_tier"] == 2
    assert "not an authentic official source" in justel["notes"]


def test_no_obsolete_formula_artifacts() -> None:
    obsolete_ext = ".r" "ac"
    obsolete = [
        path.relative_to(ROOT).as_posix()
        for path in iter_repo_files()
        if path.name.endswith(obsolete_ext)
        or path.name.endswith(f"{obsolete_ext}.test")
        or path.name in {"parameters.yaml", "tests.yaml"}
    ]

    assert obsolete == []


def test_no_disallowed_roots_or_yaml_fixtures() -> None:
    singular_bases = [ROOT, *jurisdiction_dirs()]
    disallowed_roots = [
        (base / name).relative_to(ROOT).as_posix()
        for base in singular_bases
        for name in ("statute", "regulation", "policy")
        if (base / name).exists()
    ]
    yaml_fixtures = [
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "tests").rglob("*.yaml")
        if (ROOT / "tests").exists()
    ]
    allowed = allowed_yaml_roots()
    stray_yaml = [
        path.relative_to(ROOT).as_posix()
        for path in iter_repo_files()
        if path.suffix in {".yaml", ".yml"}
        and path.relative_to(ROOT).parts[0] not in allowed
    ]

    assert disallowed_roots == []
    assert yaml_fixtures == []
    assert stray_yaml == []


def test_rulespec_files_have_companion_tests() -> None:
    missing = [
        path.relative_to(ROOT).as_posix()
        for path in iter_rulespec_files()
        if not path.with_name(f"{path.stem}.test.yaml").exists()
    ]

    assert apply_gap_ratchet("missing_companion_tests", missing) == []


def test_companion_tests_have_rulespec_files() -> None:
    orphaned = []
    for root in rulespec_content_roots():
        orphaned.extend(
            path.relative_to(ROOT).as_posix()
            for path in sorted(root.rglob("*.test.yaml"))
            if not path.with_name(f"{path.stem.removesuffix('.test')}.yaml").exists()
        )

    assert orphaned == []


def test_rulespec_files_use_rulespec_v1_shape() -> None:
    invalid: list[str] = []

    for path in iter_rulespec_files():
        payload = yaml.safe_load(path.read_text()) or {}
        if not isinstance(payload, dict):
            invalid.append(f"{path.relative_to(ROOT)}: top-level YAML is not a mapping")
            continue
        if payload.get("format") != "rulespec/v1":
            invalid.append(f"{path.relative_to(ROOT)}: missing format: rulespec/v1")
        rules = payload.get("rules")
        if not isinstance(rules, list) or not rules:
            module = payload.get("module")
            status = module.get("status") if isinstance(module, dict) else None
            if rules == [] and status in {"deferred", "entity_not_supported"}:
                continue
            invalid.append(f"{path.relative_to(ROOT)}: missing non-empty rules list")
            continue
        for index, rule in enumerate(rules):
            if not isinstance(rule, dict):
                invalid.append(f"{path.relative_to(ROOT)}: rules[{index}] is not a mapping")
                continue
            for key in ("name", "kind"):
                if key not in rule:
                    invalid.append(f"{path.relative_to(ROOT)}: rules[{index}] missing {key}")
            if rule.get("kind") in {"parameter", "derived"} and "versions" not in rule:
                invalid.append(f"{path.relative_to(ROOT)}: rules[{index}] missing versions")

    invalid_paths = sorted({item.split(":", 1)[0] for item in invalid})
    assert apply_gap_ratchet("shape_issues", invalid_paths) == []


def test_derived_rules_declare_period_metadata() -> None:
    missing: list[str] = []

    for path in iter_rulespec_files():
        payload = yaml.safe_load(path.read_text()) or {}
        rules = payload.get("rules")
        if not isinstance(rules, list):
            continue
        for rule in rules:
            if not isinstance(rule, dict) or rule.get("kind") != "derived":
                continue
            if "period" not in rule:
                name = rule.get("name", "<unnamed>")
                missing.append(f"{path.relative_to(ROOT).as_posix()}#{name}")

    assert missing == []


def test_rulespec_rules_have_source_metadata() -> None:
    missing: list[str] = []

    for path in iter_rulespec_files():
        payload = yaml.safe_load(path.read_text()) or {}
        rules = payload.get("rules")
        if not isinstance(rules, list):
            continue
        module_source_locator = module_has_source_locator(payload)
        for index, rule in enumerate(rules):
            if not isinstance(rule, dict):
                continue
            name = rule.get("name", f"rules[{index}]")
            if rule.get("kind") in {"data_relation", "source_relation"}:
                continue
            if not rule.get("source"):
                missing.append(f"{path.relative_to(ROOT)}: {name} missing source")
            if not module_source_locator:
                missing.append(
                    f"{path.relative_to(ROOT)}: {name} missing source locator"
                )

    assert missing == []


def test_policy_bearing_parameters_have_formula_proof_atoms() -> None:
    missing: list[str] = []

    for path in iter_rulespec_files():
        payload = yaml.safe_load(path.read_text()) or {}
        rules = payload.get("rules")
        if not isinstance(rules, list):
            continue
        for rule in rules:
            if not isinstance(rule, dict):
                continue
            if is_policy_bearing_parameter(rule) and not proof_atoms(rule):
                name = str(rule.get("name", "<unnamed>"))
                missing.append(f"{path.relative_to(ROOT).as_posix()}#{name}")

    assert apply_gap_ratchet("policy_parameters_missing_proof_atoms", missing) == []


def test_policy_parameter_proof_atoms_anchor_formula_values() -> None:
    invalid: list[str] = []

    for path in iter_rulespec_files():
        payload = yaml.safe_load(path.read_text()) or {}
        rules = payload.get("rules")
        if not isinstance(rules, list):
            continue
        module = payload.get("module")
        source_verification = (
            module.get("source_verification") if isinstance(module, dict) else None
        )
        module_source_paths: set[str] = set()
        if isinstance(source_verification, dict):
            citation_path = source_verification.get("corpus_citation_path")
            if isinstance(citation_path, str):
                module_source_paths.add(citation_path)
            citation_paths = source_verification.get("corpus_citation_paths")
            if isinstance(citation_paths, list):
                module_source_paths.update(
                    path for path in citation_paths if isinstance(path, str)
                )

        for rule in rules:
            if not isinstance(rule, dict):
                continue
            if not is_policy_bearing_parameter(rule):
                continue
            name = str(rule.get("name", "<unnamed>"))
            for index, atom in enumerate(proof_atoms(rule)):
                atom_id = f"{path.relative_to(ROOT).as_posix()}#{name}.atoms[{index}]"
                if not isinstance(atom, dict):
                    invalid.append(f"{atom_id}: atom is not a mapping")
                    continue
                source = atom.get("source")
                if not isinstance(source, dict):
                    invalid.append(f"{atom_id}: missing source mapping")
                    continue
                citation_path = source.get("corpus_citation_path")
                if atom.get("path") != "versions[0].formula":
                    invalid.append(f"{atom_id}: atom must anchor versions[0].formula")
                if atom.get("kind") != "parameter":
                    invalid.append(f"{atom_id}: atom kind must be parameter")
                if not isinstance(citation_path, str) or not citation_path:
                    invalid.append(f"{atom_id}: missing corpus_citation_path")
                elif citation_path not in module_source_paths:
                    invalid.append(
                        f"{atom_id}: corpus_citation_path is not in module source_verification"
                    )
                if not isinstance(source.get("span"), str) or not source["span"].strip():
                    invalid.append(f"{atom_id}: missing source span")

    assert invalid == []


def test_policy_parameter_proof_atom_spans_contain_formula_values() -> None:
    invalid: list[str] = []

    for path in iter_rulespec_files():
        payload = yaml.safe_load(path.read_text()) or {}
        rules = payload.get("rules")
        if not isinstance(rules, list):
            continue

        for rule in rules:
            if not isinstance(rule, dict):
                continue
            if not is_policy_bearing_parameter(rule):
                continue
            formula_values = parameter_formula_values(rule)
            if not formula_values:
                continue
            name = str(rule.get("name", "<unnamed>"))
            for index, atom in enumerate(proof_atoms(rule)):
                if not isinstance(atom, dict):
                    continue
                source = atom.get("source")
                span = source.get("span") if isinstance(source, dict) else None
                if not isinstance(span, str):
                    continue
                span_values = text_number_values(span)
                if not span_contains_formula_value(formula_values, span_values, span):
                    invalid.append(
                        f"{path.relative_to(ROOT).as_posix()}#{name}.atoms[{index}]"
                    )

    assert (
        apply_gap_ratchet(
            "policy_parameter_proof_atoms_missing_formula_value", invalid
        )
        == []
    )


def test_rulespec_files_use_corpus_source_locators() -> None:
    legacy: list[str] = []

    for path in iter_rulespec_files():
        payload = yaml.safe_load(path.read_text()) or {}
        if isinstance(payload, dict):
            module = payload.get("module")
            if isinstance(module, dict):
                if module.get("source_url"):
                    legacy.append(f"{path.relative_to(ROOT)}: module.source_url")
                source_verification = module.get("source_verification")
                if (
                    isinstance(source_verification, dict)
                    and source_verification.get("source_url")
                ):
                    legacy.append(
                        f"{path.relative_to(ROOT)}: "
                        "module.source_verification.source_url"
                    )
            rules = payload.get("rules")
            if isinstance(rules, list):
                for index, rule in enumerate(rules):
                    if not isinstance(rule, dict) or not rule.get("source_url"):
                        continue
                    name = rule.get("name", f"rules[{index}]")
                    legacy.append(f"{path.relative_to(ROOT)}: {name}.source_url")

    assert legacy == []


def test_rulespec_rule_names_are_specific() -> None:
    vague: list[str] = []

    for path in iter_rulespec_files():
        payload = yaml.safe_load(path.read_text()) or {}
        rules = payload.get("rules")
        if not isinstance(rules, list):
            continue
        for rule in rules:
            if not isinstance(rule, dict):
                continue
            name = rule.get("name")
            if name in DISALLOWED_GENERIC_RULE_NAMES:
                vague.append(f"{path.relative_to(ROOT)}: {name}")

    assert vague == []


def test_derived_rules_are_exercised_by_companion_tests() -> None:
    missing: list[str] = []

    for path in iter_rulespec_files():
        payload = yaml.safe_load(path.read_text()) or {}
        rules = payload.get("rules")
        if not isinstance(rules, list):
            continue
        derived_rule_names = [
            str(rule["name"])
            for rule in rules
            if isinstance(rule, dict)
            and rule.get("kind") == "derived"
            and isinstance(rule.get("name"), str)
        ]

        test_path = path.with_name(f"{path.stem}.test.yaml")
        if not test_path.exists():
            continue
        cases = yaml.safe_load(test_path.read_text()) or []
        covered_outputs: set[str] = set()
        if isinstance(cases, list):
            for case in cases:
                if not isinstance(case, dict):
                    continue
                outputs = case.get("output")
                if isinstance(outputs, dict):
                    covered_outputs.update(str(name) for name in outputs)

        missing.extend(
            f"{path.relative_to(ROOT).as_posix()}#{rule_name}"
            for rule_name in derived_rule_names
            if canonical_rule_id(path, rule_name) not in covered_outputs
        )

    assert apply_gap_ratchet("uncovered_derived_rules", missing) == []
