import logging
from collections import OrderedDict
import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect
from django.http import Http404
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from app.categories.models import Category
from app.orders.models import Order
from app.customer.models import Customer
from app.retailer.models import Retailer
from app.carts.models import Cart
from app.order_items.models import OrderItem
from app.order_shipping_address.models import OrderShippingAddress
from app.orders.helpers import get_cart_details
from common.util.instamojo import Instamojo
from common.config.config import ConfigSectionMap
from common.util.hmac_sha_helper import sign_request

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@login_required
def checkout(request):
    context = {}
    context['request'] = request
    context['user'] = request.user
    context['categories_all'] = Category.objects.all()
    context = get_cart_details(request, context)

    try:
        context['customer'] = Customer.objects.get(profile=request.user)
    except Customer.DoesNotExist:
        context['customer'] = None

    try:
        context['retailer'] = Retailer.objects.get(profile=request.user)
    except Retailer.DoesNotExist:
        context['retailer'] = None

    if  context['customer'] and context['retailer'] is None:
        return redirect('/accounts/profile/?created_profile=false')

    try:
        if request.session.get('order_id'):
            context['shipping_address'] = OrderShippingAddress.objects.get(user=request.user,
                                                                           order_id=request.session.get('order_id'))
        else:
            context['shipping_address'] = None

    except OrderShippingAddress.DoesNotExist:
        context['shipping_address'] = None

    return render(request, 'orders/checkout.html', context)


@login_required
def details(request, id):
    context = {}
    context['request'] = request
    context['user'] = request.user
    context['categories_all'] = Category.objects.all()
    context = get_cart_details(request, context)
    context['order_notes'] = None

    try:
        context['customer'] = Customer.objects.get(profile=request.user)
    except Customer.DoesNotExist:
        context['customer'] = None

    try:
        context['retailer'] = Retailer.objects.get(profile=request.user)
    except Retailer.DoesNotExist:
        context['retailer'] = None

    try:
        products_bought = OrderItem.objects.filter(order__user=request.user, order_status=3)
        context['products_bought'] = len(products_bought)
    except Exception as e:
        log.info("Exception : {0}".format(e))
        context['products_bought'] = 0

    context['shipping_address'] = OrderShippingAddress.objects.get(order_id=context['order_seller'].order.id)
    return render(request, 'orders/details.html', context)

"""
@login_required
def load_more_details(request):
    context = {}

    try:
        order_sellers = OrderSeller.objects.get(id=id)
    except OrderSeller.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = dict()

    for seller in order_sellers:
        pass


    log.info(context['order_seller'].order.id)
    context['shipping_address'] = OrderShippingAddress.objects.get(order_id=context['order_seller'].order.id)
"""

@login_required
def buyer_order_details(request, id):
    context = {}
    context['request'] = request
    context['user'] = request.user
    context['categories_all'] = Category.objects.all()
    context = get_cart_details(request, context)
    try:
        context['customer'] = Customer.objects.get(profile=request.user)
    except Customer.DoesNotExist:
        context['customer'] = None

    try:
        context['retailer'] = Retailer.objects.get(profile=request.user)
    except Retailer.DoesNotExist:
        context['retailer'] = None

    try:
        products_bought = OrderItem.objects.filter(order__user=request.user, order_status=3)
        context['books_bought'] = len(products_bought)
    except Exception as e:
        log.info("Exception : {0}".format(e))
        context['products_bought'] = 0

    context['shipping_address'] = OrderShippingAddress.objects.get(order_id=context['order_sellers'][0].order.id)
    return render(request, 'orders/buyer_details.html', context)


@api_view(['POST'])
@login_required
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_order(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        context = {}
        user = request.user
        context = get_cart_details(request, context)

        if 'total' in context:
            order, created = Order.objects.update_or_create(user=user,
                                                            order_options='1',
            )

            order.cart_total = context['cart_total']
            order.shipping_total = context['shipping_price']
            order.order_total = context['total']
            order.save()

            request.session['order_id'] = order.id
            return Response({'order_id': order.id})
        else:
            Response({'error': 'Something went wrong'})


@api_view(['POST'])
@login_required
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def create_link(request):
    if request.method == 'POST':

        if request.session.get('order_id'):

            try:
                customer = Customer.objects.get(profile=request.user)
            except Customer.DoesNotExist:
                customer = None

            try:
                retailer = Retailer.objects.get(profile=request.user)
            except Retailer.DoesNotExist:
                retailer = None

            try:
                order = Order.objects.get(id=request.session.get('order_id'))
# ---------------------------------------- change this --------------------------------------------------------------
                url = "https://www.instamojo.com/textnook/textnook/"

                if retailer is None:
                    contact_number = customer.contact_number if customer is not None else "9999999999"
                else:
                    contact_number = retailer.contact_number if retailer is not None else "9999999999"

                salt_string = "{0}|{1}|{2}|{3}".format(order.order_total,
                                                           request.user.email,
                                                           request.user.first_name,
                                                           contact_number)

                sign = sign_request(salt_string)

                url = "{0}?embed=form&data_name={1}&data_email={2}&data_phone={3}" \
                       "&data_amount={4}&data_sign={5}&data_Field_50680={6}" \
                       "&data_readonly=data_name&data_readonly=data_email" \
                       "&data_readonly=data_phone&" \
                       "data_readonly=data_amount&data_hidden=data_Field_50680".format(url,
                                                                                  request.user.first_name,
                                                                                  request.user.email,
                                                                                  contact_number,
                                                                                  order.order_total,
                                                                                  sign,
                                                                                  request.session.get('order_id'))

                #url = "https://www.instamojo.com/textnook/order_1-208e8/?" \
                 #     "embed=form&data_Field_95767={0}".format(request.session.get('order_id'))

                return Response({'url': url, 'sign': sign})
            except Order.DoesNotExist:
                raise Http404("No MyModel matches the given query.")
            except Exception as e:
                log.info("Exception {0}".format(e))
                return Response({'error': 'Something Went wrong'})


def move_cart_items_to_order(request):
    carts = Cart.objects.filter(user=request.user, is_ordered=False)
    order_seller = OrderedDict()
    cart_total = 0
    shipping_price = 0
    log.info(request.user.id)

    for cart in carts:

        cart.is_ordered = True
        cart.save()

        mrp = cart.product.price * float(cart.quantity)
        cart_total += mrp

        order_item = OrderItem.objects.create(order_id=request.session.get('order_id'),
                                         quantity=cart.quantity, product=cart.product, price=cart.product.price)

        order_item.save()


@login_required
def after_payment(request):
    context = {}
    context['request'] = request
    context['user'] = request.user
    context['categories_all'] = Category.objects.all()

    if request.session.get('order_id'):
        order_id = request.session.get('order_id')
        if request.GET.get('payment_id') and request.GET.get('status') and request.GET.get('status') == 'success':

            api_key = ConfigSectionMap('instamojo')['api_key']
            auth_token = ConfigSectionMap('instamojo')['auth_token']
            api = Instamojo(api_key=api_key, auth_token=auth_token)

            response = api.payment_detail(request.GET.get('payment_id'))

            log.info(int(response['payment']['custom_fields']['Field_50680']['value']))
            log.info(request.session.get('order_id'))

            if 'Field_50680' in response['payment']['custom_fields'] \
                    and request.session.get('order_id') == int(response['payment']['custom_fields']['Field_50680']['value']):

                try:

                    order = Order.objects.get(user=request.user, id=request.session.get('order_id'),
                                                         order_options='1')
                    order.order_options = '2'
                    order.payment_status = '3'
                    order.transaction_id = request.GET.get('payment_id')
                    order.save()
                    move_cart_items_to_order(request)
                    order_placed_email(context['user'], order)
                    del request.session['order_id']
                except Order.DoesNotExist:
                    raise Http404("No MyModel matches the given query.")

        elif request.GET.get('payment_mode'):
            if request.GET.get('payment_mode') == 'cod':
                try:

                    order = Order.objects.get(user=request.user, id=request.session.get('order_id'),
                                                         order_options='1')
                    order.order_options = '2'
                    order.payment_status = '4'
                    order.save()
                    move_cart_items_to_order(request)
                    order_placed_email(context['user'], order)

                    del request.session['order_id']
                except Order.DoesNotExist:
                    raise Http404("No MyModel matches the given query.")

                except Order.DoesNotExist:
                    log.info('except')
                    raise Http404("No objcet matches the given query.")

        else:

            try:
                order = Order.objects.get(user=request.user, id=request.session.get('order_id'),
                                                     order_options='1')
                order.payment_status = '2'
                order.save()
            except Order.DoesNotExist:
                raise Http404("No MyModel matches the given query.")

    else:
        return redirect('/user/dashboard/')

    try:
        context['customer'] = Customer.objects.get(profile=request.user)
    except Customer.DoesNotExist:
        context['customer'] = None

    try:
        context['order_items'] = OrderItem.objects.filter(order_id=order_id)
        context['order'] = order
        update_book_quantity(context['order_items'])
    except OrderItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        context['shipping_address'] = OrderShippingAddress.objects.get(order_id=order_id)
    except OrderShippingAddress.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return render(request, 'orders/paid.html', context)


def order_placed_email(user, order):
    try:
        order_items = OrderItem.objects.filter(order=order)
    except OrderItem.DoesNotExist:
        return None

    email_subject = 'Order #OD0000{0} with TextNook is successfully placed!'.format(order.id)
    message = render_to_string('email/order_placed_buyer.html', {'user': user,
                                                                 'order_items': order_items,
                                                                 'order_id': order.id,
                                                                 'root_url': os.environ.get('HOST_NAME')})
    # -------------------------- change this ----------------------------------------------
    msg = EmailMultiAlternatives(subject=email_subject, body=message,
                                 from_email="admin@textnook.com", to=[user.email,"service@textnook.in"])
    msg.attach_alternative(message, "text/html")
    msg.send()


def update_book_quantity(order_items):
    log.info(order_items)
    for order_item in order_items:
        order_item.product.quantity -= order_item.quantity
        order_item.save()


@api_view(['POST'])
@login_required
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def send_email_buyer(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        email = data['email']
        order_id = data['order_id']

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Order does not exist'})

        buyer = order.user

        email_subject = 'You have received an email from the seller regarding your order #OD0000{0}'.format(order_id)
        message = render_to_string('email/send_email.html', {'user': buyer, 'message': email})
        # ----------------------- change this -----------------------------------------------------
        msg = EmailMultiAlternatives(subject=email_subject, body=message,
                                     from_email="admin@textnook.com", to=[buyer.email,"service@textnook.in"])
        msg.attach_alternative(message, "text/html")
        msg.send()
        return Response({'status': 'success', 'message': msg.mandrill_response[0]})



