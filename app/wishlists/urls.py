from django.conf.urls import patterns, url


urlpatterns = patterns(
    'app.wishlists.views',
    url(r'^$', 'index'),
    url(r'^wishlist/add/', 'add_to_wishlist'),
    url(r'^wishlist/remove/', 'remove_from_wishlist'),


)
