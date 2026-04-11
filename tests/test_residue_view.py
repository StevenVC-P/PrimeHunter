import json
import unittest
from pathlib import Path

from scripts.tools.residue_view_experiment import MAX_RECORD_CENTERS, default_output_path, parse_primes, validate_range
from primehunter.tools.residue_view import (
    MAX_TRACKED_PRIMES,
    analyze_residue_view_range,
    build_result_envelope,
    build_summary,
    normalize_tracked_primes,
    write_json_output,
)


class ResidueViewTests(unittest.TestCase):
    def test_parse_primes(self):
        self.assertEqual(parse_primes("5,7,11"), [5, 7, 11])

    def test_default_primes(self):
        self.assertEqual(normalize_tracked_primes(), [5, 7, 11])

    def test_rejects_non_prime_values(self):
        with self.assertRaises(ValueError):
            parse_primes("5,9,11")

    def test_rejects_duplicate_values(self):
        with self.assertRaises(ValueError):
            parse_primes("5,7,7")

    def test_rejects_values_at_or_below_three(self):
        with self.assertRaises(ValueError):
            parse_primes("3,5,7")

    def test_rejects_unbounded_prime_list(self):
        oversized = [5, 7, 11, 13, 17, 19, 23]
        with self.assertRaises(ValueError):
            normalize_tracked_primes(oversized)
        self.assertEqual(MAX_TRACKED_PRIMES, 6)

    def test_record_shape(self):
        records = analyze_residue_view_range(1, 4, primes=[5, 7])
        record = records[3]
        self.assertEqual(record["center"], 24)
        self.assertEqual(record["right"]["value"], 25)
        self.assertEqual(record["right"]["residues"]["5"], 0)
        self.assertEqual(record["right"]["eliminated_by"], [5])
        self.assertEqual(record["right"]["smallest_eliminator"], 5)

    def test_prime_side_not_marked_eliminated(self):
        records = analyze_residue_view_range(1, 2, primes=[5, 7])
        first_record = records[0]
        self.assertEqual(first_record["left"]["value"], 5)
        self.assertEqual(first_record["left"]["eliminated_by"], [])
        self.assertIsNone(first_record["left"]["smallest_eliminator"])

    def test_summary_shape(self):
        records = analyze_residue_view_range(1, 12, primes=[5, 7, 11])
        summary = build_summary(records, [5, 7, 11])
        self.assertEqual(summary["center_count"], 12)
        self.assertEqual(summary["tracked_primes"], [5, 7, 11])
        self.assertEqual(summary["right_elimination_counts"]["5"], 2)
        self.assertEqual(summary["left_elimination_counts"]["5"], 2)

    def test_range_limit_enforcement(self):
        with self.assertRaises(ValueError):
            validate_range(1, MAX_RECORD_CENTERS + 1, summary_only=False)

    def test_default_output_paths(self):
        self.assertTrue(default_output_path(False).endswith("residue_view.json"))
        self.assertTrue(default_output_path(True).endswith("residue_view_summary.json"))

    def test_json_output_write(self):
        records = analyze_residue_view_range(1, 4, primes=[5, 7])
        payload = build_result_envelope(
            experiment="residue_view",
            input_data={"start_n": 1, "end_n": 4},
            summary=build_summary(records, [5, 7]),
            records=records,
            metadata={"mode": "full_record", "tracked_prime_limit": MAX_TRACKED_PRIMES},
        )

        output_dir = Path("outputs") / "test_artifacts"
        output_path = output_dir / "residue_view_test.json"
        write_json_output(output_path, payload)
        written = json.loads(output_path.read_text(encoding="utf-8"))
        self.assertEqual(written["experiment"], "residue_view")
        self.assertEqual(written["metadata"]["mode"], "full_record")
        self.assertEqual(written["metadata"]["tracked_prime_limit"], MAX_TRACKED_PRIMES)
        self.assertEqual(len(written["records"]), 4)
        output_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()

