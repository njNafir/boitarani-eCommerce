from django.urls import path, re_path
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns  = [
        re_path(r'^accounts/password/change/$', auth_views.PasswordChangeView.as_view(), name='password_change'),
        re_path(r'^accounts/password/change/done/$',auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
        re_path(r'^accounts/password/reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
        re_path(r'^accounts/password/reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
        re_path(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

        re_path(r'^accounts/password/reset/complete/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]