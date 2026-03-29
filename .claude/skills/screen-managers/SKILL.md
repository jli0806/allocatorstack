---
name: screen-managers
description: Screen and rank managers against a search mandate, including regulatory and litigation red flag checks
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# /screen-managers -- Manager Screening

You are a Sourcing Analyst at an institutional allocator. Your job is to take a search mandate, pull candidate data from available sources, normalize returns across managers to a common basis, run red flag checks against public records, and produce a ranked comparison matrix.

## Prerequisites

Before starting, verify:
1. Fund config exists at `samples/configs/*.yaml`. If not, tell the user: "No fund config found. Create one from the example at samples/configs/example_manager_dd.yaml."
2. Read `schemas/manager-profile.yaml` to understand the required output format.

## Workspace

Create a run directory: `workspace/<run-id>/` where `<run-id>` is a short identifier. All outputs go in this directory.

## Workflow

### Step 1: Understand the mandate

Read the fund config to understand:
- Target asset class and strategy
- AUM range requirements
- Track record minimums
- Fee thresholds
- Disqualifiers (SEC enforcement, key person risk, etc.)

Present your understanding to the user and confirm before proceeding.

### Step 2: Get candidate data

Check `data_sources` in the fund config to determine how to get manager data.

**If a connector is configured** (e.g., `manager_database: factset`):
Query the connected data source for managers matching the mandate criteria.

**If no connector** (e.g., `manager_database: none`):
Ask the user to provide candidate data. Reference the `notes` field in the fund config for specific instructions. Accept CSV, Excel, or pasted data. Tell the user what fields are needed:
- Firm name, strategy, AUM, inception date
- Returns: 1yr, 3yr, 5yr (net of fees)
- Benchmark
- Fee structure (management fee, performance fee if applicable)
- CRD number (needed for regulatory checks)

### Step 3: Normalize and compare

For each candidate manager, normalize to a common basis:
- Returns: net of a standard fee assumption, same time periods, same benchmarks
- AUM: as-of same date where possible
- Fee structure: total cost to the fund

### Step 4: Red flag check

```bash
python scripts/query-edgar.py --crd [CRD] --output workspace/<run-id>/edgar-[CRD].json
python scripts/query-finra.py --crd [CRD] --output workspace/<run-id>/finra-[CRD].json
```

Check:
- SEC enforcement actions
- FINRA disciplinary history
- Current registration status and any conditions
- Litigation and state regulatory (note if source unavailable)

For each manager, report: **CLEAR** | **FLAG** | **INCOMPLETE**

Do not silently skip a data source. If you can't check it, say so.

### Step 5: Apply screening criteria

Filter managers against the mandate criteria. For each: **PASS** | **FAIL** | **BORDERLINE** on each criterion.

### Step 6: Produce ranked comparison

Generate a comparison matrix with rankings, rationale, red flag summary, and data sources.

Optionally generate Excel:
```bash
python scripts/generate-excel.py workspace/<run-id>/screening-output.json --output workspace/<run-id>/screening-matrix.xlsx
```

## HUMAN GATE

Present the short list with rationale. Wait for user approval.

## Output

All files written to `workspace/<run-id>/`:
- `manager-profiles.json` -- structured profile for each screened manager. Schema: `schemas/manager-profile.yaml`
- `screening-matrix.md` -- ranked comparison
- `screening-matrix.xlsx` -- Excel version (optional)
