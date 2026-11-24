"""Local interaction state machine. All inference and sending use fixtures.

The code implements the control loop, not a real AI model or safety scanner.
"""
import copy
import hashlib
import json
import secrets

CONTACTS = {
    "internal": {"name": "Alex Reed (project colleague)", "email": "alex@team.example"},
    "external": {"name": "Alex Reed (external contact)", "email": "alex@outside.example"},
}
FILES = {
    "summary": {"name": "project_summary.txt", "text": "Public project summary. No personal records.", "classification": "Public"},
    "private": {"name": "student_records.txt", "text": "FICTIONAL TEST DATA\nSTUDENT-ID: DEMO-0042\nPrivate student record. Not for email sharing.", "classification": "Restricted fixture"},
    "budget": {"name": "public_event_budget.txt", "text": "PUBLIC WORKSHOP HANDOUT\nPublished event budget: 200 demonstration units. Approved for public sharing.", "classification": "Public"},
}
SCENARIOS = {
    "normal": {"title": "1. Review and approve", "request": "Send the public project summary to Alex, my project colleague.", "recipient": "internal", "file": "summary", "ambiguous": False},
    "risk": {"title": "2. Resolve two risks", "request": "Send the project records to Alex.", "recipient": "", "file": "private", "ambiguous": True},
    "false_alarm": {"title": "3. Correct a false alarm", "request": "Send the public workshop budget handout to my project colleague.", "recipient": "internal", "file": "budget", "ambiguous": False},
}

class Rejected(ValueError):
    pass

class Engine:
    def __init__(self):
        self.events = []
        self.receipts = {}
        self.revision = 0
        self.reset("normal")

    def event(self, kind, **fields):
        self.events.append({"n": len(self.events) + 1, "event": kind, "revision": self.revision, **fields})

    def reset(self, scenario):
        if scenario not in SCENARIOS:
            raise Rejected("Unknown scenario.")
        s = SCENARIOS[scenario]
        self.scenario = scenario
        self.revision += 1
        self.draft = {"recipient": s["recipient"], "file": s["file"], "subject": "Project document", "body": "Hi Alex, please find the selected document attached."}
        self.stage = "request"
        self.review_token = None
        self.acknowledgement = ""
        self.result = ""
        self.fail_next = False
        self.event("scenario_loaded", scenario=scenario)

    def fingerprint(self):
        return hashlib.sha256(json.dumps(self.draft, sort_keys=True).encode()).hexdigest()

    def check(self):
        issues = []
        if not self.draft["recipient"]:
            issues.append({"id": "recipient", "blocking": True, "title": "Choose the intended Alex", "evidence": "Two fixture contacts match the request.", "consequence": "The document could reach the wrong person.", "action": "Select the exact contact in the draft."})
        f = FILES[self.draft["file"]]
        if "STUDENT-ID:" in f["text"]:
            issues.append({"id": "private", "blocking": True, "title": "Restricted record detected", "evidence": "Fixture line 2: STUDENT-ID: DEMO-0042.", "consequence": "Sending would disclose a fictional private record.", "action": "Replace with the public summary, or cancel."})
        if "budget" in f["text"].lower():
            issues.append({"id": "budget", "blocking": False, "title": "Budget keyword needs context", "evidence": "The text contains 'budget', but also says 'PUBLIC WORKSHOP HANDOUT'.", "consequence": "The heuristic may be a false alarm; the word alone does not prove confidentiality.", "action": "Inspect the fixture and record a one-time decision, or cancel."})
        return issues

    def state(self):
        issues = self.check() if self.stage != "request" else []
        return copy.deepcopy({"scenario": self.scenario, "title": SCENARIOS[self.scenario]["title"], "request": SCENARIOS[self.scenario]["request"], "stage": self.stage, "revision": self.revision, "draft": self.draft, "contacts": CONTACTS, "files": FILES, "issues": issues, "blocking": any(x["blocking"] for x in issues), "acknowledgement": self.acknowledgement, "result": self.result, "events": self.events[-10:], "fail_next": self.fail_next})

    def prepare(self):
        if self.stage != "request":
            raise Rejected("Load a scenario to start another request.")
        self.stage = "review"
        self.event("fixture_draft_prepared", inference="simulated")
        return self.state()

    def edit(self, values):
        if self.stage not in ("review", "failed"):
            raise Rejected("This draft is not editable. Load a scenario to start again.")
        if not isinstance(values, dict) or set(values) - set(self.draft):
            raise Rejected("Unsupported draft fields.")
        candidate = {**self.draft, **values}
        if candidate["recipient"] not in ("", *CONTACTS):
            raise Rejected("Choose a fixture contact.")
        if candidate["file"] not in FILES:
            raise Rejected("Choose a fixture attachment.")
        if any(not isinstance(candidate[k], str) or not candidate[k].strip() or len(candidate[k]) > 1000 for k in ("subject", "body")):
            raise Rejected("Subject and message must contain 1–1000 characters.")
        self.draft = candidate
        self.revision += 1
        self.stage = "review"
        self.review_token = None
        self.acknowledgement = ""
        self.result = "Draft changed. Checks rerun; earlier review invalidated."
        self.event("draft_edited_and_rechecked")
        return self.state()

    def acknowledge(self, reason):
        if self.stage not in ("review", "failed") or not any(x["id"] == "budget" for x in self.check()):
            raise Rejected("No advisory warning is awaiting a decision.")
        if not isinstance(reason, str) or len(reason.strip()) < 10 or len(reason) > 500:
            raise Rejected("Explain this one-time decision in 10–500 characters.")
        self.acknowledgement = reason.strip()
        self.review_token = None
        self.event("one_time_correction", reason=self.acknowledgement)
        return self.state()

    def review(self, revision, checked):
        if self.stage not in ("review", "failed") or revision != self.revision:
            raise Rejected("Draft changed or closed. Review the current version.")
        if checked is not True:
            raise Rejected("Review the displayed recipient, attachment and message first.")
        if any(i["blocking"] for i in self.check()):
            raise Rejected("Resolve every blocking issue before approval.")
        if any(i["id"] == "budget" for i in self.check()) and not self.acknowledgement:
            raise Rejected("Record a one-time decision for the advisory warning.")
        self.review_token = {"value": secrets.token_hex(16), "revision": self.revision, "hash": self.fingerprint()}
        self.event("exact_draft_reviewed")
        return self.review_token["value"]

    def send(self, token):
        if not isinstance(token, str):
            raise Rejected("A valid review token is required.")
        if token in self.receipts:
            if self.receipts[token]["revision"] != self.revision:
                raise Rejected("This receipt belongs to an earlier draft.")
            return copy.deepcopy(self.receipts[token])
        t = self.review_token
        if self.stage not in ("review", "failed") or not t or token != t["value"] or t["revision"] != self.revision or t["hash"] != self.fingerprint():
            raise Rejected("Approval is missing, stale or already invalidated.")
        if any(i["blocking"] for i in self.check()):
            raise Rejected("A blocking issue remains.")
        self.review_token = None
        if self.fail_next:
            self.fail_next = False
            self.stage = "failed"
            self.result = "Simulated tool failed. Nothing was sent. Review and approve again to retry."
            self.event("mock_send_failed")
        else:
            self.stage = "sent"
            self.result = "Simulated send recorded. No real email was sent."
            self.event("mock_send_recorded", recipient=CONTACTS[self.draft["recipient"]]["email"], attachment=FILES[self.draft["file"]]["name"], fingerprint=self.fingerprint())
        result = self.state()
        self.receipts[token] = result
        return result

    def cancel(self):
        if self.stage in ("sent", "cancelled"):
            raise Rejected("This interaction is already closed.")
        self.stage = "cancelled"
        self.review_token = None
        self.result = "Cancelled. Nothing was sent."
        self.event("cancelled")
        return self.state()
