import cryptowatch as cw
import datetime
from google.protobuf.json_format import MessageToDict
from pymongo import MongoClient
from pprint import pprint
import logging
import sys


logging.basicConfig()
logging.getLogger("cryptowatch").setLevel(logging.INFO)

db = MongoClient(
    host='localhost',
    port=27017
).cryptowatch
trade_coll = db.trades

# Set your API Key (Read from ~/.cw/credentials.yml by default)
# cw.api_key = "XXXXXXXXXXXXXXXXXXXX"

# cw.stream.subscriptions = ["markets:*:trades", "markets:*:ohlc"]
# cw.stream.subscriptions = ["assets:60:book:snapshots"]
# cw.stream.subscriptions = ["assets:60:book:spread"]
# cw.stream.subscriptions = ["assets:60:book:deltas"]
# cw.stream.subscriptions = ["markets:*:ohlc"]
# cw.stream.subscriptions = ["markets:*:trades"]
cw.stream.subscriptions = ["markets:96:trades", "markets:68:trades"]


# What to do with each trade update
def handle_trades_update(trade_update):
    trade_doc = MessageToDict(trade_update)['marketUpdate']

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

    print(f'New trade doc: {trade_coll.insert_one(trade_doc).inserted_id}')

    pprint(trade_doc)


cw.stream.on_trades_update = handle_trades_update


# What to do with each candle update
def handle_intervals_update(interval_update):
    print(interval_update)


cw.stream.on_intervals_update = handle_intervals_update


# What to do with each orderbook spread update
def handle_orderbook_snapshot_updates(orderbook_snapshot_update):
    print(orderbook_snapshot_update)


cw.stream.on_orderbook_snapshot_update = handle_orderbook_snapshot_updates


# What to do with each orderbook spread update
def handle_orderbook_spread_updates(orderbook_spread_update):
    print(orderbook_spread_update)


cw.stream.on_orderbook_spread_update = handle_orderbook_spread_updates


# What to do with each orderbook delta update
def handle_orderbook_delta_updates(orderbook_delta_update):
    print(orderbook_delta_update)


cw.stream.on_orderbook_delta_update = handle_orderbook_delta_updates


if __name__ == '__main__':
    try:
        # Start receiving
        cw.stream.connect()

    except KeyboardInterrupt:
        # Stop receiving
        cw.stream.disconnect()
        sys.exit()
