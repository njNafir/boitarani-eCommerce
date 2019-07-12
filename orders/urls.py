from django.urls import path, re_path
from .views import OrderListView, OrderDetailView, LibraryView

urlpatterns = [
	re_path(r'^$', OrderListView.as_view(), name='order_list'),
	re_path(r'^(?P<order_id>[0-9A-Za-z]+)/$', OrderDetailView.as_view(), name='order_detail'),
	re_path(r'^purchase-library/$', LibraryView.as_view(), name='purchase_library'),
]