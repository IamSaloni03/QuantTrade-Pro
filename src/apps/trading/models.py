from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Asset(models.Model):
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.symbol} ({self.name})"

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.name}"
    
    def total_value(self):
        trades = self.trade_set.all()
        value = 0
        for trade in trades:
            if trade.trade_type == 'buy':
                value += trade.price * trade.quantity
            elif trade.trade_type == 'sell':
                value -= trade.price * trade.quantity
        return value
    
    def total_value(self):
       """Calculate total portfolio value based on all trades"""
       total = 0
       trades = self.trade_set.all()
       
       for trade in trades:
           if trade.trade_type == 'buy':
               total += float(trade.price) * trade.quantity
           elif trade.trade_type == 'sell':
               total -= float(trade.price) * trade.quantity
       return total

    def __str__(self):
        return f"{self.user.username} - {self.name} (Value: ${self.total_value():.2f})"


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

