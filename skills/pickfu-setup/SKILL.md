---
name: pickfu-setup
description: >-
  Use right after the PickFu plugin is installed, or when the user asks how to
  get started with PickFu, connect their PickFu account, or check that the
  connection works.
---
# Get started with PickFu

Help the user connect their PickFu account and run a first, free step. Explicit
instructions from the user take priority over this flow.

## Steps

1. Explain in one or two sentences what PickFu does: it collects feedback on
   ideas such as product names, images, and ad copy from real people.
2. Check the connection by calling `list_surveys` with a small limit. If the
   PickFu tools ask for sign-in, tell the user to finish signing in on PickFu's
   page. A free PickFu account works. Never ask for a password, API key, or
   token in the conversation.
3. If the call succeeds, confirm the account is connected and mention how many
   recent polls it has, using only what the tool returned. If it fails, report
   the error plainly and suggest retrying the sign-in. Do not guess at account
   details.
4. Explain costs: drafting, editing, and previewing polls is free. Publishing a
   poll, adding respondents, generating image variants, synthetic feedback, and
   Amazon listing mockup imports spend PickFu credits, and the cost is always
   confirmed before anything is spent.
5. Offer a first step, for example: "Want me to draft a free poll comparing two
   ideas you're deciding between?" Draft it only if the user says yes, and do
   not publish it as part of setup.

Help and documentation: https://www.pickfu.com/help/
