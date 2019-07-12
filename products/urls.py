from django.urls import path, re_path
from .views import ProductListView, ProductDetailView, ProductDetailSlugView, ProductDownloadView, product_list, product_detail, featured_product_list, featured_product_detail, product_detail_slug, featured_product_detail_slug, VagitableListView, BookListView, ElectronicListView, MensFasionListView, WomanFasionListView, HomeAppliencesListView, HelthListView, OutdoorListView

urlpatterns = [
    # re_path(r'^products/fb-v/$', product_list, name='product_list'),
    # re_path(r'^product_detail/fb-v/(?P<id>\d+)/$', product_detail, name='product_detail'),
    # re_path(r'^product_detail/fb-v/(?P<slug>[-\w]+)/$', product_detail_slug, name='product_detail_slug'),
    re_path(r'^products/$', ProductListView.as_view(), name='ProductListView'),
    re_path(r'^products/vagitable/$', VagitableListView.as_view(), name='VagitableListView'),
    re_path(r'^products/book/$', BookListView.as_view(), name='BookListView'),
    re_path(r'^products/electronic/$', ElectronicListView.as_view(), name='ElectronicListView'),
    re_path(r'^products/mens_fashion/$', MensFasionListView.as_view(), name='MensFasionListView'),
    re_path(r'^products/womens_fashion/$', WomanFasionListView.as_view(), name='WomanFasionListView'),
    re_path(r'^products/home_appliences/$', HomeAppliencesListView.as_view(), name='HomeAppliencesListView'),
    re_path(r'^products/helth/$', HelthListView.as_view(), name='HelthListView'),
    re_path(r'^products/outdoor/$', OutdoorListView.as_view(), name='OutdoorListView'),
    re_path(r'^product_detail/(?P<pk>\d+)/$', ProductDetailView.as_view(), name='ProductDetailView'),
    re_path(r'^product_detail/(?P<slug>[-\w]+)/$', ProductDetailSlugView.as_view(), name='ProductDetailSlugView'),
    re_path(r'^product_download/(?P<slug>[-\w]+)/(?P<pk>\d+)/$', ProductDownloadView.as_view(), name='download'),
    re_path(r'^featured/products/$', featured_product_list, name='featured_product_list'),
    re_path(r'^featured/product_detail/(?P<id>\d+)/$', featured_product_detail, name='featured_product_detail'),
    re_path(r'^featured/product_detail/(?P<slug>[-\w]+)/$', featured_product_detail_slug, name='featured_product_detail_slug'),
]