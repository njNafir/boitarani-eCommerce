"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include

from .views import jquery_test

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^', include('ecomapp.urls')),
    re_path(r'^', include('accounts.urls')),
    re_path(r'^', include('addresses.urls')),
    re_path(r'^', include('marketing.urls')),
    re_path(r'^', include('analytics.urls')),
    re_path(r'^', include('products.urls')),
    re_path(r'^', include('billing.urls')),
    re_path(r'^', include('accounts.passwords.urls')),
    re_path(r'^search/', include('search.urls')),
    re_path(r'^tags/', include('tags.urls')),
    re_path(r'^cart/', include('carts.urls')),
    re_path(r'^jquery/', jquery_test, name='jquery')
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)











# in ecomapp.urls:

# from django.urls import path, re_path
# from .views import home_page, contact_page, about_page, login_page, register_page

# urlpatterns = [
#     re_path(r'^$', home_page, name='home_page'),
#     re_path(r'^contact/$', contact_page, name='contact_page'),
#     re_path(r'^about/$', about_page, name='about_page'),
#     re_path(r'^login/$', login_page, name='login_page'),
#     re_path(r'^register/$', register_page, name='register_page'),
# ]

# in products.urls:

#from products.views import product_list, product_detail, featured_product_list, featured_product_detail, product_detail_slug, featured_product_detail_slug

# re_path(r'^products/$', product_list, name='product_list'),
# re_path(r'^product_detail/(?P<id>\d+)/$', product_detail, name='product_detail'),
# re_path(r'^product_detail/(?P<slug>[-\w]+)/$', product_detail_slug, name='product_detail_slug'),
# re_path(r'^featured/products/$', featured_product_list, name='featured_product_list'),
# re_path(r'^featured/product_detail/(?P<id>\d+)/$', featured_product_detail, name='featured_product_detail'),
# re_path(r'^featured/product_detail/(?P<slug>[-\w]+)/$', featured_product_detail_slug, name='featured_product_detail_slug'),