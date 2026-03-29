# AllocatorStack

Claude Code skill pack for institutional asset allocator front-office operations. Each skill maps to a role in an investment office.

## Skills

### Manager Due Diligence Pipeline

Run these in order. Each skill produces JSON output that the next skill reads.

```
/screen-managers  -->  /prep-manager-meeting  -->  /analyze-ddq  -->  /draft-memo
```

1. `/screen-managers` -- Screen candidates against fund criteria + regulatory red flag checks. Produces `manager-profiles.json`.
2. `/prep-manager-meeting` -- Prepare agendas, talking points, reference packets for manager meetings.
3. `/analyze-ddq` -- Ingest DDQ PDFs, map to ILPA taxonomy, cross-reference against SEC ADV. Produces `ddq-output.json`.
4. `/draft-memo` -- Generate IC memo draft from structured data with provenance links. Requires `ddq-output.json`.

### Quarterly Monitoring (independent workflow)

5. `/monitor-adv` -- Diff ADV filings against prior snapshots, scan news + regulatory actions, flag exceptions.

### Additional Skills (v0.2)

- `/prep-company-meeting` -- Briefing packets for direct company meetings
- `/screen-holdings` -- Responsible investing + forensic accounting screening
- `/board-report` -- Board-ready reports with trustee summaries

## Workspace Convention

Each pipeline run creates a workspace directory:
```
workspace/<run-id>/
  inputs/              # DDQ PDFs placed here
  extracted/           # JSON output from extract-pdf.py
  manager-profiles.json  # from /screen-managers
  ddq-output.json      # from /analyze-ddq
  ic-memo-draft.md     # from /draft-memo
```

Skills read from and write to the workspace. A user can re-run any skill by invoking it with the same run-id. Intermediate outputs are preserved.

## Fund Configuration

Copy and customize `samples/configs/example_manager_dd.yaml` for your fund:
- Fund profile (type, AUM, asset class targets)
- Evaluation criteria (track record minimums, fee thresholds, disqualifiers)
- Data sources (which connectors are configured vs. user-provided)

## Helper Scripts

Four Python scripts handle what Claude can't do natively:
- `scripts/extract-pdf.py` -- PDF text extraction with page numbers (PyMuPDF)
- `scripts/query-edgar.py` -- SEC EDGAR / IAPD API queries
- `scripts/query-finra.py` -- FINRA BrokerCheck API queries
- `scripts/generate-excel.py` -- Excel comparison matrix generation

Install dependencies: `pip install pymupdf requests openpyxl`

## Schemas

- `schemas/ilpa_aima_v1.yaml` -- 162 ILPA DDQ questions across 9 categories
- `schemas/ddq-output.yaml` -- Output format of /analyze-ddq
- `schemas/manager-profile.yaml` -- Output format of /screen-managers

## Design Principles

1. **Agents draft, humans decide.** Every output is a draft for human review.
2. **Show your work.** Every number traces to its source with `[Source: file, page]` notation.
3. **Fail loudly.** Missing data and implausible results get flagged, never silently passed.
4. **Verification gates.** Human review between pipeline stages.

## Testing

```bash
pytest tests/
```

Sample DDQs for testing: `samples/ddqs/` (3 synthetic PDFs).
