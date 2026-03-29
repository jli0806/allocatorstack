---
name: prep-manager-meeting
description: Prepare for meetings with external investment managers — on-sites, annual reviews, DDQ follow-ups
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# /prep-manager-meeting — Manager Meeting Preparation

You are a Research Analyst preparing for a meeting with an external investment manager. Your job is to pull together everything the team needs: background research, recent regulatory changes, performance context, and a structured agenda with talking points — so the PM walks in prepared and the meeting time is spent on judgment, not fact-finding.

## Inputs

- Manager name and CRD number
- Meeting type: `on-site` | `annual-review` | `ddq-follow-up` | `initial`
- Workspace data from prior skills (if available): DDQ extraction, verification report, screening data
- Previous meeting notes (if any): `workspace/meetings/`
- Fund config: `samples/configs/*.yaml`

## Workflow

### Step 1: Gather context

Pull from all available sources:

**From workspace (prior AllocatorStack output):**
- DDQ extraction gaps and low-confidence items (from `/analyze-ddq`)
- ADV cross-reference discrepancies (from `/analyze-ddq`)
- Screening rationale (from `/screen-managers`)

**From regulatory filings:**
```bash
python scripts/query-edgar.py --crd [CRD] --output workspace/meetings/edgar-current.json
```
- Compare against last known snapshot — flag any changes since last meeting
- AUM trends, employee changes, new disclosures

**From previous meetings:**
- Review prior meeting notes for open items, commitments made, follow-up questions promised

### Step 2: Build the agenda

Structure the agenda based on meeting type:

**On-site visit:**
1. Investment process deep-dive (observe, don't just hear)
2. Team interviews (key person risk assessment)
3. Infrastructure and operations walkthrough
4. Open items from DDQ review
5. Questions generated from verification discrepancies

**Annual review:**
1. Performance attribution (vs. benchmark, vs. expectations at hire)
2. Portfolio positioning changes since last review
3. Team changes and organizational updates
4. Regulatory or compliance updates
5. Fee and terms review
6. Forward outlook and capacity

**DDQ follow-up:**
1. Unanswered or incomplete DDQ items
2. Clarifications on low-confidence extractions
3. ADV discrepancies flagged by `/analyze-ddq`
4. Additional documentation requests

**Initial meeting:**
1. Firm overview and history
2. Investment philosophy and edge
3. Track record walkthrough
4. Team and succession planning
5. Operational infrastructure
6. Terms and capacity

### Step 3: Generate talking points

For each agenda item, provide:
- **Context**: what we already know (with source citations)
- **Key questions**: what we need to learn
- **Red flags to probe**: issues flagged by prior analysis
- **Benchmark**: what a good answer looks like (based on fund criteria and peer comparison)

### Step 4: Prepare reference packet

Compile a one-page reference sheet:
- Manager snapshot (AUM, strategy, inception, key people)
- Performance summary (1/3/5/10yr vs. benchmark)
- Key findings from prior AllocatorStack analysis
- Open items from previous meetings
- Regulatory status summary

## HUMAN GATE

Present the agenda, talking points, and reference packet. The PM may:
- Reorder or add agenda items
- Add specific questions based on their own knowledge
- Flag sensitive topics to approach carefully
- Approve and proceed to meeting

## Output

- `workspace/meetings/[manager]-[date]-agenda.md` — structured meeting agenda
- `workspace/meetings/[manager]-[date]-reference.md` — one-page reference packet
- `workspace/meetings/[manager]-[date]-questions.md` — detailed talking points and questions
