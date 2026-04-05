from __future__ import annotations

from utils.constants import TEMPLATE_BASELINE
from utils.readers import parse_python_deps, read_package_json, read_pyproject


def get_project_info() -> dict:
    """Return a full overview of the project: name, versions, scripts, and template baseline."""
    info: dict = {"template_baseline": TEMPLATE_BASELINE}

    try:
        pyproject = read_pyproject()
        proj = pyproject.get("project", {})
        info["backend"] = {
            "name": proj.get("name", "unknown"),
            "version": proj.get("version", "unknown"),
            "description": proj.get("description", ""),
            "requires_python": proj.get("requires-python", "unknown"),
            "packages": parse_python_deps(pyproject),
        }
    except Exception as exc:
        info["backend_error"] = str(exc)

    try:
        pkg = read_package_json()
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
