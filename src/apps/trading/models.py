"""
===========================================================
Project: QuantTrade-Pro (Algorithmic Trading Platform)
Author:  Saloni Gupta 
Date:    2025-12-16
Version: 0.1
Guidance: Built in collaboration with Vasvi Soni and Pratham Tyagi

Description:
------------
Core trading domain models:
- Asset: Tradable instruments (e.g., stocks, indices).
- Portfolio: User portfolios with valuation and risk helpers.
- Trade: Buy/sell transactions with basic validations.

Note:
-----
This module will be extended to integrate with MarketData
and NewsFeed from the data_pipeline app for live valuation
and P&L analytics.
===========================================================
"""







from django.db import models
from django.core.exceptions import ValidationError
from decimal import Decimal
from src.apps.data_pipeline.models import MarketData


# Create your models here.

from django.contrib.auth.models import User

from src.apps.data_pipeline.constants import VALID_SYMBOLS, is_valid_symbol

class Asset(models.Model):
    SYMBOL_CHOICES = [(symbol, symbol) for symbol in VALID_SYMBOLS]

    symbol = models.CharField(
        max_length=20,
        choices=SYMBOL_CHOICES,
        unique=True
    )

    def save(self, *args, **kwargs):
        if not is_valid_symbol(self.symbol):
            raise ValueError(f"Invalid symbol: {self.symbol}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.symbol
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.symbol} ({self.name})"

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    
    def historical_value(self) -> float:
        """
        Calculate portfolio value based only on executed trades.

        Note:
        -----
        This uses trade prices at execution time and does NOT
        use live MarketData. For live valuation, see current_value().
        """
        total = 0.0
        trades = self.trade_set.all()

        for trade in trades:
            if trade.trade_type == 'buy':
                total += float(trade.price) * trade.quantity
            elif trade.trade_type == 'sell':
                total -= float(trade.price) * trade.quantity
        return total
    
    def current_value(self) -> float:
        """
        Calculate live portfolio value using latest MarketData.

        For each Asset in this portfolio:
        - Compute net quantity (buys - sells).
        - Fetch latest MarketData close_price for that symbol.
        - Sum quantity * latest price.
        """
        total = 0.0
        # All trades in this portfolio
        trades = self.trade_set.select_related("asset").all()

        # Group by asset and compute net quantity
        asset_quantities = {}
        for trade in trades:
            symbol = trade.asset.symbol
            asset_quantities.setdefault(symbol, 0)
            if trade.trade_type == "buy":
                asset_quantities[symbol] += trade.quantity
            elif trade.trade_type == "sell":
                asset_quantities[symbol] -= trade.quantity

        # Use latest MarketData for each symbol
        for symbol, qty in asset_quantities.items():
            if qty <= 0:
                continue  # no open position
            try:
                latest_md = (
                    MarketData.objects
                    .filter(asset_symbol=symbol)
                    .latest("timestamp")
                )
                total += float(latest_md.close_price) * qty
            except MarketData.DoesNotExist:
                # No market data for this symbol yet; skip
                continue

        return total


    def __str__(self):
        return (
            f"{self.user.username} - {self.name} "
            f"(Hist: ₹{self.historical_value():.2f}, "
            f"Live: ₹{self.current_value():.2f})"
        )


    
    
    def available_cash(self):
        """Calculate available cash for new trades"""
        # You'll implement this based on initial cash - total spent
        return Decimal('10000.00')  # Placeholder - implement properly
    
    def get_asset_quantity(self, asset):
        """Get total quantity owned of an asset"""
        buy_trades = self.trade_set.filter(asset=asset, trade_type='buy')
        sell_trades = self.trade_set.filter(asset=asset, trade_type='sell')
        
        total_bought = sum(trade.quantity for trade in buy_trades)
        total_sold = sum(trade.quantity for trade in sell_trades)
        
        return total_bought - total_sold


class Trade(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    TRADE_TYPES = (
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    )
    trade_type = models.CharField(max_length=4, choices=TRADE_TYPES)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    trade_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.trade_type} {self.quantity} x {self.asset.symbol} @ {self.price}"
    
    def clean(self):
        """Validate trade before saving"""
        super().clean()
        
        # Validate buy trades have sufficient funds
        #if self.trade_type == 'buy':
            #total_cost = self.price * self.quantity
            #if self.portfolio.available_cash() < total_cost:
               # raise ValidationError(
                 #   f"Insufficient funds. Need ₹{total_cost}, have ₹{self.portfolio.available_cash()}"
                #)
        
        # Validate sell trades have sufficient quantity
        if self.trade_type == 'sell':
            owned_quantity = self.portfolio.get_asset_quantity(self.asset)
            if owned_quantity < self.quantity:
                raise ValidationError(
                    f"Insufficient shares. Trying to sell {self.quantity}, own {owned_quantity}"
                )
    
    