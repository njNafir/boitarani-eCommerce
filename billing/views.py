from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.http import is_safe_url

from .models import BillingProfile, Card

import stripe
SRIPE_SECRET_KEY = getattr(settings, 'SRIPE_SECRET_KEY')
stripe.api_key = SRIPE_SECRET_KEY
SRIPE_PUBLISH_KEY = getattr(settings, 'SRIPE_PUBLISH_KEY')

def payment_method_view(request):
	next_url = None
	next_ = request.GET.get('next')
	if is_safe_url(next_, request.get_host()):
		next_url = next_
	if request.POST and request.is_ajax():
		# print('Hmmmmm')
		billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
		if not billing_profile:
			return HttpResponse({'message':'Cannot find the user....'})
		token = request.POST.get('token[id]')
		# print(request)
		# print(request.POST)
		# print(token)
		if token is not None:
			new_card_obj = Card.objects.add_new(billing_profile, token)
			# print('Created')
		return JsonResponse({'message': 'Success! your card was added.'})
	context = {
		'publish_key': SRIPE_PUBLISH_KEY,
		'next_url': next_url
	}
	# if request.POST:
	# 	print(request.POST)
	return render(request, 'billing/payment_method.html', context)

def payment_method_create_view(request):
	print('This')
	if request.POST:
		print(request)
		print(request.POST)
		return JsonResponse({'message': 'Success'})

	return HttpResponse('error')