from enum import StrEnum

from pydantic import BaseModel, Field, HttpUrl, field_validator


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
    IMPORTANT = "important"
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
    logoid: str | None = None
    currency_logoid: str | None = Field(alias="currency-logoid", default=None)
    base_currency_logoid: str | None = Field(alias="base-currency-logoid", default=None)


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
    storyPath: HttpUrl
    relatedSymbols: list[FeedItemRelatedSymbol] = Field(default_factory=list)
    provider: FeedItemProvider

    @field_validator("storyPath", mode="before")
    @classmethod
    def make_full_url(cls, v: str | None) -> HttpUrl | None:
        if v is None:
            return None
        return HttpUrl(url=f"https://www.tradingview.com{v}")


class Feed(BaseModel):
    items: list[FeedItem]
