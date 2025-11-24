from pathlib import Path
from typing import Dict, Any


def parse_xbrl_minimal(path: Path) -> Dict[str, Any]:
    """
    XBRL からの抽出は本格実装が必要なので、
    ここではスタブ（最低限の形だけ）を用意しておく。
    """
    # TODO: 将来的に XBRL パーサ（arelle など）を使って実装
    return {
        "source_file": str(path),
        # "revenue": ...,
        # "net_income": ...,
    }
