from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
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

    def create(self, request, *args, **kwargs):
        request.data['password'] = make_password(request.data['password'])
        return super().create(request, *args, **kwargs)

    @action(methods=['get', 'post', 'delete'], detail=True)
    def cart(self, request, pk):
        response = ...
        if request.method == 'GET':
            response = CartItemSerializer(CartItem.objects.filter(user=pk), many=True).data
            status_code = status.HTTP_200_OK

        elif request.method == 'POST':
            cart_item = CartItem.objects.filter(user=get_object_or_404(User, pk=pk),
                                                product=get_object_or_404(Product, pk=request.data['product']))
            if cart_item.exists():
                cart_item = cart_item.first()
                cart_item.quantity += request.data.get('quantity') if request.data.get('quantity') else 1
                cart_item.save()
            else:
                cart_item = CartItem(user=get_object_or_404(User, pk=pk),
                                     product=get_object_or_404(Product, pk=request.data['product']),
                                     quantity= request.data.get('quantity') if request.data.get('quantity') else 1)
            cart_item.save()
            response = CartItemSerializer(cart_item).data
            status_code = status.HTTP_200_OK

        elif request.method == 'PUT':
            cart_item = CartItem.objects.filter(user=get_object_or_404(User, pk=pk),
                                                product=get_object_or_404(Product, pk=request.data['product']))
            if not cart_item.exists():
                response = 'This product is not in this user\'s cart'
                status_code = status.HTTP_404_NOT_FOUND
            else:
                cart_item = cart_item.first()
                cart_item.quantity = request.data.get('quantity') if request.data.get('quantity') else cart_item.quantity
                cart_item.quantity = request.data.get('product') if request.data.get('product') else cart_item.product
                cart_item.save()
                response = CartItemSerializer(cart_item).data
                status_code = status.HTTP_200_OK

        elif request.method == 'DELETE':
            items = CartItem.objects.filter(user=pk)
            if request.data.get('product'):
                items = items.filter(product=request.data['product'])
            items.delete()
            response = 'Cart items deleted'
            status_code = status.HTTP_204_NO_CONTENT

        return Response(response, status_code)


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
