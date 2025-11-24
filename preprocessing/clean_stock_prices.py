import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import RAW_STOCK_DIR, CLEAN_STOCK_DIR
from utils.io_utils import ensure_dir, list_csvs
from utils.date_utils import ensure_datetime_index


def clean_one_file(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    # date 列を index に
    if "date" not in df.columns:
        raise ValueError(f"{path} に 'date' 列がありません。")

    df = ensure_datetime_index(df, "date")
    # Tiingo のカラム名を想定: adjClose / close など
    rename_map = {}
    if "adjClose" in df.columns:
        rename_map["adjClose"] = "adj_close"
    if "close" in df.columns:
        rename_map["close"] = "close"
    df = df.rename(columns=rename_map)

    # 欠損を前方補間（簡易）
    df = df.sort_index()
    df = df.ffill()

    return df


def main():
    ensure_dir(CLEAN_STOCK_DIR)
    files = list_csvs(RAW_STOCK_DIR)
    if not files:
        print(f"[ERROR] RAW_STOCK_DIR にCSVがありません: {RAW_STOCK_DIR}")
        return

    for f in files:
        ticker = f.stem.replace("_raw", "")
        out_path = CLEAN_STOCK_DIR / f"{ticker}_clean.csv"
        try:
            df = clean_one_file(f)
        except Exception as e:
            print(f"[ERROR] {f.name} クリーニング失敗: {e}")
            continue
        df.to_csv(out_path)
        print(f"[OK] {ticker} -> {out_path}, shape={df.shape}")


if __name__ == "__main__":
    main()
