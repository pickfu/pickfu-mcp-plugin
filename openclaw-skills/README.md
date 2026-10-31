<!-- Source of truth: ./pickfu-market-research/SKILL.md.
     If this doc conflicts with that file, the SKILL.md wins — update this README to match. -->

# OpenClaw Skills

Source of truth for PickFu skills published to the [ClawHub marketplace](https://clawhub.ai) for [OpenClaw](https://openclaw.dev) users. Moved here from the retired internal agent-fleet repo on 2026-10-31, history included. Each subdirectory is a standalone skill package ready for `clawhub publish`.

**Publishing is manual.** A merged PR does not deploy anything to ClawHub. Edits to `SKILL.md` only reach users after running `clawhub publish` and bumping the version.

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
# Run from the repo root
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


## Adding a New Skill

1. Create a subdirectory: `openclaw-skills/<skill-slug>/`
2. Add `SKILL.md` (with YAML frontmatter) and `README.md` (ClawHub listing page)
3. Optionally add `examples/` with reference files
4. Publish via `clawhub publish ./openclaw-skills/<skill-slug> --version 1.0.0 --changelog "Initial release"`
5. Add the new skill to the **Published Skills** table above
