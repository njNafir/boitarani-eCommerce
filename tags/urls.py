from django.contrib import admin
from django.urls import path, re_path

from .views import tags_list, tag_detail

urlpatterns = [
	re_path(r'^$', tags_list, name='tags_list'),
	re_path(r'^tag/(?P<slug>[-\w]+)$', tag_detail, name='tag_detail'),
]