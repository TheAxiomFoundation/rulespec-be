from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
QUEUE_PATH = ROOT / ".axiom/be-documentary-reencoding-queue.v1.json"
ATOMIC_ROOTS = {"legislation", "policies", "regulations", "statutes"}
HOLD_PATHS = {
    "be/regulations/vat/rates.yaml",
    "be/statutes/income_tax/individual/regional_surcharge.yaml",
    "be/statutes/property_tax/additional_centimes.yaml",
    "be/statutes/social_security/chapter_10_special_contributions.yaml",
    "be/statutes/social_security/workers/contribution_rates.yaml",
}
CLEANUP_PATHS = {
    "be/policies/euromod_benefit_income_list.yaml",
    "be/policies/euromod_disposable_income_list.yaml",
    "be/policies/euromod_tax_income_list.yaml",
    "be/regulations/unemployment/payable_amount.yaml",
    "be/regulations/unemployment/pilot_oracle_pipeline.yaml",
    "be/statutes/education/study_allowance_routing.yaml",
    "be/statutes/family_benefits/birth_allowance.yaml",
    "be/statutes/family_benefits/child_benefit_base_2025.yaml",
    "be/statutes/family_benefits/regional_routing.yaml",
    "be/statutes/gift_tax/regional_routing.yaml",
    "be/statutes/income_guarantee_for_elderly/payable_amount.yaml",
    "be/statutes/income_tax/individual/couple_pit_oracle_pipeline.yaml",
    "be/statutes/income_tax/individual/pensioner_pit_oracle_pipeline.yaml",
    "be/statutes/income_tax/individual/pilot_worker_oracle_pipeline.yaml",
    "be/statutes/income_tax/individual/self_employed_oracle_pipeline.yaml",
    "be/statutes/inheritance_tax/regional_routing.yaml",
    "be/statutes/property_tax/gross_withholding_and_supplied_centimes.yaml",
    "be/statutes/property_tax/regional_routing.yaml",
    "be/statutes/social_integration/payable_amount.yaml",
    "be/statutes/social_security/pension_health_insurance_article_191.yaml",
    "be/statutes/social_security/pension_solidarity_article_68.yaml",
    "be/statutes/vehicle_tax/regional_routing.yaml",
}
FORBIDDEN_CANDIDATE_IDENTITY_RE = re.compile(
    r"(?:euromod|comparator|oracle(?:s)?|take[_ -]?up|takeup|propensity|"
    r"elasticit|random|behavio(?:u)?r|latent[ _-]?population)",
    flags=re.IGNORECASE,
)


def load_queue() -> dict:
    return json.loads(QUEUE_PATH.read_text(encoding="utf-8"))


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def canonical_record_list_sha256(records: list[dict]) -> str:
    raw = json.dumps(
        records,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return sha256(raw)


def nul_v1_path_set_sha256(paths: set[str]) -> str:
    return sha256(b"\0".join(path.encode("utf-8") for path in sorted(paths)))


def current_primary_paths() -> set[str]:
    result: set[str] = set()
    for jurisdiction in ROOT.iterdir():
        if not jurisdiction.is_dir() or not jurisdiction.name.startswith("be"):
            continue
        for atomic_root in ATOMIC_ROOTS:
            root = jurisdiction / atomic_root
            if not root.is_dir():
                continue
            result.update(
                path.relative_to(ROOT).as_posix()
                for path in root.rglob("*.yaml")
                if not path.name.endswith(".test.yaml")
            )
    return result


def dependency_paths_from_payload(payload: object) -> set[str]:
    if not isinstance(payload, dict):
        return set()
    result: set[str] = set()
    for raw_import in payload.get("imports") or []:
        assert isinstance(raw_import, str)
        module = raw_import.split("#", 1)[0]
        jurisdiction, relative = module.split(":", 1)
        result.add(f"{jurisdiction}/{relative}.yaml")
    return result


def module_dependency_paths(path: str) -> set[str]:
    payload = yaml.safe_load((ROOT / path).read_text(encoding="utf-8")) or {}
    return dependency_paths_from_payload(payload)


def frozen_module_dependency_paths(ref: str, path: str) -> set[str]:
    raw = run_git("cat-file", "blob", f"{ref}:{path}").stdout
    try:
        payload = yaml.safe_load(raw.decode("utf-8")) or {}
    except (UnicodeDecodeError, yaml.YAMLError) as exc:
        raise AssertionError(
            f"frozen RuleSpec is not valid UTF-8 YAML: {ref}:{path}"
        ) from exc
    return dependency_paths_from_payload(payload)


def companion_path(path: str) -> str:
    assert path.endswith(".yaml")
    return f"{path[:-5]}.test.yaml"


def manifest_path(path: str) -> str:
    assert path.endswith(".yaml")
    return f".axiom/encoding-manifests/{path[:-5]}.json"


def run_git(
    *args: str, allow_failure: bool = False
) -> subprocess.CompletedProcess[bytes]:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=20,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise AssertionError(
            f"bounded git command timed out: git {' '.join(args)}"
        ) from exc
    if not allow_failure and result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        raise AssertionError(
            f"required Git object is unavailable: git {' '.join(args)}: {stderr}"
        )
    assert len(result.stdout) <= 16 * 1024 * 1024, (
        f"bounded git output exceeded 16 MiB: git {' '.join(args)}"
    )
    return result


def git_tree_entries(ref: str) -> dict[str, tuple[str, str, str]]:
    entries: dict[str, tuple[str, str, str]] = {}
    raw = run_git("ls-tree", "-r", "-z", ref).stdout
    for record in raw.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, kind, oid = metadata.decode("ascii").split(" ")
        entries[raw_path.decode("utf-8")] = (mode, kind, oid)
    return entries


def assert_git_blob_evidence(
    *,
    entries: dict[str, tuple[str, str, str]],
    path: str,
    expected: list[str],
) -> None:
    assert path in entries, f"required frozen Git path is unavailable: {path}"
    mode, kind, oid = entries[path]
    assert (mode, kind) == ("100644", "blob"), (
        f"frozen path is not a regular 0644 blob: {path}: {mode} {kind}"
    )
    raw = run_git("cat-file", "blob", oid).stdout
    assert expected == [oid, sha256(raw)]


def exact_corpus_root(queue: dict) -> Path:
    configured = os.environ.get("AXIOM_CORPUS_REPO")
    candidates = [Path(configured)] if configured else []
    candidates.append(ROOT / "_axiom/axiom-corpus")
    corpus = next((path for path in candidates if path.is_dir()), None)
    assert corpus is not None, (
        "exact corpus checkout unavailable; set AXIOM_CORPUS_REPO or provide "
        "ROOT/_axiom/axiom-corpus at the queue's pinned commit"
    )
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=corpus,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=20,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise AssertionError("bounded corpus Git identity check timed out") from exc
    assert result.returncode == 0, (
        "exact corpus checkout is not a readable Git checkout: "
        + result.stderr.decode("utf-8", errors="replace").strip()
    )
    actual = result.stdout.decode("ascii").strip()
    assert actual == queue["toolchain"]["corpus"]["commit"], (
        f"corpus checkout is at {actual}, expected "
        f"{queue['toolchain']['corpus']['commit']}"
    )
    return corpus


def test_queue_is_non_authoritative_and_binds_the_exact_frozen_census() -> None:
    queue = load_queue()
    census = queue["census"]
    candidates = {item["path"] for item in queue["candidates"]}
    cleanup = {item["path"] for item in queue["cleanup"]["groups"]}
    holds = {item["path"] for item in queue["holds"]}

    assert queue["schema_version"] == "rulespec-be/documentary-reencoding-plan/v1"
    assert queue["authority"] == "non-authoritative-review-only"
    assert queue["state"] == "blocked_prerequisites_no_execution_authority"
    assert census["repository"] == "https://github.com/TheAxiomFoundation/rulespec-be"
    assert census["pull_request"] == 127
    assert census["lineage_root_commit"] == ("b105e2b3a3086ddd2de447d58a9b951346870dd1")
    assert census["lineage_root_tree"] == ("4723792ae1752ffc33727ad8f34a280d526be59b")
    assert census["review_head_commit"] == ("9aa9ee19d750fa0ac8aa7a02d9c1006c4240cb07")
    assert census["review_head_tree"] == ("b08cfbf4b8c2b13a5298d0b5fb793c9c825e7fab")
    assert census["counts"] == {
        "admitted": 0,
        "base_groups": 116,
        "cleanup_groups": 22,
        "documentary_candidates": 89,
        "holds": 5,
    }
    assert len(candidates) == 89
    assert cleanup == CLEANUP_PATHS
    assert holds == HOLD_PATHS
    assert candidates.isdisjoint(cleanup | holds)
    assert cleanup.isdisjoint(holds)
    assert len(candidates | cleanup | holds) == 116
    assert census["candidate_set_sha256_nul_v1"] == nul_v1_path_set_sha256(candidates)
    assert census["cleanup_set_sha256_nul_v1"] == nul_v1_path_set_sha256(cleanup)
    assert census["hold_set_sha256_nul_v1"] == nul_v1_path_set_sha256(holds)


def test_queue_record_digests_are_canonical_and_reproducible() -> None:
    queue = load_queue()

    assert queue["candidate_records_sha256"] == canonical_record_list_sha256(
        queue["candidates"]
    )
    assert queue["cleanup_records_sha256"] == canonical_record_list_sha256(
        queue["cleanup"]["groups"]
    )
    assert queue["hold_records_sha256"] == canonical_record_list_sha256(queue["holds"])
    assert queue["source_pin_records_sha256"] == canonical_record_list_sha256(
        queue["source_pins"]
    )
    assert [item["path"] for item in queue["candidates"]] == sorted(
        item["path"] for item in queue["candidates"]
    )
    assert [item["path"] for item in queue["cleanup"]["groups"]] == sorted(
        item["path"] for item in queue["cleanup"]["groups"]
    )
    assert [item["citation"] for item in queue["source_pins"]] == sorted(
        item["citation"] for item in queue["source_pins"]
    )


def test_review_tree_is_exactly_candidates_plus_unchanged_excluded_holds() -> None:
    queue = load_queue()
    candidates = {item["path"] for item in queue["candidates"]}
    holds = {item["path"] for item in queue["holds"]}

    assert current_primary_paths() == candidates | holds
    for hold in queue["holds"]:
        assert hold["excluded"] is True
        primary = ROOT / hold["path"]
        companion = ROOT / companion_path(hold["path"])
        assert sha256(primary.read_bytes()) == hold["review_head_primary"][1]
        assert sha256(companion.read_bytes()) == hold["review_head_companion"][1]

    queued_paths = {
        path
        for step in queue["protected_sequence"]
        for path in step.get("paths", step.get("groups", []))
    }
    assert holds.isdisjoint(queued_paths)


def test_frozen_rule_groups_are_authenticated_against_git_objects() -> None:
    queue = load_queue()
    census = queue["census"]
    base = census["lineage_root_commit"]
    head = census["review_head_commit"]

    run_git("cat-file", "-e", f"{base}^{{commit}}")
    run_git("cat-file", "-e", f"{head}^{{commit}}")
    assert (
        run_git("rev-parse", f"{base}^{{tree}}").stdout.decode().strip()
        == census["lineage_root_tree"]
    )
    assert (
        run_git("rev-parse", f"{head}^{{tree}}").stdout.decode().strip()
        == census["review_head_tree"]
    )
    base_entries = git_tree_entries(base)
    head_entries = git_tree_entries(head)

    for item in [*queue["candidates"], *queue["cleanup"]["groups"], *queue["holds"]]:
        path = item["path"]
        test_path = companion_path(path)
        assert_git_blob_evidence(
            entries=base_entries,
            path=path,
            expected=item["base_primary"],
        )
        assert_git_blob_evidence(
            entries=base_entries,
            path=test_path,
            expected=item["base_companion"],
        )
        if item["review_head_present"]:
            assert_git_blob_evidence(
                entries=head_entries,
                path=path,
                expected=item["review_head_primary"],
            )
            assert_git_blob_evidence(
                entries=head_entries,
                path=test_path,
                expected=item["review_head_companion"],
            )
            assert sha256((ROOT / path).read_bytes()) == item["review_head_primary"][1]
            assert (
                sha256((ROOT / test_path).read_bytes())
                == item["review_head_companion"][1]
            )
            if "review_changed" in item:
                expected_changed: list[str] = []
                if item["base_primary"] != item["review_head_primary"]:
                    expected_changed.append("primary")
                if item["base_companion"] != item["review_head_companion"]:
                    expected_changed.append("companion")
                assert item["review_changed"] == expected_changed
        else:
            assert path not in head_entries
            assert test_path not in head_entries


def test_every_source_pin_is_authenticated_against_exact_corpus_bytes() -> None:
    queue = load_queue()
    corpus = exact_corpus_root(queue)
    pins = {item["citation"]: item for item in queue["source_pins"]}
    candidate_paths_by_citation: dict[str, list[str]] = {}
    for candidate in queue["candidates"]:
        candidate_paths_by_citation.setdefault(candidate["citation"], []).append(
            candidate["path"]
        )
    candidate_paths_by_citation = {
        citation: sorted(paths)
        for citation, paths in candidate_paths_by_citation.items()
    }
    artifact_hashes = queue["toolchain"]["corpus_artifact_sha256"]
    corpus_contract = queue["toolchain"]["corpus"]

    selector = corpus / corpus_contract["selector"]
    assert selector.is_file(), f"pinned corpus selector is unavailable: {selector}"
    selector_raw = selector.read_bytes()
    assert sha256(selector_raw) == corpus_contract["selector_sha256"]
    selector_payload = json.loads(selector_raw)
    assert selector_payload["name"] == corpus_contract["release"]
    expected_artifacts = {
        "data/corpus/provisions/"
        f"{scope['jurisdiction']}/{scope['document_class']}/{scope['version']}.jsonl"
        for scope in selector_payload["scopes"]
    }
    assert len(expected_artifacts) == corpus_contract["scope_count"] == 13
    assert expected_artifacts == artifact_hashes.keys()

    rows_by_artifact: dict[str, list[dict]] = {}
    citation_counts: dict[str, int] = {}
    for artifact, expected_sha in artifact_hashes.items():
        artifact_path = corpus / artifact
        assert artifact_path.is_file(), (
            f"pinned corpus artifact unavailable: {artifact}"
        )
        raw = artifact_path.read_bytes()
        assert len(raw) <= 16 * 1024 * 1024, (
            f"corpus artifact exceeds bound: {artifact}"
        )
        assert sha256(raw) == expected_sha
        rows = [json.loads(line) for line in raw.splitlines()]
        rows_by_artifact[artifact] = rows
        for row in rows:
            citation = row.get("citation_path")
            if isinstance(citation, str):
                citation_counts[citation] = citation_counts.get(citation, 0) + 1

    assert (
        sum(len(rows) for rows in rows_by_artifact.values())
        == corpus_contract["row_count"]
        == 626
    )

    assert len(queue["source_pins"]) == len(pins) == 78
    assert len(queue["candidates"]) == 89
    assert pins.keys() == candidate_paths_by_citation.keys()
    for pin in pins.values():
        expected_candidate_paths = candidate_paths_by_citation[pin["citation"]]
        assert pin["candidate_paths"] == expected_candidate_paths
        assert pin["candidate_count"] == len(expected_candidate_paths)
        assert citation_counts[pin["citation"]] == 1
        rows = rows_by_artifact[pin["artifact"]]
        assert 1 <= pin["line"] <= len(rows)
        row = rows[pin["line"] - 1]
        assert row["citation_path"] == pin["citation"]
        assert row["id"] == pin["record_id"]
        assert row["source_path"] == pin["source_path"]
        assert row["source_as_of"] == pin["source_as_of"]
        assert row["expression_date"] == pin["expression_date"]
        assert isinstance(row["body"], str) and row["body"].strip()
        assert sha256(row["body"].encode("utf-8")) == pin["body_sha256"]

    for candidate in queue["candidates"]:
        pin = pins[candidate["citation"]]
        assert candidate["expected_source_body_sha256"] == pin["body_sha256"]
        assert candidate["source_record_id"] == pin["record_id"]
        payload = yaml.safe_load((ROOT / candidate["path"]).read_text(encoding="utf-8"))
        verification = payload["module"]["source_verification"]
        assert verification["corpus_citation_path"] == candidate["citation"]
        assert "source_sha256" not in verification


def test_transition_graph_is_closed_acyclic_and_exactly_layered() -> None:
    queue = load_queue()
    candidates = {item["path"]: item for item in queue["candidates"]}
    cleanup = {item["path"] for item in queue["cleanup"]["groups"]}
    holds = {item["path"] for item in queue["holds"]}
    predecessors = {path: set() for path in candidates}
    base_ref = queue["census"]["lineage_root_commit"]
    removed: set[tuple[str, str]] = set()
    review_added: set[tuple[str, str]] = set()

    for path, item in candidates.items():
        desired = set(item["documentary_dependencies"])
        base_dependencies = frozen_module_dependency_paths(base_ref, path)
        assert set(item["base_dependencies"]) == base_dependencies
        assert desired == module_dependency_paths(path)
        assert desired <= candidates.keys()
        assert desired.isdisjoint(cleanup | holds)
        actual_removed = base_dependencies - desired
        actual_added = desired - base_dependencies
        assert set(item["removed_legacy_dependencies"]) == actual_removed
        assert set(item["review_added_dependencies"]) == actual_added
        removed.update((path, producer) for producer in actual_removed)
        review_added.update((path, producer) for producer in actual_added)
        predecessors[path].update(desired)
        citation_jurisdiction = item["citation"].split("/", 1)[0]
        assert set(item["required_import_rulespec_paths"]) == {
            dependency
            for dependency in desired
            if dependency.split("/", 1)[0] == citation_jurisdiction
        }
        assert set(item["cross_jurisdiction_dependencies"]) == {
            dependency
            for dependency in desired
            if dependency.split("/", 1)[0] != citation_jurisdiction
        }

    assert len(removed) == 3
    assert review_added == set()
    for consumer, producer in removed:
        assert producer in candidates
        predecessors[producer].add(consumer)

    assert all(
        set(candidates[path]["transition_predecessors"]) == expected
        for path, expected in predecessors.items()
    )

    remaining = set(candidates)
    layers: list[set[str]] = []
    while remaining:
        layer = {path for path in remaining if predecessors[path].isdisjoint(remaining)}
        assert layer, "transition graph contains a cycle"
        layers.append(layer)
        remaining -= layer
    assert [len(layer) for layer in layers] == [69, 14, 4, 1, 1]


def test_protected_sequence_covers_each_candidate_once_with_disjoint_waves() -> None:
    queue = load_queue()
    candidates = {item["path"]: item for item in queue["candidates"]}
    pre_cleanup_path = queue["pre_cleanup"]["protected_reencode_path"]
    wave_paths: list[str] = []

    assert pre_cleanup_path == "be-wal/statutes/family_benefits/amounts.yaml"
    assert candidates[pre_cleanup_path]["phase"] == "pre_cleanup"
    assert (
        queue["pre_cleanup"]["minimum_standard_write_set"]
        == candidates[pre_cleanup_path]["standard_write_set"]
    )
    assert [(wave["wave"], wave["candidate_count"]) for wave in queue["waves"]] == [
        (1, 68),
        (2, 14),
        (3, 4),
        (4, 1),
        (5, 1),
    ]

    for index, wave in enumerate(queue["waves"], start=1):
        expected = sorted(
            path
            for path, item in candidates.items()
            if item["phase"] == "post_cleanup" and item["wave"] == index
        )
        assert wave["candidates"] == expected
        assert wave["base"] == f"F{index}"
        assert wave["freeze_as"] == f"F{index + 1}"
        write_sets = [
            set(candidates[path]["standard_write_set"]) for path in wave["candidates"]
        ]
        assert all(
            left.isdisjoint(right)
            for left_index, left in enumerate(write_sets)
            for right in write_sets[left_index + 1 :]
        )
        wave_paths.extend(wave["candidates"])

    assert len(wave_paths) == len(set(wave_paths)) == 88
    assert set(wave_paths) | {pre_cleanup_path} == candidates.keys()
    for path, item in candidates.items():
        assert item["standard_write_set"] == [
            path,
            companion_path(path),
            manifest_path(path),
        ]


def test_cleanup_is_blocked_until_the_exact_pre_cleanup_sequence_succeeds() -> None:
    queue = load_queue()
    pre_cleanup = queue["pre_cleanup"]
    cleanup = queue["cleanup"]

    assert pre_cleanup["surviving_reference_paths"] == [
        "be-wal/statutes/family_benefits/amounts.yaml",
        "data/coverage/euromod-be-coverage.json",
        "data/coverage/pilot-slice-coverage.json",
        "data/coverage/tax-benefit-source-map.json",
        "docs/ENCODING-GAPS.md",
    ]
    assert cleanup["status"] == "blocked_until_f_cleanup"
    assert cleanup["required_base_commit"] is None
    assert cleanup["required_base_symbol"] == "F_cleanup"
    assert cleanup["must_run_under_trusted_supervisor"] is True
    assert cleanup["cli"][0:2] == [
        "/opt/axiom/python/bin/axiom-encode",
        "cleanup-unmanifested-legacy",
    ]
    cli_cleanup_paths = set(cleanup["cli"][2 : 2 + len(CLEANUP_PATHS)])
    assert cli_cleanup_paths == CLEANUP_PATHS
    assert queue["earliest_batches"]["first_protected_operation"] == [
        "be-wal/statutes/family_benefits/amounts.yaml"
    ]
    assert queue["earliest_batches"]["first_post_cleanup_bounded_tranche"] == [
        "be-vlg/regulations/employment/jobbonus.yaml",
        "be-vlg/statutes/education/school_allowance.yaml",
        "be-vlg/statutes/education/study_grant.yaml",
        "be/regulations/social_security/self_employed/contributions.yaml",
        "be/statutes/social_security/non_labour_income_contributions.yaml",
    ]


def test_axiom_queue_excludes_behavior_population_and_external_model_concepts() -> None:
    queue = load_queue()
    candidates = queue["candidates"]

    assert queue["concept_boundary"]["forbidden_atomic_categories"] == [
        "take-up mechanics",
        "observed participation flags",
        "behavioral propensities",
        "labor-supply elasticities",
        "random assignment",
        "latent population variables",
        "external-model or oracle outputs",
        "calibration targets",
    ]
    assert queue["proof_summary"]["behavior_or_population_concepts_authorized"] is False
    assert all(
        FORBIDDEN_CANDIDATE_IDENTITY_RE.search(item["path"]) is None
        for item in candidates
    )
    assert all(
        FORBIDDEN_CANDIDATE_IDENTITY_RE.search(item["citation"]) is None
        for item in candidates
    )
    assert not any(
        path in CLEANUP_PATHS for wave in queue["waves"] for path in wave["candidates"]
    )


def test_toolchain_and_commands_remain_fail_closed_until_frozen() -> None:
    queue = load_queue()
    toolchain = queue["toolchain"]
    command = queue["command_contract"]

    assert toolchain["corpus"]["commit"] == ("644ee891c69b4632b0ce48d5432a6104df255571")
    assert toolchain["corpus"]["release_content_sha256"] == (
        "c1436c9f99882a819773bc2ccddf8c2a67e41efd24b0d0a408493ba5da39964a"
    )
    assert toolchain["rules_engine_commit"] == (
        "05eac9d2f89dabe5c6673176260762cef3a58f47"
    )
    assert toolchain["waiver_sha256"] == (
        "904514a87f353e22767a3de186257675eacd99a496b71ca35052b9e9aa14543f"
    )
    assert toolchain["required_execution_encoder_version"] == "0.2.1753"
    assert toolchain["required_execution_encoder_commit"] is None
    assert toolchain["reusable_workflow"]["required_compatible_commit"] is None
    assert command["status"] == (
        "non_executable_until_final_encoder_and_workflow_commits_are_frozen"
    )
    assert "--apply" in command["reencode_cli"]
    assert "--review-contract-json" in command["reencode_cli"]
    assert not set(command["forbidden_flags"]) & set(command["reencode_cli"])
    assert "--review-contract-json" in command["review_contract_requirement"]


def test_cross_jurisdiction_composition_and_documentary_holds_stay_blocked() -> None:
    queue = load_queue()
    candidates = {item["path"]: item for item in queue["candidates"]}
    elderly = candidates["be-bru/statutes/disability/elderly_care_allowance.yaml"]

    assert elderly["cross_jurisdiction_dependencies"] == [
        "be/statutes/disability/allowances.yaml"
    ]
    assert elderly["required_import_rulespec_paths"] == []
    assert elderly["status"] == "blocked_cross_jurisdiction_import_contract"
    assert (
        candidates["be-wal/statutes/education/study_allowance.yaml"]["status"]
        == "blocked_documentary_decision"
    )
    assert (
        candidates["be-bru/statutes/family_benefits/selected_amount.yaml"]["status"]
        == "blocked_documentary_decision"
    )
    assert (
        candidates["be-bru/statutes/family_benefits/eligibility.yaml"]["status"]
        == "blocked_upstream_documentary_decision"
    )
