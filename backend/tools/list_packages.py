from __future__ import annotations

from utils.readers import parse_python_deps, read_package_json, read_pyproject


def list_packages() -> dict:
    """List every package and its pinned version from both the backend (Python) and frontend (npm)."""
    result: dict = {}

    try:
        pyproject = read_pyproject()
        result["python"] = {
            "file": "backend/pyproject.toml",
            "requires_python": pyproject.get("project", {}).get(
                "requires-python", "unknown"
            ),
            "packages": parse_python_deps(pyproject),
        }
    except Exception as exc:
        result["python_error"] = str(exc)

    try:
        pkg = read_package_json()
        result["npm"] = {
            "file": "frontend/package.json",
            "dependencies": pkg.get("dependencies", {}),
            "devDependencies": pkg.get("devDependencies", {}),
        }
    except Exception as exc:
        result["npm_error"] = str(exc)

    return result
