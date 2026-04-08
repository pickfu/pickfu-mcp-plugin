---
name: pickfu-market-research
description: Run consumer research surveys with PickFu to get real human feedback in minutes — validate product names, compare logos and packaging, test pricing tiers, or collect Amazon Prime member feedback. Designs questions, targets audiences by demographics or platform (Amazon Prime, iOS users, etc.), collects responses from real people, and delivers structured analysis reports with verbatim quotes and demographic breakdowns.
emoji: "\U0001F4CA"
user-invocable: true
disable-model-invocation: false
homepage: https://www.pickfu.com
metadata: {"openclaw":{"requires":{"bins":[],"env":["PICKFU_API_KEY"]},"primaryEnv":"PICKFU_API_KEY","emoji":"📊","homepage":"https://www.pickfu.com","os":["darwin","linux","win32"],"install":[{"kind":"node","package":"@pickfu/cli","bins":["pickfu"]}]}}
---

# PickFu Market Research Procedure

Run consumer research surveys end-to-end: define a research brief, design a multi-question survey, collect responses from targeted audiences, and deliver a structured analysis report.

This skill is **adaptive** — it uses PickFu MCP tools when available, and falls back to the `@pickfu/cli` CLI otherwise.

## When to invoke this skill

**Invoke when** the user wants to collect real human feedback on a specific question or decision — choosing between designs, validating a name, testing price points, or getting audience reactions to a concept.

**Do NOT invoke when** the user is asking for your opinion or analysis, researching existing data, or exploring a topic conceptually. This skill creates real surveys that charge the user's PickFu account. When in doubt, ask: "Would you like to run an actual PickFu poll for this, or are you looking for my analysis?"

## Step 0 — Auth & Tool Detection

Detect the available interface and verify authentication before proceeding.

### 0a. Try MCP tools first

Attempt to call `list_available_targeting` (a read-only MCP tool). If it succeeds, MCP is available and authenticated.

```
MCP path detected — using PickFu MCP tools.
```

### 0b. Try CLI fallback

If MCP tools are unavailable, check for the CLI:

```bash
npx --yes @pickfu/cli@latest auth status --json
```

If the CLI is installed and authenticated, use CLI mode:

```
CLI path detected — using @pickfu/cli.
```

### 0c. New user onboarding

If neither MCP nor CLI auth is found, guide the user through setup:

1. **Explain**: "PickFu is a consumer research platform that lets you get feedback from targeted audiences in minutes. Let's get you set up."
2. **Install**: Visit [agents.pickfu.com](https://agents.pickfu.com) for install options, or use npx (zero-install, requires Node.js 20+):
   ```bash
   npx --yes @pickfu/cli@latest auth status
   ```
3. **Authenticate** (choose based on environment):
   - **API key (headless/bot environments)**: `export PICKFU_API_KEY=your_key` — best for servers, CI, and AI agents. Get a key at [app.pickfu.com/settings/api-keys](https://app.pickfu.com/settings/api-keys)
   - **Interactive OAuth (desktop)**: `npx --yes @pickfu/cli@latest auth login` (opens browser)
   - **Headless OAuth**: `npx --yes @pickfu/cli@latest auth login --headless` (prints URL to visit manually)
4. **Verify**: `npx --yes @pickfu/cli@latest auth status`
5. Once authenticated, continue to Step 1.

### 0d. Surface auth status

Tell the user which mode is active:

```
✓ PickFu connected via [MCP tools / CLI] as [email/account info]
```

## Step 1 — Research Brief

Capture what the user wants to learn. Ask these questions (adapt to context — skip what's already clear):

1. **Research objective** — What decision are you trying to make? (e.g., "Which logo resonates better with pet owners?" or "What's the ideal price point for this SaaS plan?")
2. **Product/category context** — What's the product, brand, or category? Any relevant background?
3. **Hypotheses** — Do you have a hunch about what will win, or is this exploratory?
4. **Target audience** — Who should answer? (demographics, platform users like Amazon shoppers, etc.)
5. **Any constraints** — Budget sensitivity, timeline, specific countries?

Synthesize into a structured brief:

```markdown
## Research Brief
- **Objective**: [what they want to learn]
- **Product/Context**: [product, category, background]
- **Hypotheses**: [existing assumptions or "exploratory"]
- **Target Audience**: [demographic/behavioral profile]
- **Constraints**: [budget, timeline, country requirements]
```

## Step 1b (optional) — Generate or Upload Test Assets

If the user needs images to test but doesn't have them yet (logo concepts, packaging mockups, ad creatives), generate or upload them before designing the survey.

### Generate images

**MCP**: Call `generate_image` with a `prompt` and optional `aspectRatio` (1:1, 2:3, 3:2, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9).

**CLI**:
```bash
npx --yes @pickfu/cli@latest media generate --prompt "A modern minimalist logo for a pet food brand called Pawsome" --aspect-ratio 1:1 --json
```

The response includes a `url` — use it as a `media_url` option in the survey. Generate multiple variations to test against each other.

### Upload existing files or URLs

If the user has local files or URLs to test:

**MCP**: Call `upload_media` with a `url` or local file path.

**CLI**:
```bash
# From URL
npx --yes @pickfu/cli@latest media upload --url https://example.com/logo-v2.png --json

# From local file
npx --yes @pickfu/cli@latest media upload --file ./logo-v2.png --json
```

The response includes a CDN `url` — use it as a `media_url` option in the survey.

### Creative iteration loop

After results come back (Step 5), if the user wants to iterate:
1. Review what respondents liked/disliked about each option
2. Generate refined versions incorporating the feedback
3. Run a follow-up survey comparing the refined options
4. Repeat until the user is satisfied with a winner

## Step 2 — Survey Design

Based on the brief, design a multi-question survey. Present the full design for user approval before creating.

### Survey design best practices

Follow these when drafting questions:

- **One question, one concept** — don't combine two questions into one ("Do you like the color and the font?"). Split them.
- **Write neutral, non-leading prompts** — "Which logo do you prefer?" not "Which logo looks more professional and trustworthy?"
- **Match question type to goal** — use `head_to_head` for direct A/B comparisons, `ranked` for ordering 3+ options, `open_ended` for exploratory feedback. Don't use `ranked` when you only need a winner.
- **Keep options balanced** — compare like with like. Don't put 1 polished design against 4 rough drafts.
- **Be specific in prompts** — "Which product name would you be most likely to click on in search results?" is better than "Which name do you like?"
- **Provide context when needed** — use the `context` field to give respondents background. "You're shopping for dog food online" helps frame their perspective.
- **Limit survey length** — 1-3 questions is ideal. More than 5 questions risks respondent fatigue and lower-quality answers.
- **Use images when possible** — visual options (logos, packaging, screenshots) get more engaged responses than text-only descriptions.

For more guidance, see the [PickFu survey guides](https://www.pickfu.com/help).

### 2a. Select question types

Choose from the 10 available types based on the research objective:

| Type | Best for | Options required |
|------|----------|-----------------|
| `head_to_head` | A/B comparison — pick a favorite with explanation | Exactly 2 |
| `ranked` | Preference ordering across 3-8 options | 3-8 |
| `open_ended` | Free-form written feedback on a single concept | 0-1 |
| `single_select` | Pick one favorite from multiple options with explanation | 3-8 |
| `multi_select` | Select multiple answers from options | 3-8 |
| `emoji_rating` | Quick sentiment check with emoji + explanation | 0-1 |
| `star_rating` | 1-5 star rating with written feedback | 0-1 |
| `click_test` | Heatmap of where users click on an image | 1 (image) |
| `five_second_test` | First impressions after brief timed exposure | 1 (image) |
| `screen_recording` | Record user interaction with content | 0-1 |

### 2b. Draft questions

For each question, specify:
- **type**: one of the 10 types above
- **prompt**: the question text (max 255 characters)
- **context** (optional): an object with either `text` or `media_url` (not both). Examples: `{"text": "Some background info"}` or `{"media_url": "https://example.com/image.png"}`
- **options**: array of answer choices — each option uses ONE of:
  - `value` — text
  - `media_url` — image/video URL (must be HTTPS)
  - `asin` — Amazon product ASIN
  - `image_set` — array of ASINs or URLs (with optional `image_set_direction`: "vertical" or "horizontal")
  - `mockup` — Amazon listing mockup (fields: `type` serp/listing, `image`, `title`, `num_ratings`, `review_score`, `price`, `currency`)

**Important**: All options within the same question MUST use the same content type.

### 2c. Configure targeting

Use available targeting options to match the research brief's audience:

**MCP**: Call `list_available_targeting` (optionally with a `country` parameter)
**CLI**: `npx --yes @pickfu/cli@latest targeting list --json` (or `--country GB` etc.)

Common targeting examples:
- Demographics: `male`, `female`, `25-34yo`, `35-44yo`
- Platform: `amznpr` (Amazon Prime), `iosuser`, `androiduser`
- Interests: varies by country — use the list command to discover

### 2d. Configure reporting

Add reporting demographics to segment results:

**MCP**: Call `list_available_reporting` (optionally with a `country` parameter)
**CLI**: `npx --yes @pickfu/cli@latest reporting list --json`

Common reporting segments: `gender`, `age-range`, `ethnicity`, `income`, `education`

### 2e. Set sample size

Available sizes: 15, 30, 50, 75, 100, 200, 500 respondents.

Guidelines:
- **15**: Quick directional signal, good for early iteration
- **30-50**: Standard for most A/B tests and preference polls
- **100**: Higher confidence, good for quantitative analysis
- **200-500**: Large-scale validation, demographic breakdowns

### 2f. Select country

Supported countries: US (default), CA, AU, DE, GB, JP, MX, ES, FR, IT, KR, BR, ZA, PL

### 2g. Present the design

Show the complete survey design for user review:

```markdown
## Survey Design

**Intent**: [survey_intent — what we want to learn]
**Audience**: [targeting traits] in [country]
**Sample size**: [N] respondents
**Reporting**: [reporting segments]

### Questions

**Q1** ([type]): [prompt]
  - Option A: [content]
  - Option B: [content]

**Q2** ([type]): [prompt]
  - [options or "open-ended, no options"]

[... additional questions ...]
```

Support iteration: if the user wants changes ("make Q2 ranked instead", "add a question about pricing", "increase sample size"), update and re-present.

## Step 3 — Create & Publish

Once the user approves the design, create the survey and publish on confirmation.

### 3a. Create the survey

**MCP path:**

Call `save_survey` with the survey parameters (omit `surveyId` to create a new survey):

```json
{
  "survey_intent": "Brief description of research goal",
  "country": "US",
  "sample_size": "50",
  "targeting": ["targeting-trait-1", "targeting-trait-2"],
  "reporting": ["gender", "age-range"],
  "questions": [
    {
      "type": "head_to_head",
      "prompt": "Which logo do you prefer for a pet food brand?",
      "options": [
        { "media_url": "https://example.com/logo-a.png" },
        { "media_url": "https://example.com/logo-b.png" }
      ]
    }
  ]
}
```

**CLI path:**

Write the survey JSON to a temp file and create via CLI:

```bash
SURVEY_FILE="/tmp/pickfu-survey-$$.json"
cat > "$SURVEY_FILE" << 'SURVEY_EOF'
{
  "survey_intent": "Brief description of research goal",
  "country": "US",
  "sample_size": "50",
  "targeting": ["targeting-trait-1"],
  "reporting": ["gender", "age-range"],
  "questions": [...]
}
SURVEY_EOF

SURVEY_ID=$(npx --yes @pickfu/cli@latest survey create --from-file "$SURVEY_FILE" --json | jq -r '.id')
rm -f "$SURVEY_FILE"
```

Capture the survey ID from the response.

### 3b. Show survey URL

Present the survey URL for optional manual review:

```
Survey created: https://www.pickfu.com/surveys/<id>
```

### 3c. Confirm before publishing

**⚠️ Publishing charges your account and starts data collection. This cannot be undone.**

Ask for explicit confirmation: "Ready to publish? This will charge your account and start collecting [N] responses."

### 3d. Publish

**MCP path:** Call `publish_survey` with the survey `id`.

**CLI path:**

```bash
npx --yes @pickfu/cli@latest survey publish <id> --json
```

Confirm publication:

```
✓ Survey published — collecting [N] responses from [targeting description].
```

## Step 4 — Wait for Results

Monitor the survey until all responses are collected.

### Polling path (preferred)

Poll for completion using the CLI or MCP. This is preferred because most agent runtimes enforce subprocess timeouts (e.g., 120s) that are shorter than typical survey durations.

**CLI polling:**

```bash
npx --yes @pickfu/cli@latest survey get <id> --json | jq '{status, responses_count}'
```

**MCP polling:** Call `get_survey` with the survey `id`.

- If `status` is not `"completed"`, wait and check again
- Surface progress if available: "X of N responses collected"
- Poll interval: every 60 seconds
- Timeout: after 30 minutes of polling, offer to check back later

### CLI watch (alternative — zero token cost)

For environments with long subprocess timeouts (>10 minutes):

```bash
npx --yes @pickfu/cli@latest survey watch <id> --json
```

This blocks at the process level — the agent's LLM is NOT invoked while waiting. The CLI polls every 30 seconds. When complete, results appear on stdout.

**Timeout fallback**: If the `watch` command exits with a non-zero code before results are complete (e.g., killed by runtime timeout), the survey is still running. Fall back to the polling path above.

### Completion

```
✓ All [N] responses collected. Analyzing results...
```

## Step 5 — Analyze & Report

Retrieve full results and generate a structured research report.

### 5a. Retrieve results

**MCP path:**
1. Call `get_survey` with the survey `id` — returns survey details, AI summaries, and question-level data
2. Call `get_survey_responses` with the survey `id` — returns individual respondent answers with demographics

**CLI path:**

```bash
npx --yes @pickfu/cli@latest survey get <id> --json
npx --yes @pickfu/cli@latest survey responses <id> --json
```

### 5b. Generate report

Structure the analysis report:

```markdown
## Research Report

### Executive Summary
[2-3 sentences: key finding, winner/recommendation, confidence level]

### Survey Details
- **Survey**: [survey URL: https://www.pickfu.com/surveys/<id>]
- **Respondents**: [N] from [country], targeting: [traits]
- **Duration**: [time from publish to completion]

### Per-Question Analysis

#### Q1: [prompt] ([type])
**Result**: [winner/ranking/average rating]
**Distribution**: [response breakdown — e.g., "Option A: 65%, Option B: 35%"]
**Confidence**: [statistical confidence if available]
**AI Summary**: [include the AI-generated summary from the survey data]

**Notable Quotes**:
> "[verbatim respondent quote]" — [demographic info if available]
> "[another quote]" — [demographic info]

[Repeat for each question]

### Demographic Breakdown
[If reporting segments were configured, show how results vary by demographic]

| Segment | Option A | Option B |
|---------|----------|----------|
| Male | 70% | 30% |
| Female | 58% | 42% |

### Next Steps
- [Actionable recommendation based on findings]
- [Follow-up research suggestion if applicable]
- [Link to full results: https://www.pickfu.com/surveys/<id>]
```

### 5c. Key guidelines for analysis

- **Always include the survey URL** so the user can view full results in the PickFu dashboard
- **Quote real respondent feedback** — verbatim quotes are the most valuable part of PickFu results
- **Highlight demographic differences** if reporting was configured
- **Be direct about the winner** — don't hedge when the data is clear
- **Suggest follow-up research** if results raise new questions (e.g., "The logo won overall but lost with 18-24 — consider a follow-up targeting that segment")

## Step 6 (optional) — Organize & Follow Up

### Tag surveys

Tag surveys for easy retrieval later (e.g., "q2-launch", "logo-research", "pricing-v2"):

**MCP**: Call `create_tag` with `name`, then `save_survey` with `tags: ["tag-name"]` to apply.

**CLI**:
```bash
npx --yes @pickfu/cli@latest tag create --name "q2-launch" --json
npx --yes @pickfu/cli@latest tag list --json
```

### Organize into projects

Group related surveys into a project:

**MCP**: Call `save_project` with `name` and optional `description`. Then `save_survey` with `projectId` to assign.

**CLI**:
```bash
npx --yes @pickfu/cli@latest project create --name "Brand Launch Research" --json
npx --yes @pickfu/cli@latest project list --json
```

### Add more respondents

If results are inconclusive or the user wants higher confidence, add respondents to a completed survey:

**MCP**: Call `add_respondents` with the survey `id` and `count`. Use `preview: true` to show cost first.

**CLI**:
```bash
# Preview cost before committing
npx --yes @pickfu/cli@latest survey add-respondents <id> --count 50 --preview --json

# Add respondents
npx --yes @pickfu/cli@latest survey add-respondents <id> --count 50 --json
```

### Reference past surveys

Search and retrieve previous surveys for context or comparison:

**MCP**: Call `list_surveys` with optional filters (`status`, `tags`, `projectId`). Call `get_survey` for full details.

**CLI**:
```bash
npx --yes @pickfu/cli@latest survey list --json
npx --yes @pickfu/cli@latest survey get <id> --json
npx --yes @pickfu/cli@latest survey responses <id> --json
```

### Edit a draft before publishing

If the user wants to change a survey after creation but before publishing:

**MCP**: Call `save_survey` with the `surveyId` to update.

**CLI**:
```bash
npx --yes @pickfu/cli@latest survey update <id> --from-file updated.json --json
```

### Browse playbook templates

PickFu offers pre-built research playbooks for common scenarios:

**MCP**: Call `list_playbooks` (optional `industry` filter), then `get_playbook` for full step-by-step guides.

**CLI**:
```bash
npx --yes @pickfu/cli@latest playbook list --json
npx --yes @pickfu/cli@latest playbook get <slug> --json
```

Use playbooks as inspiration for survey design — they include recommended question types, targeting, and sample sizes for each use case.

## Error Handling

### Auth issues

| Error | Action |
|-------|--------|
| MCP auth expired/invalid | Guide user to reconfigure MCP server auth token |
| CLI token expired | Run `npx --yes @pickfu/cli@latest auth login --headless` for re-auth |
| `PICKFU_API_KEY` invalid | "Your API key appears invalid. Generate a new one at app.pickfu.com/settings/api-keys" |

### Survey creation errors

| Error | Action |
|-------|--------|
| "head_to_head requires exactly 2 options" | Fix option count and re-create |
| "ranked requires 3-8 options" | Adjust option count to 3-8 range |
| "prompt must be 255 characters or less" | Shorten the question text |
| "URL must use https protocol" | Replace http:// URLs with https:// |
| Insufficient balance | "Your PickFu account balance is too low for this survey. Add funds at app.pickfu.com/settings/credits" |
| Invalid targeting trait | Re-check available traits via `list_available_targeting` |

### Watch/polling issues

| Error | Action |
|-------|--------|
| Watch timeout (>30 min) | "The survey is still collecting responses. I can check back later — just ask me to check on survey [id]." |
| Survey stuck in draft | Verify publish succeeded — re-publish if needed |
| Network error during poll | Retry with exponential backoff (max 3 retries) |
