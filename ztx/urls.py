from django.urls import path
from django.urls import path, include
from .views import CostomerViewSet, ProductViewSet, IncomeViewSet, TradeViewSet, CostomerRecharge, CostomerConsume
from rest_framework import routers


router = routers.DefaultRouter()
router.register('costomer', CostomerViewSet, basename="costomer")
router.register('product', ProductViewSet, basename="product")
router.register('income', IncomeViewSet, basename="income")
router.register('trade', TradeViewSet, basename="trade")
urlpatterns = [
    path('', include(router.urls)),
    path('recharge',CostomerRecharge.as_view()),
    path('consume',CostomerConsume.as_view())
    
]