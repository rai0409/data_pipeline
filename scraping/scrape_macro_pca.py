# scraping/scrape_macro_pca.py
"""
マクロ指標を複数ソースから収集・統合するための雛形。
現時点では「既存の手元CSVを data_raw/macro にコピーするだけ」の安全実装。
"""

from __future__ import annotations

import logging
from pathlib import Path

from config.settings import RAW_MACRO_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    RAW_MACRO_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("[MACRO] ここではまだ外部スクレイピングは行っていません。")
    logger.info("[MACRO] 既存の GDP / CPI / PPI などの CSV を data_raw/macro に手動配置してください。")


if __name__ == "__main__":
    main()
