
from build_brokers import build_brokers
import config

brokers = build_brokers(config.TRADE_MODE, config.PAIRS, config.EXCHANGES)
bot = Arbitrage(config, brokers)
pair = ("BTC", "LTC")
bot.run_trade(pair)