from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from .forms import AddressForm
from billing.models import BillingProfile
from .models import Address

def address_create_view(request):
	address_form = AddressForm(request.POST or None)
	context = {
		'address_form':address_form,
	}
	next_page = request.GET.get('next')
	next_post = request.POST.get('next')
	redirect_url = next_page or next_post or None
	if address_form.is_valid():
		instance = address_form.save(commit=False)
		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
		if billing_profile is not None:
			address_type = request.POST.get('address_type', 'shipping') 
			instance.billing_profile = billing_profile
			instance.address_type = address_type
			print(instance.address_type)
			instance.save()
			request.session[address_type + '_address_id'] = instance.id

		else:
			return redirect('checkout_home')
		if is_safe_url(redirect_url, request.get_host()):
			return redirect(redirect_url)
	return redirect('checkout_home')

def address_reuse_view(request):
	if request.user.is_authenticated:
		context = {}
		next_page = request.GET.get('next')
		next_post = request.POST.get('next')
		redirect_url = next_page or next_post or None
		if request.method == 'POST':
			billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
			shipping_address = request.POST.get('shipping', None)
			billing_address = request.POST.get('billing', None)
			address_type = request.POST.get('address_type', 'shipping') 
			if shipping_address is not None or billing_address is not None:
				address_id = shipping_address or billing_address or None
				qs = Address.objects.filter(billing_profile=billing_profile, id=address_id)
				if qs.exists():
					request.session[address_type + '_address_id'] = address_id
				if is_safe_url(redirect_url, request.get_host()):
					return redirect(redirect_url)
	return redirect('checkout_home')