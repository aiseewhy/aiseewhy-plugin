---
name: ai-crawler-policy
description: "Decide which AI crawlers a site lets in (training, AI search, user-triggered fetches) and write the robots.txt and Content-Signal lines that say so, then check them against the live site. Use when someone wants to block AI training but stay in AI answers, or asks what to put in robots.txt for GPTBot, ClaudeBot, PerplexityBot or Google-Extended."
---

# AI crawler policy

## Goal

A robots.txt that matches what the site owner actually wants: usually "stay visible in AI answers", sometimes also "do not train on my content". Many sites block AI search by accident while trying to block training.

## The three kinds of AI crawlers

| Kind | Tokens | Effect of blocking |
| --- | --- | --- |
| AI search | OAI-SearchBot, Claude-SearchBot, PerplexityBot (plus Googlebot, Bingbot, Applebot for search engines) | The site stops appearing and being cited in that AI search |
| User fetch | ChatGPT-User, Claude-User, Perplexity-User | The assistant cannot open the page when a person asks about it |
| Training | GPTBot, ClaudeBot, Google-Extended, Applebot-Extended, CCBot, Bytespider, Meta-ExternalAgent | Content is not used to train models; answers are not affected |

Google-Extended and Applebot-Extended are robots.txt tokens only: they never fetch pages, and blocking them does not remove the site from Google Search or AI Overviews.

## Tools (AISeeWhy MCP)

- `audit_url(url)`: shows what each crawler is allowed by robots.txt and what it actually receives (a firewall can block what robots.txt allows).
- `explain_finding("robots.no_content_signal")` and other robots findings.

## Workflow

1. **Ask one question** if the user has not said it: should AI companies be allowed to train on the content? Default when unsure: allow search and user crawlers, decide training separately.
2. **Read the current robots.txt** (in the repository, or fetch `/robots.txt`) and run `audit_url` on the home page to see the live result.
3. **Write the policy.** Keep existing rules for other bots. Give each AI token its own group so a `User-agent: *` rule cannot catch it by accident. Example for "visible in answers, no training":

```
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
Allow: /

User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: CCBot
Disallow: /

User-agent: *
Content-Signal: search=yes, ai-input=yes, ai-train=no
Allow: /
```

   `Content-Signal` states the same preference in words crawlers can read (search, ai-input, ai-train). Keep the `Sitemap:` line.
4. **Apply it** where the file lives (static file, framework config or CMS setting), show the diff.
5. **Check the result** after deploy with `audit_url`: robots findings should be gone for search and user crawlers, and the access table should show them reaching the page. If robots.txt allows them but they are still blocked, it is a firewall: switch to the `fix-blocked-ai-crawler` skill.

## Report to the user

The policy in one sentence, the robots.txt diff, and the before and after access table for the crawlers that changed.
