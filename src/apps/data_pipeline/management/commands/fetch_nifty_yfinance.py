import datetime
import yfinance as yf
from django.core.management.base import BaseCommand
from src.apps.data_pipeline.models import MarketData


class Command(BaseCommand):
    help = "Fetch market data from Yahoo Finance and store in MarketData."

    def add_arguments(self, parser):
        parser.add_argument(
            "--symbol",
            type=str,
            default="^NSEI",  # NIFTY 50 index on Yahoo Finance [web:71]
            help="Yahoo Finance ticker symbol (default: ^NSEI for NIFTY 50).",
        )
        parser.add_argument(
            "--asset-symbol",
            type=str,
            default="NIFTY50",
            help="Symbol to store in MarketData.asset_symbol (default: NIFTY50).",
        )
        parser.add_argument(
            "--days",
            type=int,
            default=30,
            help="Number of past days of data to fetch (default: 30).",
        )

    def handle(self, *args, **options):
        yf_symbol = options["symbol"]
        asset_symbol = options["asset_symbol"]
        days = options["days"]

        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=days)

        self.stdout.write(
            f"Fetching data for {asset_symbol} ({yf_symbol}) from {start_date} to {end_date}..."
        )

        try:
            ticker = yf.Ticker(yf_symbol)
            df = ticker.history(start=start_date, end=end_date, interval="1d")
        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"Failed to fetch data for {yf_symbol}: {e}")
            )
            return

        if df is None or df.empty:
            return

        created, updated, skipped = 0, 0, 0

        # Iterate over rows with basic validation
        for index, row in df.iterrows():
            # Skip rows with missing prices or volume
            if (
                    row.isna().any()
                    or row.get("Open") is None
                    or row.get("High") is None
                    or row.get("Low") is None
                    or row.get("Close") is None
                    or row.get("Volume") is None
                    or int(row.get("Volume")) == 0
            ):
                skipped += 1
                continue

            try:
                ts = index.to_pydatetime()

                obj, is_created = MarketData.objects.update_or_create(
                    asset_symbol=asset_symbol,
                    timestamp=ts,
                    defaults={
                        "open_price": row["Open"],
                        "high_price": row["High"],
                        "low_price": row["Low"],
                        "close_price": row["Close"],
                        "volume": int(row["Volume"]),
                    },
                )
            except Exception as e:
                skipped += 1
                self.stderr.write(
                    self.style.WARNING(
                        f"Skipped row at {index} for {asset_symbol}: {e}"
                    )
                )
                continue

            if is_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Finished fetching {asset_symbol} ({yf_symbol}) data: "
                f"{created} created, {updated} updated, {skipped} skipped."
            )
        )
