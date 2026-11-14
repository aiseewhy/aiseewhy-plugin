---
name: seo-site-audit
description: "Crawl a whole site for classic SEO problems (broken and redirected internal links, duplicate titles and descriptions, orphan, deep and thin pages, noindex or redirected URLs in the sitemap, missing titles, descriptions, H1, canonical and alt text) and fix what the repository controls. Use for a technical SEO audit, a site health check, or 'find broken links on my site'. Needs an AISeeWhy API key."
---

# SEO site audit

## Goal

A short list of site-wide fixes, ranked by how many pages each one repairs, with the template or file to change. Most site-wide SEO problems come from one template, one navigation component or one sitemap generator; find that shared cause instead of patching pages one by one.

## Tools (AISeeWhy MCP, API key required)

- `crawl_site(url, max_pages)`: crawls up to 50 pages from a start page by following internal links, then the sitemap, as a browser and respecting robots.txt. Returns site findings (`crawl.*`) with the affected pages, and on-page SEO findings (`seo.*`) counted across pages. In the AISeeWhy account the same audit goes up to 500 pages (Agency) with a CSV of every page.
- `audit_url(url)`: one page in depth. Its report has a "Classic SEO" block with its own score, separate from the AI readiness score, and checks up to 30 internal links of that page.
- `explain_finding(finding_id)`: what a `crawl.*` or `seo.*` finding means and why it matters.

If a tool answers that it needs an API key, tell the user: a key comes with the free 7-day trial at https://aiseewhy.com/account/ and is set as `AISEEWHY_API_KEY`. Do not guess the results.

## Workflow

1. **Crawl.** Start from the home page unless the user names a section. Say how many pages were crawled and whether the crawl stopped at the limit; findings cover only the crawled pages.
2. **Group by cause.** For each finding, look at the listed pages: the same problem on every page of one type points to a template; broken links reached from many pages point to navigation, a footer or a related-links block; sitemap problems point to the sitemap generator.
3. **Fix in the repository** when it is open: find the template, component, route or sitemap config that produces the problem, change it, and show the diff. Typical fixes:
   - broken internal links: update or remove the link, or add a redirect from the old URL;
   - links to redirects: point them at the final URL;
   - duplicate titles or descriptions: build them from each page's own data;
   - missing title, description, H1, canonical or alt text: add them to the template, from the page's data;
   - noindex or redirected URLs in the sitemap: filter them out of the sitemap generator;
   - orphan pages: link them from a hub or related pages, or drop them from the sitemap if they should not exist.
   Never change a production firewall, CDN or CMS setting without the user's go-ahead.
4. **Check again** after deploy: run `crawl_site` again and compare the counts.

## Report

- One sentence with the verdict, pages crawled and the site SEO score.
- The one to three fixes that repair the most pages, each with the evidence (finding id, example URLs, the page that links to a broken one) and the diff or exact change.
- A table of everything else: finding, pages affected, priority, cause.

All numbers come from the tool output. This audit checks how the site is built for search engines; it does not measure rankings, traffic or backlinks.
