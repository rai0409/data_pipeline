import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import RAW_META_DIR, FEATURE_DIR


def main():
    events_path = RAW_META_DIR / "events.csv"
    if not events_path.exists():
        print(f"[WARN] {events_path} が無いため、イベントラベル付与はスキップします。")
        return

    feat_path = FEATURE_DIR / "lgbm_features_basic.csv"
    if not feat_path.exists():
        print(f"[WARN] {feat_path} が無いため、イベントラベル付与はスキップします。")
        return

    df_feat = pd.read_csv(feat_path, parse_dates=["date"])
    df_evt = pd.read_csv(events_path, parse_dates=["date"])

    # 想定: events.csv は columns = [date, ticker, event_type]
    df = df_feat.merge(df_evt, on=["date", "ticker"], how="left")
    # event_type が NaN のときは "none"
    df["event_type"] = df["event_type"].fillna("none")

    out_path = FEATURE_DIR / "lgbm_features_with_events.csv"
    df.to_csv(out_path, index=False)
    print(f"[OK] イベントラベル付き特徴量: {out_path}, shape={df.shape}")


if __name__ == "__main__":
    main()
