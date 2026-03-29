# Expected Output

These files show what `/analyze-ddq` produces when run on the 3 sample DDQs in `samples/ddqs/`.

**These are simplified examples.** The sample DDQs are 4-8 pages each with terse answers. A real institutional DDQ runs 40-80 pages with dense narrative, performance tables, legal disclosures, organizational charts, and appendices. The analysis on real data is correspondingly deeper -- more questions answered, more nuanced confidence scoring, more detailed flags, and follow-up questions grounded in actual fund policy and mandate requirements.

The purpose of these files is to show the output structure and demonstrate the pipeline's behavior across three profiles (clean, borderline, red flags) -- not to represent the depth of real allocator analysis.

## Files

| File | Description |
|------|-------------|
| `ddq-output-granite-peak.json` | Structured extraction: 48 answers, 19 gaps, 2 flags |
| `ddq-output-meridian-value.json` | Structured extraction: 27 answers, 41 gaps, 7 flags |
| `ddq-output-osprey-global.json` | Structured extraction: 37 answers, 35 gaps, 15 flags |
| `completeness-dashboard.md` | Coverage summary by manager and category |
| `comparison-matrix.md` | Side-by-side comparison on key dimensions |
| `comparison.json` | Machine-readable comparison (feeds into Excel generation) |
| `comparison.xlsx` | Excel comparison matrix with color-coded severity |
| `follow-up-questions.md` | Generated questions for manager meetings |
