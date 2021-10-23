"""
To run this script:
poetry run main --config-name config

Adapted from: https://larshaendler.medium.com/4-things-to-do-before-writing-code-in-any-project-868ed2d575ef
"""

# TODO does this make sense as an experiment or should it be a separate utility?

import traceback
import os
import logging
from omegaconf import DictConfig
import ccxt
import pandas as pd

log = logging.getLogger(__name__)

def run(cfg: DictConfig) -> None:
    """Entry point to experiment

    Args:
        cfg (DictConfig): [description]
    """
    t_frame = '1d'  # 1-day timeframe, usually from 1-minute to 1-week depending on the exchange
    # TODO works fine when run directly, need to handle when run as experiment
    data_base_path = '../../data'

    log.debug(f"Exchanges: {ccxt.exchanges}")

    # Get exchange and authenticate to Coinbase Pro
    try:
        exchange = ccxt.coinbasepro(
            {
                "apiKey": os.environ.get("COINBASE_PRO_API_KEY"),
                "secret": os.environ.get("COINBASE_PRO_API_SECRET"),
                "password": os.environ.get("COINBASE_PRO_API_PASSPHRASE")
            }
        )
    except AttributeError:
        log.error(f'Failed to create exchange for Coinbase Pro.')
        return

    # Check if fetching of OHLC Data is supported
    if not exchange.has["fetchOHLCV"]:
        log.error(f'CoinbasePro does not support fetching OHLCV data. Please use another  exchange')
        return

    # Check requested timeframe is available. If not return a helpful error.
    if (not hasattr(exchange, 'timeframes')) or (t_frame not in exchange.timeframes):
        log.error(
            f'The requested timeframe ({t_frame}) is not available from CoinbasePro. Available timeframes are: {exchange.timeframes.keys()}')
        return

    exchange.load_markets()

    log.info(f'Coinbase Pro available symbols: {exchange.symbols}')

    # Get data
    header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']

    for coin in exchange.symbols:
        try:
            log.info(f"Fetching data for {coin}")
            data = exchange.fetch_ohlcv(coin, t_frame)
            df = pd.DataFrame(data, columns=header).set_index('Timestamp')
            df['symbol'] = coin
            filename = os.path.join(data_base_path, f'{coin.replace("/", "_")}_{t_frame}.csv')
            df.index = df.index / 1000  # Timestamp is 1000 times bigger than it should be in this case
            df['Date'] = pd.to_datetime(df.index, unit='s')
            df.to_csv(filename)
            log.info(f"{coin} data saved to {filename}")
        except Exception as error:
            log.error(f'Failed to fetch {coin} with exception {traceback.print_exc()}')
            continue


# make it easy to just run this file to download data
if __name__ == "__main__":
    # default logging level is WARN, but if we're running like this we probably want everything
    logging.basicConfig(level=logging.DEBUG)
    run({})
