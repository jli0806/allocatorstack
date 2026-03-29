#!/usr/bin/env python3
"""Generate 3 synthetic DDQ PDF samples for testing and demo.

Each DDQ follows the ILPA/AIMA template structure with numbered sections.
- Granite Peak Capital: Clean, complete, strong performer
- Meridian Value Partners: Borderline — AUM discrepancy, incomplete, key person risk
- Osprey Global Advisors: Red flags — SEC enforcement, inconsistent fees, gaps

Usage:
    python scripts/generate-sample-ddqs.py
"""
from fpdf import FPDF
from pathlib import Path
import textwrap

OUTPUT_DIR = Path("samples/ddqs")


class DDQDocument(FPDF):
    def __init__(self, firm_name, fund_name):
        super().__init__()
        self.firm_name = firm_name
        self.fund_name = fund_name
        self.set_auto_page_break(auto=True, margin=25)

    @staticmethod
    def _clean(text):
        """Replace unicode characters incompatible with latin-1 core fonts."""
        return text.replace("\u2014", "--").replace("\u2013", "-").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"').replace("~", "approx. ")

    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(128, 128, 128)
        self.cell(0, 8, self._clean(f"{self.firm_name} -- Due Diligence Questionnaire"), align="R")
        self.ln(4)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-20)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

    def add_title_page(self, subtitle="ILPA/AIMA Due Diligence Questionnaire"):
        self.add_page()
        self.ln(50)
        self.set_font("Helvetica", "B", 24)
        self.set_text_color(0, 51, 102)
        self.cell(0, 15, self._clean(self.firm_name), align="C")
        self.ln(20)
        self.set_font("Helvetica", "", 16)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, self._clean(self.fund_name), align="C")
        self.ln(15)
        self.set_font("Helvetica", "I", 12)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, self._clean(subtitle), align="C")
        self.ln(10)
        self.cell(0, 10, "Confidential", align="C")

    def add_section_header(self, number, title):
        self.set_font("Helvetica", "B", 14)
        self.set_text_color(0, 51, 102)
        self.ln(6)
        self.cell(0, 10, self._clean(f"{number}. {title}"))
        self.ln(4)
        self.set_draw_color(0, 51, 102)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def add_question(self, qid, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, self._clean(f"{qid} {text}"))
        self.ln(2)

    def add_answer(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        cleaned = self._clean(text.strip())
        self.multi_cell(0, 5, cleaned)
        self.ln(4)

    def add_table(self, headers, rows):
        """Add a simple table with alternating row colors."""
        col_width = (190) / len(headers)
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        for h in headers:
            self.cell(col_width, 7, self._clean(h), border=1, fill=True, align="C")
        self.ln()
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 9)
        for i, row in enumerate(rows):
            if i % 2 == 0:
                self.set_fill_color(240, 245, 250)
            else:
                self.set_fill_color(255, 255, 255)
            for cell in row:
                self.cell(col_width, 6, self._clean(str(cell)), border=1, fill=True, align="C")
            self.ln()
        self.ln(4)


def generate_granite_peak():
    """Granite Peak Capital — Clean, complete, strong performer."""
    pdf = DDQDocument("Granite Peak Capital", "Granite Peak Value Fund IV")
    pdf.add_title_page()

    # Section 1: Investment Strategy
    pdf.add_page()
    pdf.add_section_header("1", "Investment Strategy & Process")

    pdf.add_question("1.1", "Describe your firm's investment strategy and philosophy.")
    pdf.add_answer(
        "Granite Peak Capital pursues a concentrated value investment strategy focused on "
        "U.S. small and mid-cap companies trading below intrinsic value. Our philosophy is "
        "rooted in fundamental bottom-up analysis with a focus on companies with durable "
        "competitive advantages, strong free cash flow generation, and capable management teams. "
        "We typically hold 25-35 positions with a 3-5 year investment horizon."
    )

    pdf.add_question("1.2", "What is your target market segment, geography, and sector focus?")
    pdf.add_answer(
        "Target market: U.S. small and mid-cap equities ($500M - $10B market cap). "
        "Geography: Primarily domestic (85-95% U.S.), with selective international exposure "
        "through U.S.-listed companies with global operations. Sector focus: Opportunistic across "
        "sectors, with historical concentrations in industrials, consumer staples, healthcare, "
        "and financial services. We avoid highly capital-intensive businesses and early-stage "
        "technology companies."
    )

    pdf.add_question("1.3", "Describe your investment process from sourcing to exit.")
    pdf.add_answer(
        "Our process follows five stages:\n"
        "1. Sourcing: Quantitative screens (P/E, P/FCF, EV/EBITDA below sector medians), "
        "industry contacts, and thematic research. We review ~500 companies annually.\n"
        "2. Initial Review: Quick assessment of business quality, competitive position, and "
        "management. Narrows to ~100 candidates.\n"
        "3. Deep Due Diligence: Financial modeling, management meetings, customer/supplier "
        "interviews, site visits. 4-8 week process. Narrows to ~30 investments.\n"
        "4. Portfolio Construction: Position sizing based on conviction level and risk assessment. "
        "Initial positions typically 2-4% of portfolio.\n"
        "5. Monitoring & Exit: Continuous monitoring against thesis. Sell discipline triggered by "
        "thesis completion, valuation target reached, or thesis invalidation."
    )

    pdf.add_question("1.4", "What is your target fund size and investment period?")
    pdf.add_answer(
        "Granite Peak Value Fund IV target size: $2.5 billion. Hard cap: $3.0 billion. "
        "Investment period: Evergreen structure with quarterly liquidity (45-day notice). "
        "Soft lock: 1 year from initial investment."
    )

    pdf.add_question("1.5", "What is your typical deal size range?")
    pdf.add_answer(
        "Individual position sizes range from $50M to $150M at cost. Initial positions "
        "are typically $75M-$100M, with room to add on weakness."
    )

    pdf.add_question("1.6", "Describe your sourcing process and competitive advantages in deal origination.")
    pdf.add_answer(
        "Our sourcing advantage comes from three channels:\n"
        "1. Proprietary quantitative screens that identify statistically cheap companies "
        "before they appear on consensus value screens.\n"
        "2. Deep industry relationships built over 18 years — our senior analysts have "
        "average 12+ years of sector coverage.\n"
        "3. Thematic research pipeline that identifies structural shifts creating value "
        "opportunities (e.g., post-spin-off situations, misunderstood business transformations)."
    )

    pdf.add_question("1.7", "What is your due diligence process for evaluating potential investments?")
    pdf.add_answer(
        "Due diligence follows a structured 4-8 week process:\n"
        "- Week 1-2: Financial model construction, 10-year historical analysis\n"
        "- Week 2-3: Management meetings (CEO, CFO, division heads)\n"
        "- Week 3-4: Customer and supplier reference checks (minimum 5 each)\n"
        "- Week 4-6: Site visits for industrial/manufacturing companies\n"
        "- Week 5-8: Investment committee presentation and debate\n"
        "Every investment requires unanimous IC approval."
    )

    pdf.add_question("1.8", "Describe your portfolio construction approach, including diversification targets.")
    pdf.add_answer(
        "Portfolio targets: 25-35 positions. Maximum single position: 7% at cost, 10% at market. "
        "Maximum sector concentration: 30%. Cash target: 2-5% (tactical range 0-10%). "
        "Active share target: >90% vs. Russell 2000 Value benchmark."
    )

    pdf.add_question("1.9", "What is your approach to value creation post-investment?")
    pdf.add_answer(
        "As a public equity investor, value creation occurs through security selection rather "
        "than operational involvement. We engage constructively with management teams on capital "
        "allocation, cost structure, and strategic direction. We have participated in 3 activist "
        "campaigns in the past 10 years, all resolved constructively."
    )

    pdf.add_question("1.10", "Describe your exit strategy and typical holding period.")
    pdf.add_answer(
        "Average holding period: 3.2 years (range: 6 months to 8+ years). Sell triggers:\n"
        "1. Thesis completion — stock reaches fair value estimate\n"
        "2. Better opportunity — position replaced by higher-conviction idea\n"
        "3. Thesis invalidation — fundamental deterioration\n"
        "Historically: 60% sold at/above target, 25% replaced by better ideas, 15% sold on "
        "thesis invalidation."
    )

    # Section 2: Organization
    pdf.add_section_header("2", "Organization & Team")

    pdf.add_question("2.1", "Provide an organizational chart showing all investment and non-investment professionals.")
    pdf.add_answer(
        "Granite Peak Capital — 42 employees total\n\n"
        "Investment Team (18):\n"
        "- Robert Chen, CFA — Managing Partner & CIO (founded 2008, 26 yrs experience)\n"
        "- Sarah Martinez — Partner, Senior PM (joined 2010, 22 yrs experience)\n"
        "- David Park, CFA — Partner, Senior Analyst (joined 2011, 19 yrs experience)\n"
        "- 6 Senior Analysts (avg 14 yrs experience, avg 8 yrs at firm)\n"
        "- 5 Analysts (avg 6 yrs experience)\n"
        "- 4 Research Associates\n\n"
        "Operations & Compliance (14):\n"
        "- COO, CCO, CFO, Head of Trading, 10 operations staff\n\n"
        "Business Development & Client Service (6):\n"
        "- Head of IR, 5 client service professionals\n\n"
        "Technology (4):\n"
        "- CTO, 3 developers"
    )

    pdf.add_question("2.2", "List all senior investment professionals, their titles, years at the firm, and years of relevant experience.")
    pdf.add_answer(
        "See organizational chart above. Key investment professionals:\n"
        "Robert Chen, CFA — Managing Partner & CIO, 16 years at firm, 26 years experience\n"
        "Sarah Martinez — Partner, Senior PM, 14 years at firm, 22 years experience\n"
        "David Park, CFA — Partner, Senior Analyst, 13 years at firm, 19 years experience"
    )

    pdf.add_question("2.3", "How many total employees does the firm have?")
    pdf.add_answer(
        "42 total employees as of December 31, 2025.\n"
        "Investment: 18 | Operations & Compliance: 14 | Client Service: 6 | Technology: 4"
    )

    pdf.add_question("2.4", "Describe the ownership structure of the management company.")
    pdf.add_answer(
        "Granite Peak Capital LLC is 100% employee-owned.\n"
        "Robert Chen: 55% | Sarah Martinez: 20% | David Park: 15% | Employee pool: 10%"
    )

    pdf.add_question("2.5", "Has there been any change in ownership in the last 5 years?")
    pdf.add_answer(
        "No. Ownership structure has been stable since 2018 when David Park was elevated to Partner."
    )

    pdf.add_question("2.6", "Identify the key persons for the fund.")
    pdf.add_answer(
        "Key persons: Robert Chen and Sarah Martinez. Key person event triggers suspension "
        "of new investments until LP advisory committee convenes (within 30 days)."
    )

    pdf.add_question("2.7", "Have any key investment professionals departed in the last 3 years?")
    pdf.add_answer("No key person departures in the last 3 years. No senior analyst departures since 2021.")

    pdf.add_question("2.8", "Describe the compensation structure for investment professionals.")
    pdf.add_answer(
        "Base salary + annual bonus (0-200% of base, tied to firm and individual performance) "
        "+ carried interest participation for Partners. Analysts participate in a deferred "
        "compensation pool tied to fund performance. All investment professionals are required "
        "to invest a minimum of 50% of annual bonus in the fund."
    )

    pdf.add_question("2.9", "What is the GP commitment to the fund?")
    pdf.add_answer(
        "GP commitment: $75 million (3% of target fund size). This represents meaningful "
        "personal capital for the founding team. Partners commit additional personal capital "
        "alongside the GP commitment."
    )

    pdf.add_question("2.10", "Describe any succession planning for senior leadership.")
    pdf.add_answer(
        "Formal succession plan in place since 2020. Sarah Martinez designated as successor CIO. "
        "David Park designated as successor Managing Partner. Both have been delegated increasing "
        "portfolio management authority over the past 5 years. External board advisor reviews "
        "succession plan annually."
    )

    pdf.add_question("2.11", "List all other funds or accounts managed by the firm.")
    pdf.add_answer(
        "1. Granite Peak Value Fund III — $2.1B AUM (closed to new investors)\n"
        "2. Granite Peak Value Fund IV — $1.8B AUM (current fund, target $2.5B)\n"
        "3. Granite Peak Institutional SMA — $400M across 5 accounts\n"
        "Total firm AUM: $4.3 billion as of December 31, 2025."
    )

    pdf.add_question("2.12", "What is the firm's total assets under management?")
    pdf.add_answer("$4.3 billion as of December 31, 2025.")

    # Section 3: Track Record
    pdf.add_section_header("3", "Track Record & Attribution")

    pdf.add_question("3.1", "Provide gross and net returns for each fund managed by the firm since inception.")
    pdf.add_answer("See performance table below.")
    pdf.add_table(
        ["Fund", "Inception", "Gross Ann.", "Net Ann.", "Benchmark"],
        [
            ["Value Fund I", "2008", "18.2%", "15.8%", "12.1%"],
            ["Value Fund II", "2012", "16.5%", "14.2%", "11.8%"],
            ["Value Fund III", "2017", "14.8%", "12.6%", "9.4%"],
            ["Value Fund IV", "2022", "17.1%", "14.9%", "10.2%"],
        ],
    )

    pdf.add_question("3.3", "Provide annualized returns (1, 3, 5, 10 year and since inception) net of all fees.")
    pdf.add_answer("Granite Peak Value Fund IV net returns:")
    pdf.add_table(
        ["Period", "Fund (Net)", "Russell 2000 Value", "Excess"],
        [
            ["1 Year", "14.2%", "8.7%", "+5.5%"],
            ["3 Year", "12.8%", "7.9%", "+4.9%"],
            ["Since Inception", "14.9%", "10.2%", "+4.7%"],
        ],
    )

    pdf.add_question("3.4", "What is the relevant benchmark?")
    pdf.add_answer("Russell 2000 Value Index. Secondary benchmark: Russell 2500 Value Index.")

    pdf.add_question("3.7", "What was the fund's performance during significant market downturns?")
    pdf.add_answer(
        "2008 (Fund I inception year): -22.4% vs. -28.9% benchmark (protected 6.5%)\n"
        "Q1 2020 COVID drawdown: -18.7% vs. -27.3% benchmark (protected 8.6%)\n"
        "2022 rate shock: -8.2% vs. -14.5% benchmark (protected 6.3%)\n"
        "Downside capture ratio (since inception, all funds): 72%"
    )

    pdf.add_question("3.8", "Provide the maximum drawdown and recovery period for each fund.")
    pdf.add_answer(
        "Fund I: Max drawdown -28.1% (2008), recovered in 14 months\n"
        "Fund II: Max drawdown -12.3% (2015-16), recovered in 6 months\n"
        "Fund III: Max drawdown -22.8% (Q1 2020), recovered in 9 months\n"
        "Fund IV: Max drawdown -11.4% (2022), recovered in 5 months"
    )

    pdf.add_question("3.13", "Has the track record been audited by a third party?")
    pdf.add_answer("Yes. All fund returns are audited annually by Ernst & Young LLP. GIPS-compliant.")

    pdf.add_question("3.14", "Are the reported returns GIPS-compliant?")
    pdf.add_answer("Yes. The firm has been GIPS-compliant since 2010 and is verified by ACA Performance Services.")

    # Section 4: Fees & Terms
    pdf.add_section_header("4", "Fund Terms & Fees")

    pdf.add_question("4.1", "What is the management fee rate and basis?")
    pdf.add_answer(
        "Management fee: 85 basis points on net asset value, calculated and accrued monthly, "
        "paid quarterly in arrears."
    )

    pdf.add_question("4.2", "Does the management fee step down?")
    pdf.add_answer(
        "Yes. Fee schedule:\n"
        "First $250M: 85 bps\n"
        "$250M - $500M: 75 bps\n"
        "Above $500M: 65 bps\n"
        "Blended rate for a $500M commitment: approximately 77 bps."
    )

    pdf.add_question("4.3", "What is the carried interest rate and preferred return?")
    pdf.add_answer(
        "Performance fee: 15% of net profits above a 6% annualized hurdle rate, "
        "calculated on a high-water mark basis."
    )

    pdf.add_question("4.7", "List all fees and expenses borne by the fund.")
    pdf.add_answer("Fee schedule:")
    pdf.add_table(
        ["Fee Type", "Amount", "Basis"],
        [
            ["Management Fee", "65-85 bps", "NAV, tiered"],
            ["Performance Fee", "15%", "Above 6% hurdle"],
            ["Admin/Custody", "~8 bps", "NAV"],
            ["Audit/Legal", "~3 bps", "NAV"],
            ["Trading Costs", "~5 bps", "Turnover-dependent"],
            ["Total Expense Ratio", "~100 bps", "Estimated"],
        ],
    )

    pdf.add_question("4.20", "Provide a total expense ratio estimate.")
    pdf.add_answer("Estimated TER: approximately 100 basis points (inclusive of management fee).")

    # Section 5: Risk Management
    pdf.add_section_header("5", "Risk Management")

    pdf.add_question("5.1", "Describe your overall risk management framework.")
    pdf.add_answer(
        "Risk management is integrated into the investment process at every stage. "
        "We employ a three-lines-of-defense model:\n"
        "1. Investment team: Position-level risk assessment during due diligence\n"
        "2. Risk committee (CIO + COO + CCO): Portfolio-level monitoring, weekly review\n"
        "3. External risk consultant: Quarterly independent risk assessment\n\n"
        "Key risk limits: Max position 7% at cost / 10% at market, max sector 30%, "
        "max cash 10%, minimum 20 positions."
    )

    pdf.add_question("5.3", "Is the risk management function independent from the investment team?")
    pdf.add_answer(
        "Partially. The risk committee includes the COO and CCO (independent of investment decisions) "
        "alongside the CIO. The external risk consultant (Albourne Partners) provides fully "
        "independent quarterly assessments."
    )

    pdf.add_question("5.12", "Have there been any material risk limit breaches in the past 5 years?")
    pdf.add_answer(
        "One technical breach in Q3 2023: A position reached 10.3% of portfolio due to rapid "
        "appreciation. The position was trimmed within 5 business days per policy. "
        "No breaches of sector, cash, or diversification limits."
    )

    # Section 6: Compliance
    pdf.add_section_header("6", "Compliance & Regulatory")

    pdf.add_question("6.1", "Is the firm registered with the SEC? Provide CRD number.")
    pdf.add_answer(
        "Yes. Granite Peak Capital LLC is registered with the SEC as an investment adviser "
        "under the Investment Advisers Act of 1940. CRD Number: 287456."
    )

    pdf.add_question("6.3", "Has the firm or any principal ever been subject to any regulatory investigation or enforcement action?")
    pdf.add_answer(
        "No. Neither the firm nor any current or former principal has been subject to any "
        "regulatory investigation, enforcement action, or sanction by the SEC, FINRA, any state "
        "securities regulator, or any self-regulatory organization."
    )

    pdf.add_question("6.4", "Describe the firm's compliance program.")
    pdf.add_answer(
        "The CCO (Jennifer Walsh, 18 years compliance experience) reports directly to the "
        "Managing Partner and has a dotted line to the independent advisory board. "
        "Annual compliance review by external counsel (Dechert LLP). "
        "Quarterly compliance testing program covering personal trading, gifts/entertainment, "
        "political contributions, and information barriers."
    )

    pdf.add_question("6.13", "Who is the fund's auditor?")
    pdf.add_answer("Ernst & Young LLP. Continuous relationship since firm inception in 2008. No auditor changes.")

    pdf.add_question("6.16", "Describe any pending or threatened litigation.")
    pdf.add_answer("None. No pending or threatened litigation involving the firm or any of its principals.")

    pdf.add_question("6.17", "Has the firm filed any amended ADV disclosures related to disciplinary events?")
    pdf.add_answer("No.")

    # Section 7: Responsible Investing
    pdf.add_section_header("7", "Responsible Investing")

    pdf.add_question("7.1", "Is the firm a signatory to the UN PRI?")
    pdf.add_answer("Yes. Signatory since 2019. Most recent PRI Assessment: A+ (Strategy & Governance), A (Listed Equity).")

    pdf.add_question("7.2", "Describe the firm's sustainability policy.")
    pdf.add_answer(
        "Sustainability factors are integrated into our fundamental analysis as material risk factors. "
        "We assess governance quality, environmental liabilities, and social license to operate "
        "as part of standard due diligence. We do not apply blanket exclusions but will decline "
        "investments where sustainability risks are material and unmitigable."
    )

    pdf.add_question("7.9", "Describe the firm's approach to climate risk assessment.")
    pdf.add_answer(
        "We conduct TCFD-aligned climate risk assessment for all portfolio holdings. "
        "Physical and transition risk scores are maintained for each position. "
        "Portfolio-level carbon footprint is reported quarterly."
    )

    # Section 8: Cybersecurity
    pdf.add_section_header("8", "IT & Cybersecurity")

    pdf.add_question("8.3", "Describe the firm's cybersecurity program.")
    pdf.add_answer(
        "SOC 2 Type II certified (renewed annually). NIST Cybersecurity Framework aligned. "
        "Annual penetration testing by CrowdStrike. All data encrypted at rest (AES-256) "
        "and in transit (TLS 1.3). Multi-factor authentication required for all systems."
    )

    pdf.add_question("8.7", "Has the firm experienced any cybersecurity incidents?")
    pdf.add_answer("No material cybersecurity incidents or data breaches in the firm's history.")

    pdf.output(str(OUTPUT_DIR / "granite-peak-capital.pdf"))
    print(f"Generated: {OUTPUT_DIR / 'granite-peak-capital.pdf'} ({pdf.page_no()} pages)")


def generate_meridian_value():
    """Meridian Value Partners — Borderline: AUM discrepancy, incomplete DDQ, key person risk."""
    pdf = DDQDocument("Meridian Value Partners", "Meridian Concentrated Value Fund II")
    pdf.add_title_page()

    # Section 1: Investment Strategy
    pdf.add_page()
    pdf.add_section_header("1", "Investment Strategy & Process")

    pdf.add_question("1.1", "Describe your firm's investment strategy and philosophy.")
    pdf.add_answer(
        "Meridian Value Partners employs a concentrated deep value approach focused on "
        "U.S. small-cap equities. We invest in high-quality businesses temporarily mispriced "
        "due to short-term market dislocations, management transitions, or sector-wide sell-offs. "
        "We typically hold 15-20 positions with a 2-4 year investment horizon."
    )

    pdf.add_question("1.2", "What is your target market segment?")
    pdf.add_answer(
        "U.S. small-cap value equities, $200M - $5B market cap. Primarily domestic. "
        "Opportunistic across sectors."
    )

    pdf.add_question("1.3", "Describe your investment process.")
    pdf.add_answer(
        "Sourcing through quantitative screens and industry relationships. "
        "Deep fundamental analysis with emphasis on normalized earnings power. "
        "Investment committee approval required (majority vote)."
    )

    pdf.add_question("1.4", "What is your target fund size?")
    pdf.add_answer(
        "Meridian Concentrated Value Fund II target: $1.2 billion. Hard cap: $1.5 billion. "
        "Current AUM: $1.8 billion."
    )
    # NOTE: AUM discrepancy — DDQ says $1.8B but ADV filing shows $1.4B

    pdf.add_question("1.8", "Describe your portfolio construction approach.")
    pdf.add_answer(
        "15-20 positions. Maximum single position: 10% at cost. "
        "No explicit sector limits. Cash range: 0-15%."
    )

    pdf.add_question("1.15", "Describe your investment committee process.")
    pdf.add_answer(
        "Three-person investment committee: James Liu (CIO), Michael Torres (PM), and "
        "one rotating senior analyst. Majority vote required. James Liu has tie-breaking authority."
    )

    # Section 2: Organization — INCOMPLETE (key person risk signals)
    pdf.add_section_header("2", "Organization & Team")

    pdf.add_question("2.1", "Provide an organizational chart.")
    pdf.add_answer(
        "Meridian Value Partners — 28 employees\n\n"
        "Investment Team (12):\n"
        "- James Liu — Founder, Managing Partner & CIO (founded 2015, 20 yrs experience)\n"
        "- Michael Torres — Partner, PM (joined 2016, 15 yrs experience)\n"
        "- 4 Senior Analysts, 4 Analysts, 2 Research Associates\n\n"
        "Operations (10): COO, CCO, CFO, 7 operations staff\n"
        "Client Service (4): Head of IR, 3 staff\n"
        "Technology (2): CTO, 1 developer"
    )

    pdf.add_question("2.3", "How many total employees does the firm have?")
    pdf.add_answer("28 total employees as of September 30, 2025.")

    pdf.add_question("2.4", "Describe the ownership structure.")
    pdf.add_answer(
        "James Liu: 72% | Michael Torres: 18% | Employee pool: 10%"
    )

    pdf.add_question("2.6", "Identify the key persons.")
    pdf.add_answer(
        "Sole key person: James Liu. Key person event triggers fund suspension."
    )
    # NOTE: Single key person is a risk — no successor named

    pdf.add_question("2.7", "Have any key investment professionals departed in the last 3 years?")
    pdf.add_answer(
        "Yes. Dr. Rebecca Santos, former Head of Research and Partner (15% ownership), "
        "departed in March 2025 to join a competitor. Her departure reduced the senior "
        "investment team from 4 to 3 partners. Her ownership stake was redistributed to "
        "James Liu (7%) and the employee pool (8%)."
    )
    # NOTE: Key person departure within 12 months — potential disqualifier

    pdf.add_question("2.9", "What is the GP commitment?")
    pdf.add_answer("GP commitment: $18 million (1.5% of target). James Liu: $15M, Michael Torres: $3M.")

    pdf.add_question("2.10", "Describe any succession planning.")
    pdf.add_answer(
        "Michael Torres is the designated successor CIO. Formal succession plan is being "
        "updated following Dr. Santos's departure. Expected completion: Q2 2026."
    )
    # NOTE: Succession plan "being updated" — not finalized

    pdf.add_question("2.12", "What is the firm's total assets under management?")
    pdf.add_answer("$1.8 billion as of September 30, 2025.")
    # NOTE: AUM discrepancy with ADV ($1.4B on ADV filing)

    # Section 3: Track Record
    pdf.add_section_header("3", "Track Record & Attribution")

    pdf.add_question("3.1", "Provide gross and net returns.")
    pdf.add_answer("Performance summary:")
    pdf.add_table(
        ["Fund", "Inception", "Gross Ann.", "Net Ann.", "Benchmark"],
        [
            ["Value Fund I", "2015", "13.7%", "11.2%", "10.1%"],
            ["Value Fund II", "2020", "15.3%", "12.8%", "9.8%"],
        ],
    )

    pdf.add_question("3.3", "Provide annualized returns net of all fees.")
    pdf.add_answer("Fund II net returns:")
    pdf.add_table(
        ["Period", "Fund (Net)", "Russell 2000 Value", "Excess"],
        [
            ["1 Year", "11.5%", "8.7%", "+2.8%"],
            ["3 Year", "10.9%", "7.9%", "+3.0%"],
            ["Since Inception", "12.8%", "9.8%", "+3.0%"],
        ],
    )

    pdf.add_question("3.7", "Performance during market downturns?")
    pdf.add_answer(
        "Q1 2020 COVID: -31.2% vs. -27.3% benchmark (underperformed by 3.9%)\n"
        "2022 rate shock: -16.8% vs. -14.5% benchmark (underperformed by 2.3%)"
    )
    # NOTE: Underperformed in downturns — concentrated portfolio risk

    pdf.add_question("3.13", "Has the track record been audited?")
    pdf.add_answer("Yes. Audited by KPMG LLP.")

    pdf.add_question("3.14", "Are returns GIPS-compliant?")
    pdf.add_answer("Yes. GIPS-compliant since 2018.")

    # Section 4: Fees — intentionally sparse
    pdf.add_section_header("4", "Fund Terms & Fees")

    pdf.add_question("4.1", "What is the management fee?")
    pdf.add_answer("Management fee: 100 basis points on NAV.")

    pdf.add_question("4.3", "Carried interest and preferred return?")
    pdf.add_answer("Performance fee: 20% above a 5% hurdle rate, high-water mark.")

    # NOTE: Questions 4.2, 4.5-4.20 not answered — incomplete section

    # Section 5: Risk Management — sparse
    pdf.add_section_header("5", "Risk Management")

    pdf.add_question("5.1", "Describe your risk management framework.")
    pdf.add_answer(
        "Risk management is overseen by the CIO with support from the COO. "
        "Position limits and sector guidelines are monitored daily. "
        "No formal risk committee."
    )
    # NOTE: No independent risk function

    # Sections 6-9: Minimal responses
    pdf.add_section_header("6", "Compliance & Regulatory")

    pdf.add_question("6.1", "Is the firm registered with the SEC?")
    pdf.add_answer("Yes. SEC-registered investment adviser. CRD Number: 301892.")

    pdf.add_question("6.3", "Any regulatory investigations or enforcement actions?")
    pdf.add_answer("No enforcement actions. One routine SEC examination in 2023 with no findings.")

    pdf.add_section_header("7", "Responsible Investing")
    pdf.add_question("7.1", "Is the firm a PRI signatory?")
    pdf.add_answer("No. The firm is evaluating PRI signatory status for 2026.")

    pdf.add_question("7.2", "Describe the firm's sustainability policy.")
    pdf.add_answer("Sustainability considerations are reviewed informally during the due diligence process. No formal sustainability policy document.")
    # NOTE: No formal sustainability policy — may be required by some allocators

    pdf.add_section_header("8", "IT & Cybersecurity")
    pdf.add_question("8.3", "Describe the firm's cybersecurity program.")
    pdf.add_answer("SOC 2 Type I certified. Annual penetration testing. MFA required for all systems.")

    pdf.output(str(OUTPUT_DIR / "meridian-value-partners.pdf"))
    print(f"Generated: {OUTPUT_DIR / 'meridian-value-partners.pdf'} ({pdf.page_no()} pages)")


def generate_osprey_global():
    """Osprey Global Advisors — Red flags: SEC enforcement, inconsistent fees, gaps."""
    pdf = DDQDocument("Osprey Global Advisors", "Osprey Global Opportunities Fund III")
    pdf.add_title_page()

    # Section 1: Investment Strategy
    pdf.add_page()
    pdf.add_section_header("1", "Investment Strategy & Process")

    pdf.add_question("1.1", "Describe your firm's investment strategy and philosophy.")
    pdf.add_answer(
        "Osprey Global Advisors pursues a global multi-strategy approach combining "
        "long/short equity, event-driven, and credit opportunities. We seek absolute "
        "returns with low correlation to traditional benchmarks. The fund targets 12-15% "
        "net annual returns through market cycles."
    )

    pdf.add_question("1.2", "What is your target market segment?")
    pdf.add_answer(
        "Global, all-cap. Primary focus on North America (60%) and Europe (30%), "
        "with opportunistic emerging markets exposure (10%). Multi-sector."
    )

    pdf.add_question("1.3", "Describe your investment process.")
    pdf.add_answer(
        "Multi-strategy approach driven by the CIO's market views and individual "
        "portfolio manager conviction. Each PM manages a sleeve with independent "
        "risk budgets. Centralized risk oversight."
    )

    pdf.add_question("1.4", "What is your target fund size?")
    pdf.add_answer(
        "Osprey Global Opportunities Fund III target: $3.0 billion. "
        "Current AUM: $2.7 billion."
    )

    pdf.add_question("1.13", "Describe any use of leverage.")
    pdf.add_answer(
        "Gross leverage target: 2.5x-3.5x. Net leverage range: 0.3x-0.8x long-biased. "
        "Maximum gross leverage: 4.0x (hard limit per fund documents)."
    )

    # Section 2: Organization
    pdf.add_section_header("2", "Organization & Team")

    pdf.add_question("2.1", "Provide an organizational chart.")
    pdf.add_answer(
        "Osprey Global Advisors — 85 employees total\n\n"
        "Investment Team (38):\n"
        "- Viktor Petrov — Founder & CIO (founded 2011, 28 yrs experience)\n"
        "- 5 Portfolio Managers (avg 16 yrs experience)\n"
        "- 12 Senior Analysts, 10 Analysts, 10 Research Associates\n\n"
        "Operations (28): COO, CCO, CFO, trading desk (8), middle office (10), "
        "legal (2), compliance (4)\n"
        "Client Service (12): Head of IR, 11 staff\n"
        "Technology (7): CTO, 6 developers"
    )

    pdf.add_question("2.3", "How many total employees does the firm have?")
    pdf.add_answer("85 employees as of June 30, 2025.")

    pdf.add_question("2.4", "Describe the ownership structure.")
    pdf.add_answer(
        "Viktor Petrov: 60% | Osprey Holdings Ltd (BVI entity): 25% | Employee pool: 15%"
    )
    # NOTE: Offshore holding entity in ownership structure

    pdf.add_question("2.5", "Has there been any change in ownership in the last 5 years?")
    pdf.add_answer(
        "Yes. In 2022, the firm restructured ownership to include Osprey Holdings Ltd "
        "(a British Virgin Islands entity) as part of a tax planning initiative. "
        "Viktor Petrov is the sole beneficial owner of Osprey Holdings Ltd."
    )
    # NOTE: Offshore entity — warrants deeper investigation

    pdf.add_question("2.7", "Have any key professionals departed in the last 3 years?")
    pdf.add_answer(
        "Two portfolio managers departed in 2024:\n"
        "- Jonathan Blake (Head of Credit, 8 years at firm) — departed April 2024\n"
        "- Dr. Anya Volkov (Head of European Equities, 6 years) — departed August 2024\n"
        "Both positions have been filled."
    )

    pdf.add_question("2.12", "Total assets under management?")
    pdf.add_answer("$2.7 billion as of June 30, 2025.")

    pdf.add_question("2.19", "Has the firm been involved in any material litigation?")
    pdf.add_answer(
        "The firm settled a dispute with a former employee in 2023 regarding "
        "non-compete provisions. Settlement terms are confidential. "
        "No other material litigation."
    )

    # Section 3: Track Record
    pdf.add_section_header("3", "Track Record & Attribution")

    pdf.add_question("3.1", "Provide gross and net returns.")
    pdf.add_answer("Performance summary:")
    pdf.add_table(
        ["Fund", "Inception", "Gross Ann.", "Net Ann.", "HFRI FoF"],
        [
            ["Opp. Fund I", "2011", "14.2%", "10.1%", "5.8%"],
            ["Opp. Fund II", "2016", "11.8%", "7.9%", "5.2%"],
            ["Opp. Fund III", "2021", "9.6%", "5.8%", "4.1%"],
        ],
    )
    # NOTE: Large gap between gross and net — high fees eating returns

    pdf.add_question("3.3", "Provide annualized returns net of all fees.")
    pdf.add_answer("Fund III net returns:")
    pdf.add_table(
        ["Period", "Fund (Net)", "HFRI FoF", "Excess"],
        [
            ["1 Year", "6.2%", "5.1%", "+1.1%"],
            ["3 Year", "5.4%", "4.3%", "+1.1%"],
            ["Since Inception", "5.8%", "4.1%", "+1.7%"],
        ],
    )

    pdf.add_question("3.7", "Performance during downturns?")
    pdf.add_answer(
        "Q1 2020: -19.4% (recovered in 11 months)\n"
        "2022: -12.7% (recovered in 14 months)\n"
        "Both underperformed stated objective of capital preservation."
    )

    pdf.add_question("3.13", "Has the track record been audited?")
    pdf.add_answer("Yes. Audited by Grant Thornton LLP.")

    pdf.add_question("3.14", "Are returns GIPS-compliant?")
    pdf.add_answer("No. The firm reports returns using internal methodology. GIPS compliance is under evaluation.")
    # NOTE: Not GIPS-compliant — unusual for a $2.7B firm

    # Section 4: Fees — inconsistent
    pdf.add_section_header("4", "Fund Terms & Fees")

    pdf.add_question("4.1", "What is the management fee?")
    pdf.add_answer("Management fee: 150 basis points on committed capital.")

    pdf.add_question("4.3", "Carried interest and preferred return?")
    pdf.add_answer(
        "Performance fee: 20% of net profits. No preferred return / hurdle rate."
    )
    # NOTE: No hurdle rate — unusual and investor-unfriendly

    pdf.add_question("4.7", "List all fees and expenses borne by the fund.")
    pdf.add_answer("Fund expenses include management fee, performance fee, operating expenses, "
        "and transaction costs. Organizational expenses were borne by the fund up to $2M.")

    pdf.add_question("4.8", "What is the policy on transaction and monitoring fees?")
    pdf.add_answer(
        "Transaction fees may be charged on certain private transactions. "
        "Monitoring fees may be charged to portfolio companies. "
        "Fees are not offset against the management fee."
    )
    # NOTE: No fee offset — fees on top of fees

    pdf.add_question("4.20", "Total expense ratio?")
    pdf.add_answer("Estimated TER: approximately 350 basis points (inclusive of all fees and expenses).")
    # NOTE: 350 bps TER is very high

    # Section 5: Risk Management — gaps
    pdf.add_section_header("5", "Risk Management")

    pdf.add_question("5.1", "Describe your risk management framework.")
    pdf.add_answer(
        "Risk management is overseen by the CIO with support from a dedicated risk analyst. "
        "Daily P&L monitoring, weekly risk report, monthly stress testing."
    )

    pdf.add_question("5.3", "Is risk management independent from the investment team?")
    pdf.add_answer(
        "The risk analyst reports to the CIO. The COO reviews risk reports monthly."
    )
    # NOTE: Risk reports to CIO — not independent

    pdf.add_question("5.12", "Any material risk limit breaches?")
    pdf.add_answer(
        "Two breaches in 2024:\n"
        "1. Gross leverage exceeded 4.0x limit briefly in March 2024 (reached 4.3x, "
        "corrected within 3 business days)\n"
        "2. Single-name concentration exceeded 15% limit in August 2024 due to a "
        "merger arbitrage position (resolved upon deal closing)"
    )
    # NOTE: Two risk breaches in one year

    # Section 6: Compliance — enforcement history
    pdf.add_section_header("6", "Compliance & Regulatory")

    pdf.add_question("6.1", "Is the firm registered with the SEC?")
    pdf.add_answer("Yes. SEC-registered. CRD Number: 295731.")

    pdf.add_question("6.3", "Any regulatory investigations or enforcement actions?")
    pdf.add_answer(
        "In 2021, the SEC issued a deficiency letter following a routine examination "
        "identifying inadequate disclosure of certain fee arrangements to fund investors. "
        "The firm remediated the identified issues and enhanced its disclosure practices. "
        "No formal enforcement action was taken.\n\n"
        "In 2023, the firm paid a $450,000 civil penalty to the SEC to settle charges "
        "related to inadequate disclosure of conflicts of interest arising from the "
        "allocation of co-investment opportunities. The firm neither admitted nor denied "
        "the findings. Enhanced compliance procedures were implemented."
    )
    # NOTE: SEC enforcement action — civil penalty

    pdf.add_question("6.4", "Describe the compliance program.")
    pdf.add_answer(
        "The CCO (appointed 2023, following the SEC settlement) reports to the COO. "
        "Annual compliance review. Quarterly testing program."
    )
    # NOTE: CCO appointed after settlement — suggests prior CCO was inadequate

    pdf.add_question("6.7", "Conflicts of interest policy?")
    pdf.add_answer(
        "Conflicts of interest policy was enhanced in 2023 following the SEC settlement. "
        "The policy now includes detailed disclosure requirements for co-investment "
        "allocation, fee arrangements, and related-party transactions."
    )

    pdf.add_question("6.13", "Who is the fund's auditor?")
    pdf.add_answer(
        "Grant Thornton LLP (since 2022). Previously audited by a regional firm "
        "(changed following the SEC examination)."
    )
    # NOTE: Changed auditors — may indicate issues with prior audit

    pdf.add_question("6.16", "Pending or threatened litigation?")
    pdf.add_answer(
        "One pending matter: A former LP has filed a demand for arbitration alleging "
        "breach of the LPA related to fee disclosures. The firm believes the claim is "
        "without merit. No reserve has been established."
    )
    # NOTE: Pending litigation related to fees

    pdf.add_question("6.17", "Amended ADV disclosures related to disciplinary events?")
    pdf.add_answer("Yes. ADV was amended in 2023 to disclose the SEC settlement.")

    # Section 7: Responsible Investing — minimal
    pdf.add_section_header("7", "Responsible Investing")

    pdf.add_question("7.1", "Is the firm a PRI signatory?")
    pdf.add_answer("No.")

    pdf.add_question("7.2", "Sustainability policy?")
    pdf.add_answer("The firm does not have a formal sustainability policy. Sustainability factors may be considered on a case-by-case basis.")
    # NOTE: No sustainability policy at all

    # Section 8: Cybersecurity — gaps
    pdf.add_section_header("8", "IT & Cybersecurity")

    pdf.add_question("8.3", "Cybersecurity program?")
    pdf.add_answer(
        "The firm follows industry standard cybersecurity practices. "
        "Annual security review conducted internally. MFA implemented in 2024."
    )
    # NOTE: No SOC certification, no external pen test, MFA only recently added

    pdf.add_question("8.4", "Third-party cybersecurity assessment?")
    pdf.add_answer("No external penetration testing has been conducted. Internal security review is performed annually.")
    # NOTE: No external pen test

    pdf.add_question("8.7", "Any cybersecurity incidents?")
    pdf.add_answer(
        "In 2023, a phishing attack compromised an employee email account. "
        "The incident was contained within 48 hours. No client data was exposed. "
        "This incident prompted the implementation of MFA across all systems."
    )
    # NOTE: Cybersecurity incident — phishing

    pdf.output(str(OUTPUT_DIR / "osprey-global-advisors.pdf"))
    print(f"Generated: {OUTPUT_DIR / 'osprey-global-advisors.pdf'} ({pdf.page_no()} pages)")


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generate_granite_peak()
    generate_meridian_value()
    generate_osprey_global()
    print("\nAll 3 sample DDQs generated successfully.")
