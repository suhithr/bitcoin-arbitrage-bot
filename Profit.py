import config

class Profit(object):
    def __init__(self, brokers, pair):
        self.brokers = brokers
        self.pair = pair # (bidderexchange, askerexchange)
        self.spread = {} # maintains the profit spread matrix for a pair between all exchanges
        self.prices = {} # maintains high bids and low asks for each exchange

        self.build_profit_spread()

    def build_profit_spread(self):
        self.prices = { b.exchange.name : { "bid" : b.get_highest_bid(self.pair),
                                         "ask" : b.get_lowest_ask(self.pair)} for b in self.brokers}
        for bidder in self.brokers:
            for asker in self.brokers:
                bid_price = self.prices[bidder.exchange.name]["bid"]
                ask_price = self.prices[asker.exchange.name]["ask"]
                if bid_price or ask_price is None:
                    self.spread[bidder][asker] = None
                else:
                    self.spread[bidder][asker] = self.calc_profit_spread(bid_price, bidder.exchange.bid_fee, ask_price, asker.exchange.ask_fee)

        self.print_spread()

    def calc_profit_spread(self, bid_price, bidder_fee, ask_price, asker_fee):
        # This formula is representative of the spread and doesn't take order volume into account
        # Basically if high_bid = 510 and low_ask = 500
        # With the high_bid you will be able to to get the amount of 510 if you sell .998 of alt because of the fee
        # So we need to buy exactly .998 of alt from base of which .998 of this is only effective
        # Basically whatever we spend to buy alt using base we only get .998 for 1
        # Since 500 * .002 = 1 (fee)
        # so we have 500 - 1 = 499 base to spend
        # We get 499 / 500 of alt = .998 alt
        # Now this is the true price per 1 alt
        # Now we have .998 of alt to sell at a rate of 510 with a fee
        # so (.998 * 510) - (.998 * .002 * 510) = Amt of money got for that amt of alt - fee charged on the received money
        # therefore = .998 * .998 * 510 = 507.9624
        # There for profit spread in this case is 507.9624 - 500
        return ((1.0 - bidder_fee) * (1.0 - asker_fee) * bid_price) - ask_price

    def print_spread(self):
        for key, value in self.spread:
            print key
            for k, val in value:
                print k
                print val

    def check_spread(self):
        for bidder in self.brokers:
            for asker in self.brokers:
                profit_spread = self.spread[bidder.exchange.name][asker.exchange.name]
                # Check if spread's greater than minimum profit
                if profit_spread is not None and profit_spread >= config.MINIMUM_PROFIT:
                    # Check depth
                    base, alt = self.pair
                    bids = bidder.depth[base + "_" + alt]["bids"]
                    asks = asker.depth[base + "_" + alt]["asks"]
                    real_profit = calc_real_profit(bidder, asker, bids, asks)