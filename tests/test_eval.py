"""Small unit tests for the evaluation logic; run with python3 -m unittest discover -s tests."""
import unittest
from eval import baseline, grade, parse_json_response


class TestEvaluation(unittest.TestCase):
    def setUp(self):
        self.case = {
            "policy": "Members may use one pass per year.",
            "gold_answer": "yes",
            "gold_evidence": "Members may use one pass per year.",
        }

    def test_correct_answer_and_citation(self):
        result = grade(self.case, {"answer": "yes", "evidence": self.case["policy"]})
        self.assertTrue(result["strict_pass"])

    def test_incorrect_answer_fails(self):
        result = grade(self.case, {"answer": "no", "evidence": self.case["policy"]})
        self.assertFalse(result["strict_pass"])
        self.assertTrue(result["gold_evidence_match"])

    def test_fabricated_citation_fails(self):
        result = grade(self.case, {"answer": "yes", "evidence": "A fabricated rule."})
        self.assertFalse(result["strict_pass"])
        self.assertFalse(result["evidence_appears_in_policy"])

    def test_json_parsing(self):
        self.assertEqual(parse_json_response('```json\n{"answer":"yes","evidence":"OK"}\n```')["answer"], "yes")

    def test_naive_baseline(self):
        prediction = baseline("Items are not refundable.", "Can I refund it?")
        self.assertEqual(prediction["answer"], "no")


if __name__ == "__main__":
    unittest.main()
