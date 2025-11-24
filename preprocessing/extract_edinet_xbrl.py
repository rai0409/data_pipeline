import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import RAW_FUND_DIR, DATA_CLEAN_DIR
from utils.io_utils import ensure_dir
from utils.edinet_xbrl_utils import parse_xbrl_minimal


def main():
    if not RAW_FUND_DIR.exists():
        print(f"[WARN] RAW_FUND_DIR がありません: {RAW_FUND_DIR}")
        return

    xbrl_files = list(RAW_FUND_DIR.glob("**/*.xbrl"))
    if not xbrl_files:
        print(f"[WARN] XBRL ファイルが見つかりません: {RAW_FUND_DIR}")
        return

    rows = []
    for f in xbrl_files:
        try:
            data = parse_xbrl_minimal(f)
        except Exception as e:
            print(f"[ERROR] XBRL パース失敗: {f} -> {e}")
            continue
        rows.append(data)

    if not rows:
        print("[WARN] 有効な XBRL データがありません。")
        return

    df = pd.DataFrame(rows)
    out_dir = DATA_CLEAN_DIR / "fundamentals"
    ensure_dir(out_dir)
    out_path = out_dir / "fundamentals_minimal.csv"
    df.to_csv(out_path, index=False)
    print(f"[OK] XBRL 最小抽出結果: {out_path}, shape={df.shape}")


if __name__ == "__main__":
    main()
