from Profit import Profit
# Runs the arbitrage strategy

# Make it Arbitrage(Bot) , write a bot baseclass
class Arbitrage(object):
    def __init__(self, config, brokers):
        super(Arbitrage, self).__init__()
        self.config = config
        self.brokers = brokers

        if self.config.TRADE_MODE == 'paper':
            for broker in self.brokers:
                broker.initialize_balance()

    def run_trade(self, pair):
        for broker in self.brokers:
            broker.get_depth(pair)
        base, alt = pair
        print "Searching for arbitrage in the {}_{} market".format(base, alt)
        profit = Profit(self.brokers, pair)
        # Checks for existence of profitable trades
        profit.check_spread()
        # TODO: Have check spread return data, and print handled by a seperate function
        # TODO: Implement actual balance calculations even for Paper trading
        # for pair in self.config.PAIRS:
        #     for broker in self.brokers:
        #         # Update balances for each currency in the broker object
        #         broker.update_all_balances()