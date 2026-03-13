from django.urls import path
from .views import BacktestView

urlpatterns = [
    path("backtest/run/", BacktestView.as_view(), name="run-backtest"),
]