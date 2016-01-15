from django.conf.urls import patterns, url


urlpatterns = patterns(
    'app.customer.views',
    url(r'^dashboard/customer$', 'dashboard'),
    url(r'^customer/$', 'customer_list'),
    url(r'^customer/(?P<id>[0-9]+)$', 'customer_details'),

)
