import multiprocessing
import time
import websocket


class CryptowatchSocket:
    def __init__(self, exchange, quote, base):
        pass


class KrakenSocket:
    def __init__(self, quote, base):
        pass


class BitmexSocket:
    def __init__(self, quote, base):
        pass


class BinanceSocket:
    def __init__(self, quote, base):
        pass


class cbWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url = 'wss://ws-feed.pro.coinbase.com'
        self.products = ['ETH-USD']
        self.mongo_collection = trade_collection
        self.channels = ['ticker']
        self.message_count = 0
        #self.should_print = True

    def on_message(self, msg):
        self.message_count += 1
        pprint(msg)
        if 'price' in msg and 'type' in msg:
            print(f"type: {msg['type']} - {msg['price']}")

    def on_close(self):
        logger.info('Closing websocket.')


class CoinbaseSocket:
    def __init__(self, quote, base):
        pass


if __name__ == '__main__':
    kraken_client = KrakenSocket('eth', 'usd')
    cryptowatch_client = CryptowatchSocket('kraken', 'eth', 'usd')
    binance_client = BinanceSocket('eth', 'usd')
    coinbase_client = CoinbaseSocket('eth', 'usd')

    kraken_feed = multiprocessing.Process(
        target=kraken_client.start_feed, args=tuple()
    )

    cryptowatch_feed = multiprocessing.Process(
        target=cryptowatch_client.start_feed, args=tuple()
    )

    binance_feed = multiprocessing.Process(
        target=binance_client.start_feed, args=tuple()
    )

    coinbase_feed = multiprocessing.Process(
        target=coinbase_client.start_feed, args=tuple()
    )
