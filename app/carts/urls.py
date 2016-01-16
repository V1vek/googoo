from django.conf.urls import patterns, url

urlpatterns = patterns(
    'app.carts.views',
    url(r'^add_to_cart/$', 'add_to_cart'),
    url(r'^cart/$', 'cart_list'),
    url(r'^cart/update/$', 'update_cart'),
    url(r'^cart/remove/$', 'remove_cart'),
    )
