from django.urls import path, include
from rest_framework.routers import DefaultRouter

from mystore.views import ProductViewSet, CartItemViewSet, UserViewSet

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('cart-items', CartItemViewSet)
router.register('customers', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
