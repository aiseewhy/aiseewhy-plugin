# AISeeWhy agent plugin

Skills and an MCP server that let AI agents check whether ChatGPT, Claude, Perplexity and Gemini crawlers can reach and read a page, find what blocks them, fix it and prove the fix worked. Hosted service: [aiseewhy.com](https://aiseewhy.com).

## Claude Code

```
/plugin marketplace add aiseewhy/aiseewhy-plugin
/plugin install aiseewhy@aiseewhy
```

## Skills only, for any agent that reads SKILL.md

```sh
npx skills add aiseewhy/aiseewhy-plugin
```

Then connect the MCP server in your agent (Codex, Cursor and others): https://aiseewhy.com/docs/#agents

See [plugins/aiseewhy/README.md](plugins/aiseewhy/README.md) for what the skills do and how to set the API key. The skills are MIT licensed; the AISeeWhy service has its own [terms](https://aiseewhy.com/terms/).
