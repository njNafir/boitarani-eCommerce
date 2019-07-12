from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse
from .models import Cart
from orders.models import Order
from products.models import Product
from accounts.models import GuestEmail
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from addresses.forms import AddressForm
from addresses.models import Address

SRIPE_SECRET_KEY = getattr(settings, 'SRIPE_SECRET_KEY')
SRIPE_PUBLISH_KEY = getattr(settings, 'SRIPE_PUBLISH_KEY')

def cart_api_view(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	products = [{'id': x.id, 'name': x.name, 'price': x.price, 'link': x.get_product_detail_url()} for x in cart_obj.products.all()]
	jeson_data = {'products': products, 'subtotal': cart_obj.subtotal, 'total': cart_obj.total}
	return JsonResponse(jeson_data)

def cart_home(request):
	title = 'Home page (Cart)'
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	context = {
		'title':title,
		'cart':cart_obj
	}
	return render(request, 'carts/home.html', context)

def cart_update(request):
	prduct_id = request.POST.get('product_id')
	try:
		product = Product.objects.get(id=prduct_id)
	except Product.DoesNotExist:
		print('Product is gone.')
		return redirect('cart_home')

	cart_obj, new_obj = Cart.objects.new_or_get(request)
	if product in cart_obj.products.all():
		cart_obj.products.remove(product)
		added = False
	else:
		cart_obj.products.add(product)
		added = True
	request.session['cart_products']=cart_obj.products.count()
	user_ready = False
	if request.user.is_authenticated:
		user_ready = True
	if request.is_ajax():
		jeson_data = {
			'added': added,
			'removed': not added,
			'user_ready': user_ready,
			'itemCount': cart_obj.products.count()
		}
		return JsonResponse(jeson_data)
		# return JsonResponse({'message':'This'}, status_code=400)
	return redirect('cart_home')

def checkout_home(request):
	cart_obj, new_obj = Cart.objects.new_or_get(request)
	order_obj = None
	address_qs = None
	has_card = False
	login_form = LoginForm(request)
	guest_form = GuestForm(request=request)
	address_form = AddressForm()
	shipping_address_required = not cart_obj.is_all_digital
	shipping_address_id = request.session.get('shipping_address_id', None)
	billing_address_id = request.session.get('billing_address_id', None)

	billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

	if new_obj or cart_obj.products.count()==0:
		return redirect('cart_home')
	if billing_profile is not None:
		if request.user.is_authenticated:
			address_qs = Address.objects.filter(billing_profile=billing_profile)

		order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
		if shipping_address_id:
			order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
			del request.session['shipping_address_id']
		if billing_address_id:
			order_obj.billing_address = Address.objects.get(id=billing_address_id)
			del request.session['billing_address_id']
		if shipping_address_id or billing_address_id:
			order_obj.save()
		has_card = billing_profile.has_card

	if request.method == 'POST':
		is_done = order_obj.check_done()
		if is_done:
			charge_did, charge_msg = billing_profile.charge(order_obj)
			if charge_did:
				order_obj.mark_paid()
				request.session['cart_products'] = 0
				del request.session['cart_id']
				if not billing_profile.user:
					billing_profile.set_cards_inactive()
				return redirect('checkout_success')
			else:
				print('Charge not dided')
				return redirect('checkout_home')

	context = {
		'object':order_obj,
		'billing_profile':billing_profile,
		'address_qs':address_qs,
		'login_form':login_form,
		'guest_form':guest_form,
		'address_form':address_form,
		'has_card':has_card,
		'publish_key':SRIPE_PUBLISH_KEY,
		'shipping_address_required':shipping_address_required
	}
	return render(request, 'carts/checkout.html', context)

def checkout_success(request):
	return render(request, 'carts/checkout_success.html', {})