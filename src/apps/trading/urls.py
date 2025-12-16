from rest_framework.routers import DefaultRouter
from .views import AssetViewSet, PortfolioViewSet, TradeViewSet

app_name = "trading"

router = DefaultRouter()
router.register(r"assets", AssetViewSet)
router.register(r"portfolios", PortfolioViewSet)
router.register(r"trades", TradeViewSet)

urlpatterns = router.urls
