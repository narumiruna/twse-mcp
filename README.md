# mcp-server-twse

### GitHub

```json
{
  "mcpServers": {
    "mcp-server-twse": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/narumiruna/mcp-server-twse",
        "mcp-server-twse"
      ]
    }
  }
}
```

### Local

```json
{
  "mcpServers": {
    "mcp-server-twse": {
      "command": "uv",
      "args": [
        "run",
        "--directory",
        "/home/<user>/workspace/mcp-server-twse",
        "mcp-server-twse"
      ]
    }
  }
}
```
