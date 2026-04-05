from __future__ import annotations

from utils.drift import compute_drift


def suggest_drift_fixes() -> dict:
    """Generate actionable suggestions and shell commands to resolve template drift.

    Internally runs drift detection and produces a prioritised fix list.
    Severity levels: high (breaking) → medium (functional) → low (cosmetic) → info.
    """
    drift = compute_drift()
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
                        "suggestion": "Re-add the package.",
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
                        "Intentional addition? If so, update TEMPLATE_BASELINE in utils/constants.py. "
                        "Otherwise remove it."
                    ),
                }
            )

    _order = {"high": 0, "medium": 1, "low": 2, "info": 3}
    suggestions.sort(key=lambda s: _order.get(s["severity"], 99))

    return {
        "drift_summary": drift.get("summary", ""),
        "suggestions": suggestions,
        "total_suggestions": len(suggestions),
    }
