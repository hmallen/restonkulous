from google.protobuf.json_format import MessageToJson
import cryptowatch as cw

# Set your API Key
# cw.api_key = "123"

# Subscribe to resources (https://docs.cryptowat.ch/websocket-api/data-subscriptions#resources)
cw.stream.subscriptions = ["markets:68:trades"]

# What to do on each trade update


def handle_trades_update(trade_update):
    """
        trade_update follows Cryptowatch protocol buffer format:
        https://github.com/cryptowatch/proto/blob/master/public/markets/market.proto
    """
    MessageToJson(trade_update)


cw.stream.on_trades_update = handle_trades_update


# Start receiving
cw.stream.connect()
