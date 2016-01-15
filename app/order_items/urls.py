from django.conf.urls import patterns, url

urlpatterns = patterns(
    'app.order_items.views',
    url(r'^seller/order_item_details/change/$', 'update_order_item_details_seller'),
    url(r'^buyer/order_item_details/change/$', 'update_order_item_details_buyer'),
    url(r'^order_item_details/$', 'get_order_item_details'),

    )