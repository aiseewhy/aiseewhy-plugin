#!/usr/bin/env python3
"""Local fallback for the aiseewhy-audit skill: read-only GET checks of one page from this machine.

Python 3.9+ standard library only. Usage: python3 local_check.py https://example.com/page [--json]

What it checks: robots.txt (RFC 9309 group matching, longest match, Allow wins a tie, * and $), the page fetched
with each AI crawler's documented user agent next to a desktop browser user agent (HTTP status, bytes, visible text,
challenge pages), noindex (meta and X-Robots-Tag), canonical, <html lang>, JSON-LD, and /llms.txt.

What it cannot check: requests come from this machine's IP, not the crawlers' published IP ranges, so a firewall
that verifies crawler IPs may treat the real crawler differently; JavaScript is not run, so "browser" means a
browser user agent, not a rendered page. It gives findings, never a score.
"""
from __future__ import annotations

import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urlsplit

TIMEOUT = 20
MAX_BYTES = 3_000_000
BROWSER_UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/131.0.0.0 Safari/537.36")

# (name, robots.txt token, documented user agent or None when the vendor documents only a token, class)
# class: search = AI search / search engines, user = fetches when a person asks an assistant, training = model training
CRAWLERS = [
    ("OAI-SearchBot", "OAI-SearchBot", "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-SearchBot/1.4; +https://openai.com/searchbot", "search"),
    ("ChatGPT-User", "ChatGPT-User", "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot", "user"),
    ("GPTBot", "GPTBot", "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.4; +https://openai.com/gptbot", "training"),
    ("Claude-SearchBot", "Claude-SearchBot", "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Claude-SearchBot/1.0; +Claude-SearchBot@anthropic.com)", "search"),
    ("Claude-User", "Claude-User", "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Claude-User/1.0; +Claude-User@anthropic.com)", "user"),
    ("ClaudeBot", "ClaudeBot", "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; ClaudeBot/1.0; +claudebot@anthropic.com)", "training"),
    ("PerplexityBot", "PerplexityBot", "Mozilla/5.0 (compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)", "search"),
    ("Perplexity-User", "Perplexity-User", "Mozilla/5.0 (compatible; Perplexity-User/1.0; +https://perplexity.ai/perplexity-user)", "user"),
    ("Googlebot", "Googlebot", "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)", "search"),
    ("Bingbot", "bingbot", "Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)", "search"),
    ("Applebot", "Applebot", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15 (Applebot/0.1; +http://www.apple.com/go/applebot)", "search"),
    ("DuckAssistBot", "DuckAssistBot", "DuckAssistBot/1.2; (+http://duckduckgo.com/duckassistbot.html)", "search"),
    ("Google-Extended", "Google-Extended", None, "training"),
    ("Applebot-Extended", "Applebot-Extended", None, "training"),
    ("CCBot", "CCBot", "CCBot/2.0 (https://commoncrawl.org/faq/)", "training"),
]

CHALLENGE = re.compile(r"just a moment\.\.\.|cf-chl-|challenge-platform|attention required|captcha|"
                       r"access denied|verify you are human|ddos-guard|perimeterx|datadome", re.I)


def fetch(url: str, ua: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": ua, "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
                                               "Accept-Language": "en"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read(MAX_BYTES)
            return {"status": r.status, "final_url": r.geturl(), "headers": {k.lower(): v for k, v in r.headers.items()},
                    "body": body.decode(r.headers.get_content_charset() or "utf-8", "replace")}
    except urllib.error.HTTPError as e:
        body = e.read(MAX_BYTES) if e.fp else b""
        return {"status": e.code, "final_url": url, "headers": {k.lower(): v for k, v in (e.headers or {}).items()},
                "body": body.decode("utf-8", "replace")}
    except Exception as e:  # DNS, TLS, timeout, connection reset
        return {"status": None, "final_url": url, "headers": {}, "body": "", "error": f"{type(e).__name__}: {e}"}


# ---------- robots.txt, RFC 9309 ----------

def parse_robots(text: str) -> list[tuple[list[str], list[tuple[str, str]]]]:
    """Groups of (user agents, [(allow|disallow, path)]). Consecutive user-agent lines start one group."""
    groups: list[tuple[list[str], list[tuple[str, str]]]] = []
    agents: list[str] = []
    rules: list[tuple[str, str]] = []
    last_was_agent = False
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip().lower(), val.strip()
        if key == "user-agent":
            if not last_was_agent and (agents or rules):
                groups.append((agents, rules))
                agents, rules = [], []
            agents.append(val.lower())
            last_was_agent = True
        elif key in ("allow", "disallow"):
            if agents:
                rules.append((key, val))
            last_was_agent = False
        else:
            last_was_agent = False
    if agents:
        groups.append((agents, rules))
    return groups


def rules_for(groups, token: str) -> tuple[list[tuple[str, str]], str]:
    """All rules of the groups naming this token (merged, as RFC 9309 says), else of '*' groups."""
    tok = token.lower()
    named = [r for a, rs in groups if tok in a for r in rs]
    if any(tok in a for a, _ in groups):
        return named, token
    return [r for a, rs in groups if "*" in a for r in rs], "*"


def _pattern(path: str) -> re.Pattern:
    anchored = path.endswith("$")
    core = re.escape(path[:-1] if anchored else path).replace(r"\*", ".*")
    return re.compile(core + ("$" if anchored else ""))


def allowed(rules: list[tuple[str, str]], path: str) -> tuple[bool, str | None]:
    best: tuple[int, int, str] | None = None  # (length, allow wins tie, line)
    for kind, p in rules:
        if not p:  # empty Disallow allows everything
            continue
        if _pattern(p).match(path):
            cand = (len(p), 1 if kind == "allow" else 0, f"{kind.capitalize()}: {p}")
            if best is None or cand[:2] > best[:2]:
                best = cand
    if best is None:
        return True, None
    return best[1] == 1, best[2]


# ---------- page ----------

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.text: list[str] = []
        self.skip = 0
        self.title = ""
        self._in_title = False
        self.lang = None
        self.canonical = None
        self.robots_meta: list[str] = []
        self.jsonld = 0

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang") or None
        elif tag in ("script", "style", "noscript", "template", "svg"):
            self.skip += 1
            if tag == "script" and "ld+json" in a.get("type", "").lower():
                self.jsonld += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonical = a.get("href")
        elif tag == "meta" and a.get("name", "").lower() in ("robots", "googlebot"):
            self.robots_meta.append(a.get("content", "").lower())

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "template", "svg") and self.skip:
            self.skip -= 1
        elif tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif not self.skip:
            self.text.append(data)

    def visible_chars(self) -> int:
        return len(re.sub(r"\s+", " ", " ".join(self.text)).strip())


def read_page(body: str) -> Page:
    p = Page()
    try:
        p.feed(body)
    except Exception:
        pass
    return p


def check(url: str) -> dict:
    if "://" not in url:
        url = "https://" + url
    parts = urlsplit(url)
    origin = f"{parts.scheme}://{parts.netloc}"
    path = (parts.path or "/") + (f"?{parts.query}" if parts.query else "")
    findings: list[dict] = []

    def add(priority, fid, what, evidence, fix):
        findings.append({"priority": priority, "id": fid, "what": what, "evidence": evidence, "fix": fix})

    # robots.txt
    rb = fetch(origin + "/robots.txt", BROWSER_UA)
    robots = {"status": rb["status"], "error": rb.get("error")}
    groups = []
    if rb["status"] == 200:
        groups = parse_robots(rb["body"])
        robots["sitemaps"] = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", rb["body"])
    elif rb["status"] and 500 <= rb["status"] < 600:
        add("P1", "robots.unreachable", "robots.txt answers a server error; under RFC 9309 crawlers treat the whole site as disallowed",
            f"GET /robots.txt -> HTTP {rb['status']}", "Serve robots.txt with HTTP 200 (or 404 if you want no rules).")

    # browser baseline
    base = fetch(url, BROWSER_UA)
    bpage = read_page(base["body"])
    bchars = bpage.visible_chars()
    if base["status"] != 200:
        add("P1", "page.status", "The page does not answer 200 to a browser user agent",
            f"HTTP {base['status']}{' ' + base.get('error', '') if base.get('error') else ''}", "Fix the page or check the URL.")

    rows = []
    for name, token, ua, cls in CRAWLERS:
        rules, group = rules_for(groups, token)
        ok, line = allowed(rules, path)
        row = {"crawler": name, "class": cls, "robots": "allowed" if ok else "disallowed",
               "robots_group": group, "robots_line": line}
        if ua:
            r = fetch(url, ua)
            pg = read_page(r["body"])
            chars = pg.visible_chars()
            challenge = bool(CHALLENGE.search(r["body"][:20000])) or "cf-mitigated" in r["headers"]
            verdict = "ok"
            if r["status"] is None:
                verdict = "error"
            elif r["status"] in (401, 403, 406, 429, 503) or challenge:
                verdict = "blocked (firewall or bot protection)"
            elif r["status"] != 200:
                verdict = f"HTTP {r['status']}"
            elif bchars > 500 and chars < bchars * 0.3:
                verdict = "stub (much less text than the browser got)"
            row.update({"http": r["status"], "text_chars": chars, "fetch": verdict,
                        "server": r["headers"].get("server"), "error": r.get("error")})
        else:
            row.update({"http": None, "text_chars": None, "fetch": "robots.txt token only (no user agent to send)"})
        rows.append(row)

        important = cls in ("search", "user")
        if not ok:
            add("P1" if important else "P3", "access.robots_disallow",
                f"{name} ({cls}) is disallowed in robots.txt" + ("" if important else "; a policy choice if you do not want model training"),
                f"group User-agent: {group}; matching rule {line}",
                f"Add `User-agent: {token}` with `Allow: /` (or remove the Disallow) if you want {name} to read the page.")
        if row.get("fetch", "").startswith("blocked") or row.get("fetch", "").startswith("stub"):
            add("P1" if important else "P3", "access.firewall",
                f"{name} ({cls}) got {row['fetch']}",
                f"HTTP {row['http']}, {row['text_chars']} text chars vs {bchars} for the browser UA, server: {row.get('server')}",
                "Allow verified AI crawlers in the CDN or WAF bot settings (for example Cloudflare's verified bots / AI crawl control) "
                "or add a skip rule for this user agent.")

    # page signals from the browser fetch
    xrobots = base["headers"].get("x-robots-tag", "").lower()
    if "noindex" in xrobots or any("noindex" in m for m in bpage.robots_meta):
        add("P1", "index.noindex", "The page asks search engines not to index it",
            f"X-Robots-Tag: {xrobots or '-'}; meta robots: {bpage.robots_meta or '-'}", "Remove noindex if the page should appear in search and AI answers.")
    if base["status"] == 200 and bchars < 300:
        add("P1", "content.js_only", "Very little text in the HTML; it may appear only after JavaScript, which most AI crawlers do not run",
            f"{bchars} visible text characters in the raw HTML", "Render the main content on the server (SSR or static HTML).")
    if base["status"] == 200 and not bpage.canonical:
        add("P2", "meta.canonical_missing", "No canonical link", "no <link rel=canonical>", "Add <link rel=\"canonical\" href=\"...\"> with the page's preferred URL.")
    if base["status"] == 200 and not bpage.lang:
        add("P2", "meta.lang_missing", "No page language", "<html> has no lang attribute", "Add lang to <html>, for example <html lang=\"en\">.")
    if base["status"] == 200 and bpage.jsonld == 0:
        add("P2", "schema.none", "No JSON-LD structured data on the page", "no <script type=application/ld+json>",
            "Add JSON-LD that matches the page (Organization, Article, Product, FAQPage...).")

    # llms.txt
    lt = fetch(origin + "/llms.txt", BROWSER_UA)
    llms = {"status": lt["status"]}
    ctype = lt["headers"].get("content-type", "")
    if lt["status"] == 200 and "html" not in ctype.lower() and lt["body"].lstrip().startswith("#"):
        llms.update({"found": True, "bytes": len(lt["body"]), "links": len(re.findall(r"\]\((https?://[^)]+)\)", lt["body"]))})
    else:
        llms["found"] = False
        add("P2", "llms.missing", "No usable /llms.txt", f"GET /llms.txt -> HTTP {lt['status']}, content-type {ctype or '-'}",
            "Publish /llms.txt in the llmstxt.org format (title, one-line summary, links to the key pages). A convenience for assistants, not a ranking factor.")

    order = {"P1": 0, "P2": 1, "P3": 2}
    findings.sort(key=lambda f: order[f["priority"]])
    return {"url": url, "robots_txt": robots, "browser": {"http": base["status"], "text_chars": bchars,
            "title": bpage.title.strip()[:120], "lang": bpage.lang, "canonical": bpage.canonical, "jsonld_blocks": bpage.jsonld},
            "crawlers": rows, "llms_txt": llms, "findings": findings,
            "limits": "Fetched from this machine's IP with crawler user agents; no JavaScript rendering; not the crawlers' real "
                      "IP ranges. No score is computed. A clean result means nothing here blocks the page, not that AI will cite it."}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__)
        sys.exit(2)
    res = check(args[0])
    if "--json" in sys.argv:
        print(json.dumps(res, indent=1))
        return
    print(f"URL: {res['url']}")
    b = res["browser"]
    print(f"Browser UA: HTTP {b['http']}, {b['text_chars']} text chars, lang={b['lang']}, canonical={b['canonical']}, JSON-LD blocks={b['jsonld_blocks']}")
    print(f"robots.txt: HTTP {res['robots_txt']['status']}; llms.txt: {'found' if res['llms_txt'].get('found') else 'missing'} (HTTP {res['llms_txt']['status']})\n")
    print(f"{'crawler':18} {'class':9} {'robots.txt':11} {'http':5} {'chars':>7}  fetch")
    for r in res["crawlers"]:
        print(f"{r['crawler']:18} {r['class']:9} {r['robots']:11} {str(r['http'] or '-'):5} {str(r['text_chars'] if r['text_chars'] is not None else '-'):>7}  {r['fetch']}")
    print("\nFindings:" if res["findings"] else "\nFindings: none from the local checks.")
    for f in res["findings"]:
        print(f"- [{f['priority']}] {f['what']}\n    evidence: {f['evidence']}\n    fix: {f['fix']}")
    print(f"\nLimits: {res['limits']}")


if __name__ == "__main__":
    main()
