 AI-Assisted Proposal Triage Design

 1. AI vs. rules

I would use AI to extract facts from proposal documents because contractors may describe the same information in different wording and layouts. The extraction output should be structured JSON and include a short evidence quote and page reference for each material fact. Missing or ambiguous facts must be returned as `null` or flagged; the model must not fill gaps with assumptions.

I would use ordinary application code for schema validation, mandatory eligibility checks, budget and timeline limits, weighted scoring, sorting, and audit logging. These operations need to be repeatable and testable. The AI does not choose the winner and cannot change weights or eligibility rules.

 2. Consistency and explainability

The admin configures criteria in an admin screen; the criteria are stored as data, not hard-coded. Each configuration has a version, effective date, weights, thresholds, and a record of who changed it. For each run, the system stores the criteria version, extraction output, evidence, validation warnings, rule results, subscores, weighted total, and ranking.

The scoring formula and tie-break rules are deterministic, so identical validated inputs and the same criteria version produce the same result. A reviewer can open each criterion to see the extracted value, source evidence, subscore, weight, and contribution to the total. The model version and prompt version are recorded because extraction may vary across model versions.

Scoring assumption: The brief provides the weights but does not define exact subscore bands. For this design, the prototype uses explicit example bands documented in its code. These bands are proposed assumptions, not rules supplied by the brief, and an administrator should approve them before operational use.

 3. Human in the loop

A reviewer confirms the selected category and checks unreadable files, missing evidence, conflicting statements, and low-confidence extraction. Any mandatory criterion marked unknown is sent for review rather than treated as a pass. The system can recommend a result, but a person makes the final award decision.

A reviewer may override an extracted fact, eligibility result, or recommendation only with a reason. The audit record should include the original value, corrected value, evidence, reviewer identity, timestamp, criteria version, scores before and after the change, and final decision. The system should preserve the original machine result rather than silently replacing it.

 4. Changing criteria

If an administrator changes a criterion or weight, the system creates a new criteria version instead of overwriting the version used for earlier evaluations. The UI should warn that weights must total 100% and that changes may affect existing rankings. The reviewer can explicitly rerun proposals against the new version. The new run is stored separately and linked to the previous run, preserving the original result and the reason for re-scoring.

 5. Risks and safeguards

- Incorrect extraction or OCR: Keep evidence quotes and page references; validate data types and ranges; flag unreadable or conflicting content for human review.
- Made-up facts: Require evidence for material fields. Missing evidence stays unknown; never infer that a licence, clearance, insurance, or warranty exists.
- Prompt injection inside a proposal: Treat uploaded documents as untrusted data. Ignore instructions in the document that attempt to control the model or ranking. Proposal C's embedded request to rank itself first must not affect its evaluation.
- Incorrect eligibility decisions: Implement mandatory checks as explicit rules. A bidder-held licence must be stated for the bidder itself; a proposed subcontractor is not automatically equivalent. Unknown mandatory evidence is flagged, not passed.
- Bias or inconsistent scoring: Use admin-defined criteria, published scoring bands, fixed weights, deterministic calculations, and test cases. Review outcomes for unexplained patterns.
- Manipulation or accidental edits: Restrict criteria editing to authorized admins, version all changes, and log overrides.
- Cost and latency: Extract only relevant fields, limit document size, cache extraction by file hash where appropriate, and send only exceptions for additional AI review.
- Misleading ranking: Show ranked, flagged, and ineligible groups separately. Do not assign a numeric score to a proposal that is ineligible or not safely scorable.

 Sample-set handling

Proposal B is ineligible under the stated bidder-held licence requirement because the proposal says its electrical subcontractor will be confirmed after award and does not confirm the bidder's own licence. Proposal D is flagged because its completion timeline is not provided, so compliance with the 16-week limit cannot be confirmed. Proposal C's embedded instruction is ignored. The numeric ordering of eligible proposals is illustrative because the brief does not specify exact subscore bands; the assumed bands must be visible and approved before real use.
