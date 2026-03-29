# Changelog

## v0.1.0 (2026-03-28)

First release. The core manager due diligence pipeline works end-to-end.

### Skills

- `/screen-managers` -- Screen candidates against fund criteria, normalize returns, run SEC/FINRA red flag checks, produce ranked comparison
- `/prep-manager-meeting` -- Prepare agendas, talking points, and reference packets for manager meetings (on-site, annual review, DDQ follow-up, initial)
- `/analyze-ddq` -- Ingest DDQ PDFs, extract structured answers mapped to ILPA taxonomy, compare across managers, flag gaps and outliers, produce comparison matrix
- `/draft-memo` -- Generate IC memo draft with provenance links on every data point
- `/monitor-adv` -- Quarterly monitoring: diff ADV filings, scan regulatory actions, flag exceptions by severity

Three additional skills defined for v0.2: `/prep-company-meeting`, `/screen-holdings`, `/board-report`.

### Data Layer

- ILPA/AIMA DDQ taxonomy with 150+ questions across 8 categories
- Schema contracts for pipeline handoffs (`ddq-output.yaml`, `manager-profile.yaml`)
- 3 synthetic sample DDQs for testing and demo (Granite Peak Capital, Meridian Value Partners, Osprey Global Advisors)
- Fund configuration system (YAML-based, customizable per fund)

### Helper Scripts

- `extract-pdf.py` -- PDF text extraction with page numbers, password-protected PDF detection, scanned image PDF warning
- `query-edgar.py` -- SEC EDGAR / IAPD API queries by CRD number or firm name
- `query-finra.py` -- FINRA BrokerCheck API queries
- `generate-excel.py` -- Formatted Excel comparison matrices with color-coded severity

### Testing

- 45 pytest tests covering all 4 helper scripts
- Mock API responses for SEC/FINRA (no real API calls in tests)
- Sample DDQ PDFs as test fixtures

### Demo

- `./demo` script extracts sample DDQs and shows the pipeline entry point
