import logging
import config

class Broker(object):
    def __init__(self, mode, exchange):
        super(Broker, self).__init__()
        self.mode = mode
        self.exchange = exchange

        self.balances = {}
        self.orders = [] # list of orders in the book
        self.depth = {} # "base" : ([buy orders], [sell orders])

    def get_pairstr(self, pair):
        base, alt = pair
        return base.upper() + "_" + alt.upper()

    def get_depth(self, pair):
        base, alt = pair
        pairstr = self.get_pairstr(pair)
        self.depth[pairstr] = self.exchange.get_depth(base, alt)

        # Sort the bids in descending order and asks in ascending order
        self.depth[pairstr]["bids"].sort(key=lambda x : x.price, reverse=True)
        self.depth[pairstr]["asks"].sort(key=lambda x : x.price, reverse=False)

    def get_highest_bid(self, pair):
        # self.get_depth(pair)
        pairstr = self.get_pairstr(pair)
        return self.depth[pairstr]["bids"][0]

    def get_lowest_ask(self, pair):
        # self.get_depth(pair)
        pairstr = self.get_pairstr(pair)
        return self.depth[pairstr]["asks"][0]

    def update_all_balances(self):
        if self.mode == 'paper':
            pass
        elif self.mode == 'real':
            self.balances = self.exchange.get_all_balances()
        else:
            logging.error('This mode is unsupported: ' + self.mode)

    # Only initialize balance when paper trading
    def initialize_balance(self):
        self.balances = config.INITIAL_BALANCE