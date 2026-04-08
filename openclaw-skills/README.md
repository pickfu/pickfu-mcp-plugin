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

Polly (our Survey Assistant bot) uses the same SKILL.md as the published ClawHub skill. This ensures we catch issues before external users do.

**After editing a skill here, copy it to Polly:**

```bash
cp openclaw-skills/pickfu-market-research/SKILL.md \
   persistent-bots/polly/skills/market-research/SKILL.md
```

Then deploy Polly to pick up the change: `./scripts/deploy.sh polly`

## Adding a New Skill

1. Create a subdirectory: `openclaw-skills/<skill-slug>/`
2. Add `SKILL.md` (with YAML frontmatter) and `README.md` (ClawHub listing page)
3. Optionally add `examples/` with reference files
4. Publish via `npx clawhub skill publish`
5. If a fleet bot should use it, copy the SKILL.md into that bot's `skills/` directory
