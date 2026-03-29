# Contributing

AllocatorStack is open source and welcomes contributions. Here's how to get started.

## Quick Start

```bash
# Clone the repo
git clone https://github.com/jli0806/allocatorstack.git
cd allocatorstack

# Install dependencies
pip install pymupdf requests openpyxl pytest

# Run tests
pytest tests/ -v

# Run the demo
./demo
```

## Project Structure

```
allocatorstack/
|
|-- .claude/skills/          # Registered skills (Claude Code discovers these)
|   |-- analyze-ddq/
|   |-- draft-memo/
|   |-- monitor-adv/
|   |-- prep-manager-meeting/
|   +-- screen-managers/
|
|-- schemas/                 # Data contracts
|   |-- ilpa_aima_v1.yaml    # 150+ ILPA DDQ questions
|   |-- ddq-output.yaml      # Output format of /analyze-ddq
|   +-- manager-profile.yaml # Output format of /screen-managers
|
|-- scripts/                 # Python helper scripts (~400 lines total)
|   |-- extract-pdf.py       # PDF text extraction (PyMuPDF)
|   |-- query-edgar.py       # SEC EDGAR / IAPD API
|   |-- query-finra.py       # FINRA BrokerCheck API
|   |-- generate-excel.py    # Excel comparison output
|   +-- generate-sample-ddqs.py  # Sample DDQ PDF generator
|
|-- templates/               # Output templates
|   |-- ic_memo.md
|   |-- screening_report.md
|   +-- board_report.md
|
|-- samples/
|   |-- configs/             # Example fund configurations
|   +-- ddqs/                # 3 synthetic DDQ PDFs for testing
|
|-- tests/                   # pytest suite (45 tests)
|
|-- docs/                    # Extended documentation
|   |-- skills.md            # Skill deep dives
|   |-- positioning.md       # Value prop and messaging
|   +-- designs/             # Design documents
|
|-- analyze-ddq/             # Root-level skill references
|-- draft-memo/              #   (canonical versions are in .claude/skills/)
|-- screen-managers/
|-- ...
|
|-- CLAUDE.md                # Project instructions for Claude Code
|-- ETHOS.md                 # Design philosophy
|-- ARCHITECTURE.md          # Technical design decisions
|-- CHANGELOG.md             # Release notes
+-- TODOS.md                 # Roadmap
```

## What to Work On

Check `TODOS.md` for the current roadmap. Good first contributions:

- **Add questions to the ILPA schema** -- `schemas/ilpa_aima_v1.yaml` could always use refinement from people with domain expertise
- **Improve sample DDQs** -- Make the synthetic data more realistic
- **Add tests** -- Coverage for edge cases in the helper scripts
- **Fix SEC/FINRA API responses** -- The API scripts could handle more response formats

## How Skills Work

Skills are SKILL.md files that Claude Code reads and follows. They're not code -- they're structured instructions.

The canonical skill definitions live in `.claude/skills/{skill-name}/SKILL.md`. Root-level copies (`analyze-ddq/SKILL.md`, etc.) are reference versions.

When editing a skill:
1. Edit the `.claude/skills/` version (this is what Claude Code reads)
2. Update the root-level version to match
3. Test by invoking the skill in Claude Code

## Writing a New Skill

Follow the existing pattern:

```yaml
---
name: your-skill-name
description: One-line description of what it does
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# /your-skill-name -- Title

You are a [Role] at an institutional allocator. Your job is to [what the skill does].

## Prerequisites

Before starting, verify:
1. [Required inputs exist]
2. [Schemas are readable]

## Workspace

Write output to `workspace/<run-id>/`.

## Workflow

### Step 1: [First step]
...

## HUMAN GATE

Present results. Wait for user to review and approve.

## Output

- `workspace/<run-id>/output-file.json` -- description
```

Key rules:
- Always include a **Prerequisites** section that checks inputs exist
- Always include a **HUMAN GATE** before final output
- Reference schemas for output formats
- Use `workspace/<run-id>/` for all file paths
- Include `[Source: ...]` provenance notation in outputs

## Helper Scripts

The 4 Python scripts in `scripts/` are intentionally simple. They handle only what Claude can't do natively:

- PDF binary parsing (needs PyMuPDF)
- API rate limiting (SEC requires max 10 req/sec)
- Excel formatting (needs openpyxl)

If you're adding a new script, keep it under 100 lines, take JSON in/out, and handle errors with structured JSON error objects.

## Tests

```bash
# Run all tests
pytest tests/ -v

# Run a specific test file
pytest tests/test_extract_pdf.py -v

# Run with coverage
pytest tests/ --cov=scripts/
```

Tests mock all external API calls. Sample DDQ PDFs in `samples/ddqs/` serve as test fixtures.

## Commit Style

- One logical change per commit
- Present tense ("Add fee normalization" not "Added fee normalization")
- No need to reference internal tracking -- just describe what changed

## Questions?

Open an issue at https://github.com/jli0806/allocatorstack/issues
