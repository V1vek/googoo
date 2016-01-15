from django.conf.urls import patterns, url

urlpatterns = patterns(
    'app.orders.views',
    url(r'^checkout/$', 'checkout'),
    url(r'^details/(?P<id>[0-9]+)$', 'details'),
    url(r'^buyer/details/(?P<id>[0-9]+)$', 'buyer_order_details'),
    url(r'^orders/$', 'create_order'),
    url(r'^instamojo/link/$', 'create_link'),
    url(r'^paid/$', 'after_payment'),
    url(r'^send_email/buyer/$', 'send_email_buyer')

    # API URL'S [eg : /api/link-here/]

)
