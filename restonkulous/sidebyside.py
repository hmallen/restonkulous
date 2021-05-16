import multiprocessing
import time
import websocket


class TradeSocket:
    def __init__(self, exchange, quote, base):
        pass


if __name__ == '__main__':
    kraken_client = TradeSocket('kraken', 'eth', 'usd')
    cryptowatch_client = TradeSocket('cryptowatch', 'eth', 'usd')

    kraken_feed = multiprocessing.Process(
        target=kraken_client.start_feed, args=tuple()
    )

    cryptowatch_feed = multiprocessing.Process(
        target=cryptowatch_client.start_feed, args=tuple()
    )
