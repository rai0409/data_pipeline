import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import CLEAN_STOCK_DIR, FEATURE_DIR
from utils.io_utils import ensure_dir, list_csvs
from utils.date_utils import ensure_datetime_index


def build_stock_panel(price_col: str = "adj_close") -> pd.DataFrame:
    files = list_csvs(CLEAN_STOCK_DIR)
    if not files:
        raise RuntimeError("clean stock csv がありません")

    dfs = []
    for f in files:
        ticker = f.stem.replace("_clean", "")
        df = pd.read_csv(f)
        if "date" in df.columns:
            df = ensure_datetime_index(df, "date")
        else:
            df.index = pd.to_datetime(df.index)

        if price_col not in df.columns:
            # adj_close がなければ close を使う
            fallback_col = "close" if "close" in df.columns else None
            if not fallback_col:
                print(f"[WARN] {f.name}: {price_col} も close も無いのでスキップ")
                continue
            col = fallback_col
        else:
            col = price_col

        s = df[col].rename(ticker)
        dfs.append(s)

    if not dfs:
        raise RuntimeError("panel を構築できる銘柄がありません。")

    panel = pd.concat(dfs, axis=1).sort_index()
    # 日付完全化（全銘柄のmin〜max）
    full_idx = pd.date_range(panel.index.min(), panel.index.max(), freq="B")
    panel = panel.reindex(full_idx)
    panel = panel.ffill()

    return panel


def main():
    ensure_dir(FEATURE_DIR)
    panel = build_stock_panel()
    out_path = FEATURE_DIR / "stock_panel_adjclose.csv"
    panel.to_csv(out_path, index_label="date")
    print(f"[OK] stock_panel_adjclose.csv 出力: {out_path}, shape={panel.shape}")


if __name__ == "__main__":
    main()
