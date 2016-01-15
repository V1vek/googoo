from django.conf.urls import patterns, url

urlpatterns = patterns(
    'app.accounts.views',
    url(r'^token/$', 'get_token'),
    url(r'^profile/$', 'profile'),
    url(r'^accounts/change_password/$', 'change_password'),
    url(r'^signup_user/$', 'signup_user'),
    url(r'^login_user/$', 'login_user'),
    url(r'^forgot_password/$', 'forgot_password'),
    url(r'^confirm_email/(?P<key>.*)/$', 'confirm_email'),
    url(r'^reset_password/(?P<key>.*)/$', 'reset_password'),
    url(r'^resend_verification_email/$', 'resend_verification_email'),
    url(r'^resend_email/$', 'verify_email_api'),
    url(r'^update_new_password/$', 'update_new_password'),
)
