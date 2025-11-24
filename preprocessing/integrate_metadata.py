# preprocessing/integrate_metadata.py
from __future__ import annotations

import logging

from config.settings import FEATURE_DIR
from utils.io_utils import read_csv_safe, write_csv_safe
from utils.jpx_utils import save_ticker_metadata

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    # パネル読み込み
    panel_path = FEATURE_DIR / "panel_merged.csv"
    panel = read_csv_safe(panel_path)
    if panel is None:
        logger.error("[META] パネルが存在しません: %s", panel_path)
        return

    # 銘柄メタ情報を統合
    meta_path = save_ticker_metadata()
    from utils.io_utils import read_csv_safe as _read

    meta = _read(meta_path)
    if meta is None or "code" not in meta.columns:
        logger.error("[META] メタ情報の読み込みに失敗: %s", meta_path)
        return

    if "ticker" not in panel.columns:
        logger.error("[META] panel に ticker 列がありません")
        return

    # 簡易対応: ticker の数値部分を code とみなす（例: 7203.T → 7203）
    panel = panel.copy()
    panel["code"] = panel["ticker"].str.extract(r"(\d+)").iloc[:, 0].str.zfill(4)

    merged = panel.merge(meta, on="code", how="left")

    out_path = FEATURE_DIR / "panel_with_meta.csv"
    write_csv_safe(merged, out_path)
    logger.info("[META] メタ統合済みパネル保存: %s shape=%s", out_path, merged.shape)


if __name__ == "__main__":
    main()
