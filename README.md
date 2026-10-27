# PickFu MCP (Agent Plugin)

Connects your agent to the live PickFu MCP server so it can test ideas with real people. Docs: https://www.pickfu.com/docs/developers/mcp-server

## What it does

Connects an agent (Codex, ChatGPT, Cursor, Grok Bot, and other Agent Plugins clients) to PickFu over remote MCP so it can draft polls, publish on ask, and summarize consumer results.

## Connect

- MCP URL: `https://mcp.pickfu.com/mcp` (streamable HTTP)
- Auth: the first time a tool runs, you'll sign in to your own PickFu account through PickFu's OAuth page. A free account works. No API key or shared credentials are needed.
- Cost: drafting, editing and previewing polls is free. Publishing a poll, adding respondents and generating image variants spend your PickFu credits, as do synthetic feedback and Amazon listing mockup imports. The agent drafts first and confirms the cost before anything that spends.

## Install in Codex

```bash
codex plugin marketplace add pickfu/pickfu-mcp-plugin
codex plugin add pickfu-mcp@pickfu
```

This adds the `pickfu` marketplace from `.agents/plugins/marketplace.json` and installs both skills plus the `pickfu` MCP server. Sign-in happens on first use of a PickFu tool (`codex mcp login pickfu` also works).

## Components

| Path | Role |
| --- | --- |
| `plugin.json` | Agent Plugins 1.0.0 manifest; OpenAI listing, review and release metadata under `extensions.com.openai` |
| `mcp.json` | Remote `pickfu` server (OAuth is discovered from the server) |
| `skills/pickfu-consumer-polls/` | When to call tools; never invent results |
| `skills/pickfu-setup/` | Onboarding: connect the account and run a first free step |
| `assets/` | `logo.png` (512 px) and `icon.png` (128 px) listing icons |
| `.agents/plugins/marketplace.json` | Codex repo marketplace pointing at the repo root |
| `scripts/validate.py` | Schema and OpenAI submission checks |

## Public-safe bar

- No operator / internal skills
- No internal IDs or team tokens in the pack
- Publish / spend only when the user asks

## Validate

```bash
pip install jsonschema
python3 scripts/validate.py            # TODO placeholders are warnings
python3 scripts/validate.py --release  # TODO placeholders are errors
```

The script checks `plugin.json` and `mcp.json` against https://agent-plugins.org/schemas/1.0.0/, the Codex marketplace entry, skill front matter, icons, and the OpenAI listing and review limits. To prove it in an IDE, install under Cursor local plugins. Grok Bot loads marketplace plugins only (not `~/.cursor/plugins/local`).

## Build the OpenAI upload ZIP

Fill in `review.demo_recording_url` in `plugin.json`, make sure `--release` passes, then:

```bash
git archive --format=zip -o pickfu-mcp-$(python3 -c "import json;print(json.load(open('plugin.json'))['version'])").zip HEAD \
  plugin.json mcp.json skills assets LICENSE README.md
```

Upload it to the existing PickFu plugin in the OpenAI plugin portal (Upload plugin), not as a new plugin.
