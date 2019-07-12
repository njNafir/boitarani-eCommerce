from django.urls import path, re_path
from .views import cart_api_view, cart_home, cart_update, checkout_home, checkout_success

urlpatterns = [
	re_path(r'^$', cart_home, name='cart_home'),
	re_path(r'^update/', cart_update, name='cart_update'),
	re_path(r'^api/view/', cart_api_view, name='cart_api'),
	re_path(r'^checkout/', checkout_home, name='checkout_home'),
	re_path(r'^checkout/success/', checkout_success, name='checkout_success'),
]