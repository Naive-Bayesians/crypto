"""
To run this script:
poetry run main --config-name trading
"""
import os
import logging
from omegaconf import DictConfig
import ccxt
from ccxt.base.exchange import Exchange
import schedule
from datetime import datetime, timedelta, time
import pandas as pd

# Amount of money you're willing to buy bitcoin at
C_BITCOIN_BUY_ORDER_LIMIT = 100000

log = logging.getLogger(__name__)


def run(cfg: DictConfig) -> None:
    """Entry point to experiment

    Args:
        cfg (DictConfig): Config
    """
    log.debug("Welcome to simple trading bot")

    exchange = connect_to_exchange(cfg=cfg)

    show_balance(exchange=exchange)

    # Run strategy
    schedule.every(1).minutes.until(timedelta(minutes=5)).do(
        job, exchange=exchange, cfg=cfg
    )
    while True:
        schedule.run_pending()
        if not schedule.jobs:
            print("Done")
            break


def job(exchange: Exchange, cfg: DictConfig) -> None:
    log.info(f"I am working {cfg.experiment.name}")

    buy_some_bitcoin(exchange=exchange)
    show_balance(exchange=exchange)


def buy_some_bitcoin(exchange: Exchange) -> None:
    exchange.create_limit_buy_order(
        "BTC/USD", amount=0.5, price=C_BITCOIN_BUY_ORDER_LIMIT
    )


def connect_to_exchange(cfg: DictConfig):
    exchange = ccxt.gemini(
        {
            "apiKey": os.environ.get("GEMINI_SNDBX_API_KEY"),
            "secret": os.environ.get("GEMINI_SNDBX_API_SECRET"),
        }
    )
    exchange.set_sandbox_mode(True)
    return exchange


def show_balance(exchange: Exchange) -> None:
    account_balance = exchange.fetch_balance()
    df_balance = pd.DataFrame.from_records(account_balance["info"])

    numeric_cols = [
        "amount",
        "available",
        "availableForWithdrawal",
    ]
    for col in numeric_cols:
        df_balance = df_balance.assign(
            **{col: lambda x: pd.to_numeric(x[col], errors="coerce")}
        )

    print(df_balance.set_index("currency")[numeric_cols])
