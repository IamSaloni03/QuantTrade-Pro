from celery import shared_task
from django.core.management import call_command


@shared_task
def fetch_market_data_task(symbol="^NSEI", asset_symbol="NIFTY50", days=30):
    """
    Celery task to call the existing management command that fetches
    market data from Yahoo Finance and stores it in MarketData.
    """
    call_command(
        "fetch_nifty_yfinance",
        f"--symbol={symbol}",
        f"--asset-symbol={asset_symbol}",
        f"--days={days}",
    )
