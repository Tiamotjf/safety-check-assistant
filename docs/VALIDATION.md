# Validation

Operator: Codex, during authorised project preparation on 24 November 2026. Local loopback prototype only. No participants recruited and no email sent.

## Automated evidence

Run `python -m unittest discover -s tests -v`. The recorded console output is in `../evidence/automated-tests.txt`. All 18 tests passed when the record was generated. Test names identify the claim each check supports; HTTP tests run an isolated local server on an available port.

## Browser observations

| Path | Actions actually performed | Observed result | Screenshot |
|---|---|---|---|
| Normal | Prepare draft; inspect; check the review box; approve | Draft locked; `Simulated send recorded. No real email was sent.` | `normal-review.jpg`, `normal-result.jpg` |
| Two blocking issues | Prepare risk scenario | Both contact ambiguity and fictional identifier are shown; Approve unavailable | `risk-blocked.jpg` |
| Edit and recheck | Select internal Alex; replace attachment with summary; apply | Version changed; old review invalidated; both fixture issues resolved; approval still requires a fresh check | `risk-rechecked.jpg` |
| Cancel | Cancel the revised risk draft | Cancellation confirmation; draft closed | `cancelled.jpg` |
| False alarm | Inspect public handout and budget keyword warning | Advisory explicitly identifies uncertainty; approval unavailable pending correction | `false-alarm-warning.jpg` |
| Presentation comparison | Switch warning to generic and back | Wording changes; gate stays active | `generic-warning.jpg` |
| Correction | Enter a reason; record one-time correction; review; approve | Correction limited to this draft; simulated result displayed | `false-alarm-corrected.jpg`, `false-alarm-result.jpg` |
| Tool failure | Enable next-call failure; review; approve | Failed state, no success message; fresh review required before retry | `send-failure.jpg` |

Browser screenshots live in `../evidence/`. `browser-observations.txt` retains the final failure-state DOM snapshot before the demonstration was reset.

## Report demonstration replay

For the illustrated-report revision, Codex repeated the interactions in a fresh local server session on port 8767 on 24 November 2026. The student's existing port 8765 session was not reset. All 17 original full-page screenshots and matching DOM snapshots are in [report-demo](../evidence/report-demo/); [observations.json](../evidence/report-demo/observations.json) records the actions and observed panel regions. See [report demonstrations](REPORT_DEMONSTRATIONS.md) for the capture-by-capture account and its mapping to the three report examples and supplementary failure/retry check.

The replay also checks that an old false-alarm correction is cleared after reloading the scenario and that a failed tool call can recover only after a fresh review. Captures `16-unsaved-edit-guard` and `17-saved-edit-switch` verify the warning-selector correction: trying to switch with unapplied edits restores the previous selection and prompts the user to apply changes; switching works after the new draft is checked. Original captures are preserved alongside the enlarged report crops. They are functional evidence produced by Codex, not participant data.

The latest regression console record is [automated-tests.txt](../evidence/automated-tests.txt). It is separate from the browser record and identifies the actual command and test outcomes. The report text now applies course concepts without formal lecture citations and retains Harvard references for external research, following the student's editing request.

## Limits of evidence

This verifies selected interactions and control invariants. It does not measure security against arbitrary attacks, scanner accuracy, decision quality, accessibility conformance or long-term warning fatigue. Browser UI controls and semantic labels were inspected, but no systematic accessibility audit was conducted. The generic/detailed mode still shares contextual fixture metadata; a future controlled study must isolate wording carefully and counterbalance scenario order.

Sessions and the interaction record are held in memory and lost on server restart. The server is deliberately a single-process loopback teaching prototype, not a production mail gateway.
