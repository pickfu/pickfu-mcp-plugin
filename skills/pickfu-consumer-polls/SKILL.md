---
name: pickfu-consumer-polls
description: >-
  Use when the user wants consumer feedback via PickFu: draft or publish a
  poll, pull results, summarize what respondents said, or suggest a follow-up.
  Calls PickFu MCP tools only; never invent poll results.
---
# PickFu consumer polls

Explicit instructions from the user take priority over these guidelines, except
that results must never be invented and credits must never be spent without the
user's confirmation.

## When to use

- Create or refine a consumer poll or survey
- Publish only when the user explicitly asks
- Fetch results and summarize qualitative and quantitative feedback
- Suggest a follow-up question from the answers

## Rules

- Use the PickFu MCP tools (`save_survey`, `publish_survey`, `get_survey`, `get_survey_responses`, `list_surveys`, `list_templates`, and others as available). Do not invent responses, scores, or demographics.
- Auth is the user's own PickFu account via MCP OAuth. Never use a shared or team token.
- Do **not** auto-publish or spend credits. Create drafts freely. Before publishing a poll, adding respondents, or any other paid action, state the cost and wait for the user to confirm.
- If a tool fails or returns no results, say so plainly instead of guessing.
- Prefer plain, non-leading questions. Keep options parallel.
- Respondents are anonymous. Share their answers and the demographics PickFu reports, never attempt to identify or contact them.
- Keep account IDs and internal identifiers out of user-facing copy.

## Flow

1. Confirm the question and options (and targeting if they named an audience). Ask a follow-up when either is missing.
2. Save as a draft, then show the poll URL or ID when available.
3. Publish only after the user says to publish and has confirmed the cost.
4. When results exist, summarize the winner and notable qualitative themes, then offer one follow-up.
