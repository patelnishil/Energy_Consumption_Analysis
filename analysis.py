import pandas as pd
import numpy as np


def records_to_dataframe(records):
    if not records:
        return pd.DataFrame(
            columns=["id", "appliance", "category", "date", "units_kwh", "cost"]
        )

    df = pd.DataFrame(records)
    df["units_kwh"] = pd.to_numeric(df["units_kwh"])
    df["cost"] = pd.to_numeric(df["cost"])
    df["date"] = pd.to_datetime(df["date"])
    return df


def calculate_summary(records):
    df = records_to_dataframe(records)

    if df.empty:
        return {
            "total_units": 0,
            "average_units": 0,
            "total_cost": 0
        }

    return {
        "total_units": float(df["units_kwh"].sum()),
        "average_units": float(np.mean(df["units_kwh"])),
        "total_cost": float(df["cost"].sum())
    }


def compare_appliances(records):
    df = records_to_dataframe(records)
    if df.empty:
        return pd.DataFrame(columns=["appliance", "units_kwh"])

    result = (
        df.groupby("appliance", as_index=False)["units_kwh"]
        .sum()
        .sort_values("units_kwh", ascending=False)
    )
    return result


def compare_categories(records):
    df = records_to_dataframe(records)
    if df.empty:
        return pd.DataFrame(columns=["category", "units_kwh"])

    return (
        df.groupby("category", as_index=False)["units_kwh"]
        .sum()
        .sort_values("units_kwh", ascending=False)
    )


def compare_periods(records):
    df = records_to_dataframe(records)
    if df.empty:
        return pd.DataFrame(columns=["period", "units_kwh"])

    df["period"] = df["date"].dt.to_period("M").astype(str)
    return (
        df.groupby("period", as_index=False)["units_kwh"]
        .sum()
        .sort_values("period")
    )


def find_high_usage(records):
    df = records_to_dataframe(records)
    if df.empty:
        return df

    average = np.mean(df["units_kwh"])
    return df[df["units_kwh"] > average].sort_values(
        "units_kwh", ascending=False
    )


def highest_category(records):
    result = compare_categories(records)
    return result.iloc[0] if not result.empty else None
