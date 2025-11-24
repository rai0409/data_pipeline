# scraping/scrape_edinet_xbrl.py
"""
EDINET API からXBRL zipをダウンロードする雛形。
安全のため、デフォルトでは実際のダウンロードは行わず、
URLと保存先のパス設計だけをしている。
"""

from __future__ import annotations

import logging
from pathlib import Path

import requests

from config.settings import RAW_FUND_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_edinet_zip(doc_id: str, out_dir: Path) -> Path:
    """
    doc_id (EDINET書類ID) のXBRL zipをダウンロードする。

    実際のEDINET API仕様に合わせてURLやヘッダーを調整する必要あり。
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{doc_id}.zip"

    # EDINET のAPI仕様は公式ドキュメント参照。
    url = f"https://disclosure.edinet-fsa.go.jp/api/v1/documents/{doc_id}?type=1"

    resp = requests.get(url, timeout=60)
    resp.raise_for_status()

    with out_path.open("wb") as f:
        f.write(resp.content)

    logger.info("[EDINET] ダウンロード完了: %s", out_path)
    return out_path


def main() -> None:
    RAW_FUND_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("[EDINET] doc_id を決めてから download_edinet_zip(doc_id, RAW_FUND_DIR) を呼んでください。")
    logger.info("[EDINET] 実運用前に EDINET API 利用規約・レート制限を必ず確認してください。")


if __name__ == "__main__":
    main()
