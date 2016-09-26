from Exchange import Exchange
from Order import Order
import btceapi
import os
import logging

class BTCE(Exchange):
    def __init__(self, keypath):
        keyfile = os.path.abspath(keypath)
        self.keyhandler = btceapi.KeyHandler(keyfile)
        key = self.keyhandler.getKeys()[0]
        self.conn  = btceapi.BTCEConnection()
        self.api = btceapi.TradeAPI(key, self.keyhandler)

        self.name = 'BTCE'
        self.trading_fee = 0.2 # The fee is 0.2% for all pairs, maker and taker
        self.tradeable_pairs = self.get_tradeable_pairs()

    def get_tradeable_pairs(self):
        tradeable_pairs = []
        for pair in btceapi.all_pairs:
            a, b = pair.split("_")
            tradeable_pairs.append((a.upper(), b.upper()))
        return tradeable_pairs

    def get_depth(self, base, alt):
        order_book = {'bids': [], 'asks': []}
        pair, swapped = self.get_validated_pair((base, alt))
        if pair is None:
            return

        pairstr = pair[0].lower() + "_" + pair[1].lower()
        if swapped:
            bids, asks = btceapi.getDepth(pairstr)
        else:
            asks, bids = btceapi.getDepth(pairstr)

        print pairstr + "----------"

        print "BTCE.get_depth : asks -> "
        print asks
        print " -> bids -> "
        print bids

        order_book['bids'] = [Order(float(b[0]), float(b[1])) for b in bids]
        order_book['asks'] = [Order(float(a[0]), float(a[1])) for a in asks]

        return order_book

    def get_min_vol(self, pair, depth):
        base, alt =  pair
        slug = base + "_" + alt
        test = self.get_validated_pair(pair)
        if test is not None:
            true_pair, swapped = test
            if not swapped:
                return 0.1
            else:
                # Use depth to find out how much alt to trade
                # to fulfill min base vol
                return self.get_clipped_alt_volume(depth, 0.101)

    def get_balance(self, currency):
        data = self.api.getInfo(connection = self.conn)
        return getattr(data, 'balance_' + currency.lower())

    def get_all_balances(self):
        balances = self.api.getBalances(self.conn)
        return balances

