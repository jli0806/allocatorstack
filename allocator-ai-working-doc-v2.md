# ALLOCATOR AI

## An Open-Source Framework for AI Agents in Institutional Asset Allocation

**Working Document: Project Foundation & Workflow Analysis**

How public pension funds, endowments, and foundations run their front offices today, where leading allocators are deploying AI, and where agents can do real work.

*Draft v0.2 · March 2026*  
*Joyce Li* 

---

## 1. What This Document Is

This is the foundation document for an open-source project called Allocator AI. The project has two deliverables: a white paper explaining how asset owners can use AI agents in their front-office operations, and a GitHub repository implementing working prototypes of those agents.

This document serves a specific purpose. It maps the operational reality of how public pension funds, endowments, and foundations actually run their investment front offices today. It traces four real workflows from start to finish, identifies where each workflow breaks down or consumes disproportionate staff time, and specifies where an AI agent could do useful work at each step. It also documents how several leading allocators are already deploying AI in production, drawing on their own public disclosures.

The intended readers are two groups: investment professionals at asset owners who want to evaluate whether this framework addresses their actual problems, and developers who want to understand the domain well enough to build agents that produce outputs a CIO would trust.

### 1.1 What We Are Building

A modular, open-source Python framework where each module maps to a real front-office function. Users bring their own data sources (Bloomberg, eVestment, Preqin, custodian feeds, or CSV exports). The framework provides the agent logic, workflow orchestration, and output templates.

The first release covers four front-office workflows at medium depth, with the manager due diligence workflow receiving the most detailed treatment. Each workflow includes working code that runs against sample data, producing outputs in formats that mirror what investment staff actually create (memos, comparison tables, scenario reports, board summaries).

### 1.2 Who This Is For

- **Public pension funds.** Typically $50B-$500B+ AUM, 100-400 investment staff, heavy reliance on external managers, governed by boards of trustees, long strategic asset allocation cycles.
- **University endowments.** $1B+ AUM. Lean teams of 5-30 investment professionals, high allocation to alternatives, managed through investment companies or internal offices.
- **Private foundations.** $500M+ AUM. Similar to endowments in team size and allocation, with the additional constraint of 5% mandatory annual distribution under IRC Section 4942.

### 1.3 What We Are Not Building

- A trading system. Allocators are not traders. They select and oversee external managers who trade.
- A portfolio management system to replace Aladdin, FactSet, or Bloomberg PORT. Those are enterprise platforms with decades of integration.
- A robo-advisor or automated decision-maker. Every consequential investment decision at a public pension fund goes through a human committee with fiduciary responsibility.
- A data vendor. The framework connects to data sources. It does not provide proprietary data.

---

## 2. How the Allocator Front Office Actually Works

Understanding the operational reality is essential before designing agents. The front office at a public pension fund or endowment is structured around a small number of high-stakes decisions made slowly and deliberately, supported by a large volume of data gathering, document creation, and analysis that consumes most of the staff's time.

### 2.1 Organizational Structure

A public pension fund's investment division typically organizes into the following layers:

**Board of Trustees / Investment Board**

Sets the assumed rate of return (typically 6.5-7.5%), approves the strategic asset allocation, and delegates implementation authority to the CIO within defined ranges. Meets monthly or quarterly. Members are elected, appointed, or serve ex officio. Board size ranges widely, from as few as 3 trustees to 13 or more, depending on the fund's enabling legislation. The board is the ultimate fiduciary.

**CIO and Senior Investment Leadership**

The CIO oversees all investment activity, manages the senior team, and represents the fund externally. A Deputy CIO or Managing Director for each major asset class reports to the CIO. A Total Fund Portfolio Management team handles asset allocation implementation, rebalancing, and overlay strategies. A large public pension fund ($200B+ AUM) typically employs 200-400 investment professionals, with investment operations budgets running $150-$200M annually alongside $1-2B in external management fees.

**Asset Class Teams**

Each team (public equity, fixed income, private equity, real assets, credit, sustainable investing) has a Managing Director, Portfolio Managers, Senior Investment Officers, and Analysts. Their core functions: sourcing and evaluating external managers, monitoring existing manager performance, recommending allocation changes within their asset class, and preparing investment memos for the internal investment committee.

**Internal Investment Committee**

Approves individual manager hires, terminations, and commitment increases above a delegation threshold. At most public pension funds, the CIO can approve allocations up to a certain dollar amount (e.g., $500M) without full board approval. The IC meets frequently, sometimes weekly for deal-heavy periods in private markets.

### 2.2 How Endowments Differ

The most important structural difference is staffing. The average endowment above $1B has roughly 9 full-time investment employees including the CIO, per NACUBO data. Even the largest university endowments, managing $40-$60B+, operate with fewer than 30-70 total staff. This lean staffing model creates an acute version of the same problems public pension funds face: too much data to process, too few people to process it.

Endowments also allocate differently. Those above $5B hold only about 8% in U.S. public equities versus over 40% for those under $50M. The largest endowments hold 15-20% in private equity and 10-15% in venture capital. This heavy alternatives weighting means endowment staff spend proportionally more time on manager sourcing and due diligence in opaque asset classes where data is sparse, documents are long, and evaluation is qualitative.

The governance chain is shorter. An endowment CIO typically reports to an investment committee of the university board, with fewer layers of approval than a public pension fund. Decision-making can be faster, but documentation expectations remain high because of fiduciary obligations.

### 2.3 The Data Environment

Allocator front offices operate in a fragmented data environment. There is no single system of record. Data arrives from multiple sources in different formats, on different schedules, with different levels of reliability.


| Data Source                                   | What It Provides                                                                                                                | Update Frequency              | Format / Access                                                            |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- | -------------------------------------------------------------------------- |
| Bloomberg Terminal                            | Market data, analytics, news                                                                                                    | Real-time                     | Terminal + API (BQL). Per-seat licensing.                                  |
| eVestment                                     | Qualitative and quantitative information on managers: returns, AUM, strategy descriptions, style analytics, organizational data | Monthly (lagged 30-60 days)   | Web portal + data exports. Subscription.                                   |
| Preqin / PitchBook                            | PE/VC fund data, fundraising, deals, performance                                                                                | Quarterly (lagged 60-90 days) | Web portal + API. Subscription.                                            |
| Burgiss / Cambridge Associates                | Private markets benchmarks, cash flows, peer comparisons                                                                        | Quarterly (lagged 90+ days)   | Client portal. Consulting relationship.                                    |
| Custodian (BNY, State Street, Northern Trust) | Holdings, transactions, NAVs, cash positions                                                                                    | Daily (T+1 or T+2)            | SFTP flat files, portal, API. Custody contract.                            |
| External Managers                             | Monthly/quarterly reports, capital call notices, K-1s, DDQs                                                                     | Monthly or quarterly          | Email attachments, investor portals (200+ portals for a large fund), PDFs. |
| Aladdin / FactSet / Bloomberg PORT            | Portfolio analytics, risk decomposition, attribution                                                                            | Daily                         | Enterprise platform. Multi-year contract.                                  |


A typical allocator workflow for evaluating external managers combines two of these sources in sequence. The fund has access to a database like eVestment, which contains both qualitative and quantitative information on managers, including strategy descriptions, organizational data, AUM, and performance history. After identifying candidates through the database, the fund sends managers its own due diligence questionnaires (DDQs) to gather additional detail that the database does not cover, such as specific portfolio construction rules, risk limits, key person provisions, and compliance history. This two-step pattern (database screening followed by DDQ) is the backbone of the manager sourcing workflow described in Section 3.

> **Key pain point:** A public pension fund with 150 external managers might need to log into 80+ investor portals to collect quarterly reports. Each report arrives in a different PDF format. Aggregating this data into a consistent view of the total portfolio takes days of manual work every quarter.

### 2.4 The Time Budget Problem

Investment professionals at allocators spend the majority of their time on data gathering, document creation, and process administration. A rough breakdown of how a senior investment officer's time splits:


| Activity                                | % of Time | Nature of Work                                           |
| --------------------------------------- | --------- | -------------------------------------------------------- |
| Data collection and reconciliation      | 25-30%    | Pulling reports, normalizing data, building spreadsheets |
| Document review and analysis            | 20-25%    | Reading DDQs, PPMs, quarterly letters, legal docs        |
| Memo writing and reporting              | 15-20%    | IC memos, board reports, performance summaries           |
| Meetings (internal + external managers) | 15-20%    | IC meetings, manager meetings, team meetings, board prep |
| Judgment and decision-making            | 10-15%    | Evaluating managers, forming views, debating allocation  |


> **The ratio is striking:** roughly 60-75% of an investment professional's time goes to data handling and document production. Only 10-15% goes to the judgment work that justifies their compensation and expertise. This is the core problem the framework addresses.

---

## 3. Four Front-Office Workflows, Mapped End to End

Each workflow below follows the same structure: what triggers it, who is involved, what steps happen in sequence, what data and documents flow through each step, how long it takes, and where agents can do useful work. The manager due diligence workflow receives the deepest treatment because it involves the most document-heavy, time-intensive work that is well-suited to agent automation.

### 3.1 Workflow 1: Manager Due Diligence (Sourcing to IC Approval)

This is the most labor-intensive front-office workflow. From initial sourcing to investment committee approval, a single manager hire typically takes 3-6 months at a public pension fund and 2-4 months at a well-staffed endowment. The elapsed time is driven less by the complexity of any single step than by the sheer volume of documents to read, data to gather, and comparisons to build.

#### Step 1: Opportunity Identification

**Trigger:** An asset class team identifies a gap in the portfolio. This might come from a strategic asset allocation review (e.g., the board increased the target allocation to real assets by 3%), a manager termination (underperformance, key-person departure, style drift), or an opportunistic pitch from a manager or placement agent.

**Who:** Portfolio Manager or Senior Investment Officer on the relevant asset class team.

**Current process:** The PM defines a search mandate: asset class, strategy type, return target, risk budget, geographic focus, AUM range, track record length, any sustainability or governance requirements. They log into a manager database like eVestment (for public markets) or Preqin/PitchBook (for private markets). These databases contain both qualitative information (strategy descriptions, team bios, investment philosophy, organizational structure) and quantitative data (returns, AUM, risk metrics, style analytics). The PM sets filters and exports a universe of 50-200 potential managers. They also draw on their personal network, conference contacts, and placement agent relationships.

**Time:** 1-2 weeks.

**Output:** A long list of 15-40 candidates with basic data (firm name, strategy, AUM, headline returns, inception date).

**Pain point:** The screening criteria live in the PM's head and in the investment policy statement, but connecting the IPS constraints to the database filters requires manual translation. The PM also needs to check whether the fund has looked at any of these managers before, which means searching old memos, emails, and CRM notes. There is no institutional memory system that connects past evaluations to current searches.

> **Agent opportunity:** A Manager Sourcing Agent could take a natural-language search mandate ("Find US small-cap value managers with 5+ year track records, AUM between $1B and $10B, top-quartile vs. Russell 2000 Value over trailing 3 and 5 years, no SEC enforcement actions"), query the database through its API, cross-reference against the fund's own records of past evaluations, and produce a ranked long list with the screening criteria documented. Estimated time savings: from 1-2 weeks to 1-2 days.

#### Step 2: Preliminary Screening

**Current process:** The PM narrows the long list to 8-12 candidates through a combination of quantitative screening (returns, risk-adjusted metrics, drawdown analysis, peer ranking) and qualitative filtering (team stability, organizational reputation, strategy capacity). They request pitch books from the shortlisted managers and review them. Each pitch book is 30-60 pages. The PM reads 8-12 of them.

**Time:** 2-3 weeks.

**Output:** A short list of 4-6 managers to advance to full due diligence, with a brief rationale for each. A comparison spreadsheet with normalized performance data.

**Pain point:** Normalizing data across managers is tedious. Managers report returns on different bases (gross vs. net, different fee structures, different benchmark periods). AUM figures may be as-of different dates. Building a true apples-to-apples comparison table requires manual adjustment. Pitch books emphasize different metrics depending on what makes the manager look best, so extracting comparable data from 8-12 different document formats is slow work.

> **Agent opportunity:** A Screening Agent could ingest the pitch books (PDFs), extract key quantitative data into a standardized schema, normalize returns to a common basis (net of a standard fee assumption, same time periods, same benchmarks), and produce a comparison matrix. It could also flag discrepancies between manager-reported data and database data. Estimated time savings: from 2-3 weeks to 3-5 days.

#### Step 3: Full Investment Due Diligence

**Current process:** This is the most document-intensive step. The PM sends each shortlisted manager the fund's DDQ (Due Diligence Questionnaire). Industry-standard DDQ templates from ILPA and AIMA run approximately 200 questions covering: investment strategy and process, organization and team, track record and attribution, fund terms and fees, risk management, compliance and regulatory, responsible investing, and IT and cybersecurity.

The manager returns a completed DDQ (typically 40-80 pages), along with supplementary materials: audited financials, sample portfolio reports, compliance manual excerpts, biographies of key personnel, references. The PM reads each DDQ cover to cover, cross-references claims against third-party data, and prepares a detailed evaluation. For private markets, this also includes reviewing the LPA (Limited Partnership Agreement) and side letter terms.

This step is where the database and the DDQ play complementary roles. The database (eVestment, Preqin) provides standardized, comparable data across the full manager universe. The DDQ goes deeper into areas the database cannot capture: how the manager actually constructs portfolios, what their risk limits are in practice, how they handled specific drawdowns, what their succession plan looks like, how their compliance program works day to day. The PM needs both sources to form a complete picture.

**On-site visits:** For managers advancing past DDQ review, the team conducts in-person meetings at the manager's office. A typical on-site visit involves 4-6 hours of meetings with the PM, analyst team, traders, operations, compliance, and the CEO/CIO. The team prepares specific questions in advance based on DDQ analysis.

**Reference checks:** The PM contacts 3-5 references provided by the manager, and ideally 2-3 back-channel references (other LPs, former employees, industry contacts) that the manager did not provide.

**Time:** 4-8 weeks per manager. With 4-6 managers on the short list, this step often runs in parallel but still takes 6-10 weeks total.

**Output:** A detailed DD evaluation for each manager. A recommendation to advance 1-2 finalists to the investment committee.

**Pain points:** Reading 4-6 DDQs of 40-80 pages each takes 20-30 hours of focused reading time. Cross-referencing DDQ claims against public data (ADV filings, SEC enforcement database, litigation searches, news) is another 3-5 hours per manager. Comparing how different managers answered the same questions requires flipping between documents. There is no structured way to see, at a glance, how Manager A's risk management approach compares to Manager B's.

> **Agent opportunity:** A DDQ Analysis Agent could ingest completed DDQs, extract answers into a structured database organized by question category, produce side-by-side comparison views, cross-reference key claims against public data (SEC EDGAR for ADV filings, FINRA BrokerCheck, court records), and flag areas requiring follow-up questions. For the on-site visit, the agent could generate a tailored question list based on gaps, inconsistencies, or unusual answers in the DDQ. Estimated time savings: from 20-30 hours of reading per manager to 3-4 hours of review per manager.

#### Step 4: Operational Due Diligence

**Current process:** Runs in parallel with investment DD but is typically handled by a separate team (Operations, Risk, or a dedicated ODD function). Covers: valuation policies, trade execution and allocation, cash management, business continuity, insurance coverage, regulatory compliance history, cybersecurity posture, and conflicts of interest. At larger public pension funds, the ODD team has its own questionnaire (distinct from the investment DDQ).

**Time:** 3-6 weeks, running concurrently with investment DD.

**Output:** An ODD report with a recommendation (proceed, proceed with conditions, or reject).

#### Step 5: Investment Committee Memo and Approval

**Current process:** The PM drafts an investment committee memo. At a public pension fund, this is a formal document, typically 10-25 pages, following a standard template: executive summary and recommendation, strategy overview, investment thesis, track record analysis with attribution, team assessment, fee analysis and terms comparison, risk factors and mitigants, operational DD summary, portfolio fit analysis (how the new manager fits within the overall asset class allocation and total fund), and a comparison to existing managers in the same sleeve.

The memo goes through internal review (team lead, Deputy CIO, legal, compliance) before the IC meeting. The IC discussion lasts 30-60 minutes per manager. The committee votes to approve, reject, or request additional information.

**Time:** Memo drafting takes 2-4 days of concentrated work. Internal review and revision adds 1-2 weeks. The IC meeting itself is scheduled monthly or as-needed.

**Output:** Approved IC memo with committee vote. If approved, handoff to legal for contract negotiation (IMA or LPA subscription).

**Pain point:** The memo is assembled from data scattered across 5-10 sources: the DDQ, the manager's pitch book, database data, the fund's own portfolio analytics, the ODD report, reference check notes, and the PM's own analysis. Pulling this together into a coherent narrative with consistent data is the most time-consuming document creation task in the front office.

> **Agent opportunity:** An IC Memo Agent could generate a first draft from structured inputs: the DDQ analysis output, screening comparison data, reference check notes, and ODD summary. The agent would populate all quantitative sections (performance tables, fee comparisons, portfolio fit analysis) from data and leave qualitative assessment sections (investment thesis, risk judgment) clearly marked for the PM to write. This separates data assembly from judgment, which is exactly how the work should split between agent and human. Estimated time savings: from 2-4 days to 4-8 hours of drafting time, with the PM focused on narrative and judgment rather than data formatting.

#### Total Workflow Summary: Manager Due Diligence


| Step                   | Current Time   | With Agents    | Savings  | Agent Role           |
| ---------------------- | -------------- | -------------- | -------- | -------------------- |
| 1. Opportunity ID      | 1-2 weeks      | 1-2 days       | ~80%     | Sourcing Agent       |
| 2. Preliminary Screen  | 2-3 weeks      | 3-5 days       | ~65%     | Screening Agent      |
| 3. Full DD             | 6-10 weeks     | 3-5 weeks      | ~50%     | DDQ Analysis Agent   |
| 4. ODD                 | 3-6 weeks      | 2-4 weeks      | ~35%     | ODD Extraction Agent |
| 5. IC Memo + Approval  | 3-4 weeks      | 1-2 weeks      | ~55%     | IC Memo Agent        |
| **Total Elapsed Time** | **3-6 months** | **6-12 weeks** | **~50%** |                      |


### 3.2 Workflow 2: Strategic Asset Allocation Review

The strategic asset allocation (SAA) defines the fund's target allocation to each asset class. It is the single most important investment decision a public pension fund or endowment makes, responsible for 80-90% of long-term return variation. SAA reviews occur on multi-year cycles: every 3-5 years at most public pension funds, and annually at many endowments.

#### How It Works Today

**Step 1: Capital Market Assumptions (CMAs).** The fund's investment consultant (Mercer, Aon, Callan, Cambridge Associates, Meketa) or internal team develops forward-looking return, risk, and correlation estimates for every asset class. These are typically 10-year or 20-year projections. Most funds receive CMAs from 2-3 sources and form a blended view. Time: 4-8 weeks.

**Step 2: Liability Modeling.** For public pension funds, the actuary provides a model of future benefit payments based on current demographics, mortality tables, salary growth assumptions, and plan provisions. The SAA must generate returns sufficient to meet these liabilities at the assumed discount rate. Endowments substitute a spending rule (typically 4-5% of a trailing average market value) for the liability stream. Time: concurrent with CMAs.

**Step 3: Optimization and Scenario Analysis.** The consultant runs mean-variance optimization (often with Black-Litterman adjustments) to generate an efficient frontier of candidate portfolios. The team then runs scenario analysis: how does each candidate portfolio perform in a 2008-type drawdown, a stagflation scenario, a sustained low-rate environment, a rapid rate-rise scenario? Time: 4-6 weeks.

**Step 4: Board Education and Deliberation.** The CIO presents the analysis to the board, typically over 2-3 board meetings. Board members are often not investment professionals (elected officials, union representatives, public members). The materials must explain complex tradeoffs in accessible language. Time: 2-4 months including meeting scheduling.

**Step 5: Approval and Implementation Plan.** The board votes on the new SAA. Staff develops a multi-year transition plan, because moving from the current allocation to the new target (especially in private markets) takes 3-5 years of adjusted commitment pacing. Time: ongoing.

#### Where Agents Fit

- **CMA Synthesis Agent.** Collects CMAs from multiple consultants and published sources, normalizes them to consistent asset class definitions and time horizons, and produces a comparison matrix showing where assumptions agree and diverge. Today this is a multi-week spreadsheet exercise.
- **Scenario Modeling Agent.** Takes a candidate portfolio and runs it through historical stress periods and forward-looking scenarios defined in natural language. Produces visualizations of funded status impact, drawdown paths, and recovery timelines. Connects to the fund's actual liability model through the BYOD interface.
- **Board Communication Agent.** Transforms technical SAA analysis into plain-language board materials. Generates executive summaries, annotated charts, and FAQ documents anticipating trustee questions.

### 3.3 Workflow 3: Ongoing Manager Monitoring and Watchlist

After a manager is hired, the front office monitors their performance, organizational stability, and adherence to the investment mandate on an ongoing basis. This is a continuous workflow, but it peaks around quarterly reporting cycles.

#### How It Works Today

**Quarterly cycle (weeks 1-3 after quarter-end):** Managers submit quarterly reports. For a fund with 150 external managers, this means 150 separate documents arriving over 2-3 weeks, each in a different format. Staff extract key data: returns (gross and net), attribution, portfolio characteristics, organizational changes, any compliance exceptions, capital calls and distributions (for private markets).

**Performance review:** Each manager is evaluated against their benchmark, peer group, and the fund's expected return for that mandate. Underperformance triggers a structured review: is it style-related (the manager's factor exposures are out of favor), stock-specific (bad picks in an otherwise sound process), or structural (the process itself is broken)? Persistent underperformance (typically 3+ years below benchmark) moves a manager to a formal watchlist.

**Watchlist management:** Managers on the watchlist receive enhanced monitoring: more frequent calls, additional data requests, and a formal review timeline. The PM prepares a watchlist memo for the IC every quarter.

**Organizational monitoring:** Between quarters, staff track news about their managers: key person departures, regulatory actions, M&A activity, fund flow trends, and any public controversy. This is largely an ad-hoc process relying on news alerts and industry contacts.

#### Where Agents Fit

- **Report Ingestion Agent.** Collects quarterly reports from investor portals and email, extracts key data points into a standardized schema, and flags missing or late submissions.
- **Performance Attribution Agent.** Calculates and decomposes manager returns into factor exposures, stock selection, and timing effects. Compares current-quarter results against the manager's own historical pattern to detect style drift.
- **Watchlist Intelligence Agent.** Monitors news, regulatory filings, and LinkedIn (for key person departures) for all active managers. Generates alerts when material events occur.

### 3.4 Workflow 4: Board and Stakeholder Reporting

Public pension funds face transparency requirements that endowments and foundations generally do not. Board meetings are often public. Investment reports are published on the fund's website. Legislative committees request testimony and data. This creates a significant reporting burden on the investment team.

#### How It Works Today

**Monthly/quarterly board report:** The investment team produces a comprehensive report covering: total fund performance (1-month, QTD, YTD, 1/3/5/10-year), performance by asset class, attribution analysis, risk metrics (VaR, tracking error, concentration), private markets activity (commitments, capital calls, distributions, NAV changes), compliance status (are all allocations within policy ranges?), and market commentary.

**The report audience problem:** Board members range from finance professionals to elected officials with no investment background. The report must be both technically rigorous and accessible. This dual-audience requirement makes the report harder to write than a purely technical document.

**Time:** 3-5 business days to compile data, create charts, write commentary, and go through internal review. For a fund that reports monthly, this is a recurring burden.

#### Where Agents Fit

- **Report Generation Agent.** Pulls performance data from the portfolio management system, private markets data from internal tracking, and market data from Bloomberg. Generates the standard sections of the board report automatically. Leaves market commentary and forward-looking sections for staff.
- **Plain-Language Translation Agent.** Takes technical sections (risk decomposition, factor attribution) and generates summaries suitable for non-specialist trustees.
- **Historical Context Agent.** For any metric in the current report, retrieves the same metric from prior periods and annotates changes with explanatory context.

---

## 4. How Leading Allocators Are Using AI Today

The workflows described in Section 3 represent the current operational norm at most public pension funds and endowments. But a handful of large allocators have moved meaningfully ahead, deploying AI in production settings and publishing detailed accounts of what worked, what failed, and what they learned. Their experiences provide both validation for the framework's design and practical lessons about implementation.

This section draws exclusively on public disclosures from the allocators themselves, published in their own reports, board documents, and attributed statements to institutional investment media.

### 4.1 NBIM (Norges Bank Investment Management)

Norway's Government Pension Fund Global, managed by NBIM, is the world's largest sovereign wealth fund at approximately $2.2 trillion. It holds stakes in roughly 7,200 companies across 60 countries. NBIM has been the most publicly aggressive about AI adoption among institutional allocators.

**What they deployed:** Since 2025, NBIM has used large language models to screen every company on its first day of entering the equity portfolio. According to their February 2026 responsible investment report, the AI scans public information that goes beyond what traditional data vendors typically cover. Where risks emerge around key themes, the model conducts deeper searches and provides contextual summaries. Within 24 hours of a new investment, the AI flags companies with potential links to issues like forced labor, corruption, or fraud.

*Source: CNBC, February 26, 2026; NBIM Responsible Investment Report 2025; NordSIP, March 20, 2026.*

**Behavioral analytics:** NBIM also developed an internal "Investment Simulator" that monitors portfolio manager behavior. It produces behavioral scorecards tracking trading habits and biases, giving PMs feedback to support more rational, data-driven decisions.

*Source: Top1000funds, October 2025; Investment Magazine Australia, June 2025.*

**Organizational commitment:** NBIM's CEO Nicolai Tangen declared the fund is "all-in on AI" in its Strategy 2028 document. Approximately half of the fund's 700 employees actively code their own AI tools. Tangen told Norway's parliament that tasks that previously took days now take minutes. The fund invested millions of crowns in AI infrastructure and reports that the benefits have already reached the billions. Despite this, the fund does not plan to reduce headcount; roles are shifting from administrative tasks toward front-end investment and strategic analysis.

*Source: IPE, January 2026; Chief Investment Officer (ai-cio.com), 2025; dbbnwa.com, March 2026.*

> **Relevance to this project:** NBIM's day-one screening workflow is a production implementation of the Sourcing Agent concept from Section 3.1, applied at the holding level rather than the manager level. Their behavioral analytics tool demonstrates an application of AI that most allocators have not considered: using AI not to replace human judgment but to improve it by making cognitive biases visible.

### 4.2 CPP Investments

Canada's public pension fund manager (C$777.5 billion, approximately $562 billion USD) has published the most detailed and transparent account of AI experimentation among institutional allocators. Their Insight Institute has released multiple papers describing specific experiments, metrics, and lessons.

**Deployment at scale:** CPP Investments deployed ChatGPT Enterprise to roughly 1,800 eligible employees and reached an 83% activation rate within 90 days, surpassing the 75% industry average for financial services firms. 84.3% of users maintained weekly active usage throughout that period. They also obtained more than 2,100 licenses for Microsoft Copilot.

*Source: CPP Investments Insight Institute, October 2025 and November 2024.*

**Head-to-head agent trials:** In January 2026, CPP published results from trials comparing autonomous multi-agent AI systems against traditional workflows on three real investment tasks. First, reconciling a $522 million portfolio that contained hidden errors. Second, conducting performance attribution. Third, analyzing a forward-looking tariff scenario. The multi-agent systems used a self-organizing structure with verification gates. The COO's published assessment: the AI did not merely accelerate existing workflows; for the first two tasks, it rendered the traditional approaches obsolete.

*Source: Top1000funds, January 15, 2026; CPP Investments Insight Institute, November 2025.*

**Three-pattern framework:** CPP organized their AI deployment around three patterns based on task characteristics. "AI Excels" for clear, rules-based tasks where AI can operate with high autonomy. "AI Executes" for heavy quantitative work requiring human oversight. "AI Explores" for ambiguous problems where human judgment drives the value. Each investment capability was mapped to one of these patterns, which then determined how the system was configured.

*Source: CPP Investments Insight Institute, "Rethinking Work," November 2025.*

**Five-gate verification model:** CPP found that verification infrastructure matters more than sophisticated orchestration. They built a five-gate verification system with confidence thresholds at each stage. The tariff scenario analysis revealed why this matters: without human guardrails, the AI predicted gains when there should have been losses. With the proper human-AI framework, the system produced a credible prediction.

*Source: Top1000funds, January 15, 2026.*

**Institutional knowledge capture:** CPP's growth equity team used a generative AI tool to extract trends from 100+ general partner reports. The fund also developed custom GPTs and prompt libraries that convert individual expertise into reusable institutional tools. Their published framing: tacit knowledge (what to scrutinize, what to ignore, how to triangulate) can be converted into repeatable workflows that transform individual expertise into institutional leverage.

*Source: CPP Investments, "Making AI Governance, Education and Skills a Priority," November 2024.*

> **Relevance to this project:** CPP's three-pattern framework (Excels / Executes / Explores) maps directly to the tiered autonomy model in Section 5. Their five-gate verification architecture is the basis for the governance layer in the proposed repository. The head-to-head trial results on portfolio reconciliation and performance attribution validate two of the four workflows in this document.

### 4.3 CalSTRS

The California State Teachers' Retirement System ($401.6 billion as of February 2026, the largest educator-only pension fund in the world) has been the most transparent U.S. public pension fund about its AI strategy. In July 2025, CalSTRS staff presented a detailed AI integration plan to their board.

**Use case pipeline:** As of mid-2025, CalSTRS had documented 25 candidate AI use cases across more than ten business programs, six of which are in investments. Investment use cases include predictive dashboards, cash flow forecasting, memo drafting, and manager due diligence automation. The fund estimated an 85% increase in efficiency for targeted processes, with certain tasks reduced from 2.5 hours to 15 minutes.

*Source: Top1000funds, July 29, 2025; CalSTRS Investment Branch Business Plans FY 2025-26.*

**Change management approach:** CalSTRS wrote formal generative AI policies and guidelines, conducted a cost-benefit analysis, and planned an AI bootcamp for investment staff. Their consultants advised starting small, demonstrating quick wins to build momentum, and tying costs to mission-driven outcomes. Their board materials also documented the evolution of AI capabilities, noting that agentic AI is now capable of planning and executing tasks end-to-end.

*Source: Top1000funds, July 29, 2025.*

**Operational DD software:** The fund's risk-mitigating strategies team has already implemented AlternativeSoft's Operational Due Diligence software, which improved research and reporting efficiency by enabling integration of data from managers and service providers. Staff also participate in branch AI working groups testing tools that enhance research and analytical capabilities.

*Source: CalSTRS Investment Branch Business Plans FY 2025-26.*

> **Relevance to this project:** CalSTRS' documented use cases (memo drafting, manager DD automation, cash flow forecasting) align directly with Workflows 1, 2, and 4. Their 85% efficiency estimate for targeted processes provides a benchmark for what the framework should deliver. Their change management approach (policies first, then pilot, then scale) is a model for how institutions would adopt an open-source framework.

### 4.4 GIC

Singapore's sovereign wealth fund ($936 billion) has been investing heavily in AI capabilities, both as an investment theme and as an internal operations tool.

**Virtual IC member:** GIC is developing a prototype "virtual investment committee member" that draws on institutional knowledge to generate probing questions and challenge assumptions during the deal evaluation process. Public equity teams already use AI to interpret annual reports and management call transcripts. Private strategy teams draft underwriting reports with AI assistance and generate AI-driven questions for deal assessment.

*Source: Top1000funds, April 2025; GIC Newsroom.*

**Investment in AI infrastructure:** GIC led Anthropic's $30 billion Series G funding round in February 2025, signaling deep conviction in the technology's relevance to institutional investing. GIC established an AI Council in 2023 to coordinate adoption across the organization.

*Source: Vulcan Post, February 2025; Top1000funds, April 2025.*

> **Relevance to this project:** GIC's virtual IC member concept validates the IC Memo Agent approach from Section 3.1, taken a step further. Rather than just drafting the memo, GIC envisions an AI that plays devil's advocate during the actual committee discussion.

### 4.5 ADIA (Abu Dhabi Investment Authority)

ADIA ($1.1 trillion) has built one of the largest quantitative and data science teams among sovereign wealth funds, with approximately 150 data scientists and quantitative researchers. They launched the independent ADIA Lab research institution in 2022, focused on basic and applied research in data and computational sciences. ADIA expanded internal management from 55% to 64% of assets, partly enabled by technology-driven efficiencies.

*Source: Top1000funds, December 2024; Abu Dhabi Media Office.*

### 4.6 Patterns Across Early Adopters

Several consistent patterns emerge from these disclosures that inform the design of this framework:

- **Verification infrastructure is more important than model sophistication.** CPP's five-gate model and NBIM's 24-hour screening cycle both prioritize structured verification over raw AI capability. The framework's design reflects this: every agent output passes through a provenance-tracking layer before reaching a human reviewer.
- **Start with document-heavy, time-intensive tasks.** CalSTRS' use case pipeline and CPP's experiments both target work where humans spend the most time on data gathering and the least time on judgment. This is exactly the time-budget problem described in Section 2.4.
- **Organizational adoption requires policy and training before technology.** CalSTRS wrote policies before deploying tools. CPP trained all employees on responsible use before issuing licenses. The framework needs to ship with governance templates, not just code.
- **The goal is not fewer people but different work.** NBIM explicitly stated that AI will not reduce headcount. CPP's framing emphasizes that value will migrate from data processing to relationship management and judgment. The framework should amplify existing staff, not replace them.

---

## 5. Agent Design Principles for Fiduciary Settings

Agents operating in an institutional allocator context must follow design principles that reflect the fiduciary, governance, and regulatory environment. These principles constrain the architecture.

### 5.1 Agents Draft, Humans Decide

Every agent output that feeds into an investment decision is a draft. The PM reviews, edits, and takes ownership before it enters the decision process. The IC memo that reaches the committee is the PM's memo, not the agent's memo. The agent accelerated the data assembly; the PM provided the judgment.

This principle is operationally important because of ERISA's prudence standard (for public pension funds) and the Uniform Prudent Investor Act (for endowments and foundations). Delegating to an AI tool does not transfer fiduciary responsibility. The human must be able to explain and defend every recommendation.

### 5.2 Show Your Work

Every agent output must include a clear provenance chain. If the agent states that a manager's 5-year annualized return is 12.3%, the output must show where that number came from (eVestment query, DDQ page 14, or the manager's pitch book page 8). If the agent flags a discrepancy, it must show both data points and their sources.

This is required both for audit purposes and for practical trust-building. Investment professionals will not use an agent whose outputs they cannot verify. CPP Investments' published principle reinforces this: they are building toward a "zero-hallucination environment where every artifact of data is attributable."

### 5.3 Match AI to the Work

CPP Investments' three-pattern framework provides a useful taxonomy for agent design:

- **AI Excels:** Clear, rules-based tasks where the agent can operate with high autonomy. Examples: data extraction from standardized reports, performance calculation, compliance range checks, peer ranking.
- **AI Executes:** Quantitative work requiring human oversight. Examples: portfolio optimization, scenario modeling, attribution analysis. The agent does the computation; the human validates the methodology and interprets the results.
- **AI Explores:** Ambiguous problems where human judgment drives the value. Examples: evaluating a manager's investment thesis, assessing organizational culture during an on-site visit, forming a view on whether a strategy will work in the current market environment. The agent provides research support; the human makes the call.

### 5.4 Fail Loudly, Not Silently

When an agent cannot complete a task (data source unavailable, document format not parseable, calculation produces implausible results), it must surface the failure clearly rather than producing a best-guess output. A wrong number in an IC memo is worse than a gap flagged for manual completion.

### 5.5 BYOD (Bring Your Own Data)

The framework provides standardized data interfaces (adapters) for common data sources. Institutions implement the adapter for their specific setup. The adapter translates proprietary data formats into the framework's internal schema. This means:

- An institution using Bloomberg can implement the Bloomberg adapter.
- An institution without Bloomberg but with FactSet can implement the FactSet adapter.
- An institution that exports data to CSV from any system can use the CSV adapter as a starting point.

The framework ships with a CSV adapter and sample data so that anyone can run the workflows immediately without any paid data subscriptions. Adapters for open data sources (SEC EDGAR, FRED, Yahoo Finance via yfinance) are included in the first release.

