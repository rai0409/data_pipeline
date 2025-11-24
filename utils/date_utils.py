import pandas as pd


def to_datetime(series: pd.Series):
    return pd.to_datetime(series, errors="coerce")


def ensure_datetime_index(df: pd.DataFrame, col: str = "date") -> pd.DataFrame:
    df = df.copy()
    df[col] = pd.to_datetime(df[col], errors="coerce")
    df = df.dropna(subset=[col])
    df = df.sort_values(col)
    df = df.set_index(col)
    return df
