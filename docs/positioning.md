# AllocatorStack: Why a Skill Pack

## The design decision

AllocatorStack is a set of Claude Skills for allocator front-office operations: manager screening, meeting preparation, DDQ analysis, IC memo drafting, and ongoing manager monitoring.

The alternative would be writing a Python library or web application. Either approach means writing extraction code, adapter layers, rendering logic, and orchestration — thousands of lines to do things Claude already does natively: reading documents, comparing data across sources, identifying discrepancies, writing structured output. The useful work is in knowing how allocator professionals do those things. Which taxonomy maps to which DDQ section. What constitutes a material discrepancy in an AUM figure. Where in the workflow a human needs to review before the next step proceeds. How provenance chains work when every number in an IC memo traces back to a specific page in a specific document.

A SKILL.md file encodes that operational knowledge directly. Claude reads the instructions, follows the workflow, calls helper scripts when it needs to do something it can't do natively (parse a PDF binary, query the SEC EDGAR API with rate limiting, generate an Excel file), and produces structured output in a defined schema. The SKILL.md is readable by a CIO in five minutes — what the agent reads, what it produces, where it pauses for human review, what it flags. A Python library with the same behavior spread across 20 files is not.

## Why this works for deployment

Claude's Team and Enterprise plans allow admins to provision skills organization-wide from a central console. The end user doesn't clone a repo or touch a terminal. They open Claude, upload a DDQ, and the skill handles extraction, taxonomy mapping, confidence scoring, and output formatting. The deployment path at a fund: admin enables code execution, uploads the AllocatorStack skills, provisions to the investment team. A Team plan starts at $25/seat/month with a 5-seat minimum — negligible relative to any institutional fund's operational budget.

## What the skill pack structure provides

**Repeatability.** Without a skill, asking Claude to analyze a DDQ produces different output every time — different structure, different things flagged, no consistent schema. A skill enforces the full workflow: extract text with page numbers, map answers to the ILPA/AIMA taxonomy, score confidence per answer, generate a completeness dashboard by category, pause for the analyst to review before proceeding. Output goes to a defined JSON schema that the next skill in the pipeline reads directly.

**Pipeline chaining.** Manager due diligence is not one step. It runs from sourcing through manager meetings, DDQ analysis, and IC memo drafting. Each skill writes structured JSON to a workspace directory. The next skill reads it. Schemas define the contracts between stages. The portfolio manager reviews at human gates between stages. Running this in a single chat session loses provenance at every handoff.

**Fund-level configuration.** A $50B endowment and a $300B pension fund run the same skills with different YAML config files: different asset class targets, different fee thresholds, different track record minimums, different IC memo templates, different data sources. The skill reads the config and adapts its output. No code changes.

**Data source flexibility.** Every fund has different data sources — one uses eVestment, another has FactSet, a third works from spreadsheets and custodian exports. Skills pull data from three tiers: MCP connectors (FactSet, PitchBook, Morningstar — the skill queries the source directly), public APIs (SEC EDGAR, FINRA — always available via helper scripts), and user-provided data (CSV, Excel, paste — the fallback when no connector exists). The fund config specifies which connectors are set up. Skills use what's available and explicitly note what's missing. A fund with no connectors runs the full pipeline — they provide their own data at the screening step.

**Modifiability by non-developers.** An investment analyst can read a SKILL.md, understand the workflow, and change it. Adjusting a confidence threshold or adding a screening criterion means editing a line in a markdown file.

## What AllocatorStack is for

**Production use at allocator firms.** A fund with a Claude Team or Enterprise plan can have their investment team running AllocatorStack the same afternoon. The barrier is a self-serve signup, not an enterprise sales process.

**Distribution through the skills ecosystem.** Anthropic's Skills Directory includes partner-built skills from Notion, Figma, Atlassian, and others. AllocatorStack would be the first institutional investment skills package in that directory — a distribution channel that doesn't require direct sales.

**Advisory engagements.** In a consulting context, the demo and the production deployment are nearly the same thing. Run the pipeline on a real DDQ during a meeting. If the fund wants it, their admin uploads the skills. The team is live that week.

**Demonstrating capability.** A running system that takes a DDQ, maps it to ILPA taxonomy, cross-checks claims against SEC filings, and produces an IC memo with full provenance shows something a slide deck cannot.

## Competitive position

Anyone can write a prompt that says "analyze this DDQ." What that prompt won't do: map to ILPA taxonomy with per-answer confidence scoring, chain through a multi-stage pipeline with schema contracts between stages, cross-reference claims against the manager's own ADV filing, screen for litigation and regulatory red flags before the fund invests time in due diligence, enforce human review at each stage, adapt to fund-specific evaluation criteria, and produce output with provenance linking every number to its source document and page. Building that workflow requires understanding how allocator front offices actually operate — how DDQs are structured, what cross-referencing means in practice, what an IC memo needs to contain, where human judgment is irreplaceable. That domain knowledge is what took months to encode and is hard to replicate without operational experience.

## How this ages

Traditional AI applications write orchestration code to chain LLM calls, parse outputs, handle retries, manage state between steps. When the model improves — better instruction following, larger context window, better tool use — that orchestration code becomes a constraint. It's doing worse what the model would now do natively.

SKILL.md files are instructions. When Claude improves, the skills improve with it. The only maintained code is four helper scripts (~400 lines total) for things Claude genuinely cannot do today: parsing PDF binaries, calling rate-limited external APIs, generating Excel files. That list gets shorter over time, not longer.

## Maintenance comparison

| | Traditional AI app | AllocatorStack |
|---|---|---|
| Code to maintain | Thousands of lines | ~400 lines across 4 scripts |
| Deployment | Server, CI/CD, hosting | Admin uploads skills |
| Updates | Release cycle, versioning | Edit the markdown file |
| Customization | Code changes | Edit YAML config |
| Data governance | Data flows to your server + API | Runs within Claude Team/Enterprise |
| Who can modify | Developers | Anyone who can read the SKILL.md |
