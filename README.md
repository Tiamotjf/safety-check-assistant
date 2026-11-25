# AI Agent Safety Check Assistant

README prose word count: 436 (headings and table text included; code and setup commands excluded).

## Status

An offline prototype for inspecting an agent's proposed email before approval. Implemented: editable draft, separate risk explanations, blocking checks, one-time false-alarm correction, per-draft approval, cancellation, simulated failure and visible feedback. Simulated: request understanding, contacts, attachment contents, sensitivity judgements and sending. Planned: evaluated live inference, authenticated file/mail access and human evaluation. No mail service is connected.

## Run and inspect

Python 3.10 or newer; standard library only. No installation, account, API key or internet required.

```text
python app.py --port 8765
```

Open `http://127.0.0.1:8765/`. Stop with Ctrl+C. Use another port if occupied. Session records disappear when the server stops.

1. Review and approve: prepare, inspect, tick the review box, approve.
2. Resolve two risks: select the intended Alex, replace the restricted fixture with the public summary, apply changes and recheck, then review or cancel.
3. Correct a false alarm: inspect the public budget handout, enter a correction reason, record it, then review and approve. Reloading this scenario requires a new decision.

The warning-presentation selector compares generic and specific wording without weakening the gate. It is not a completed user study. The failure control demonstrates honest failure feedback.

## Technology and tests

| File | Role |
|---|---|
| `app.py` | Loopback HTTP server and session isolation |
| `engine.py` | Fixture inference, state, checks, review tokens and mock tool |
| `web/` | HTML, CSS and JavaScript interaction |
| `tests/` | Control and HTTP regression checks |
| `evidence/` | Actual test output and browser screenshots |
| `docs/` | Architecture, storyboards, development record and limitations |

```text
python -m unittest discover -s tests -v
```

The recorded run passed 18 tests. Approvals are bound to draft version and content; edits invalidate them. Duplicate requests do not create duplicate mock sends. This is not a security certification.

## Development record and assistance

See [development record](docs/DEVELOPMENT.md), [validation](docs/VALIDATION.md), [report demonstrations](docs/REPORT_DEMONSTRATIONS.md) and [lecture mapping](docs/LECTURE_MAPPING.md). Earlier Lab 2/3 documents are retained as explicitly labelled provenance, not runnable features. No Lab 4 code is reused.

Codex assisted with Python and browser-interface implementation, test generation, diagrams, report drafting and browser walkthroughs. Its outputs were checked through 18 automated tests, recorded interface runs and reference verification. Checks led to fixes for cancellation, completed-state headings and the warning selector. The design follows the A1 review and Lab 2–3 specifications; the prototype uses scripted fixtures and simulated email delivery.

## Submission and additional files

Public repository: [https://github.com/Tiamotjf/safety-check-assistant](https://github.com/Tiamotjf/safety-check-assistant). Submission version: [a2-submission-v3](https://github.com/Tiamotjf/safety-check-assistant/tree/a2-submission-v3).

The [English illustrated report](docs/A2_Project_Report_3110586_Final.docx) and [Chinese reading version](docs/A2_Project_Report_中文版_提交对照版.docx) include three primary interaction examples and a supplementary failure/retry check. Their screenshots come from the 17-state replay recorded in [report demonstrations](docs/REPORT_DEMONSTRATIONS.md). All project evidence can reasonably be kept in the repository; no supplementary submission ZIP is needed merely to duplicate it.

The local handover archive is a convenience for moving the project, not an assignment requirement. There are no credentials or external dependencies to configure.
