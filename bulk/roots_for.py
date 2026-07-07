#!/usr/bin/env python3
"""Print the guard-generated `--roots` for an applied module path.

`axiom-encode guard-generated --roots` wants the space-separated jurisdiction
roots that the changed files live under. A bulk job touches exactly one
jurisdiction directory plus (defensively) the federal `be` root, matching how
the org validate workflow scopes a single-jurisdiction change. rulespec-be is a
federal + regional monorepo: the federal root is `be`; the regional roots are
`be-bru`, `be-dg`, `be-vlg`, `be-wal`.

Usage:
  python bulk/roots_for.py be/statutes/employment/guaranteed_salary.yaml   # -> "be"
  python bulk/roots_for.py be-vlg/statutes/family/x.yaml                   # -> "be be-vlg"
"""

from __future__ import annotations

import sys
from pathlib import PurePosixPath


def roots_for(module_path: str) -> str:
    parts = PurePosixPath(module_path).parts
    if not parts:
        return "be"
    juris = parts[0]
    # Always include the federal root so cross-jurisdiction imports resolve;
    # include the module's own jurisdiction when it is a regional directory.
    roots = ["be"]
    if juris != "be" and juris.startswith("be-"):
        roots.append(juris)
    return " ".join(dict.fromkeys(roots))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: roots_for.py <module-path>", file=sys.stderr)
        raise SystemExit(2)
    print(roots_for(sys.argv[1]))
