# Report demonstrations

Functional walkthroughs recorded on 24 November 2026 using fictional data, with Codex assisting browser operation. Email delivery is simulated; no real email was sent.

The assignment requires two or three examples of use in the report, with user actions, system responses and relevant feedback or control. The updated report uses three primary examples and one supplementary failure/retry check. It need not show every control as a separate example.

## What was actually run

| Capture | User action | Visible result |
|---|---|---|
| 01-request | Open normal scenario | Request state, no draft yet |
| 02-normal-review | Prepare and inspect | Contact, file text and message visible; approval requires review |
| 03-normal-result | Review checkbox, then approve | Simulated result, locked draft |
| 04-risk-blocked | Load and prepare risk scenario | Two independent blocking issues |
| 05-contact-fixed | Select exact internal Alex and apply | Contact issue clears; restricted attachment still blocks approval |
| 06-risk-rechecked | Replace attachment; edit subject/body; apply | New version, fresh review required |
| 07-cancelled | Cancel | Draft closed; nothing sent |
| 08-false-alarm-detailed | Prepare public budget task | Public-sharing statement and specific advisory visible |
| 09-false-alarm-generic | Switch presentation | Generic wording, same control requirements |
| 10-one-time-correction | Return to detailed; enter reason; record correction | Decision limited to this draft; review still required |
| 11-false-alarm-result | Review, then approve | Simulated result |
| 12-correction-reset | Reload same scenario and prepare | Old correction cleared; new decision required |
| 13-failure-configured | Set next-call failure in normal scenario | Failure fixture enabled |
| 14-send-failed | Review and approve | Failed state; no success claimed; fresh review needed |
| 15-retry-success | Review again and approve | Retry records simulated success |
| 16-unsaved-edit-guard | Edit message without applying; try switching warning | Error prompt; selector returns to the actual displayed mode; approval blocked |
| 17-saved-edit-switch | Apply edit, then switch | Switching works after checks rerun |

Original full-page JPGs, DOM snapshots and observed panel coordinates are in `../evidence/report-demo/`. `observations.json` records the action and observed screenshot regions. Report crops in `figures/report-demo/` enlarge those regions without changing their text; `crop_manifest.json` links them to originals.

## Small correction during this revision

Code review identified that attempting a warning-mode change with unapplied draft edits could leave the dropdown and warning card inconsistent. The selector now returns to its previously displayed value until the changes are applied. Captures 16 and 17 verify this. The existing draft/approval enforcement was retained.

## Report editing

Course concepts are applied in the report without formal lecture citations. External research keeps Harvard author-date citations and an alphabetised reference list. The English text was revised for concrete descriptions of the actual implementation. AI assistance remains declared in the development record.

Project repository: https://github.com/Tiamotjf/safety-check-assistant. Submission version: `a2-submission-final`.
