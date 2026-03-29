# AllocatorStack Architecture

This document explains the design decisions behind AllocatorStack — why it is
built the way it is, not just what it contains.

---

## 1. The Core Idea

AllocatorStack is a Claude Code skill pack, not a Python library or a SaaS
application. The reason is simple: the hard part of due diligence is reading
comprehension. A DDQ reviewer reads a 25-page PDF, matches answers to a
taxonomy of 150+ questions, compares responses across managers, and
flags gaps and outliers. Claude does all of that natively. Python scripts handle
only what Claude cannot: extracting text from binary PDFs (PyMuPDF needs native
bindings), calling rate-limited government APIs (SEC EDGAR, FINRA BrokerCheck),
and generating Excel files (openpyxl). Total Python across the entire project:
approximately 400 lines in 4 scripts. Everything else — the analysis, the
comparison, the memo drafting, the gap detection — is Claude reading documents
and following instructions.

---

## 2. Why Skill Packs

AllocatorStack follows the gstack pattern. Each skill is a SKILL.md file:
markdown instructions that Claude Code follows directly. There is no application
server, no database, no deployment pipeline, no compiled binary. A CIO can open
the SKILL.md file, read it in five minutes, and understand exactly what the
agent does, what it produces, and where it pauses for human review. This is not
a minor convenience — in fiduciary settings, the people accountable for
investment decisions need to understand what the tool is doing.

```
┌─────────────────────────────────────────────────────────┐
│                    How a Skill Runs                      │
│                                                         │
│  User types /analyze-ddq                                │
│        │                                                │
│        ▼                                                │
│  Claude Code loads analyze-ddq/SKILL.md                 │
│        │                                                │
│        ▼                                                │
│  Claude follows the workflow instructions:               │
│    1. Runs extract-pdf.py (Bash)                        │
│    2. Reads ILPA taxonomy (YAML)                        │
│    3. Maps DDQ answers to taxonomy (native LLM)         │
│    4. Cross-refs claims vs ADV filings (native LLM)     │
│    5. Writes ddq-output.json to workspace               │
│    6. Presents summary to user                          │
│        │                                                │
│        ▼                                                │
│  ┌─────────────┐                                        │
│  │ HUMAN GATE  │  User reviews, edits, approves         │
│  └─────────────┘                                        │
└─────────────────────────────────────────────────────────┘
```

The SKILL.md frontmatter declares allowed tools (`Read`, `Write`, `Bash`,
etc.), a description, and the skill name. The body is a step-by-step workflow
with embedded Bash blocks for the helper scripts. Claude Code reads it and
executes it. That is the entire runtime.

---

## 3. The Pipeline Model

Skills chain through JSON files in a shared workspace directory. Each skill
reads the previous skill's output and writes its own. The workspace is a plain
directory on disk — no database, no message queue, no service bus.

```
workspace/<run-id>/
│
│  /screen-managers
│  ┌────────────────────┐
│  │ Screen candidates   │
│  │ against fund        │
│  │ criteria + red      │
│  │ flag checks         │
│  └────────┬───────────┘
│           │
│           ▼
│  manager-profiles.json
│           │
│      HUMAN GATE ◄── "Approve short list"
│           │
│  /prep-manager-meeting
│  ┌────────────────────┐
│  │ Prepare agendas,   │
│  │ talking points,    │
│  │ reference packets  │
│  └────────┬───────────┘
│           │
│      HUMAN GATE ◄── "Review agenda, add questions"
│           │
│  /analyze-ddq
│  ┌────────────────────┐
│  │ Extract DDQ text,  │
│  │ map to ILPA,       │
│  │ cross-ref vs ADV   │
│  └────────┬───────────┘
│           │
│           ▼
│  ddq-output.json
│           │
│      HUMAN GATE ◄── "Review extraction, check discrepancies"
│           │
│  /draft-memo
│  ┌────────────────────┐
│  │ Assemble IC memo   │
│  │ from structured    │
│  │ data + template    │
│  └────────┬───────────┘
│           │
│           ▼
│  ic-memo-draft.md
│           │
│      HUMAN GATE ◄── "Review draft, write judgment sections"
```

Every arrow between skills passes through a human gate. The user approves the
short list before meeting prep begins. The user reviews DDQ extraction before
the memo is drafted. No skill auto-triggers the next one. This is deliberate
(see Section 8).

The workspace directory retains all intermediate outputs. A user can re-run any
skill by invoking it with the same run-id. If the DDQ extraction looks wrong,
fix the inputs and re-run `/analyze-ddq` — the memo skill will pick up the new
`ddq-output.json` on its next run.

---

## 4. Schema Contracts

Two YAML schema files define the handoff points between skills:

- **`schemas/manager-profile.yaml`** — Output format of `/screen-managers`.
  Contains manager name, CRD number, AUM, strategy, regulatory flags, and
  screening scores. This is what `/prep-manager-meeting` and `/analyze-ddq`
  read as input.

- **`schemas/ddq-output.yaml`** — Output format of `/analyze-ddq`. Contains
  extracted answers mapped to ILPA categories, provenance (source file + page
  number), confidence scores, completeness percentages, and ADV cross-reference
  results. This is what `/draft-memo` reads as input.

Each skill checks for the existence of its prerequisite files before running.
If `/draft-memo` cannot find `ddq-output.json`, it tells the user to run
`/analyze-ddq` first rather than failing silently or producing an empty memo.

The schemas serve three purposes: they document the data contract between
skills, they give Claude a structural target when producing output, and they
let a human inspect intermediate JSON and understand what each field means.

---

## 5. The ILPA Taxonomy

The ILPA/AIMA Due Diligence Questionnaire is the industry standard for
alternative investment manager evaluation. AllocatorStack uses it as the common
data model — the Rosetta Stone that makes DDQs from different managers
comparable.

The taxonomy lives in `schemas/ilpa_aima_v1.yaml` and contains 162 questions
across 9 categories:

```
Category                          Questions
─────────────────────────────────────────────
1. Organization & Structure           ~25
2. Investment Strategy & Process      ~22
3. Risk Management                    ~18
4. Operations & Infrastructure        ~20
5. Compliance & Regulatory            ~15
6. Fees & Expenses                    ~12
7. Performance & Track Record         ~18
8. Responsible Investing & Sustainability  ~15
```

When `/analyze-ddq` processes a DDQ PDF, Claude maps each extracted answer to
the corresponding ILPA question. This is reading comprehension — a DDQ from
Manager A might call it "Key Person Risk" on page 12 while Manager B calls it
"Team Dependency" on page 8, but both map to ILPA question 1.15. The taxonomy
normalizes this so the comparison matrix works.

Non-ILPA DDQ formats are handled best-effort. Claude maps what it can and flags
low-confidence areas. This works better than rule-based parsing because the
mapping is semantic, not syntactic.

---

## 6. Helper Scripts

Four Python scripts, approximately 400 lines total.

| Script | Purpose | Why Python |
|--------|---------|------------|
| `scripts/extract-pdf.py` | Extract text from PDF files with page numbers | PyMuPDF requires native C bindings. Claude can read PDFs visually but cannot reliably extract text at scale with page-level provenance. |
| `scripts/query-edgar.py` | Query SEC EDGAR IAPD API for ADV filing data | Rate limiting (SEC requires 10 req/sec max), XML parsing of ADV form structure, retry logic. |
| `scripts/query-finra.py` | Query FINRA BrokerCheck for registration data | Same pattern — API wrapper with rate limiting and structured JSON output. |
| `scripts/generate-excel.py` | Generate Excel comparison matrices | openpyxl for .xlsx generation. Claude cannot produce binary Excel files. |

Each script reads from and writes to the workspace directory. Each produces
JSON output (or an Excel file). Each can be run independently from the command
line for debugging. The scripts are tools that Claude invokes via Bash blocks
in the SKILL.md workflows — they are not a framework, not a library, not an
abstraction layer.

---

## 7. Data Source Tiering

Skills pull data from three tiers, adapting to what is available:

```
Tier 1: MCP Connectors (richest data, requires configuration)
┌──────────────────────────────────────────────┐
│ FactSet  │  PitchBook  │  Morningstar       │
│ Bloomberg│  Preqin     │  eVestment          │
└──────────────────────────────────────────────┘
        │  Not configured? Fall through.
        ▼
Tier 2: Public APIs (always available, free)
┌──────────────────────────────────────────────┐
│ SEC EDGAR / IAPD  │  FINRA BrokerCheck      │
│ OFAC SDN List     │  SEC AAER / Litigation   │
└──────────────────────────────────────────────┘
        │  API down? Fall through.
        ▼
Tier 3: User-Provided (fallback)
┌──────────────────────────────────────────────┐
│ CSV uploads  │  Excel files  │  Paste text   │
│ Manual entry │  Prior run data               │
└──────────────────────────────────────────────┘
```

The fund configuration YAML (`samples/configs/example_manager_dd.yaml`)
declares which MCP connectors are set up. Skills check the config, use what is
available, and explicitly report what is missing. If the SEC EDGAR API is
unreachable, `/analyze-ddq` still runs — it just notes "ADV cross-reference
skipped: SEC EDGAR unavailable" in the output. The user sees exactly what data
informed the analysis and what did not.

This tiering means AllocatorStack works on day one with zero connector setup
(Tier 2 + Tier 3), and gets richer as you configure data sources.

---

## 8. Human Gates

Every skill pauses for human review before its output is consumed downstream.
This is a fiduciary requirement, not a UX choice.

Allocators are fiduciaries. They have a legal obligation to exercise prudent
judgment when selecting and monitoring investment managers. An AI tool that
auto-approves a short list or auto-generates an IC memo without human review
creates legal liability. The human gates exist because:

1. **Regulatory expectation.** SEC and DOL expect documented human judgment at
   each stage of the manager selection process. "The AI did it" is not a
   defense.

2. **Error propagation.** A misextracted AUM figure in `/analyze-ddq` becomes
   a wrong number in the IC memo if no one checks. Human gates are circuit
   breakers.

3. **Judgment sections.** Certain parts of an IC memo — the investment thesis,
   the risk assessment, the recommendation — require the PM's professional
   judgment. Claude drafts the scaffolding; the human writes the judgment.

4. **Provenance verification.** Every quantitative claim in the output includes
   `[Source: file, page]` notation. The human gate is where someone spot-checks
   those references.

The design principle: **agents draft, humans decide.**

---

## 9. What We Didn't Build

Several things that might seem like obvious features were intentionally omitted.

**No database.** The workspace directory with JSON files is the data store.
Each pipeline run produces a self-contained directory with all inputs, intermediate
outputs, and final deliverables. JSON is human-readable, diffable with git,
and requires no server process. A SQLite provenance store was considered and
rejected — it adds complexity without adding capability that JSON does not
already provide.

**No CLI.** Claude Code IS the CLI. There is no `allocator` binary, no
`allocator analyze --input ddq.pdf` command. The user types `/analyze-ddq` in
Claude Code and the skill runs. Adding a separate CLI would mean maintaining
two interfaces to the same functionality.

**No web UI.** The terminal is sufficient for v1. The users are investment
professionals working in Claude Code, not casual consumers who need a dashboard.
A web comparison matrix (Flask/Streamlit) is deferred to post-v1 and would
read from the same workspace JSON files.

**No authentication.** AllocatorStack runs locally on a single user's machine
under their Claude Code session. There is no multi-user scenario in v1, so
there is no auth system. This changes if/when the tool supports shared
workspaces.

**No Python library.** The original design had 20+ Python files with an
AgentRegistry, WorkflowContext, PipelineConfig, and DataAdapter ABC. All of
that was deleted. Claude does the analysis natively; wrapping it in Python
abstractions adds indirection without adding capability. The gstack pattern
proved that SKILL.md files are sufficient.

**No Jinja2 rendering.** IC memo templates exist as markdown guidance files,
not as Jinja2 templates that a rendering engine processes. Claude reads the
template and drafts the memo directly. The template is a reference, not a
program.

---

## Summary

```
┌──────────────────────────────────────────────────────┐
│                  AllocatorStack                       │
│                                                      │
│  5 SKILL.md files      = the workflows               │
│  3 YAML schemas        = the data contracts          │
│  4 Python scripts      = the native-binding glue     │
│  1 YAML fund config    = the customization layer     │
│  1 workspace directory = the data store              │
│                                                      │
│  Claude Code           = the runtime                 │
│  The human             = the decision maker          │
└──────────────────────────────────────────────────────┘
```

The architecture is deliberately minimal. Every component exists because
removing it would make the tool unable to do its job. Nothing exists because
"we might need it later."
