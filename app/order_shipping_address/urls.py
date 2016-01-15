from django.conf.urls import patterns, url

urlpatterns = patterns(
    'app.order_shipping_address.views',
    url(r'^shipping_addresses/$', 'addresses_list'),

)
