from __future__ import annotations

from pathlib import Path

# Two levels up from utils/: backend/utils/ → backend/ → app-template/
WORKSPACE_ROOT = Path(__file__).parent.parent.parent

TEMPLATE_BASELINE: dict = {
    "python_version": "3.14",
    "backend": {
        "fastapi[standard]": "0.135.3",
        "fastmcp": "3.2.0",
        "httpx": "0.28.1",
        "ruff": "0.15.9",
    },
    "frontend": {
        "dependencies": {
            "vue": "^3.5.30",
        },
        "devDependencies": {
            "@types/node": "^24.12.0",
            "@vitejs/plugin-vue": "^6.0.5",
            "@vue/tsconfig": "^0.9.0",
            "typescript": "~5.9.3",
            "vite": "^8.0.1",
            "vue-tsc": "^3.2.5",
        },
    },
    "structure": [
        "backend/main.py",
        "backend/server.py",
        "backend/pyproject.toml",
        "backend/.python-version",
        "frontend/index.html",
        "frontend/package.json",
        "frontend/vite.config.ts",
        "frontend/tsconfig.json",
        "frontend/tsconfig.app.json",
        "frontend/tsconfig.node.json",
        "frontend/src/App.vue",
        "frontend/src/main.ts",
        "frontend/src/style.css",
    ],
}
