from django.urls import path, re_path, include
from django.conf.urls import url
from .views import AccountHomeView, EmailActivationView, GuestRegisterView, RegisterView, LoginView, UserDetailChangeView #, login_page , register_page, login_required_view, guest_register
from products.views import UserProductHistoryView
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView

urlpatterns = [
	# re_path(r'^accounts/', login_required_view, name='login_required_view'),
	re_path(r'^accounts/$', RedirectView.as_view(url='/account/'), name='account_home_re_f_acs'),
	re_path(r'^settings/', RedirectView.as_view(url='/account/'), name='account_home_re_f_set'),
    re_path(r'^account/$', AccountHomeView.as_view(), name='account_home'),
    re_path(r'^account/email/confirm/(?P<key>[0-9A-Za-z]+)/$', EmailActivationView.as_view(), name='email_activate'),
    re_path(r'^account/resend-activation/$', EmailActivationView.as_view(), name='resend_activation'),
    re_path(r'^account/update-detail/$', UserDetailChangeView.as_view(), name='update_detail'),
    re_path(r'^account/history/product/$', UserProductHistoryView.as_view(), name='user_history_product'),
    re_path(r'^account/order/', include('orders.urls')),
    # re_path(r'^login/$', login_page, name='login_page'),
    re_path(r'^login/$', LoginView.as_view(), name='login_page'),
    re_path(r'^logout/$', LogoutView.as_view(), name='logout_page'),
    # re_path(r'^register/$', register_page, name='register_page'),
    re_path(r'^register/$', RegisterView.as_view(), name='register_page'),
    # re_path(r'^register/guest/$', guest_register, name='guest_register'),
    re_path(r'^register/guest/$', GuestRegisterView.as_view(), name='guest_register'),
]
