from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url('', include('django.contrib.auth.urls', namespace='auth')),

    # url(r'^$', include('app.home.urls')),

    url(r'^home/', include('app.home.urls')),
    url(r'^accounts/', include('app.accounts.urls')),
    url(r'^books/', include('app.products.urls')),
    url(r'^customer/', include('app.customer.urls')),
    url(r'^retailer/', include('app.retailer.urls')),
    url(r'^wishlist/', include('app.wishlists.urls')),
    url(r'^orders/', include('app.orders.urls')),

    # API URL's
    url(r'^api/', include('app.categories.urls')),
    url(r'^api/', include('app.sub_categories.urls')),
    url(r'^api/', include('app.products.urls')),
    url(r'^api/', include('app.accounts.urls')),
    url(r'^api/', include('app.retailer.urls')),
    url(r'^api/', include('app.customer.urls')),
    url(r'^api/', include('app.wishlists.urls')),
    url(r'^api/', include('app.carts.urls')),
    url(r'^api/', include('app.order_shipping_address.urls')),
    url(r'^api/', include('app.orders.urls')),
    url(r'^api/', include('app.discount_coupon.urls')),
    url(r'^api/', include('app.order_items.urls')),


)
