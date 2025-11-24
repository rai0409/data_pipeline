import pandas as pd


def add_returns(df: pd.DataFrame, price_col: str = "adj_close") -> pd.DataFrame:
    df = df.copy()
    df["ret_1d"] = df[price_col].pct_change()
    return df


def add_rolling_stats(df: pd.DataFrame, price_col: str = "adj_close") -> pd.DataFrame:
    df = df.copy()
    df["ma_5"] = df[price_col].rolling(5).mean()
    df["ma_20"] = df[price_col].rolling(20).mean()
    df["vol_20"] = df[price_col].pct_change().rolling(20).std()
    return df
