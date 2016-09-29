EXCHANGES = ['BTCE']
# , 'BITFINEX', 'POLOINEX', 'BTCC','GDAX'

# BTCC Can only do LTC BTC
PAIRS = [("BTC","LTC"),("BTC","ETH")]

BALLPARK_VALUE = {
    "BTC" : 580,
    "LTC" : 3,
    "ETH" : 12
} # Ballpark value of each currency in USD

MINIMUM_PROFIT_VOLUME = { key : 0.01/value for (key, value) in BALLPARK_VALUE.iteritems()} # {"currency" : "minimum profit} we want the equivalent of 0.01 dollars

TRADE_MODE = "paper" # paper or real

# Initial balance of each currency, used in paper trading mode
INITIAL_BALANCE = {
    "BTC" : 0,
    "LTC" : 0,
    "ETH" : 0
}