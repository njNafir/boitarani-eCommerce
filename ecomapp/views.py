from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .forms import ContactForm
from products.models import Product

def home_page(request):

	vagitable_product_obj = Product.objects.vagitable_product()
	book_product_obj = Product.objects.book_product()
	electronic_product_obj = Product.objects.electronic_product()
	mens_fashion_product_obj = Product.objects.mens_fashion_product()
	womens_fashion_product_obj = Product.objects.womens_fashion_product()
	home_appliences_product_obj = Product.objects.home_appliences_product()
	helth_product_obj = Product.objects.helth_product()
	outdoor_product_obj = Product.objects.outdoor_product()

	context = {
		'vagitable': vagitable_product_obj,
		'book': book_product_obj,
		'electronic': electronic_product_obj,
		'mens_fashion': mens_fashion_product_obj,
		'womens_fashion': womens_fashion_product_obj,
		'home_appliences': home_appliences_product_obj,
		'helth': helth_product_obj,
		'outdoor': outdoor_product_obj
	}
	
	if request.user.is_authenticated:
		context['premium_content'] = 'This is premium content'
		context['title'] = 'Boitarani-Ecommerce | Your best choice !'
	return render(request, 'pages/home_page.html', context)

def contact_page(request):
	contact_form = ContactForm(request.POST or None)
	context = {
		'title':'Welcome to contact page',
		'content':'Welcome to contact page',
		'form':contact_form,
	}
	# if request.method == 'POST':
	# 	print(request.POST.get('fullname'))
	# 	print(request.POST.get('email'))
	# 	print(request.POST.get('description'))
	if contact_form.is_valid():
		print(contact_form.cleaned_data)
		if request.is_ajax():
			json_data = {
				'message': 'Form submited! Thank you for your submission.',
			}
			return JsonResponse(json_data)
	if contact_form.errors:
		errors = contact_form.errors.as_json()
		if request.is_ajax():
			return HttpResponse(errors, status=400, content_type='application/json')
	return render(request, 'pages/contact_page.html', context)
	
def about_page(request):
	context = {
		'title':'Welcome to about page',
		'content':'Welcome to about page'
	}
	return render(request, 'pages/about_page.html', context)
