from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    AssetViewSet,
    PortfolioViewSet,
    TradeViewSet,
    latest_prices,
    historical_prices,
    buy_asset,
    sell_asset,
    portfolio_detail
)

app_name = "trading"

router = DefaultRouter()
router.register(r"assets", AssetViewSet)
router.register(r"portfolios", PortfolioViewSet)
router.register(r"trades", TradeViewSet)

urlpatterns = [
    path("latest-price/", latest_prices, name="latest-prices"),
    path("history/<str:symbol>/", historical_prices, name="historical-prices"),
    path("trade/buy/", buy_asset, name="buy-asset"),
    path("trade/sell/", sell_asset, name="sell-asset"),
    path("portfolio/<int:portfolio_id>/", portfolio_detail, name="portfolio-detail"),
]
urlpatterns += router.urls