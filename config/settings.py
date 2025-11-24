from pathlib import Path
from dotenv import load_dotenv
import os

ENV_PATH = PROJECT_ROOT / ".env"
if ENV_PATH.exists():
    load_dotenv(ENV_PATH)

TIINGO_API_KEY = os.getenv("TIINGO_API_KEY")
# プロジェクトルート（このファイルから見て1つ上の階層）
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# データパス
DATA_RAW_DIR = PROJECT_ROOT / "data_raw"
DATA_CLEAN_DIR = PROJECT_ROOT / "data_clean"
LOG_DIR = PROJECT_ROOT / "logs"
CONFIG_DIR = PROJECT_ROOT / "config"

# サブカテゴリ
RAW_STOCK_DIR = DATA_RAW_DIR / "stock"
RAW_MACRO_DIR = DATA_RAW_DIR / "macro"
RAW_FUND_DIR = DATA_RAW_DIR / "fundamentals"
RAW_META_DIR = DATA_RAW_DIR / "metadata"

CLEAN_STOCK_DIR = DATA_CLEAN_DIR / "stock"
CLEAN_MACRO_DIR = DATA_CLEAN_DIR / "macro"
FEATURE_DIR = DATA_CLEAN_DIR / "features"

# 設定ファイル
TOPIX1000_TICKERS_CSV = CONFIG_DIR / "tickers_topix1000.csv"
MACRO_SOURCES_YAML = CONFIG_DIR / "macro_sources.yaml"

# ログ
LOG_FILE = LOG_DIR / "data_pipeline.log"

# Tiingo API
TIINGO_API_KEY = os.getenv("TIINGO_API_KEY", "")


def ensure_directories() -> None:
    """必要なディレクトリを一括作成"""
    for p in [
        DATA_RAW_DIR,
        DATA_CLEAN_DIR,
        RAW_STOCK_DIR,
        RAW_MACRO_DIR,
        RAW_FUND_DIR,
        RAW_META_DIR,
        CLEAN_STOCK_DIR,
        CLEAN_MACRO_DIR,
        FEATURE_DIR,
        LOG_DIR,
    ]:
        p.mkdir(parents=True, exist_ok=True)
