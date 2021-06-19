import multiprocessing
import datetime
import time
import websocket
from pprint import pprint
import loghandler
import configparser
import csv
import sys

import cbpro

from google.protobuf.json_format import MessageToDict
from pymongo import MongoClient

logger = loghandler.LogHandler().create_logger("sidebyside")

config = configparser.RawConfigParser()
config.read('config/settings.conf')

mongo_uri = f"mongodb://{config['mongodb']['host']}:{config['mongodb']['port']}"


class CryptowatchSocket:
    import cryptowatch as cw

    def __init__(self, exchange, quote, base, market_reference='./cw_market_ids.csv'):
        self.mongo = MongoClient(f"{mongo_uri}")[
            config['mongodb']['db']]['sidebyside']

        logger.info(f"{exchange}:{quote}-{base}")

        market_id = self.cw_market_lookup(
            exchange, quote, base, market_reference)

        if not market_id:
            sys.exit(1)
        else:
            logger.info(
                f"Using market id {market_id} for {exchange.lower()}-{base.lower()}{quote.lower()}")
            self.cw.stream.subscriptions = [f"markets:{market_id}:trades"]
        """self.cw.stream.subscriptions = [
            "markets:96:trades",    #
            "markets:68:trades"     #
        ]"""

        self.cw.stream.on_trades_update = self.on_message

    def cw_market_lookup(self, exchange, quote, base, market_reference):
        with open(market_reference, 'r') as market_file:
            markets = csv.DictReader(market_file)

        exchange_filter = list(
            filter(lambda exch: exch['Exchange'] == exchange.lower(), markets))
        logger.debug(f"len(exchange_filter): {len(exchange_filter)}")
        market_filter = list(filter(
            lambda mark: mark['Instrument'] == f"{base.lower()}{quote.lower()}", exchange_filter))
        logger.debug(f"len(market_filter): {len(market_filter)}")

        # If 1 result found, return it
        if len(market_filter) == 1:
            return market_filter[0]

        # If any other number of results found, log an error then return False
        elif len(market_filter) == 0:
            logger.error(
                f"No market found for {exchange.lower()}-{base.lower()}{quote.lower()}.")
        else:
            [print(mkt) for mkt in market_filter]

            logger.error(
                f"More than 1 result returned for {exchange.lower()}-{base.lower()}{quote.lower()}.")
        return False

    def on_message(self, msg):
        received_ns = time.time_ns()

        trade_doc = MessageToDict(msg)['marketUpdate']

        #trade_doc['tradesUpdate']['received_ns'] = received_ns

        for idx, trade in enumerate(trade_doc['tradesUpdate']['trades']):
            trade_doc['tradesUpdate']['trades'][idx]['timestamp'] = int(
                trade['timestamp'])
            trade_doc['tradesUpdate']['trades'][idx]['datetime'] = datetime.datetime.fromtimestamp(
                trade['timestamp'])
            trade_doc['tradesUpdate']['trades'][idx]['price'] = float(
                trade['priceStr'])
            trade_doc['tradesUpdate']['trades'][idx]['amount'] = float(
                trade['amountStr'])
            trade_doc['tradesUpdate']['trades'][idx]['timestampNano'] = int(
                trade['timestampNano'])
            trade_doc['tradesUpdate']['trades'][idx]['received_ns'] = received_ns

        pprint(trade_doc)


class KrakenSocket:
    def __init__(self, quote, base):
        self.mongo = MongoClient(f"{mongo_uri}")[
            config['mongodb']['db']]['sidebyside']

    def on_message(self, msg):
        msg['received_ns'] = time.time_ns()


class BitmexSocket:
    def __init__(self, quote, base):
        self.mongo = MongoClient(f"{mongo_uri}")[
            config['mongodb']['db']]['sidebyside']

    def on_message(self, msg):
        msg['received_ns'] = time.time_ns()


class BinanceSocket:
    def __init__(self, quote, base):
        self.mongo = MongoClient(f"{mongo_uri}")[
            config['mongodb']['db']]['sidebyside']

    def on_message(self, msg):
        msg['received_ns'] = time.time_ns()


class CoinbaseSocket:
    def __init__(self, quote, base):
        self.mongo = MongoClient(f"{mongo_uri}")[
            config['mongodb']['db']]['sidebyside']


class cbWebsocketClient(cbpro.WebsocketClient):
    def __init__(self, quote, base):
        self.mongo = MongoClient(f"{mongo_uri}")[
            config['mongodb']['db']]['sidebyside']

        self.products = ['{base}-{quote}']

    def on_open(self):
        self.url = 'wss://ws-feed.pro.coinbase.com'
        self.channels = ['ticker']
        self.message_count = 0
        #self.should_print = True

    def on_message(self, msg):
        msg['received_ns'] = time.time_ns()

        self.message_count += 1
        pprint(msg)
        if 'price' in msg and 'type' in msg:
            print(f"type: {msg['type']} - {msg['price']}")

    def on_close(self):
        logger.info('Closing websocket.')


if __name__ == '__main__':
    cryptowatch_client = CryptowatchSocket('kraken', 'eth', 'usd')
    #binance_client = BinanceSocket('eth', 'usd')
    #kraken_client = KrakenSocket('eth', 'usd')
    #coinbase_client = CoinbaseSocket('eth', 'usd')

    cryptowatch_feed = multiprocessing.Process(
        target=cryptowatch_client.cw.stream.connect, args=tuple())
    cryptowatch_feed.daemon = True

    """binance_feed = multiprocessing.Process(
        target=binance_client.start_feed, args=tuple())

    kraken_feed = multiprocessing.Process(
        target=kraken_client.start_feed, args=tuple())

    coinbase_feed = multiprocessing.Process(
        target=coinbase_client.start_feed, args=tuple())"""

    try:
        cryptowatch_feed.start()
        while True:
            time.sleep(0.1)

    except KeyboardInterrupt:
        logger.info('Exit signal received.')

    finally:
        logger.info('Joining process.')
        cryptowatch_feed.join()
