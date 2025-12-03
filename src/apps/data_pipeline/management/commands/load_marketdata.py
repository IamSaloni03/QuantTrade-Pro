import csv
from django.core.management.base import BaseCommand
from src.apps.data_pipeline.models import MarketData
  # Use the correct import path for your model

class Command(BaseCommand):
    help = 'Load market data from a CSV file.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        with open(options['csv_file'], 'r') as f:
            reader = csv.DictReader(f)
            created = 0
            for row in reader:
                MarketData.objects.create(
                    asset_symbol=row['asset_symbol'],
                    timestamp=row['timestamp'],
                    open_price=row['open_price'],
                    high_price=row['high_price'],
                    low_price=row['low_price'],
                    close_price=row['close_price'],
                    volume=row['volume'],
                )
                created += 1
            self.stdout.write(self.style.SUCCESS(f"Imported {created} rows to MarketData"))
