# Ethos

## The Problem Worth Solving

Investment professionals at pension funds, endowments, and foundations manage billions on behalf of retirees, students, and charitable missions. They spend 60-75% of their time on data gathering and document assembly.

A PM reads a 50-page DDQ cover to cover, normalizes fee structures in a spreadsheet, and assembles an IC memo from five different sources. This takes weeks. The actual judgment work -- "should we invest with this manager?" -- gets 10-15% of the total time.

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
Management fee: 85 bps (first $250M), 75 bps ($250M-$500M), 65 bps (above $500M)
  [Source: granite-peak-capital-ddq.pdf, p.6]
Key persons: Robert Chen, Sarah Martinez [Source: granite-peak-capital-ddq.pdf, p.4]
```

When the CIO asks "where did this number come from?" the answer is a page number, not "the AI said so." Provenance is the difference between a useful draft and a liability.

### Fail Loudly

When data is missing, say so. When a number looks wrong, flag it. When a data source is unavailable, report what was skipped.

```
Completeness check for Meridian Value Partners:
  Investment Strategy:     6/8 questions answered
  Risk Management:         2/8 questions answered  [SPARSE]
  Fees & Terms:            2/12 questions answered  [SPARSE]
  Overall:                 22/52 questions (42%)    [INCOMPLETE]
```

The worst outcome isn't a missing data point. It's a missing data point that nobody notices. Every gap is surfaced. Every limitation is documented. The reviewer sees exactly what was covered and what wasn't.

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

These principles show up in the actual implementation:

- **Schema contracts** (`ddq-output.yaml`, `manager-profile.yaml`) -- every field has a `source` and `confidence` attribute
- **Prerequisite checks** -- skills verify inputs exist before running, with clear error messages pointing to the upstream skill
- **Human gates** -- every skill pauses for review before writing final output
- **Graceful degradation** -- every external dependency has an explicit fallback path
- **Workspace isolation** -- each run gets its own directory, so re-running a skill doesn't corrupt prior results
