from __future__ import annotations

import re
import time
from typing import Any

import httpx
from pydantic import BaseModel
from pydantic import Field


def escape_markdown(text: str | None) -> str:
    """Escape special characters for Telegram MarkdownV2 format.

    Args:
        text: Text to escape, can be None

    Returns:
        Escaped text string, or empty string if input is None
    """
    if text is None:
        return ""

    pattern = r"([_*\[\]()~`>#+=|{}.!-])"
    return re.sub(pattern, r"\\\1", text)


class StockInfo(BaseModel):
    """Real-time stock information from TWSE."""

    exchange_id: str | None = Field(None, validation_alias="@")
    trade_volume: str | None = Field(None, validation_alias="tv")
    price_spread: str | None = Field(None, validation_alias="ps")
    price_id: str | None = Field(None, validation_alias="pid")
    trade_price: str | None = Field(None, validation_alias="pz")
    best_price: str | None = Field(None, validation_alias="bp")
    final_volume: str | None = Field(None, validation_alias="fv")
    best_ask_price: str | None = Field(None, validation_alias="oa")
    best_bid_price: str | None = Field(None, validation_alias="ob")
    market_percent: str | None = Field(None, validation_alias="m%")
    caret: str | None = Field(None, validation_alias="^")
    key: str | None = None
    ask_prices: str | None = Field(None, validation_alias="a")
    bid_prices: str | None = Field(None, validation_alias="b")
    symbol: str | None = Field(None, validation_alias="c")
    hash_id: str | None = Field(None, validation_alias="#")
    trade_date: str | None = Field(None, validation_alias="d")
    price_change_percent: str | None = Field(None, validation_alias="%")
    ticker: str | None = Field(None, validation_alias="ch")
    timestamp: str | None = Field(None, validation_alias="tlong")
    order_time: str | None = Field(None, validation_alias="ot")
    ask_volumes: str | None = Field(None, validation_alias="f")
    bid_volumes: str | None = Field(None, validation_alias="g")
    intraday_price: str | None = Field(None, validation_alias="ip")
    market_time: str | None = Field(None, validation_alias="mt")
    open_volume: str | None = Field(None, validation_alias="ov")
    high_price: str | None = Field(None, validation_alias="h")
    index: str | None = Field(None, validation_alias="i")
    intraday_time: str | None = Field(None, validation_alias="it")
    open_price_z: str | None = Field(None, validation_alias="oz")
    low_price: str | None = Field(None, validation_alias="l")
    name: str | None = Field(None, validation_alias="n")
    open_price: str | None = Field(None, validation_alias="o")
    price: str | None = Field(None, validation_alias="p")
    exchange: str | None = Field(None, validation_alias="ex")  # TSE or OTC
    sequence: str | None = Field(None, validation_alias="s")
    time: str | None = Field(None, validation_alias="t")
    upper_limit: str | None = Field(None, validation_alias="u")
    accumulated_volume: str | None = Field(None, validation_alias="v")
    lower_limit: str | None = Field(None, validation_alias="w")
    full_name: str | None = Field(None, validation_alias="nf")
    prev_close: str | None = Field(None, validation_alias="y")
    last_price: str | None = Field(None, validation_alias="z")
    tick_sequence: str | None = Field(None, validation_alias="ts")

    def _parse_float(self, value: str | None) -> float:
        """Parse string to float, handling None and invalid values."""
        if not value or value == "-":
            return 0.0
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def _parse_int(self, value: str | None) -> int:
        """Parse string to integer, handling None and invalid values."""
        if not value or value == "-":
            return 0
        try:
            return int(value)
        except (ValueError, TypeError):
            return 0

    def _get_mid_price(self) -> float:
        """Calculate mid price from best ask and bid prices."""
        if not self.ask_prices or not self.bid_prices:
            return 0.0

        try:
            asks = [self._parse_float(a) for a in self.ask_prices.split("_")]
            bids = [self._parse_float(b) for b in self.bid_prices.split("_")]
            if not asks or not bids:
                return 0.0

            best_ask = min(asks)
            best_bid = max(bids)

            if best_ask == 0:
                return best_bid
            if best_bid == 0:
                return best_ask

            return (best_ask + best_bid) / 2.0
        except (IndexError, ValueError):
            return 0.0

    def _get_last_price(self) -> float:
        """Get last price from trade price or mid price."""
        trade_price = self._parse_float(self.trade_price)
        return trade_price if trade_price > 0 else self._get_mid_price()

    def pretty_repr(self) -> str:
        """Format stock information in Telegram MarkdownV2 format."""
        if not self.symbol:
            return ""

        last_price = self._get_last_price()
        prev_close = self._parse_float(self.prev_close)
        net_change = ((last_price / prev_close - 1.0) * 100) if prev_close > 0 else 0.0
        net_change_symbol = "🔺" if net_change > 0 else "🔻" if net_change < 0 else "⏸️"

        # Format numbers with escaped special characters
        open_price = escape_markdown(f"{self._parse_float(self.open_price):,.2f}")
        high_price = escape_markdown(f"{self._parse_float(self.high_price):,.2f}")
        low_price = escape_markdown(f"{self._parse_float(self.low_price):,.2f}")
        last_price_str = escape_markdown(f"{last_price:,.2f}")
        net_change_str = escape_markdown(f"{net_change:+.2f}%")
        volume = escape_markdown(f"{self._parse_int(self.accumulated_volume):,}")

        return (
            f"📊 *{escape_markdown(self.name)} \\({escape_markdown(self.symbol)}\\)*\n"
            f"Open: `{open_price}`\n"
            f"High: `{high_price}`\n"
            f"Low: `{low_price}`\n"
            f"Last: `{last_price_str}`\n"
            f"Change: {net_change_symbol} `{net_change_str}`\n"
            f"Volume: `{volume}`"
        )


class QueryTime(BaseModel):
    """Query time information from TWSE."""

    sys_date: str = Field(validation_alias="sysDate")
    stock_info_item: int = Field(validation_alias="stockInfoItem")
    stock_info: int = Field(validation_alias="stockInfo")
    session_str: str = Field(validation_alias="sessionStr")
    sys_time: str = Field(validation_alias="sysTime")
    show_chart: bool = Field(validation_alias="showChart")
    session_from_time: int = Field(validation_alias="sessionFromTime")
    session_latest_time: int = Field(validation_alias="sessionLatestTime")


class StockInfoResponse(BaseModel):
    """Response from TWSE stock information API."""

    msg_array: list[StockInfo] = Field(validation_alias="msgArray")
    referer: str | None = None
    user_delay: int | None = Field(None, validation_alias="userDelay")
    rtcode: str | None = None
    query_time: QueryTime = Field(validation_alias="queryTime")
    rtmessage: str | None = None
    ex_key: str | None = Field(None, validation_alias="exKey")
    cached_alive: int | None = Field(None, validation_alias="cachedAlive")

    def pretty_repr(self) -> str:
        """Format response in Telegram MarkdownV2 format."""
        if not self.msg_array:
            return "*No stock information available*"

        result = []
        for stock in self.msg_array:
            if stock_info := stock.pretty_repr():
                result.append(stock_info)

        return "\n\n".join(result)


def build_ex_ch(symbols: list[str]) -> str:
    """Build exchange channel string for API request."""
    strings = []
    for symbol in symbols:
        if symbol.isdigit():
            strings.extend([f"tse_{symbol}.tw", f"otc_{symbol}.tw"])
        else:
            strings.append(symbol)
    return "|".join(strings)


class StockInfoRequest(BaseModel):
    symbols: list[str] = Field(
        default_factory=list,
        description="List of stock symbols to query.",
    )

    @property
    def params(self) -> dict[str, Any]:
        return {
            "ex_ch": build_ex_ch(self.symbols),
            "json": 1,
            "delay": 0,
            "_": int(time.time() * 1000),
        }

    async def do(self) -> StockInfoResponse:
        url = "https://mis.twse.com.tw/stock/api/getStockInfo.jsp"
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=self.params)
            resp.raise_for_status()
            return StockInfoResponse.model_validate(resp.json())
