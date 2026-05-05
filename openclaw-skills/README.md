<!-- Source of truth: ./pickfu-market-research/SKILL.md.
     If this doc conflicts with that file, the SKILL.md wins — update this README to match. -->

# OpenClaw Skills

Source of truth for PickFu skills published to the [ClawHub marketplace](https://clawhub.ai). Each subdirectory is a standalone skill package ready for `clawhub publish`.

**Publishing is manual.** A merged PR does not deploy anything to ClawHub. Edits to `SKILL.md` only reach users (and Polly) after running `clawhub publish` and bumping the version.

## Published Skills

| Skill | Slug | Description |
|-------|------|-------------|
| [pickfu-market-research](./pickfu-market-research/) | `pickfu-market-research` | Consumer research surveys — design, target, collect, analyze |

## Publishing to ClawHub

### One-time setup

```bash
clawhub login         # opens browser, stores token
clawhub whoami        # confirms auth
```

### Publish a new version

The skill folder name (`pickfu-market-research/`) and the SKILL.md frontmatter `name:` field already match the slug, so no `--slug` or `--name` flags are needed.

```bash
# Run from pickfu-agents/ root
clawhub publish ./openclaw-skills/pickfu-market-research \
  --version <semver> \
  --changelog "<short summary of what changed>"
```

### Verify it landed

```bash
clawhub inspect pickfu-market-research | head
```

Confirm `Latest:` matches the version you just published. If it doesn't, the publish silently failed — re-run.

### Versioning

| Bump | When |
|------|------|
| Patch (1.0.x) | Doc clarifications, error message tweaks, additive guidance |
| Minor (1.x.0) | New sections, new patterns, new optional flags surfaced |
| Major (x.0.0) | Renamed/removed steps, breaking changes to the documented contract |

### Pushing the update to Polly

Polly (our Survey Assistant bot) installs the skill from ClawHub — same artifact external users get. After a publish, push the update to her VPS:

```bash
ssh polly.bots.pickfu-corp.com \
  "sudo -u openclaw XDG_RUNTIME_DIR=/run/user/\$(id -u openclaw) openclaw skills update pickfu-market-research"
```

Polly's `openclaw.json` denies `skills_install` and `skills_remove` — she cannot self-update. The push must come from an operator with SSH access.

Polly does NOT use a workspace copy. Do not add skill files to `persistent-bots/polly/skills/`.

## Adding a New Skill

1. Create a subdirectory: `openclaw-skills/<skill-slug>/`
2. Add `SKILL.md` (with YAML frontmatter) and `README.md` (ClawHub listing page)
3. Optionally add `examples/` with reference files
4. Publish via `clawhub publish ./openclaw-skills/<skill-slug> --version 1.0.0 --changelog "Initial release"`
5. Fleet bots that should use it install via `openclaw skills install <slug>` on the VPS
6. Add the new skill to the **Published Skills** table above
