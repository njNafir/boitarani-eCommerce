from django.urls import path, re_path
from .views import home_page, contact_page, about_page

urlpatterns = [
    re_path(r'^$', home_page, name='home_page'),
    re_path(r'^contact/$', contact_page, name='contact_page'),
    re_path(r'^about/$', about_page, name='about_page'),
]
