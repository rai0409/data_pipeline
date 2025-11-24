from pathlib import Path
import pandas as pd
from typing import List


def load_topix1000_tickers(path: Path) -> pd.DataFrame:
    """
    TOPIX1000 構成銘柄一覧を読み込む。

    想定カラム（どれかがあればOK）:
      - ticker / code / symbol
      - name
      - sector
      - start_date
      - end_date
    """
    df = pd.read_csv(path)
    # ティッカー列名を統一
    for col in ["ticker", "code", "symbol"]:
        if col in df.columns:
            df = df.rename(columns={col: "ticker"})
            break
    if "ticker" not in df.columns:
        raise ValueError("tickers_topix1000.csv に ticker/code/symbol のいずれかの列が必要です。")
    return df


def get_ticker_list(df: pd.DataFrame) -> List[str]:
    return df["ticker"].astype(str).tolist()
