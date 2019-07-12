from django.urls import path, re_path
from .views import search_product, search_featured_product

urlpatterns = [
    re_path(r'^product/$', search_product, name='search_product'),
    re_path(r'^(?P<search>[-\w]+)/$', search_product, name='search_product'),
    re_path(r'^featured/product/$', search_featured_product, name='search_featured_product'),
    re_path(r'^(?P<search>[-\w]+)/$', search_featured_product, name='search_featured_product'),
]