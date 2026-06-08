# API Reference

Python client for TradingView's news feed API. Wraps the
`https://news-mediator.tradingview.com/news-flow/v2/news` endpoint.

> [!NOTE]
> 
> Requires Python 3.14+.

## Installation

```bash
uv add git+https://github.com:Siddhesh-Agarwal/tradingview-news-feed.git
```

Or with pip:

```bash
pip install git+https://github.com:Siddhesh-Agarwal/tradingview-news-feed.git
```

## Quickstart

```python
from tradingview import TradingViewNewsFeed

feed = TradingViewNewsFeed()
result = feed.fetch()

for item in result.items:
    print(item.title, item.published)
```

## Client

### `TradingViewNewsFeed`

Constructor parameters (all keyword-only):

|      Parameter      | Type                   | Default | Description                                                   |
| :-----------------: | ---------------------- | :-----: | ------------------------------------------------------------- |
| `economic_category` | `Economics \| None`    | `None`  | Filter by economic category                                   |
|     `priority`      | `FeedFormat \| None`   | `None`  | Filter by priority/format                                     |
|      `symbol`       | `str \| None`          | `None`  | Filter by symbol in `EXCHANGE:TICKER` format (e.g. `NSE:TCS`) |
|      `market`       | `Market \| None`       | `None`  | Filter by market type                                         |
|  `market_country`   | `list[str] \| None`    | `None`  | Filter by market country codes                                |
|      `sector`       | `MarketSector \| None` | `None`  | Filter by market sector                                       |

The client applies the following default filters:

- `lang:en`
- `client=screener`
- `streaming=false`
- `user_prostatus=non_pro`

#### Methods

**`fetch() -> Feed`**

Synchronous request. Returns a `Feed` instance. Raises `httpx.HTTPError` on transport or HTTP errors.

```python
feed = TradingViewNewsFeed(market=Market.CRYPTO)
result = feed.fetch()
```

**`fetch_async() -> Feed`**

Asynchronous equivalent. Requires an async context.

```python
import asyncio

from tradingview import TradingViewNewsFeed


async def main():
    feed = TradingViewNewsFeed(market=Market.CRYPTO)
    result = await feed.fetch_async()
    for item in result.items:
        print(item.title)


asyncio.run(main())
```

## Data Models

### `Feed`

Top-level response model.

| Field | Type | Description |
| :-----: | :--------------; | ------------------ |
| `items` | `list[FeedItem]` | List of news items |

### `FeedItem`

A single news article.

|      Field       |             Type              | Description                   |
| :--------------: | :---------------------------: | ----------------------------- |
|       `id`       |             `str`             | Unique identifier             |
|     `title`      |             `str`             | Article headline              |
|   `published`    |             `int`             | Unix timestamp of publication |
|    `urgency`     |             `int`             | Urgency level                 |
|      `link`      |       `HttpUrl \| None`       | Link to full article          |
|   `storyPath`    |             `str`             | Story path identifier         |
| `relatedSymbols` | `list[FeedItemRelatedSymbol]` | Related ticker symbols        |
|    `provider`    |      `FeedItemProvider`       | Source of the article         |

### `FeedItemProvider`

|   Field   | Type  | Description           |
| :-------: | :---: | --------------------- |
|   `id`    | `str` | Provider identifier   |
|  `name`   | `str` | Provider display name |
| `logo_id` | `str` | Logo identifier       |

### `FeedItemRelatedSymbol`

|         Field          | Type          | Description                                                  |
| :--------------------: | ------------- | ------------------------------------------------------------ |
|        `symbol`        | `str`         | Ticker symbol                                                |
|        `logoid`        | `str \| None` | Logo identifier                                              |
|   `currency_logoid`    | `str \| None` | Currency logo identifier (alias `currency-logoid`)           |
| `base_currency_logoid` | `str \| None` | Base currency logo identifier (alias `base-currency-logoid`) |

## Enums

### `FeedFormat`

|     Value     | Description    |
| :-----------: | -------------- |
|    `FLASH`    | Flash news     |
|  `INPORTANT`  | Important news |
| `TOP_STORIES` | Top stories    |
|  `KEY_FACTS`  | Key facts      |

### `Market`

|       Value        | Description |
| :----------------: | ----------- |
|      `STOCKS`      | `stock`     |
|       `ETFS`       | `etf`       |
|      `CRYPTO`      | `crypto`    |
|      `FOREX`       | `forex`     |
|     `INDICES`      | `index`     |
|     `FUTURES`      | `futures`   |
| `GOVERNMENT_BONDS` | `bond`      |
| `CORPORATE_BONDS`  | `corp_bond` |
|     `ECONOMY`      | `economic`  |

### `MarketSector`

|          Value           | Description            |
| :----------------------: | ---------------------- |
|  `COMMERCIAL_SERVICES`   | Commercial Services    |
|     `COMMUNICATIONS`     | Communications         |
|   `CONSUMER_DURABLES`    | Consumer Durables      |
| `CONSUMER_NON_DURABLES`  | Consumer Non-Durables  |
|   `CONSUMER_SERVICES`    | Consumer Services      |
| `DISTRIBUTION_SERVICES`  | Distribution Services  |
|    `ELECTRONIC_TECH`     | Electronic Technology  |
|    `ENERGY_MINERALS`     | Energy Minerals        |
|        `FINANCE`         | Finance                |
|       `GOVERNMENT`       | Government             |
|    `HEALTH_SERVICES`     | Health Services        |
|      `HEALTH_TECH`       | Health Technology      |
|  `INDUSTRIAL_SERVICES`   | Industrial Services    |
|     `MISCELLANEOUS`      | Miscellaneous          |
|  `NON_ENERGY_MINERALS`   | Non-Energy Minerals    |
|   `PROCESS_INDUSTRIES`   | Process Industries     |
| `PRODUCER_MANUFACTURING` | Producer Manufacturing |
|      `RETAIL_TRADE`      | Retail Trade           |
|     `TECH_SERVICES`      | Technology Services    |
|     `TRANSPORTATION`     | Transportation         |
|       `UTILITIES`        | Utilities              |

### `Economics`

|    Value     | Description            |
| :----------: | ---------------------- |
|    `GDP`     | Gross Domestic Product |
|   `LABOR`    | Labor                  |
|   `PRICES`   | Prices                 |
|   `HEALTH`   | Health                 |
|   `MONEY`    | Money                  |
|   `TRADE`    | Trade                  |
| `GOVERNMENT` | Government             |
|  `BUSINESS`  | Business               |
|  `CONSUMER`  | Consumer               |
|  `HOUSING`   | Housing                |
|   `TAXES`    | Taxes                  |

## Error Handling

- **`httpx.HTTPError`** — raised by `fetch()` and `fetch_async()` for connection failures, timeouts, non-2xx responses
- **`pydantic.ValidationError`** — raised during response parsing if the API returns unexpected data

Wrap calls to handle cleanly:

```python
from httpx import HTTPError
from pydantic import ValidationError

try:
    result = feed.fetch()
except HTTPError:
    print("Request failed")
except ValidationError:
    print("Unexpected response format")
```
