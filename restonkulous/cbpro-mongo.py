# import PyMongo and connect to a local, running Mongo instance
from pymongo import MongoClient
import cbpro
import time
import logging
from pprint import pprint
import sys

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

mongo_client = MongoClient(
    host='localhost',
    port=27017
)

# specify the database and collection
db = mongo_client['cbpro']
trade_collection = db['ethusd']


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


if __name__ == '__main__':
    # instantiate a WebsocketClient instance, with a Mongo collection as a parameter
    wsClient = cbWebsocketClient()
    wsClient.start()
    print(wsClient.url, wsClient.products)

    try:
        while (wsClient.message_count < 25):
            # print(wsClient.message_count)
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info('Exit signal received.')

    except Exception as e:
        logger.exception(e)

    finally:
        wsClient.close()
        sys.exit()
