# PickFu MCP (Grok Bot / Agent Plugin)

Connects your agent to the live PickFu MCP server so it can test ideas with real people. Docs: https://www.pickfu.com/docs/developers/mcp-server

## What it does

Connects a Grok Bot to PickFu over remote MCP so the bot can draft polls, publish on ask, and summarize consumer results.

## Connect

- MCP URL: `https://mcp.pickfu.com/mcp` (streamable HTTP)
- Auth: the first time a tool runs, you'll sign in to your own PickFu account through PickFu's OAuth page. A free account works. No API key or shared credentials are needed.
- Cost: drafting, editing and previewing polls is free. Publishing a poll, adding respondents and generating image variants spend your PickFu credits. The agent drafts first and confirms the cost before anything that spends.

## Components

| Path | Role |
| --- | --- |
| `plugin.json` | Agent Plugins 1.0.0 manifest |
| `mcp.json` | Remote `pickfu` server |
| `skills/pickfu-consumer-polls/` | When to call tools; never invent results |

## Public-safe bar

- No operator / internal skills
- No internal IDs or team tokens in the pack
- Publish / spend only when the user asks

## Prove locally

Validate manifests against https://agent-plugins.org/schemas/1.0.0/ — then install under Cursor local plugins if proving in IDE. Grok Bot loads marketplace plugins only (not `~/.cursor/plugins/local`).
