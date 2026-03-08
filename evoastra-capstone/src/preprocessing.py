"""Data preprocessing module for supply chain capstone."""

import pandas as pd


def load_data(filepath: str) -> pd.DataFrame:
    """Load raw dataset."""
    df = pd.read_csv(filepath, encoding="latin1")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Basic cleaning."""

    # remove duplicates
    df = df.drop_duplicates()

    # fill numeric missing values
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    # fill categorical missing values
    cat_cols = df.select_dtypes(include=["object"]).columns
    df[cat_cols] = df[cat_cols].fillna("Unknown")

    return df