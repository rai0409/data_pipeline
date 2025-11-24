# preprocessing/clean_macro_data.py
from __future__ import annotations

import logging

import pandas as pd

from config.settings import RAW_MACRO_DIR, CLEAN_MACRO_DIR
from utils.date_utils import ensure_date_index
from utils.io_utils import read_csv_safe, write_csv_safe

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def clean_one_macro(path):
    df = read_csv_safe(path)
    if df is None:
        return

    # 日付列を推定（Date / date / 日付 など）
    date_col = None
    for cand in ["Date", "date", "日付", "年月", "year_month"]:
        if cand in df.columns:
            date_col = cand
            break

    if date_col:
        df = ensure_date_index(df, date_col)
    else:
        logger.warning("[MACRO] 日付列が見つからないため index はそのまま: %s", path)

    df = df.sort_index().ffill().bfill()

    out_path = CLEAN_MACRO_DIR / path.name
    write_csv_safe(df.reset_index(), out_path)


def main() -> None:
    RAW_MACRO_DIR.mkdir(parents=True, exist_ok=True)
    CLEAN_MACRO_DIR.mkdir(parents=True, exist_ok=True)

    for path in RAW_MACRO_DIR.glob("*.csv"):
        logger.info("[MACRO] 前処理開始: %s", path.name)
        try:
            clean_one_macro(path)
        except Exception as e:
            logger.exception("[MACRO] 前処理失敗: %s (%s)", path, e)


if __name__ == "__main__":
    main()
