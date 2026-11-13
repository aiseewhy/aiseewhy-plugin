---
name: ai-readiness-report
description: "Audit many pages of a site from its sitemap, compare it with up to two competitors, and set up monitoring, then deliver a one-page report on how ready the site is for AI search and what to fix first. Use for a site-wide AI search / AEO / GEO audit, a client report, or a competitor comparison. Needs an AISeeWhy API key."
---

# AI readiness report

## Goal

A site-level answer for an owner or a client: which page types AI crawlers can and cannot read, how the site compares with its competitors, and the one to three fixes that unlock the most pages. Recommend selectively; one fix in a shared template or firewall rule often repairs hundreds of pages.

## Tools (AISeeWhy MCP, API key required)

- `audit_sitemap(sitemap_url, max_urls)`: audits pages from a sitemap or sitemap index; returns a P1/P2/P3 line per page and full reports for pages with findings.
- `compare_urls(urls)`: 2–3 pages side by side (score, findings, blocked crawlers, llms.txt, structured data, text without JavaScript). Put the user's page first.
- `audit_url(url)`: one page in depth.
- `watch_site(url, freq)` and `list_watched_sites()`: scheduled checks with an email when a new P1 appears or the score drops by 10 or more.
- `explain_finding(finding_id)`.

If a tool answers that it needs an API key, tell the user: a key comes with the free 7-day trial at https://aiseewhy.com/account/ and is set as `AISEEWHY_API_KEY`. Do not continue with guesses.

## Workflow

1. **Scope.** Find the sitemap (`/sitemap.xml`, or the `Sitemap:` line in robots.txt). Choose `max_urls` so each page type (home, product, pricing, docs, articles, categories, locations) is represented.
2. **Run `audit_sitemap`.** Group the results by page type and by finding id. A finding on every page of one type points to a shared cause (template, rendering, firewall rule); say which.
3. **Compare.** Ask the user for one or two competitors if they did not name any; run `compare_urls` on equivalent pages (home vs home, pricing vs pricing).
4. **Choose the fixes.** Rank by pages affected times severity: P1 access problems for search and user crawlers first, then JavaScript-only content, then the rest. One to three recommendations; everything else goes in a "checked, not urgent" table with a reason.
5. **Offer monitoring** for the key pages with `watch_site` (weekly by default; daily for pages that change often). Add only the pages the user agrees to.

## Report

- Verdict in one sentence, then a table: page type, pages checked, pages fully readable by AI search crawlers, main problem.
- The recommendations with evidence (finding ids, crawlers, status codes, example URLs) and the exact fix from the reports.
- The competitor table and one sentence on what they do better or worse.
- What is monitored from now on.

All numbers come from the tool output. Do not estimate traffic or citations; this audit measures access and readability, not rankings.
