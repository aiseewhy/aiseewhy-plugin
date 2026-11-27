# AISeeWhy agent plugin

Skills and an MCP server that let AI agents check whether ChatGPT, Claude, Perplexity and Gemini crawlers can reach and read a page, find what blocks them, fix it and prove the fix worked. Hosted service: [aiseewhy.com](https://aiseewhy.com/?utm_source=plugin&utm_medium=integration&utm_campaign=readme).

Eight skills: the access check, the fix, the crawler policy, llms.txt, a readiness report, a site-wide SEO crawl, store structured data, and `aiseewhy-audit`, which runs the access check without the MCP server (public API or a local read-only script). See [plugins/aiseewhy/README.md](plugins/aiseewhy/README.md) for what each skill does and how to set the API key, and [CHANGELOG.md](CHANGELOG.md) for changes.

## Claude Code

```
/plugin marketplace add aiseewhy/aiseewhy-plugin
/plugin install aiseewhy@aiseewhy
```

The plugin brings the skills and the MCP server; check with `/mcp` that `aiseewhy` is connected.

MCP only, without the skills:

```sh
claude mcp add --transport http aiseewhy https://api.aiseewhy.com/mcp --header "x-api-key: $AISEEWHY_API_KEY"
```

## Skills only, for any agent that reads SKILL.md

```sh
npx skills add aiseewhy/aiseewhy-plugin
```

Or copy folders from `plugins/aiseewhy/skills/` into your agent's skills folder. Without the MCP server, the `aiseewhy-audit` skill still works through the public API or its local script.

### Codex

Skills: copy the folders into your Codex skills folder (user level `~/.codex/skills/`, or the repository's skills folder; check the Codex docs for your version), or use `npx skills add aiseewhy/aiseewhy-plugin`.

MCP server, in `~/.codex/config.toml`:

```toml
[mcp_servers.aiseewhy]
url = "https://api.aiseewhy.com/mcp"
http_headers = { "x-api-key" = "asw_..." }
```

### Cursor

Skills: copy the folders into the project's `.cursor/skills/` (or install with `npx skills add aiseewhy/aiseewhy-plugin`). Agents without skill support can be pointed at a `SKILL.md` from their rules file.

MCP server, in `.cursor/mcp.json`:

```json
{ "mcpServers": { "aiseewhy": { "url": "https://api.aiseewhy.com/mcp",
  "headers": { "x-api-key": "${env:AISEEWHY_API_KEY}" } } } }
```

### Any agent, no install

```sh
python3 plugins/aiseewhy/skills/aiseewhy-audit/scripts/local_check.py https://example.com/page
```

Read-only GET requests from your own machine; findings, never a score. More docs: https://aiseewhy.com/docs/?utm_source=plugin&utm_medium=integration&utm_campaign=readme#agents

## Listing checklist (maintainers)

| Where | What it needs |
|---|---|
| This GitHub repo | README, LICENSE, tagged release per version; topics `claude-code-plugin`, `agent-skills`, `mcp` |
| Claude Code community marketplaces and plugin directories | `.claude-plugin/marketplace.json` at the repo root; a PR or form with the repo URL, short description, category |
| Anthropic's official plugin directory | Plugin submission form; passes `claude plugin validate`; clear privacy and data-handling notes (the MCP server receives the audited URL) |
| Agent Skills directories (`npx skills`, community skill indexes) | `skills/<name>/SKILL.md` with valid frontmatter; most index from GitHub automatically or via a PR |
| Codex and Cursor skill and MCP listings | Repo URL, SKILL.md, the MCP config snippets above; Cursor's MCP directory wants a one-click install link |
| Official MCP Registry | Server entry `com.aiseewhy/aiseewhy`; bump its version when tools change |
| Awesome lists (Claude Code, MCP, Agent Skills) | PR with one line: name, link, one-sentence description |

Before any listing: run `claude plugin validate .` and `claude plugin validate plugins/aiseewhy`, run the local check against a test site, and confirm the pricing text in `plugins/aiseewhy/README.md` still matches https://aiseewhy.com/pricing/?utm_source=plugin&utm_medium=integration&utm_campaign=readme.

The skills and the script are MIT licensed; the AISeeWhy service has its own [terms](https://aiseewhy.com/terms/).
