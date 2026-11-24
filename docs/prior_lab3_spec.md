# 01_SPEC.md: Email a project report safely

## Use case and user goal

Based on the Week 2 normal-interaction storyboard: the person asks an AI agent to email a project report to a colleague. The agent drafts the message and selects a recipient and attachment, runs safety checks, presents the draft and any warnings, then waits for an explicit user decision before sending.

## System inputs

- User request: “Send the project report to my colleague.”
- Project context: report file `project_report.pdf` (simulated fixture).
- Recipient context: a contact suggestion, `colleague@school.edu` (simulated fixture; not a real address).
- Attachment contents and sensitivity labels are simulated. No real email account, file, or personal data is accessed.

## Processing and technology

1. **Request parser (simulated language model):** identify the requested action, document, and intended recipient.
2. **Context lookup (simulated contacts/files):** propose a matching recipient and report attachment. If there are multiple matches, ask the user to choose.
3. **Draft composer (simulated language model):** create a short subject and message, showing recipient, attachment, and body before action.
4. **Safety gate (simulated deterministic checks):** verify recipient against the selected contact; scan attachment metadata/content indicators for sensitive data; confirm the planned action is exactly one email and the listed attachment. Any flag pauses execution.
5. **Human confirmation:** display warnings and draft details. Approve sends exactly the displayed version; Edit returns to draft editing and reruns all checks; Cancel sends nothing.
6. **Email tool (simulated only):** records a mock send result after approval; no external side effect occurs.

## Intended result and next action

When all checks pass or warnings have been reviewed and the user explicitly approves, show a sent confirmation with recipient and attachment. On a safety flag, explain the issue and wait. On edit, re-check the changed draft. On cancel, confirm that nothing was sent. If sending fails, report failure and do not claim success.

## Fallback strategy

- Unclear or multiple recipients: ask the user to select the exact contact; do not infer from a vague “colleague”.
- Missing or ambiguous attachment: show candidate files and ask for a choice; do not attach a guessed file.
- Sensitive-data finding: block automatic sending and identify the flagged category; allow the user to remove/replace the attachment or cancel. An override, if permitted by a real deployment, must be explicit and logged.
- Changed recipient, file, or message after review: invalidate prior approval and rerun checks.
- Email tool unavailable or send failure: keep the draft, show a failure state, and offer retry/edit/cancel; never show sent confirmation.

## System path / interaction diagram

See [`system_diagram.svg`](system_diagram.svg), an exported system-flow diagram. All processing and sending in this lab are simulated.

## Test A: standard input

**Input:** “Send the project report to my colleague.”

**What the system receives:** One simulated contact (`colleague@school.edu`), one file (`project_report.pdf`) with no sensitive-data indicator, and a request for one email.

**What it does:** Drafts subject “Project report” and a concise message; checks exact recipient, attachment identity/content scan, and planned action. Checks pass. Shows the complete draft and waits for a decision. User selects Approve. The simulated email tool returns success.

**Response and next action:** “Email sent successfully” with recipient and attachment. The user can continue their task. No real email is sent in this simulation.

## Test B: problem input (sensitive attachment and recipient ambiguity)

**Input:** “Send the project report to my colleague.” The contact lookup returns two plausible colleagues; the selected draft candidate is `colleague@school.edu`. The attachment scan flags `project_report.pdf` as containing a simulated personal identifier.

**What the system receives:** Ambiguous recipient candidates and a sensitive-data warning on the attachment.

**What it does (first pass):** Initially, a single warning panel showed the attachment risk but did not make the unresolved recipient ambiguity explicit enough. The user could approve with both concerns still unclear. This is a safety and interaction defect; the test must not proceed to send.

**Response and next action (revised):** Block approval until the user selects the exact recipient and resolves the attachment issue (remove/replace it, or inspect and explicitly confirm an allowed exception). Show separate, specific warnings for recipient and attachment. Then rebuild the draft and rerun recipient, attachment, and action checks. Cancel remains available at all times. This test ends at the paused state; nothing is sent.

## Review and revision

**Evidence:** Test A follows the storyboard through a clear draft, approval, mock send, and confirmation. Test B exposes two material risks: ambiguous identity was hidden behind a plausible default, and a generic warning did not sufficiently prevent a one-click send with unresolved sensitive data.

**Interaction change:** The review panel now lists each unresolved issue separately, disables Approve while ambiguity or a blocking sensitivity flag remains, and offers clear Select recipient / Replace attachment / Cancel actions. This makes the decision understandable and prevents accidental approval.

**System change:** Add a hard pre-send gate: recipient must be uniquely selected and the attachment scan must be resolved; any edit invalidates prior checks and triggers a fresh scan. This is safer than relying on a model-generated warning alone.

**Test B rerun:** With the revised gate, the system identifies both candidate contacts and the sensitive-data category, pauses, and does not call the email tool. After the user selects the colleague and replaces the flagged file, checks run again; only a clean draft can be approved. If either issue remains unresolved, send is unavailable. Outcome: safe pause; no send.

## Scope and limitations

This is a structured Markdown simulation, not a live model or working email prototype. Checks are illustrative and cannot establish that a real file is safe. A real system would need authenticated contact/file access, robust content scanning, auditability, permission controls, and a reliable email API, while still requiring review before an external send.
