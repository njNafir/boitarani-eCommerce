from .utils import Mailchimp
from django.conf import settings
from .mixins import CsrfExemptMixin
from django.http import HttpResponse
from .models import MarketingPreference
from django.shortcuts import render, redirect
from .forms import MarketingPreferenceUpdateForm
from django.views.generic import UpdateView, View
from django.contrib.messages.views import SuccessMessageMixin


MAILCHIMP_EMAIL_LIST_ID = getattr(settings, 'MAILCHIMP_EMAIL_LIST_ID')

class MarketingPreferenceUpdateView(SuccessMessageMixin, UpdateView):
	form_class = MarketingPreferenceUpdateForm
	template_name = 'marketing/update_form.html'
	success_url = '/settings/email/'
	success_message = 'Your email preference is successfully updated'

	def dispatch(self, *args, **kwargs):
		user = self.request.user
		if not user.is_authenticated:
			# return HttpResponse('Not allowed')
			return redirect('/login/?next=/settings/email/')
		return super(MarketingPreferenceUpdateView, self).dispatch(*args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(MarketingPreferenceUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Update marketing preference.'
		return context

	def get_object(self):
		user = self.request.user
		obj, created = MarketingPreference.objects.get_or_create(user=user)
		return obj

class MarketingWebhookView(CsrfExemptMixin, View):
	def get(self, request, *args, **kwargs):
		return HttpResponse('Terminal says: <br/><br/> Method Not Allowed (GET): /webhooks/mailchimp/<br/> Method Not Allowed: /webhooks/mailchimp/ <br/><br/>Webhook says: <br/><br/> http://127.0.0.1:8000/webhooks/mailchimp/ <br/> Invalid destination. Please try a different URL <br/> Location in your app where Mailchimp should send list updates', status=200)

	def post(self, request, *args, **kwargs):
		data = request.POST
		list_id = data.get('data[list_id]')

		if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
			hook_type = data.get('type')
			email = data.get('data[email]')
			response_status, response = Mailchimp().check_subscription_status(email)
			sub_status = response['status']
			is_subbed = None
			is_mailchimp_subbed = None
			if sub_status == 'subscribed':
				is_subbed, is_mailchimp_subbed = (True, True)
			if sub_status == 'unsubscribed':
				is_subbed, is_mailchimp_subbed = (False, False)
			if is_subbed is not None and is_mailchimp_subbed is not None:
				qs = MarketingPreference.objects.filter(user__email__iexact=email)
				if qs.exists():
					qs.update(
							subscribed=is_subbed,
							mailchimp_subscribed=is_mailchimp_subbed,
							mailchimp_ms=str(data)
						)
		return HttpResponse('Thank you', status=200)




# type: unsubscribe
# data[id]: 77568bbc3e
# data[merges][ADDRESS]:
# data[action]: unsub
# data[ip_opt]: 45.251.230.166
# data[list_id]: 6b089001b8
# data[merges][LNAME]:
# data[web_id]: 16883065
# data[merges][EMAIL]: islamismotivation24434@gmail.com
# data[reason]: manual
# data[merges][PHONE]:
# fired_at: 2019-04-26 13:40:11
# data[merges][BIRTHDAY]:
# data[email]: islamismotivation24434@gmail.com
# data[merges][FNAME]:
# data[email_type]: html



# def marketing_webhook_view(request):
# 	data = request.POST
# 	list_id = data.get('data[list_id]')

# 	if str(list_id) == str(MAILCHIMP_EMAIL_LIST_ID):
# 		hook_type = data.get('type')
# 		email = data.get('data[email]')
# 		response_status, response = Mailchimp().check_subscription_status(email)
# 		sub_status = response['status']
# 		is_subbed = None
# 		is_mailchimp_subbed = None
# 		if sub_status == 'subscribed':
# 			is_subbed, is_mailchimp_subbed = (True, True)
# 		if sub_status == 'unsubscribed':
# 			is_subbed, is_mailchimp_subbed = (False, False)
# 		if is_subbed is not None and is_mailchimp_subbed is not None:
# 			qs = MarketingPreference.objects.filter(user__email__iexact=email)
# 			if qs.exists():
# 				qs.update(
# 						subscribed=is_subbed,
# 						mailchimp_subscribed=is_mailchimp_subbed,
# 						mailchimp_ms=str(data)
# 					)
# 	return HttpResponse('Thank you', status_code=200)