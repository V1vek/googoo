import logging

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

from app.customer.models import Customer
from app.categories.models import Category
from app.customer.serializers import CustomerSerializer
from app.order_items.models import OrderItem
from app.orders.models import Order
from app.orders.helpers import get_cart_details

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@login_required
def dashboard(request):
    context = {}
    str_title=""
    context['request'] = request
    context['user'] = request.user
    context['categories_all'] = Category.objects.all()
    context = get_cart_details(request, context)
    str_title=context['user'].first_name+" -Customer Dashboard|Customer profile"
    context['page_title'] = str_title

    try:
        context['customer'] = Customer.objects.get(profile=request.user)
    except Customer.DoesNotExist:
        context['customer'] = None

    if request.user.id is not None:
        context['orders'] = Order.objects.filter(user=request.user, order_options='2')

        try:
            products_bought = OrderItem.objects.filter(order__user=request.user, order_status=3)
            context['products_bought'] = len(products_bought)
        except Exception as e:
            log.info("Exception : {0}".format(e))
            context['products_bought'] = 0

        log.info(context['orders'])
    return render(request, 'user/dashboard.html', context)


@api_view(['GET', 'POST'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def customer_list(request):
    if request.method == 'GET':
        customer = Customer.objects.all()
        customer_serializer = CustomerSerializer(customer, many=True)
        return Response(customer_serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        customer_serializer = CustomerSerializer(data=data)
        if customer_serializer.is_valid():
            customer_serializer.save()
            return Response(customer_serializer.data, status=status.HTTP_201_CREATED)
        return Response(customer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def customer_details(request, id):

    try:
        customer = Customer.objects.get(pk=id)
    except customer.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        customer_serializer = CustomerSerializer(customer)
        return Response(customer_serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        customer_serializer = CustomerSerializer(customer, data=data)
        if customer_serializer.is_valid():
            customer_serializer.save()
            return Response(customer_serializer.data)
        return Response(customer_serializer.errors, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        customer.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
