# Run MCP Server

```bash
cd backend && uv run fastmcp run server.py:mcp --transport streamable-http --port 8001
```

# Send Request to MCP Server

Run the `send_request_to_mcp.sh` script to send a test request to the MCP server.

```bash
cd backend && ./send_request_to_mcp.sh
```

# Run FastAPI Server

```bash
cd backend && uv run fastapi dev
```
