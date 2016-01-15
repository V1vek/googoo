from django.conf.urls import patterns, url

urlpatterns = patterns(
    'app.categories.views',
    url(r'^categories/$', 'categories_list'),
    url(r'^category/(?P<category_type>[a-zA-Z]+)(?:/(?P<category>[a-zA-Z]+))?/$', 'category_details'),
)
