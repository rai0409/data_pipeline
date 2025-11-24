import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import ensure_directories

# scraping
from scraping.scrape_tiingo_prices import main as scrape_prices_main

# preprocessing
from preprocessing.clean_stock_prices import main as clean_stock_main
from preprocessing.merge_panel_all import main as merge_panel_main
from preprocessing.extract_edinet_xbrl import main as extract_xbrl_main

# features
from features.build_tft_features import main as tft_feat_main
from features.build_lgbm_features import main as lgbm_feat_main
from features.label_events import main as label_events_main


def main():
    ensure_directories()

    # 1. 株価取得（Tiingo）
    try:
        scrape_prices_main()
    except Exception as e:
        print(f"[ERROR] scrape_tiingo_prices 失敗: {e}")

    # 2. 株価クリーニング
    try:
        clean_stock_main()
    except Exception as e:
        print(f"[ERROR] clean_stock_prices 失敗: {e}")

    # 3. パネル統合
    try:
        merge_panel_main()
    except Exception as e:
        print(f"[ERROR] merge_panel_all 失敗: {e}")

    # 4. XBRL（スタブ）
    try:
        extract_xbrl_main()
    except Exception as e:
        print(f"[ERROR] extract_edinet_xbrl 失敗: {e}")

    # 5. 特徴量生成（TFT / LGBM）
    try:
        tft_feat_main()
    except Exception as e:
        print(f"[ERROR] build_tft_features 失敗: {e}")

    try:
        lgbm_feat_main()
    except Exception as e:
        print(f"[ERROR] build_lgbm_features 失敗: {e}")

    # 6. イベントラベリング（events.csv があれば）
    try:
        label_events_main()
    except Exception as e:
        print(f"[ERROR] label_events 失敗: {e}")

    print("\n[INFO] main_pipeline 完了")


if __name__ == "__main__":
    main()
