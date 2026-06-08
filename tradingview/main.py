from enum import StrEnum
from urllib.parse import quote

import httpx
from pydantic import BaseModel, Field, HttpUrl


class Market(StrEnum):
    STOCKS = "stock"
    ETFS = "etf"
    CRYPTO = "crypto"
    FOREX = "forex"
    INDICES = "index"
    FUTURES = "futures"
    GOVERNMENT_BONDS = "bond"
    CORPORATE_BONDS = "corp_bond"
    ECONOMY = "economic"


class MarketSector(StrEnum):
    COMMERCIAL_SERVICES = "Commercial Services"
    COMMUNICATIONS = "Communications"
    CONSUMER_DURABLES = "Consumer Durables"
    CONSUMER_NON_DURABLES = "Consumer Non-Durables"
    CONSUMER_SERVICES = "Consumer Services"
    DISTRIBUTION_SERVICES = "Distribution Services"
    ELECTRONIC_TECH = "Electronic Technology"
    ENERGY_MINERALS = "Energy Minerals"
    FINANCE = "Finance"
    GOVERNMENT = "Government"
    HEALTH_SERVICES = "Health Services"
    HEALTH_TECH = "Health Technology"
    INDUSTRIAL_SERVICES = "Industrial Services"
    MISCELLANEOUS = "Miscellaneous"
    NON_ENERGY_MINERALS = "Non-Energy Minerals"
    PROCESS_INDUSTRIES = "Process Industries"
    PRODUCER_MANUFACTURING = "Producer Manufacturing"
    RETAIL_TRADE = "Retail Trade"
    TECH_SERVICES = "Technology Services"
    TRANSPORTATION = "Transportation"
    UTILITIES = "Utilities"


class FeedFormat(StrEnum):
    FLASH = "flash"
    INPORTANT = "important"
    TOP_STORIES = "top_stories"
    KEY_FACTS = "key_facts"


class Economics(StrEnum):
    GDP = "gdp"
    LABOR = "labor"
    PRICES = "prices"
    HEALTH = "health"
    MONEY = "money"
    TRADE = "trade"
    GOVERNMENT = "government"
    BUSINESS = "business"
    CONSUMER = "consumer"
    HOUSING = "housing"
    TAXES = "taxes"


class FeedItemRelatedSymbol(BaseModel):
    symbol: str
    logoid: str


class FeedItemProvider(BaseModel):
    id: str
    name: str
    logo_id: str


class FeedItem(BaseModel):
    id: str
    title: str
    published: int
    urgency: int
    link: HttpUrl | None = None
    storyPath: str
    relatedSymbols: list[FeedItemRelatedSymbol] = Field(default_factory=list)
    provider: FeedItemProvider


class Feed(BaseModel):
    items: list[FeedItem]


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
