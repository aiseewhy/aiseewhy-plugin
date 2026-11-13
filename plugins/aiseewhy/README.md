# AISeeWhy for Claude Code

Can ChatGPT, Claude and Perplexity read your page? This plugin lets your agent find out and fix it.

It connects the hosted AISeeWhy MCP server, which fetches a page as 16 AI and search crawlers next to a real browser, reads robots.txt as RFC 9309 says, and reports what blocks each crawler with a ready-to-paste fix. Five skills guide the agent from the check to a verified fix.

## What you can ask

- "Can ChatGPT and Perplexity read https://example.com/pricing?"
- "Something blocks ClaudeBot on my site. Find it, fix it and prove it works."
- "Block AI training but keep us in AI answers. Update robots.txt."
- "Write an llms.txt for this site."
- "Audit our sitemap for AI crawlers, compare us with competitor.com and monitor the key pages."

## Included skills

- **ai-crawler-audit**: check one page and explain the one to three fixes that matter
- **fix-blocked-ai-crawler**: find where the block lives (firewall, robots.txt, JavaScript rendering), apply the fix, audit again
- **ai-crawler-policy**: choose which AI crawlers to allow and write robots.txt and Content-Signal
- **llms-txt**: write or fix /llms.txt from the site's real pages
- **ai-readiness-report**: sitemap audit, competitor comparison and monitoring in one report (needs a key)

## API key

Without a key the server gives a free preview: the score, the counts and the first finding. For every finding with its fix, sitemap audits, comparisons and monitoring, create a key in your account at https://aiseewhy.com/account/ (7-day free trial, no card) and set it before starting Claude Code:

```sh
export AISEEWHY_API_KEY=asw_…
```

## Links

- [AISeeWhy](https://aiseewhy.com)
- [API and MCP docs](https://aiseewhy.com/docs/)
- [Privacy](https://aiseewhy.com/privacy/) · [Terms](https://aiseewhy.com/terms/)
- Support: support@aiseewhy.com
