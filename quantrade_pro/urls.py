
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from src.apps.trading.views import AssetViewSet, PortfolioViewSet, TradeViewSet
from src.apps.analytics.views import SentimentAnalysisViewSet, StrategyPerformanceViewSet
from src.apps.data_pipeline.views import MarketDataViewSet, NewsFeedViewSet


router = routers.DefaultRouter()
router.register(r'assets', AssetViewSet)
router.register(r'portfolios', PortfolioViewSet)
router.register(r'trades', TradeViewSet)
router.register(r'sentiment', SentimentAnalysisViewSet)
router.register(r'strategy', StrategyPerformanceViewSet)
router.register(r'marketdata', MarketDataViewSet)
router.register(r'newsfeed', NewsFeedViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    # path('api/trading/', include('trading.urls'))
]

