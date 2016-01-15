from django.conf.urls import patterns, url

urlpatterns = patterns(
    'app.discount_coupon.views',
    url(r'^coupon/apply/$', 'apply_coupon'),
    url(r'^coupon/remove/$', 'remove_coupon'),

    )