class Order(object):
    def __init__(self, price, volume):
        self.price = price
        self.volume = volume

    def __repr__(self):
        return "Order of price : {} , volume : {}".format(self.price, self.volume)