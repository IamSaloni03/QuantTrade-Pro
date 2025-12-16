"""
===========================================================
Project: QuantTrade-Pro (Algorithmic Trading Platform)
Author:  Saloni Gupta 
Date:    2025-12-16
Version: 0.1
Guidance: Built in collaboration with Vasvi Soni

Description:
------------
Django management command to import historical NIFTY 50
market data from a CSV file into the MarketData model.

The CSV is expected at:
- src/apps/data_pipeline/nifty50_30days.csv

Columns expected (header row):
- asset_symbol, timestamp, open_price, high_price,
  low_price, close_price, volume

Note:
-----
Each row is upserted based on (asset_symbol, timestamp)
using MarketData.objects.update_or_create().
===========================================================
"""

import csv
from pathlib import Path
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from src.apps.data_pipeline.models import MarketData


class Command(BaseCommand):
    """
    Import NIFTY50 historical data from CSV into MarketData.
    """

    help = "Import NIFTY50 OHLCV data from nifty50_30days.csv into MarketData."

    def handle(self, *args, **options):
        # Locate project root and CSV path
        csv_path = Path("src") / "apps" / "data_pipeline" / "nifty50_30days.csv"
        csv_path = csv_path.resolve()

        if not csv_path.exists():
            raise CommandError(f"CSV file not found at: {csv_path}")

        self.stdout.write(self.style.NOTICE(f"Reading CSV: {csv_path}"))

        created_count = 0
        updated_count = 0
        skipped_count = 0

        with csv_path.open(mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row_num, row in enumerate(reader, start=2):
                try:
                    asset_symbol = row["asset_symbol"].strip()
                    timestamp_str = row["timestamp"].strip()
                    open_price = float(row["open_price"])
                    high_price = float(row["high_price"])
                    low_price = float(row["low_price"])
                    close_price = float(row["close_price"])
                    volume = int(row["volume"])

                    # adjust format if your timestamp is different
                    timestamp = datetime.fromisoformat(timestamp_str)

                except KeyError as e:
                    raise CommandError(
                        f"Missing column {e!r} in CSV header. "
                        f"Offending row #{row_num}: {row}"
                    )
                except ValueError as e:
                    skipped_count += 1
                    self.stderr.write(
                        self.style.WARNING(
                            f"Skipping row #{row_num} due to parsing error: {e}. Row: {row}"
                        )
                    )
                    continue

                obj, created = MarketData.objects.update_or_create(
                    asset_symbol=asset_symbol,
                    timestamp=timestamp,
                    defaults={
                        "open_price": open_price,
                        "high_price": high_price,
                        "low_price": low_price,
                        "close_price": close_price,
                        "volume": volume,
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Import completed. Created: {created_count}, "
                f"Updated: {updated_count}, Skipped: {skipped_count}"
            )
        )
