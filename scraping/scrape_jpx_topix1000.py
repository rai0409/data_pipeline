# scraping/scrape_jpx_topix1000.py
import pandas as pd
from pathlib import Path
import requests
from io import BytesIO

# JPX TOPIX1000 Excel URL（公式）
JPX_TOPIX1000_URL = "https://www.jpx.co.jp/markets/indices/topix/files/topix1000_j.xls"

def download_topix1000_tickers(out_csv_path: Path):
    print("[INFO] JPX TOPIX1000 Excel をダウンロード中...")

    response = requests.get(JPX_TOPIX1000_URL)
    response.raise_for_status()

    # Excel 読み込み
    df = pd.read_excel(BytesIO(response.content))

    # JPX の列名が環境により違う場合があるので rename を柔軟に処理
    rename_map = {
        "コード": "code",
        "銘柄名": "name",
        "市場": "market",
    }
    df = df.rename(columns=rename_map)

    if "code" not in df.columns:
        raise RuntimeError("JPX Excel に 'コード' 列が見つかりません。形式変更の可能性。")

    # ticker形式へ（例: 7203 → 7203.T）
    df["ticker"] = df["code"].astype(str).str.zfill(4) + ".T"

    # 必須列だけ抽出
    out_df = df[["ticker", "name"]].copy()

    # 保存
    out_csv_path.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(out_csv_path, index=False, encoding="utf-8")

    print(f"[INFO] TOPIX1000 CSV を生成しました: {out_csv_path}")
    print(out_df.head())


if __name__ == "__main__":
    # 保存先：data_pipeline/config/tickers_topix1000.csv
    project_root = Path(__file__).resolve().parents[1]
    out_csv = project_root / "config" / "tickers_topix1000.csv"

    download_topix1000_tickers(out_csv)
