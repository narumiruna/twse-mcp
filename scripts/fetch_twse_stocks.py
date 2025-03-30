# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "beautifulsoup4",
#     "httpx",
#     "pandas",
#     "rich",
#     "typer",
# ]
# ///
# uv run -s scripts/fetch_twse_stocks.py
from typing import Literal
from typing import TypedDict

import httpx
import pandas as pd
import typer
from bs4 import BeautifulSoup
from rich import print


class Stock(TypedDict):
    symbol: str
    name: str
    isin_code: str
    listing_date: str
    market: Literal["上市", "上櫃", "興櫃"]
    sector: Literal[
        "汽車工業",
        "航運業",
        "數位雲端",
        "運動休閒",
        "鋼鐵工業",
        "居家生活",
        "其他業",
        "電器電纜",
        "化學工業",
        "食品工業",
        "通信網路業",
        "半導體業",
        "電腦及週邊設備業",
        "紡織纖維",
        "油電燃氣業",
        "觀光餐旅",
        "金融保險業",
        "綠能環保",
        "玻璃陶瓷",
        "建材營造業",
        "水泥工業",
        "電機機械",
        "塑膠工業",
        "貿易百貨業",
        "其他電子業",
        "電子通路業",
        "資訊服務業",
        "電子零組件業",
        "造紙工業",
        "橡膠工業",
        "光電業",
        "生技醫療業",
    ]


def main(output_file: str = "twse.csv") -> None:
    url = "https://isin.twse.com.tw/isin/C_public.jsp?strMode=2"
    response = httpx.get(url, follow_redirects=True)
    response.encoding = "big5"

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.find_all("tr")

    stocks = []
    for row in rows:
        cols = [col.get_text(strip=True) for col in row.find_all("td")]

        splits = cols[0].split("　")
        if len(splits) != 2:
            continue

        stocks.append(
            Stock(
                symbol=splits[0],
                name=splits[1],
                isin_code=cols[1],
                listing_date=cols[2],
                market=cols[3],
                sector=cols[4],
            )
        )

    df = pd.DataFrame(stocks)
    print(df.head())

    print(f"Saving to {output_file}...")
    df.to_csv(output_file, index=False)


if __name__ == "__main__":
    typer.run(main)
