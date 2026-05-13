from __future__ import annotations

from app.tools.utils.constants import TEMPLATE_BASELINE, WORKSPACE_ROOT
from app.tools.utils.readers import (
    parse_python_deps,
    read_package_json,
    read_pyproject,
)


def compute_drift() -> dict:
    """Compute the full drift report between the project and the template baseline.

    Shared by detect_template_drift and suggest_drift_fixes tools.
    Returns a dict with keys: structural, dependency, config, summary.
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
                {
                    "type": "python_version",
                    "expected": expected_pv,
                    "actual": current_pv,
                }
            )

    # 3. Backend dependency drift
    try:
        current_deps = parse_python_deps(read_pyproject())
        template_backend: dict = TEMPLATE_BASELINE["backend"]
        template_names = {p.split("[")[0].lower() for p in template_backend}

        for pkg, expected_ver in template_backend.items():
            pkg_name = pkg.split("[")[0].lower()
            if pkg_name not in current_deps:
                dependency.append(
                    {
                        "ecosystem": "python",
                        "package": pkg,
                        "type": "removed",
                        "expected": expected_ver,
                    }
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
                    {
                        "ecosystem": "python",
                        "package": pkg_name,
                        "type": "added",
                        "actual": ver,
                    }
                )
    except Exception as exc:
        dependency.append({"ecosystem": "python", "error": str(exc)})

    # 4. Frontend dependency drift
    try:
        pkg_json = read_package_json()
        all_current = {
            **pkg_json.get("dependencies", {}),
            **pkg_json.get("devDependencies", {}),
        }
        all_expected = {
            **TEMPLATE_BASELINE["frontend"]["dependencies"],
            **TEMPLATE_BASELINE["frontend"]["devDependencies"],
        }

        for pkg, expected_ver in all_expected.items():
            if pkg not in all_current:
                dependency.append(
                    {
                        "ecosystem": "npm",
                        "package": pkg,
                        "type": "removed",
                        "expected": expected_ver,
                    }
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
                    {
                        "ecosystem": "npm",
                        "package": pkg,
                        "type": "added",
                        "actual": all_current[pkg],
                    }
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

    return {
        "structural": structural,
        "dependency": dependency,
        "config": config,
        "summary": summary,
    }
