import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import FEATURE_DIR
from utils.feature_utils import add_returns


def main():
    panel_path = FEATURE_DIR / "stock_panel_adjclose.csv"
    if not panel_path.exists():
        print(f"[ERROR] {panel_path} がありません。先に merge_panel_all.py を実行してください。")
        return

    panel = pd.read_csv(panel_path, parse_dates=["date"]).set_index("date")

    # long 形式に変換: date, ticker, adj_close
    df_long = panel.reset_index().melt(id_vars="date", var_name="ticker", value_name="adj_close")
    df_long = df_long.dropna(subset=["adj_close"])

    # 簡易特徴量（TFT では追加のstatic/known futureなどは後で拡張）
    df_long = df_long.sort_values(["ticker", "date"])
    df_long = df_long.groupby("ticker", group_keys=False).apply(add_returns)

    out_path = FEATURE_DIR / "tft_features_basic.csv"
    df_long.to_csv(out_path, index=False)
    print(f"[OK] TFT 用基本特徴量: {out_path}, shape={df_long.shape}")


if __name__ == "__main__":
    main()
