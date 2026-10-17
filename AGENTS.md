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
cd frontend && pnpm dev        # dev server on :5173
cd frontend && pnpm build      # type-check + build
```

## API contract

`openapi.yaml` (repo root) is generated from the FastAPI app and is the contract between backend and frontend. After changing endpoints or schemas:

```bash
cd backend && uv run python export_openapi.py   # backend -> openapi.yaml
cd frontend && pnpm gen:api                     # openapi.yaml -> frontend/src/api (@hey-api/openapi-ts)
```

When staged changes include `backend/**/*.py`, the pre-commit hook runs `ruff format` and `ruff check --fix` on those files (and re-stages them), `ty check` on the whole backend, then re-runs the export and stages `openapi.yaml`, so the committed contract can't go stale. Frontend files are checked with `vp staged`. Tests are not part of the hook.

`frontend/src/api/` is gitignored and never edited by hand. It is regenerated automatically on `pnpm install`, `pnpm dev` and `pnpm build`; commit `openapi.yaml`, not the generated code.

Package manager: **uv** for Python, **pnpm** for Node. Do not use pip, npm or yarn.

## Conventions

- **Frontend**: SFC components in `frontend/src/components/`, composables in `frontend/src/composables/` (create if needed)
- **Linting**: `ruff` for Python (configured via pyproject.toml), `vue-tsc` for TypeScript

## Key Files

- `backend/pyproject.toml` — Python deps (pinned with `==`)
- `frontend/package.json` — frontend deps (pnpm)
- `frontend/vite.config.ts` — Vite config (host 0.0.0.0, port 5173)
