# Development record

Development and verification: 24–25 November 2026. This record summarises the design changes, implementation checks and use of AI assistance.

## Existing evidence inspected

- The supplied A1 report defines the problem as informed email approval and distinguishing genuine risks from false alarms.
- Lab 2 supplies the sense/infer/do loop, draft preview, and approve/edit/cancel storyboards. Its secondary-user description is a design assumption, not verified participant feedback.
- Lab 3 is explicitly a Markdown simulation. Its problem case exposes ambiguous contacts and a sensitive attachment; its revised specification requires separate warnings and fresh checks after edits. Copies are retained in this folder with `prior_` prefixes.
- Lab 4 demonstrates evidence visibility and confirmation for a different teaching assistant. It was inspected for continuity; its course-answering, image and scheduling code is not represented as an email implementation or copied into this prototype.

## Stage 1 — Narrow and implement the interaction

Commit: `c928379` (initial prototype and 18 tests).

Scope decision: implement a small local prototype instead of connecting a real mail account. This develops the existing interaction while keeping personal data and external sending outside scope. Fixed fixture outputs simulate language understanding. A deliberately crude budget keyword rule makes uncertainty visible. Real controls enforce recipient selection, a restricted-file block and per-draft approval.

Check: 14 state-machine tests and four HTTP tests passed. They exercise normal approval, duplicate-send requests, missing/stale review, cancelling, blocking issues, correction invalidation, failure/retry, input constraints, separate sessions and cross-origin rejection.

## Stage 2 — Inspect actual browser behaviour and revise

Commit: see `git log --oneline` for the cancel/terminal-state fix immediately after the initial commit.

The first browser review exposed an interface defect: `render()` disabled Cancel while a request was busy, but the completion callback only restored Approve. Revision: update both controls from the same completion state. Reload and actual cancellation then showed `Cancelled. Nothing was sent.`

A second inconsistency appeared after the false-alarm send: the warning-based heading still said a decision was needed. Revision: make terminal state headings take priority over warning headings. Reload confirmed `Decision recorded`. The warning evidence remains visible as context for the completed action.

These functional checks identified implementation defects; user evaluation remains future work.

## Stage 3 — Trace evidence and describe limits

Three illustrated paths cover review/approval, blocking/recovery/cancel, and false-alarm correction/approval. The generic-message toggle changes only warning wording, not the enforcement gate. It is a demonstration comparison, not a completed experiment.

Architecture, the report and README identify what is implemented, simulated and planned. Automated records and browser screenshots are separate evidence. No scan accuracy, trust, decision-time or participant statistics were collected.

## Stage 4 — Put actual demonstrations in the report

The final report uses actual interface states for three primary examples, plus a supplementary failure/retry check. [Report demonstrations](REPORT_DEMONSTRATIONS.md) links the steps, original screenshots, DOM snapshots and report crops.

Seventeen interface states were replayed in a separate local session on 24 November 2026, with Codex assisting browser operation. The run covered preparation and approval; independent recipient and attachment blocks; edits and rechecking; cancellation; generic and specific warnings; one-time correction and its reset; tool failure; retry; and the unsaved-edit guard. The original evidence is in `../evidence/report-demo/`, with `observations.json` describing the observed actions and regions. These remain functional demonstrations with fictional data, not observations of recruited participants.

A third interface inconsistency was identified during this revision: changing the warning selector while draft edits were unapplied could leave the selector showing generic wording while the cards still displayed the detailed explanation. The revised handler restores the previous selector value, keeps approval blocked and asks the user to apply the draft changes first. Capture `16-unsaved-edit-guard` verifies that guard; `17-saved-edit-switch` verifies that switching works after applying the edit and rerunning checks. The existing approval and server validation requirements were retained.

The submission revision is identified by `a2-submission-final` in the [public repository](https://github.com/Tiamotjf/safety-check-assistant). The latest automated output is retained in `../evidence/automated-tests.txt`; browser evidence is recorded separately because it checks visible behaviour that the control tests do not establish.

## AI assistance

Codex assisted with Python and browser-interface implementation, test generation, diagrams, report drafting and browser walkthroughs. Its outputs were checked through 18 automated tests, recorded interface runs and reference verification. Checks led to fixes for cancellation, completed-state headings and the warning selector. The design follows the A1 review and Lab 2–3 specifications; the prototype uses scripted fixtures and simulated email delivery.
