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
        # Just to be sure we sort the bids in descending order and asks in ascending order
        self.depth[pairstr]["bids"].sort(reverse=True)
        self.depth[pairstr]["asks"].sort(reverse=False)

    def get_highest_bid(self, pair):
        # update the depth
        self.get_depth(pair)
        pairstr = self.get_pairstr(pair)
        return self.depth[pairstr]["bids"][0]

    def get_lowest_ask(self, pair):
        # Update the depth
        self.get_depth(pair)
        pairstr = self.get_pairstr(pair)
        return self.depth[pairstr]["asks"][0]

    def update_all_balances(self):
        pass