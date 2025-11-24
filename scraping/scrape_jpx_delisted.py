import pandas as pd
import requests
from bs4 import BeautifulSoup
from config.settings import RAW_META_DIR, DELISTED_CSV

URL = "https://www.jpx.co.jp/listing/stocks/delisting/index.html"


def main():
    r = requests.get(URL)
    soup = BeautifulSoup(r.text, "html.parser")

    rows = []
    for tr in soup.select("table.table_style01 tbody tr"):
        tds = tr.find_all("td")
        if len(tds) < 4:
            continue
        code = tds[0].text.strip()
        name = tds[1].text.strip()
        date = tds[2].text.strip()
        reason = tds[3].text.strip()
        rows.append([code, name, date, reason])

    df = pd.DataFrame(rows, columns=["code", "name", "delist_date", "reason"])
    df["ticker"] = df["code"].astype(str) + ".T"

    out = DELISTED_CSV
    df.to_csv(out, index=False)
    print("廃止銘柄を取得:", out)


if __name__ == "__main__":
    main()
