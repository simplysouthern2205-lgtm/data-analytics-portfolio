"""
Data Cleaning & Analysis Script (Beginner Portfolio Project)
Author: Brandon Lee (portfolio sample)

Input:
  - messy_sales_data.csv

Outputs (written to --outdir):
  - cleaned_sales_data.csv
  - summary_by_month.csv
  - summary_by_region.csv

Run:
  python python_data_cleaning_analysis.py --input messy_sales_data.csv --outdir .
"""

from __future__ import annotations
import argparse
import pandas as pd


CURRENCY_COLS = ["unit_price", "revenue", "cost", "profit"]


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def parse_currency(series: pd.Series) -> pd.Series:
    # Remove $ and commas, coerce to float (nullable Float64)
    return (
        series.astype(str)
        .str.replace("$", "", regex=False)
        .str.replace(",", "", regex=False)
        .replace("nan", pd.NA)
        .astype("Float64")
    )


def clean_text(series: pd.Series) -> pd.Series:
    return (
        series.astype("string")
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
        .str.title()
    )


def build_summaries(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = df.copy()
    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)

    by_month = (
        df.groupby("order_month", dropna=False)[["revenue", "profit"]]
        .sum()
        .reset_index()
        .sort_values("order_month")
    )

    by_region = (
        df.groupby("region", dropna=False)[["revenue", "profit"]]
        .sum()
        .reset_index()
        .sort_values("profit", ascending=False)
    )
    return by_month, by_region


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    df = normalize_columns(df)

    # Standardize text columns
    for col in ["region", "channel", "segment", "category", "product", "city", "state"]:
        if col in df.columns:
            df[col] = clean_text(df[col])

    # Parse mixed date formats
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    # Parse money columns
    for col in CURRENCY_COLS:
        if col in df.columns:
            df[col] = parse_currency(df[col])

    # Simple missing-value handling (beginner friendly)
    if "segment" in df.columns and df["segment"].isna().any():
        df["segment"] = df["segment"].fillna(df["segment"].mode(dropna=True).iloc[0])

    if "city" in df.columns and df["city"].isna().any():
        df["city"] = df["city"].fillna("Unknown")

    # Ensure numeric units
    df["units"] = pd.to_numeric(df["units"], errors="coerce").fillna(0).astype(int)

    # Recalculate revenue/profit if missing (optional safety)
    if "unit_price" in df.columns and df["revenue"].isna().any():
        df["revenue"] = (df["units"] * df["unit_price"]).astype("Float64")

    if "cost" in df.columns and df["profit"].isna().any():
        df["profit"] = (df["revenue"] - df["cost"]).astype("Float64")

    return df


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="messy_sales_data.csv", help="Path to input CSV")
    parser.add_argument("--outdir", default=".", help="Output folder")
    args = parser.parse_args()

    raw = pd.read_csv(args.input)
    cleaned = clean_dataset(raw)
    by_month, by_region = build_summaries(cleaned)

    cleaned_path = f"{args.outdir.rstrip('/')}/cleaned_sales_data.csv"
    month_path = f"{args.outdir.rstrip('/')}/summary_by_month.csv"
    region_path = f"{args.outdir.rstrip('/')}/summary_by_region.csv"

    cleaned.to_csv(cleaned_path, index=False)
    by_month.to_csv(month_path, index=False)
    by_region.to_csv(region_path, index=False)

    print("Saved:")
    print(" -", cleaned_path)
    print(" -", month_path)
    print(" -", region_path)


if __name__ == "__main__":
    main()
