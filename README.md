# AllocatorStack

Claude skills for allocator front-office operations.

Drop in DDQ PDFs from multiple managers. Get a structured side-by-side comparison mapped to the ILPA taxonomy, a completeness dashboard showing what's missing, and a first-draft IC memo with provenance on every number. Each skill encodes the workflow of a specific role in an investment office. Humans review at every stage.

## Quick Start

```bash
git clone https://github.com/jli0806/allocatorstack.git
cd allocatorstack
pip install pymupdf requests openpyxl

# Extract 3 sample DDQs
./demo

# Then in Claude, run the pipeline:
# /analyze-ddq     <- map DDQ answers to ILPA taxonomy, flag gaps and outliers
# /draft-memo      <- generate IC memo with provenance links
```

## Why This Matters

Without a skill, asking Claude to "analyze this DDQ" produces different output every time -- different structure, different things flagged, no consistent schema. There's no way to compare two managers on the same basis, no provenance chain, no pipeline that passes structured data from one stage to the next.

A SKILL.md file encodes the full workflow: extract text with page numbers, map answers to the ILPA/AIMA taxonomy, score confidence per answer, generate a completeness dashboard by category, flag gaps and outliers, pause for the analyst to review before proceeding. Output goes to a defined JSON schema that the next skill reads directly.

A CIO can open a SKILL.md, read it in five minutes, and understand what the agent does, what it produces, and where it pauses for human review. A Python library with the same behavior spread across 20 files does not offer that.

## Skills

### Manager Due Diligence Pipeline

Each skill produces JSON that the next one reads. Human review between stages.

```
/screen-managers  -->  /prep-manager-meeting  -->  /analyze-ddq  -->  /draft-memo
```

| Skill | Role | What It Does |
|-------|------|-------------|
| `/screen-managers` | Sourcing Analyst | Takes a search mandate, screens candidates against fund criteria and public records, produces a ranked short list |
| `/prep-manager-meeting` | Research Analyst | Prepares agendas, talking points, and reference packets for manager meetings |
| `/analyze-ddq` | DDQ Reviewer | Ingests DDQ PDFs, extracts answers mapped to ILPA categories, compares across managers, flags gaps and outliers |
| `/draft-memo` | IC Memo Drafter | Assembles first-draft IC memo from pipeline data, with provenance on every claim |

### Quarterly Monitoring

| Skill | Role | What It Does |
|-------|------|-------------|
| `/monitor-adv` | Compliance Analyst | Diffs ADV filings against prior snapshots, scans regulatory actions, flags exceptions by severity |

### Additional Skills (v0.2)

| Skill | Role | What It Does |
|-------|------|-------------|
| `/prep-company-meeting` | Research Analyst | Briefing packets for direct company meetings -- governance, financials, engagement topics |
| `/screen-holdings` | Sustainability / Forensic Analyst | Screens holdings for responsible investing risks and forensic accounting red flags |
| `/board-report` | Board Reporting | Board-ready reports with technical sections for the IC and plain-language summaries for trustees |

## How It Works

Skills are SKILL.md files -- instructions Claude follows to do specific allocator work. Four helper scripts (~400 lines Python total) handle things Claude can't do natively: parsing PDF binaries, calling rate-limited government APIs, generating Excel files. Everything else -- the reading comprehension, the taxonomy mapping, the comparison, the memo drafting -- Claude does directly.

Skills chain through JSON files in a workspace directory. Schemas define the contracts between stages. The ILPA/AIMA DDQ taxonomy provides a 150+ question framework that makes DDQs from different managers comparable on the same basis.

## Deployment

Install the skills in any Claude plan that supports custom skills -- Max, Team, or Enterprise. Admin uploads the skill files, provisions to the investment team. The end user opens Claude, drops in a DDQ, and runs `/analyze-ddq`. No server, no CI/CD, no infrastructure.

For development and testing, clone the repo and run skills through Claude Code.

## Data Sources

Skills pull data from three tiers:

1. **MCP connector** (FactSet, PitchBook, Morningstar) -- skill queries the source directly
2. **Public API** (SEC EDGAR, FINRA BrokerCheck) -- always available via helper scripts
3. **User-provided** (CSV, Excel, paste) -- the fallback when no connector exists

The fund config specifies which connectors are set up. Skills use what's available and tell you what's missing. A fund with no connectors runs the full pipeline -- they provide their own data at the screening step.

## Customization

Each fund provides configuration in YAML, not code:

- **Fund profile** -- type, AUM, asset class targets, assumed rate of return
- **Evaluation criteria** -- track record minimums, AUM ranges, fee thresholds, disqualifiers
- **Data sources** -- which connectors are configured
- **Templates** -- IC memo, board report, screening report

Same skills, different config, different output. See `samples/configs/example_manager_dd.yaml`.

## Sample DDQs

Three synthetic DDQ PDFs in `samples/ddqs/`:

| Manager | Profile | Key Features |
|---------|---------|-------------|
| Granite Peak Capital | Clean, strong performer | Complete DDQ, tables with fee/performance data, consistent disclosures |
| Meridian Value Partners | Borderline | Incomplete sections, key person departure, sparse risk management |
| Osprey Global Advisors | Red flags | 350 bps TER, no hurdle rate, risk limit breaches, cybersecurity incident |

Sample candidate data for screening: `samples/candidate-data.csv` (8 managers, including pass/fail/borderline cases).

Expected output from running the pipeline on these samples: `samples/expected-output/`. These are simplified examples on synthetic data -- real institutional DDQs are 40-80 pages with dense narrative, and the analysis is correspondingly deeper.

## Scope

AllocatorStack covers **manager selection, due diligence, and monitoring** -- the document-heavy, judgment-heavy workflows where analysts spend most of their time.

It does not cover portfolio management, trading, risk analytics, or asset allocation optimization. Those are quantitative, real-time problems that need specialized systems (Aladdin, FactSet, Bloomberg PORT). Claude skills are the wrong tool for that work and the right tool for reading DDQs, comparing managers, drafting memos, and monitoring regulatory filings.

## See It Work

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

## How This Ages

Traditional AI applications write orchestration code to chain LLM calls, parse outputs, manage state. When the model improves, that code becomes a constraint -- doing worse what the model would now do natively.

SKILL.md files are instructions. When Claude improves, the skills improve with it. The only maintained code is four helper scripts for things Claude genuinely cannot do today: parsing PDF binaries, calling rate-limited APIs, generating Excel files. That list gets shorter over time, not longer.

| | Traditional AI app | AllocatorStack |
|---|---|---|
| Code to maintain | Thousands of lines | ~400 lines across 4 scripts |
| Deployment | Server, CI/CD, hosting | Upload skill files |
| Updates | Release cycle, versioning | Edit the markdown file |
| Customization | Code changes | Edit YAML config |
| Who can modify | Developers | Anyone who can read the SKILL.md |

## Documentation

| Doc | What It Covers |
|-----|---------------|
| [ETHOS.md](ETHOS.md) | Design philosophy |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Technical design decisions |
| [docs/skills.md](docs/skills.md) | Skill deep dives with examples |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Developer guide |
| [CHANGELOG.md](CHANGELOG.md) | Release notes |

## Testing

```bash
pip install pytest
pytest tests/ -v
```

45 tests covering PDF extraction, SEC/FINRA API queries, and Excel generation.

## Related

- [manager-ADV-parsing](https://github.com/jli0806/manager-ADV-parsing) -- Standalone SEC ADV monitoring app (Streamlit). The `/monitor-adv` skill integrates this.

## License

MIT
