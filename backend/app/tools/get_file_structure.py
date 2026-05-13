from __future__ import annotations

from pathlib import Path

from app.tools.utils.constants import WORKSPACE_ROOT

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
                items.append(
                    {
                        "name": child.name,
                        "type": "directory",
                        "children": _walk(child, depth + 1),
                    }
                )
            else:
                items.append({"name": child.name, "type": "file"})
    except PermissionError:
        pass
    return items


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

    return {"path": str(relative_path), "structure": _walk(target)}
