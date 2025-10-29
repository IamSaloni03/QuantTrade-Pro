"""
URL configuration for quantrade_pro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
]

