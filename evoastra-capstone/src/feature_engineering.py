"""Feature engineering module."""

import pandas as pd


def create_lag_features(df: pd.DataFrame, columns: list, lags: list) -> pd.DataFrame:
    """Create lag features for time-series analysis."""

    df_copy = df.copy()

    for col in columns:
        for lag in lags:
            df_copy[f"{col}_lag_{lag}"] = df_copy[col].shift(lag)

    df_copy = df_copy.dropna()

    return df_copy