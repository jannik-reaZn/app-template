from __future__ import annotations


from utils.readers import parse_python_deps, read_package_json, read_pyproject
from pydantic import BaseModel
from enum import StrEnum


class EcosystemEnum(StrEnum):
    PYTHON = "python"
    NPM = "npm"
    AUTO = "auto"


class PackageVersionInfo(BaseModel):
    found: bool
    package: str | None = None
    python: dict | None = None
    npm: dict | None = None
    python_error: str | None = None
    npm_error: str | None = None
    message: str | None = None


def get_package_version(
    package_name: str,
    ecosystem: EcosystemEnum = EcosystemEnum.AUTO,
) -> PackageVersionInfo:
    """Return the pinned version of a package from the project's dependency files.

    Args:
        package_name: Package to look up (e.g. 'vue', 'fastapi', 'vite').
        ecosystem: Which ecosystem to check: 'python' (pyproject.toml), 'npm' (package.json), or 'auto' (both).
    """
    name_lower = package_name.lower()
    results = PackageVersionInfo(found=False, package=package_name)

    if ecosystem in (EcosystemEnum.PYTHON.value, EcosystemEnum.AUTO.value):
        try:
            deps = parse_python_deps(read_pyproject())
            if name_lower in deps:
                results.python = {
                    "version": deps[name_lower],
                    "file": "backend/pyproject.toml",
                }
        except Exception as exc:
            results.python_error = str(exc)

    if ecosystem in (EcosystemEnum.NPM.value, EcosystemEnum.AUTO.value):
        try:
            pkg = read_package_json()
            all_deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            matched = next((k for k in all_deps if k.lower() == name_lower), None)
            if matched:
                results.npm = {
                    "version": all_deps[matched],
                    "file": "frontend/package.json",
                    "type": "dependency"
                    if matched in pkg.get("dependencies", {})
                    else "devDependency",
                }
        except Exception as exc:
            results.npm_error = str(exc)

    if not results.found:
        eco_label = (
            "python or npm" if ecosystem == EcosystemEnum.AUTO.value else ecosystem
        )
        results.message = f"'{package_name}' not found in {eco_label} dependencies."

    return results
