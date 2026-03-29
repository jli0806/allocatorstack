# AllocatorStack — Project Summary

Claude Skills for institutional asset allocator front-office operations. Each skill maps to a role in an investment office: DDQ Reviewer, IC Memo Drafter, Sourcing Analyst, Compliance Analyst.

Deploys on Claude Team and Enterprise plans.

## Core Insight

Claude can read documents, compare data across sources, and draft structured output. What it doesn't have is the operational knowledge of how allocator professionals do those things — which taxonomy maps to which DDQ section, what constitutes a material AUM discrepancy, where in the workflow a human needs to review, how provenance chains work when every number in an IC memo traces to a specific page in a specific document.

AllocatorStack provides that knowledge as SKILL.md files. A CIO can read the file and understand what the agent does, what it produces, and where it pauses for human review.

## Architecture

Skills are SKILL.md files. Four helper scripts (~400 lines total) handle PDF extraction, SEC/FINRA API calls, and Excel generation. No Python library, no application server.

## Skills

### Manager Due Diligence Pipeline
1. `/screen-managers` — Takes a search mandate, screens candidates against fund criteria and public records (regulatory history, litigation), produces a ranked short list.
2. `/prep-manager-meeting` — Prepares agendas, talking points, and reference packets for meetings with shortlisted managers.
3. `/analyze-ddq` — Ingests DDQ PDFs, extracts answers mapped to ILPA categories, compares across managers, flags gaps, outliers, and inconsistencies.
4. `/draft-memo` — Assembles first-draft IC memo from pipeline data with provenance on every quantitative claim. Qualitative sections marked for the PM.

### Other Skills
5. `/prep-company-meeting` — Briefing packets for direct company meetings: governance, financials, engagement topics.
6. `/monitor-adv` — Quarterly monitoring across the full manager roster. Diffs ADV filings against prior snapshots, scans for news, regulatory actions, and sanctions hits. Flags exceptions so the team reviews only what changed.
7. `/screen-holdings` — Screens holdings for responsible investing risks and forensic accounting red flags. Fast screen, then deep research on flagged items.
8. `/board-report` — Board-ready reports with technical sections for the IC and plain-language summaries for trustees.

## Data Sources

Skills pull data from three tiers: MCP connectors if configured (FactSet, PitchBook, Morningstar), public APIs that are always available (SEC EDGAR, FINRA), and user-provided data as fallback (CSV, Excel, paste). The fund config specifies which connectors are set up. Skills adapt and tell you what's missing.

## Customization

Fund config is YAML:
- Fund profile: type, AUM, asset class targets, risk limits, assumed rate of return
- Evaluation criteria: track record minimums, AUM ranges, fee thresholds, disqualifiers
- Data sources: which MCP connectors are configured
- Templates: IC memo template, board report template, DDQ template

Same skills, different config, different output.

## Design Principles

1. **Agents draft, humans decide.** Every output is a draft for human review.
2. **Show your work.** Every number traces to its source.
3. **Fail loudly.** Missing data and implausible results get flagged.
4. **Verification gates.** Confidence scoring, human review when confidence is low.

## Domain Reference

The working document (`allocator-ai-working-doc-v2.md`) has the full operational context: how allocator front offices are structured, how the core workflows run, where the pain points are, and what design principles apply in fiduciary settings.
