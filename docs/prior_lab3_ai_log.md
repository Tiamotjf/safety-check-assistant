# 02_PROMPT_LOG.md

This project used a structured Markdown simulation. No live Gemini, Copilot, language-model API, email service, or external tool was used. Codex assisted in drafting and revising the lab documents from the supplied storyboard and starter specification; all scenario outputs below are written simulations, not observed model responses.

## 2026-10-22 — Inspect materials and map the use case

**Tool used:** Codex (AI assistant); supplied Week 2 storyboard image and Lab 3 starter files.

**Request:** Use the storyboard about emailing a project report to a colleague. Preserve the starter files; create a Markdown simulation, system diagram, specification, prompt log, and package folder.

**What came back:** A proposed flow covering request parsing, recipient/file lookup, email drafting, checks for sensitive data/wrong recipient/action, a warning and explicit approve/edit/cancel decision, and a send confirmation. The storyboard specifies `colleague@school.edu` and `project_report.pdf` as example values.

**Decision:** Kept the storyboard's user journey and example values, but marked all contact/file data and the send operation as simulated. Chose Markdown because no live account or practical model route was provided and a real send is an external side effect.

## 2026-10-22 — Simulate standard and problem inputs; revise

**Tool used:** Codex (AI assistant) for drafting the structured simulation and diagram source; scenario reasoning is explicitly simulated.

**Request:** Specify one expected input and one problem input, show what the system receives/does/responds, identify a problem from the test, then revise the interaction and system path and rerun the problem case.

**What came back:** Standard case completed the checks and reached a mock sent confirmation after approval. Problem case surfaced two plausible contacts plus a simulated personal identifier in the attachment. The first-pass warning design could leave both concerns unresolved while still appearing approvable.

**Decision:** Kept both test scenarios. Changed the design to separate and name the issues, block approval until ambiguity and a blocking sensitivity finding are resolved, and rerun checks after edits. Rejected any representation of the mock send as a real email or of a simulated scan as a verified safety result.

## 2026-10-22 — Package preparation

**Tool used:** Local file operations to copy the supplied storyboard, retain starter files, and create the project archive.

**Request:** Preserve the complete working project folder, include created/changed files and exported diagram, and exclude secrets/caches.

**What came back:** Starter ZIP contained `.gitignore`, `01_SPEC.md`, and `02_PROMPT_LOG.md`; it did not contain a Git repository or commit history.

**Decision:** Retained all three starter files, updated both Markdown templates, added the simulation and exported SVG, and included the supplied storyboard image. No history was available to preserve. No secrets or generated caches were added.
