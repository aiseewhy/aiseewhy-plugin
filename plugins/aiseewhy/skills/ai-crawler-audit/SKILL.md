---
name: ai-crawler-audit
description: "Check whether ChatGPT, Claude, Perplexity, Gemini and other AI crawlers can reach and read a web page, then explain in plain words what blocks them and the one to three fixes that matter most. Use when someone asks whether AI can see, read or cite their site or page."
---

# AI crawler audit

## Goal

Answer one question for a real page: can the crawlers behind AI answers reach it and read the same text a person sees? Then tell the user the few changes that would let them, ranked by effect. Research the page fully; recommend selectively.

## Tools (AISeeWhy MCP)

- `audit_url(url, language)`: fetches the page as 16 AI and search crawlers next to a real browser, reads robots.txt as RFC 9309 says, and checks text without JavaScript, structured data, freshness, hreflang, sitemap and llms.txt. Returns a Markdown report: a 0–100 score, findings with priority (P1 blocks AI answers, P2 important, P3 nice to have), evidence and ready-to-paste fixes.
- `explain_finding(finding_id, language)`: what a finding means, why it matters, how to fix it. Use it for any finding id you are unsure about instead of guessing.

Without an API key `audit_url` returns a preview: the score, the counts and the first finding. Work with that, say plainly that the other findings are hidden, and tell the user a key (free 7-day trial at https://aiseewhy.com/account/, set as `AISEEWHY_API_KEY`) shows every finding with its fix. Never invent the hidden findings.

If the AISeeWhy tools are not available, say so and stop; do not imitate the audit with generic advice.

## Workflow

1. **Pick the page.** Use the exact URL the user cares about. A home page often differs from articles, product or pricing pages; if the user asks about "my site", audit the home page and one important inner page.
2. **Run `audit_url`** in the user's language (`language`: en, de, ja, …).
3. **Read the access table first.** It decides everything else. For each crawler class:
   - *search* (OAI-SearchBot, Claude-SearchBot, PerplexityBot, Googlebot, Bingbot, Applebot): blocked here means the page cannot appear or be cited in that AI search.
   - *user* (ChatGPT-User, Claude-User, Perplexity-User): blocked means the assistant cannot open the page when a person asks about it.
   - *training* (GPTBot, ClaudeBot, Google-Extended, Applebot-Extended, CCBot and others): blocking these is often a deliberate choice. Do not call it a problem unless the user wants to be in training data.
   A verdict of blocked with HTTP 403/429/503 or a challenge page is a firewall or bot protection, not robots.txt. "Stub page" means the crawler got far less text than the browser. "Disallowed in robots.txt" means the site asked the crawler not to read it.
4. **Then the content findings**: `content.js_only` (text appears only after JavaScript, most AI crawlers do not run it), missing answer-first text, structured data, freshness, llms.txt.
5. **Choose one to three recommendations.** P1 access problems for search and user crawlers come first. Pick changes that the user can actually make, and say who makes them (site owner in the CDN dashboard, developer in the code, CMS setting).

## Report to the user

- One sentence verdict: can AI answers read and cite this page, yes, partly or no.
- The recommendations, each with: what is wrong (with the evidence: crawler, HTTP status, firewall name or robots.txt line), the exact fix from the report, and where to apply it.
- A short table of what else was checked and is fine, so the user sees the audit was complete.
- Offer to apply the fix (use the `fix-blocked-ai-crawler` skill) and to check again afterwards.

Keep it short and concrete. Quote the evidence; do not add claims the report does not support. An outside check comes from AISeeWhy's servers, not OpenAI's or Anthropic's networks; if a firewall verifies crawler IP ranges, mention that the real crawler may be treated differently and that server logs show real visits.
