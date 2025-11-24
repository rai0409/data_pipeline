import os
import time
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path

import yfinance as yf

from config.settings import (
    RAW_STOCK_DIR,
    TOPIX1000_TICKERS_CSV,
    ensure_directories,
)

TIINGO_API_KEY = os.getenv("TIINGO_API_KEY")
TIINGO_URL = "https://api.tiingo.com/tiingo/daily"

START_DATE = "2010-01-01"
END_DATE = datetime.now().strftime("%Y-%m-%d")


def fetch_tiingo(ticker):
    """Tiingo APIで株価取得"""
    url = f"{TIINGO_URL}/{ticker}/prices"
    params = {
        "token": TIINGO_API_KEY,
        "startDate": START_DATE,
        "endDate": END_DATE,
        "format": "json",
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()
        if len(data) == 0:
            return pd.DataFrame()
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"]).dt.date
        df.set_index("date", inplace=True)
        return df
    except:
        return pd.DataFrame()


def fetch_yf(ticker):
    """yfinance fallback"""
    df = yf.download(ticker, start=START_DATE, end=END_DATE, progress=False)
    if df.empty:
        return df
    df = df.reset_index()
    df["date"] = pd.to_datetime(df["Date"]).dt.date
    df.set_index("date", inplace=True)
    df = df.drop(columns=["Date"])
    return df


def fetch_with_retry(ticker):
    """Tiingo → yfinance → retry の順で取得"""
    # 1) Tiingo
    df = fetch_tiingo(ticker)
    if not df.empty:
        return df, "tiingo"

    # 2) yfinance fallback
    df = fetch_yf(ticker)
    if not df.empty:
        return df, "yfinance"

    # 3) retry (yfinance)
    time.sleep(2)
    df = fetch_yf(ticker)
    if not df.empty:
        return df, "yfinance-retry"

    # 4) fail
    return pd.DataFrame(), "fail"


def main():
    ensure_directories()

    tickers = pd.read_csv(TOPIX1000_TICKERS_CSV)["ticker"].tolist()
    print(f"対象銘柄: {len(tickers)}")

    for t in tickers:
        print(f"\n=== {t} 取得中 ===")
        df, source = fetch_with_retry(t)

        if df.empty:
            print(f"取得失敗: {t} （Tiingo & Yahoo）")
            continue

        out = RAW_STOCK_DIR / f"{t}.csv"
        df.to_csv(out)
        print(f"[保存完了] {out}  via {source}")

    print("\n=== 完全自動株価取得 完了 ===")


if __name__ == "__main__":
    main()
