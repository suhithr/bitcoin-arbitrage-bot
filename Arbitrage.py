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
        base, alt = pair
        profit = Profit(self.brokers, pair)
        # Make into function
        profit.check_spread()
        # find the trade if they exist
        # print the info
        for pair in self.config.PAIRS:
            for broker in self.brokers:
                # Update balances for each currency in the broker object
                broker.update_all_balances()