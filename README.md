# TWSE MCP Server

### GitHub

```json
{
  "mcpServers": {
    "twsemcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/narumiruna/twse-mcp",
        "twsemcp"
      ]
    }
  }
}
```

### Local

```json
{
  "mcpServers": {
    "twsemcp": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/home/<user>/workspace/twse-mcp",
        "twsemcp"
      ]
    }
  }
}
```
