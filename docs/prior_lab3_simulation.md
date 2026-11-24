# Markdown simulation: Email a project report

**Mode:** Scripted scenario simulation. No live model, inbox, contact directory, file scanner, or email tool is connected. Names, addresses, files, and scan results are illustrative.

## Test A — Expected input

**Person:** Send the project report to my colleague.

**Agent — draft preview:**

- **To:** colleague@school.edu
- **Subject:** Project report
- **Attachment:** project_report.pdf
- **Message:** Hi, please find the project report attached. Best, [your name]

**System checks:** Recipient matches the one selected contact ✓ · Attachment is the requested report and scan has no simulated sensitive-data flag ✓ · Planned action is one email with this recipient and attachment ✓

**Agent — review:** Everything is ready. Review the recipient, attachment, and message. **Approve / Edit / Cancel**

**Person:** Approve.

**Simulated email tool:** Mock send result: success. (No email was sent.)

**Agent:** Email sent successfully in this simulation. To: colleague@school.edu · Attachment: project_report.pdf

**Outcome:** Expected path reaches confirmation after explicit approval.

## Test B — Problem input (initial design)

**Person:** Send the project report to my colleague.

**Simulated lookup:** Two possible contacts: colleague@school.edu and alex.lee@school.edu. The first candidate is inserted into the draft.

**Simulated attachment scan:** project_report.pdf contains a personal-identifier indicator.

**Agent — initial warning design:** Possible risk detected: the attachment may contain sensitive information. To: colleague@school.edu · Attachment: project_report.pdf · **Approve / Edit / Cancel**

**Review finding:** The warning did not disclose that the recipient was ambiguous and still presented Approve as an available action. The system must pause here. The email tool is not called and nothing is sent.

## Revised Test B — After changes

**Agent — revised review panel:**

- **Recipient needs confirmation:** Two contacts match “my colleague.” Select the intended contact before continuing.
- **Attachment needs review:** A personal-identifier indicator was found in project_report.pdf. Replace/remove it or inspect it under your organisation’s policy.
- **Approve:** unavailable until both blocking issues are resolved.
- **Available actions:** Select recipient · Replace attachment · Cancel

**Person:** Selects the intended contact and replaces the flagged attachment with a clean report copy.

**System:** Rebuilds the draft and reruns recipient, attachment, and planned-action checks. Prior approval/check results are invalidated by the edits.

**Agent:** All simulated checks pass for the revised draft. Review the exact recipient, file, and message. **Approve / Edit / Cancel**

**Outcome:** If the person approves, the simulated tool may return success; if a problem persists or the person cancels, no send occurs. This rerun ends safely at the paused/review state because the supplied storyboard does not provide a real recipient-selection interaction or real scan result to verify.

## Checks to apply when reviewing either run

1. Does the preview expose the complete recipient, subject, body, and attachment before any send?
2. Does the system distinguish a uniquely selected contact from a guessed or ambiguous match?
3. Does a flagged attachment create a clear pause, with the issue explained and actionable options?
4. Do Edit and any other content changes invalidate approval and trigger fresh checks?
5. Is the send action impossible before explicit approval of the exact displayed draft?
6. Does the confirmation match the tool result, and does failure avoid a false success message?

In this exercise these are review criteria applied to the scripted outputs, not automated measurements or live security guarantees.
