"""
data_loader.py
--------------
Loads and preprocesses the Costco grocery CSV dataset.
"""

import pandas as pd
import os


def load_data(csv_path: str = None) -> pd.DataFrame:
    if csv_path is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(base_dir, "costco_grocery.csv")

    df = pd.read_csv(csv_path)
    df = df.dropna(subset=["title", "price", "rating"])
    df = df[df["price"] > 0]
    df["price"] = df["price"].astype(float)
    df["rating"] = df["rating"].astype(float)
    df["subcategory"] = df["subcategory"].astype(str).str.strip()
    df["title"] = df["title"].astype(str).str.strip()

    if df["vegetarian"].dtype == object:
        df["vegetarian"] = df["vegetarian"].str.strip().str.lower() == "true"
    else:
        df["vegetarian"] = df["vegetarian"].astype(bool)

    return df.reset_index(drop=True)


def filter_items(
    df: pd.DataFrame,
    subcategories: list = None,
    vegetarian_only: bool = False,
) -> list:
    filtered = df.copy()
    if vegetarian_only:
        filtered = filtered[filtered["vegetarian"] == True]
    if subcategories:
        filtered = filtered[filtered["subcategory"].isin(subcategories)]
    return filtered.to_dict(orient="records")


def get_subcategories(df: pd.DataFrame) -> list:
    return sorted(df["subcategory"].unique().tolist())
