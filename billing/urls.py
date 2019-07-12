from django.contrib import admin
from django.urls import path, re_path
from .views import payment_method_view, payment_method_create_view

urlpatterns = [
	re_path(r'payment/', payment_method_view, name='payment_view'),
	re_path(r'payment/create/', payment_method_create_view, name='payment_create_view'),
]
