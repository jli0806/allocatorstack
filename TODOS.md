# Roadmap

## v0.1 (shipped)

Core manager due diligence pipeline: `/screen-managers` → `/prep-manager-meeting` → `/analyze-ddq` → `/draft-memo`. Plus `/monitor-adv` for quarterly monitoring. ILPA schema, output contracts, sample DDQs, golden output, 45 tests, documentation.

---

## v0.2 — Real-world hardening

The gap between sample data and real DDQs. These items come from running the pipeline on actual institutional documents.

### Test on real DDQs
- **What:** Run `/analyze-ddq` on 5-10 real DDQs (different managers, different formats, different lengths). Document where extraction breaks, where confidence scoring is wrong, where the ILPA mapping misses.
- **Why:** Sample DDQs are 4-8 pages with clean formatting. Real DDQs are 40-80 pages with inconsistent headers, embedded tables, appendices, and non-ILPA structures. The skill instructions need to be calibrated against real data.
- **Depends on:** Access to real (non-confidential) DDQs, or DDQs from a willing pilot fund.

### Register remaining 3 skills
- **What:** Move `/prep-company-meeting`, `/screen-holdings`, `/board-report` into `.claude/skills/` with the same structure as the core 5.
- **Why:** Completes the full 8-skill offering.
- **Depends on:** Nothing. Can do anytime.

### Refine ILPA schema from real data
- **What:** After testing on real DDQs, update the ILPA schema with questions that real DDQs actually answer vs. what the template says they should answer. Add common non-ILPA questions that keep appearing.
- **Why:** The current schema is based on the ILPA template. Real DDQs deviate — some add proprietary sections, some skip categories, some use different numbering.

### SEC EDGAR integration
- **What:** The IAPD API endpoint returns 403 for programmatic access. Either: (a) scrape the IAPD website, (b) use EDGAR XBRL feeds for ADV data, (c) accept ADV PDFs as user-provided input, or (d) integrate with a licensed data provider.
- **Why:** ADV cross-referencing is a useful optional step but currently doesn't work. Need to decide on the right approach.
- **Context:** This is optional verification, not core pipeline. The pipeline works without it.

### Integrate manager-ADV-parsing Streamlit app
- **What:** Bridge the existing [manager-ADV-parsing](https://github.com/jli0806/manager-ADV-parsing) app into `/monitor-adv`.
- **Why:** The Streamlit app already does ADV parsing and diffing. Integration path undefined: extract parsing logic into helper script vs. invoke as separate tool vs. keep as companion project.

---

## v0.3 — Multi-run and institutional workflows

### Persistent workspace with run history
- **What:** Track runs over time. Compare DDQ extractions across vintages (e.g., "what changed in Granite Peak's DDQ from last year?"). Link meeting notes to DDQ follow-ups.
- **Why:** Manager relationships span years. The pipeline should accumulate context, not start from scratch each time.

### Fund-specific ILPA extensions
- **What:** Let funds add custom questions to the ILPA schema (the `custom` category exists but isn't wired up). Custom questions should flow through the full pipeline — extraction, comparison, memo.
- **Why:** Every fund has questions that aren't in the ILPA template. Public pension funds ask about state-specific compliance. Endowments ask about mission alignment.

### Multi-manager comparison at scale
- **What:** Handle 10-20 managers in a single comparison run (current samples test 3). The comparison matrix and Excel output need to work at this scale without degrading.
- **Why:** Real searches often shortlist 8-15 managers. The comparison matrix is the most useful output and needs to scale.

---

## v0.4 — Distribution and deployment

### Skills Directory submission
- **What:** Package skills for Anthropic's Skills Directory. Understand the submission requirements, packaging format, and review process.
- **Why:** Distribution channel that doesn't require direct sales. Funds discover AllocatorStack in the directory, admin enables it, team is live.

### Setup script
- **What:** Single `./setup` command that installs Python dependencies, validates the environment, and confirms skills are discoverable.
- **Why:** `pip install pymupdf requests openpyxl` is fine for developers but not for an investment team admin.

### Configuration wizard
- **What:** Interactive setup that walks a new fund through creating their config file. "What's your fund type? What's your AUM? What benchmarks do you use? What data sources do you have?"
- **Why:** The YAML config is readable but not obvious for a first-time user. A guided setup reduces the barrier.

---

## Not on the roadmap

These are out of scope and will stay out of scope:

- **Portfolio management, trading, rebalancing.** Wrong tool. Use Aladdin, FactSet, Bloomberg PORT.
- **Real-time risk analytics.** Same reason. Claude skills are for document workflows, not live data.
- **Multi-user access control.** The tool runs on the analyst's machine or within their Claude plan. Enterprise auth is Anthropic's problem, not ours.
- **Web dashboard.** The terminal and Claude's chat interface are sufficient. Adding a web UI adds deployment complexity for marginal UX gain.
