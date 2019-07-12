from django.shortcuts import render, Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from .models import Order, ProductPurchase

class OrderListView(LoginRequiredMixin, ListView):
	def get_queryset(self):
		return Order.objects.by_request(self.request)

class OrderDetailView(LoginRequiredMixin, DetailView):
	def get_object(self):
		qs = Order.objects.by_request(
				self.request
			).filter(
				order_id=self.kwargs.get('order_id')
			)
		if qs.count() == 1:
			return qs.first()
		else:
			return Http404

	def get_queryset(self):
		return Order.objects.by_request(self.request)

class LibraryView(LoginRequiredMixin, ListView):
	template_name = 'orders/purchase-library.html'

	def get_queryset(self):
		return ProductPurchase.objects.products_by_request(self.request)