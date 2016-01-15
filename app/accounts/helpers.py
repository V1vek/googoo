import logging

from midway.app.carts.models import Cart
from midway.app.orders.models import Order
from midway.app.discount_coupon.models import Discount

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def get_cart_details(request, context, coupon=None):
    carts = Cart.objects.filter(user=request.user, is_ordered=False)
    context['cart_products'] = []
    cart_total = 0
    shipping_price = 0
    order, created = Order.objects.update_or_create(user=request.user, order_options='1')
    request.session['order_id'] = order.id

    try:
        for cart in carts:
            try:

                log.info("mrp : {0}, quantity : {1}".format(cart.product.price, cart.quantity))

                mrp = cart.product.price * float(cart.quantity)
                cart_total += mrp

                context['cart_products'].append({
                    'products': cart.product,
                    'mrp_price': mrp,
                    'c': cart
                })
            except Exception as e:
                log.info("Exception :".format(e))

        context['cart_total'] = cart_total
        if cart_total < 500 :
            shipping_price = 50
        context['shipping_price'] = shipping_price
        context['total'] = cart_total+shipping_price
        context['complete_total'] = context['total']

        context['cart_count'] = len(carts)
        if order.discount_id_id is not None or coupon is not None:
            if coupon is None and order.discount_id_id is not None:
                try:
                    coupon = Discount.objects.get(id=order.discount_id_id)
                except Discount.DoesNotExist:
                    coupon = None
            if coupon:
                if context['total'] > coupon.minimum_amount:
                    log.info(coupon.offer_type)

                    if coupon.offer_type == '1':
                        context['discount_price'] = coupon.offer_value
                    else:
                        context['discount_price'] = (context['total']/100) * coupon.offer_value

                    context['total'] = context['total'] - context['discount_price']
                    order.discount_id = coupon
                    order.discount_price = context['discount_price']
                    context['coupon_code'] = coupon.coupon_code
                    # coupon.valid_uses -= 1
                    # coupon.save()
                else:
                    order.discount_price = 0
                    context['coupon_code'] = None
                    # coupon.valid_uses += 1
                    # coupon.save()

        order.order_total = context['total']
        order.complete_total = context['complete_total']
        order.cart_total = context['cart_total']
        order.shipping_price = context['shipping_price']
        log.info(order)
        res = order.save()
        context['order'] = order

    except Exception as e:
        log.info("Exception {0}".format(e))
        context['cart_products'] = None
    return context

