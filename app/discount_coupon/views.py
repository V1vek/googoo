from datetime import date
import logging

from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from app.discount_coupon.models import Discount
from app.orders.models import Order
from app.orders.helpers import get_cart_details

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@api_view(['POST'])
@login_required
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def apply_coupon(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            context = {}
            data = JSONParser().parse(request)
            user = request.user
            coupon_code = data['coupon_code']

            try:
                coupon = Discount.objects.get(coupon_code=coupon_code)
            except Discount.DoesNotExist:
                return Response({'error': 'Coupon Does Not Exist'})

            try:
                order = Order.objects.get(id=request.session.get('order_id'))
            except Order.DoesNotExist:
                order = None

            if order:
                if coupon.start_date is not None and coupon.end_date is not None:

                    if coupon.start_date <= date.today() <= coupon.end_date:
                        context = get_cart_details(request, context, coupon)
                    else:
                        return Response({'error': 'Coupon Expired'})

                else:
                    context = get_cart_details(request, context, coupon)

                log.info(context['coupon_code'])

                if context['coupon_code']:
                    cart_values = {}
                    cart_values['total'] = context['total']
                    cart_values['discount_price'] = context['discount_price']
                    cart_values['cart_total'] = context['cart_total']

                    return Response({
                        'success': 'Coupon Applied',
                        'coupon_code': coupon.coupon_code,
                        'cart_values': cart_values
                    })
                else:
                    return Response({'error': 'Invalid Coupon Code'})
            else:
                return Response({'error': 'Coupon Expired'})
        else:
            return Response({'error': 'Authentication failed'})



@api_view(['POST'])
@login_required
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def remove_coupon(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            context = {}
            data = JSONParser().parse(request)
            user = request.user
            coupon_code = data['coupon_code']

            try:
                coupon = Discount.objects.get(coupon_code=coupon_code)
            except Discount.DoesNotExist:
                return Response({'error': 'Coupon Does Not Exist'})

            try:
                order = Order.objects.get(id=request.session.get('order_id'))
            except Order.DoesNotExist:
                order = None

            order.discount_id_id = None
            order.discount_price = 0
            order.save()
            context = get_cart_details(request, context)

            coupon.save()

            cart_values = {}
            cart_values['total'] = context['total']
            cart_values['discount_price'] = context['discount_price'] if 'discount_price' in context else 0
            cart_values['cart_total'] = context['cart_total']
            return Response({'success': 'Coupon removed', 'cart_values': cart_values})
        else:
            return Response({'error': 'Authentication failed'})
