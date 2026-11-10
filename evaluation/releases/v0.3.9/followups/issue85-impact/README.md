# N1 complete: documentary curation impact for model 0.3.2

This packet compares the 82 current catalog concepts with the 80 concepts in documentary review 0.1.0. It preserves the historical review and does not accept or publish a successor curation component.

[All 82 decisions](impact.csv) · [Source-bound data and controls](impact.json) · [Reproduction](analyze.py).

| Population | Result and next action |
|---|---|
| 17 reuse candidates | Direct authored fields, incident associations/inheritance and the two removed mixed-set contexts are unchanged. Verify documentary edition/locator and comparison scope before compatible reuse; this is not automatic equivalence. |
| 57 structural-context checks | Direct concept fields are unchanged, but association/inheritance or inherited mixed-set context requires confirmation. Keep existing source evidence; a context flag does not prove a defect or require a new literature review. |
| 6 authored/typing changes | Review RKM-C014, C015, C048, C049, C066 and X01. Only X01 changes its authored definition and identity basis; the other five change typing rationale. Review the effect on each external comparison. |
| 2 new concepts | Establish documentary dispositions for EvidenceUseRelator (C075) and EvidenceReferenceRole (C076). Explicitly unassessed/not applicable is permitted with a reason; do not invent an equivalent. |

79 of the original 80 definitions retain identical text. This is source accounting, not a semantic-correctness score. The separately indexed external anchor is outside this 82-concept catalog denominator.

Run `python evaluation/releases/v0.3.9/followups/issue85-impact/analyze.py` from the repository. Inputs are SHA-256 bound. Missing review rows, stale definition digests and incomplete subdomain allocation are rejected by three actual mutation controls. Two runs must reproduce JSON/CSV bytes.

Next: review the six changed records and two new records, confirm compatible reuse/context boundaries for the other 74, then qualify and publish the current curation component. #85 remains open until its own publication/readback gate. Exact normative crosswalks remain #78 and independent semantic acceptance remains #23.
