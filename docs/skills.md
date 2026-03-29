# AllocatorStack Skills -- Deep Dive

AllocatorStack ships eight skills. Each one maps to a job that someone in an allocator's front office does today -- screening managers, reading DDQs, drafting memos, monitoring filings, preparing for meetings, screening holdings, and reporting to the board. The skills are SKILL.md files that give Claude the operational knowledge to do these jobs: which taxonomy to use, what counts as a material discrepancy, where to pause for human review, and how to chain provenance from a DDQ page number all the way through to an IC memo.

This document explains what each skill does, when you would reach for it, what a real interaction looks like, and how the skills connect to each other.

---

## Skill Overview

| Skill | Role | One-liner |
|-------|------|-----------|
| `/screen-managers` | Sourcing Analyst | Screen candidates against a search mandate, check regulatory records, produce a ranked short list |
| `/prep-manager-meeting` | Research Analyst | Build agendas, talking points, and reference packets for manager meetings |
| `/analyze-ddq` | DDQ Reviewer | Extract DDQ answers into ILPA categories, cross-reference claims against ADV filings |
| `/draft-memo` | IC Memo Drafter | Assemble a first-draft IC memo with provenance on every number |
| `/monitor-adv` | Compliance Analyst | Quarterly monitoring -- diff ADV filings, scan for news and regulatory actions, flag exceptions |
| `/screen-holdings` | RI / Forensic Analyst | Screen holdings for responsible investing risks and forensic accounting red flags |
| `/prep-company-meeting` | Research Analyst | Briefing packets for direct company meetings -- governance, financials, engagement |
| `/board-report` | Board Reporting Specialist | Board-ready reports with technical and plain-language trustee sections |

---

## Core Pipeline

These four skills form the manager due diligence pipeline. They run in sequence -- each one produces structured data that the next one consumes. You can run any skill standalone, but running them in order gives you a complete pipeline from search mandate to IC memo.

---

### /screen-managers

#### What it does

Takes a search mandate from your fund config (e.g., "US small cap value, $1B-$10B AUM, 5-year minimum track record, sub-100bps management fee") and screens candidate managers against those criteria. It normalizes returns to a common basis, runs red flag checks against SEC EDGAR and FINRA BrokerCheck, and produces a ranked comparison matrix. Every manager gets a PASS / FAIL / BORDERLINE on each criterion and a CLEAR / FLAG / INCOMPLETE on regulatory checks. The output is a short list with rationale, ready for your review.

#### When to use it

You have a new allocation to fill. The investment committee has approved a search in US small cap value, and you need to go from a universe of candidates to a short list of three to five managers worth meeting. This is the first step.

#### Example dialogue

> **You:** Screen managers for our US small cap value search. Here's the candidate data from eVestment -- I exported it as CSV.
>
> **Claude:** I've read your fund config. The mandate is US small cap value, benchmarked to Russell 2000 Value. Criteria: $1B-$10B AUM, 5+ year track record, management fee under 100bps, SEC registered, sustainability policy required. Disqualifiers: SEC enforcement actions, key person departures within 12 months, AUM discrepancies over 20%.
>
> I see 14 managers in the CSV. Let me normalize returns, run red flag checks, and screen against your criteria.
>
> **Claude:** Screening complete. Here's the ranked short list:
>
> | Rank | Manager | 5yr Net Return | AUM | Fee | Regulatory | Notes |
> |------|---------|---------------|-----|-----|------------|-------|
> | 1 | Granite Peak Capital | +12.4% vs +9.1% benchmark | $3.2B | 75bps | CLEAR | Consistent alpha, low drawdown |
> | 2 | Meridian Value Partners | +11.8% vs +9.1% benchmark | $2.1B | 80bps | CLEAR | Strong stock selection, newer team |
> | 3 | Osprey Global Advisors | +11.2% vs +9.1% benchmark | $4.7B | 85bps | FLAG | Outperformance concentrated in 2023-2024 |
>
> Osprey has a FLAG: FINRA BrokerCheck shows a customer complaint from 2022 that was settled for $180K. The complaint alleged unsuitable concentrated positions. Not an SEC enforcement action (so not an automatic disqualifier), but worth probing in the meeting.
>
> 6 managers were eliminated: 3 below AUM minimum, 2 with track records under 5 years, 1 with a management fee of 125bps. 5 managers passed criteria but ranked lower on risk-adjusted returns. Full details in the screening matrix.
>
> Want me to proceed with this short list?

#### What it produces

| File | Description |
|------|-------------|
| `workspace/<run-id>/manager-profiles.json` | Structured profile for each screened manager (follows `schemas/manager-profile.yaml`) |
| `workspace/<run-id>/screening-matrix.md` | Ranked comparison with pass/fail on each criterion and red flag summary |
| `workspace/<run-id>/screening-matrix.xlsx` | Excel version of the comparison (optional) |

#### How it connects

- **Reads from:** Fund config (`samples/configs/*.yaml`) for search criteria and data source configuration
- **Feeds into:** `/prep-manager-meeting` (CRD numbers, screening rationale), `/analyze-ddq` (manager profiles with CRD numbers for ADV cross-referencing)

---

### /prep-manager-meeting

#### What it does

Prepares everything your team needs before sitting down with a manager: a structured agenda tailored to the meeting type (on-site, annual review, DDQ follow-up, or initial), detailed talking points with context and key questions for each topic, and a one-page reference packet summarizing the manager's profile, performance, open items, and regulatory status. It pulls from prior AllocatorStack output -- DDQ gaps, ADV discrepancies, screening rationale -- so your questions are specific, not generic.

#### When to use it

You have scheduled a meeting with one of the short-listed managers. Maybe it is a first meeting after screening, a follow-up to clarify DDQ gaps, or an annual review of an existing manager. You need an agenda that reflects what you already know and focuses the conversation on what you still need to learn.

#### Example dialogue

> **You:** Prep for our on-site visit with Granite Peak Capital next Tuesday. CRD 123456.
>
> **Claude:** I found prior data for Granite Peak:
> - Screening results from run `2026-03-15`: ranked #1, all criteria PASS, regulatory CLEAR
> - DDQ extraction from run `2026-03-20`: 4 unanswered ILPA questions, 2 low-confidence extractions, 1 ADV discrepancy (employee count: DDQ says 42, ADV Item 5.A says 38)
>
> Building an on-site agenda. Since this is a first on-site, I'll focus on investment process deep-dive, team interviews, and the specific items flagged in the DDQ analysis.
>
> **Claude:** Here is the draft agenda:
>
> **1. Investment Process (45 min)**
> - Walk through a recent position: Acme Industrial -- initiated Q3 2025 at $34, now $52. What was the thesis? What would trigger a sell?
> - Discuss the team's approach to position sizing. The DDQ mentions a 5% max position, but Osprey's DDQ cited a 3% limit. Why 5%?
>
> **2. Team & Organization (30 min)**
> - The DDQ reports 42 investment professionals. The most recent ADV filing shows 38. Can they clarify the difference? (Could be timing -- ADV filed March 2025 vs. DDQ dated January 2026.)
> - Key person risk: two PMs manage 80% of AUM. What is the succession plan?
>
> **3. Open DDQ Items (20 min)**
> - ILPA Category 7 (Valuation): no answer provided. How do they value illiquid positions?
> - ILPA Category 8 (Responsible Investing): low-confidence extraction. Need verbal confirmation of their sustainability policy.
>
> Want me to adjust emphasis or add any topics?

#### What it produces

| File | Description |
|------|-------------|
| `workspace/meetings/[manager]-[date]-agenda.md` | Structured meeting agenda organized by topic |
| `workspace/meetings/[manager]-[date]-reference.md` | One-page reference packet: snapshot, performance, key findings, regulatory status |
| `workspace/meetings/[manager]-[date]-questions.md` | Detailed talking points with context, questions, and benchmarks for each topic |

#### How it connects

- **Reads from:** `/screen-managers` (screening rationale, red flags), `/analyze-ddq` (DDQ gaps, low-confidence items, ADV discrepancies), prior meeting notes
- **Feeds into:** Meeting notes that inform subsequent `/analyze-ddq` runs and `/draft-memo`

---

### /analyze-ddq

#### What it does

Ingests completed DDQ PDFs, extracts answers mapped to the 162-question ILPA/AIMA taxonomy across 9 categories, and cross-references key verifiable claims against the manager's SEC ADV filing. It checks AUM, employee count, registration status, disciplinary history, and fee schedules -- flagging discrepancies with severity ratings. The output is a structured JSON extraction with confidence scores, a completeness dashboard showing coverage by category, and a list of follow-up questions generated from gaps and discrepancies. When you feed it multiple DDQs, it produces a side-by-side comparison matrix.

#### When to use it

The short-listed managers have returned their DDQs. You need to read three 80-page PDFs, compare them systematically, verify the claims, and figure out what questions to ask next. Instead of spending two weeks on it, you run this skill and spend your time reviewing the output and investigating the flags.

#### Example dialogue

> **You:** Analyze DDQs for our three finalists. PDFs are in workspace/inputs/: granite-peak-ddq.pdf, meridian-value-ddq.pdf, osprey-global-ddq.pdf.
>
> **Claude:** Extracting text from 3 PDFs...done. Mapping to ILPA taxonomy (162 questions, 9 categories). Pulling ADV filings for cross-reference.
>
> **Claude:** Extraction complete. Here's the completeness dashboard:
>
> | Category | Granite Peak | Meridian Value | Osprey Global |
> |----------|-------------|----------------|---------------|
> | Investment Strategy (20 Qs) | 19 answered | 18 answered | 20 answered |
> | Organization & Team (22 Qs) | 20 answered | 22 answered | 19 answered |
> | Track Record (18 Qs) | 18 answered | 16 answered | 17 answered |
> | Operations (25 Qs) | 23 answered | 24 answered | 22 answered |
> | Risk Management (15 Qs) | 14 answered | 13 answered | 15 answered |
> | Fees & Terms (12 Qs) | 12 answered | 12 answered | 12 answered |
> | Legal & Compliance (18 Qs) | 17 answered | 18 answered | 16 answered |
> | Valuation (14 Qs) | 10 answered | 12 answered | 14 answered |
> | Responsible Investing (18 Qs) | 15 answered | 14 answered | 11 answered |
>
> **ADV Cross-Reference Results:**
>
> - **Granite Peak:** 4 confirmed, 1 discrepancy (employee count: DDQ 42 vs. ADV 38, severity MEDIUM), 0 unverifiable
> - **Meridian Value:** 5 confirmed, 0 discrepancies, 0 unverifiable
> - **Osprey Global:** 3 confirmed, 2 discrepancies (AUM: DDQ $5.1B vs. ADV $4.7B, severity HIGH; fee schedule: DDQ omits performance fee disclosed in ADV Part 2A, severity MEDIUM), 1 unverifiable
>
> The Osprey AUM discrepancy is 8.5%, under the 20% disqualifier threshold, but combined with the omitted performance fee this warrants probing. Generated 14 follow-up questions across the three managers.
>
> Want to review the full extraction, adjust any confidence scores, or proceed to draft the memo?

#### What it produces

| File | Description |
|------|-------------|
| `workspace/<run-id>/ddq-output.json` | Structured extraction for each manager with ILPA mappings, confidence scores, and ADV cross-reference results (follows `schemas/ddq-output.yaml`) |
| `workspace/<run-id>/completeness-dashboard.md` | Coverage summary by category with ADV cross-reference results |
| `workspace/<run-id>/comparison-matrix.md` | Side-by-side comparison across managers (when multiple DDQs are analyzed) |
| `workspace/<run-id>/follow-up-questions.md` | Questions generated from gaps, low-confidence extractions, and discrepancies |

#### How it connects

- **Reads from:** `/screen-managers` (manager profiles with CRD numbers), DDQ PDFs provided by user
- **Feeds into:** `/draft-memo` (structured extraction is the primary data source for the IC memo), `/prep-manager-meeting` (gaps and discrepancies drive meeting agendas)

---

### /draft-memo

#### What it does

Generates a first-draft Investment Committee memo from the structured data produced by the rest of the pipeline. Every quantitative claim -- every return number, AUM figure, fee calculation -- includes a provenance link back to its source (DDQ page number, ADV item, screening output). Sections requiring investment judgment are clearly marked with `[PM TO COMPLETE]` placeholders. The memo adapts to whatever data is available: full pipeline output produces a comprehensive memo; DDQ extraction alone produces a lighter version with more placeholders.

#### When to use it

The DDQs have been analyzed, the meetings have been held, and now you need to write the IC memo. The first draft is the tedious part -- pulling numbers from multiple documents, building tables, making sure every figure is sourced. This skill does that work so the PM can focus on the investment thesis and recommendation.

#### Example dialogue

> **You:** Draft the IC memo for Granite Peak Capital.
>
> **Claude:** I found the following data for Granite Peak:
> - DDQ extraction (run `2026-03-20`): 148 of 162 ILPA questions answered
> - ADV cross-reference: 4 confirmed, 1 discrepancy (employee count, MEDIUM severity)
> - Screening results (run `2026-03-15`): ranked #1, all criteria PASS
>
> Sections I can auto-populate: Track Record, Fees & Portfolio Fit, Operations Summary, Peer Comparison, ADV Cross-Reference, Risk Factors (draft). Sections that need your input: Executive Summary, Investment Thesis, Recommendation.
>
> **Claude:** Draft memo complete. Here are the highlights:
>
> **Track Record (auto-populated):**
> | Period | Granite Peak (Net) | Russell 2000 Value | Excess Return |
> |--------|-------------------|-------------------|---------------|
> | 1 Year | +14.2% | +11.8% | +2.4% |
> | 3 Year | +11.9% | +9.6% | +2.3% |
> | 5 Year | +12.4% | +9.1% | +3.3% |
>
> `[Source: granite-peak-ddq.pdf, p.14]`
>
> **ADV Cross-Reference Section:**
> - 4 of 5 key claims confirmed against SEC ADV filing
> - 1 discrepancy: employee count (DDQ: 42 `[p.8]` vs. ADV Item 5.A: 38 `[filed 03/2025]`). Likely timing difference -- ADV is 12 months older. Recommend confirming at on-site. Severity: MEDIUM.
>
> **Sections needing your input:**
> - `[PM TO COMPLETE -- Executive Summary: summarize thesis and recommendation]`
> - `[PM TO COMPLETE -- Investment Thesis: articulate why Granite Peak for this mandate]`
> - `[PM TO COMPLETE -- Recommendation: recommend / do not recommend / further DD needed]`
>
> The draft is at `workspace/2026-03-20/ic-memo-draft.md`. Ready for your edits.

#### What it produces

| File | Description |
|------|-------------|
| `workspace/<run-id>/ic-memo-draft.md` | First-draft IC memo with provenance links on every quantitative claim and `[PM TO COMPLETE]` markers on judgment sections |

#### How it connects

- **Reads from:** `/analyze-ddq` (primary data source -- DDQ extraction with ADV cross-reference), `/screen-managers` (screening rationale, peer comparison data), fund config (portfolio fit analysis), IC memo template (`templates/ic_memo.md`)
- **Feeds into:** The PM's review and the investment committee meeting. The memo is the deliverable.

---

## Monitoring

---

### /monitor-adv

#### What it does

Runs quarterly monitoring across your full manager roster. For each manager on your watchlist, it pulls the current ADV filing from SEC EDGAR, diffs it against the previous snapshot, and flags changes by severity: CRITICAL (ownership change, new disciplinary event, AUM drop over 20%, key person departure), WARNING (employee count shift over 10%, fee changes, custody changes), and INFO (address change, minor AUM fluctuation). It also scans FINRA BrokerCheck for new disciplinary history and notes which data sources it could and could not check. The output is a monitoring report where most managers show up as "clean" and the team's attention goes only to the exceptions.

#### When to use it

It is the end of the quarter. You have 35 managers on your roster and you need to confirm nothing material has changed at any of them since last quarter. Instead of manually pulling 35 ADV filings and reading each one, you run this skill and review only the flagged items.

#### Example dialogue

> **You:** Run quarterly monitoring. Watchlist is at workspace/watchlist.yaml.
>
> **Claude:** Found 35 managers on the watchlist. Pulling current ADV filings and comparing against snapshots from Q4 2025.
>
> **Claude:** Monitoring complete. Results:
>
> **CRITICAL (1 manager):**
> - **Osprey Global Advisors (CRD 789012):** AUM decreased from $4.7B to $3.6B (-23.4%). This exceeds the 20% threshold. ADV Item 5.F shows the decline. Additionally, ADV Part 2A discloses a new material conflict of interest related to affiliated broker-dealer transactions not present in the prior filing.
>   - *Recommended action:* Schedule call with Osprey. Request explanation for AUM decline and details on the new conflict disclosure.
>
> **WARNING (3 managers):**
> - **Meridian Value Partners (CRD 456789):** Employee count changed from 28 to 24 (-14.3%). ADV Item 5.A.
>   - *Recommended action:* Confirm whether departures were investment team or operations. Check if key personnel are affected.
> - **Ridgeline Fixed Income (CRD 234567):** Management fee increased from 45bps to 55bps per ADV Part 2A Item 5.
>   - *Recommended action:* Verify this applies to our fee schedule (we may have a separate agreement).
> - **Summit Equity Group (CRD 345678):** New custody arrangement disclosed.
>   - *Recommended action:* Routine -- confirm operational due diligence is current.
>
> **CLEAN: 31 managers** -- no material changes detected.
>
> **Incomplete checks:** News scan limited to SEC/FINRA public data (no market data connector configured). OFAC sanctions check unavailable (no connector). State regulatory checks not performed.
>
> Snapshots saved for next quarter. Want to review the details on any flagged manager?

#### What it produces

| File | Description |
|------|-------------|
| `workspace/monitoring-<date>/monitoring-report.md` | Flagged exceptions grouped by severity, with findings, sources, and recommended actions |
| `workspace/adv-snapshots/` | Updated filing snapshots for the next quarter's comparison |

#### How it connects

- **Reads from:** Watchlist (`workspace/watchlist.yaml`), prior ADV snapshots (`workspace/adv-snapshots/`), fund config
- **Feeds into:** `/prep-manager-meeting` (flagged items drive annual review agendas), `/board-report` (manager watch list status and activity summary)

---

## Additional Skills

---

### /screen-holdings

#### What it does

Screens the underlying holdings of your managers' portfolios (or your fund's direct positions) for two categories of risk. First, responsible investing risks: controversial weapons, forced labor indicators, deforestation, sanctions exposure, and any fund-specific exclusions mandated by your board. Second, forensic accounting red flags: revenue growth outpacing cash flow, unusual accruals, payables extensions, frequent restatements, and off-balance-sheet growth. It runs a fast screen across all holdings to narrow the list, then conducts deep research on flagged items with supply chain analysis, multi-year trend comparisons, and peer benchmarking.

#### When to use it

Your board has a responsible investing policy and you need to verify that your managers' portfolios comply. Or you are doing operational due diligence and want to check whether any holdings show signs of accounting manipulation. You run this after receiving holdings data from managers (typically as part of annual reporting or during a new manager search).

#### Example dialogue

> **You:** Screen Granite Peak's holdings against our RI policy. Holdings are in workspace/inputs/granite-peak-holdings.csv.
>
> **Claude:** Read 127 holdings from the CSV. Running fast screen against your fund's responsible investing criteria and forensic accounting indicators.
>
> **Claude:** Fast screen complete. 119 holdings CLEAR. 8 holdings flagged for deep review.
>
> Running deep research on flagged holdings...
>
> **Claude:** Results:
>
> **Responsible Investing Flags:**
> - **NovaChem Industries (2.3% of portfolio):** Subsidiary operates in jurisdiction flagged for forced labor risk. Supply chain analysis shows raw material sourcing from Xinjiang region. Risk: HIGH. Recommendation: ENGAGE.
> - **Consolidated Defense Systems (1.1%):** Manufactures components used in cluster munitions per NGO reporting. Risk: HIGH. Recommendation: EXCLUDE (triggers board exclusion policy).
>
> **Forensic Accounting Flags:**
> - **Rapid Growth Technologies (3.8%):** Revenue grew 34% YoY while operating cash flow declined 12%. Receivables up 58%. This divergence is an outlier vs. sector peers (median receivables growth: 11%). Two analyst downgrades in the past quarter cite "revenue quality concerns." Risk: HIGH. Recommendation: MONITOR.
> - **Pacific Logistics Corp (1.5%):** Auditor changed twice in 3 years. Payables extended from 45 to 78 days while reporting stable margins. Risk: MEDIUM. Recommendation: MONITOR.
>
> **Portfolio-Level Summary:**
> - Total exposure to HIGH-risk holdings: 7.2% of portfolio
> - 1 holding triggers your board's exclusion policy (Consolidated Defense Systems)
> - Granite Peak has higher concentration in flagged holdings than Meridian Value (7.2% vs. 2.1%)
>
> Do you want me to dig deeper on any holding, or include these findings in the IC memo?

#### What it produces

| File | Description |
|------|-------------|
| `workspace/holdings-screen.json` | Structured screening results with risk scores, evidence, and recommendations |
| `workspace/holdings-screen-summary.md` | Human-readable summary with portfolio-level risk exposure |
| `workspace/holdings-flagged.md` | Detailed findings and evidence for each flagged holding |

#### How it connects

- **Reads from:** Holdings data (user-provided CSV/Excel or extracted from DDQs), fund config (responsible investing policy, exclusion lists)
- **Feeds into:** `/draft-memo` (RI findings inform risk factors section), `/board-report` (responsible investing summary), `/prep-company-meeting` (engagement topics for flagged companies)

---

### /prep-company-meeting

#### What it does

Prepares briefing packets for direct meetings with portfolio companies -- public equity positions, private equity co-investments, real estate, infrastructure, or companies flagged for responsible investing engagement. It researches the company across financial, governance, and sustainability dimensions, builds a structured agenda tailored to the meeting context (engagement, annual meeting, board seat, co-investment DD, or monitoring), and produces talking points that connect the fund's investment thesis to specific questions. It includes a governance scorecard, financial trend analysis, and prior engagement history.

#### When to use it

You hold a direct equity position and the company's annual meeting is next month -- you need to decide how to vote on the proxy and what to raise in the meeting. Or your responsible investing team has flagged a portfolio company for engagement on labor practices and you need a structured approach. Or you are evaluating a co-investment alongside a GP and need to prepare for management meetings.

#### Example dialogue

> **You:** Prep for our engagement meeting with NovaChem Industries. We're raising the Xinjiang supply chain issue flagged by /screen-holdings.
>
> **Claude:** I found prior context:
> - Holdings screening flagged NovaChem for forced labor risk in supply chain (HIGH severity)
> - Fund holds 0.4% of outstanding shares ($12M position, initiated Q2 2024)
> - No prior engagement meetings on record
>
> Building an engagement agenda focused on supply chain transparency.
>
> **Claude:** Agenda ready:
>
> **1. Supply Chain Transparency (30 min)**
> - Context: NGO reports identify raw material sourcing from Xinjiang region. NovaChem's 2025 10-K discloses "diverse global sourcing" but does not address region-specific risks.
> - Key question: Can NovaChem provide a supplier audit covering the flagged facilities?
> - Benchmark: 3 of 5 sector peers have published independent supply chain audits. NovaChem has not.
> - Engagement leverage: We co-filed a shareholder proposal with two other institutional holders requesting supply chain disclosure.
>
> **2. Remediation Timeline (15 min)**
> - What specific steps is NovaChem taking? By when?
> - What does the company consider adequate evidence of compliance?
>
> **3. Escalation Path (10 min)**
> - If NovaChem does not provide adequate disclosure by Q4 2026, our options: vote against board directors, support additional shareholder proposals, or recommend divestment to the IC.
>
> Briefing packet includes: company snapshot, 3-year financial trends, governance scorecard (board independence: 67%, below sector median of 78%), and key personnel bios for the meeting participants.

#### What it produces

| File | Description |
|------|-------------|
| `workspace/company-meetings/[company]-[date]-agenda.md` | Structured meeting agenda tailored to context |
| `workspace/company-meetings/[company]-[date]-briefing.md` | Briefing packet with financials, governance scorecard, prior engagement history |
| `workspace/company-meetings/[company]-[date]-questions.md` | Talking points with context, questions, benchmarks, and engagement leverage |

#### How it connects

- **Reads from:** `/screen-holdings` (responsible investing flags drive engagement topics), fund position data, prior meeting notes, public filings
- **Feeds into:** Meeting notes that inform future `/screen-holdings` runs and `/board-report` (engagement activity summary)

---

### /board-report

#### What it does

Generates a board-ready investment report that serves two audiences in the same document. The technical sections give the investment committee what they need: performance attribution, manager-level returns vs. benchmarks with quartile rankings, risk metrics, watch list status, and activity summaries. The trustee summary translates all of that into plain language that a non-investment-professional board member can read and act on -- no jargon, clear explanations of what matters and what decisions the board needs to make. It includes compliance attestations, policy deviation analysis, and responsible investing summaries when holdings screening data is available.

#### When to use it

The quarterly board meeting is in two weeks. You need to produce the board book. The data is scattered across performance reports, manager updates, compliance logs, and the responsible investing team's engagement tracker. This skill pulls it together into a consistent format, with the trustee summary up front so board members who are not investment professionals can engage meaningfully.

#### Example dialogue

> **You:** Generate the Q1 2026 board report. Portfolio data is in workspace/inputs/q1-portfolio.csv. Manager performance is in workspace/inputs/q1-manager-returns.csv.
>
> **Claude:** I found additional data from prior AllocatorStack runs:
> - Monitoring report from `workspace/monitoring-2026-03-28/`: 1 CRITICAL flag (Osprey AUM decline), 3 WARNINGs
> - Holdings screening from `workspace/holdings-screen.json`: 1 exclusion policy trigger, 3 holdings on MONITOR
> - Manager search activity: US small cap value search in progress (3 finalists, IC memo drafted for Granite Peak)
>
> Building the report. I can auto-populate: portfolio overview, manager performance tables, risk metrics, activity summary, monitoring exceptions, responsible investing summary. Sections needing CIO input: forward-looking commentary, recommendation on Osprey watch list status.
>
> **Claude:** Report drafted. Highlights from the trustee summary:
>
> *"The fund returned 2.1% in Q1 2026, slightly ahead of the 1.9% policy benchmark. The portfolio is within all policy allocation ranges. One manager, Osprey Global Advisors, experienced a significant decline in assets under management and has been placed on the watch list for enhanced monitoring. The investment team is conducting a search for a new US small cap value manager and expects to present a recommendation at the June meeting. One portfolio holding was found to conflict with the fund's responsible investing exclusion policy and has been flagged for the board's review."*
>
> The full report runs 18 pages. The trustee summary is 3 pages. Excel supplement includes all performance data tables.
>
> Sections needing your input:
> - `[CIO TO COMPLETE -- Forward-looking commentary and market outlook]`
> - `[CIO TO COMPLETE -- Recommendation on Osprey: maintain, terminate, or enhanced monitoring]`

#### What it produces

| File | Description |
|------|-------------|
| `workspace/board-reports/[period]-board-report.md` | Full board report with technical IC sections and compliance attestations |
| `workspace/board-reports/[period]-trustee-summary.md` | Standalone 2-3 page plain-language summary for non-investment board members |
| `workspace/board-reports/[period]-supplement.xlsx` | Excel data supplement with performance tables (optional) |

#### How it connects

- **Reads from:** `/monitor-adv` (manager watch list and monitoring exceptions), `/screen-holdings` (responsible investing summary), `/screen-managers` (search activity), fund config (policy targets, risk limits), portfolio and performance data (user-provided)
- **Feeds into:** The board meeting. This is the end-of-pipeline deliverable for the quarterly reporting cycle.

---

## How the Skills Connect

```
                        ┌──────────────────┐
                        │  /screen-managers │
                        │  (ranked short    │
                        │   list)           │
                        └────────┬─────────┘
                                 │
                    ┌────────────┼────────────┐
                    ▼            ▼             │
          ┌─────────────┐ ┌───────────┐       │
          │ /prep-manager│ │/analyze-  │       │
          │  -meeting    │ │ ddq       │       │
          │ (agenda,     │ │(extraction│       │
          │  questions)  │ │ + ADV     │       │
          └──────────────┘ │ cross-ref)│       │
                           └─────┬─────┘       │
                                 │             │
                                 ▼             │
                        ┌────────────────┐     │
                        │  /draft-memo   │◄────┘
                        │  (IC memo with │
                        │   provenance)  │
                        └────────────────┘

  ┌──────────────┐    ┌──────────────────┐    ┌──────────────┐
  │/monitor-adv  │───►│  /board-report   │◄───│/screen-      │
  │(quarterly    │    │  (board book)    │    │ holdings     │
  │ exceptions)  │    └──────────────────┘    │(RI + forensic│
  └──────────────┘                            │ flags)       │
                                              └──────┬───────┘
                      ┌──────────────────┐           │
                      │/prep-company-    │◄──────────┘
                      │ meeting          │
                      │(engagement       │
                      │ briefing)        │
                      └──────────────────┘
```

The core pipeline flows top-to-bottom: screen, meet, analyze, memo. The monitoring and holdings skills run on their own cadence (quarterly) and feed into the board report. Company meeting prep draws from holdings screening when the meeting is about responsible investing engagement. Every skill reads from and writes to the shared `workspace/` directory, passing structured JSON between stages.
