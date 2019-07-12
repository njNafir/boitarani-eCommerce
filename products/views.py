from django.shortcuts import render, get_object_or_404, Http404, HttpResponse, redirect, HttpResponseRedirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from mimetypes import guess_type
from wsgiref.util import FileWrapper
from django.conf import settings
import os
from .models import Product, ProductFile
from carts.models import Cart
from analytics.mixins import ObjectViewedMixin
from analytics.signals import object_viewed_signal
from orders.models import ProductPurchase

class UserProductHistoryView(LoginRequiredMixin, ListView):	
	# template_name = 'products/product_list.html'

	def get_context_data(self, *args, **kwargs):
		context = super(UserProductHistoryView, self).get_context_data(*args, **kwargs)
		request = self.request
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		context['cart'] = cart_obj
		return context

	def get_queryset(self, *args, **kwargs):
		request = self.request
		views = request.user.objectviewed_set.by_model(Product, model_queryset=False) # when model_queryset is True the view must be need another template, my preference
		return views

class ProductListView(ListView):	
	def get_context_data(self, *args, **kwargs):
		context = super(ProductListView, self).get_context_data(*args, **kwargs)
		request = self.request
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		context['cart'] = cart_obj

		return context

	# queryset = Product.objects.all() #There are two defference way
	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.all()

class VagitableListView(ListView):	
	def get_context_data(self, *args, **kwargs):
		context = super(VagitableListView, self).get_context_data(*args, **kwargs)
		request = self.request
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		context['cart'] = cart_obj

		return context

	# queryset = Product.objects.vagitable_product() #There are two defference way
	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.vagitable_product()

class BookListView(ListView):	
	def get_context_data(self, *args, **kwargs):
		context = super(BookListView, self).get_context_data(*args, **kwargs)
		request = self.request
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		context['cart'] = cart_obj

		return context

	# queryset = Product.objects.book_product() #There are two defference way
	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.book_product()

class ElectronicListView(ListView):	
	def get_context_data(self, *args, **kwargs):
		context = super(ElectronicListView, self).get_context_data(*args, **kwargs)
		request = self.request
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		context['cart'] = cart_obj

		return context

	# queryset = Product.objects.electronic_product() #There are two defference way
	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.electronic_product()

class MensFasionListView(ListView):	
	def get_context_data(self, *args, **kwargs):
		context = super(MensFasionListView, self).get_context_data(*args, **kwargs)
		request = self.request
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		context['cart'] = cart_obj

		return context

	# queryset = Product.objects.mens_fashion_product() #There are two defference way
	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.mens_fashion_product()

class WomanFasionListView(ListView):	
	def get_context_data(self, *args, **kwargs):
		context = super(WomanFasionListView, self).get_context_data(*args, **kwargs)
		request = self.request
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		context['cart'] = cart_obj

		return context

	# queryset = Product.objects.womens_fashion_product() #There are two defference way
	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.womens_fashion_product()

class HomeAppliencesListView(ListView):	
	def get_context_data(self, *args, **kwargs):
		context = super(HomeAppliencesListView, self).get_context_data(*args, **kwargs)
		request = self.request
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		context['cart'] = cart_obj

		return context

	# queryset = Product.objects.home_appliences_product() #There are two defference way
	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.home_appliences_product()

class HelthListView(ListView):	
	def get_context_data(self, *args, **kwargs):
		context = super(HelthListView, self).get_context_data(*args, **kwargs)
		request = self.request
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		context['cart'] = cart_obj

		return context

	# queryset = Product.objects.helth_product() #There are two defference way
	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.helth_product()
		
class OutdoorListView(ListView):	
	def get_context_data(self, *args, **kwargs):
		context = super(OutdoorListView, self).get_context_data(*args, **kwargs)
		request = self.request
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		context['cart'] = cart_obj

		return context

	# queryset = Product.objects.outdoor_product() #There are two defference way
	def get_queryset(self, *args, **kwargs):
		request = self.request
		return Product.objects.outdoor_product()

class ProductDetailView(ObjectViewedMixin, DetailView):
	# queryset = Product.objects.all() #There are three difference way to do it
	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		return context

	# def get_queryset(self, *args, **kwargs):
	# 	request = self.request
	# 	pk = self.kwargs.get('pk')
	# 	return Product.objects.filter(pk=pk)

	def get_object(self, *args, **kwargs):
		request = self.request
		pk = self.kwargs.get('pk')
		instance = Product.objects.get_by_id(pk)
		if instance is None:
			raise Http404('Product not found')
		return instance

class ProductDetailSlugView(ObjectViewedMixin, DetailView):
	template_name = 'products/product_detail.html'
	def get_context_data(self, *args, **kwargs):
		request = self.request
		context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
		cart_obj, new_obj = Cart.objects.new_or_get(request)
		print(request.user)
		context['cart'] = cart_obj
		return context

	def get_object(self, *args, **kwargs):
		
		request = self.request
		slug = self.kwargs.get('slug')
		# instance = Product.objects.get_by_slug(slug)
		# if instance is None:
		# 	raise Http404('Product not found')
		# object_viewed_signal.send(instance.__class__, instance=instance, request=request)
		try:
			instance = Product.objects.get(slug=slug, active=True)
		except Product.DoesNotExist:
			raise Http404('Not found...')
		except Product.MultipleObjectsReturned:
			qs = Product.objects.filter(slug=slug, active=True)
			instance = qs.first()
		except:
			raise Http404('Uhmmmm...')
		# object_viewed_signal.send(instance.__class__, instance=instance, request=request)

		return instance

class ProductDownloadView(View):
	def get(self, *args, **kwargs):
		slug = kwargs.get('slug')
		pk = kwargs.get('pk')
		downloads_qs = ProductFile.objects.filter(pk=pk, product__slug=slug)
		if downloads_qs.count() != 1:
			response = Http404('Download not found.')
		download_obj = downloads_qs.first()

		can_download = False
		user_ready = True
		request = self.request
		if download_obj.user_required:
			if not request.user.is_authenticated:
				user_ready = False

		purchased_product = ProductPurchase.objects.none()
		if download_obj.free:
			can_download = True
		else:
			purchased_product = ProductPurchase.objects.products_by_request(request)
			if download_obj.product in purchased_product:
				can_download = True

		if not can_download:
			messages.error(request, "This is a premium product..")
			return redirect(download_obj.get_default_url())

		if not user_ready:
			messages.error(request, "You need to login or register first for download this product..")
			return redirect(download_obj.get_default_url())

		# for aws {
		# aws_filepath = download_obj.generate_download_url()
		# return HttpResponseRedirect(aws_filepath)
		# }

		# for local {
		main_root = settings.PREM_PRO_ROOT
		file_root = download_obj.file.path
		final_root = os.path.join(main_root, file_root)
		with open(final_root, 'rb') as f:
			wrapper = FileWrapper(f)
			mimetype = "application/force-download"
			guessed_type = guess_type(file_root)[0]
			if guessed_type:
				mimetype = guessed_type
			response = HttpResponse(wrapper, mimetype)
			response['Content-Disposition'] = "attachment;filename=%s"%(download_obj.get_name)
			response['X-SendFile'] = "%s"%(download_obj.get_name)
			return response
		# }	

def product_list(request):
	products = Product.objects.all()
	context = {
		'object_list':products,
	}
	return render(request, 'products/product_list.html', context)


def product_detail(request, id=None):
	product = Product.objects.get_by_id(id)
	if product is None:
		raise Http404('Product does not exists.')
	#print(product)
	#product = get_object_or_404(Product, id=id)
	context = {
		'object':product,
	}
	return render(request, 'products/product_detail.html', context)

def product_detail_slug(request, slug=None):
	cart_obj, new_obj = Cart.objects.new_or_get(request)

	product = get_object_or_404(Product, slug=slug, active=True)
	context = {
		'object':product,
		'cart':cart_obj,
	}
	return render(request, 'products/product_detail.html', context)

def featured_product_list(request):
	products = Product.objects.featured_all()
	context = {
		'products':products
	}
	return render(request, 'products/featured/products.html', context)

def featured_product_detail(request, id=None, *args):
	product = Product.objects.featured_get_by_id(id)
	#product = get_object_or_404(Product, id=id, featured=True)
	context = {
		'object':product
	}
	return render(request, 'products/featured/detail.html', context)

def featured_product_detail_slug(request, slug=None):
	product = get_object_or_404(Product, slug=slug, active=True, featured=True)
	context = {
		'object':product,
	}
	return render(request, 'products/featured/detail.html', context)

