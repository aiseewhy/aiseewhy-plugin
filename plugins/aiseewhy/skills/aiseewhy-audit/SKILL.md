---
name: aiseewhy-audit
description: "Check AI crawler access to a web page without the AISeeWhy MCP tools: through the AISeeWhy public API, or with a bundled local read-only script (robots.txt per crawler, the page fetched as GPTBot, OAI-SearchBot, ClaudeBot, PerplexityBot and others, noindex, canonical, page language, JSON-LD, llms.txt). Use when the audit_url tool is not connected, the agent has this skill but no MCP server set up (for example Codex or Cursor installed with skills only), the service answers with an error or a daily limit, or the user asks for a local, offline or no-third-party check. When the AISeeWhy MCP tools are connected, use ai-crawler-audit instead."
license: MIT
metadata:
  author: AISeeWhy
  homepage: https://aiseewhy.com/?utm_source=plugin&utm_medium=integration&utm_campaign=aiseewhy-audit
  version: "1.4.0"
---

# AISeeWhy audit

## Goal

Answer one question for a real page: can the crawlers behind AI answers reach it and read the text a person sees? Then give the one to three changes that would let them, ranked P1 to P3, each with its evidence and the exact fix. Report what was checked; never claim more.

Honesty rules, always:

- Do not lead with or make up a score. Findings and evidence are the result. If a report contains AISeeWhy's 0-100 index and the user asks for it, give it and say it is a checklist index, not a measure or forecast of citations.
- Never promise that a fix gets the page cited. Removing a block lets AI read the page; whether it is cited also depends on the content, the query and the assistant.
- Never invent findings that a tool did not return (including findings hidden in a free preview).
- Say which mode produced the result: AISeeWhy service (MCP or API) or local checks.

## Pick the mode

1. **AISeeWhy MCP tools connected** (`audit_url`, `explain_finding`, ...): this skill is not needed; follow the `ai-crawler-audit` skill, which runs the full check through them. Agents without that skill: call `audit_url(url, language)` and use `explain_finding(finding_id, language)` for any finding id you are unsure about; in apps that render MCP Apps `show_ai_crawler_check` shows the same check as a card.
2. **No MCP tools, but network access**: call the public API (below). Same check as the MCP server.
3. **The API errors or hits its daily limit, the agent has no network to the API, or the user does not want a third-party service**: run the local checks (below) and say plainly that they are a subset.

## Public API (no MCP)

```sh
curl -sS https://api.aiseewhy.com/v1/audit \
  -H 'content-type: application/json' \
  -H "x-api-key: ${AISEEWHY_API_KEY:-}" \
  -d '{"url":"https://example.com/pricing","markdown":true,"ref":"plugin"}'
```

An empty key is treated as no key (free preview).

Errors come back as JSON with an `error` field (422 bad URL, 429 daily limit). On 429 tell the user the free allowance for today is used and fall back to local checks.

## Free preview vs paid

Without a key, or with a key of a free account, the answer is a preview: the counts, the crawler access table and the costliest finding in full; the other findings show only their priority. A domain already checked for free returns that earlier result instead of a new check. Work with the preview, say plainly that the rest is hidden, and mention once, without pressure, that every finding with its fix comes with a plan at https://aiseewhy.com/pricing/?utm_source=plugin&utm_medium=integration&utm_campaign=aiseewhy-audit (key from https://aiseewhy.com/account/?utm_source=plugin&utm_medium=integration&utm_campaign=aiseewhy-audit, set as `AISEEWHY_API_KEY`) or a one-time full report of the page on the website. Sample of a full report: https://aiseewhy.com/example-report/?utm_source=plugin&utm_medium=integration&utm_campaign=aiseewhy-audit.

## Local checks (fallback)

Run the bundled script (Python 3 standard library, read-only GET requests only):

```sh
python3 scripts/local_check.py https://example.com/page        # table + findings
python3 scripts/local_check.py https://example.com/page --json # for parsing
```

The path is relative to this skill's folder. If Python is not available, do the same by hand with curl:

```sh
curl -sS https://example.com/robots.txt
curl -sS -o /dev/null -w '%{http_code} %{size_download}\n' -A 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' https://example.com/page
curl -sS -o /dev/null -w '%{http_code} %{size_download}\n' -A 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-SearchBot/1.4; +https://openai.com/searchbot' https://example.com/page
curl -sS -o /dev/null -w '%{http_code} %{size_download}\n' -A 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Claude-SearchBot/1.0; +Claude-SearchBot@anthropic.com)' https://example.com/page
curl -sS -o /dev/null -w '%{http_code} %{size_download}\n' -A 'Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)' https://example.com/page
curl -sS -I https://example.com/llms.txt
```

Compare each crawler's status and size with a browser user agent. 403/429/503 or a challenge page ("Just a moment...", captcha) means a firewall or bot protection, not robots.txt.

What local checks cannot see, and you must say so: requests come from the user's own IP, not the crawlers' published IP ranges, so a firewall that verifies crawler IPs may treat the real crawler differently in either direction; JavaScript is not rendered; freshness, answer passages and deeper structured data checks are not done. Server logs show real crawler visits.

## Priorities

- **P1**, closes the page to AI search or assistants: a search or user crawler blocked by the firewall or robots.txt, `noindex`, main text present only after JavaScript, a page or robots.txt that does not answer properly (robots.txt 5xx makes crawlers treat the site as disallowed).
- **P2**, weakens how search and AI read the page: missing canonical, no `<html lang>`, no llms.txt, no date, no or thin structured data, product offers without price or availability, slow response.
- **P3**, nice to have or a policy choice, for example blocking training crawlers.

Crawler classes decide the weight:

- *search* (OAI-SearchBot, Claude-SearchBot, PerplexityBot, Googlebot, Bingbot, Applebot, DuckAssistBot): blocked means the page cannot be found or cited in that AI search.
- *user* (ChatGPT-User, Claude-User, Perplexity-User): blocked means the assistant cannot open the page when a person asks about it.
- *training* (GPTBot, ClaudeBot, Google-Extended, Applebot-Extended, CCBot): blocking them is often deliberate. Not a problem unless the user wants to be in training data. Blocking GPTBot does not remove a page from ChatGPT search; OAI-SearchBot does that.

llms.txt: a convenience map for assistants and agents, not a ranking factor, and it never fixes a blocked crawler. Access problems come first.

## Workflow

1. Use the exact URL the user cares about. For "my site", check the home page and one important inner page (pricing, product, docs, article).
2. Run the check in the chosen mode, in the user's language where the tool supports it.
3. Read the access table first; it decides everything else. Then the content findings.
4. Pick one to three recommendations: P1 for search and user crawlers first, then the P2 that affect the pages that matter most. Say who applies each fix (CDN or WAF dashboard, developer, CMS setting, for example Cloudflare, Shopify, WordPress).

## Report to the user

- Mode used (AISeeWhy service or local checks) and the URL checked.
- One-sentence verdict: can AI search and assistants read this page: yes, partly or no.
- The recommendations, each with priority, what is wrong, the evidence (crawler, HTTP status, robots.txt line, header) and the exact fix.
- A short list of what was checked and is fine, so the user sees the scope.
- What was not checked (preview limits or local-check limits).
- Offer to apply the fix and to check again afterwards.
