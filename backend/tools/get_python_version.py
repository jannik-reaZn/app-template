from __future__ import annotations

from pydantic import BaseModel

from utils.constants import WORKSPACE_ROOT
from utils.readers import read_pyproject


class PythonVersionInfo(BaseModel):
    python_version_file: str | None = None
    pyproject_requires_python: str | None = None
    pyproject_error: str | None = None


def get_python_version() -> PythonVersionInfo:
    """Return the required Python version from .python-version and pyproject.toml."""
    result = PythonVersionInfo()

    pv_path = WORKSPACE_ROOT / "backend" / ".python-version"
    if pv_path.exists():
        result.python_version_file = pv_path.read_text().strip()

    try:
        pyproject = read_pyproject()
        result.pyproject_requires_python = pyproject.get("project", {}).get(
            "requires-python", "not set"
        )
    except Exception as exc:
        result.pyproject_error = str(exc)

    return result
