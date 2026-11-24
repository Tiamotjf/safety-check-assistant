import unittest
from engine import Engine, Rejected

class ControlTests(unittest.TestCase):
    def draft(self, scenario="normal"):
        e=Engine();e.reset(scenario);e.prepare();return e

    def test_no_send_without_approval(self):
        e=self.draft()
        with self.assertRaises(Rejected):e.send("invented")
        self.assertFalse(any(x["event"]=="mock_send_recorded" for x in e.events))

    def test_normal_and_duplicate_request(self):
        e=self.draft();token=e.review(e.revision,True)
        first=e.send(token);second=e.send(token)
        self.assertEqual(first,second)
        self.assertEqual(sum(x["event"]=="mock_send_recorded" for x in e.events),1)

    def test_stale_approval_after_edit(self):
        e=self.draft();token=e.review(e.revision,True)
        e.edit({"recipient":"external"})
        with self.assertRaises(Rejected):e.send(token)

    def test_unresolved_contact_blocks_review(self):
        e=self.draft("risk");e.edit({"file":"summary"})
        with self.assertRaises(Rejected):e.review(e.revision,True)

    def test_contact_selection_does_not_clear_sensitive_file(self):
        e=self.draft("risk");e.edit({"recipient":"internal"})
        self.assertEqual([i["id"] for i in e.check()],["private"])
        with self.assertRaises(Rejected):e.review(e.revision,True)

    def test_both_issues_resolved_then_send(self):
        e=self.draft("risk");e.edit({"recipient":"internal","file":"summary"})
        result=e.send(e.review(e.revision,True));self.assertEqual(result["stage"],"sent")

    def test_advisory_requires_reason(self):
        e=self.draft("false_alarm")
        with self.assertRaises(Rejected):e.review(e.revision,True)
        with self.assertRaises(Rejected):e.acknowledge("ok")
        e.acknowledge("Public handout explicitly approved for sharing.")
        self.assertEqual(e.send(e.review(e.revision,True))["stage"],"sent")

    def test_correction_not_a_future_permission(self):
        e=self.draft("false_alarm");e.acknowledge("Public handout explicitly approved for sharing.")
        e.reset("false_alarm");e.prepare()
        self.assertEqual(e.acknowledgement,"")
        with self.assertRaises(Rejected):e.review(e.revision,True)

    def test_edit_invalidates_correction(self):
        e=self.draft("false_alarm");e.acknowledge("Public handout explicitly approved for sharing.")
        e.edit({"subject":"New draft"});self.assertEqual(e.acknowledgement,"")

    def test_cancel_invalidates_approval(self):
        e=self.draft();token=e.review(e.revision,True);e.cancel()
        with self.assertRaises(Rejected):e.send(token)

    def test_failure_never_claims_success_and_retry_needs_review(self):
        e=self.draft();e.fail_next=True;token=e.review(e.revision,True)
        result=e.send(token);self.assertEqual(result["stage"],"failed")
        self.assertFalse(any(x["event"]=="mock_send_recorded" for x in e.events))
        self.assertEqual(e.send(token)["stage"],"failed")
        self.assertEqual(e.send(e.review(e.revision,True))["stage"],"sent")

    def test_invalid_fixture_and_empty_message(self):
        e=self.draft()
        for data in ({"recipient":"random@anywhere.example"},{"file":"arbitrary-file"},{"body":""},{"extra":True}):
            with self.assertRaises(Rejected):e.edit(data)

    def test_old_receipt_cannot_replace_new_scenario(self):
        e=self.draft();token=e.review(e.revision,True);e.send(token);e.reset("risk")
        with self.assertRaises(Rejected):e.send(token)

    def test_review_requires_current_version_and_explicit_check(self):
        e=self.draft()
        for version,checked in ((e.revision-1,True),(e.revision,False),(e.revision,"yes")):
            with self.assertRaises(Rejected):e.review(version,checked)

if __name__=="__main__":unittest.main()
