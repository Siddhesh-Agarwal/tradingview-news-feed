from tradingview import TradingViewNewsFeed, FeedFormat, Market

feed = TradingViewNewsFeed(priority=FeedFormat.INPORTANT, market=Market.STOCKS, symbol="NSE:TCS")
res = feed.fetch()
print(res.model_dump_json(indent=4))