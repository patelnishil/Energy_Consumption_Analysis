import csv
from pathlib import Path
from datetime import datetime


DATA_FILE = Path(__file__).parent / "data" / "energy_records.csv"


class EnergyValidationError(Exception):
    """Raised when an energy record contains invalid data."""


def ensure_file():
    DATA_FILE.parent.mkdir(exist_ok=True)
    if not DATA_FILE.exists():
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["id", "appliance", "category", "date", "units_kwh", "cost"]
            )
            writer.writeheader()

def delete_record_by_id(record_id):
    records = load_records()

    updated_records = [
        r for r in records
        if str(r["id"]) != str(record_id)
    ]

    if len(updated_records) == len(records):
        raise EnergyValidationError("Record not found.")

    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "id",
            "appliance",
            "category",
            "date",
            "units_kwh",
            "cost"
        ]

        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames
        )

        writer.writeheader()
        writer.writerows(updated_records)

def load_records():
    ensure_file()
    records = []
    with open(DATA_FILE, "r", newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            records.append(row)
    return records


def validate_record(appliance, category, date, units, cost):
    if not appliance.strip():
        raise EnergyValidationError("Appliance name is required.")

    if not category.strip():
        raise EnergyValidationError("Category is required.")

    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise EnergyValidationError("Date must be in YYYY-MM-DD format.")

    try:
        units_value = float(units)
        cost_value = float(cost)
    except ValueError:
        raise EnergyValidationError("Units and cost must be numeric.")

    if units_value < 0:
        raise EnergyValidationError("Units cannot be negative.")

    if cost_value < 0:
        raise EnergyValidationError("Cost cannot be negative.")

    return units_value, cost_value


def add_record(appliance, category, date, units, cost):
    units_value, cost_value = validate_record(
        appliance, category, date, units, cost
    )

    records = load_records()
    new_id = max([int(r["id"]) for r in records], default=0) + 1

    record = {
        "id": str(new_id),
        "appliance": appliance.strip(),
        "category": category.strip(),
        "date": date,
        "units_kwh": f"{units_value:.2f}",
        "cost": f"{cost_value:.2f}"
    }

    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=record.keys())
        writer.writerow(record)

    return record


def filter_records(records, appliance="", period=""):
    result = records

    if appliance.strip():
        key = appliance.strip().lower()
        result = [
            r for r in result
            if key in r["appliance"].lower()
        ]

    if period.strip():
        result = [
            r for r in result
            if r["date"].startswith(period.strip())
        ]

    return result
