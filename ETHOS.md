# Ethos

## The Problem Worth Solving

Investment professionals at pension funds, endowments, and foundations are some of the most capable people in finance. They manage billions on behalf of retirees, students, and charitable missions. And they spend 60-75% of their time on data gathering and document assembly.

A PM reads a 50-page DDQ cover to cover, cross-references every claim against SEC filings, normalizes fee structures in a spreadsheet, and assembles an IC memo from five different sources. This takes weeks. The actual judgment work -- "should we invest with this manager?" -- gets 10-15% of the total time.

AllocatorStack doesn't replace the judgment. It replaces the assembly.

## Principles

### Agents Draft, Humans Decide

Every output is a draft. The IC memo has `[PM TO COMPLETE]` placeholders. The screening matrix has a human gate before advancing candidates. The DDQ extraction pauses for review before feeding into the memo.

This isn't a safety rail bolted on after the fact. It's the architecture. Skills are designed around the pause points -- the moments where a human needs to look at the data and make a call.

In a fiduciary setting, there is no "fully automated" path. The allocator is legally responsible for every investment decision. The tool accelerates the work that leads to the decision. It never makes the decision.

### Show Your Work

Every number in an AllocatorStack output traces to its source.

```
AUM: $4.3 billion [Source: granite-peak-capital-ddq.pdf, p.3]
AUM (ADV): $4.28 billion [Source: SEC ADV Item 5.F, filed 2025-12-31]
Status: CONFIRMED (difference < 1%)
```

This isn't optional formatting. It's how institutional investment teams work. When the CIO asks "where did this number come from?" the answer has to be specific. A page number. A filing date. An API endpoint.

Provenance is the difference between a useful draft and a liability.

### Fail Loudly

When data is missing, say so. When a number looks wrong, flag it. When an API is unreachable, report what was skipped.

```
Red flag check for Meridian Value Partners:
  SEC enforcement:    CLEAR
  FINRA discipline:   CLEAR
  Litigation (PACER): INCOMPLETE -- PACER access not configured
  State regulatory:   INCOMPLETE -- state databases not searched
```

The worst outcome isn't a missing data point. It's a missing data point that nobody notices. Every gap is surfaced. Every limitation is documented. The reviewer sees exactly what was checked and what wasn't.

### Adapt to What's Available

Not every fund has FactSet. Not every fund has Bloomberg. Some funds have everything. AllocatorStack works with all of them.

```
Data sources:
  Manager database: none        -> skill asks for CSV/Excel
  Market data:      factset     -> skill queries FactSet MCP
  SEC EDGAR:        always on   -> free public API
  FINRA:            always on   -> free public API
```

The same skill, the same workflow, different data sources. A $50B pension with every connector and a $500M endowment with just SEC/FINRA both get a working pipeline. The output quality scales with data richness, but the workflow never breaks.

## How This Shapes the Code

These principles aren't aspirational -- they're structural. They show up in:

- **Schema contracts** (`ddq-output.yaml`, `manager-profile.yaml`) -- every field has a `source` and `confidence` attribute
- **Prerequisite checks** -- skills verify inputs exist before running, with clear error messages pointing to the upstream skill
- **Human gates** -- every skill pauses for review before writing final output
- **Graceful degradation** -- every external dependency (SEC, FINRA, connectors) has an explicit fallback path
- **Workspace isolation** -- each run gets its own directory, so re-running a skill doesn't corrupt prior results

The goal is simple: when an allocator uses this tool, they should feel like they have a well-prepared junior analyst who does thorough work, documents everything, and always asks before making assumptions.
