# AllocatorStack

Claude Code skills for institutional asset allocation.

Drop in DDQ PDFs from multiple managers. Get a structured side-by-side comparison mapped to the ILPA taxonomy, a completeness dashboard showing gaps and outliers, and a draft IC memo with provenance on every number. Each skill maps to a role in an investment office. Humans review at every stage.

## Quick Start

```bash
# Clone and install
git clone https://github.com/jli0806/allocatorstack.git
cd allocatorstack
pip install pymupdf requests openpyxl

# Run the demo (extracts 3 sample DDQs)
./demo

# Then open Claude Code and run the full pipeline:
# /analyze-ddq     <- maps DDQ answers to ILPA taxonomy, cross-refs against ADV
# /draft-memo      <- generates IC memo with provenance links
```

The demo extracts text from 3 synthetic DDQ PDFs (Granite Peak Capital, Meridian Value Partners, Osprey Global Advisors) and shows the ILPA-structured content. Then use Claude Code skills to analyze, compare, and draft.

## Why This Exists

Investment professionals at pension funds, endowments, and foundations spend 60-75% of their time on data gathering and document production -- reading 50-page DDQs, cross-referencing SEC filings, normalizing fee structures across managers, assembling IC memos from scattered sources. Only 10-15% goes to the judgment work that justifies their expertise.

AllocatorStack puts that operational knowledge into Claude Code skills so the analyst's time goes to judgment instead of assembly. Open source, on-prem. The AI comes to the data, not the data to the AI.

## Skills

### Manager Due Diligence Pipeline

Run these in order. Each produces JSON that the next one reads.

```
/screen-managers  -->  /prep-manager-meeting  -->  /analyze-ddq  -->  /draft-memo
```

| Skill | Role | What It Does |
|-------|------|-------------|
| `/screen-managers` | Sourcing Analyst | Takes a search mandate, screens candidates against fund criteria and public records (regulatory, litigation), produces a ranked short list |
| `/prep-manager-meeting` | Research Analyst | Prepares agendas, talking points, and reference packets for meetings with shortlisted managers |
| `/analyze-ddq` | DDQ Reviewer | Ingests DDQ PDFs, extracts answers mapped to ILPA categories, compares across managers, flags gaps and outliers |
| `/draft-memo` | IC Memo Drafter | Assembles first-draft IC memo from pipeline data, with provenance links on every claim |

### Quarterly Monitoring

| Skill | Role | What It Does |
|-------|------|-------------|
| `/monitor-adv` | Compliance Analyst | Diffs ADV filings against prior snapshots, scans news and regulatory actions, flags exceptions by severity |

### Additional Skills (v0.2)

| Skill | Role | What It Does |
|-------|------|-------------|
| `/prep-company-meeting` | Research Analyst | Briefing packets for direct company meetings -- governance, financials, engagement topics |
| `/screen-holdings` | RI / Forensic Analyst | Screens holdings for responsible investing risks and forensic accounting red flags |
| `/board-report` | Board Reporting | Board-ready reports with technical sections for the IC and plain-language summaries for trustees |

## How It Works

Skills are SKILL.md files in `.claude/skills/` -- instructions Claude Code follows to do specific allocator work. Four helper scripts (~340 lines Python total) handle what Claude can't do natively:

- `scripts/extract-pdf.py` -- PDF text extraction with page numbers (PyMuPDF)
- `scripts/query-edgar.py` -- SEC EDGAR / IAPD API queries
- `scripts/query-finra.py` -- FINRA BrokerCheck API queries
- `scripts/generate-excel.py` -- Excel comparison matrix output

Skills chain through JSON files in a workspace directory. Schemas define the contracts between stages (`schemas/ddq-output.yaml`, `schemas/manager-profile.yaml`). The ILPA/AIMA DDQ taxonomy (`schemas/ilpa_aima_v1.yaml`) provides a 150+ question framework for structured DDQ analysis.

## Data Sources

Skills pull data from three tiers, depending on what the fund has available:

1. **MCP connector configured** (FactSet, PitchBook, Morningstar, etc.) -- skill queries the source directly
2. **Public API** (SEC EDGAR, FINRA BrokerCheck) -- skill uses helper scripts, always available
3. **No connector** -- skill asks the user to provide data as CSV, Excel, or paste

The fund config specifies which connectors are set up. Skills adapt and tell you what's missing.

## Customization

Copy `samples/configs/example_manager_dd.yaml` and customize for your fund:

- **Fund profile** -- type, AUM, asset class targets, assumed rate of return
- **Evaluation criteria** -- track record minimums, AUM ranges, fee thresholds, disqualifiers
- **Data sources** -- which MCP connectors are configured
- **Templates** -- IC memo, board report, screening report (in `templates/`)

Same skills, different config, different output.

## Sample DDQs

Three synthetic DDQ PDFs in `samples/ddqs/` for testing and demo:

| Manager | Profile | Key Features |
|---------|---------|-------------|
| Granite Peak Capital | Clean, strong performer | Complete DDQ, tables with fee/performance data, consistent disclosures |
| Meridian Value Partners | Borderline | Incomplete sections, key person departure, sparse risk management |
| Osprey Global Advisors | Red flags | 350 bps TER, no hurdle rate, risk limit breaches, cybersecurity incident |

## Design Principles

1. **Agents draft, humans decide.** Every output is a draft for human review. No automated investment decisions.
2. **Show your work.** Every number traces to its source -- `[Source: manager-ddq.pdf, p.12]`.
3. **Fail loudly.** Missing data and implausible results are flagged, never silently passed.
4. **Verification gates.** Human review between pipeline stages.

## See It Work

Here's what running `/analyze-ddq` on the sample DDQs looks like:

```
> /analyze-ddq

Extracting text from 3 DDQ PDFs...
  granite-peak-capital.pdf: 8 pages, 15,227 characters
  meridian-value-partners.pdf: 4 pages, 5,197 characters
  osprey-global-advisors.pdf: 6 pages, 7,838 characters

Mapping answers to ILPA taxonomy (150+ questions across 8 categories)...

Completeness Dashboard:
| Manager         | Answered | Gaps | Confidence |
|-----------------|----------|------|------------|
| Granite Peak    | 48/52    | 4    | HIGH       |
| Meridian Value  | 22/52    | 30   | MEDIUM     |
| Osprey Global   | 31/52    | 21   | MEDIUM     |

Flags:
  Granite Peak:  Complete, consistent data across all categories
  Meridian:      30 unanswered questions, risk management section sparse
  Osprey:        Fee structure inconsistent (150 bps mgmt + 20% carry, no hurdle)

7 follow-up questions generated for Meridian, 5 for Osprey.

HUMAN GATE: Review the extraction before proceeding to /draft-memo.
```

See `docs/skills.md` for detailed walkthroughs of every skill.

## Documentation

| Doc | What It Covers |
|-----|---------------|
| [ETHOS.md](ETHOS.md) | Design philosophy -- why every decision was made |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Technical design -- why a skill pack, not a library |
| [docs/skills.md](docs/skills.md) | Deep dives on every skill with examples |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Developer guide -- how to add skills and scripts |
| [CHANGELOG.md](CHANGELOG.md) | Release notes |

## Testing

```bash
pip install pytest
pytest tests/ -v
```

45 tests covering PDF extraction, SEC/FINRA API queries, and Excel generation.

## Related

- [manager-ADV-parsing](https://github.com/jli0806/manager-ADV-parsing) -- Standalone SEC ADV monitoring app (Streamlit). The `/monitor-adv` skill integrates this functionality.

## License

MIT
