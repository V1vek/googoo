from django.conf.urls import patterns, url


urlpatterns = patterns(
    'app.retailer.views',
    url(r'^dashboard/retailer$', 'dashboard'),
    url(r'^retailer/$', 'retailer_list'),
    url(r'^retailer/(?P<id>[0-9]+)$', 'retailer_details'),

)
