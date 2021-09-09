from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
# Create your views here.
from mystore.models import Product, CartItem
from mystore.serializers import ProductSerializer, CartItemSerializer, UserSerializer
from django.contrib.auth import authenticate
from rest_framework import status


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

class LoginView(ViewSet):
    '''A simple viewset to verify user credentials and if it exists return its information'''
    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user_exists = User.objects.filter(username=username).exists()

        if user_exists:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                return Response(UserSerializer(user).data)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
            