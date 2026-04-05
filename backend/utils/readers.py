from __future__ import annotations

import json
import tomllib

from utils.constants import WORKSPACE_ROOT


def read_pyproject() -> dict:
    """Load and return the parsed backend/pyproject.toml."""
    path = WORKSPACE_ROOT / "backend" / "pyproject.toml"
    with open(path, "rb") as f:
        return tomllib.load(f)


def read_package_json() -> dict:
    """Load and return the parsed frontend/package.json."""
    path = WORKSPACE_ROOT / "frontend" / "package.json"
    with open(path) as f:
        return json.load(f)


def parse_python_deps(pyproject: dict) -> dict[str, str]:
    """Return {normalized_name: version} extracted from pyproject.toml dependencies."""
    deps: dict[str, str] = {}
    for dep in pyproject.get("project", {}).get("dependencies", []):
        for op in ("==", ">=", "<=", "~=", "!="):
            if op in dep:
                name, version = dep.split(op, 1)
                name = name.split("[")[0].strip().lower()
                deps[name] = version.strip()
                break
        else:
            deps[dep.strip().lower()] = "*"
    return deps
