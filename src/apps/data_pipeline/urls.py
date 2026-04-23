from django.urls import path
from .views import get_market_data

urlpatterns = [
    path("market-data/", get_market_data),
]