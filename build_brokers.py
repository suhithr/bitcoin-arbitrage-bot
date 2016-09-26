from Broker import Broker
from btce import BTCE
import logging

def build_brokers(mode, pairs, exchanges):
    brokers = []
    # Returns array of broker objects
    for e in exchanges:
        if e == 'BTCE':
            exchange = BTCE('./btce_keys.txt')
        # elif e == 'GDAX':
        #     exchange = GDAX()
        # elif e == 'POLONIEX':
        #     exchange = POLONIEX()
        else:
            logging.error("This exchange is not yet supported : " + e)

        broker = Broker(mode, exchange)
        brokers.append(broker)

    return brokers