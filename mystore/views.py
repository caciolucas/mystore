from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
# Create your views here.
from mystore.models import Product, CartItem
from mystore.serializers import ProductSerializer, CartItemSerializer, UserSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get', 'post'], detail=True)
    def cart(self, request, pk):
        return Response(CartItemSerializer(CartItem.objects.filter(user=pk), many=True).data)