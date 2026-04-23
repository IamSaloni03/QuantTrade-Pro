from django.urls import path
from .views import BacktestView
from .views_signals import SignalsView
urlpatterns = [
    path("backtest/run/", BacktestView.as_view(), name="run-backtest"),
    path("signals/", SignalsView.as_view(), name="signals"),
]