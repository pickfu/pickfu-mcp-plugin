# OpenClaw Skills

Source of truth for PickFu skills published to the [ClawHub marketplace](https://clawhub.ai). Each subdirectory is a standalone skill package ready for `clawhub skill publish`.

## Published Skills

| Skill | Slug | Description |
|-------|------|-------------|
| [pickfu-market-research](./pickfu-market-research/) | `pickfu-market-research` | Consumer research surveys — design, target, collect, analyze |

## Publishing to ClawHub

```bash
# First time — authenticate with GitHub
npx clawhub login

# Publish (or update)
npx clawhub skill publish ./openclaw-skills/pickfu-market-research \
  --slug pickfu-market-research \
  --name "PickFu Market Research" \
  --version <semver>

# For updates, bump version and add changelog
npx clawhub skill publish ./openclaw-skills/pickfu-market-research \
  --slug pickfu-market-research \
  --version 1.1.0 \
  --changelog "Added best practices section, switched to npx"
```

Users get updates via `openclaw skills update`.

## Dog-fooding with Polly

Polly (our Survey Assistant bot) installs skills from ClawHub — the same artifact external users get. This ensures we catch install-path and runtime issues before customers do.

**After publishing a new version**, update Polly:

```bash
ssh polly.bots.pickfu-corp.com \
  "sudo -u openclaw XDG_RUNTIME_DIR=/run/user/\$(id -u openclaw) openclaw skills update pickfu-market-research"
```

Polly does NOT use a workspace copy. Do not add skill files to `persistent-bots/polly/skills/`.

## Adding a New Skill

1. Create a subdirectory: `openclaw-skills/<skill-slug>/`
2. Add `SKILL.md` (with YAML frontmatter) and `README.md` (ClawHub listing page)
3. Optionally add `examples/` with reference files
4. Publish via `npx clawhub skill publish`
5. Fleet bots that should use it install via `openclaw skills install <slug>` on the VPS
