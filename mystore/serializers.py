from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from mystore.models import Product, CartItem


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CartItemSerializer(ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
