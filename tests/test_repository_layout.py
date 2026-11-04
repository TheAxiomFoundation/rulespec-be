from __future__ import annotations

import json
import re
import shutil
import subprocess
import tomllib
from decimal import Decimal, InvalidOperation
from pathlib import Path

import pytest
import yaml


ROOT = Path(__file__).resolve().parents[1]
JURISDICTION_DIR_RE = re.compile(r"^be(?:-[a-z0-9]+)*$")
ATOMIC_CONTENT_DIRS = ("legislation", "policies", "regulations", "statutes")
CANONICAL_CONTENT_DIRS = (*ATOMIC_CONTENT_DIRS, "programs")
APPLIED_ENCODING_MANIFEST_SCHEMA = "axiom-encode/applied-rulespec/v5"
CORPUS_CITATION_PATH_RE = re.compile(
    r"^be(?:-[a-z]{2,4})?/(?:guidance|regulation|statute)"
    r"(?:/[A-Za-z0-9][A-Za-z0-9 .\-–]*)+$"
)
SOURCE_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
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
    r"(?<![\w.,])(?:[-+]\s*)?(?:\d+(?:[ .\u00a0]\d{3})+|\d+)(?:\s*[,.]\s*\d+)?\s*(?:%|p\.c\.|pc|pour cent|procent|EUR|euros?)?(?![\w.,])",
    flags=re.IGNORECASE,
)
SIMPLE_NUMERIC_FORMULA_RE = re.compile(r"^[+-]?\d+(?:\.\d+)?$")
FORMULA_PROOF_PATH_RE = re.compile(r"^versions\[(\d+)\]\.formula$")
# A parameter *table* stores its policy numbers under `versions[i].values`, not
# a scalar `versions[i].formula`, so its proof atom anchors the table location.
# This is the same contract the axiom-encode money-atom gate derives and the
# base proof validator enforces (axiom-encode#1032); accepting it here lets a
# single table atom satisfy both strict gates.
VALUES_PROOF_PATH_RE = re.compile(r"^versions\[(\d+)\]\.values$")
FRENCH_NUMBER_WORD_VALUES = {
    "un": Decimal("1"),
    "une": Decimal("1"),
    "deux": Decimal("2"),
    "trois": Decimal("3"),
    "quatre": Decimal("4"),
    "cinq": Decimal("5"),
    "six": Decimal("6"),
    "sixième": Decimal("6"),
    "sept": Decimal("7"),
    "huit": Decimal("8"),
    "neuf": Decimal("9"),
    "dix": Decimal("10"),
    "onze": Decimal("11"),
    "douze": Decimal("12"),
    "douzième": Decimal("12"),
    "douzièmes": Decimal("12"),
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
    "vingt-cinq": Decimal("25"),
    "trente": Decimal("30"),
    "quarante": Decimal("40"),
    "cinquante": Decimal("50"),
    "soixante": Decimal("60"),
    "quart": Decimal("0.25"),
    "quatre cents": Decimal("400"),
    "huit cents": Decimal("800"),
    "moitié": Decimal("0.5"),
}
DUTCH_NUMBER_WORD_VALUES = {
    "nul": Decimal("0"),
    "twee": Decimal("2"),
    "drie": Decimal("3"),
    "vier": Decimal("4"),
    "vijf": Decimal("5"),
    "zes": Decimal("6"),
    "zeven": Decimal("7"),
    "acht": Decimal("8"),
    "negen": Decimal("9"),
    "tien": Decimal("10"),
    "elf": Decimal("11"),
    "twaalf": Decimal("12"),
    "dertien": Decimal("13"),
    "veertien": Decimal("14"),
    "vijftien": Decimal("15"),
    "zestien": Decimal("16"),
    "zeventien": Decimal("17"),
    "achttien": Decimal("18"),
    "negentien": Decimal("19"),
    "twintig": Decimal("20"),
    "vijfentwintig": Decimal("25"),
    "dertig": Decimal("30"),
    "veertig": Decimal("40"),
    "vijftig": Decimal("50"),
    "vierduizend": Decimal("4000"),
    "opdeciem": Decimal("0.1"),
    "gehalveerd": Decimal("0.5"),
}


def jurisdiction_dirs(root: Path = ROOT) -> list[Path]:
    return sorted(
        child
        for child in root.iterdir()
        if child.is_dir()
        and JURISDICTION_DIR_RE.match(child.name)
        and any((child / marker).is_dir() for marker in CANONICAL_CONTENT_DIRS)
    )


def rulespec_content_roots() -> list[Path]:
    return [
        jurisdiction / marker
        for jurisdiction in jurisdiction_dirs()
        for marker in ATOMIC_CONTENT_DIRS
        if (jurisdiction / marker).is_dir()
    ]


def allowed_yaml_roots() -> set[str]:
    return {
        ".axiom",
        ".github",
        "data",
        "known-validation-gaps.yaml",
        "oracle-coverage-pending.yaml",
        *(d.name for d in jurisdiction_dirs()),
    }


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


def nested_keys(value: object):
    if isinstance(value, dict):
        for key, nested in value.items():
            if isinstance(key, str):
                yield key
            yield from nested_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from nested_keys(nested)


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
    values: list[Decimal] = []
    for version in versions:
        if not isinstance(version, dict):
            continue
        formula = version.get("formula")
        if isinstance(formula, int | float):
            formula = str(formula)
        if not isinstance(formula, str):
            continue
        formula = formula.strip()
        if SIMPLE_NUMERIC_FORMULA_RE.fullmatch(formula):
            values.append(Decimal(formula))
    return values


def rule_version_is_parameter_table(rule: dict, version_index: int) -> bool:
    """Whether the rule's ``versions[version_index]`` is a parameter table.

    A parameter table stores its cells under ``values`` (a mapping) rather than
    a scalar ``formula``. Such a version's proof atom anchors
    ``versions[i].values`` with ``kind: parameter_table``.
    """
    versions = rule.get("versions")
    if not isinstance(versions, list) or version_index >= len(versions):
        return False
    version = versions[version_index]
    return isinstance(version, dict) and isinstance(version.get("values"), dict)


def text_number_values(text: str) -> list[Decimal]:
    values: list[Decimal] = []
    for match in NUMERIC_TEXT_RE.finditer(text):
        token = match.group().strip().replace("\u00a0", " ")
        lower_token = token.lower()
        is_percent = (
            lower_token.endswith("%")
            or lower_token.endswith("p.c.")
            or lower_token.endswith("pc")
            or lower_token.endswith("pour cent")
            or lower_token.endswith("procent")
        )
        token = re.sub(
            r"(?:%|p\.c\.|pc|pour cent|procent|EUR|euros?)$",
            "",
            token,
            flags=re.IGNORECASE,
        )
        token = re.sub(r"\s+", "", token)
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
        # A separated hyphen is ambiguous in flattened legal text: it may be a
        # negative sign (``- 12,5 %``) or a list/range separator
        # (``- 33,14 %`` / ``25.000,01 - 50.000,00``). Retain both readings.
        if value < 0:
            values.append(abs(value))
        if is_percent:
            values.append(value / Decimal("100"))
            if value < 0:
                values.append(abs(value) / Decimal("100"))
    # Table extraction can flatten adjacent columns into ambiguous text such as
    # ``6 126,12`` (fiscal-power value 6, amount EUR 126.12). Preserve both
    # column interpretations in addition to the thousands-group interpretation.
    for match in re.finditer(
        r"(?<![\w.,])(\d{1,3})\s+(\d{2,3}[,.]\d{2})(?![\w.,])", text
    ):
        values.append(Decimal(match.group(1)))
        values.append(Decimal(match.group(2).replace(",", ".")))
    # Effective-date parameters are proven by dates such as ``01.01.2028``.
    for year in re.findall(r"\b\d{1,2}[./-]\d{1,2}[./-](\d{4})\b", text):
        values.append(Decimal(year))
    for match in re.finditer(
        r"(?<![\w.,])(\d+(?:\s*[,.]\d+)?)\s*(?:et|à|a|-)\s*(\d+(?:\s*[,.]\d+)?)\s*%",
        text,
        flags=re.IGNORECASE,
    ):
        for token in match.groups():
            try:
                values.append(
                    Decimal(token.strip().replace(" ", "").replace(",", "."))
                    / Decimal("100")
                )
            except InvalidOperation:
                continue
    lower_text = text.lower()
    for word_values in (FRENCH_NUMBER_WORD_VALUES, DUTCH_NUMBER_WORD_VALUES):
        for word, value in word_values.items():
            if re.search(rf"\b{re.escape(word)}\b", lower_text):
                values.append(value)
    return values


def excerpt_contains_formula_value(
    formula_values: list[Decimal], excerpt_values: list[Decimal], excerpt: str
) -> bool:
    if any(
        formula_value == excerpt_value
        for formula_value in formula_values
        for excerpt_value in excerpt_values
    ):
        return True
    lower_excerpt = excerpt.lower()
    if Decimal("0") in formula_values and any(
        marker in lower_excerpt
        for marker in (
            "ne devez pas payer de taxe",
            "géén verkeersbelasting verschuldigd",
            "geen verkeersbelasting verschuldigd",
            "exonération",
            "vrijgesteld",
        )
    ):
        return True
    if (
        "%" not in excerpt
        and "p.c." not in excerpt
        and "pour cent" not in excerpt
        and "procent" not in excerpt
    ):
        return False
    return any(
        Decimal("0") < formula_value < Decimal("1")
        and formula_value * Decimal("100") == excerpt_value
        for formula_value in formula_values
        for excerpt_value in excerpt_values
    )


def proof_atom_anchor_text(source: object) -> str | None:
    """Return the exact corpus-body excerpt for a direct proof atom."""
    if not isinstance(source, dict):
        return None
    value = source.get("excerpt")
    if isinstance(value, str) and value.strip():
        return value
    return None


def module_has_source_locator(payload: object) -> bool:
    if not isinstance(payload, dict):
        return False
    module = payload.get("module")
    if not isinstance(module, dict):
        return False
    source_verification = module.get("source_verification")
    if not isinstance(source_verification, dict):
        return False
    citation_path = source_verification.get("corpus_citation_path")
    return isinstance(citation_path, str) and bool(citation_path.strip())


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


def test_canonical_jurisdiction_layout_is_a_hard_cut() -> None:
    problems: list[str] = []
    for marker in CANONICAL_CONTENT_DIRS:
        root_path = ROOT / marker
        if root_path.exists() or root_path.is_symlink():
            problems.append(f"repository-root content tree: {marker}")

    for jurisdiction in jurisdiction_dirs():
        for child in sorted(jurisdiction.iterdir()):
            relative = child.relative_to(ROOT).as_posix()
            if child.is_symlink():
                problems.append(f"symlink: {relative}")
            elif child.is_dir() and child.name not in CANONICAL_CONTENT_DIRS:
                problems.append(f"noncanonical content root: {relative}")
        for marker in CANONICAL_CONTENT_DIRS:
            content_root = jurisdiction / marker
            if not content_root.is_dir():
                continue
            for path in sorted(content_root.rglob("*")):
                if path.is_dir():
                    continue
                relative = path.relative_to(ROOT).as_posix()
                if path.is_symlink() or not path.is_file():
                    problems.append(f"non-regular content file: {relative}")
                elif path.suffix != ".yaml":
                    problems.append(f"content file must use exact .yaml: {relative}")

    assert problems == []


def test_program_roots_are_declarative_axiom_compose_only() -> None:
    problems: list[str] = []
    for jurisdiction in jurisdiction_dirs():
        program_root = jurisdiction / "programs"
        if not program_root.is_dir():
            continue
        for path in sorted(program_root.rglob("*.yaml")):
            relative = path.relative_to(ROOT).as_posix()
            payload = yaml.safe_load(path.read_text()) or {}
            if not isinstance(payload, dict):
                problems.append(f"{relative}: program spec is not a mapping")
                continue
            forbidden = sorted(set(payload) & {"format", "module", "rules"})
            if forbidden:
                problems.append(
                    f"{relative}: atomic RuleSpec keys in program spec {forbidden}"
                )
            if not isinstance(payload.get("program"), str) or not payload["program"]:
                problems.append(f"{relative}: missing declarative program id")
            if "period" not in payload:
                problems.append(f"{relative}: missing period")
            outputs = payload.get("outputs")
            if not isinstance(outputs, list) or not outputs:
                problems.append(f"{relative}: missing non-empty outputs")

    assert problems == []


def test_atomic_roots_contain_no_composition_modules() -> None:
    compositions: list[str] = []
    for path in iter_rulespec_files():
        payload = yaml.safe_load(path.read_text()) or {}
        module = payload.get("module") if isinstance(payload, dict) else None
        if isinstance(module, dict) and module.get("kind") == "composition":
            compositions.append(path.relative_to(ROOT).as_posix())

    assert compositions == []


def test_source_verification_uses_exact_singular_contract() -> None:
    problems: list[str] = []
    allowed_keys = {"corpus_citation_path", "source_sha256"}
    for path in iter_rulespec_files():
        payload = yaml.safe_load(path.read_text()) or {}
        relative = path.relative_to(ROOT).as_posix()
        module = payload.get("module") if isinstance(payload, dict) else None
        verification = (
            module.get("source_verification") if isinstance(module, dict) else None
        )
        if not isinstance(verification, dict):
            problems.append(f"{relative}: source_verification is not a mapping")
            continue
        unknown = sorted(set(verification) - allowed_keys)
        if unknown:
            problems.append(f"{relative}: unknown source_verification keys {unknown}")
        citation_path = verification.get("corpus_citation_path")
        if not isinstance(citation_path, str) or not citation_path.strip():
            problems.append(f"{relative}: missing singular corpus_citation_path")
        elif CORPUS_CITATION_PATH_RE.fullmatch(citation_path) is None:
            problems.append(f"{relative}: invalid corpus citation path {citation_path!r}")
        source_sha256 = verification.get("source_sha256")
        if source_sha256 is not None and (
            not isinstance(source_sha256, str)
            or SOURCE_SHA256_RE.fullmatch(source_sha256) is None
        ):
            problems.append(f"{relative}: source_sha256 must be lowercase hex")

    assert problems == []


def test_legacy_source_claim_and_plural_provenance_is_absent() -> None:
    problems: list[str] = []
    for path in iter_rulespec_files():
        payload = yaml.safe_load(path.read_text()) or {}
        relative = path.relative_to(ROOT).as_posix()
        keys = set(nested_keys(payload))
        if "corpus_citation_paths" in keys:
            problems.append(f"{relative}: plural corpus_citation_paths")
        if "source_claims" in keys:
            problems.append(f"{relative}: source_claims")
        rules = payload.get("rules") if isinstance(payload, dict) else None
        if not isinstance(rules, list):
            continue
        for rule in rules:
            if not isinstance(rule, dict):
                continue
            for atom in proof_atoms(rule):
                if not isinstance(atom, dict):
                    continue
                atom_keys = set(nested_keys(atom))
                if "claim" in atom_keys:
                    problems.append(
                        f"{relative}#{rule.get('name', '<unnamed>')}: proof claim"
                    )
                if "span" in atom_keys:
                    problems.append(
                        f"{relative}#{rule.get('name', '<unnamed>')}: legacy span"
                    )
                source = atom.get("source")
                if isinstance(source, dict) and source.get("corpus_citation_path"):
                    excerpt = source.get("excerpt")
                    if not isinstance(excerpt, str) or not excerpt.strip():
                        problems.append(
                            f"{relative}#{rule.get('name', '<unnamed>')}: "
                            "direct source lacks exact excerpt"
                        )

    assert problems == []


def encoding_manifest_problems(root: Path = ROOT) -> list[str]:
    """List the encoding manifests under root that the encoder would not write.

    The supervised encoder writes one v5 manifest for each atomic module it
    applies, at `.axiom/encoding-manifests/<module path>.json`, and lists the
    module among the manifest's applied files. When it retires the module, it
    rewrites that manifest to list the module as deleted and removes the
    module. The tree admits those manifests and nothing else: no legacy v1
    manifest, no manifest for a companion test or a program, and no manifest
    root inside a jurisdiction.

    This checks schema, placement and applied/deleted module entries. The
    generated guard verifies signatures and file hashes. At the older pins in
    ENCODERS_THAT_SKIP_MANIFEST_ONLY_CHANGES, it reads changed manifests only
    when the change also touches RuleSpec YAML; otherwise it returns without
    reading them. manifests_the_guard_skips refuses every manifest at those
    pins to close that gap. A refused manifest gets one line, for the first
    problem in the order read, schema, placement, entry, file.
    """
    jurisdictions = jurisdiction_dirs(root)
    names = set(BELGIAN_JURISDICTIONS)
    problems = [
        f"co-located manifest root: {nested.relative_to(root).as_posix()}"
        for nested in (
            jurisdiction / ".axiom" / "encoding-manifests"
            for jurisdiction in jurisdictions
        )
        if nested.exists() or nested.is_symlink()
    ]
    manifest_root = root / ".axiom" / "encoding-manifests"
    if not manifest_root.is_dir():
        return problems
    for manifest in sorted(manifest_root.rglob("*.json")):
        relative = manifest.relative_to(manifest_root)
        problem = encoding_manifest_problem(root, names, relative)
        if problem is not None:
            problems.append(f"{relative.as_posix()}: {problem}")
    return problems


def encoding_manifest_problem(
    root: Path, jurisdictions: set[str], relative: Path
) -> str | None:
    """Return the first problem with one manifest, or None to admit it."""
    try:
        # Like the encoder's loader, decode strict UTF-8 before parsing.
        payload = json.loads(
            (root / ".axiom" / "encoding-manifests" / relative)
            .read_bytes()
            .decode("utf-8")
        )
    except OSError:
        return "is not a readable file"
    except (RecursionError, ValueError):
        return "is not JSON"
    schema = payload.get("schema_version") if isinstance(payload, dict) else None
    if schema != APPLIED_ENCODING_MANIFEST_SCHEMA:
        return f"schema {schema!r}"
    module = relative.with_suffix(".yaml")
    if (
        # The encoder writes <module path> with its suffix swapped for .json,
        # so a name with no suffix, such as `.json`, maps back to no module.
        relative.suffix != ".json"
        or len(module.parts) < 3
        or module.parts[0] not in jurisdictions
        or module.parts[1] not in ATOMIC_CONTENT_DIRS
        or module.name.endswith(".test.yaml")
    ):
        return "mirrors no atomic module path"
    entries = payload.get("applied_files")
    deleted = {
        entry.get("deleted") is True
        for entry in (entries if isinstance(entries, list) else [])
        if isinstance(entry, dict) and entry.get("path") == module.as_posix()
    }
    module_path = root / module
    if not deleted:
        return f"does not list {module.as_posix()}"
    if deleted == {False, True}:
        return f"both applies and deletes {module.as_posix()}"
    if deleted == {False} and not module_path.is_file():
        return f"{module.as_posix()} is missing"
    if deleted == {True} and (module_path.exists() or module_path.is_symlink()):
        return f"deletes {module.as_posix()} but it still exists"
    return None


# These historical encoder pins return from guard-generated before reading
# any manifest when a change touches no RuleSpec YAML. Changes that also touch
# RuleSpec YAML still verify manifests. axiom-encode#1853 (fa0da5e8) closes the
# gap; a re-pin to that commit or later needs no test changes.
ENCODERS_THAT_SKIP_MANIFEST_ONLY_CHANGES = frozenset(
    {
        "185b2457c16df11bf328fd6257a5b7fbe3fe7534",
        "b9d376684cfb5e86202daa3451b8fc716703ed19",
    }
)
FIRST_ENCODER_THAT_CHECKS_MANIFEST_ONLY_CHANGES = (
    "fa0da5e834214052cc8d9d381e25ff409dd1062f"
)

# Historical evidence, independent of whichever encoder the workflow pins now.
SKIPPING_ENCODER_PIN_HISTORY = {
    "185b2457c16df11bf328fd6257a5b7fbe3fe7534": "2966944dffd68e48dbed4a862c127a842f21f83c",
    "b9d376684cfb5e86202daa3451b8fc716703ed19": "bbf143dd234cf0d3f8ba2acc5404bc239617067b",
}


def pinned_encoder_ref(root: Path = ROOT) -> str:
    """Return the axiom-encode commit that CI runs the generated guard from."""
    workflow = yaml.safe_load(
        (root / ".github/workflows/repository-checks.yml").read_text()
    )
    return workflow["jobs"]["validate"]["with"]["axiom-encode-ref"]


def manifests_the_guard_skips(root: Path = ROOT) -> list[str]:
    """List every manifest under root while the pinned guard skips them.

    At a pin in ENCODERS_THAT_SKIP_MANIFEST_ONLY_CHANGES, the guard admits a
    change that adds only manifests without reading them, so the tree admits
    no manifest. At any other pin this returns nothing and leaves each
    manifest to encoding_manifest_problems and the guard.
    """
    manifest_root = root / ".axiom" / "encoding-manifests"
    encoder_ref = pinned_encoder_ref(root)
    if encoder_ref not in ENCODERS_THAT_SKIP_MANIFEST_ONLY_CHANGES:
        return []
    return [
        f"{manifest.relative_to(manifest_root).as_posix()}: the pinned encoder "
        f"{encoder_ref[:8]} does not verify a change that adds only manifests"
        for manifest in sorted(manifest_root.rglob("*.json"))
    ]


def test_encoding_manifests_sit_where_the_encoder_writes_them() -> None:
    assert encoding_manifest_problems() == []


def test_no_manifest_lands_while_the_pinned_guard_skips_manifest_only_changes() -> None:
    assert manifests_the_guard_skips() == []


def test_the_skipping_encoders_are_full_commit_ids() -> None:
    # The workflow pins full lowercase ids; a short one here would never match.
    for encoder_ref in (
        *ENCODERS_THAT_SKIP_MANIFEST_ONLY_CHANGES,
        FIRST_ENCODER_THAT_CHECKS_MANIFEST_ONLY_CHANGES,
    ):
        assert re.fullmatch(r"[0-9a-f]{40}", encoder_ref), encoder_ref
    assert (
        FIRST_ENCODER_THAT_CHECKS_MANIFEST_ONLY_CHANGES
        not in ENCODERS_THAT_SKIP_MANIFEST_ONLY_CHANGES
    )


def test_the_skipping_encoders_match_the_recorded_historical_pins() -> None:
    assert ENCODERS_THAT_SKIP_MANIFEST_ONLY_CHANGES == set(SKIPPING_ENCODER_PIN_HISTORY)
    for repository_commit in SKIPPING_ENCODER_PIN_HISTORY.values():
        assert re.fullmatch(r"[0-9a-f]{40}", repository_commit), repository_commit


def test_the_recorded_encoder_pins_match_repository_history() -> None:
    shallow = subprocess.check_output(
        ["git", "rev-parse", "--is-shallow-repository"], cwd=ROOT, text=True
    ).strip()
    if shallow == "true":
        pytest.skip("Historical pin commits are unavailable in a shallow checkout")
    assert shallow == "false"
    for encoder_ref, repository_commit in SKIPPING_ENCODER_PIN_HISTORY.items():
        workflow = yaml.safe_load(
            subprocess.check_output(
                [
                    "git",
                    "show",
                    f"{repository_commit}:.github/workflows/repository-checks.yml",
                ],
                cwd=ROOT,
                text=True,
            )
        )
        assert workflow["jobs"]["validate"]["with"]["axiom-encode-ref"] == encoder_ref


BELGIAN_JURISDICTIONS = ("be", "be-bru", "be-dg", "be-vlg", "be-wal")
MODULE = "be/statutes/example/rule.yaml"
COMPANION = "be/statutes/example/rule.test.yaml"
MANIFEST = "be/statutes/example/rule.json"


def write_manifest_fixture(
    root: Path,
    *,
    schema: object = APPLIED_ENCODING_MANIFEST_SCHEMA,
    manifest: str = MANIFEST,
    applied: tuple[str, ...] = (MODULE, COMPANION),
    deleted: tuple[str, ...] = (),
    files: tuple[str, ...] = (MODULE, COMPANION),
) -> None:
    """Write a manifest under root's manifest root, and the files it names.

    The manifest holds only the two fields the check reads: the schema and
    the applied files, each entry naming a path, as applied or as deleted.
    """
    for jurisdiction in BELGIAN_JURISDICTIONS:
        (root / jurisdiction / "statutes").mkdir(parents=True, exist_ok=True)
    for name in files:
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text("format: rulespec/v1\n")
    entries = [{"path": path} for path in applied]
    entries += [{"path": path, "deleted": True} for path in deleted]
    payload: dict[str, object] = {"applied_files": entries}
    if schema is not None:
        payload["schema_version"] = schema
    write_raw_manifest(root, manifest, json.dumps(payload).encode())


def write_raw_manifest(root: Path, manifest: str, content: bytes) -> None:
    path = root / ".axiom" / "encoding-manifests" / manifest
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def test_the_jurisdiction_fixture_matches_the_repository() -> None:
    assert tuple(path.name for path in jurisdiction_dirs()) == BELGIAN_JURISDICTIONS


@pytest.mark.parametrize("jurisdiction", BELGIAN_JURISDICTIONS)
@pytest.mark.parametrize("atomic_root", ATOMIC_CONTENT_DIRS)
def test_the_manifests_the_encoder_writes_are_admitted(
    tmp_path: Path, jurisdiction: str, atomic_root: str
) -> None:
    applied = tmp_path / "applied"
    retired = tmp_path / "retired"
    stem = f"{jurisdiction}/{atomic_root}/example/rule"
    module, companion = f"{stem}.yaml", f"{stem}.test.yaml"
    write_manifest_fixture(
        applied,
        manifest=f"{stem}.json",
        applied=(module, companion),
        files=(module, companion),
    )
    # A retirement keeps the manifest, lists both files as deleted and removes them.
    write_manifest_fixture(
        retired,
        manifest=f"{stem}.json",
        applied=(),
        deleted=(module, companion),
        files=(),
    )
    assert encoding_manifest_problems(applied) == []
    assert encoding_manifest_problems(retired) == []


@pytest.mark.parametrize("jurisdiction", BELGIAN_JURISDICTIONS)
def test_retirement_manifests_survive_an_empty_jurisdiction(
    tmp_path: Path, jurisdiction: str
) -> None:
    # be-dg's two modules can both be retired, leaving no jurisdiction directory.
    for name in ("amounts", "eligibility"):
        stem = f"{jurisdiction}/statutes/family_benefits/{name}"
        write_manifest_fixture(
            tmp_path,
            manifest=f"{stem}.json",
            applied=(),
            deleted=(f"{stem}.yaml", f"{stem}.test.yaml"),
            files=(),
        )
    shutil.rmtree(tmp_path / jurisdiction)
    assert not (tmp_path / jurisdiction).exists()
    assert encoding_manifest_problems(tmp_path) == []


def test_other_applied_files_and_deleted_paths_do_not_matter(tmp_path: Path) -> None:
    # A signed replacement also lists repository files it rewrote, and a path
    # migration's manifest lists the module's old path as deleted.
    write_manifest_fixture(
        tmp_path,
        applied=(
            MODULE,
            COMPANION,
            ".axiom/toolchain.toml",
            "known-validation-gaps.yaml",
        ),
        deleted=("be/statutes/old/rule.yaml", "be/statutes/old/rule.test.yaml"),
    )
    assert encoding_manifest_problems(tmp_path) == []


FAULTS = ("schema", "placement", "entry", "file")


@pytest.mark.parametrize(
    "faults",
    [
        tuple(fault for bit, fault in enumerate(FAULTS) if mask >> bit & 1)
        for mask in range(1 << len(FAULTS))
    ],
    ids=lambda faults: "+".join(faults) or "none",
)
def test_a_manifest_gets_one_line_for_its_first_problem(
    tmp_path: Path, faults: tuple[str, ...]
) -> None:
    manifest = "be/programs/example/rule.json" if "placement" in faults else MANIFEST
    write_manifest_fixture(
        tmp_path,
        schema="axiom-encode/applied-rulespec/v1"
        if "schema" in faults
        else APPLIED_ENCODING_MANIFEST_SCHEMA,
        manifest=manifest,
        applied=(COMPANION,) if "entry" in faults else (MODULE, COMPANION),
        files=(COMPANION,) if "file" in faults else (MODULE, COMPANION),
    )
    first = {
        "schema": "schema 'axiom-encode/applied-rulespec/v1'",
        "placement": "mirrors no atomic module path",
        "entry": f"does not list {MODULE}",
        "file": f"{MODULE} is missing",
    }
    expected = [f"{manifest}: {first[faults[0]]}"] if faults else []
    assert encoding_manifest_problems(tmp_path) == expected


@pytest.mark.parametrize(
    ("fixture", "problem"),
    [
        ({"schema": None}, "schema None"),
        ({"schema": 5}, "schema 5"),
        (
            {"schema": "axiom-encode/applied-rulespec/v50"},
            "schema 'axiom-encode/applied-rulespec/v50'",
        ),
        (
            {"schema": "axiom-encode/applied-rulespec/v"},
            "schema 'axiom-encode/applied-rulespec/v'",
        ),
        (
            {"schema": "axiom-encode/applied-rulespec/v5 "},
            "schema 'axiom-encode/applied-rulespec/v5 '",
        ),
        (
            {"manifest": "rule.json", "applied": ("rule.yaml",)},
            "mirrors no atomic module path",
        ),
        (
            {"manifest": "be/statutes.json", "applied": ("be/statutes.yaml",)},
            "mirrors no atomic module path",
        ),
        (
            {"manifest": "be-xx/statutes/example/rule.json"},
            "mirrors no atomic module path",
        ),
        (
            {"manifest": "be/statutes/example/rule.test.json"},
            "mirrors no atomic module path",
        ),
        # The encoder would write be/statutes/.json.json for this module.
        (
            {
                "manifest": "be/statutes/.json",
                "applied": ("be/statutes/.json.yaml",),
                "files": ("be/statutes/.json.yaml",),
            },
            "mirrors no atomic module path",
        ),
        (
            {"applied": (MODULE,), "deleted": (MODULE,)},
            f"both applies and deletes {MODULE}",
        ),
        (
            {"applied": (), "deleted": (MODULE, COMPANION)},
            f"deletes {MODULE} but it still exists",
        ),
    ],
)
def test_a_manifest_the_encoder_would_not_write_is_refused(
    tmp_path: Path, fixture: dict[str, object], problem: str
) -> None:
    write_manifest_fixture(tmp_path, **fixture)
    manifest = fixture.get("manifest", MANIFEST)
    assert encoding_manifest_problems(tmp_path) == [f"{manifest}: {problem}"]


def test_a_directory_at_the_module_path_is_not_the_module(tmp_path: Path) -> None:
    write_manifest_fixture(tmp_path, files=(COMPANION,))
    (tmp_path / MODULE).mkdir()
    assert encoding_manifest_problems(tmp_path) == [f"{MANIFEST}: {MODULE} is missing"]


def test_a_link_left_at_a_deleted_module_path_still_exists(tmp_path: Path) -> None:
    write_manifest_fixture(tmp_path, applied=(), deleted=(MODULE, COMPANION), files=())
    (tmp_path / MODULE).parent.mkdir(parents=True)
    (tmp_path / MODULE).symlink_to(tmp_path / "nowhere.yaml")
    assert encoding_manifest_problems(tmp_path) == [
        f"{MANIFEST}: deletes {MODULE} but it still exists"
    ]


def v5_manifest(applied_files: object) -> bytes:
    return json.dumps(
        {
            "schema_version": APPLIED_ENCODING_MANIFEST_SCHEMA,
            "applied_files": applied_files,
        }
    ).encode()


@pytest.mark.parametrize(
    ("content", "problem"),
    [
        pytest.param(b"{", "is not JSON", id="truncated"),
        pytest.param(b"\x80{}", "is not JSON", id="not-utf-8"),
        pytest.param(
            v5_manifest([{"path": MODULE}]).decode().encode("utf-16"),
            "is not JSON",
            id="utf-16",
        ),
        pytest.param(
            v5_manifest([{"path": MODULE}]).decode().encode("utf-32"),
            "is not JSON",
            id="utf-32",
        ),
        pytest.param(
            b"\xef\xbb\xbf" + v5_manifest([{"path": MODULE}]),
            "is not JSON",
            id="utf-8-bom",
        ),
        # Deep enough that the decoder raises RecursionError.
        pytest.param(b"[" * 1_000_000, "is not JSON", id="deep-nesting"),
        pytest.param(b"[]", "schema None", id="list"),
        pytest.param(
            json.dumps(APPLIED_ENCODING_MANIFEST_SCHEMA).encode(),
            "schema None",
            id="string",
        ),
        pytest.param(
            json.dumps({"schema_version": APPLIED_ENCODING_MANIFEST_SCHEMA}).encode(),
            f"does not list {MODULE}",
            id="no-applied-files",
        ),
        pytest.param(
            v5_manifest({"path": MODULE}),
            f"does not list {MODULE}",
            id="applied-files-object",
        ),
        pytest.param(
            v5_manifest([MODULE]), f"does not list {MODULE}", id="entry-string"
        ),
        pytest.param(
            v5_manifest([{"path": [MODULE]}]),
            f"does not list {MODULE}",
            id="path-list",
        ),
        pytest.param(
            v5_manifest([{"path": {"be": 1}}]),
            f"does not list {MODULE}",
            id="path-object",
        ),
        # As in the encoder, only a literal true marks a file deleted.
        pytest.param(
            v5_manifest([{"path": MODULE, "deleted": "true"}]),
            None,
            id="deleted-string",
        ),
    ],
)
def test_malformed_content_gets_a_line_not_an_exception(
    tmp_path: Path, content: bytes, problem: str | None
) -> None:
    write_manifest_fixture(tmp_path)
    write_raw_manifest(tmp_path, MANIFEST, content)
    expected = [] if problem is None else [f"{MANIFEST}: {problem}"]
    assert encoding_manifest_problems(tmp_path) == expected


def test_a_manifest_path_that_is_not_a_file_gets_a_line(tmp_path: Path) -> None:
    write_manifest_fixture(tmp_path)
    (
        tmp_path / ".axiom" / "encoding-manifests" / "be" / "statutes" / "folder.json"
    ).mkdir()
    (
        tmp_path / ".axiom" / "encoding-manifests" / "be" / "statutes" / "dangling.json"
    ).symlink_to(tmp_path / "nowhere.json")
    assert encoding_manifest_problems(tmp_path) == [
        "be/statutes/dangling.json: is not a readable file",
        "be/statutes/folder.json: is not a readable file",
    ]


@pytest.mark.parametrize("jurisdiction", BELGIAN_JURISDICTIONS)
@pytest.mark.parametrize("kind", ["directory", "file", "dangling symlink"])
def test_a_manifest_root_inside_any_jurisdiction_is_refused(
    tmp_path: Path, jurisdiction: str, kind: str
) -> None:
    write_manifest_fixture(tmp_path)
    nested = tmp_path / jurisdiction / ".axiom" / "encoding-manifests"
    nested.parent.mkdir(parents=True)
    if kind == "directory":
        nested.mkdir()
    elif kind == "file":
        nested.write_text("{}\n")
    else:
        nested.symlink_to(tmp_path / "nowhere")
    assert encoding_manifest_problems(tmp_path) == [
        f"co-located manifest root: {jurisdiction}/.axiom/encoding-manifests"
    ]


def test_problems_do_not_depend_on_the_order_the_filesystem_lists_files(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    write_manifest_fixture(tmp_path)
    for jurisdiction in BELGIAN_JURISDICTIONS:
        (tmp_path / jurisdiction / ".axiom" / "encoding-manifests").mkdir(parents=True)
    for name in ("a", "m", "z"):
        write_raw_manifest(tmp_path, f"be/statutes/{name}/rule.json", b"{")
    listed = encoding_manifest_problems(tmp_path)
    assert listed == [
        *(
            f"co-located manifest root: {name}/.axiom/encoding-manifests"
            for name in BELGIAN_JURISDICTIONS
        ),
        *(f"be/statutes/{name}/rule.json: is not JSON" for name in ("a", "m", "z")),
    ]
    iterdir, rglob = Path.iterdir, Path.rglob
    monkeypatch.setattr(
        Path, "iterdir", lambda self: iter(sorted(iterdir(self), reverse=True))
    )
    monkeypatch.setattr(
        Path,
        "rglob",
        lambda self, *args, **kwargs: iter(
            sorted(rglob(self, *args, **kwargs), reverse=True)
        ),
    )
    assert encoding_manifest_problems(tmp_path) == listed


def write_pinned_encoder(root: Path, encoder_ref: str) -> None:
    """Write the one repository-checks.yml field pinned_encoder_ref reads."""
    workflow = root / ".github" / "workflows" / "repository-checks.yml"
    workflow.parent.mkdir(parents=True, exist_ok=True)
    workflow.write_text(
        yaml.safe_dump(
            {"jobs": {"validate": {"with": {"axiom-encode-ref": encoder_ref}}}}
        )
    )


# A change that adds only this manifest names an existing module and carries
# no signature, file hashes or producer.
UNSIGNED_MODULE = "be/policies/euromod_benefit_income_list.yaml"
UNSIGNED_MANIFEST = "be/policies/euromod_benefit_income_list.json"
UNSIGNED_CONTENT = (
    b'{"schema_version":"axiom-encode/applied-rulespec/v5",'
    b'"applied_files":[{"path":"be/policies/euromod_benefit_income_list.yaml"}]}'
)


def write_unsigned_manifest_only_change(root: Path, encoder_ref: str) -> None:
    write_manifest_fixture(
        root,
        manifest=UNSIGNED_MANIFEST,
        applied=(UNSIGNED_MODULE,),
        files=(UNSIGNED_MODULE, UNSIGNED_MODULE.replace(".yaml", ".test.yaml")),
    )
    write_raw_manifest(root, UNSIGNED_MANIFEST, UNSIGNED_CONTENT)
    write_pinned_encoder(root, encoder_ref)


@pytest.mark.parametrize(
    "encoder_ref", sorted(SKIPPING_ENCODER_PIN_HISTORY)
)
def test_an_unsigned_manifest_is_refused_while_the_guard_skips_it(
    tmp_path: Path, encoder_ref: str
) -> None:
    write_unsigned_manifest_only_change(tmp_path, encoder_ref)
    # The placement check admits it; the pin check is what refuses it.
    assert encoding_manifest_problems(tmp_path) == []
    assert manifests_the_guard_skips(tmp_path) == [
        f"{UNSIGNED_MANIFEST}: the pinned encoder {encoder_ref[:8]} does not "
        "verify a change that adds only manifests"
    ]


@pytest.mark.parametrize(
    "encoder_ref", [FIRST_ENCODER_THAT_CHECKS_MANIFEST_ONLY_CHANGES, "f" * 40]
)
def test_an_unlisted_encoder_leaves_manifests_to_the_guard(
    tmp_path: Path, encoder_ref: str
) -> None:
    write_unsigned_manifest_only_change(tmp_path, encoder_ref)
    assert manifests_the_guard_skips(tmp_path) == []


@pytest.mark.parametrize(
    "encoder_ref", sorted(ENCODERS_THAT_SKIP_MANIFEST_ONLY_CHANGES)
)
def test_every_manifest_gets_a_line_while_the_guard_skips_them(
    tmp_path: Path, encoder_ref: str
) -> None:
    write_manifest_fixture(tmp_path)
    contents = {
        "be/statutes/a/rule.json": b"{",
        "be/statutes/m/rule.json": json.dumps(
            {"schema_version": "axiom-encode/applied-rulespec/v1"}
        ).encode(),
        "be-vlg/statutes/z/rule.json": v5_manifest([{"path": MODULE}]),
    }
    for manifest, content in contents.items():
        write_raw_manifest(tmp_path, manifest, content)
    write_pinned_encoder(tmp_path, encoder_ref)
    assert manifests_the_guard_skips(tmp_path) == [
        f"{manifest}: the pinned encoder {encoder_ref[:8]} does not verify a "
        "change that adds only manifests"
        # The check sorts paths part by part, which puts be/ before be-vlg/.
        for manifest in sorted([MANIFEST, *contents], key=lambda name: Path(name).parts)
    ]


def test_a_tree_without_manifests_passes_while_the_guard_skips_them(
    tmp_path: Path,
) -> None:
    write_pinned_encoder(tmp_path, sorted(ENCODERS_THAT_SKIP_MANIFEST_ONLY_CHANGES)[0])
    assert manifests_the_guard_skips(tmp_path) == []


def test_workflow_toolchain_mirrors_the_validation_workflow() -> None:
    """workflow-toolchain.toml repeats the checkout refs repository-checks.yml pins.

    axiom-encode's signed re-encode workflow reads only an optional
    axiom_compose_ref from this file, so the refs here are a record, kept
    equal to the ones CI runs.
    """
    pins = tomllib.loads((ROOT / ".axiom/workflow-toolchain.toml").read_text())
    assert set(pins) == {"workflow_toolchain"}
    table = pins["workflow_toolchain"]
    workflow = yaml.safe_load(
        (ROOT / ".github/workflows/repository-checks.yml").read_text()
    )
    job = workflow["jobs"]["validate"]
    uses_path, _, uses_ref = job["uses"].rpartition("@")
    assert uses_path == "TheAxiomFoundation/.github/.github/workflows/validate-rulespec.yml"
    inputs = job["with"]
    actual = {
        "axiom_encode_ref": inputs["axiom-encode-ref"],
        "axiom_rules_engine_ref": inputs["axiom-rules-engine-ref"],
        "axiom_corpus_ref": inputs["axiom-corpus-ref"],
        "rulespec_us_ref": inputs["rulespec-us-ref"],
        "shared_workflow_ref": uses_ref,
    }
    # No axiom_compose_ref: axiom-compose stays disabled here.
    assert "axiom-compose-ref" not in inputs
    assert set(table) == set(actual)
    for key, value in actual.items():
        assert isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value), key
        assert table[key] == value, key


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

    assert missing == []


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

    assert invalid == []


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

    assert missing == []


def test_policy_parameter_proof_atoms_anchor_formula_values() -> None:
    """Every policy-bearing parameter proof atom must anchor a corpus provision.

    A rule-level atom may cite an independently operative provision instead of
    repeating the module's single review anchor. It must use a canonical corpus
    citation path and carry a non-empty exact anchor quote.
    """
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
                atom_path = atom.get("path")
                formula_path_match = (
                    FORMULA_PROOF_PATH_RE.fullmatch(atom_path)
                    if isinstance(atom_path, str)
                    else None
                )
                values_path_match = (
                    VALUES_PROOF_PATH_RE.fullmatch(atom_path)
                    if isinstance(atom_path, str)
                    else None
                )
                if formula_path_match is not None:
                    version_index = int(formula_path_match.group(1))
                    versions = rule.get("versions")
                    if (
                        not isinstance(versions, list)
                        or version_index >= len(versions)
                    ):
                        invalid.append(
                            f"{atom_id}: atom anchors missing version {version_index}"
                        )
                    if atom.get("kind") != "parameter":
                        invalid.append(f"{atom_id}: atom kind must be parameter")
                elif values_path_match is not None:
                    # A parameter table anchors `versions[i].values` (its cells)
                    # with `kind: parameter_table` — the same contract the
                    # money-atom gate derives (axiom-encode#1032).
                    version_index = int(values_path_match.group(1))
                    if not rule_version_is_parameter_table(rule, version_index):
                        invalid.append(
                            f"{atom_id}: atom anchors versions[{version_index}].values "
                            "but that version is not a parameter table"
                        )
                    if atom.get("kind") != "parameter_table":
                        invalid.append(
                            f"{atom_id}: table atom kind must be parameter_table"
                        )
                else:
                    invalid.append(
                        f"{atom_id}: atom must anchor versions[N].formula "
                        "(or versions[N].values for a parameter table)"
                    )
                if not isinstance(citation_path, str) or not citation_path:
                    invalid.append(f"{atom_id}: missing corpus_citation_path")
                elif CORPUS_CITATION_PATH_RE.fullmatch(citation_path) is None:
                    invalid.append(
                        f"{atom_id}: invalid corpus_citation_path {citation_path!r}"
                    )
                if proof_atom_anchor_text(source) is None:
                    invalid.append(f"{atom_id}: missing exact source excerpt")

    assert invalid == []


def test_policy_parameter_proof_excerpts_contain_formula_values() -> None:
    """A parameter's exact proof excerpt must contain its encoded value."""
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
                excerpt = proof_atom_anchor_text(source)
                if excerpt is None:
                    continue
                excerpt_values = text_number_values(excerpt)
                if not excerpt_contains_formula_value(
                    formula_values, excerpt_values, excerpt
                ):
                    invalid.append(
                        f"{path.relative_to(ROOT).as_posix()}#{name}.atoms[{index}]"
                    )

    assert invalid == []


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

    assert missing == []
