import cryptowatch as cw
import sys

# Set your API Key (Read from ~/.cw/credentials.yml by default)
# cw.api_key = "123"

# Subscribe to resources (https://docs.cryptowat.ch/websocket-api/data-subscriptions#resources)
# cw.stream.subscriptions = ["markets::trades"]
cw.stream.subscriptions = ["markets:96:trades", "markets:68:trades"]

# What to do on each trade update


def handle_trades_update(trade_update):
    """
        trade_update follows Cryptowatch protocol buffer format:
        https://github.com/cryptowatch/proto/blob/master/public/markets/market.proto
    """
    market_msg = ">>> Market#{} Exchange#{} Pair#{}: {} New Trades".format(
        trade_update.marketUpdate.market.marketId,
        trade_update.marketUpdate.market.exchangeId,
        trade_update.marketUpdate.market.currencyPairId,
        len(trade_update.marketUpdate.tradesUpdate.trades),
    )
    print(market_msg)
    for trade in trade_update.marketUpdate.tradesUpdate.trades:
        trade_msg = "\tID:{} TIMESTAMP:{} TIMESTAMPNANO:{} PRICE:{} AMOUNT:{}".format(
            trade.externalId,
            trade.timestamp,
            trade.timestampNano,
            trade.priceStr,
            trade.amountStr,
        )
        print(trade_msg)


cw.stream.on_trades_update = handle_trades_update


if __name__ == '__main__':
    try:
        # Start receiving
        cw.stream.connect()

    except KeyboardInterrupt:
        # Call disconnect to close the stream connection
        cw.stream.disconnect()
        sys.exit()
