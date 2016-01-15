from django.conf.urls import patterns, url

urlpatterns = patterns(
    'app.products.views',
    url(r'^(?P<product_type>[a-zA-Z]+)/(?P<product_category>[a-zA_Z]+)/$', 'products_list'),
    url(r'^(?P<product_type>[a-zA-Z]+)/(?P<product_category>[a-zA_Z]+)/(?P<product_id>[0-9a-zA_Z]+)$', 'product_details'),
    url(r'^filters/(?P<product_type>[a-zA-Z]+)/(?P<category>[a-zA_Z]+)/$', 'filter_list'),
)
