#!/usr/bin/env python3
"""Validate this plugin package before a release or an OpenAI ZIP upload.

Checks the Agent Plugins 1.0.0 schemas, the Codex repo marketplace, skill front
matter, icon files, and the OpenAI listing/review limits documented at
https://developers.openai.com/plugins/deploy/submission-errors.

Usage: pip install jsonschema && python3 scripts/validate.py [--release]
--release also fails on TODO placeholders that must be filled before upload.
"""
import json
import re
import struct
import sys
import urllib.request
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
SCHEMAS = "https://agent-plugins.org/schemas/1.0.0/{}.schema.json"
CATEGORIES = {
    "Productivity", "Creativity", "Developer Tools", "Business & Operations",
    "Data & Analytics", "Communication", "Education & Research", "Security",
    "Finance", "Healthcare", "Travel", "Entertainment", "Other",
}
errors, warnings = [], []


def check(cond, msg, warn=False):
    if not cond:
        (warnings if warn else errors).append(msg)


def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def schema(name):
    with urllib.request.urlopen(SCHEMAS.format(name), timeout=20) as r:
        return json.load(r)


def png_size(path):
    data = path.read_bytes()[:24]
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", data[16:24])


def relpath(value, field):
    check(isinstance(value, str) and value.startswith("./"), f"{field} must be a ./-prefixed path")
    path = (ROOT / value).resolve()
    check(ROOT in path.parents and path.exists(), f"{field} points to a missing file: {value}")
    return path


def https(value, field):
    check(isinstance(value, str) and value.startswith("https://") and len(value) <= 1024,
          f"{field} must be an HTTPS URL of at most 1024 characters")


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return None, ""
    fields, key = {}, None
    for line in m.group(1).splitlines():
        top = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if top:
            key, val = top.group(1), top.group(2).strip()
            fields[key] = "" if val in (">-", ">", "|", "|-") else val
        elif key:
            fields[key] = (fields[key] + " " + line.strip()).strip()
    return fields, m.group(2).strip()


def main(release):
    plugin, mcp, market = load("plugin.json"), load("mcp.json"), load(".agents/plugins/marketplace.json")

    for name, doc in (("plugin", plugin), ("mcp", mcp)):
        try:
            jsonschema.validate(doc, schema(name))
        except jsonschema.ValidationError as e:
            errors.append(f"{name}.json fails the Agent Plugins schema: {e.message}")

    check(re.fullmatch(r"\d+\.\d+\.\d+", plugin.get("version", "")), "version must be semver")
    check(plugin.get("author", {}).get("name"), "author.name is required")

    servers = mcp.get("mcpServers", {})
    check(len(servers) == 1, "plugin-level review test cases require exactly one MCP server")
    for sname, server in servers.items():
        https(server.get("url"), f"mcpServers.{sname}.url")
        check(not server.get("headers"), f"mcpServers.{sname} must not declare headers for public submission")

    entries = [p for p in market.get("plugins", []) if p.get("name") == plugin["name"]]
    check(len(entries) == 1, "marketplace.json must list this plugin exactly once")
    for entry in entries:
        source = entry.get("source")
        path = source.get("path") if isinstance(source, dict) else source
        check(isinstance(path, str) and path.startswith("./"), "marketplace source.path must start with ./")
        check((ROOT / path / "plugin.json").exists(), "marketplace source.path must contain plugin.json")
        policy = entry.get("policy", {})
        check(policy.get("installation") in {"AVAILABLE", "INSTALLED_BY_DEFAULT", "NOT_AVAILABLE"},
              "marketplace policy.installation is missing or invalid")
        check(policy.get("authentication") in {"ON_INSTALL", "ON_USE"},
              "marketplace policy.authentication is missing or invalid")
        check(entry.get("category"), "marketplace category is required")

    openai = plugin.get("extensions", {}).get("com.openai", {})
    check(not any(k in openai for k in ("apps", "hooks")), "apps and hooks block public submission")
    ui = openai.get("interface", {})
    for field, limit in (("displayName", 30), ("shortDescription", 30), ("longDescription", 4000),
                         ("developerName", 80)):
        value = ui.get(field, "")
        check(value and len(value) <= limit, f"interface.{field} is required, at most {limit} characters")
    check("\n" not in ui.get("shortDescription", ""), "interface.shortDescription must be one line")
    check(ui.get("category") in CATEGORIES, "interface.category must be a supported category")
    caps = ui.get("capabilities", [])
    check(len(caps) <= 20 and all(0 < len(c) <= 120 for c in caps), "interface.capabilities limits exceeded")
    for field in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        https(ui.get(field), f"interface.{field}")
    prompts = ui.get("defaultPrompt", [])
    prompts = [prompts] if isinstance(prompts, str) else prompts
    check(len(prompts) <= 3 and len(set(prompts)) == len(prompts), "defaultPrompt: at most 3 unique prompts")
    check(all(len(p) <= 128 and "@" not in p for p in prompts), "defaultPrompt: at most 128 chars, no @mentions")
    check(re.fullmatch(r"#[0-9A-Fa-f]{6}", ui.get("brandColor", "#000000")), "brandColor must be #RRGGBB")
    for field in ("logo", "composerIcon"):
        path = relpath(ui.get(field), f"interface.{field}")
        if path.exists():
            size = png_size(path)
            check(size and size[0] == size[1] and 48 <= size[0] <= 4096,
                  f"interface.{field} must be a square PNG between 48 and 4096 px")
            check(path.stat().st_size <= 5 * 1024 * 1024, f"interface.{field} must be at most 5 MiB")
    check("screenshots" not in ui, "screenshots are only allowed when the MCP server has a UI template")

    skill_names = []
    for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
        fields, body = front_matter(skill)
        rel = skill.relative_to(ROOT)
        check(fields is not None, f"{rel} must start with YAML front matter")
        fields = fields or {}
        name, desc = fields.get("name", ""), fields.get("description", "")
        check(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) and name == skill.parent.name,
              f"{rel}: name must be lowercase-hyphenated and match its directory")
        check(0 < len(desc) <= 1024, f"{rel}: description is required, at most 1024 characters")
        check(body, f"{rel}: instructions must not be empty")
        check(len(f"{plugin['name']}:{name}") <= 64, f"{rel}: plugin:skill identity exceeds 64 characters")
        check(not re.search(r"\bclaude\b|anthropic", skill.read_text(encoding="utf-8"), re.I),
              f"{rel}: replace Claude-specific wording with provider-neutral language")
        skill_names.append(name)
    check(skill_names and len(set(skill_names)) == len(skill_names), "skills must exist and have unique names")

    if "onboardingSkill" in openai:
        relpath(openai["onboardingSkill"], "onboardingSkill")

    review = openai.get("review", {})
    cases = review.get("test_cases", {})
    positive, negative = cases.get("positive", []), cases.get("negative", [])
    check(len(positive) == 5, "initial MCP review needs exactly 5 positive test cases")
    check(len(negative) == 3, "initial MCP review needs exactly 3 negative test cases")
    for i, case in enumerate(positive):
        for field in ("description", "prompt", "tools_triggered", "expected_behavior"):
            check(case.get(field), f"positive case {i + 1} is missing {field}")
    for i, case in enumerate(negative):
        for field in ("description", "prompt"):
            check(case.get(field), f"negative case {i + 1} is missing {field}")
    check(not any(k in review for k in ("test_credentials", "reviewer_instructions")),
          "credentials and reviewer instructions belong in the dashboard, not the package")
    check(openai.get("publication", {}).get("release_notes"), "publication.release_notes is required")

    demo = review.get("demo_recording_url", "")
    if demo.startswith("TODO"):
        check(False, "review.demo_recording_url is still a TODO placeholder", warn=not release)
    else:
        https(demo, "review.demo_recording_url")

    for w in warnings:
        print(f"WARNING: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main("--release" in sys.argv[1:]))
