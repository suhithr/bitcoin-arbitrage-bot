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
        self.trading_fee = 0.002 # The fee is 0.2% for all pairs, maker and taker
        self.bid_fee = self.trading_fee
        self.ask_fee = self.trading_fee
        self.tradeable_pairs = self.get_tradeable_pairs()
        self.minimum_amount = {}
        self.decimal_places = {}
        self.get_info()

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

        order_book['bids'] = [Order(float(b[0]), float(b[1])) for b in bids]
        order_book['asks'] = [Order(float(a[0]), float(a[1])) for a in asks]
        return order_book

    def get_min_vol(self, pair, depth):
        base, alt =  pair
        slug = base + "_" + alt
        test = self.get_validated_pair(pair)
        if test is not None:
            true_pair, swapped = test
            pairstr = "{}_{}".format(true_pair[0].lower(), true_pair[1].lower())
            return self.minimum_amount[pairstr]
            # Does swapped matter?

    def get_balance(self, currency):
        data = self.api.getInfo(connection = self.conn)
        return getattr(data, 'balance_' + currency.lower())

    def get_all_balances(self):
        balances = self.api.getBalances(self.conn)
        return balances

    # The wrapper used is outdated, so I'm writing my own function to add support for the Public Info function
    # the method info is https://btc-e.com/api/3/docs#info
    def get_info(self):
        connection = btceapi.common.BTCEConnection()
        info = connection.makeJSONRequest("/api/3/info")["pairs"]
        self.minimum_amount.update({pair :  info[pair]["min_amount"] for pair in btceapi.all_pairs})
        self.decimal_places.update({pair : info[pair]["decimal_places"] for pair in btceapi.all_pairs})
