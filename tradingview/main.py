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
        self.url += quote("?filter=lang:en")
        if economic_category is not None:
            self.url += quote("&filter=economic_category:" + economic_category.value)
        if priority is not None:
            self.url += quote("&filter=priority:" + priority.value)
        if symbol is not None:
            # symbol is of the format exchange:ticker
            self.url += quote("&filter=symbol:" + symbol)
        if market is not None:
            self.url += quote("&filter=market:" + market.value)
        if market_country:
            self.url += quote("&filter=market_country:" + ",".join(market_country))
        if sector is not None:
            self.url += quote("&filter=sector:" + sector.value)
        self.url += "&client=screener"
        self.url += "&streaming=false"
        self.url += "&user_prostatus=non_pro"
        print(self.url)

    def fetch(self) -> Feed:
        with httpx.Client() as client:
            response = client.get(self.url)
            response.raise_for_status()
            return Feed.model_validate(response.json())

    async def fetch_async(self) -> Feed:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.url)
            response.raise_for_status()
            return Feed.model_validate(response.json())
