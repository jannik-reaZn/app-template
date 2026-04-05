# Project Guidelines — app-template

Full-stack template: **Python 3.14 FastMCP/FastAPI backend** + **Vue 3 + Vite + TypeScript frontend**.

## Architecture

| Layer      | Path                | Tech                                    |
| ---------- | ------------------- | --------------------------------------- |
| MCP Server | `backend/server.py` | FastMCP 3.2.0, streamable-http on :8001 |
| REST API   | `backend/main.py`   | FastAPI 0.135.3                         |
| Frontend   | `frontend/src/`     | Vue 3.5, Vite 8, TypeScript strict      |

The MCP server (`server.py`) is the primary interface for AI agents. It exposes tools that inspect and audit projects derived from this template. `main.py` is a separate FastAPI app entry point.

## Build & Run

```bash
# Backend (MCP server)
cd backend && uv run fastmcp run server.py:mcp --transport streamable-http --port 8001

# Backend (FastAPI)
cd backend && uv run fastapi dev main.py

# Frontend
cd frontend && npm run dev        # dev server on :5173
cd frontend && npm run build      # type-check + build
```

Package manager: **uv** for Python, **npm** for Node. Do not use pip or yarn.

## MCP Server Tools

All tools live in `backend/server.py`. When adding a new tool:

- Decorate with `@mcp.tool`
- Use precise type annotations (including `Literal` for fixed choices)
- Async tools (`async def`) for any network I/O (PyPI/npm API calls via `httpx`)
- Return plain `dict` — FastMCP serialises it automatically

When the template's canonical dependency versions change, update `TEMPLATE_BASELINE` in `server.py`.

## Conventions

- **Python**: `tomllib` (stdlib) for TOML; all paths resolved via `WORKSPACE_ROOT = Path(__file__).parent.parent`
- **Path safety**: never resolve paths outside `WORKSPACE_ROOT` (enforced in `get_file_structure`)
- **Async gather pattern**: wrap independent async checks in `asyncio.gather(*tasks)` — see `check_outdated_packages`
- **Frontend**: SFC components in `frontend/src/components/`, composables in `frontend/src/composables/` (create if needed)
- **Linting**: `ruff` for Python (configured via pyproject.toml), `vue-tsc` for TypeScript

## Testing the MCP Server

See `README.md` for the 3-step curl workflow (init → extract session-id → call tool).

## Key Files

- `backend/server.py` — all MCP tools + `TEMPLATE_BASELINE` constant
- `backend/pyproject.toml` — Python deps (pinned with `==`)
- `frontend/package.json` — npm deps
- `frontend/vite.config.ts` — Vite config (host 0.0.0.0, port 5173)
