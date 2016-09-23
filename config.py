EXCHANGES = ['BTCE', 'BITFINEX', 'POLOINEX', 'BTCC','GDAX']

# BTCC Can only do LTC BTC
PAIRS = [("LTC","BTC"),("ETH","BTC")]

BALLPARK_VALUE = {
    "BTC" : 580,
    "LTC" : 3,
    "ETH" : 12
} # Ballpark value of each currency in USD

MINIMUM_PROFIT = { 0.01/value for key, value in BALLPARK_VALUE } # {"currency" : "minimum profit} we want the equivalent of 0.01 dollars

TRADE_MODE = "paper" # paper or real