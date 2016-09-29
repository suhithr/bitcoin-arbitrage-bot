import config
import logging

class Profit(object):
    def __init__(self, brokers, pair):
        self.brokers = brokers
        self.pair = pair # (bidderexchange, askerexchange)
        self.spread = {} # maintains the profit spread matrix for a pair between all exchanges
        self.prices = {} # maintains high bids and low asks for each exchange

        self.build_profit_spread()

    def build_profit_spread(self):
        self.spread = { b.exchange.name : { a.exchange.name : 0 for a in self.brokers } for b in self.brokers} # { bidder : {asker, spread} }
        self.prices = { b.exchange.name : { "bid" : b.get_highest_bid(self.pair),
                                         "ask" : b.get_lowest_ask(self.pair)} for b in self.brokers}

        for bidder in self.brokers:
            for asker in self.brokers:
                bid_price = self.prices[bidder.exchange.name]["bid"]
                ask_price = self.prices[asker.exchange.name]["ask"]

                if bid_price is None or ask_price is None:
                    self.spread[bidder.exchange.name][asker.exchange.name] = None
                else:
                    self.spread[bidder.exchange.name][asker.exchange.name] = self.calc_profit_spread(bid_price.price, bidder.exchange.bid_fee, ask_price.price, asker.exchange.ask_fee)

        # self.print_spread()

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
        for key, asker_spread in self.spread.iteritems():
            print key
            for k, val in asker_spread.iteritems():
                print k
                print val

    def calc_real_profit(self, bidder, asker, bids, asks, pair):
        # Since we are only trying to fulfill trades with the first order from the book
        # We check if that order satisfies minimum volume
        # It's probably safe to assume orders placed are valid :/
        min_bid_vol = bidder.exchange.get_min_vol(pair, bidder.depth)
        min_ask_vol = asker.exchange.get_min_vol(pair, asker.depth)

        asker_factor = 1.0 - asker.exchange.ask_fee
        bidder_factor = 1.0 - bidder.exchange.bid_fee
        base, alt = pair

        # We want to fulfill the order using the best prices so we trade with the least volume on offer
        # vol_reqd is the volume of alt we need
        vol_reqd = min(asks[0].volume * asker_factor, bids[0].volume)

        # TODO: Check with balance of each currency and volume to find the optimized volume_required

        if min_bid_vol < vol_reqd and min_ask_vol < vol_reqd:
            # Check if we have enough balance in each exchange
            if (asker.balances[base] >= (vol_reqd/asker_factor) * asks[0].volume) and (bidder.balances[alt] >= vol_reqd):
                spent_btc_at_asker = (vol_reqd/asker_factor) * asks[0].price
                gained_btc_at_bidder = vol_reqd * bids[0].price * bidder_factor
                profit = gained_btc_at_bidder - spent_btc_at_asker

                # TODO: Add a check to make sure we don't move too much currency relative to the profit

                if profit > config.MINIMUM_PROFIT_VOLUME["BTC"]:
                    print "SUCCESS -> Arbitrage oppurtunity discovered"
                    print "Buy {} of {} of which lowest ask is {} for {} of {}".format(vol_reqd, alt, asker.exchange.name ,asks[0].price, base)
                    print "Sell {} of {} of which highest bid is {} for {} of {}".format(vol_reqd, alt, bidder.exchange.name, bids[0].price, base)
                    print "PROFIT: {} of {}".format(profit, base)
            else:
                logging.error("The balance in the exchanges was not enough to make a trade")
        else:
            logging.error("Not enough volume for the exchange")

    def check_spread(self):
        for bidder in self.brokers:
            for asker in self.brokers:
                profit_spread = self.spread[bidder.exchange.name][asker.exchange.name]
                base, alt = self.pair
                # Check if spread's greater than minimum profit
                if profit_spread is not None and profit_spread >= config.MINIMUM_PROFIT_VOLUME[base]:
                    # Check depth

                    bids = bidder.depth[base + "_" + alt]["bids"]
                    asks = asker.depth[base + "_" + alt]["asks"]
                    self.calc_real_profit(bidder, asker, bids, asks, self.pair)