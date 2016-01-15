from django.conf.urls import patterns, url

urlpatterns = patterns(
    'app.sub_categories.views',
    url(r'^sub_categories/(?P<type>[a-zA-Z]+)/(?P<category>[a-zA-Z]+)$', 'sub_category_list'),
)
