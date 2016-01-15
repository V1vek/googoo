from django.conf.urls import patterns, url

urlpatterns = patterns(
    'app.carts.views',
    url(r'^cart/add/$', 'add_to_cart'),
    url(r'^cart/update/$', 'update_cart'),
    url(r'^cart/remove/$', 'remove_cart'),
    )
