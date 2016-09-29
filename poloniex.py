# Under construction
from Exchange import Exchange
import poloniex
import config_key

class POLONIEX(Exchange):
    def __init__(self):
        self.name = 'POLONIEX'
        self.public_api = poloniex.Poloniex()
        self.private_api = poloniex.Poloniex(config_key.poloniex_api_key, config_key.poloniex_secret_key)
        # This is the taker fee for a 30 day volume of <600BTC
        # in this arbitrage strategy we do not make orders, only fill(take) existing ones thus we apply the taker fee
        self.trading_fee = 0.25

    def get_tradeable_pairs(self):
        tradeable_pairs = []
        # we just fetch the 24hour volume for all  markets and read keys
        vol = self.public_api.marketVolume()
        for key in vol:
            a, b = key.split("_")
            tradeable_pairs.append((a.upper(), b.upper()))
        return tradeable_pairs

    def get_depth(self, base, alt):
        order_book = {'bids': [], 'asks': []}
        pair, swapped = self.get_validated_pair((base, alt))
        if pair is None:
            return

        pairstr = pair[0].upper() + "_" + pair[1].upper()
        # Get orderbook to a depth of 150 since that's the default in the BTCE API
        if swapped:
            bids, asks = self.public_api.marketOrders(pairstr, 150)
        else:
            asks, bids = self.public_api.marketOrders(pairstr, 150)

    def get_min_vol(self, pair, depth):
        base, alt = pair
