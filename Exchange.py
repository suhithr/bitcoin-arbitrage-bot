'''
Abstract class for all Exchanges
'''
import abc
class Exchange(object):

    def __init__(self):
        super(Exchange, self).__init__()
        self.name = None
        self.trading_fee = None
        self.ok =True
        self.tradeable_pairs = self.get_tradeable_pairs()

    def get_validated_pair(self, pair):
        # Checks for existence of supported pain in exchange
        base, alt = pair
        if pair in self.tradeable_pairs:
            return (pair, False)
        elif (alt, base) in self.tradeable_pairs:
            return ((alt, base), True)
        else:
            # pair is not traded
            return None

    def get_min_vol(self, pair, depth):
        base, alt = pair
        test = self.get_validated_pair(pair)
        if test is not None:
            true_pair, swapped = test
            if not swapped:
                return 0.01
            # TODO: Implement the alternate function
            else:
                return get_converted_alt_volume()