#!/usr/bin/env python3
"""Generate a realistic ILPA DDQ 2.0 filled-in PDF for Granite Peak Capital.

Follows the official ILPA Due Diligence Questionnaire 2.0 (November 2021) template
with 19 sections (section 20 excluded). Covers ~100 substantive questions across
all sections with realistic data for a US small/mid-cap value manager.

Manager profile:
- Granite Peak Capital, founded 2008
- US small/mid-cap value equity strategy
- $4.3B firm AUM, Fund IV targeting $2.5B
- 42 employees, CRD 287456
- Strong performer, clean compliance record

Usage:
    python scripts/generate-ilpa-ddq.py
"""
from fpdf import FPDF
from pathlib import Path

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
        return (
            text.replace("\u2014", "--")
            .replace("\u2013", "-")
            .replace("\u2019", "'")
            .replace("\u201c", '"')
            .replace("\u201d", '"')
            .replace("\u2018", "'")
            .replace("\u2022", "-")
            .replace("\u2026", "...")
            .replace("\u00ae", "(R)")
            .replace("\u2122", "(TM)")
            .replace("~", "approx. ")
            .replace("\u00b7", "-")
        )

    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(128, 128, 128)
        self.cell(
            0,
            8,
            self._clean(
                f"{self.firm_name} -- ILPA Due Diligence Questionnaire 2.0"
            ),
            align="R",
        )
        self.ln(4)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(6)

    def footer(self):
        self.set_y(-20)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(
            0, 10, f"Confidential  |  Page {self.page_no()}", align="C"
        )

    def add_title_page(
        self, subtitle="ILPA Due Diligence Questionnaire 2.0", date="March 2026"
    ):
        self.add_page()
        self.ln(40)
        self.set_font("Helvetica", "B", 28)
        self.set_text_color(0, 51, 102)
        self.cell(0, 15, self._clean(self.firm_name), align="C")
        self.ln(20)
        self.set_font("Helvetica", "", 18)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, self._clean(self.fund_name), align="C")
        self.ln(18)
        self.set_font("Helvetica", "I", 13)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, self._clean(subtitle), align="C")
        self.ln(12)
        self.set_font("Helvetica", "", 11)
        self.cell(0, 10, f"As of December 31, 2025", align="C")
        self.ln(8)
        self.cell(0, 10, f"Prepared: {date}", align="C")
        self.ln(16)
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(180, 0, 0)
        self.cell(0, 10, "CONFIDENTIAL", align="C")
        self.ln(8)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(100, 100, 100)
        self.multi_cell(
            0,
            5,
            self._clean(
                "This document contains confidential and proprietary information of "
                "Granite Peak Capital LLC. It is provided solely for the purpose of "
                "evaluating an investment in Granite Peak Value Fund IV and may not be "
                "reproduced, distributed, or disclosed to any third party without the "
                "prior written consent of Granite Peak Capital LLC."
            ),
            align="C",
        )

    def add_section_header(self, number, title):
        # Start new page for each major section
        self.add_page()
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(0, 51, 102)
        self.cell(0, 10, self._clean(f"Section {number}. {title}"))
        self.ln(4)
        self.set_draw_color(0, 51, 102)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())
        self.set_line_width(0.2)
        self.ln(8)

    def add_question(self, qid, text):
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(0, 0, 0)
        self.multi_cell(0, 5, self._clean(f"{qid}  {text}"))
        self.ln(2)

    def add_answer(self, text):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(40, 40, 40)
        cleaned = self._clean(text.strip())
        self.multi_cell(0, 5, cleaned)
        self.ln(4)

    def add_table(self, headers, rows, col_widths=None):
        """Add a simple table with alternating row colors."""
        if col_widths is None:
            col_width = 190 / len(headers)
            col_widths = [col_width] * len(headers)
        self.set_font("Helvetica", "B", 9)
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(
                col_widths[i], 7, self._clean(h), border=1, fill=True, align="C"
            )
        self.ln()
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "", 9)
        for ri, row in enumerate(rows):
            if ri % 2 == 0:
                self.set_fill_color(240, 245, 250)
            else:
                self.set_fill_color(255, 255, 255)
            for ci, cell in enumerate(row):
                self.cell(
                    col_widths[ci],
                    6,
                    self._clean(str(cell)),
                    border=1,
                    fill=True,
                    align="C",
                )
            self.ln()
        self.ln(4)


def generate_granite_peak_ilpa():
    """Granite Peak Capital -- Full ILPA DDQ 2.0 (Sections 1-19)."""
    pdf = DDQDocument("Granite Peak Capital", "Granite Peak Value Fund IV")
    pdf.add_title_page()

    # =========================================================================
    # SECTION 1: FIRM
    # =========================================================================
    pdf.add_section_header("1", "Firm")

    pdf.add_question(
        "1.1",
        "Provide a brief overview of the Firm, including information on the founding, "
        "subsequent history and information on any predecessor firm and/or parent firm.",
    )
    pdf.add_answer(
        "Granite Peak Capital LLC was founded in 2008 by Robert Chen in Denver, Colorado, "
        "with an initial focus on U.S. small and mid-cap value equities. Mr. Chen previously "
        "served as a Portfolio Manager at T. Rowe Price for 10 years, where he managed the "
        "Small-Cap Value Fund. The firm launched Granite Peak Value Fund I in September 2008, "
        "capitalizing on the financial crisis to build positions in high-quality companies at "
        "deeply discounted valuations. Since inception, the firm has grown organically to 42 "
        "employees and $4.3 billion in assets under management across three commingled funds "
        "and a small institutional separate account platform. There is no predecessor firm "
        "or parent organization; Granite Peak Capital is independently owned by its founding "
        "partners and employees."
    )

    pdf.add_question(
        "1.2",
        "Describe any plans to change or expand the Firm over the next five years.",
    )
    pdf.add_answer(
        "Granite Peak Capital does not plan any material changes to its business model over "
        "the next five years. The firm intends to remain focused exclusively on U.S. small "
        "and mid-cap value equities. We anticipate growing the team by 4-6 professionals "
        "over the next three years, primarily in research and operations. We opened a small "
        "satellite office in New York in 2023 to support East Coast client relationships and "
        "may add 2-3 professionals there. We have no plans to launch additional strategies, "
        "enter new geographies, or pursue a public listing."
    )

    pdf.add_question(
        "1.3",
        "Provide an overview of the ownership structure of the Firm.",
    )
    pdf.add_answer(
        "Granite Peak Capital LLC is 100% employee-owned. The ownership is distributed as "
        "follows: Robert Chen (Managing Partner & CIO) -- 55%; Sarah Martinez (Partner, "
        "Senior PM) -- 20%; David Park, CFA (Partner, Senior Analyst) -- 15%; Employee "
        "equity pool -- 10%. The employee equity pool is allocated among six senior team "
        "members who have been with the firm for more than five years. Ownership changes "
        "require unanimous consent of the three named partners. There are no external "
        "investors in the management company, and no portion of the firm has been sold or "
        "pledged as collateral."
    )

    pdf.add_question(
        "1.4",
        "Provide an organizational chart showing the management/organizational structure "
        "of the Firm.",
    )
    pdf.add_answer(
        "Granite Peak Capital -- 42 employees total\n\n"
        "Executive Leadership:\n"
        "- Robert Chen, CFA -- Managing Partner & CIO (founded 2008, 26 yrs experience)\n"
        "- Sarah Martinez -- Partner, Senior PM (joined 2010, 22 yrs experience)\n"
        "- David Park, CFA -- Partner, Senior Analyst (joined 2011, 19 yrs experience)\n\n"
        "Investment Team (18 total):\n"
        "- 3 Partners (above)\n"
        "- 6 Senior Analysts (avg 14 yrs experience, avg 8 yrs at firm)\n"
        "- 5 Analysts (avg 6 yrs experience)\n"
        "- 4 Research Associates\n\n"
        "Operations & Compliance (14 total):\n"
        "- Michael Huang -- COO (joined 2009, 20 yrs experience)\n"
        "- Jennifer Walsh -- CCO (joined 2012, 18 yrs compliance experience)\n"
        "- Thomas Reeves -- CFO (joined 2013, 16 yrs experience)\n"
        "- Amanda Li -- Head of Trading (joined 2014, 15 yrs experience)\n"
        "- 10 operations, compliance, and accounting staff\n\n"
        "Business Development & Client Service (6 total):\n"
        "- Christopher Yang -- Head of Investor Relations (joined 2015, 14 yrs experience)\n"
        "- 5 client service and marketing professionals\n\n"
        "Technology (4 total):\n"
        "- Daniel Kim -- CTO (joined 2016, 18 yrs experience)\n"
        "- 3 developers/systems administrators"
    )

    pdf.add_question("1.5", "Provide an overview of the C-suite at the Firm.")
    pdf.add_answer(
        "Robert Chen, CFA -- Managing Partner & Chief Investment Officer. Mr. Chen founded "
        "Granite Peak Capital in 2008 after 10 years at T. Rowe Price, where he was a PM on "
        "the Small-Cap Value team. He holds a BS in Economics from the University of "
        "Pennsylvania and an MBA from Columbia Business School. He is a CFA charterholder.\n\n"
        "Michael Huang -- Chief Operating Officer. Mr. Huang joined the firm in 2009 from "
        "Goldman Sachs Asset Management, where he served as VP of Operations for hedge fund "
        "services. He holds a BS in Finance from NYU Stern.\n\n"
        "Jennifer Walsh -- Chief Compliance Officer. Ms. Walsh joined in 2012 from Deloitte's "
        "Investment Management Advisory practice. She holds a JD from Georgetown University "
        "Law Center and is a member of the Colorado Bar.\n\n"
        "Thomas Reeves -- Chief Financial Officer. Mr. Reeves joined in 2013 from KPMG, where "
        "he was a Senior Manager in the Asset Management audit practice. He is a CPA.\n\n"
        "Daniel Kim -- Chief Technology Officer. Mr. Kim joined in 2016 from Bloomberg LP, "
        "where he led the Portfolio Analytics development team. He holds an MS in Computer "
        "Science from Carnegie Mellon University."
    )

    pdf.add_question(
        "1.6",
        "Does the Firm have any existing business lines that are unrelated to the "
        "Fund's investment strategy?",
    )
    pdf.add_answer(
        "No. Granite Peak Capital is exclusively focused on U.S. small and mid-cap value "
        "equity investing. All investment vehicles managed by the firm follow the same core "
        "strategy, differing only in vehicle structure (commingled fund vs. separate account) "
        "and, in some cases, portfolio concentration."
    )

    pdf.add_question(
        "1.7",
        "Provide a list of all investment vehicles previously managed by the Firm over "
        "the last five years.",
    )
    pdf.add_answer(
        "1. Granite Peak Value Fund I -- Launched September 2008, $380M at peak AUM, "
        "fully liquidated in 2019.\n"
        "2. Granite Peak Value Fund II -- Launched January 2012, $1.1B at peak AUM, "
        "fully liquidated in 2023.\n"
        "3. Granite Peak Value Fund III -- Launched March 2017, $2.1B current AUM, "
        "closed to new investors since Q4 2021.\n"
        "4. Granite Peak Value Fund IV -- Launched July 2022, $1.8B current AUM, "
        "target $2.5B, currently accepting new investors.\n"
        "5. Granite Peak Institutional SMA Program -- Launched 2019, $400M across 5 "
        "separately managed accounts for institutional clients with minimum $50M commitment."
    )

    pdf.add_question(
        "1.8",
        "Has the Firm entered any joint ventures with or sold a minority interest "
        "in the Firm to another manager?",
    )
    pdf.add_answer(
        "No. Granite Peak Capital has not entered into any joint ventures, strategic "
        "partnerships, or minority interest sales with any other investment manager. The "
        "firm has been approached periodically by larger asset management firms regarding "
        "potential acquisitions or strategic investments, but has declined all such inquiries. "
        "The partners are committed to maintaining full independence."
    )

    pdf.add_question(
        "1.9",
        "Describe the Firm's capital raising plans over the next five years.",
    )
    pdf.add_answer(
        "The firm's primary near-term capital raising objective is completing the fundraise "
        "for Granite Peak Value Fund IV, targeting $2.5 billion with a hard cap of $3.0 "
        "billion. Fund IV has raised $1.8 billion to date and we anticipate reaching the "
        "target by Q3 2026. We expect to launch Fund V in 2028-2029, depending on the "
        "deployment pace of Fund IV capital. The SMA program may grow modestly to $500-600M "
        "as we accept one or two additional mandates. We have no plans to take the firm "
        "public, raise permanent capital, or launch any new strategies."
    )

    pdf.add_question(
        "1.10",
        "Provide information regarding indebtedness of any kind.",
    )
    pdf.add_answer(
        "The firm has no indebtedness of any kind. The management company operates on a "
        "debt-free basis and has never borrowed funds for operational purposes. No partner's "
        "interest in the management company has been pledged as collateral for any loan. The "
        "firm maintains a cash reserve equivalent to approximately 18 months of operating "
        "expenses."
    )

    pdf.add_question(
        "1.11",
        "Has the Firm or any affiliated entity ever failed to make payments under "
        "any secured or unsecured indebtedness?",
    )
    pdf.add_answer("No. Not applicable; the firm has no indebtedness.")

    pdf.add_question(
        "1.19", "Is the Firm a publicly held company?"
    )
    pdf.add_answer(
        "No. Granite Peak Capital LLC is a privately held limited liability company "
        "organized under the laws of the State of Delaware."
    )

    pdf.add_question(
        "1.20",
        "Provide information regarding the Firm's liquidity and capitalization.",
    )
    pdf.add_answer(
        "The management company is well-capitalized with strong liquidity. As of December "
        "31, 2025, the firm holds approximately $28 million in cash and short-term "
        "investments, representing roughly 18 months of operating expenses. Revenue is "
        "generated from management fees (approximately $34M annually) and performance fees "
        "(variable). The firm has been profitable every year since 2010 and has no external "
        "debt. The management company's financial statements are audited annually by "
        "Ernst & Young LLP."
    )

    pdf.add_question(
        "1.24", "Does the Firm have dedicated human resources staff?"
    )
    pdf.add_answer(
        "Yes. The firm has a dedicated HR Manager who reports to the COO. The HR function "
        "handles recruiting, onboarding, benefits administration, employee engagement "
        "surveys, background checks (conducted via Sterling Check for all new hires), "
        "performance review coordination, and policy administration. The HR Manager works "
        "with external employment counsel (Fisher Phillips LLP) on compliance matters. All "
        "new hires undergo comprehensive background checks including criminal history, "
        "credit history, employment verification, and education verification."
    )

    pdf.add_question(
        "1.25", "Does the Firm have defined values?"
    )
    pdf.add_answer(
        "Yes. Granite Peak Capital's core values are: (1) Intellectual Rigor -- we demand "
        "thorough, evidence-based analysis in every investment decision; (2) Integrity -- we "
        "act as fiduciaries first and foremost; (3) Collaboration -- our best ideas emerge "
        "from open debate and constructive challenge; (4) Patience -- our long-term "
        "orientation drives superior compounding; and (5) Continuous Improvement -- we "
        "conduct post-mortems on every realized investment and systematically refine our "
        "process. These values are embedded in our recruiting criteria, annual performance "
        "reviews, and compensation decisions."
    )

    pdf.add_question(
        "1.29",
        "Indicate whether the Firm has any of the following codes, manuals or policies.",
    )
    pdf.add_answer(
        "The firm maintains the following policies, all of which are reviewed at least "
        "annually by the CCO and/or external counsel:\n"
        "- Compliance Manual (updated annually, last reviewed November 2025)\n"
        "- Code of Ethics / Code of Conduct\n"
        "- Conflicts of Interest Policy\n"
        "- Personal Trading Policy (pre-clearance required for all employee trades)\n"
        "- MNPI Policy (Material Non-Public Information)\n"
        "- Remote Work Policy (updated 2023)\n"
        "- Political/Charitable Contributions Policy\n"
        "- Risk Management Policy\n"
        "- Whistleblower Policy\n"
        "- AML/KYC Policy\n"
        "- Privacy Policy (GDPR and CCPA compliant)\n"
        "- Valuation Policy\n"
        "- Cyber/Information Security Policy (NIST-aligned)\n"
        "- Business Continuity Plan (tested semi-annually)\n"
        "- Disaster Recovery Plan\n"
        "- Responsible Investment Policy (adopted 2019)\n"
        "- Recruiting Process and Policy\n"
        "Copies of all policies are available upon request under NDA."
    )

    # =========================================================================
    # SECTION 2: FUND
    # =========================================================================
    pdf.add_section_header("2", "Fund")

    pdf.add_question(
        "2.1",
        "Provide the legal and tax structure of the Fund.",
    )
    pdf.add_answer(
        "Granite Peak Value Fund IV is structured as a Delaware limited partnership. The "
        "General Partner is Granite Peak GP IV LLC, a Delaware limited liability company "
        "wholly owned by Granite Peak Capital LLC. An offshore feeder (Granite Peak Value "
        "Fund IV Offshore, Ltd., a Cayman Islands exempted company) invests into the main "
        "fund to accommodate non-U.S. and tax-exempt investors. The fund operates under "
        "standard partnership tax treatment (pass-through). The fund's legal counsel is "
        "Dechert LLP; tax counsel is Sidley Austin LLP."
    )

    pdf.add_question(
        "2.3",
        "Will Placement Agents be used during the capital raising process for this Fund?",
    )
    pdf.add_answer(
        "No. Granite Peak Capital raises capital entirely through its internal investor "
        "relations team. The firm has never used a placement agent for any of its funds. "
        "Capital raising is led by Christopher Yang, Head of Investor Relations, supported "
        "by five client service professionals."
    )

    pdf.add_question(
        "2.5",
        "Describe where the responsibilities for capital raising live within the Firm.",
    )
    pdf.add_answer(
        "Capital raising is managed by the Investor Relations team under Christopher Yang, "
        "who reports directly to Robert Chen. The three partners (Chen, Martinez, Park) "
        "participate actively in investor meetings, on-site due diligence visits, and annual "
        "investor days. The IR team manages the fundraising pipeline, coordinates DDQ "
        "responses, and maintains ongoing LP relationships. Fundraising activities do not "
        "detract from investment activities, as the IR team operates independently from the "
        "investment team."
    )

    pdf.add_question(
        "2.6",
        "Detail the capital raising timeline.",
    )
    pdf.add_answer(
        "Granite Peak Value Fund IV held its first close in July 2022 at $750 million. "
        "Subsequent closes: Second close December 2022 ($350M), Third close June 2023 "
        "($300M), Fourth close March 2024 ($200M), Fifth close September 2024 ($200M). "
        "Total capital raised to date: $1.8 billion across 47 limited partners. The fund "
        "is targeting a final close at $2.5 billion by Q3 2026, with a hard cap of $3.0 "
        "billion. The investor base includes public pension funds (35%), corporate pension "
        "plans (15%), endowments and foundations (20%), family offices (15%), insurance "
        "companies (10%), and fund-of-funds (5%)."
    )

    pdf.add_question(
        "2.9",
        "Will there be an annual investor meeting throughout the life of the Fund?",
    )
    pdf.add_answer(
        "Yes. Granite Peak Capital hosts an Annual Investor Day each September at its Denver "
        "headquarters. The event includes portfolio review presentations, market outlook, "
        "team introductions, and a Q&A session with the CIO. The meeting is offered in "
        "hybrid format (in-person and virtual). Recordings are made available on the investor "
        "portal within two weeks. In addition, the firm hosts quarterly conference calls open "
        "to all LPs within 30 days of quarter-end."
    )

    pdf.add_question(
        "2.11",
        "Describe the expected timing and format of LPAC meetings.",
    )
    pdf.add_answer(
        "The LPAC meets at least twice per year, typically in March and September. "
        "Additional ad hoc meetings are convened as needed for conflict-of-interest reviews "
        "or material matters. Meetings are conducted via video conference with the option "
        "for in-person attendance at the Denver office. An in-camera session (without GP "
        "presence) is facilitated at each meeting. Meeting minutes are distributed within "
        "15 business days. LPAC members serve two-year terms with the option to renew."
    )

    pdf.add_question(
        "2.12",
        "Describe the anticipated composition of the Fund's LPAC.",
    )
    pdf.add_answer(
        "The LPAC consists of 5-7 members representing the fund's largest and most "
        "engaged limited partners. Current LPAC members include representatives from: "
        "Colorado PERA, University of Michigan Endowment, MetLife Investment Management, "
        "and two family office investors. The LPAC reviews conflicts of interest, valuations, "
        "key person events, and fund extension requests. LPAC members do not receive "
        "compensation or preferential economic terms for their service."
    )

    pdf.add_question(
        "2.14",
        "Is the Fund prohibited from holding leverage on its balance sheet?",
    )
    pdf.add_answer(
        "The fund does not employ portfolio-level leverage as a structural element of "
        "the strategy. The LPA permits borrowing up to 15% of committed capital solely for "
        "bridging purposes (i.e., to facilitate portfolio transactions or cover short-term "
        "timing differences between capital calls and deployment). Any borrowing in excess "
        "of 30 days requires LPAC notification."
    )

    pdf.add_question(
        "2.17",
        "Provide the Fund's annualized pro-forma budget.",
    )
    pdf.add_answer(
        "Fund IV estimated annual expenses (at target $2.5B AUM):\n"
        "- Management fee (to GP): approx. $19.3M (blended rate approx. 77 bps)\n"
        "- Administration & custody: approx. $2.0M\n"
        "- Audit & tax: approx. $750K\n"
        "- Legal: approx. $500K\n"
        "- Insurance: approx. $200K\n"
        "- Other fund expenses: approx. $300K\n"
        "- Total estimated annual expense: approx. $23.1M\n"
        "- Estimated total expense ratio: approx. 92 bps (inclusive of management fee)\n"
        "Organizational expenses were capped at $1.5 million, with actual organizational "
        "costs of $1.2 million."
    )

    # =========================================================================
    # SECTION 3: TEAM (Succession Planning / Key Persons in ILPA)
    # =========================================================================
    pdf.add_section_header("3", "Succession Planning / Key Persons")

    pdf.add_question(
        "3.1",
        "Is there a succession plan for the Firm?",
    )
    pdf.add_answer(
        "Yes. A formal succession plan has been in place since 2020 and is reviewed annually "
        "by the partners and an independent advisory board member. Sarah Martinez is "
        "designated as successor CIO, and David Park is designated as successor Managing "
        "Partner. Both have been delegated increasing portfolio management and business "
        "management authority over the past five years. The succession plan covers leadership "
        "transition, economic transition (gradual transfer of management company economics "
        "over a 5-7 year period), client relationship continuity, and governance changes."
    )

    pdf.add_question(
        "3.7",
        "Has there been a transition to retirement or departure by a member of Leadership "
        "in the Firm's history?",
    )
    pdf.add_answer(
        "No. There have been no transitions to retirement or departures by any member of "
        "Leadership in the firm's history. All three founding/early partners remain actively "
        "engaged in the business. Robert Chen (age 52) has communicated his intention to "
        "remain as CIO for at least the next 10 years."
    )

    pdf.add_question(
        "3.8",
        "Is a member of Leadership or a Senior Investment Professional currently in the "
        "process of or anticipated to transition to retirement or depart the Firm?",
    )
    pdf.add_answer(
        "No. All members of Leadership and Senior Investment Professionals are expected to "
        "remain with the firm through the Fund's investment period and beyond. No departures "
        "are anticipated."
    )

    pdf.add_question(
        "3.12",
        "Provide an overview of the Fund's Key Person provision.",
    )
    pdf.add_answer(
        "The Key Persons for Fund IV are Robert Chen and Sarah Martinez. A Key Person Event "
        "is triggered if either Key Person ceases to devote substantially all of their "
        "professional time to the firm's investment activities, or if both Key Persons cease "
        "to be actively involved. Upon a Key Person Event, the investment period is suspended "
        "and no new investments may be made until the LPAC convenes (within 30 business days) "
        "to determine next steps: (a) reinstatement with a replacement approved by LPAC, "
        "(b) extension of the suspension, or (c) termination of the investment period. The "
        "Key Person provision in Fund IV is consistent with Fund III."
    )

    pdf.add_question(
        "3.14",
        "Describe any hires and promotions within members of Leadership or Senior "
        "Investment Professionals that took place over the last year.",
    )
    pdf.add_answer(
        "In 2025, two analysts were promoted to Senior Analyst: Katherine Moore (Healthcare "
        "sector, 9 years at firm) and James Rodriguez (Industrials sector, 7 years at firm). "
        "One new analyst, William Chang, was hired from Fidelity Investments in March 2025. "
        "No changes were made to the Leadership team."
    )

    # =========================================================================
    # SECTION 4: INVESTMENT STRATEGY
    # =========================================================================
    pdf.add_section_header("4", "Investment Strategy")

    pdf.add_question(
        "4.1",
        "Summarize the Fund's investment strategy and types of transactions the Fund "
        "will pursue.",
    )
    pdf.add_answer(
        "Granite Peak Value Fund IV pursues a concentrated value investment strategy focused "
        "on U.S. small and mid-cap companies (market capitalization $500M to $10B at time of "
        "initial investment) trading below our estimate of intrinsic value. Our philosophy "
        "is rooted in fundamental, bottom-up analysis emphasizing companies with durable "
        "competitive advantages, strong free cash flow generation, capable management teams, "
        "and healthy balance sheets. The portfolio typically holds 25-35 positions with a "
        "3-5 year investment horizon. Target return: 10-15% net annualized over a full market "
        "cycle. Geographic focus: 85-95% U.S.-domiciled companies, with selective exposure "
        "to U.S.-listed companies with significant international operations."
    )

    pdf.add_question(
        "4.2",
        "Is the Fund's strategy meaningfully different from the predecessor fund?",
    )
    pdf.add_answer(
        "No. Fund IV follows the same investment strategy as Fund III. The only meaningful "
        "difference is the target fund size ($2.5B for Fund IV vs. $2.0B for Fund III), "
        "which reflects organic growth in the opportunity set and the firm's demonstrated "
        "capacity to deploy capital effectively at this level. Position sizes have scaled "
        "proportionally. The investment process, team, risk limits, and return targets remain "
        "unchanged."
    )

    pdf.add_question(
        "4.5",
        "Describe the background and evolution of the Firm's investment strategy.",
    )
    pdf.add_answer(
        "The firm's investment strategy has remained consistent since inception in 2008: "
        "concentrated U.S. small/mid-cap value equity. The primary evolution has been in "
        "position sizing and research depth rather than strategy. Fund I ($380M) held 20-25 "
        "positions; Fund IV ($2.5B target) targets 25-35 positions, reflecting our ability to "
        "deploy more capital per idea without compromising returns. Our quantitative screening "
        "tools have become more sophisticated, incorporating alternative data sources since "
        "2020 (satellite imagery, web traffic, patent filings). We added a dedicated ESG "
        "integration framework in 2019 when we became a PRI signatory."
    )

    pdf.add_question(
        "4.7",
        "Provide detail on the Fund's diversification strategy.",
    )
    pdf.add_answer(
        "Portfolio construction guidelines:\n"
        "- Number of positions: 25-35\n"
        "- Maximum single position at cost: 7% of portfolio\n"
        "- Maximum single position at market: 10% of portfolio\n"
        "- Maximum sector concentration: 30%\n"
        "- Cash target: 2-5% (tactical range 0-10%)\n"
        "- Minimum positions: 20\n"
        "- Active share target: >90% vs. Russell 2000 Value Index\n"
        "- Market cap range at purchase: $500M - $10B\n"
        "We do not employ formal geographic concentration limits as the portfolio is "
        "substantially all U.S.-listed equities. Sector diversification is managed actively "
        "but opportunistically -- we do not force allocation to sectors where we lack conviction."
    )

    pdf.add_question(
        "4.13",
        "Describe the use of leverage at the portfolio company level.",
    )
    pdf.add_answer(
        "As a public equity investor, we do not control leverage decisions at portfolio "
        "companies. However, balance sheet quality is a critical factor in our investment "
        "analysis. We generally avoid companies with net debt/EBITDA exceeding 3.0x and "
        "favor companies with strong interest coverage ratios (>5.0x). The fund itself does "
        "not employ leverage for investment purposes. See Section 2 for details on the "
        "fund's limited borrowing capacity for bridging purposes."
    )

    pdf.add_question(
        "4.19",
        "Describe any investments that will not be considered.",
    )
    pdf.add_answer(
        "The fund will not invest in: (1) companies with market capitalization below $300M "
        "or above $15B at the time of initial purchase; (2) pre-revenue or early-stage "
        "companies; (3) special purpose acquisition companies (SPACs); (4) cryptocurrencies "
        "or digital assets; (5) commodities or commodity futures; (6) private placements "
        "or pre-IPO securities; (7) companies deriving more than 15% of revenue from tobacco, "
        "controversial weapons, or thermal coal extraction."
    )

    pdf.add_question(
        "4.20",
        "Describe the risk factors of the Fund's investment strategy.",
    )
    pdf.add_answer(
        "Key risk factors include: (1) Market risk -- small/mid-cap equities exhibit higher "
        "volatility than large-cap indices, particularly during risk-off environments; "
        "(2) Concentration risk -- a portfolio of 25-35 positions carries meaningful single-name "
        "risk; (3) Value trap risk -- companies appearing statistically cheap may face "
        "structural decline; (4) Liquidity risk -- some smaller positions may have limited "
        "trading volume, requiring patience to build or exit positions; (5) Factor rotation "
        "risk -- extended periods of growth outperformance may create headwinds for value "
        "strategies. Mitigants include rigorous fundamental analysis, position sizing "
        "discipline, sector diversification, stop-loss monitoring, and deep management "
        "engagement."
    )

    pdf.add_question(
        "4.23",
        "What is the targeted return-profile threshold for investments by the Fund?",
    )
    pdf.add_answer(
        "We target a gross IRR of 13-18% and a net IRR of 10-15% per investment over a "
        "3-5 year holding period. At the portfolio level, we target net returns of 10-15% "
        "annualized over a full market cycle, with a Sharpe ratio exceeding 0.60 and downside "
        "capture below 80% relative to the Russell 2000 Value Index. We seek a minimum 30% "
        "discount to our estimate of intrinsic value at the time of initial purchase, "
        "providing a margin of safety."
    )

    # =========================================================================
    # SECTION 5: SOURCING / DUE DILIGENCE (Co-Investments in ILPA)
    # =========================================================================
    pdf.add_section_header("5", "Co-Investments")

    pdf.add_question(
        "5.1",
        "Will the Fund offer co-investments?",
    )
    pdf.add_answer(
        "Yes. The fund may offer co-investment opportunities to existing LPs on a selective "
        "basis for positions where the GP wishes to allocate additional capital beyond the "
        "fund's concentration limits. Co-investments are offered at no additional management "
        "fee and no carried interest. Co-investment allocation is determined by the GP based "
        "on LP interest, relationship, and ability to execute within required timelines. "
        "Historically, Fund III offered 4 co-investment opportunities totaling approximately "
        "$180 million in aggregate."
    )

    pdf.add_question(
        "5.2",
        "Identify any changes to the Fund's policy regarding co-investments relative "
        "to the predecessor fund.",
    )
    pdf.add_answer(
        "No material changes. The co-investment policy for Fund IV is consistent with "
        "Fund III. Co-investments remain at the GP's discretion, offered without additional "
        "management fees or carried interest. The minimum co-investment amount remains $10 "
        "million per opportunity."
    )

    # =========================================================================
    # SECTION 6: PORTFOLIO CONSTRUCTION (GP-Led Secondaries in ILPA)
    # =========================================================================
    pdf.add_section_header("6", "GP-Led Secondaries / Continuation Funds")

    pdf.add_question(
        "6.1",
        "Has the Firm carried out a GP-led secondary transaction over the last five years?",
    )
    pdf.add_answer(
        "No. Granite Peak Capital has never carried out a GP-led secondary transaction or "
        "continuation fund transaction. As a public equity manager with liquid underlying "
        "investments, GP-led secondaries are not relevant to our fund structure. LPs have "
        "quarterly redemption rights subject to a 45-day notice period."
    )

    # =========================================================================
    # SECTION 7: PORTFOLIO MANAGEMENT (Credit Facilities in ILPA)
    # =========================================================================
    pdf.add_section_header("7", "Credit Facilities")

    pdf.add_question(
        "7.1",
        "Describe the Fund's approach to credit facilities.",
    )
    pdf.add_answer(
        "Fund IV maintains a $200 million subscription line of credit with JPMorgan Chase "
        "to bridge timing differences between capital calls and investment deployment. "
        "The facility is secured by LP commitments and is used solely for short-term "
        "liquidity management (typically drawn for less than 15 business days). Maximum "
        "borrowing is limited to 15% of aggregate unfunded commitments. The facility has "
        "never been drawn for more than 20 consecutive days. Interest costs are borne by "
        "the fund."
    )

    pdf.add_question(
        "7.3",
        "Is the Fund currently using a subscription line of credit?",
    )
    pdf.add_answer(
        "Yes. The fund has a $200 million subscription line of credit with JPMorgan Chase, "
        "established at fund inception in July 2022. As of December 31, 2025, there was no "
        "outstanding balance on the facility. During 2025, the facility was drawn four times "
        "for an average of 8 business days per draw, with an average draw amount of $45 "
        "million."
    )

    pdf.add_question(
        "7.9",
        "Does the Fund provide LPs with their Net IRR with and without the use of the "
        "subscription line of credit?",
    )
    pdf.add_answer(
        "Yes. Quarterly and annual performance reports include net IRR calculated both "
        "with and without the impact of the subscription line of credit. The difference "
        "has historically been less than 20 basis points, reflecting the limited and "
        "short-term nature of our credit facility usage."
    )

    # =========================================================================
    # SECTION 8: FUND RESTRUCTURINGS (Investment Process in ILPA)
    # =========================================================================
    pdf.add_section_header("8", "Investment Process")

    pdf.add_question(
        "8.5",
        "Describe the Firm's deal sourcing capabilities.",
    )
    pdf.add_answer(
        "Our sourcing advantage comes from three channels:\n"
        "1. Proprietary quantitative screens: We screen the Russell 2000 and Russell 2500 "
        "universes weekly using custom factor models (P/E, P/FCF, EV/EBITDA, dividend yield "
        "vs. sector medians, insider buying, short interest anomalies). These screens "
        "identify statistically cheap companies before they appear on consensus value screens. "
        "We review approximately 500 companies annually through this process.\n"
        "2. Deep industry relationships: Our senior analysts have an average of 12+ years of "
        "sector coverage and maintain extensive networks with management teams, board members, "
        "industry consultants, and sell-side analysts.\n"
        "3. Thematic research pipeline: We maintain a standing list of 8-10 structural themes "
        "(e.g., post-spin-off situations, misunderstood business transformations, cyclical "
        "troughs, regulatory-driven dislocations) and systematically screen for companies "
        "affected by these themes."
    )

    pdf.add_question(
        "8.6",
        "Describe the Firm's screening and due diligence processes.",
    )
    pdf.add_answer(
        "Due diligence follows a structured 4-8 week process:\n"
        "- Week 1-2: Financial model construction based on 10-year historical analysis. "
        "Normalized earnings, ROIC decomposition, free cash flow bridge. Initial competitive "
        "positioning assessment.\n"
        "- Week 2-3: Management meetings with CEO, CFO, and relevant division heads. We "
        "prioritize in-person meetings at company headquarters.\n"
        "- Week 3-4: Customer and supplier reference checks (minimum 5 each). Competitor "
        "interviews where possible.\n"
        "- Week 4-6: Site visits for industrial and manufacturing companies. Independent "
        "expert consultations (Gerson Lehrman Group network).\n"
        "- Week 5-8: Investment Committee presentation, challenge session, and vote.\n"
        "Every investment requires unanimous Investment Committee approval (Chen, Martinez, "
        "Park). Each IC presentation includes a dedicated 'bear case advocate' who argues "
        "against the investment."
    )

    pdf.add_question(
        "8.11",
        "Provide details on the Firm's internal decision making and approval process.",
    )
    pdf.add_answer(
        "The Investment Committee consists of three members: Robert Chen (CIO, Chair), "
        "Sarah Martinez (Senior PM), and David Park (Senior Analyst). The IC meets weekly "
        "to review the portfolio and pipeline. New investment decisions require unanimous "
        "approval following a formal presentation by the sponsoring analyst. Each presentation "
        "includes: (1) investment thesis summary, (2) detailed financial model with scenario "
        "analysis, (3) competitive analysis, (4) management assessment, (5) ESG risk "
        "assessment, (6) risk factors and mitigants, and (7) a bear case presentation by a "
        "designated devil's advocate. Position sizing is determined by the CIO based on "
        "conviction level and portfolio construction considerations."
    )

    pdf.add_question(
        "8.17",
        "Describe the Firm's strategy for exiting investments.",
    )
    pdf.add_answer(
        "Average holding period: 3.2 years (range: 6 months to 8+ years). Exit triggers "
        "include:\n"
        "1. Thesis completion -- stock reaches our estimate of fair value (historically "
        "60% of exits)\n"
        "2. Better opportunity -- position replaced by a higher-conviction idea (25% of "
        "exits)\n"
        "3. Thesis invalidation -- fundamental deterioration or change in competitive "
        "dynamics (15% of exits)\n"
        "All exits require IC discussion and approval. We maintain sell discipline even when "
        "positions are performing well -- if a stock reaches fair value, we reduce or "
        "eliminate the position regardless of momentum. For positions where our thesis has "
        "been invalidated, we aim to exit within 30-60 days, accepting short-term liquidity "
        "costs to protect capital."
    )

    # =========================================================================
    # SECTION 9: FUNDRAISING (Team in ILPA)
    # =========================================================================
    pdf.add_section_header("9", "Team")

    pdf.add_question(
        "9.1",
        "Provide the shared work history of the Firm's Principals.",
    )
    pdf.add_answer(
        "Robert Chen and Sarah Martinez worked together at T. Rowe Price from 2004 to 2008, "
        "where Ms. Martinez was an analyst on Mr. Chen's Small-Cap Value team. When Mr. Chen "
        "founded Granite Peak Capital in 2008, Ms. Martinez was among the first hires, "
        "joining in January 2010 after completing her MBA at Wharton. David Park joined in "
        "2011 from Citadel's fundamental equity team, where he had been an analyst for five "
        "years. While Park did not overlap with Chen and Martinez at T. Rowe Price, Chen was "
        "familiar with Park's work through industry conferences and publications. The three "
        "partners have worked together continuously at Granite Peak for over 13 years."
    )

    pdf.add_question(
        "9.4",
        "Describe the Firm's remote work policy.",
    )
    pdf.add_answer(
        "The firm adopted a hybrid work policy in 2021, updated in 2023. Investment "
        "professionals are expected to be in the office a minimum of four days per week. "
        "Operations and support staff are expected in the office a minimum of three days per "
        "week. All employees have firm-issued laptops with VPN access, MFA-enabled "
        "authentication, and encrypted hard drives. Investment Committee meetings, team "
        "research discussions, and client meetings are conducted in-person whenever possible. "
        "The firm provides a $2,500 annual stipend for home office equipment."
    )

    pdf.add_question(
        "9.5",
        "Describe the Firm's process and policy for recruiting and hiring staff.",
    )
    pdf.add_answer(
        "Recruiting is managed by the HR Manager in coordination with department heads. For "
        "investment professionals, we recruit from top MBA programs (Wharton, Columbia, "
        "Chicago Booth, Kellogg), the CFA program, and through referrals from our industry "
        "network. Research Associates are typically recruited from top undergraduate programs "
        "with demonstrated interest in value investing. All candidates undergo a structured "
        "interview process including: (1) initial screening call, (2) case study/stock pitch, "
        "(3) panel interview with investment team members, (4) meeting with partners, and "
        "(5) reference checks (minimum 3 professional references). All offers are contingent "
        "on background checks conducted by Sterling Check."
    )

    pdf.add_question(
        "9.7",
        "Describe other benefits Team Members receive.",
    )
    pdf.add_answer(
        "Benefits include: 401(k) with 6% employer match (immediate vesting); comprehensive "
        "medical, dental, and vision insurance (firm covers 90% of premiums for employees "
        "and dependents); life insurance (2x base salary); long-term disability insurance; "
        "20 days paid time off plus 10 holidays; 16 weeks paid parental leave (gender-neutral); "
        "tuition reimbursement up to $15,000 per year for job-related education; CFA exam "
        "fee reimbursement; gym membership subsidy; wellness program; Employee Assistance "
        "Program; and commuter benefits."
    )

    # =========================================================================
    # SECTION 10: ALIGNMENT OF INTERESTS
    # =========================================================================
    pdf.add_section_header("10", "Alignment of Interests")

    pdf.add_question(
        "10.1",
        "Describe the compensation structure for all Team Members.",
    )
    pdf.add_answer(
        "Compensation consists of three components:\n"
        "1. Base salary: Competitive with market; reviewed annually.\n"
        "2. Annual bonus: 0-200% of base salary, determined by a combination of firm "
        "performance (60% weight) and individual contribution (40% weight). All investment "
        "professionals are required to invest a minimum of 50% of their after-tax annual "
        "bonus in the fund, creating direct alignment with LP interests.\n"
        "3. Carried interest: Partners participate in 15% performance fee allocation. "
        "Chen: 55% of carry pool; Martinez: 25%; Park: 15%; Senior analyst pool: 5%. "
        "Carry vests over 4 years with a 1-year cliff.\n\n"
        "Non-investment professionals receive base salary plus annual discretionary bonus "
        "(0-100% of base) based on firm performance and individual contribution."
    )

    pdf.add_question(
        "10.5",
        "Describe how the General Partner's contribution for investments is allocated.",
    )
    pdf.add_answer(
        "The GP commitment to Fund IV is $75 million (3% of target fund size). This "
        "commitment is funded entirely with cash -- no management fee waivers or leverage "
        "is used. The GP commitment is allocated among the partners as follows: Robert Chen "
        "$41.25M (55%), Sarah Martinez $15.0M (20%), David Park $11.25M (15%), and the "
        "employee equity pool $7.5M (10%). In addition to the GP commitment, partners invest "
        "additional personal capital alongside the fund. Total insider capital (GP + personal) "
        "represents approximately $95 million, demonstrating strong alignment."
    )

    pdf.add_question(
        "10.6",
        "Will all the Firm's Principals and/or affiliates invest in the Fund?",
    )
    pdf.add_answer(
        "Yes. All three partners have made substantial personal commitments to Fund IV in "
        "addition to their share of the GP commitment. Senior analysts and other investment "
        "professionals are encouraged (but not required) to invest personally in the fund. "
        "As of December 31, 2025, 85% of investment professionals have made personal "
        "investments in Fund IV."
    )

    pdf.add_question(
        "10.8",
        "Describe how the General Partner's contribution will be financed.",
    )
    pdf.add_answer(
        "The GP commitment of $75 million is financed entirely with cash from the partners' "
        "personal resources and the management company's retained earnings. No portion of "
        "the GP commitment is financed through leverage, management fee waivers, deferred "
        "compensation, or assets from other funds. No commitments from the GP or any "
        "principal are leveraged or loaned."
    )

    pdf.add_question(
        "10.16",
        "Were there any carry clawback situations in any of the Firm's prior funds?",
    )
    pdf.add_answer(
        "No. No carry clawback has occurred in any of the firm's prior funds. All funds "
        "have generated positive net returns for LPs, and carried interest distributions "
        "have been well-supported by realized gains. The fund includes a standard clawback "
        "provision requiring the GP to return excess carried interest upon final liquidation "
        "if aggregate LP returns fall below the 6% preferred return hurdle."
    )

    # =========================================================================
    # SECTION 11: MARKET ENVIRONMENT
    # =========================================================================
    pdf.add_section_header("11", "Market Environment")

    pdf.add_question(
        "11.1",
        "Describe the markets in which the Fund will operate and provide an overview "
        "of the current opportunities.",
    )
    pdf.add_answer(
        "The U.S. small/mid-cap value equity market represents one of the most attractive "
        "segments for active fundamental investors. As of year-end 2025, small-cap value "
        "stocks trade at a historically wide discount to large-cap growth on both P/E and "
        "EV/EBITDA metrics. The Russell 2000 Value Index trades at approximately 12.5x "
        "forward earnings versus 22x for the S&P 500. This valuation dispersion, combined "
        "with lower analyst coverage (average 4 analysts per company vs. 20+ for large caps), "
        "creates a rich environment for our bottom-up, research-intensive approach. We see "
        "particular opportunity in industrials benefiting from reshoring trends, regional "
        "banks consolidating after the 2023 stress, and healthcare services companies at "
        "cyclical troughs."
    )

    pdf.add_question(
        "11.5",
        "Describe and list the Fund's direct competitors.",
    )
    pdf.add_answer(
        "Our primary competitors in the institutional U.S. small/mid-cap value space include: "
        "Dimensional Fund Advisors (systematic value), LSV Asset Management (quantitative "
        "value), Hotchkis & Wiley (concentrated value), Royce Investment Partners (small-cap "
        "specialists), and Ariel Investments (patient value). Our differentiation lies in "
        "our concentrated portfolio (25-35 positions vs. 100+ for many peers), long holding "
        "period (3+ years), and deep fundamental research process with direct management "
        "engagement. Our track record of consistent downside protection (72% downside capture "
        "ratio) distinguishes us from both systematic and more aggressive fundamental managers."
    )

    # =========================================================================
    # SECTION 12: FUND TERMS
    # =========================================================================
    pdf.add_section_header("12", "Fund Terms")

    pdf.add_question(
        "12.1",
        "Provide information on the fee structures for each vehicle.",
    )
    pdf.add_answer(
        "Fee structure comparison across fund generations:"
    )
    pdf.add_table(
        ["", "Fund II", "Fund III", "Fund IV"],
        [
            ["Mgmt Fee (Tier 1)", "100 bps", "90 bps", "85 bps"],
            ["Mgmt Fee (Tier 2)", "90 bps", "80 bps", "75 bps"],
            ["Mgmt Fee (Tier 3)", "80 bps", "70 bps", "65 bps"],
            ["Tier 1 Threshold", "<$100M", "<$200M", "<$250M"],
            ["Tier 2 Threshold", "$100-250M", "$200-400M", "$250-500M"],
            ["Tier 3 Threshold", ">$250M", ">$400M", ">$500M"],
            ["Performance Fee", "18%", "17%", "15%"],
            ["Hurdle Rate", "5%", "6%", "6%"],
            ["High Water Mark", "Yes", "Yes", "Yes"],
        ],
        col_widths=[50, 46.7, 46.7, 46.6],
    )
    pdf.add_answer(
        "The trend reflects our commitment to reducing fees as AUM grows. The blended "
        "effective management fee for a $500M commitment in Fund IV is approximately 77 bps. "
        "Management fees are calculated on net asset value, accrued monthly, and paid "
        "quarterly in arrears."
    )

    pdf.add_question(
        "12.4",
        "Have any prospective investors received side agreements or rights?",
    )
    pdf.add_answer(
        "Yes. Side letters have been executed with 8 of 47 limited partners, primarily "
        "addressing: (1) most-favored-nation fee provisions, (2) enhanced reporting "
        "requirements for certain public pension plans, (3) tax-related structuring for "
        "certain non-U.S. investors, and (4) ERISA representations. No side letter provides "
        "preferential economic terms beyond the standard fee schedule tiers. All material "
        "side letter terms are subject to MFN provisions and are available to all LPs upon "
        "request."
    )

    pdf.add_question(
        "12.9",
        "Describe the methodology the Firm uses for the Fund's distribution waterfall.",
    )
    pdf.add_answer(
        "Fund IV uses a whole-fund (European) waterfall with the following tiers:\n"
        "1. Return of capital: 100% of distributions to LPs until all contributed capital "
        "is returned.\n"
        "2. Preferred return: 100% to LPs until a 6% annualized preferred return is achieved "
        "on all contributed capital.\n"
        "3. GP catch-up: 100% to GP until GP has received 15% of total profits.\n"
        "4. Carried interest split: 85% to LPs / 15% to GP.\n"
        "Distributions are made quarterly based on realized gains and income. Unrealized "
        "appreciation is not distributed."
    )

    pdf.add_question(
        "12.13",
        "Describe the Fund's clawback provision.",
    )
    pdf.add_answer(
        "The GP is subject to a clawback obligation on a several basis (not joint). Upon "
        "final fund liquidation, if aggregate LP distributions are less than contributed "
        "capital plus the 6% preferred return, the GP is required to return excess carry "
        "distributions (net of taxes actually paid, at a maximum assumed rate of 45%). "
        "20% of all carry distributions are held in an escrow account maintained by the "
        "fund's administrator (State Street) as security for the clawback obligation. The "
        "clawback is tested annually and at final liquidation."
    )

    pdf.add_question(
        "12.18",
        "State the Fund's management fees and other amounts payable to the General Partner.",
    )
    pdf.add_answer(
        "Management fee: 65-85 bps on NAV (tiered as described in 12.1), calculated monthly, "
        "paid quarterly in arrears. Performance fee: 15% of net profits above a 6% annualized "
        "hurdle rate, subject to a high-water mark, calculated and crystallized annually. "
        "No transaction fees, monitoring fees, or other portfolio company-level fees are "
        "charged. Broken deal expenses are borne by the management company, not the fund. "
        "Organizational expenses are capped at $1.5M (actual: $1.2M)."
    )

    pdf.add_question(
        "12.20",
        "State the Fund's provisions regarding the transferability of partnership interests.",
    )
    pdf.add_answer(
        "LP interests may be transferred with the prior written consent of the GP, which "
        "shall not be unreasonably withheld. Transfers are subject to: (1) minimum transfer "
        "amount of $5 million, (2) compliance with applicable securities laws, (3) tax and "
        "regulatory opinion satisfactory to the GP, and (4) payment of a $25,000 transfer "
        "fee to cover administrative and legal costs. The GP has a right of first refusal "
        "on any proposed transfer. No transfers are permitted during the first 12 months "
        "following an LP's subscription."
    )

    # =========================================================================
    # SECTION 13: FIRM GOVERNANCE / RISK / COMPLIANCE
    # =========================================================================
    pdf.add_section_header("13", "Firm Governance / Risk / Compliance")

    pdf.add_question(
        "13.3",
        "Describe the Firm's compliance policies.",
    )
    pdf.add_answer(
        "The compliance program is overseen by CCO Jennifer Walsh, who has 18 years of "
        "compliance experience and reports directly to the Managing Partner with a dotted "
        "line to the independent advisory board. Key compliance program elements include:\n"
        "- Pre-clearance requirement for all personal securities transactions by employees\n"
        "- 30-day holding period for personal equity investments\n"
        "- Quarterly gifts and entertainment reporting (de minimis threshold: $250)\n"
        "- Semi-annual political contribution attestations\n"
        "- Annual compliance training for all employees (4 hours minimum)\n"
        "- Quarterly compliance testing program covering personal trading, information "
        "barriers, and expense reporting\n"
        "- Annual compliance program review by external counsel (Dechert LLP)\n"
        "- Whistleblower hotline operated by an independent third party (EthicsPoint)"
    )

    pdf.add_question(
        "13.4",
        "Describe the Firm's Conflicts of Interest policy.",
    )
    pdf.add_answer(
        "The firm maintains a comprehensive Conflicts of Interest policy that identifies, "
        "manages, and discloses potential conflicts. Key provisions include: (1) All personal "
        "trading by employees requires pre-clearance and is monitored by the CCO; (2) No "
        "employee may invest personally in any company under active consideration by the "
        "fund; (3) Allocation of investment opportunities across funds and accounts follows "
        "a written allocation policy (pro rata based on available capital and suitability); "
        "(4) Related-party transactions require LPAC review and approval; (5) Side-by-side "
        "management of SMA accounts follows the same allocation procedures. No material "
        "conflicts have been identified in the past five years."
    )

    pdf.add_question(
        "13.11",
        "Describe the role of compliance staff in the Firm.",
    )
    pdf.add_answer(
        "The compliance team consists of the CCO (Jennifer Walsh) and two compliance "
        "analysts. The CCO reports directly to the Managing Partner and has independent "
        "access to the firm's advisory board. Key responsibilities include: policy "
        "development and maintenance, employee trading surveillance, regulatory filings "
        "(Form ADV, Form PF, 13F, 13D/G), examination preparation, compliance testing, "
        "training, and incident management. The team uses ComplySci for personal trading "
        "monitoring, ACA ComplianceAlpha for regulatory filings, and Bloomberg Vault for "
        "electronic communications surveillance."
    )

    pdf.add_question(
        "13.13",
        "Describe the Firm's approach to risk management.",
    )
    pdf.add_answer(
        "Risk management is integrated into the investment process at every stage. We employ "
        "a three-lines-of-defense model:\n"
        "1. Investment team (first line): Position-level risk assessment during due diligence, "
        "including scenario analysis and stress testing. Each investment memo includes a "
        "dedicated risk section.\n"
        "2. Risk committee (second line): The CIO, COO, and CCO meet weekly to review "
        "portfolio-level risk metrics including concentration, sector exposure, factor "
        "exposures, liquidity, and drawdown. Risk limits are monitored daily by the "
        "operations team.\n"
        "3. External risk consultant (third line): Albourne Partners provides quarterly "
        "independent risk assessments, including factor attribution, stress testing, and "
        "peer comparison.\n\n"
        "Enterprise risks (operational, cyber, regulatory, business continuity) are managed "
        "by the COO and reviewed by the advisory board quarterly."
    )

    pdf.add_question(
        "13.17",
        "Is the Firm a registered investment advisor with the SEC?",
    )
    pdf.add_answer(
        "Yes. Granite Peak Capital LLC is registered with the SEC as an investment adviser "
        "under the Investment Advisers Act of 1940. SEC File Number: 801-78234. CRD Number: "
        "287456. The firm has been registered since its inception in 2008. The firm also "
        "files Form PF as a large private fund adviser. The firm is not registered as a "
        "broker-dealer."
    )

    pdf.add_question(
        "13.19",
        "Has a Regulatory Exam Deficiency Letter been issued to the Firm?",
    )
    pdf.add_answer(
        "No. The firm has undergone two SEC examinations (2016 and 2022). Neither examination "
        "resulted in a deficiency letter or any findings. The 2022 examination focused on "
        "fees and expenses, valuation practices, and conflicts of interest, and concluded "
        "without any findings or recommendations."
    )

    pdf.add_question(
        "13.29",
        "Describe the types of insurance coverage the Firm maintains.",
    )
    pdf.add_answer(
        "The firm maintains the following insurance coverage:\n"
        "- Errors & Omissions / Professional Liability: $25 million per occurrence / $50M "
        "aggregate (Chubb)\n"
        "- Directors & Officers: $15 million (AIG)\n"
        "- Fidelity Bond / Crime: $10 million (Travelers)\n"
        "- Cyber Liability: $10 million (Beazley)\n"
        "- General Commercial Liability: $5 million (Hartford)\n"
        "- Employment Practices Liability: $5 million (Chubb)\n"
        "No material claims have been made under any policy in the firm's history."
    )

    # =========================================================================
    # SECTION 14: TRACK RECORD
    # =========================================================================
    pdf.add_section_header("14", "Track Record")

    pdf.add_question(
        "14.1",
        "Have any of the portfolio companies within the Fund family ever filed for "
        "bankruptcy?",
    )
    pdf.add_answer(
        "No. No portfolio company held by any Granite Peak fund has filed for bankruptcy "
        "during the firm's holding period. We have experienced three positions across all "
        "funds that declined more than 50% from our cost basis, but all three were exited "
        "before any bankruptcy filing, and the aggregate loss on these three positions was "
        "approximately $45 million against cumulative fund profits exceeding $2.8 billion."
    )

    pdf.add_answer(
        "Fund performance summary (as of December 31, 2025):"
    )
    pdf.add_table(
        ["Fund", "Vintage", "Size", "Gross Ann.", "Net Ann.", "Benchmark"],
        [
            ["Value Fund I", "2008", "$380M", "18.2%", "15.8%", "12.1%"],
            ["Value Fund II", "2012", "$1.1B", "16.5%", "14.2%", "11.8%"],
            ["Value Fund III", "2017", "$2.1B", "14.8%", "12.6%", "9.4%"],
            ["Value Fund IV", "2022", "$1.8B", "17.1%", "14.9%", "10.2%"],
        ],
        col_widths=[38, 27, 27, 27, 27, 44],
    )

    pdf.add_answer(
        "Benchmark: Russell 2000 Value Index. All returns are annualized and reported as "
        "of December 31, 2025. Returns are audited by Ernst & Young LLP and are "
        "GIPS-compliant."
    )

    pdf.add_question(
        "14.5",
        "Provide 3-5 examples of investments with a TVPI below 1.0x in the "
        "predecessor fund.",
    )
    pdf.add_answer(
        "Fund III loss positions (TVPI < 1.0x):\n\n"
        "1. Horizon Specialty Chemicals (Industrials) -- Invested $65M, realized $38M "
        "(0.58x TVPI). Thesis: Specialty chemicals consolidator trading below replacement "
        "cost. What went wrong: A key customer (15% of revenue) terminated its contract "
        "following a product quality issue. Action taken: Engaged directly with management "
        "on remediation; ultimately exited when it became clear market share was permanently "
        "impaired. Lesson applied: Increased customer concentration threshold to 10% max.\n\n"
        "2. Pacific Coast Healthcare Services (Healthcare) -- Invested $48M, realized $34M "
        "(0.71x TVPI). Thesis: Regional hospital operator with strong market position. What "
        "went wrong: Unexpected CMS reimbursement rate changes and staffing cost inflation "
        "compressed margins. Action taken: Exited within 60 days of recognizing structural "
        "headwind. Lesson applied: Incorporated regulatory sensitivity scoring.\n\n"
        "3. DataBridge Solutions (Technology) -- Invested $42M, realized $35M (0.83x TVPI). "
        "Thesis: Legacy data integration company transitioning to cloud. What went wrong: "
        "Cloud transition slower than expected, and a larger competitor launched a competing "
        "product. Action taken: Reduced position as thesis timeline extended, exited "
        "completely when competitive dynamics deteriorated."
    )

    pdf.add_question(
        "14.6",
        "Describe the most appropriate benchmarks and compare LP returns.",
    )
    pdf.add_answer(
        "Primary benchmark: Russell 2000 Value Index. Secondary benchmark: Russell 2500 "
        "Value Index."
    )
    pdf.add_table(
        ["Period", "Fund IV (Net)", "R2000V", "R2500V", "Alpha vs R2000V"],
        [
            ["1 Year", "14.2%", "8.7%", "9.1%", "+5.5%"],
            ["3 Year (Ann.)", "12.8%", "7.9%", "8.3%", "+4.9%"],
            ["Since Inception", "14.9%", "10.2%", "10.8%", "+4.7%"],
        ],
        col_widths=[38, 38, 38, 38, 38],
    )

    pdf.add_answer(
        "Downside/upside capture analysis (all funds, since inception):\n"
        "- Downside capture ratio: 72% (i.e., captured only 72% of benchmark declines)\n"
        "- Upside capture ratio: 108%\n"
        "- Maximum drawdown Fund III: -22.8% vs. -31.2% benchmark (Q1 2020)\n"
        "- Maximum drawdown Fund IV: -11.4% vs. -14.5% benchmark (2022)\n"
        "- Average recovery period: 8.5 months"
    )

    # =========================================================================
    # SECTION 15: ACCOUNTING / VALUATION
    # =========================================================================
    pdf.add_section_header("15", "Accounting / Valuation")

    pdf.add_question(
        "15.1",
        "For the responsibilities associated with accounting, tax, fund administration "
        "and audit performed in-house, describe how these responsibilities are carried out.",
    )
    pdf.add_answer(
        "The firm's internal accounting and operations team is led by CFO Thomas Reeves "
        "(CPA, 16 years experience) and includes 4 accountants and 2 operations analysts. "
        "Internal responsibilities include: daily portfolio reconciliation, monthly NAV "
        "calculation (shadow), trade settlement and confirmation, cash management, expense "
        "accrual, and management fee calculations. The team uses Bloomberg AIM for portfolio "
        "management, Geneva (SS&C) for fund accounting, and Advent APX for portfolio reporting. "
        "All internal calculations are independently reconciled against the fund administrator's "
        "records on a monthly basis."
    )

    pdf.add_question(
        "15.2",
        "For the responsibilities performed by a third-party, provide details on the "
        "third-party providers.",
    )
    pdf.add_answer(
        "- Fund Administrator: State Street Fund Services (since Fund II, 2012). Provides "
        "official NAV calculation, investor reporting, capital activity processing, and "
        "regulatory reporting support.\n"
        "- Auditor: Ernst & Young LLP (since inception, 2008). Conducts annual financial "
        "statement audit for all funds and the management company.\n"
        "- Tax: PricewaterhouseCoopers LLP. Prepares K-1s and handles tax compliance.\n"
        "- Custodian: Bank of New York Mellon (since inception). Provides custody, trade "
        "settlement, and securities lending (the fund does not engage in securities lending)."
    )

    pdf.add_question(
        "15.5",
        "Has the Firm's Valuation Policy remained significantly unchanged?",
    )
    pdf.add_answer(
        "Yes. The firm's Valuation Policy has not changed materially in the past five years. "
        "Since the fund invests exclusively in publicly traded equities, valuation is "
        "straightforward: positions are marked to market daily based on closing prices from "
        "the primary exchange. For the rare situations involving thinly traded securities, "
        "the policy prescribes a hierarchy: (1) last trade price if traded within the prior "
        "24 hours, (2) bid/ask midpoint if no recent trade, (3) independent pricing service "
        "(Bloomberg BVAL) for securities with insufficient market activity."
    )

    pdf.add_question(
        "15.6",
        "What accounting principles does the Fund operate under?",
    )
    pdf.add_answer(
        "The fund's financial statements are prepared in accordance with U.S. Generally "
        "Accepted Accounting Principles (U.S. GAAP). The fund follows ASC 820 (Fair Value "
        "Measurement) for investment valuation and ASC 946 (Financial Services -- Investment "
        "Companies) for fund-level financial reporting."
    )

    pdf.add_question(
        "15.10",
        "Is the Fund's audit firm independent from the Firm and Fund?",
    )
    pdf.add_answer(
        "Yes. Ernst & Young LLP is fully independent from the firm and fund. No family "
        "members of any firm employee are employed by EY. EY does not provide any consulting "
        "or advisory services to the firm -- the engagement is limited to audit and "
        "attestation services. EY's independence is confirmed annually in their engagement "
        "letter."
    )

    pdf.add_question(
        "15.14",
        "Does the Fund use an independent, unaffiliated Fund Administrator?",
    )
    pdf.add_answer(
        "Yes. State Street Fund Services serves as the fund's independent administrator. "
        "State Street calculates the official NAV, processes subscriptions and redemptions, "
        "prepares investor statements, and provides AML/KYC screening. The firm reconciles "
        "its internal (shadow) NAV against State Street's official NAV monthly; discrepancies "
        "are investigated and resolved within 3 business days. Historical discrepancies have "
        "been immaterial (less than 1 basis point)."
    )

    # =========================================================================
    # SECTION 16: REPORTING
    # =========================================================================
    pdf.add_section_header("16", "Reporting")

    pdf.add_question(
        "16.1",
        "Describe how reporting and investor relations responsibilities are carried out.",
    )
    pdf.add_answer(
        "The Investor Relations team (6 professionals under Christopher Yang) manages all LP "
        "reporting and communications. The team produces: (1) monthly estimated performance "
        "reports (distributed within 10 business days of month-end), (2) quarterly detailed "
        "reports including portfolio commentary, attribution analysis, market outlook, and "
        "capital account statements (distributed within 45 days of quarter-end), (3) annual "
        "audited financial statements (distributed within 90 days of year-end), (4) K-1 tax "
        "documents (distributed by March 15). Reports are delivered via the investor portal "
        "and email, in both PDF and Excel formats."
    )

    pdf.add_question(
        "16.3",
        "Describe the reporting provided to Limited Partners.",
    )
    pdf.add_answer(
        "LP reporting package includes:\n"
        "- Monthly: Estimated net returns, portfolio summary, top/bottom contributors\n"
        "- Quarterly: Detailed portfolio review (30-40 pages), capital account statement, "
        "attribution analysis by sector/position, risk metrics (volatility, Sharpe, "
        "drawdown, active share), fee disclosure, and CIO letter\n"
        "- Annually: Audited financial statements, GIPS-compliant performance report, "
        "annual review presentation, and K-1 tax documentation\n"
        "- Ad hoc: Material event notifications (within 1 business day), position "
        "concentration alerts, and custom reporting upon request\n"
        "All reports are available on the secure investor portal (IntraLinks) and via email. "
        "Quarterly conference calls are held within 30 days of quarter-end."
    )

    pdf.add_question(
        "16.5",
        "Will the Fund's standard reporting package include the majority of content found "
        "in the ILPA Reporting Best Practices?",
    )
    pdf.add_answer(
        "Yes. The fund's reporting is aligned with ILPA Reporting Best Practices, including "
        "the ILPA Reporting Template for fees, expenses, and carried interest, and the ILPA "
        "Standardized Capital Call and Distribution Template. We also comply with ILPA "
        "guidance on subscription line of credit reporting, providing IRR with and without "
        "the credit facility impact."
    )

    pdf.add_question(
        "16.10",
        "Does the Firm have an investor portal for LPs to access Fund information?",
    )
    pdf.add_answer(
        "Yes. The firm maintains a secure investor portal through IntraLinks (SS&C). The "
        "portal provides access to: quarterly reports, monthly performance estimates, capital "
        "account statements, K-1s, audited financials, legal documents (LPA, subscription "
        "agreements, side letters), DDQ materials, and event invitations. Access is secured "
        "via multi-factor authentication and role-based permissions. Portal activity is "
        "logged and monitored. Documents are available in PDF, Excel, and XML formats."
    )

    pdf.add_question(
        "16.12",
        "Does the Firm claim compliance with the Global Investment Performance Standards "
        "(GIPS)?",
    )
    pdf.add_answer(
        "Yes. Granite Peak Capital has claimed GIPS compliance since 2010. The firm has been "
        "independently verified by ACA Performance Services (formerly Ashland Partners) for "
        "all periods since 2010. The most recent verification covers the period through "
        "December 31, 2025. GIPS-compliant performance presentations are available for all "
        "fund composites and are included in the annual reporting package."
    )

    # =========================================================================
    # SECTION 17: LEGAL
    # =========================================================================
    pdf.add_section_header("17", "Legal")

    pdf.add_question(
        "17.1",
        "Have there been any criminal, civil or administrative proceedings or investigations "
        "brought against the Firm?",
    )
    pdf.add_answer(
        "No. Neither the firm, its affiliated entities, nor any current or former employee "
        "(while employed by the firm) has been the subject of any criminal, civil, or "
        "administrative proceedings or investigations."
    )

    pdf.add_question(
        "17.2",
        "Have there been any litigation or other legal proceedings against the Firm?",
    )
    pdf.add_answer(
        "No. The firm has not been involved in any litigation or other legal proceedings "
        "(including civil proceedings) as either plaintiff or defendant. This clean record "
        "extends to all affiliated entities and all current and former employees during their "
        "tenure at the firm."
    )

    pdf.add_question(
        "17.3",
        "Have there been any investigations by an industry regulatory body?",
    )
    pdf.add_answer(
        "No. Beyond routine SEC examinations (2016 and 2022, both concluded without findings "
        "-- see Section 13.19), the firm has not been subject to any investigation by the "
        "SEC, FINRA, any state securities regulator, or any self-regulatory organization."
    )

    pdf.add_question(
        "17.4",
        "Are there any pending or ongoing litigation, investigations or other proceedings?",
    )
    pdf.add_answer(
        "No. There are no pending or ongoing litigation, investigations, or other "
        "administrative or legal proceedings involving the firm, its affiliated entities, "
        "or any current or former employee."
    )

    pdf.add_question(
        "17.7",
        "Will the Firm have a fiduciary obligation to act in the best interests of the "
        "Fund and its investors?",
    )
    pdf.add_answer(
        "Yes. Granite Peak Capital acknowledges and embraces its fiduciary duty to the fund "
        "and its investors. As a registered investment adviser under the Investment Advisers "
        "Act of 1940, the firm owes duties of care and loyalty to its advisory clients. The "
        "firm's fiduciary standard is embedded in the fund's LPA and is not limited or waived "
        "by any contractual provision."
    )

    pdf.add_question(
        "17.9",
        "Describe the Firm's view on its fiduciary duty.",
    )
    pdf.add_answer(
        "We view fiduciary duty as the cornerstone of our relationship with investors. Our "
        "fiduciary obligations include: (1) duty of care -- making investment decisions with "
        "the skill, prudence, and diligence that a professional investment manager would "
        "exercise; (2) duty of loyalty -- placing LP interests ahead of our own; (3) duty "
        "to disclose -- providing full and fair disclosure of all material facts and conflicts "
        "of interest. The contractual standard of care in the LPA is consistent with the "
        "regulatory fiduciary standard imposed by the SEC. There is no discrepancy between "
        "our contractual and regulatory obligations."
    )

    pdf.add_question(
        "17.11",
        "For the legal responsibilities performed in-house, describe how these are "
        "carried out.",
    )
    pdf.add_answer(
        "The firm does not have a dedicated General Counsel. Legal oversight is provided by "
        "the CCO (Jennifer Walsh, JD) for compliance and regulatory matters, and by external "
        "counsel for transactional, fund formation, and litigation matters. External legal "
        "advisors include: Dechert LLP (fund formation, regulatory, compliance review), "
        "Sidley Austin LLP (tax), and Fisher Phillips LLP (employment law). The firm's annual "
        "legal budget is approximately $1.2 million, with the majority related to fund "
        "formation and ongoing regulatory compliance."
    )

    # =========================================================================
    # SECTION 18: DATA SECURITY / TECHNOLOGY
    # =========================================================================
    pdf.add_section_header("18", "Data Security / Technology / Third-Party(s)")

    pdf.add_question(
        "18.1",
        "Describe the development/implementation of and/or any significant changes to the "
        "Firm's cyber/information security policy within the last five years.",
    )
    pdf.add_answer(
        "The firm's cyber/information security policy was originally adopted in 2015 and has "
        "undergone significant enhancements:\n"
        "- 2020: Implemented zero-trust architecture and enhanced VPN infrastructure to "
        "support remote work during COVID-19.\n"
        "- 2021: Achieved SOC 2 Type II certification (renewed annually since).\n"
        "- 2022: Deployed advanced endpoint detection and response (CrowdStrike Falcon). "
        "Implemented Security Information and Event Management (SIEM) platform.\n"
        "- 2023: Enhanced identity and access management with privileged access management "
        "(PAM) solution. Updated incident response plan.\n"
        "- 2024: Completed alignment with NIST Cybersecurity Framework 2.0. Added AI-based "
        "email threat detection.\n"
        "The policy is approved by the CTO and Managing Partner, reviewed quarterly by the "
        "risk committee, and updated at least annually."
    )

    pdf.add_question(
        "18.4",
        "Does the Firm have an annual independent, third-party audit of the Firm's "
        "cyber/information security policy and controls?",
    )
    pdf.add_answer(
        "Yes. The firm undergoes an annual SOC 2 Type II audit conducted by Coalfire Systems, "
        "covering security, availability, and confidentiality trust service criteria. The "
        "most recent audit (October 2025) resulted in an unqualified opinion with no "
        "exceptions noted. Additionally, CrowdStrike Services conducts annual penetration "
        "testing (both external and internal), with results reviewed by the CTO and risk "
        "committee."
    )

    pdf.add_question(
        "18.5",
        "Has the Firm or any of its portfolio companies had any cyber breaches in the "
        "last five years?",
    )
    pdf.add_answer(
        "No. The firm has not experienced any cyber breaches, data breaches, or material "
        "cybersecurity incidents in its history. The firm conducts monthly phishing simulations; "
        "the current click rate is below 2% (industry average: 8-12%). No portfolio companies "
        "held by the fund have experienced material cyber breaches during our holding period."
    )

    pdf.add_question(
        "18.6",
        "Does the Firm carry out penetration testing?",
    )
    pdf.add_answer(
        "Yes. Annual penetration testing is conducted by CrowdStrike Services. Testing "
        "includes external network penetration testing, internal network penetration testing, "
        "web application testing, and social engineering (phishing) campaigns. The most recent "
        "penetration test (September 2025) identified zero critical findings and two low-risk "
        "findings, both remediated within 30 days."
    )

    pdf.add_question(
        "18.8",
        "Does the Firm carry out training designed at preventing cyber breaches?",
    )
    pdf.add_answer(
        "Yes. All employees complete mandatory cybersecurity awareness training upon hire "
        "and annually thereafter. Training covers phishing identification, social engineering, "
        "password hygiene, data classification and handling, incident reporting procedures, "
        "and secure remote work practices. The training is provided by KnowBe4 and includes "
        "monthly phishing simulations. Employees who fail phishing simulations receive "
        "additional targeted training within 48 hours. The firm also conducts tabletop "
        "incident response exercises twice per year."
    )

    pdf.add_question(
        "18.9",
        "Describe the Firm's Business Continuity Plan (BCP).",
    )
    pdf.add_answer(
        "The BCP was originally developed in 2009 and most recently updated in November 2025. "
        "Key elements include: (1) All critical systems are replicated to a secondary data "
        "center (AWS us-east-1 and us-west-2 regions); (2) Recovery Time Objective (RTO) of "
        "4 hours for critical systems; (3) Recovery Point Objective (RPO) of 1 hour; "
        "(4) Remote work capability for 100% of staff tested quarterly; (5) Designated "
        "backup site at a WeWork facility in Denver; (6) Crisis communication plan including "
        "employee notification tree, LP communication templates, and regulatory notification "
        "procedures. The BCP is tested semi-annually, most recently in October 2025."
    )

    pdf.add_question(
        "18.15",
        "Is sensitive data encrypted -- stored and in transit?",
    )
    pdf.add_answer(
        "Yes. All data is encrypted at rest using AES-256 encryption and in transit using "
        "TLS 1.3. All endpoints (laptops, mobile devices) use full-disk encryption. Cloud "
        "storage (AWS S3, Microsoft 365) is encrypted using customer-managed encryption keys. "
        "Multi-factor authentication is required for all system access. USB storage devices "
        "are disabled on all firm-managed endpoints."
    )

    pdf.add_question(
        "18.17",
        "For the IT responsibilities performed in-house, describe how these are carried out.",
    )
    pdf.add_answer(
        "The IT team is led by CTO Daniel Kim (18 years experience, formerly at Bloomberg LP) "
        "and includes 3 developers/systems administrators. In-house responsibilities include: "
        "infrastructure management (cloud and on-premises), application development and "
        "customization (portfolio analytics tools, internal dashboards), end-user support, "
        "security monitoring and incident response, vendor management, and technology strategy. "
        "Key technology partners include AWS (cloud infrastructure), Microsoft 365 (productivity "
        "suite), CrowdStrike (endpoint security), Palo Alto Networks (network security), "
        "and Bloomberg (market data and analytics)."
    )

    # =========================================================================
    # SECTION 19: SUSTAINABILITY & GOVERNANCE (ESG)
    # =========================================================================
    pdf.add_section_header("19", "Sustainability & Governance")

    pdf.add_question(
        "19.1.1",
        "Do you have a responsible investment policy?",
    )
    pdf.add_answer(
        "Yes. Granite Peak Capital adopted a formal Responsible Investment (RI) Policy in "
        "2019 when the firm became a PRI signatory. The policy was most recently updated in "
        "September 2025. It covers ESG integration in the investment process, active "
        "ownership and engagement, proxy voting, exclusions, and reporting. The policy has "
        "been fully implemented across all funds and accounts. It is reviewed annually by "
        "the CIO and CCO, with input from the ESG working group (3 senior analysts designated "
        "as ESG leads). A copy of the policy is available upon request and is posted on the "
        "firm's website."
    )

    pdf.add_question(
        "19.1.2",
        "What international standards, industry guidelines, or initiatives that promote "
        "responsible investment practices have you committed to?",
    )
    pdf.add_answer(
        "- UN Principles for Responsible Investment (PRI) -- Signatory since 2019. Most "
        "recent PRI Assessment: 4 stars (Strategy & Governance) and 4 stars (Listed Equity).\n"
        "- Task Force on Climate-related Financial Disclosures (TCFD) -- Supporter since 2021. "
        "TCFD-aligned reporting commenced in 2022.\n"
        "- SASB Standards (now part of ISSB) -- Used as a framework for identifying material "
        "ESG factors by sector.\n"
        "- CFA Institute Asset Manager Code of Professional Conduct -- Adopted since 2012.\n"
        "We do not currently participate in Climate Action 100+ or the Net Zero Asset "
        "Managers Initiative, though we monitor these developments and may consider future "
        "participation."
    )

    pdf.add_question(
        "19.1.3",
        "How are oversight and implementation responsibilities for ESG incorporation "
        "structured within your organization?",
    )
    pdf.add_answer(
        "ESG oversight: The CIO (Robert Chen) has ultimate responsibility for ESG integration "
        "in the investment process. An ESG Working Group of 3 senior analysts (led by Katherine "
        "Moore) coordinates ESG research, training, and reporting.\n\n"
        "Implementation: ESG factors are integrated directly into each analyst's fundamental "
        "research rather than managed through a separate ESG team. Every investment memo "
        "includes a dedicated ESG section addressing material environmental, social, and "
        "governance risks and opportunities. The ESG Working Group meets monthly to discuss "
        "emerging issues, share best practices, and review portfolio-level ESG metrics.\n\n"
        "The CCO provides oversight on ESG policy compliance and regulatory developments. "
        "The LPAC is briefed on ESG activities at each semi-annual meeting."
    )

    pdf.add_question(
        "19.1.5",
        "How do you equip your investment professionals to understand ESG risks and "
        "opportunities?",
    )
    pdf.add_answer(
        "All investment professionals receive annual ESG training (minimum 4 hours) covering: "
        "SASB materiality frameworks by sector, climate risk analysis (physical and transition), "
        "governance best practices, and case studies from our own portfolio. Two analysts have "
        "completed the CFA Certificate in ESG Investing. The firm provides access to ESG "
        "data through MSCI ESG Research and Sustainalytics. New hires undergo ESG onboarding "
        "that includes review of the RI Policy, portfolio ESG case studies, and a shadowing "
        "session with the ESG Working Group."
    )

    pdf.add_question(
        "19.3.1",
        "How do you conduct ESG materiality analysis for potential investments and due "
        "diligence on potentially material ESG risks and opportunities?",
    )
    pdf.add_answer(
        "ESG materiality analysis is integrated into our standard due diligence process:\n\n"
        "(i) Materiality assessment: We use the SASB Materiality Map to identify the ESG "
        "factors most relevant to each company's industry. For each material factor, we "
        "assess the company's exposure, management practices, and performance relative to "
        "peers using MSCI and Sustainalytics data, supplemented by our own analysis of "
        "company disclosures, CDP responses, and news/controversy screening.\n\n"
        "(ii) Due diligence process: During management meetings, we raise ESG topics directly "
        "-- including board composition, executive compensation alignment, environmental "
        "liabilities, supply chain practices, and data security. We review proxy statements "
        "for governance quality (board independence, director tenure, shareholder rights). "
        "For industrial companies, we assess environmental remediation liabilities and "
        "regulatory compliance history.\n\n"
        "Example: In 2024, we declined to invest in a chemicals company despite attractive "
        "valuation because our ESG due diligence revealed inadequate environmental controls "
        "at two facilities and a pattern of regulatory citations."
    )

    pdf.add_question(
        "19.4.5",
        "Do you monitor and track ESG key performance indicators for your investments?",
    )
    pdf.add_answer(
        "Yes. We track the following ESG KPIs at the portfolio level, reported quarterly to "
        "LPs:\n"
        "- Weighted average MSCI ESG Rating (current: A)\n"
        "- Weighted average carbon intensity (tCO2e/$M revenue) vs. benchmark\n"
        "- Board independence (average: 78% across portfolio)\n"
        "- Gender diversity on boards (average: 28%)\n"
        "- Controversies (MSCI flags -- currently no 'red flag' positions)\n"
        "- UN Global Compact compliance (100% of portfolio)\n\n"
        "At the individual company level, we track sector-specific KPIs aligned with SASB "
        "standards. These are monitored by the responsible analyst and reviewed by the ESG "
        "Working Group quarterly."
    )

    pdf.add_question(
        "19.5.1",
        "How do you report and evidence progress on ESG performance to Limited Partners?",
    )
    pdf.add_answer(
        "ESG reporting to LPs includes:\n"
        "- Quarterly: Portfolio-level ESG scorecard (carbon intensity, ESG rating distribution, "
        "controversy flags) included in the standard quarterly report.\n"
        "- Annually: Dedicated ESG section in the annual report (10-15 pages) covering "
        "ESG integration activities, engagement summary, proxy voting statistics, carbon "
        "footprint analysis, and case studies. The annual PRI Transparency Report is also "
        "made available.\n"
        "- Annual Investor Day: ESG is a standing agenda item, typically a 30-minute "
        "presentation by the ESG Working Group lead.\n"
        "- Ad hoc: Material ESG incidents (if any) are communicated within 1 business day.\n\n"
        "Sample ESG disclosures from Fund III's 2024 annual report are available upon request."
    )

    pdf.add_question(
        "19.6.1",
        "How do you measure and report the greenhouse gas emissions associated with "
        "your investments?",
    )
    pdf.add_answer(
        "We measure portfolio carbon footprint using the TCFD-recommended metrics:\n"
        "- Weighted Average Carbon Intensity (WACI): tCO2e per $M revenue, calculated using "
        "company-reported Scope 1 and Scope 2 emissions data (sourced from CDP and company "
        "filings) supplemented by MSCI estimated data where company reporting is unavailable.\n"
        "- Total Carbon Emissions: Portfolio's share of investee companies' Scope 1 + 2 "
        "emissions, allocated by enterprise value.\n\n"
        "As of December 31, 2025, Fund IV's WACI is approximately 95 tCO2e/$M revenue, "
        "which is 22% below the Russell 2000 Value Index benchmark (approximately 122 "
        "tCO2e/$M revenue). This is primarily driven by our underweight to utilities and "
        "energy, and preference for asset-light business models. Carbon data is reported "
        "quarterly and included in the annual TCFD-aligned disclosure."
    )

    pdf.add_question(
        "19.7.2",
        "How do you manage your management company's internal ESG risks and opportunities?",
    )
    pdf.add_answer(
        "Internally, the firm manages its own environmental and social footprint through: "
        "(1) Carbon neutrality -- the firm has been carbon neutral since 2022, offsetting "
        "its Scope 1 and 2 emissions through verified carbon credits; (2) Office sustainability "
        "-- LEED Gold certified Denver headquarters, renewable energy procurement, waste "
        "reduction program; (3) Employee well-being -- comprehensive benefits including "
        "16 weeks gender-neutral parental leave, mental health resources, flexible work "
        "arrangements; (4) Community engagement -- the Granite Peak Foundation contributes "
        "0.5% of management fee revenue annually to education and environmental nonprofits "
        "in Colorado; (5) Governance -- independent advisory board member, annual compliance "
        "review, transparent LP reporting."
    )

    # Generate the PDF
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_DIR / "granite-peak-capital-ilpa.pdf"
    pdf.output(str(output_path))
    print(f"Generated: {output_path} ({pdf.page_no()} pages)")


if __name__ == "__main__":
    generate_granite_peak_ilpa()
