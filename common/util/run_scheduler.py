import time
from datetime import date
import logging

from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

import schedule
from app.order_sellers.models import OrderSeller
from dateutil.relativedelta import relativedelta

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def call_schedule_ever_day(run_time, job):
    schedule.every().day.at(run_time).do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


def get_rental_expired_books():
    order_sellers = OrderSeller.objects.filter(order_seller_item__renting_options='1',
                                               order_seller_item__order_status='3').distinct()
    orders_before_expiry = dict()
    expired_orders = dict()

    for order_seller in order_sellers:
        expired_orders[order_seller.order.id] = expired_orders[order_seller.order.id] \
            if order_seller.order.id in expired_orders else []

        orders_before_expiry[order_seller.order.id] = orders_before_expiry[order_seller.order.id] \
            if order_seller.order.id in orders_before_expiry else []

        for order_item in order_seller.order_seller_item.all():
            current_date = date.today()
            after_six_months = order_item.order.ordered_date + relativedelta(
                months=+order_item.seller_book_condition.seller.tenure)
            one_week_before = after_six_months+relativedelta(weeks=-1)
            log.info(order_seller.seller.id)
            if one_week_before == current_date:
                orders_before_expiry[order_seller.order.id].append(order_item)
            elif after_six_months == current_date:
                expired_orders[order_seller.order.id].append(order_item)

    items_grouped_by_order_and_seller = dict()

    # Before a week from expiration time
    for order_id, ordered_items in orders_before_expiry.items():
        send_rental_before_expire_email_buyer(ordered_items)

        items_grouped_by_order_and_seller[order_id] = items_grouped_by_order_and_seller[order_id] \
            if order_id in items_grouped_by_order_and_seller else dict()

        for item in ordered_items:
            items_grouped_by_order_and_seller[order_id][item.seller_book_condition.seller_book.seller.id] \
                = items_grouped_by_order_and_seller[order_id][item.seller_book_condition.seller_book.seller.id] \
                if item.seller_book_condition.seller_book.seller.id in items_grouped_by_order_and_seller[order_id] else []

            items_grouped_by_order_and_seller[order_id][item.seller_book_condition.seller_book.seller.id].append(item)

    for order_id, seller_items in items_grouped_by_order_and_seller.items():
        for seller_id, items in seller_items.items():
            send_rental_expired_email_seller(items)

    items_grouped_by_order_and_seller = dict()

    # For expired orders
    for order_id, ordered_items in expired_orders.items():
        send_rental_expired_email_buyer(ordered_items)

        items_grouped_by_order_and_seller[order_id] = items_grouped_by_order_and_seller[order_id] \
            if order_id in items_grouped_by_order_and_seller else dict()

        for item in ordered_items:
            items_grouped_by_order_and_seller[order_id][item.seller_book_condition.seller_book.seller.id] \
                = items_grouped_by_order_and_seller[order_id][item.seller_book_condition.seller_book.seller.id] \
                if item.seller_book_condition.seller_book.seller.id in items_grouped_by_order_and_seller[order_id] else []

            items_grouped_by_order_and_seller[order_id][item.seller_book_condition.seller_book.seller.id].append(item)

    for order_id, seller_items in items_grouped_by_order_and_seller.items():
        for seller_id, items in seller_items.items():
            send_rental_expired_email_seller(items)

    log.info(expired_orders)

    return items_grouped_by_order_and_seller


def send_rental_before_expire_email_buyer(order_items):
    email_subject = ' Rental period about to expire for your order OD0000{0} in 7 days '.format(order_items[0].order.id)
    user = order_items[0].order.user
    expiry_date = order_items[0].order.ordered_date + relativedelta(
        months=+order_items[0].seller_book_condition.seller.tenure)
    message = render_to_string('email/rental_expiry_notify_buyer.html',
                               {'user': user, 'order_items': order_items, 'date': expiry_date})
    msg = EmailMultiAlternatives(subject=email_subject, body=unicode(message),
                                 from_email="admin@textnook.com", to=[user.email])
    msg.attach_alternative(message, "text/html")
    msg.send()


def send_rental_expired_email_buyer(order_items):
    email_subject = 'Rental period expired for your order OD0000{0}'.format(order_items[0].order.id)
    user = order_items[0].order.user
    message = render_to_string('email/rental_expired_notify_buyer.html',
                               {'user': user, 'order_items': order_items})
    msg = EmailMultiAlternatives(subject=email_subject, body=unicode(message),
                                 from_email="admin@textnook.com", to=[user.email])
    msg.attach_alternative(message, "text/html")
    msg.send()


def send_rental_before_expire_email_seller(order_items):
    email_subject = 'Rental period about to expire for Order OD0000{0}'.format(order_items[0].order.id)
    user = order_items[0].seller_book_condition.seller_book.seller.profile
    message = render_to_string('email/rental_expiry_notify_seller.html',
                               {'user': user, 'order_items': order_items})
    msg = EmailMultiAlternatives(subject=email_subject, body=unicode(message),
                                 from_email="admin@textnook.com", to=[user.email])
    msg.attach_alternative(message, "text/html")
    msg.send()


def send_rental_expired_email_seller(order_items):
    email_subject = 'Rental period expired for order OD0000{0}'.format(order_items[0].order.id)
    user = order_items[0].seller_book_condition.seller_book.seller.profile
    message = render_to_string('email/rental_expired_notify_seller.html',
                               {'user': user, 'order_items': order_items})
    msg = EmailMultiAlternatives(subject=email_subject, body=unicode(message),
                                 from_email="admin@textnook.com", to=[user.email])
    msg.attach_alternative(message, "text/html")
    msg.send()


if __name__ == "__main__":
    log.info("Today {0} Scheduler Initiated".format(date.today))
    call_schedule_ever_day("10:30", get_rental_expired_books)
    get_rental_expired_books()
    log.info("Today {0} Scheduler Completed".format(date.today))

