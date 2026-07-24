# gemlogin-mcp

> Drive your GemLogin antidetect browser from Claude Code, Claude Desktop, Cursor, or any other MCP-compatible client.

[GemLogin](https://gemlogin.app) ships a local REST API on `http://localhost:1010` for managing Chromium browser profiles with isolated fingerprints. This package wraps that API as a [Model Context Protocol](https://modelcontextprotocol.io) server so an AI agent can list, start, and stop profiles by natural language and attach Puppeteer / Playwright / Selenium to the returned Chrome DevTools URL.

---

## Install (60 seconds)

### 1. Make sure GemLogin is running
GemLogin's local API must be reachable on `localhost:1010`:

```bash
open /Applications/GemLogin.app          # macOS
curl -s http://localhost:1010/api/status # should return JSON with success: true
```

### 2. Install the package
Pick whichever you prefer:

```bash
# Recommended: pipx (isolated, on your PATH)
pipx install gemlogin-mcp

# or plain pip
pip install gemlogin-mcp

# or directly from source
pip install git+https://forgejo.contentsdigital.us/ccdev/gemlogin-mcp.git
```

### 3. Register it with your AI client

**Claude Code (terminal)**
```bash
claude mcp add gemlogin -- gemlogin-mcp
```

**Claude Desktop** — add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "gemlogin": {
      "command": "gemlogin-mcp"
    }
  }
}
```

**Cursor** — add to `~/.cursor/mcp.json`:
```json
{
  "mcpServers": {
    "gemlogin": { "command": "gemlogin-mcp" }
  }
}
```

### 4. Verify
```bash
claude mcp list          # should include "gemlogin"
```

Then in your AI client:

> "Use gemlogin to list my profiles, then open profile 1 and tell me what the CDP URL is."

---

## What it exposes

### Tools (the AI calls these)

**Local app (`localhost:1010`)**
| Tool | Args | Returns |
|---|---|---|
| `gemlogin_status` | — | server health, `activeBrowsers`, features |
| `gemlogin_list_profiles` | — | all profiles |
| `gemlogin_get_profile` | `profile_id` | one profile detail |
| `gemlogin_start_profile` | `profile_id` | `remote_debugging_address`, `browser_location`, `driver_path` |
| `gemlogin_stop_profile` | `profile_id` | success/failure |
| `gemlogin_list_groups` | — | profile groups |
| `gemlogin_list_scripts` | optional `include_sensitive_defaults` | installed automation scripts + parameter schemas (sensitive defaults masked by default) |
| `gemlogin_browser_versions` | — | available Chromium versions |
| `gemlogin_find_script` | `script_name`, optional `top_k` | best local script matches by name |
| `gemlogin_execute_local_script` | `profile_id[]`, `script_id` or `script_name`, optional `parameters`/`close_browser`/`require_exact_script_name`/`retries` | run local script via `/api/scripts/execute/{id}` with per-profile retries; exact-name matching is enabled by default |
| `gemlogin_check_local_script_status` | `script_id`, `profile_id` | local script status via `/api/scripts/check-status/{id}` |
| `gemlogin_kill_local_script` | `script_id`, `profile_id` | stop local script via `/api/scripts/kill-execute/{id}` |

**Cloud (`app.gemlogin.io/api/v2/execscript`)** — added in v0.2.0
| Tool | Args | Returns |
|---|---|---|
| `gemlogin_cloud_execscript` | `profile_id`, `workflow_id`, optional `device_id`/`soft_id`/`token`/`extra` | cloud webhook response |

### Resources (the AI reads these without firing a tool)
| URI | Returns |
|---|---|
| `gemlogin://status` | server status snapshot |
| `gemlogin://profiles` | all profiles JSON |
| `gemlogin://profile/{id}` | one profile JSON |

### Prompts (templates the user can pick)
| Prompt | Use for |
|---|---|
| `warm_profile(profile_id, minutes)` | gentle warm-up flow for one persona |
| `post_to_group(group_name, content)` | fan out content across every profile in a group |

---

## Configuration

**Local app**
| Env var | Default | Purpose |
|---|---|---|
| `GEMLOGIN_BASE` | `http://localhost:1010` | GemLogin Express base URL |
| `GEMLOGIN_TIMEOUT` | `60` | per-request timeout (seconds) — `start` is slow |

**Cloud webhook** (for `gemlogin_cloud_execscript`; get all three from
`app.gemlogin.io` → Automation → Webhook for your device)
| Env var | Default | Purpose |
|---|---|---|
| `GEMLOGIN_CLOUD_BASE` | `https://app.gemlogin.io` | cloud SaaS base URL |
| `GEMLOGIN_CLOUD_DEVICE_ID` | — | your device's cloud id |
| `GEMLOGIN_CLOUD_SOFT_ID` | — | your software/app id |
| `GEMLOGIN_CLOUD_TOKEN` | — | per-device webhook secret (the actual auth) |

> Note: `gemlogin_cloud_execscript` authenticates via the **`token` body field**, not a Bearer header. `GEMLOGIN_CLOUD_BEARER` is accepted but optional and ignored by the server.

Override per-client by passing env to the command. Claude Desktop example with both surfaces:

```json
{
  "mcpServers": {
    "gemlogin": {
      "command": "gemlogin-mcp",
      "env": {
        "GEMLOGIN_BASE": "http://localhost:1010",
        "GEMLOGIN_CLOUD_DEVICE_ID": "device-xxxx",
        "GEMLOGIN_CLOUD_SOFT_ID":   "soft-xxxx",
        "GEMLOGIN_CLOUD_TOKEN":     "tok-xxxx"
      }
    }
  }
}
```

---

## Example session

```
You:  Open profile 1 and tell me the CDP URL.

AI:   [calls gemlogin_start_profile(1)]
      Profile 1 ("Frilly-Language") is now running.
      Chrome DevTools URL: http://127.0.0.1:63608
      Browser binary: /Users/ccdev/.gemlogin/browser/130/...

You:  Close it.

AI:   [calls gemlogin_stop_profile(1)]
      Closed. activeBrowsers is now 0.
```

---

## Use cases

- **Account warming at scale** — "Warm profiles 1–50 for 25 minutes each, parallel batches of 10."
- **Cookie / session sweeps** — "Dump cookie jars from every profile in group `Hotmail` to ./cookies/."
- **Multi-persona posting** — "For each profile in group `Marketing`, open the feed, post today's content, screenshot, close."
- **QA across fingerprints** — "Visit my checkout flow with every profile and report any UA-specific render bugs."
- **Replay a captured flow** — Claude reads your Playwright trace, asks gemlogin to spin up the right profile, and replays.

---

## How it works

```
┌──────────────────┐    stdio MCP     ┌──────────────────┐    HTTP    ┌──────────────────┐
│  Claude Code     │ ───────────────▶ │  gemlogin-mcp    │ ─────────▶ │  GemLogin :1010  │
│  Claude Desktop  │                  │  (this package)  │            │  Electron / Vue  │
│  Cursor, Zed, …  │                  │                  │            │                  │
└──────────────────┘                  └──────────────────┘            └──────────────────┘
                                                                              │
                                                                              ▼
                                                                       launches Chromium
                                                                       w/ remote-debug port
                                                                              │
                                                       ┌──────────────────────┴──────────────────┐
                                                       │ Puppeteer / Playwright / Selenium       │
                                                       │ attach to remote_debugging_address      │
                                                       └─────────────────────────────────────────┘
```

The MCP server is a thin async-httpx wrapper — no state, no DB, no daemon. It speaks stdio (the default Claude/Cursor transport) and exits when the client exits.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `connection refused :1010` | GemLogin app isn't running | `open /Applications/GemLogin.app` and wait for the UI |
| `command not found: gemlogin-mcp` | install dir not on PATH | use `pipx`, or `python -m gemlogin_mcp` |
| Claude says "no MCP servers" | not registered | rerun `claude mcp add gemlogin -- gemlogin-mcp` |
| `start` times out | first-time Chromium download | increase `GEMLOGIN_TIMEOUT=120` and retry |
| Wrong remote host | env not picked up | export `GEMLOGIN_BASE=...` *before* launching your client, or set it in the client's `mcpServers.env` block |

---

## Development

```bash
git clone https://forgejo.contentsdigital.us/ccdev/gemlogin-mcp.git
cd gemlogin-mcp
pip install -e ".[dev]"
pytest
ruff check .
```

Smoke-run against your local GemLogin:
```bash
python -m gemlogin_mcp
# (speaks MCP over stdio — useful for an MCP inspector client)
```

---

## License

MIT — © Contents Digital. See [LICENSE](LICENSE).

## Links

- Source: <https://forgejo.contentsdigital.us/ccdev/gemlogin-mcp>
- MCP spec: <https://modelcontextprotocol.io>
- GemLogin: <https://gemlogin.app>
- Claude Code: <https://docs.claude.com/en/docs/claude-code>
