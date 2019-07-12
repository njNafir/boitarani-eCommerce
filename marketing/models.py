from django.db import models
from django.conf import settings
from django.db.models.signals import post_save, pre_save

from .utils import Mailchimp

class MarketingPreference(models.Model):
	user					= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete='user')
	mailchimp_subscribed 	= models.NullBooleanField(blank=True)
	subscribed				= models.BooleanField(default=True)
	mailchimp_ms			= models.TextField(null=True, blank=True)
	timestamp				= models.DateTimeField(auto_now_add=True)
	updated					= models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.user.email

def marketing_pref_user_create_reciever(sender, instance, created, *args, **kwargs):
	if created:
		status_code, responce_data = Mailchimp().subscribe(instance.user.email)
		print(instance.user.email)
		print(status_code)
		print(responce_data)

post_save.connect(marketing_pref_user_create_reciever, sender=MarketingPreference)

def marketing_pref_user_update_reciever(sender, instance, *args, **kwargs):
	if instance.subscribed != instance.mailchimp_subscribed:
		if instance.subscribed:
			status_code, responce_data = Mailchimp().subscribe(instance.user.email)
		else:
			status_code, responce_data = Mailchimp().unsubscribe(instance.user.email)

		if responce_data['status'] == 'subscribed':
			instance.subscribed = True
			instance.mailchimp_subscribed = True
			instance.mailchimp_ms = responce_data
		else:
			instance.subscribed = False
			instance.mailchimp_subscribed = False
			instance.mailchimp_ms = responce_data

pre_save.connect(marketing_pref_user_update_reciever, sender=MarketingPreference)

def marketing_pref_create_reciever(sender, instance, created, *args, **kwargs):
	if created:
		MarketingPreference.objects.get_or_create(user=instance)

post_save.connect(marketing_pref_create_reciever, sender=settings.AUTH_USER_MODEL)