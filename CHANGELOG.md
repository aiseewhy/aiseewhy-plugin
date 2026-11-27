# Changelog

## 1.4.0 (2026-11-27)

- New skill `aiseewhy-audit`: the AI crawler access check without the MCP server. It calls the public API (`POST https://api.aiseewhy.com/v1/audit`) or runs the bundled `scripts/local_check.py` (Python 3 standard library, GET requests only): robots.txt per crawler, the page fetched with each crawler's documented user agent, noindex, canonical, page language, JSON-LD and llms.txt. Findings P1 to P3 with evidence, no score, and it says which mode produced the result.
- `ai-crawler-audit` now hands over to `aiseewhy-audit` when the AISeeWhy MCP tools are not connected, instead of stopping. The two skill descriptions are split: with MCP tools, and without them.
- Plugin manifest: privacy policy link and icon.
- README: install for Codex and Cursor (skills and MCP config), the local check and its limits, and a listing checklist for maintainers.

## 1.3.0 (2026-11-20)

- `show_ai_crawler_check` card for Claude Desktop and ChatGPT, described in `ai-crawler-audit`.

Earlier versions: see the repository history.
