from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL

# abc@nafir.com --->>> 10000000000 BillingProfile
# user abc@nafir.com --- 1 BillingProfile

import stripe
SRIPE_SECRET_KEY = getattr(settings, 'SRIPE_SECRET_KEY')
stripe.api_key = SRIPE_SECRET_KEY
SRIPE_PUBLISH_KEY = getattr(settings, 'SRIPE_PUBLISH_KEY')

class BillingProfileManager(models.Manager):
	def new_or_get(self, request):
		obj = None
		created = None
		user = request.user
		g_e_id = request.session.get('guest_user_id')

		if user.is_authenticated:
			obj, created = self.model.objects.get_or_create(user=user, email=user.email)
		elif g_e_id is not None:
			g_e_obj = GuestEmail.objects.get(id=g_e_id)
			obj, created = self.model.objects.get_or_create(email=g_e_obj.email)
		else:
			pass

		return obj, created


class BillingProfile(models.Model):
	user 		= models.ForeignKey(User, unique=True, null=True, blank=True, on_delete='user')
	email 		= models.EmailField()
	active 		= models.BooleanField(default=True)
	created 	= models.DateTimeField(auto_now_add=True)
	updated 	= models.DateTimeField(auto_now=True)
	customer_id = models.CharField(max_length=120, blank=True, null=True)
	# customer_id basicly for Stripe or Braintree

	objects = BillingProfileManager()

	def __str__(self):
		return self.email

	def charge(self, order_obj, card=None):
		return Charge.objects.do(self, order_obj, card)

	def get_card(self):
		return self.card_set.all()

	def set_cards_inactive(self):
		cards_qs = self.get_card()
		cards_qs.update(active=False)
		return cards_qs.filter(active=True).count()

	def get_peyment_method_url(self):
		return reverse('payment_view')

	@property
	def name(self):
		return self.user

	@property
	def has_card(self):
		card_qs = self.get_card()
		return card_qs.exists()

	@property
	def default_card(self):
		default_cards = self.get_card().filter(active=True, default=True)
		if default_cards.exists():
			return default_cards.first()
		return None
	
def customer_id_reciver(sender, instance, *args, **kwargs):
	if not instance.customer_id and instance.email:
		# print('ACTUAL API REQUEST sent to Stripe/Braintree')
		customer = stripe.Customer.create(
				email = instance.email
			)
		# print(customer)
		# print(instance)
		instance.customer_id = customer.id

pre_save.connect(customer_id_reciver, sender=BillingProfile)

def post_save_user_reciever(sender, instance, created, *args, **kwargs):
	if created and instance.email:
		BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(post_save_user_reciever, sender=User)


class CardManager(models.Manager):
	def all(self, *args, **kwargs):
		return self.get_queryset().filter(active=True)

	def add_new(self, billing_profile, token):
		if token:
			# print(token)
			# new = billing_profile.customer_id
			# print(new)
			stripe_card_response = stripe.Customer.create_source(
					billing_profile.customer_id,
					source=token
				)
			new_card = self.model(
					billing_profile = billing_profile,
					stripe_id 		= stripe_card_response.id,
					brand 			= stripe_card_response.brand,
					country 		= stripe_card_response.country,
					exp_month 		= stripe_card_response.exp_month,
					exp_year 		= stripe_card_response.exp_year,
					last4 			= stripe_card_response.last4
				)
			new_card.save()
			return new_card
		return None

class Card(models.Model):
	billing_profile = models.ForeignKey(BillingProfile, on_delete='billing_profile')
	stripe_id 		= models.CharField(max_length=120)
	brand 			= models.CharField(max_length=120, blank=True, null=True)
	country 		= models.CharField(max_length=20, blank=True, null=True)
	exp_month 		= models.IntegerField(blank=True, null=True)
	exp_year 		= models.IntegerField(blank=True, null=True)
	last4 			= models.CharField(max_length=4, blank=True, null=True)
	default 		= models.BooleanField(default=True)
	active 			= models.BooleanField(default=True)
	timestamp 		= models.DateTimeField(auto_now_add=True)

	objects = CardManager()

	def __str__(self):
		return '{} {}'.format(self.brand, self.last4)

def card_post_save_riciever(sender, instance, created, *args, **kwargs):
	if instance.default:
		qs = Card.objects.filter(billing_profile=instance.billing_profile).exclude(pk=instance.id)
		qs.update(default=False)

post_save.connect(card_post_save_riciever, sender=Card)

class ChargeManager(models.Manager):
	def do(self, billing_profile, order_obj, card=None):
		card_obj = card
		if card_obj is None:
			cards = billing_profile.card_set.filter(default=True)
			if cards.exists():
				card_obj = cards.first()
		if card_obj is None:
			return False, 'No Cards Available'

		charge_c = stripe.Charge.create(
		  amount 		= int(order_obj.total * 100),
		  currency 		= "usd",
		  customer 		= billing_profile.customer_id,
		  source 		= card_obj.stripe_id, # obtained with Stripe.js
		  metadata 		= {'order_id':order_obj.order_id},
		)

		new_charge_obj = self.model(
				billing_profile = billing_profile,
				stripe_id 		= charge_c.id,
				paid 			= charge_c.paid,
				refunded 		= charge_c.refunded,
				outcome 		= charge_c.outcome,
				outcome_type	= charge_c.outcome['type'],
				seller_message 	= charge_c.outcome.get('seller_message'),
				risk_level 		= charge_c.outcome.get('risk_level'),
			)
		new_charge_obj.save()
		return new_charge_obj.paid, new_charge_obj.seller_message

class Charge(models.Model):
	billing_profile = models.ForeignKey(BillingProfile, on_delete='billing_profile')
	stripe_id 		= models.CharField(max_length=120)
	paid 			= models.BooleanField(default=False)
	refunded 		= models.BooleanField(default=False)
	outcome 		= models.TextField(blank=True, null=True)
	outcome_type	= models.CharField(max_length=120, blank=True, null=True)
	seller_message 	= models.CharField(max_length=120, blank=True, null=True)
	risk_level 		= models.CharField(max_length=120, blank=True, null=True)

	objects = ChargeManager()

	def __str__(self):
		return 'null'
