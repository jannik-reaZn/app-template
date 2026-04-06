# MCP Server

### Run MCP Server

```bash
cd backend && uv run fastmcp run server.py:mcp --transport streamable-http --port 8000
```

Sometimes the MCP server and its tools are not present for copilot. In that case, start the MCP server manually using the command panel in VS Code. Open the command palette (Ctrl+Shift+P), search for "Run MCP Server", and select it to start the server.

### Using MCP Server with Copilot

In Github Copilot Chat, you can specify the MPC server and the tool that should be used for a request. For example:

```bash
#mcp-test What is the current python version of the application template project?
```

You may need to click `Allow in this Session` for the MCP server to be used in Copilot.

### Restart MCP Server

Go to Extensions -> MCP Server INSTALLED -> Gear Icon -> Restart Server

# Send Request to MCP Server

Run the `send_request_to_mcp.sh` script to send a test request to the MCP server.

```bash
cd backend && ./send_request_to_mcp.sh
```

# Run FastAPI Server

```bash
cd backend && uv run fastapi dev
```
