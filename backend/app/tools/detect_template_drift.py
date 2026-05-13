from __future__ import annotations

from app.tools.utils.drift import compute_drift


def detect_template_drift() -> dict:
    """Detect drift between the current project and the original template baseline.

    Checks three categories:
    - **structural**: files from the template that are missing in the project.
    - **dependency**: packages added, removed, or with changed version pins.
    - **config**: Python version or other config values that changed.
    """
    return compute_drift()
