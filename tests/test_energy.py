import unittest
from data_manager import validate_record, EnergyValidationError
from analysis import calculate_summary, compare_appliances, find_high_usage


class TestEnergyProject(unittest.TestCase):

    def test_valid_record(self):
        units, cost = validate_record(
            "Fan", "Cooling", "2026-10-01", "2.5", "20"
        )
        self.assertEqual(units, 2.5)
        self.assertEqual(cost, 20.0)

    def test_invalid_units(self):
        with self.assertRaises(EnergyValidationError):
            validate_record(
                "Fan", "Cooling", "2026-10-01", "-2", "20"
            )

    def test_summary(self):
        records = [
            {
                "id": "1", "appliance": "Fan", "category": "Cooling",
                "date": "2026-10-01", "units_kwh": "2", "cost": "16"
            },
            {
                "id": "2", "appliance": "AC", "category": "Cooling",
                "date": "2026-10-01", "units_kwh": "8", "cost": "64"
            }
        ]
        summary = calculate_summary(records)
        self.assertEqual(summary["total_units"], 10)
        self.assertEqual(summary["average_units"], 5)
        self.assertEqual(summary["total_cost"], 80)

    def test_appliance_comparison(self):
        records = [
            {
                "id": "1", "appliance": "Fan", "category": "Cooling",
                "date": "2026-10-01", "units_kwh": "2", "cost": "16"
            },
            {
                "id": "2", "appliance": "AC", "category": "Cooling",
                "date": "2026-10-01", "units_kwh": "8", "cost": "64"
            }
        ]
        result = compare_appliances(records)
        self.assertEqual(result.iloc[0]["appliance"], "AC")

    def test_high_usage(self):
        records = [
            {
                "id": "1", "appliance": "Fan", "category": "Cooling",
                "date": "2026-10-01", "units_kwh": "2", "cost": "16"
            },
            {
                "id": "2", "appliance": "AC", "category": "Cooling",
                "date": "2026-10-01", "units_kwh": "8", "cost": "64"
            }
        ]
        result = find_high_usage(records)
        self.assertEqual(len(result), 1)
        self.assertEqual(result.iloc[0]["appliance"], "AC")


if __name__ == "__main__":
    unittest.main()
