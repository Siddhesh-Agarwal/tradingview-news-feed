from urllib.parse import quote

import httpx

from tradingview.types import Economics, Feed, FeedFormat, Market, MarketSector


class TradingViewNewsFeed:
    _base_url = "https://news-mediator.tradingview.com/news-flow/v2/news"

    def __init__(
        self,
        *,
        economic_categories: list[Economics] | None = None,
        priorities: list[FeedFormat] | None = None,
        symbol: str | None = None,
        markets: list[Market] | None = None,
        market_countries: list[str] | None = None,
        sectors: list[MarketSector] | None = None,
    ):
        self.url = self._base_url
        self.url += "?filter=lang%3Aen"
        if economic_categories is not None:
            self.url += "&filter=economic_category%3A" + ",".join(
                i.value for i in economic_categories
            )
        if markets is not None and len(markets) > 0:
            self.url += "&filter=market%3A" + ",".join(i.value for i in markets)
        if priorities is not None and len(priorities) > 0:
            self.url += "&filter=priority%3A" + ",".join(i.value for i in priorities)
        if symbol is not None:
            # symbol is of the format exchange:ticker
            self.url += "&filter=symbol%3A" + quote(symbol)
        if market_countries is not None and len(market_countries) > 0:
            self.url += "&filter=market_country%3A" + ",".join(market_countries)
        if sectors is not None and len(sectors) > 0:
            self.url += "&filter=sector%3A" + ",".join(quote(i.value) for i in sectors)
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
