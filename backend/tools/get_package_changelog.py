from __future__ import annotations

from typing import Literal

import httpx


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
        versions = [
            v for v in data.get("versions", {}) if v not in ("created", "modified")
        ]
        recent = sorted(versions, key=lambda v: times.get(v, ""), reverse=True)[
            :num_releases
        ]
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
