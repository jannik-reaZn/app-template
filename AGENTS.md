# Project Guidelines — app-template

Full-stack template: **Python 3.14 FastAPI backend** + **Vue 3 + Vite + TypeScript frontend**.

## Testing

```bash
cd backend
uv run pytest
```

## Architecture

| Layer      | Path                | Tech                                    |
| ---------- | ------------------- | --------------------------------------- |
| REST API   | `backend/main.py`   | FastAPI 0.135.3                         |
| Frontend   | `frontend/src/`     | Vue 3.5, Vite 8, TypeScript strict      |

## Build & Run

```bash
# Backend (FastAPI)
cd backend && uv run fastapi dev main.py

# Frontend
cd frontend && npm run dev        # dev server on :5173
cd frontend && npm run build      # type-check + build
```

Package manager: **uv** for Python, **npm** for Node. Do not use pip or yarn.

## Conventions

- **Frontend**: SFC components in `frontend/src/components/`, composables in `frontend/src/composables/` (create if needed)
- **Linting**: `ruff` for Python (configured via pyproject.toml), `vue-tsc` for TypeScript

## Key Files

- `backend/pyproject.toml` — Python deps (pinned with `==`)
- `frontend/package.json` — npm deps
- `frontend/vite.config.ts` — Vite config (host 0.0.0.0, port 5173)
