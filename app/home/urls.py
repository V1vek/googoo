from django.conf.urls import patterns, url

from app.home import views

urlpatterns = patterns('app.home.views',
    url(r'index/$', 'index'),
    url(r'faq/$', 'faq'),
    url(r'about/$', 'about'),
    url(r'terms_and_conditions/$', 'terms_and_conditions'),
)