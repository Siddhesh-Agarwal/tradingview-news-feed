from enum import StrEnum

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
    COMMERCIAL_SERVICES = ""
    COMMUNICATIONS = ""
    CONSUMER_DURABLES = ""
    CONSUMER_NON_DURABLES = ""
    CONSUMER_SERVICES = ""
    DISTRIBUTION_SERVICES = ""
    ELECTRONIC_TECH = ""
    ENERGY_MINERALS = ""
    FINANCE = ""
    GOVERNMENT = ""
    HEALTH_SERVICES = ""
    HEALTH_TECH = ""
    INDUSTRIAL_SERVICES = ""
    MISCELLANEOUS = ""
    NON_ENERGY_MINERALS = ""
    PROCESS_INDUSTRIES = ""
    PRODUCER_MANUFACTURING = ""
    RETAIL_TRADE = ""
    TECH_SERVICES = ""
    TRANSPORTATION = ""
    UTILITIES = ""


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
        self.url = f"{self._base_url}?filter=lang%3Aen"
        if economic_category is not None:
            self.url += "&filter=economic_category%3A" + economic_category.value
        if priority is not None:
            self.url += "&filter=priority%3A" + priority.value
        if symbol is not None:
            # symbol is of the format exchange:ticker
            self.url += "&filter=symbol%3A" + symbol
        if market:
            self.url += "&filter=market%3A" + market.value
        if market_country:
            self.url += "&filter=market_country%3A" + ",".join(market_country)
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
