"""
Template Reference MCP Server
==============================
Provides tools for inspecting, auditing, and repairing projects that were
bootstrapped from this template.

Run:
    uv run fastmcp run server.py:mcp --transport streamable-http --port 8001
"""

from __future__ import annotations

import asyncio
import json
import tomllib
from pathlib import Path
from typing import Literal

import httpx
from fastmcp import FastMCP

mcp = FastMCP("Template Reference MCP 🚀")

# ── Workspace root (two levels up from this file: backend/ → app-template/) ──
WORKSPACE_ROOT = Path(__file__).parent.parent

# ── Template baseline ─────────────────────────────────────────────────────────
# Snapshot of the original template's expected state.
# Update these values whenever the template itself changes.
TEMPLATE_BASELINE: dict = {
    "python_version": "3.14",
    "backend": {
        "fastapi[standard]": "0.135.3",
        "fastmcp": "3.2.0",
        "httpx": "0.28.1",
        "ruff": "0.15.9",
    },
    "frontend": {
        "dependencies": {
            "vue": "^3.5.30",
        },
        "devDependencies": {
            "@types/node": "^24.12.0",
            "@vitejs/plugin-vue": "^6.0.5",
            "@vue/tsconfig": "^0.9.0",
            "typescript": "~5.9.3",
            "vite": "^8.0.1",
            "vue-tsc": "^3.2.5",
        },
    },
    "structure": [
        "backend/main.py",
        "backend/server.py",
        "backend/pyproject.toml",
        "backend/.python-version",
        "frontend/index.html",
        "frontend/package.json",
        "frontend/vite.config.ts",
        "frontend/tsconfig.json",
        "frontend/tsconfig.app.json",
        "frontend/tsconfig.node.json",
        "frontend/src/App.vue",
        "frontend/src/main.ts",
        "frontend/src/style.css",
    ],
}

# ── Internal helpers ──────────────────────────────────────────────────────────


def _read_pyproject() -> dict:
    path = WORKSPACE_ROOT / "backend" / "pyproject.toml"
    with open(path, "rb") as f:
        return tomllib.load(f)


def _read_package_json() -> dict:
    path = WORKSPACE_ROOT / "frontend" / "package.json"
    with open(path) as f:
        return json.load(f)


def _parse_python_deps(pyproject: dict) -> dict[str, str]:
    """Return {normalized_name: version} from pyproject.toml dependencies."""
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


# ═════════════════════════════════════════════════════════════════════════════
# STEP 1 — Package version tools
# ═════════════════════════════════════════════════════════════════════════════


@mcp.tool
def get_package_version(
    package_name: str,
    ecosystem: Literal["python", "npm", "auto"] = "auto",
) -> dict:
    """Return the pinned version of a package from the project's dependency files.

    Args:
        package_name: Package to look up (e.g. 'vue', 'fastapi', 'vite').
        ecosystem: 'python' searches pyproject.toml, 'npm' searches package.json,
                   'auto' searches both.
    """
    results: dict = {}
    name_lower = package_name.lower()

    if ecosystem in ("python", "auto"):
        try:
            deps = _parse_python_deps(_read_pyproject())
            if name_lower in deps:
                results["python"] = {
                    "version": deps[name_lower],
                    "file": "backend/pyproject.toml",
                }
        except Exception as exc:
            results["python_error"] = str(exc)

    if ecosystem in ("npm", "auto"):
        try:
            pkg = _read_package_json()
            all_deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            matched = next((k for k in all_deps if k.lower() == name_lower), None)
            if matched:
                results["npm"] = {
                    "version": all_deps[matched],
                    "file": "frontend/package.json",
                    "type": "dependency" if matched in pkg.get("dependencies", {}) else "devDependency",
                }
        except Exception as exc:
            results["npm_error"] = str(exc)

    if not results:
        eco_label = "python or npm" if ecosystem == "auto" else ecosystem
        return {"found": False, "message": f"'{package_name}' not found in {eco_label} dependencies."}

    return {"found": True, "package": package_name, **results}


@mcp.tool
def list_packages() -> dict:
    """List every package and its pinned version from both the backend (Python) and frontend (npm)."""
    result: dict = {}

    try:
        pyproject = _read_pyproject()
        result["python"] = {
            "file": "backend/pyproject.toml",
            "requires_python": pyproject.get("project", {}).get("requires-python", "unknown"),
            "packages": _parse_python_deps(pyproject),
        }
    except Exception as exc:
        result["python_error"] = str(exc)

    try:
        pkg = _read_package_json()
        result["npm"] = {
            "file": "frontend/package.json",
            "dependencies": pkg.get("dependencies", {}),
            "devDependencies": pkg.get("devDependencies", {}),
        }
    except Exception as exc:
        result["npm_error"] = str(exc)

    return result


@mcp.tool
def get_python_version() -> dict:
    """Return the required Python version from .python-version and pyproject.toml."""
    result: dict = {}

    pv_path = WORKSPACE_ROOT / "backend" / ".python-version"
    if pv_path.exists():
        result["python_version_file"] = pv_path.read_text().strip()

    try:
        pyproject = _read_pyproject()
        result["pyproject_requires_python"] = (
            pyproject.get("project", {}).get("requires-python", "not set")
        )
    except Exception as exc:
        result["pyproject_error"] = str(exc)

    return result


# ═════════════════════════════════════════════════════════════════════════════
# STEP 2 — Changelog / release-history tools
# ═════════════════════════════════════════════════════════════════════════════


@mcp.tool
async def get_package_changelog(
    package_name: str,
    ecosystem: Literal["python", "npm"],
    num_releases: int = 5,
) -> dict:
    """Fetch recent release history for a package from PyPI or the npm registry.

    Args:
        package_name: Package name (e.g. 'fastapi', 'vue').
        ecosystem: 'python' queries PyPI; 'npm' queries the npm registry.
        num_releases: Number of recent releases to return (1–20, default 5).
    """
    num_releases = max(1, min(num_releases, 20))

    async with httpx.AsyncClient(timeout=10) as client:
        if ecosystem == "python":
            resp = await client.get(f"https://pypi.org/pypi/{package_name}/json")
            if resp.status_code == 404:
                return {"error": f"'{package_name}' not found on PyPI."}
            resp.raise_for_status()
            data = resp.json()
            info = data["info"]
            releases = sorted(data["releases"].keys(), reverse=True)[:num_releases]
            releases_info = [
                {
                    "version": v,
                    "upload_time": data["releases"][v][0].get("upload_time", "unknown")
                    if data["releases"][v]
                    else "unknown",
                }
                for v in releases
            ]
            return {
                "package": package_name,
                "ecosystem": "python",
                "latest_version": info["version"],
                "summary": info.get("summary", ""),
                "changelog_url": info.get("project_urls", {}).get("Changelog", ""),
                "recent_releases": releases_info,
            }

        # npm
        resp = await client.get(f"https://registry.npmjs.org/{package_name}")
        if resp.status_code == 404:
            return {"error": f"'{package_name}' not found on npm."}
        resp.raise_for_status()
        data = resp.json()
        times: dict = data.get("time", {})
        versions = [v for v in data.get("versions", {}) if v not in ("created", "modified")]
        recent = sorted(versions, key=lambda v: times.get(v, ""), reverse=True)[:num_releases]
        return {
            "package": package_name,
            "ecosystem": "npm",
            "latest_version": data.get("dist-tags", {}).get("latest", "unknown"),
            "description": data.get("description", ""),
            "homepage": data.get("homepage", ""),
            "recent_releases": [
                {"version": v, "published": times.get(v, "unknown")} for v in recent
            ],
        }


# ═════════════════════════════════════════════════════════════════════════════
# STEP 3 — Outdated packages check
# ═════════════════════════════════════════════════════════════════════════════


@mcp.tool
async def check_outdated_packages(
    ecosystem: Literal["python", "npm", "all"] = "all",
) -> dict:
    """Check which packages have newer versions available on PyPI or npm.

    Compares each pinned version in the project against the current latest release.

    Args:
        ecosystem: 'python', 'npm', or 'all' (default).
    """
    outdated: list = []
    up_to_date: list = []
    errors: list = []

    async def _check_pypi(name: str, pinned: str) -> None:
        try:
            async with httpx.AsyncClient(timeout=8) as client:
                resp = await client.get(f"https://pypi.org/pypi/{name}/json")
                if resp.status_code != 200:
                    return
                latest = resp.json()["info"]["version"]
            entry = {"package": name, "pinned": pinned, "latest": latest, "ecosystem": "python"}
            (outdated if latest != pinned else up_to_date).append(entry)
        except Exception as exc:
            errors.append({"package": name, "ecosystem": "python", "error": str(exc)})

    async def _check_npm(name: str, pinned: str) -> None:
        try:
            async with httpx.AsyncClient(timeout=8) as client:
                resp = await client.get(f"https://registry.npmjs.org/{name}/latest")
                if resp.status_code != 200:
                    return
                latest = resp.json().get("version", "unknown")
            clean_pinned = pinned.lstrip("^~")
            entry = {"package": name, "pinned": pinned, "latest": latest, "ecosystem": "npm"}
            (outdated if latest != clean_pinned else up_to_date).append(entry)
        except Exception as exc:
            errors.append({"package": name, "ecosystem": "npm", "error": str(exc)})

    tasks: list = []

    if ecosystem in ("python", "all"):
        try:
            deps = _parse_python_deps(_read_pyproject())
            tasks.extend(_check_pypi(name, ver) for name, ver in deps.items())
        except Exception as exc:
            errors.append({"package": "pyproject.toml", "error": str(exc)})

    if ecosystem in ("npm", "all"):
        try:
            pkg = _read_package_json()
            all_deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            tasks.extend(_check_npm(name, ver) for name, ver in all_deps.items())
        except Exception as exc:
            errors.append({"package": "package.json", "error": str(exc)})

    await asyncio.gather(*tasks)

    return {
        "outdated": outdated,
        "up_to_date": up_to_date,
        "errors": errors,
        "summary": (
            f"{len(outdated)} outdated, {len(up_to_date)} up to date, {len(errors)} errors"
        ),
    }


# ═════════════════════════════════════════════════════════════════════════════
# STEP 4 — Template drift detection
# ═════════════════════════════════════════════════════════════════════════════


@mcp.tool
def detect_template_drift() -> dict:
    """Detect drift between the current project and the original template baseline.

    Checks three categories:
    - **structural**: files from the template that are missing in the project.
    - **dependency**: packages added, removed, or with changed version pins.
    - **config**: Python version or other config values that changed.
    """
    structural: list = []
    dependency: list = []
    config: list = []

    # 1. Structural drift — missing files
    for expected_file in TEMPLATE_BASELINE["structure"]:
        if not (WORKSPACE_ROOT / expected_file).exists():
            structural.append({"type": "missing_file", "file": expected_file})

    # 2. Config drift — Python version
    pv_path = WORKSPACE_ROOT / "backend" / ".python-version"
    if pv_path.exists():
        current_pv = pv_path.read_text().strip()
        expected_pv = TEMPLATE_BASELINE["python_version"]
        if current_pv != expected_pv:
            config.append(
                {"type": "python_version", "expected": expected_pv, "actual": current_pv}
            )

    # 3. Backend dependency drift
    try:
        current_deps = _parse_python_deps(_read_pyproject())
        template_backend: dict = TEMPLATE_BASELINE["backend"]
        template_names = {p.split("[")[0].lower() for p in template_backend}

        for pkg, expected_ver in template_backend.items():
            pkg_name = pkg.split("[")[0].lower()
            if pkg_name not in current_deps:
                dependency.append(
                    {"ecosystem": "python", "package": pkg, "type": "removed", "expected": expected_ver}
                )
            elif current_deps[pkg_name] != expected_ver:
                dependency.append(
                    {
                        "ecosystem": "python",
                        "package": pkg,
                        "type": "version_changed",
                        "expected": expected_ver,
                        "actual": current_deps[pkg_name],
                    }
                )

        for pkg_name, ver in current_deps.items():
            if pkg_name not in template_names:
                dependency.append(
                    {"ecosystem": "python", "package": pkg_name, "type": "added", "actual": ver}
                )
    except Exception as exc:
        dependency.append({"ecosystem": "python", "error": str(exc)})

    # 4. Frontend dependency drift
    try:
        pkg_json = _read_package_json()
        all_current = {**pkg_json.get("dependencies", {}), **pkg_json.get("devDependencies", {})}
        all_expected = {
            **TEMPLATE_BASELINE["frontend"]["dependencies"],
            **TEMPLATE_BASELINE["frontend"]["devDependencies"],
        }

        for pkg, expected_ver in all_expected.items():
            if pkg not in all_current:
                dependency.append(
                    {"ecosystem": "npm", "package": pkg, "type": "removed", "expected": expected_ver}
                )
            elif all_current[pkg] != expected_ver:
                dependency.append(
                    {
                        "ecosystem": "npm",
                        "package": pkg,
                        "type": "version_changed",
                        "expected": expected_ver,
                        "actual": all_current[pkg],
                    }
                )

        for pkg in all_current:
            if pkg not in all_expected:
                dependency.append(
                    {"ecosystem": "npm", "package": pkg, "type": "added", "actual": all_current[pkg]}
                )
    except Exception as exc:
        dependency.append({"ecosystem": "npm", "error": str(exc)})

    total = len(structural) + len(dependency) + len(config)
    summary = (
        "No drift detected. Project matches the template baseline."
        if total == 0
        else (
            f"Drift detected: {len(structural)} structural, "
            f"{len(dependency)} dependency, {len(config)} config changes."
        )
    )

    return {"structural": structural, "dependency": dependency, "config": config, "summary": summary}


# ═════════════════════════════════════════════════════════════════════════════
# STEP 5 — Drift fix suggestions
# ═════════════════════════════════════════════════════════════════════════════


@mcp.tool
def suggest_drift_fixes() -> dict:
    """Generate actionable suggestions and shell commands to resolve template drift.

    Internally runs detect_template_drift and produces a prioritised fix list.
    Severity levels: high (breaking) → medium (functional) → low (cosmetic) → info.
    """
    drift = detect_template_drift()
    suggestions: list = []

    for item in drift.get("structural", []):
        if item.get("type") == "missing_file":
            suggestions.append(
                {
                    "severity": "high",
                    "issue": f"Missing file: {item['file']}",
                    "suggestion": f"Restore '{item['file']}' from the template repository.",
                }
            )

    for item in drift.get("config", []):
        if item.get("type") == "python_version":
            suggestions.append(
                {
                    "severity": "high",
                    "issue": (
                        f"Python version mismatch: expected {item['expected']}, got {item['actual']}"
                    ),
                    "suggestion": (
                        f"Update backend/.python-version to '{item['expected']}' "
                        "and adjust pyproject.toml requires-python."
                    ),
                    "command": f"echo '{item['expected']}' > backend/.python-version",
                }
            )

    for item in drift.get("dependency", []):
        if "error" in item:
            continue
        eco = item.get("ecosystem", "")
        pkg = item.get("package", "")
        dtype = item.get("type", "")

        if dtype == "removed":
            if eco == "python":
                suggestions.append(
                    {
                        "severity": "medium",
                        "issue": f"Python package '{pkg}' removed (was {item['expected']})",
                        "suggestion": f"Re-add the package.",
                        "command": f'cd backend && uv add "{pkg}=={item["expected"]}"',
                    }
                )
            else:
                suggestions.append(
                    {
                        "severity": "medium",
                        "issue": f"npm package '{pkg}' removed (was {item['expected']})",
                        "suggestion": "Re-add the package.",
                        "command": f"cd frontend && npm install {pkg}@{item['expected'].lstrip('^~')}",
                    }
                )

        elif dtype == "version_changed":
            if eco == "python":
                suggestions.append(
                    {
                        "severity": "low",
                        "issue": f"Python '{pkg}' changed from {item['expected']} → {item['actual']}",
                        "suggestion": "Pin back to the template version or update the baseline.",
                        "command": f'cd backend && uv add "{pkg}=={item["expected"]}"',
                    }
                )
            else:
                suggestions.append(
                    {
                        "severity": "low",
                        "issue": f"npm '{pkg}' changed from {item['expected']} → {item['actual']}",
                        "suggestion": "Revert to template version or update the baseline.",
                        "command": f"cd frontend && npm install {pkg}@{item['expected'].lstrip('^~')}",
                    }
                )

        elif dtype == "added":
            suggestions.append(
                {
                    "severity": "info",
                    "issue": f"Extra package '{pkg}' ({eco}) not in template",
                    "suggestion": (
                        "Intentional addition? If so, update TEMPLATE_BASELINE in server.py. "
                        "Otherwise remove it."
                    ),
                }
            )

    # Sort: high → medium → low → info
    _order = {"high": 0, "medium": 1, "low": 2, "info": 3}
    suggestions.sort(key=lambda s: _order.get(s["severity"], 99))

    return {
        "drift_summary": drift.get("summary", ""),
        "suggestions": suggestions,
        "total_suggestions": len(suggestions),
    }


# ═════════════════════════════════════════════════════════════════════════════
# STEP 6 — File structure & project overview
# ═════════════════════════════════════════════════════════════════════════════


@mcp.tool
def get_file_structure(relative_path: str = ".") -> dict:
    """Return the directory tree for a path inside the project.

    Args:
        relative_path: Path relative to the workspace root (default '.' = whole project).
    """
    target = (WORKSPACE_ROOT / relative_path).resolve()

    # Security: stay within workspace root
    if not str(target).startswith(str(WORKSPACE_ROOT.resolve())):
        return {"error": "Path is outside the project root."}
    if not target.exists():
        return {"error": f"Path '{relative_path}' does not exist."}

    _SKIP_DIRS = {"node_modules", "__pycache__", ".venv", "dist", ".git", ".mypy_cache"}
    _SHOW_DOTFILES = {".python-version", ".gitignore"}

    def _walk(path: Path, depth: int = 0) -> list:
        if depth > 4:
            return [{"name": "…", "type": "truncated"}]
        items = []
        try:
            for child in sorted(path.iterdir()):
                if child.name in _SKIP_DIRS:
                    continue
                if child.name.startswith(".") and child.name not in _SHOW_DOTFILES:
                    continue
                if child.is_dir():
                    items.append({"name": child.name, "type": "directory", "children": _walk(child, depth + 1)})
                else:
                    items.append({"name": child.name, "type": "file"})
        except PermissionError:
            pass
        return items

    return {"path": str(relative_path), "structure": _walk(target)}


@mcp.tool
def get_project_info() -> dict:
    """Return a full overview of the project: name, versions, scripts, and template baseline."""
    info: dict = {"template_baseline": TEMPLATE_BASELINE}

    try:
        pyproject = _read_pyproject()
        proj = pyproject.get("project", {})
        info["backend"] = {
            "name": proj.get("name", "unknown"),
            "version": proj.get("version", "unknown"),
            "description": proj.get("description", ""),
            "requires_python": proj.get("requires-python", "unknown"),
            "packages": _parse_python_deps(pyproject),
        }
    except Exception as exc:
        info["backend_error"] = str(exc)

    try:
        pkg = _read_package_json()
        info["frontend"] = {
            "name": pkg.get("name", "unknown"),
            "version": pkg.get("version", "unknown"),
            "scripts": pkg.get("scripts", {}),
            "dependencies": pkg.get("dependencies", {}),
            "devDependencies": pkg.get("devDependencies", {}),
        }
    except Exception as exc:
        info["frontend_error"] = str(exc)

    return info


if __name__ == "__main__":
    mcp.run(port=8001)
