from urllib.parse import quote

import httpx

from tradingview.types import Economics, Feed, FeedFormat, Market, MarketSector


class TradingViewNewsFeed:
    _base_url = "https://news-mediator.tradingview.com/news-flow/v2/news"

    def __init__(
        self,
        *,
        economic_category: Economics | None = None,
        priority: FeedFormat | None = None,
        symbol: str | None = None,
        market: Market | None = None,
        market_country: list[str] | None = None,
        sector: MarketSector | None = None,
    ):
        self.url = self._base_url
        self.url += "?filter=lang%3Aen"
        if economic_category is not None:
            self.url += "&filter=economic_category%3A" + economic_category.value
        if market is not None:
            self.url += "&filter=market%3A" + market.value
        if priority is not None:
            self.url += "&filter=priority%3A" + priority.value
        if symbol is not None:
            # symbol is of the format exchange:ticker
            self.url += "&filter=symbol%3A" + quote(symbol)
        if market_country is not None:
            self.url += "&filter=market_country%3A" + ",".join(market_country)
        if sector is not None:
            self.url += "&filter=sector%3A" + quote(sector.value)
        self.url += "&client=screener"
        self.url += "&streaming=false"
        self.url += "&user_prostatus=non_pro"
        print(self.url)

    def fetch(self) -> Feed:
        with httpx.Client() as client:
            response = client.get(self.url)
            response.raise_for_status()
            return Feed.model_validate_json(response.text, strict=True)

    async def fetch_async(self) -> Feed:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.url)
            response.raise_for_status()
            return Feed.model_validate_json(response.text, strict=True)
