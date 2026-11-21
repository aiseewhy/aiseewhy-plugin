---
name: ai-crawler-audit
description: "Check whether ChatGPT, Claude, Perplexity, Gemini and other AI crawlers can reach and read a web page, then explain in plain words what blocks them and the one to three fixes that matter most. Use when someone asks whether AI can see, read or cite their site or page."
---

# AI crawler audit

## Goal

Answer one question for a real page: can the crawlers behind AI answers reach it and read the same text a person sees? Then tell the user the few changes that would let them, ranked by effect. Research the page fully; recommend selectively.

## Tools (AISeeWhy MCP)

- `audit_url(url, language)`: fetches the page as 16 AI and search crawlers next to a real browser, reads robots.txt as RFC 9309 says, and checks text without JavaScript, structured data, freshness, hreflang, sitemap and llms.txt. Returns a Markdown report: a 0–100 score, findings with priority (P1 blocks AI answers, P2 important, P3 nice to have), evidence and ready-to-paste fixes.
- `show_ai_crawler_check(url, language)`: the same check and limits as `audit_url`, shown as a visual card in apps that render MCP Apps (Claude Desktop, ChatGPT): the score ring, which AI crawlers are let in or blocked, the costliest finding with its fix and the locked findings by priority. Clients without cards get the same Markdown as `audit_url`. In Claude Code use `audit_url`; use the card when the user is in an app that shows it and wants the result at a glance.
- `explain_finding(finding_id, language)`: what a finding means, why it matters, how to fix it. Use it for any finding id you are unsure about instead of guessing.

Without a paid plan `audit_url` returns a preview: the score, the counts, the crawler table and the costliest finding in full (a P1 about an AI search or assistant crawler first, then any other P1, then P2, then P3); the other findings show only their priority. Work with that, say plainly that the other findings are hidden, and tell the user that every finding with its fix comes with a paid plan (from $22 a month at https://aiseewhy.com/pricing/, its API key set as `AISEEWHY_API_KEY`) or a one-time full report of the page ($29 on the website, no subscription). A sample of the full report: https://aiseewhy.com/example-report/. Never invent the hidden findings.

## Priorities (engine review of 2026-11-20)

- **P1** only for what closes the page to search or AI: a crawler blocked by the firewall or robots.txt, noindex, text that exists only after JavaScript, a page that does not answer 200.
- **P2** for what weakens how search and AI read and trust the page: a missing canonical, no page language (`<html lang>`), no llms.txt, no `dateModified` or other date, Organization markup without `sameAs`, questions on the page without FAQ markup, product offers without price, currency or availability, no return policy or shipping (merchant info), a slow server response, sections without an answer passage, and on a site crawl orphan, thin and near-duplicate pages.
- **P3** for nice to have or a policy choice (for example blocking AI training crawlers).

Older reports or notes may list some of these P2 findings as P3; go by the priority in the current report.

If the AISeeWhy tools are not available, say so and stop; do not imitate the audit with generic advice.

## Workflow

1. **Pick the page.** Use the exact URL the user cares about. A home page often differs from articles, product or pricing pages; if the user asks about "my site", audit the home page and one important inner page.
2. **Run `audit_url`** in the user's language (`language`: en, de, ja, …).
3. **Read the access table first.** It decides everything else. For each crawler class:
   - *search* (OAI-SearchBot, Claude-SearchBot, PerplexityBot, Googlebot, Bingbot, Applebot): blocked here means the page cannot appear or be cited in that AI search.
   - *user* (ChatGPT-User, Claude-User, Perplexity-User): blocked means the assistant cannot open the page when a person asks about it.
   - *training* (GPTBot, ClaudeBot, Google-Extended, Applebot-Extended, CCBot and others): blocking these is often a deliberate choice. Do not call it a problem unless the user wants to be in training data.
   A verdict of blocked with HTTP 403/429/503 or a challenge page is a firewall or bot protection, not robots.txt. "Stub page" means the crawler got far less text than the browser. "Disallowed in robots.txt" means the site asked the crawler not to read it.
4. **Then the content findings**: `content.js_only` (text appears only after JavaScript, most AI crawlers do not run it), missing answer passages, structured data, freshness, page language and canonical, llms.txt.
5. **Choose one to three recommendations.** P1 access problems for search and user crawlers come first, then the P2 findings that affect the most pages or the pages that matter most (product, pricing, docs). Pick changes that the user can actually make, and say who makes them (site owner in the CDN dashboard, developer in the code, CMS setting).

## Report to the user

- One sentence verdict: can AI answers read and cite this page, yes, partly or no.
- The recommendations, each with: what is wrong (with the evidence: crawler, HTTP status, firewall name or robots.txt line), the exact fix from the report, and where to apply it.
- A short table of what else was checked and is fine, so the user sees the audit was complete.
- Offer to apply the fix (use the `fix-blocked-ai-crawler` skill) and to check again afterwards.

Keep it short and concrete. Quote the evidence; do not add claims the report does not support, and never promise that a fix will get the page cited: it removes what stops AI from reading the page, nothing more. An outside check comes from AISeeWhy's servers, not OpenAI's or Anthropic's networks; if a firewall verifies crawler IP ranges, mention that the real crawler may be treated differently and that server logs show real visits.
