from django.shortcuts import render

from products.models import Product

def search_product(request, *args):
	query = request.GET.get('search')
	products = Product.objects.search(query)
	# query = None
	# if query is not None:
	# 	products = Product.objects.filter(title__icontains=query)
	# 	if products.count()==0:
	# 		products = Product.objects.filter(description__icontains=query)
	# else:
	# 	products = Product.objects.all()
	context = {
		'products':products,
		'query':query,
	}
	return render(request, 'search/product_list.html', context)

def search_featured_product(request, *args):
	query = request.GET.get('search')
	products = Product.objects.featured_search(query)
	# query = None
	# if query is not None:
	# 	products = Product.objects.filter(title__icontains=query, featured=True)
	# else:
	# 	products = Product.objects.featured_all()
	context = {
		'products':products
	}
	return render(request, 'search/featured/products.html', context)
