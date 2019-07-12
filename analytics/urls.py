from django.contrib import admin
from django.urls import path, re_path, include
from .views import SalesView

urlpatterns = [
	re_path(r'^analytic/sales/$', SalesView.as_view(), name='sales_page'),
]