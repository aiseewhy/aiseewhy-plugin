---
name: llms-txt
description: "Write or fix a site's llms.txt (the llmstxt.org format: a Markdown map of the pages that matter, for AI assistants) from its real pages, place it at /llms.txt and check it. Use when someone asks for an llms.txt, or an audit reported llms.missing or llms.page_not_listed."
---

# llms.txt

## Goal

A short, accurate `/llms.txt` that points AI assistants to the pages that answer real questions about the site. Be honest with the user about its weight: it is a convenience for assistants and agents, not a ranking factor, and no major AI search crawler has said it relies on it. It never fixes a blocked crawler.

## Format (llmstxt.org)

```
# Site or product name

> One or two sentences: what it is and for whom.

Optional paragraph with key facts (pricing model, regions, what it does not do).

## Docs
- [Getting started](https://example.com/docs/start): what a reader finds there
- [API reference](https://example.com/docs/api): endpoints and limits

## Optional
- [Blog](https://example.com/blog/): longer guides
```

One H1, one blockquote summary, then H2 sections of Markdown links with a short description each. Absolute URLs. The `## Optional` section holds what can be skipped when context is short.

## Tools (AISeeWhy MCP)

- `audit_url(url)`: reports `llms.missing` or `llms.page_not_listed` and checks the format once the file is live.

## Workflow

1. **Collect the real pages**: the sitemap, the main navigation, docs, pricing, about, contact, the most useful guides. Read each page you list; describe what it actually says.
2. **Draft the file.** 10–40 links is typical. Pricing, product facts and docs first. No marketing claims the pages do not make.
3. **Place it** where the site serves `/llms.txt` (static folder, framework route or CMS file) and show the diff. If the site has many languages, write it in the main language and link the language versions.
4. **Check** after deploy: fetch `/llms.txt` (status 200, `text/plain` or `text/markdown`) and run `audit_url` on the home page; the llms findings should be gone.
