import sys
from pathlib import Path
import time
import requests
import pandas as pd

# プロジェクトルートを import パスに追加
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import (
    RAW_STOCK_DIR,
    TOPIX1000_TICKERS_CSV,
    TIINGO_API_KEY,
)
from utils.io_utils import ensure_dir
from utils.jpx_utils import load_topix1000_tickers, get_ticker_list


TIINGO_URL = "https://api.tiingo.com/tiingo/daily/{ticker}/prices"


def fetch_tiingo_price(ticker: str, start_date: str, end_date: str) -> pd.DataFrame:
    if not TIINGO_API_KEY:
        raise RuntimeError("TIINGO_API_KEY が環境変数に設定されていません。")

    params = {
        "startDate": start_date,
        "endDate": end_date,
        "token": TIINGO_API_KEY,
    }
    url = TIINGO_URL.format(ticker=ticker)
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    data = r.json()
    if not data:
        return pd.DataFrame()
    df = pd.DataFrame(data)
    # date, adjClose を含んでいる想定
    return df


def main(
    start_date: str = "2010-01-01",
    end_date: str = "2025-12-31",
    sleep_sec: float = 0.3,
) -> None:
    ensure_dir(RAW_STOCK_DIR)
    tickers_df = load_topix1000_tickers(TOPIX1000_TICKERS_CSV)
    tickers = get_ticker_list(tickers_df)

    print(f"[INFO] Tiingo から {len(tickers)} 銘柄の株価を取得します。")

    for i, t in enumerate(tickers, 1):
        out_path = RAW_STOCK_DIR / f"{t}_raw.csv"
        if out_path.exists():
            print(f"[SKIP] {t} は既に存在: {out_path}")
            continue

        try:
            df = fetch_tiingo_price(t, start_date, end_date)
        except Exception as e:
            print(f"[ERROR] {t} 取得失敗: {e}")
            continue

        if df.empty:
            print(f"[WARN] {t} データなし")
            continue

        df.to_csv(out_path, index=False)
        print(f"[OK] ({i}/{len(tickers)}) {t}: {len(df)} 行保存 -> {out_path}")
        time.sleep(sleep_sec)


if __name__ == "__main__":
    main()
