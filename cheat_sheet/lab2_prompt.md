1. Install DDG MCP:
```
Install this MCP on this workspace: {
  "mcpServers": {
    "ddg-search": {
      "command": "uvx",
      "args": ["duckduckgo-mcp-server"]
    }
  }
}
```

2. After installation, agent might still not call MCP. Here you should create agent rule `AGENTS.md` in your root folder which contains message:
```
- Any question out of knowledge cut-off, try searching on internet with DDG MCP.
```

## Troubleshoot:
- If the mcp.json already configured and still does not work. Try running `uvx duckduckgo-mcp-server` manually.
