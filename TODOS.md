# TODOS

Items are numbered in dependency order. Complete them sequentially (or in parallel where noted).

## HIGH Priority (blocks v0.1 announcement)

### 1. Populate ILPA schema questions
- **What:** Fill in ~200 questions across the 9 categories in `schemas/ilpa_aima_v1.yaml`. Each question needs an id, text, answer_type, and required flag.
- **Why:** The schema is the foundation for `/analyze-ddq` — it defines what questions exist and how answers are categorized. Currently all `questions: []` arrays are empty.
- **Pros:** Unblocks sample DDQ creation, enables taxonomy mapping in `/analyze-ddq`, gives the project real domain substance.
- **Cons:** Requires domain expertise to get question coverage and wording right.
- **Context:** The ILPA/AIMA DDQ template is the industry standard. Cover all 9 categories: investment strategy, organization/team, track record, fees/terms, risk management, compliance, responsible investing, cybersecurity. The schema already has the category structure — just needs the questions populated.
- **Depends on:** Nothing. This is step zero.

### 2. Define output schema contracts
- **What:** Create `schemas/ddq-output.yaml` and `schemas/manager-profile.yaml` defining the JSON structures that skills produce and consume.
- **Why:** Skills pass data through the workspace via JSON files. Without defined contracts, `/analyze-ddq` output won't reliably feed into `/draft-memo`, and `/screen-managers` output won't feed into `/prep-manager-meeting`.
- **Pros:** Makes the pipeline composable and testable. Each skill can validate its inputs and outputs.
- **Cons:** Contracts may need iteration once tested with real data.
- **Context:** The design doc has top-level field definitions for both schemas. `/analyze-ddq` SKILL.md already references `ddq-output.yaml` and `/screen-managers` references `manager-profile.yaml`, but neither file exists. Ensure ddq-output.yaml includes ADV cross-reference fields (ADV cross-referencing is step 3 of /analyze-ddq).
- **Depends on:** ILPA schema (the DDQ output schema maps to ILPA categories).

### 3. Fix query-edgar.py to use real SEC IAPD API
- **What:** Replace the ADVFN third-party endpoint (`https://api.advfn.com/v2`) in `scripts/query-edgar.py` with the actual SEC Investment Adviser Public Disclosure (IAPD) API endpoints.
- **Why:** ADVFN is a third-party aggregator, not the official SEC system. Data could be stale, incomplete, or unavailable if ADVFN changes their API. The ADV cross-referencing demo depends on accurate SEC data.
- **Pros:** Correct, authoritative data source. No third-party dependency for core functionality.
- **Cons:** SEC IAPD API documentation is sparse; may need to reverse-engineer endpoints from the IAPD website.
- **Context:** The `search_firms()` function correctly uses EDGAR full-text search. Only `get_adv_by_crd()` uses the wrong endpoint. The real IAPD API serves ADV filing data at SEC-hosted URLs. The script is only 82 lines — straightforward fix.
- **Depends on:** Nothing. Can be done in parallel with #1-2.

### 4. Harden extract-pdf.py
- **What:** Two fixes: (1) detect password-protected PDFs with a clear error message instead of a generic exception, (2) detect scanned image PDFs (pages exist but no selectable text) and add a warning flag in the JSON output.
- **Why:** Both are realistic failure modes for institutional DDQs. Password-protected PDFs are common when managers send confidential documents. Scanned PDFs produce empty extraction with no indication of why.
- **Pros:** Clear error messages prevent user confusion. Scanned PDF detection enables the /analyze-ddq skill to flag "OCR required" as designed.
- **Cons:** None — ~10 lines of code total.
- **Context:** Eng review items #13 (password detection) and failure mode analysis (scanned PDF detection). PyMuPDF raises `fitz.FileDataError` for encrypted PDFs. Scanned PDFs can be detected by checking if any page has non-empty text.
- **Depends on:** Nothing. Can be done in parallel with #1-3.

### 5. Create synthetic sample DDQs
- **What:** Create 3 synthetic DDQ PDFs that follow the ILPA template structure, generated via pandoc from markdown source.
- **Why:** Real DDQs are confidential. Without sample data, the pipeline can't be demoed or tested end-to-end.
- **Pros:** Enables full pipeline testing, provides demo material for README, serves as test fixtures for pytest.
- **Cons:** Requires domain expertise to make realistic enough to be credible.
- **Context:** Three fictional managers per the CEO plan: (1) **Granite Peak Capital** — strong performer, clean compliance, complete DDQ. (2) **Meridian Value Partners** — borderline: AUM discrepancy vs ADV, incomplete DDQ, key person risk. (3) **Osprey Global Advisors** — red flags: SEC enforcement history, inconsistent fees, risk management gaps. 15-25 pages each, ILPA template numbering. Include tables (fee schedules, performance data) in at least one. Include non-standard formatting in one to test graceful degradation.
- **Depends on:** ILPA schema (#1) — need to know what questions to answer.

### 6. Write pytest for helper scripts
- **What:** Write tests for all 4 helper scripts in `scripts/` (extract-pdf.py, query-edgar.py, query-finra.py, generate-excel.py). Use sample DDQs as test fixtures for PDF extraction. Mock SEC/FINRA API responses for network tests.
- **Why:** These scripts handle PDF extraction and API calls — the most failure-prone parts of the pipeline. Tests catch regressions and document expected behavior.
- **Pros:** Confidence in the data layer before demo. Catches bugs from the API fix (#4) and PDF hardening (#5).
- **Cons:** Need mock data for SEC/FINRA API responses.
- **Context:** 22 test paths identified in eng review test coverage audit: extract-pdf (8 paths including password/scanned detection), query-edgar (5 paths), query-finra (4 paths), generate-excel (4 paths), plus schema validation.
- **Depends on:** Sample DDQs (#5) for PDF extraction fixtures. API fix (#3) and PDF hardening (#4) for testing new code paths.

### 7. Register core skills in .claude/skills/
- **What:** Move 5 core skills (`/screen-managers`, `/prep-manager-meeting`, `/analyze-ddq`, `/draft-memo`, `/monitor-adv`) into `.claude/skills/` directory so they're invocable in Claude Code. Add run-id workspace namespacing (`workspace/<run-id>/`). Add schema references to each SKILL.md frontmatter.
- **Why:** Skills currently exist as standalone SKILL.md files in the repo root. Claude Code discovers skills from `.claude/skills/`. Without registration, no skill can actually be invoked.
- **Pros:** Makes the skill pack actually usable. Run-id namespacing prevents workspace collisions across runs.
- **Cons:** Need to test the registration path and ensure SKILL.md format is compatible with Claude Code's discovery.
- **Context:** Follows the gstack pattern. Each skill needs YAML frontmatter (name, description, allowed-tools) and schema refs. The 3 non-core skills (/prep-company-meeting, /screen-holdings, /board-report) move in v0.2.
- **Depends on:** Output schemas (#2) — skills reference them in frontmatter.

### 8. Add prerequisite checks to skills
- **What:** Each skill verifies its required inputs exist before running. E.g., `/draft-memo` checks that `workspace/<run-id>/ddq-output.json` exists and tells user to run `/analyze-ddq` first. `/analyze-ddq` checks that DDQ PDF paths were provided.
- **Why:** Without checks, skills fail mid-run with confusing errors when upstream data is missing.
- **Pros:** Better UX — clear error messages pointing to what's missing and which skill to run first.
- **Cons:** Small amount of work per skill (~5 lines each).
- **Context:** Identified in eng review. Part of making the pipeline robust for demo. Checks validate against the schema contracts (#2).
- **Depends on:** Schema contracts (#2), skill registration (#7).

### 9. Create CLAUDE.md project instructions
- **What:** Create a CLAUDE.md at the repo root with project-level instructions for Claude Code: what the skill pack does, workspace conventions, how skills chain, data source configuration, and the human gate pattern.
- **Why:** CLAUDE.md is how Claude Code users discover and understand a skill pack. It's the first thing Claude reads when entering the project directory.
- **Pros:** Essential for announcement — users need to know how to use the skills. Documents the workspace convention and skill chaining pattern.
- **Cons:** None.
- **Context:** Eng review item #8. The design doc and CEO plan both reference this. Should include: skill inventory, workspace layout, config instructions, pipeline overview, and human gate explanation.
- **Depends on:** Skill registration (#7) — CLAUDE.md references the registered skill names.

### 10. Create board report template
- **What:** Create `templates/board_report.md` — the template referenced by `/board-report` SKILL.md.
- **Why:** The skill references this template but it doesn't exist, creating a broken reference visible to anyone exploring the repo.
- **Pros:** Completes the template set (IC memo, screening report, board report). Prevents runtime errors if someone runs /board-report.
- **Cons:** None — ~30-40 lines of markdown.
- **Context:** Only `templates/ic_memo.md` and `templates/screening_report.md` exist. Board report template should follow the same pattern: header, sections for portfolio overview, manager performance, risk metrics, trustee summary, compliance attestations.
- **Depends on:** Nothing. Can be done in parallel with anything.

### 11. Create demo script and README demo instructions
- **What:** Create a `demo` shell script that runs the full pipeline on sample DDQs (extract → analyze → draft memo). Update README with installation instructions, demo walkthrough, and sample output.
- **Why:** The announcement trigger is "this exists, it works, and you can try it." The demo script is the 5-minute path from clone to "whoa."
- **Pros:** Makes the announcement concrete. Lets anyone verify the pipeline works end-to-end.
- **Cons:** Demo script needs sample DDQs and registered skills to work.
- **Context:** CEO plan scope decision #8 accepted `allocator demo` command. Design doc step 13: "Announce — README, working demo." README currently says "v0.1.0, core pipeline under active construction" — needs to be updated for announcement.
- **Depends on:** Sample DDQs (#5), registered skills (#7), CLAUDE.md (#9). This is the final task before announcement.

## MEDIUM Priority (v0.2)

### Wire non-core skills as slash commands
- **What:** Move /prep-company-meeting, /screen-holdings, /board-report into .claude/skills/ and update their SKILL.md files with schema references and run-id workspace paths.
- **Why:** These skills are fully defined but not part of the v0.1 demo pipeline. Wiring them up expands the skill pack's utility.
- **Pros:** Completes the full 8-skill offering. Holdings screening and board reporting are high-value for allocator teams.
- **Cons:** Each skill needs testing with real-ish data to validate the workflow.
- **Context:** SKILL.md files are written and reviewed. They need the same updates applied to the core 5 skills (schema refs, workspace run-id paths, CLAUDE.md awareness).
- **Depends on:** Core 5-skill pipeline working end-to-end.

### Integrate manager-ADV-parsing Streamlit app
- **What:** Bridge the existing manager-ADV-parsing Streamlit app into the /monitor-adv skill.
- **Why:** The Streamlit app already does ADV parsing and diffing. The /monitor-adv SKILL.md references it but the integration path (adapt into helper script vs. invoke Streamlit app) is undefined.
- **Pros:** Reuses existing tested code. Provides a visual UI option alongside the skill.
- **Cons:** Streamlit app may need refactoring to work as a CLI tool invoked by the skill.
- **Context:** The Streamlit app lives in a separate repo (github.com/jli0806/manager-ADV-parsing). Need to decide: (a) extract the parsing logic into a helper script, or (b) have the skill invoke the Streamlit app, or (c) keep them as separate tools that share a data format.
- **Depends on:** /monitor-adv skill being wired up (already in v0.1 core).
