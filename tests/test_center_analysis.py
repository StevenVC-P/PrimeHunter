import json
import unittest
from pathlib import Path

from center_analysis_experiment import (
    MAX_RECORD_CENTERS,
    default_output_path,
    validate_range,
)
from primehunter.tools.center_analysis import (
    analyze_center,
    analyze_center_range,
    build_result_envelope,
    build_summary,
    classify_center,
    smallest_disruptor,
    summarize_center_range,
    write_json_output,
)


class CenterAnalysisTests(unittest.TestCase):
    def test_classification_states(self):
        self.assertEqual(classify_center(True, True), "twin_prime")
        self.assertEqual(classify_center(True, False), "left_only_prime")
        self.assertEqual(classify_center(False, True), "right_only_prime")
        self.assertEqual(classify_center(False, False), "neither_prime")

    def test_smallest_disruptor(self):
        self.assertEqual(smallest_disruptor(35), 5)
        self.assertEqual(smallest_disruptor(91), 7)
        self.assertIsNone(smallest_disruptor(97))

    def test_known_center_record(self):
        record = analyze_center(4)
        self.assertEqual(record["center"], 24)
        self.assertEqual(record["classification"], "left_only_prime")
        self.assertTrue(record["left"]["is_prime"])
        self.assertFalse(record["right"]["is_prime"])
        self.assertEqual(record["right"]["smallest_disruptor"], 5)
        self.assertEqual(record["right"]["factorization"], [5, 5])

    def test_summary_only_shape(self):
        summary = summarize_center_range(1, 12)
        payload = build_result_envelope(
            experiment="twin_center_analysis",
            input_data={"start_n": 1, "end_n": 12, "summary_only": True},
            summary=summary,
            records=[],
            metadata={"mode": "summary_only"},
        )
        self.assertEqual(payload["records"], [])
        self.assertIn("metadata", payload)
        self.assertEqual(payload["metadata"]["mode"], "summary_only")
        self.assertEqual(payload["summary"]["center_count"], 12)

    def test_range_limit_enforcement(self):
        with self.assertRaises(ValueError):
            validate_range(1, MAX_RECORD_CENTERS + 1, summary_only=False)

    def test_default_output_paths(self):
        self.assertTrue(default_output_path(False).endswith("twin_center_analysis.json"))
        self.assertTrue(default_output_path(True).endswith("twin_center_analysis_summary.json"))

    def test_json_output_write(self):
        records = analyze_center_range(1, 3)
        payload = build_result_envelope(
            experiment="twin_center_analysis",
            input_data={"start_n": 1, "end_n": 3},
            summary=build_summary(records),
            records=records,
            metadata={"mode": "full_record"},
        )

        output_dir = Path("outputs") / "test_artifacts"
        output_path = output_dir / "center_analysis_test.json"
        write_json_output(output_path, payload)
        written = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(written["experiment"], "twin_center_analysis")
        self.assertEqual(written["metadata"]["mode"], "full_record")
        self.assertEqual(len(written["records"]), 3)
        output_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
