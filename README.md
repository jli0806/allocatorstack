# Allocator AI

An open-source Python framework for AI agents in institutional asset allocation.

Built for public pension funds, endowments, and foundations. Runs entirely on-premises — no confidential data leaves your network.

## What It Does

Allocator AI automates the data-gathering and document-production work in investment front offices. v1 focuses on the **Manager Due Diligence** workflow:

- **DDQ Analysis** — Ingest completed Due Diligence Questionnaires (PDFs), extract answers into a structured schema, compare managers side-by-side
- **SEC Cross-Reference** — Check manager claims against SEC EDGAR ADV filings and FINRA BrokerCheck
- **IC Memo Drafting** — Generate first-draft Investment Committee memos with provenance links for every quantitative claim
- **Verification Gates** — Configurable checks between pipeline steps to catch missing data, implausible values, and cross-source discrepancies

Every agent output includes a provenance chain showing exactly where each data point came from.

## Quick Start

```bash
pip install allocator-ai
```

```python
from allocator_ai import Pipeline

pipeline = Pipeline.from_config("allocator_ai_config.yaml")
pipeline.run()
```

See `samples/configs/` for example configurations.

## Design Principles

1. **Agents draft, humans decide.** Every output is a draft for human review. No automated investment decisions.
2. **Show your work.** Every number traces back to its source (file, page, field).
3. **Fail loudly.** Missing data and implausible results are flagged, never silently passed.
4. **Bring your own data.** CSV adapter included. Commercial data integrations via the adapter interface.

## White Paper

For the full analysis of allocator front-office workflows and how AI agents fit, see [docs/white-paper.md](docs/white-paper.md).

## Status

v0.1.0 — Early development. Manager DD workflow in progress. SAA Review, Monitoring, and Board Reporting are stub interfaces.

## License

MIT
