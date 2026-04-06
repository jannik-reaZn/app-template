#!/usr/bin/env bash
set -e

BASE_URL="http://localhost:8000/mcp/"

# Step 1: Initialize session
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"curl","version":"1.0"}},"id":0}' \
  -D /tmp/mcp_headers.txt > /dev/null

# Step 2: Extract session ID
SESSION_ID=$(grep -i "mcp-session-id" /tmp/mcp_headers.txt | awk '{print $2}' | tr -d '\r')
echo "Session ID: $SESSION_ID"

# Step 3: Call list_packages tool
echo ""
echo "Calling list_packages..."
curl -s -X POST "$BASE_URL" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: $SESSION_ID" \
  -d '{"jsonrpc":"2.0","method":"tools/call","params":{"name":"list_packages","arguments":{}},"id":1}'
echo ""
