from Arbitrage import Arbitrage
from build_brokers import build_brokers
import config

brokers = build_brokers(config.TRADE_MODE, config.PAIRS, config.EXCHANGES)
bot = Arbitrage(config, brokers)
# TODO: Loop for the bot to fetch data and make calculations once every couple of seconds
for pair in config.PAIRS:
    bot.run_trade(pair)