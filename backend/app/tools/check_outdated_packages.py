from __future__ import annotations

import asyncio
from typing import Literal

import httpx

from app.tools.utils.readers import parse_python_deps, read_package_json, read_pyproject


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
            entry = {
                "package": name,
                "pinned": pinned,
                "latest": latest,
                "ecosystem": "python",
            }
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
            entry = {
                "package": name,
                "pinned": pinned,
                "latest": latest,
                "ecosystem": "npm",
            }
            (outdated if latest != clean_pinned else up_to_date).append(entry)
        except Exception as exc:
            errors.append({"package": name, "ecosystem": "npm", "error": str(exc)})

    tasks: list = []

    if ecosystem in ("python", "all"):
        try:
            deps = parse_python_deps(read_pyproject())
            tasks.extend(_check_pypi(name, ver) for name, ver in deps.items())
        except Exception as exc:
            errors.append({"package": "pyproject.toml", "error": str(exc)})

    if ecosystem in ("npm", "all"):
        try:
            pkg = read_package_json()
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
