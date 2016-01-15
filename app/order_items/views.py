from django.contrib.auth.decorators import login_required
from app.order_items.models import OrderItem
from app.order_shipping_address.models import OrderShippingAddress
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
import logging
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@api_view(['POST'])
@login_required
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def update_order_item_details_seller(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        order_item_id = data['order_item_id']
        order_status = data['order_status']
        tracking_id = data['tracking_id']
        tracking_url = data['tracking_url']
        context = {}
        user = request.user

        try:
            if user.id is not None:
                order_item = OrderItem.objects.get(id=order_item_id)

                order_item.product = order_item.product.id
                order_item.order_status = order_status
                order_item.tracking_id = tracking_id
                order_item.tracking_url = tracking_url
                order_item.save()
                order_details = order_item

                if order_status == '3' and order_details is not None:
                    send_order_shipped_mail(user, [order_item], order_details)

                if order_status == '4' and order_details is not None:
                    send_order_delivered_mail(user, [order_item], order_details)

                if order_status == '5' and order_details is not None:
                    send_return_order_received_mail(user, [order_item], order_details)

            return Response({'status': 'success'})
        except OrderItem.DoesNotExist:
            return Response({'error': 'Item Not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@login_required
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def update_order_item_details_buyer(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        order_item_id = data['order_item_id']
        order_status = '2'
        context = {}
        user = request.user

        try:
            if user.id is not None:
                order_item = OrderItem.objects.get(id=order_item_id,
                                                   order__user=request.user)
                order_item.product = order_item.product.id
                order_item.order_status = order_status
                order_item.save()
                send_return_order_mail(user, order_item.order.id, [order_item])
            return Response({'status': 'success'})
        except OrderItem.DoesNotExist:
            return Response({'error': 'Item Not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@login_required
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def get_order_item_details(request):
    if request.method == 'GET':
        # data = JSONParser().parse(request)
        # log.info(data)

        order_item_id = int(request.GET.get('order_item_id'))
        sender = request.GET.get('sender')
        log.info(order_item_id)

        context = {}
        user = request.user

        try:
            if user.id is not None:
                if sender == 'customer' or sender == 'retailer':
                    order_item = OrderItem.objects.get(id=order_item_id, order__user=request.user)

                context['id'] = order_item.id
                context['tracking_id'] = order_item.tracking_id
                context['tracking_url'] = order_item.tracking_url
                context['order_status'] = order_item.order_status

            return Response(context)
        except OrderItem.DoesNotExist:
            return Response({'error': 'Item Not found'}, status=status.HTTP_404_NOT_FOUND)


def send_order_shipped_mail(user, order_items, order_details):
    try:
        shipping_address = OrderShippingAddress.objects.get(order_id=order_details.order.id)
    except OrderShippingAddress.DoesNotExist:
        shipping_address = None

    email_subject = 'One or more book(s) of your order OD0000{0} has been dispatched'.format(order_details.order.id)
    message = render_to_string('email/order_dispatched.html',
                               {'user': user,
                                'order_items': order_items,
                                'details': order_details,
                                'shipping_address': shipping_address
                               })
# --------------------------------------- change this ----------------------------------------------------
    msg = EmailMultiAlternatives(subject=email_subject, body=unicode(message),
                                 from_email="admin@textnook.com", to=[user.email, "service@textnook.in"])
    msg.attach_alternative(message, "text/html")
    msg.send()


def send_order_delivered_mail(user, order_items, order_details):
    email_subject = 'Delivery Confirmation and Invoice copy for your order OD0000{0}'.format(order_details.order.id)
    message = render_to_string('email/order_delivered.html',
                               {'user': user, 'order_items': order_items, 'details': order_details})
# ------------------------------------------------ change this -----------------------------------------------------
    msg = EmailMultiAlternatives(subject=email_subject, body=unicode(message),
                                 from_email="admin@textnook.com", to=[user.email, "service@textnook.in"])
    msg.attach_alternative(message, "text/html")
    msg.send()


def send_return_order_mail(user, order_id, order_items):
    email_subject = 'Your return request for the order OD0000{0}'.format(order_id)
    message = render_to_string('email/return_order_notify_buyer.html',
                               {'user': user, 'order_id': order_id, 'order_items': order_items})
# ------------------------------------------------ change this -------------------------------------------------------
    msg = EmailMultiAlternatives(subject=email_subject, body=unicode(message),
                                 from_email="admin@textnook.com", to=[user.email, "service@textnook.in"])
    msg.attach_alternative(message, "text/html")
    msg.send()


def send_return_order_received_mail(user, order_items, order_details):

    email_subject = 'Refund for returned book(s) - Order OD0000{0}'.format(order_details.order.id)
    message = render_to_string('email/return_book_received_buyer.html',
                               {'user': user, 'order_items': order_items, 'details': order_details})
# ------------------------------------------------ change this -------------------------------------------------------
    msg = EmailMultiAlternatives(subject=email_subject, body=unicode(message),
                                 from_email="admin@textnook.com", to=[user.email,"service@textnook.in"])
    msg.attach_alternative(message, "text/html")
    msg.send()


def send_email_before_rental_expiry_time(user, order_items, order_details):
    email_subject = 'Delivery Confirmation and Invoice copy for your order OD0000{0}'.format(order_details.order.id)
    message = render_to_string('email/order_delivered.html',
                               {'user': user, 'order_items': order_items, 'details': order_details})
# ------------------------------------------------ change this -------------------------------------------------------
    msg = EmailMultiAlternatives(subject=email_subject, body=unicode(message),
                                 from_email="admin@textnook.com", to=[user.email, "service@textnook.in"])
    msg.attach_alternative(message, "text/html")
    msg.send()