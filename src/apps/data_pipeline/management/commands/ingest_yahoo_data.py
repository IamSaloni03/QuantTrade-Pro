from django.core.management.base import BaseCommand
import yfinance as yf
from src.apps.data_pipeline.models import MarketData

class Command(BaseCommand):
    help = "Ingest market data for multiple symbols from Yahoo Finance"

    def add_arguments(self, parser):
        parser.add_argument(
            '--symbols',
            nargs='+',
            type=str,
            help='List of asset symbols'
        )

    def handle(self, *args, **options):
        symbols = options.get('symbols')

        if not symbols:
            self.stdout.write(self.style.ERROR("No symbols provided"))
            return

        for symbol in symbols:
            self.stdout.write(self.style.SUCCESS(f"Fetching data for {symbol}..."))

            try:
                # Handle index symbols differently
                if symbol == "NIFTY50":
                    ticker_symbol = "^NSEI"
                else:
                    ticker_symbol = symbol + ".NS"

                ticker = yf.Ticker(ticker_symbol)
                data = ticker.history(period="6mo", interval="1d")

                if data.empty:
                    self.stdout.write(self.style.WARNING(f"No data found for {symbol}"))
                    continue

                count = 0  # track saved rows

                for index, row in data.iterrows():
                    obj, created = MarketData.objects.get_or_create(
                        asset_symbol=symbol,
                        timestamp=index.to_pydatetime(),
                        defaults={
                            'open_price': row['Open'],
                            'high_price': row['High'],
                            'low_price': row['Low'],
                            'close_price': row['Close'],
                            'volume': int(row['Volume'])
                        }
                    )

                    if created:
                        count += 1

                self.stdout.write(
                    self.style.SUCCESS(f"{symbol}: {count} rows saved")
                )

            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"Error fetching {symbol}: {str(e)}")
                )