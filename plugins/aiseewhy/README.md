# AISeeWhy for Claude Code

Can ChatGPT, Claude and Perplexity read your page? This plugin lets your agent find out and fix it.

It connects the hosted AISeeWhy MCP server, which fetches a page as 16 AI and search crawlers next to a real browser, reads robots.txt as RFC 9309 says, and reports what blocks each crawler with a ready-to-paste fix. Six skills guide the agent from the check to a verified fix, and a seventh crawls the whole site for classic SEO problems. In Claude Desktop and ChatGPT the `show_ai_crawler_check` tool shows the result as a visual card (score, AI crawler access, the costliest finding with its fix); Claude Code gets the same result as text.

## What you can ask

- "Can ChatGPT and Perplexity read https://example.com/pricing?"
- "Something blocks ClaudeBot on my site. Find it, fix it and prove it works."
- "Block AI training but keep us in AI answers. Update robots.txt."
- "Write an llms.txt for this site."
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
- **store-structured-data**: product offers, merchant info (returns, shipping), prices in the page text, and the local business profile (LocalBusiness markup, phone, map listing, ratings shown on the page)

## API key

Without a paid plan the server gives a free preview: the score, the counts, the crawler table and the costliest finding (a P1 about an AI search or assistant crawler first, then P1, P2, P3). For every finding with its fix, sitemap audits, site crawls, broken link checks, comparisons and monitoring, choose a plan at https://aiseewhy.com/pricing/ (from $22 a month), create a key in your account at https://aiseewhy.com/account/ and set it before starting Claude Code. One page's full report is also sold once ($29 on the website, no subscription, no API key). A sample of the full report: https://aiseewhy.com/example-report/.

Set the key like this:

```sh
export AISEEWHY_API_KEY=asw_…
```

## Links

- [AISeeWhy](https://aiseewhy.com)
- [API and MCP docs](https://aiseewhy.com/docs/)
- [Privacy](https://aiseewhy.com/privacy/) · [Terms](https://aiseewhy.com/terms/)
- Support: support@aiseewhy.com
