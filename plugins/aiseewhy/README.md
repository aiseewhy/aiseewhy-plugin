# AISeeWhy for Claude Code

Can ChatGPT, Claude and Perplexity read your page? This plugin lets your agent find out and fix it.

It connects the hosted AISeeWhy MCP server, which fetches a page as 16 AI and search crawlers next to a real browser, reads robots.txt as RFC 9309 says, and reports what blocks each crawler with a ready-to-paste fix. Six skills guide the agent from the check to a verified fix, a seventh crawls the whole site for classic SEO problems, and an eighth runs the access check without the MCP server (public API or a local read-only script). In Claude Desktop and ChatGPT the `show_ai_crawler_check` tool shows the result as a visual card (score, AI crawler access, the costliest finding with its fix); Claude Code gets the same result as text.

## Install

```
/plugin install aiseewhy --marketplace aiseewhy/aiseewhy-plugin
```

On older Claude Code versions: `/plugin marketplace add aiseewhy/aiseewhy-plugin`, then `/plugin install aiseewhy@aiseewhy`. Codex, Cursor and other agents: see the [repository README](../../README.md).

## What you can ask

- "Can ChatGPT and Perplexity read https://example.com/pricing?"
- "Something blocks ClaudeBot on my site. Find it, fix it and prove it works."
- "Block AI training but keep us in AI answers. Update robots.txt."
- "Write an llms.txt for this site."
- "Without any outside service, check whether robots.txt or our firewall blocks GPTBot and PerplexityBot."
- "Audit our sitemap for AI crawlers, compare us with competitor.com and monitor the key pages."
- "Crawl our site, find broken links and duplicate titles, and fix them in the templates."
- "Our product pages: are the offers, prices, returns and shipping in the markup, and does the page show the price?"

## Included skills

- **ai-crawler-audit**: check one page and explain the one to three fixes that matter
- **fix-blocked-ai-crawler**: find where the block lives (firewall, robots.txt, JavaScript rendering), apply the fix, audit again
- **ai-crawler-policy**: choose which AI crawlers to allow and write robots.txt and Content-Signal
- **llms-txt**: write or fix /llms.txt from the site's real pages
- **ai-readiness-report**: sitemap audit, competitor comparison and monitoring in one report (needs a key)
- **seo-site-audit**: crawl the site for broken links, duplicate titles, orphan pages and sitemap problems, and fix the shared cause (needs a key)
- **aiseewhy-audit**: the same access check when the MCP server is not connected: the public API, or `scripts/local_check.py` (Python 3 standard library, GET requests only) for a local, offline or no-third-party check; findings P1 to P3 with evidence, never a score
- **store-structured-data**: product offers, merchant info (returns, shipping), prices in the page text, and the local business profile (LocalBusiness markup, phone, map listing, ratings shown on the page)

## API key

Without a paid plan the server gives a free preview: the score, the counts, the crawler table and the costliest finding (a P1 about an AI search or assistant crawler first, then P1, P2, P3). For every finding with its fix, sitemap audits, site crawls, broken link checks, comparisons and monitoring, choose a plan at https://aiseewhy.com/pricing/?utm_source=plugin&utm_medium=integration&utm_campaign=readme (from $22 a month), create a key in your account at https://aiseewhy.com/account/?utm_source=plugin&utm_medium=integration&utm_campaign=readme and set it before starting Claude Code. One page's full report is also sold once ($29 on the website, no subscription, no API key). A sample of the full report: https://aiseewhy.com/example-report/?utm_source=plugin&utm_medium=integration&utm_campaign=readme.

Set the key like this:

```sh
export AISEEWHY_API_KEY=asw_…
```

## Local checks and their limits

`skills/aiseewhy-audit/scripts/local_check.py` reads robots.txt per crawler (RFC 9309 group matching), fetches the page with each crawler's documented user agent next to a browser user agent, and checks noindex, canonical, page language, JSON-LD and /llms.txt. Run it directly with `python3 skills/aiseewhy-audit/scripts/local_check.py https://example.com/page` (add `--json` for parsing). It runs from your own IP, not the crawlers' published IP ranges, so a firewall that verifies crawler IPs can treat the real crawler differently. It does not render JavaScript and does not check freshness or answer passages. Server logs show real crawler visits.

## Links

- [AISeeWhy](https://aiseewhy.com/?utm_source=plugin&utm_medium=integration&utm_campaign=readme)
- [API and MCP docs](https://aiseewhy.com/docs/?utm_source=plugin&utm_medium=integration&utm_campaign=readme)
- [Privacy](https://aiseewhy.com/privacy/) · [Terms](https://aiseewhy.com/terms/)
- Support: support@aiseewhy.com
