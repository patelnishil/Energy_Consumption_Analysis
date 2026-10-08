from pathlib import Path
import matplotlib.pyplot as plt

from analysis import (
    records_to_dataframe,
    compare_appliances,
    compare_periods
)


REPORT_DIR = Path(__file__).parent / "reports"


def generate_reports(records):
    df = records_to_dataframe(records)

    if df.empty:
        raise ValueError("No energy records available for reports.")

    REPORT_DIR.mkdir(exist_ok=True)

    # Report 1: Appliance-wise consumption
    appliance_data = compare_appliances(records)
    plt.figure(figsize=(9, 5))
    plt.bar(appliance_data["appliance"], appliance_data["units_kwh"])
    plt.xlabel("Appliance")
    plt.ylabel("Energy Consumption (kWh)")
    plt.title("Report 1: Appliance-wise Energy Consumption")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()

    report1 = REPORT_DIR / "appliance_consumption.png"
    plt.savefig(report1, dpi=150)
    plt.close()

    # Report 2: Monthly consumption
    period_data = compare_periods(records)
    plt.figure(figsize=(9, 5))
    plt.plot(
        period_data["period"],
        period_data["units_kwh"],
        marker="o"
    )
    plt.xlabel("Month")
    plt.ylabel("Energy Consumption (kWh)")
    plt.title("Report 2: Monthly Energy Consumption Trend")
    plt.xticks(rotation=30, ha="right")
    plt.grid(True)
    plt.tight_layout()

    report2 = REPORT_DIR / "monthly_consumption_trend.png"
    plt.savefig(report2, dpi=150)
    plt.close()

    return [str(report1), str(report2)]
