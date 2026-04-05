# Run MCP Server

```bash
cd backend && uv run fastmcp run server.py:mcp --transport streamable-http --port 8001
```

# Send Request to MCP Server

- Step 1: Initialize and save headers

```bash
curl -s -X POST http://localhost:8001/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"curl","version":"1.0"}},"id":0}' \
  -D /tmp/headers.txt > /dev/null
```

- Step 2: Extract session ID

```bash
SESSION_ID=$(grep -i "mcp-session-id" /tmp/headers.txt | awk '{print $2}' | tr -d '\r')
```

- Step 3: Call the tool

```bash
curl -X POST http://localhost:8001/mcp \
 -H "Content-Type: application/json" \
 -H "Accept: application/json, text/event-stream" \
 -H "mcp-session-id: $SESSION_ID" \
 -d '{"jsonrpc": "2.0", "method": "tools/call", "params": {"name": "add", "arguments": {"a": 2, "b": 3}}, "id": 1}'

```
