import json
import unittest
from pathlib import Path

from missing_partner_analysis_experiment import (
    MAX_RECORD_CENTERS,
    default_output_path,
    validate_range,
)
from primehunter.tools.missing_partner_analysis import (
    analyze_missing_partner_range,
    build_result_envelope,
    build_summary,
    extract_missing_partner_cases,
    is_missing_partner_case,
    summarize_missing_partner_range,
    write_json_output,
)
from primehunter.tools.center_analysis import analyze_center_range


class MissingPartnerAnalysisTests(unittest.TestCase):
    def test_missing_partner_case_detection(self):
        records = analyze_center_range(1, 6)
        self.assertFalse(is_missing_partner_case(records[0]))
        self.assertTrue(is_missing_partner_case(records[3]))
        self.assertTrue(is_missing_partner_case(records[5]))

    def test_extract_missing_partner_cases(self):
        records = analyze_center_range(1, 12)
        missing_partner_records = extract_missing_partner_cases(records)
        self.assertEqual(len(missing_partner_records), 5)
        self.assertTrue(
            all(
                record["classification"] in ("left_only_prime", "right_only_prime")
                for record in missing_partner_records
            )
        )

    def test_analyze_missing_partner_range(self):
        records = analyze_missing_partner_range(1, 12)
        self.assertEqual(len(records), 5)
        self.assertEqual(records[0]["center"], 24)
        self.assertEqual(records[0]["classification"], "left_only_prime")

    def test_summary_only_shape(self):
        summary = summarize_missing_partner_range(1, 12)
        payload = build_result_envelope(
            experiment="missing_partner_analysis",
            input_data={"start_n": 1, "end_n": 12, "summary_only": True},
            summary=summary,
            records=[],
            metadata={"mode": "summary_only"},
        )
        self.assertEqual(payload["records"], [])
        self.assertEqual(payload["summary"]["center_count"], 12)
        self.assertEqual(payload["summary"]["missing_partner_count"], 5)
        self.assertEqual(payload["summary"]["left_missing_partner_ratio"], 0.6)
        self.assertEqual(payload["metadata"]["mode"], "summary_only")

    def test_summary_counts(self):
        records = analyze_missing_partner_range(1, 12)
        summary = build_summary(records, analyzed_center_count=12)
        self.assertEqual(summary["center_count"], 12)
        self.assertEqual(summary["missing_partner_count"], 5)
        self.assertEqual(summary["left_missing_partner_count"], 3)
        self.assertEqual(summary["right_missing_partner_count"], 2)
        self.assertEqual(summary["right_missing_partner_ratio"], 0.4)

    def test_range_limit_enforcement(self):
        with self.assertRaises(ValueError):
            validate_range(1, MAX_RECORD_CENTERS + 1, summary_only=False)

    def test_default_output_paths(self):
        self.assertTrue(default_output_path(False).endswith("missing_partner_analysis.json"))
        self.assertTrue(default_output_path(True).endswith("missing_partner_analysis_summary.json"))

    def test_json_output_write(self):
        records = analyze_missing_partner_range(1, 12)
        payload = build_result_envelope(
            experiment="missing_partner_analysis",
            input_data={"start_n": 1, "end_n": 12},
            summary=build_summary(records, analyzed_center_count=12),
            records=records,
            metadata={"mode": "full_record"},
        )

        output_dir = Path("outputs") / "test_artifacts"
        output_path = output_dir / "missing_partner_analysis_test.json"
        write_json_output(output_path, payload)
        written = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(written["experiment"], "missing_partner_analysis")
        self.assertEqual(written["metadata"]["mode"], "full_record")
        self.assertEqual(written["summary"]["center_count"], 12)
        self.assertEqual(len(written["records"]), 5)
        output_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
