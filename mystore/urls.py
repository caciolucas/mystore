from django.urls import path, include
from rest_framework.routers import DefaultRouter

from mystore.views import LoginView, ProductViewSet, CartItemViewSet, UserViewSet

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('cart-items', CartItemViewSet)
router.register('customers', UserViewSet)
router.register('login', LoginView, basename='login')

urlpatterns = [
    path('', include(router.urls)),
]
