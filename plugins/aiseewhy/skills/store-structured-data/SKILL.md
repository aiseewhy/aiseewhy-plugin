---
name: store-structured-data
description: "Check and fix the structured data of shop and local business pages: Product offers (price, currency, availability), merchant info (return policy, shipping), the price shown in the page text, LocalBusiness markup (address, phone, opening hours, geo, map listing) and ratings or reviews that match what the page shows. Use for product, category or location pages, or when an audit reports schema.offer_*, schema.merchant_info_missing, content.price_not_in_text, schema.local_business_*, schema.nap_mismatch, schema.no_map_profile, schema.rating_not_visible or schema.reviews_no_markup."
---

# Store and local business structured data

## Goal

Markup that says the same as the page, complete enough for shopping results, maps and AI assistants to use it: what is sold, at what price, whether it is in stock, how returns and shipping work, and where the business is. Fix it in the template that prints the JSON-LD, from the page's own data. Never add a fact the page does not state.

## Tools (AISeeWhy MCP)

- `audit_url(url, language)`: reads the server's HTML (what crawlers without JavaScript read) and reports the findings below with the evidence and a JSON-LD skeleton to fill.
- `explain_finding(finding_id, language)`: what a finding means and how to fix it.

Without a paid plan `audit_url` shows the costliest finding in full and the rest only by priority. Every finding with its fix comes with a paid plan (from $22 a month at https://aiseewhy.com/pricing/, its API key set as `AISEEWHY_API_KEY`) or a one-time full report of the page ($29 on the website, no subscription). A sample of the full report: https://aiseewhy.com/example-report/. Never invent the hidden findings.

## What the audit checks

The price check covers every `Product` and `ProductGroup` offer in the markup; the other product checks count only the page's own products (a top-level `Product` or the page's `mainEntity`, not the products of a category list). All checks read the server's HTML; the ones that compare markup with the page text (price, ratings, local business) skip a page with almost no text, where `content.js_only` is the finding that matters.

| Finding | Priority | Fires when | Fix |
|---|---|---|---|
| `schema.offer_no_price` | P2 | a Product offer has no price | `price` (or `priceSpecification.price`) on every offer |
| `schema.offer_incomplete` | P2 | an offer has no `priceCurrency`, or no `availability` (an `AggregateOffer` needs no availability) | ISO currency code and a schema.org availability URL |
| `schema.merchant_info_missing` | P2 | no `hasMerchantReturnPolicy` and/or no `shippingDetails`, neither on the offers nor for the whole shop (Organization or OnlineStore) | a `MerchantReturnPolicy` and `OfferShippingDetails`, once on the Organization when they apply to the whole shop |
| `content.price_not_in_text` | P2 | the markup has a price that the page text never shows (for example only in an image) | print the price as text near the product name |
| `schema.rating_not_visible` | P2 | `AggregateRating` values or `Review` texts in the markup do not appear on the page | show them on the page, or remove them from the markup |
| `schema.reviews_no_markup` | P3 | a product page shows two or more review blocks but has no review markup | `aggregateRating` / `review` from the reviews shown |
| `schema.local_business_missing` | P2 | the page shows a map, or opening hours with a phone or an address, and has no LocalBusiness (or Organization with an address) | a LocalBusiness subtype with name, address, phone, hours, geo |
| `schema.local_business_incomplete` | P3 | a LocalBusiness with an address lacks `telephone`, opening hours or `geo` | add the missing ones from the page |
| `schema.nap_mismatch` | P2 | the phone in the markup is not any phone the page shows | one phone number, the same in markup and text |
| `schema.no_map_profile` | P3 | the business links to no map listing | the listing URL in `sameAs` and `hasMap` |

P1 stays for what closes a page to search or AI (a blocked crawler, noindex, text only after JavaScript); these findings never outrank that.

## Workflow

1. **Audit** the product or location page (and one category page if the user sells many products). Read the evidence: it names the missing fields, the prices or phones found and where.
2. **Find the template** that prints the JSON-LD (theme snippet, product component, CMS or shop plugin setting). One template usually serves every product page; fix it there, not per page.
3. **Fill from real data.** Price, currency and availability from the product data; return days, countries and shipping costs from the shop's own policy pages. If the policy is not written anywhere, ask the user instead of guessing. Ratings only when the page shows them.
4. **Keep markup and page in step.** A price, rating or phone in the markup must appear in the visible text; the audit reports any that does not.
5. **Check again** after deploy with `audit_url`; the findings should be gone. Mention that Google's Rich Results Test validates the markup against Google's own rules.

## Report

- Which findings were on the page, with the evidence (missing fields, prices or phones found).
- The template or setting changed and the diff.
- What is still open and why (for example: no written return policy yet).

Structured data makes the page easier to read for search, shopping and AI surfaces. It does not guarantee rich results, a map listing or a citation; say so if the user expects that.
