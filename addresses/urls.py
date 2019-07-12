from django.urls import path, re_path
from .views import address_create_view, address_reuse_view

urlpatterns = [
	re_path(r'checkout/address/create/', address_create_view, name='address_create'),
	re_path(r'checkout/address/reuse/', address_reuse_view, name='address_reuse'),
]