import logging
from math import floor
import json

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from app.accounts.models import User
from app.products.models import Product
from app.carts.serializers import CartSerializer

from app.carts.models import Cart
from app.orders.helpers import get_cart_details

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


#@login_required
#@authentication_classes((JSONWebTokenAuthentication,))
#@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def add_to_cart(request):
    if request.method == 'POST':
        if not request.user.is_authenticated():
            #log.info(request.user.id)

            data = JSONParser().parse(request)
            log.info(data)
            product_id = data['product_id']
            size = data['size']
            quantity = data['quantity']

            user = User.objects.get(username='admin')
            product = Product.objects.get(id=product_id)

            price = float(quantity) * product.unit_price
            print user

            #user = request.user
            try:
                cart = Cart.objects.get(product_id=product_id, user=user, is_ordered=False)
                cart.quantity += 1
                cart.price += product.unit_price
            except Cart.DoesNotExist:
                cart = Cart.objects.create(product_id=product_id, user=user, size=size, quantity=quantity, price=price, is_ordered=False)

            cart.save()
            carts = Cart.objects.filter(user=user, is_ordered=False)
            cart_quantity = len(carts)

            if cart:
                return Response({'message': 'success', 'quantity': cart_quantity, 'user_id': user.id},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Authentication failed'})

@api_view(['GET'])
def cart_list(request):
    if request.method == 'GET':
        user = User.objects.get(username='admin')
        cart_list = Cart.objects.filter(user=user)
        cart_serialized = CartSerializer(cart_list, many=True)
        return Response(cart_serialized.data)


@login_required
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def update_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            data = JSONParser().parse(request)
            context = {}
            id = data['cart_id']
            quantity = data['quantity']
            user = request.user

            try:
                cart = Cart.objects.get(id=id)
            except Cart.DoesNotExist:
                return HttpResponse(status=status.HTTP_404_NOT_FOUND)

            cart.save()
            cart_quantity = cart.quantity

            context = get_cart_details(request, context)

            cart_details = dict()
            cart_details['cart_total'] = context['cart_total']
            cart_details['quantity'] = cart_quantity
            cart_details['shipping_price'] = context['shipping_price']
            cart_details['total'] = context['total']
            cart_details['item_price'] = cart.product.price*float(cart_quantity)
            cart_details['discount_price'] = context['discount_price'] if 'discount_price' in context else 0

            return Response({'cart': cart_details}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Authentication failed'})


@login_required
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def remove_cart(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        id = data['cart_id']

        try:
            cart = Cart.objects.get(id=id)
        except Cart.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        cart.delete()

        context = {}
        context = get_cart_details(request, context)

        # is_cod_available = chec_cod_availability(request)

        cart_details = dict()
        # cart_details['is_cod_available'] = is_cod_available
        cart_details['cart_total'] = context['cart_total']
        cart_details['shipping_price'] = context['shipping_price']
        cart_details['total'] = context['total']
        cart_details['discount_price'] = context['discount_price'] if 'discount_price' in context else 0
        return Response({'cart': cart_details})

"""
def chec_cod_availability(request):
    carts = Cart.objects.filter(user=request.user)
    is_cod_available = True

    for cart in carts:
        if not cart.seller_book_condition.seller_book.seller.is_cod_available:
            is_cod_available = False
        return is_cod_available

    return is_cod_available
"""