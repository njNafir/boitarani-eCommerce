from math import fsum
from django.db import models
from django.urls import reverse
from carts.models import Cart
from django.conf import settings
import random, string, datetime
from django.utils import timezone
from billing.models import BillingProfile
from addresses.models import Address
from products.models import Product
from ecommerce.mixins import get_unique_path
from django.db.models import Sum, Avg, Count
from django.db.models.signals import pre_save, post_save

User = settings.AUTH_USER_MODEL

class OrderQuerySet(models.query.QuerySet):
	def by_weeks_range(self, week_ago=1, number_of_week=1):
		if number_of_week > week_ago:
			number_of_week = week_ago
		start_date_day = week_ago * 7
		end_date_day = start_date_day - (number_of_week * 7)
		start_date = timezone.now() - datetime.timedelta(days=start_date_day)
		end_date = timezone.now() - datetime.timedelta(days=end_date_day)
		return self.by_range(start_date, end_date=end_date)

	def by_range(self, start_date, end_date=None):
		if end_date is None:
			return self.filter(updated__gte=start_date)
		return self.filter(updated__gte=start_date, updated__lte=end_date)

	def get_recent_breakpoint(self):
		recent = self.recent()
		shipped = recent.by_status(status='shipped')
		paid = recent.by_status(status='paid')
		orders_total = recent.totals_data()
		shipped_orders_total = shipped.totals_data()
		paid_orders_total = paid.totals_data()
		orders_count = recent.count_order()
		shipped_orders_count = shipped.count_order()
		paid_orders_count = paid.count_order()
		cart_total = recent.carts_data()
		data = {
			'recent_order': recent,
			'shipped_order': shipped,
			'paid_order': paid,
			'recent_orders_total': orders_total,
			'recent_shipped_orders_total': shipped_orders_total,
			'recent_paid_orders_total': paid_orders_total,
			'recent_orders_count': orders_count,
			'recent_shipped_orders_count': shipped_orders_count,
			'recent_paid_orders_count': paid_orders_count,
			'recent_orders_cart_total': cart_total,
		}
		return data

	def count_order(self):
		return self.aggregate(Count('order_id'))

	def totals_data(self):
		return self.aggregate(Sum('total'), Avg('total'))

	def carts_data(self):
		return self.aggregate(Sum('cart__products__price'), Avg('cart__products__price'), Count('cart__products'))

	def recent(self):
		return self.order_by('-updated', '-timestamp')

	def not_refunded(self):
		return self.exclude(status='refunded')

	def by_date(self, days=7):
		day = timezone.now() - datetime.timedelta(days=days)
		return self.filter(updated__day__gte=day.day)

	def by_status(self, status='shipped'):
		return self.filter(status=status)

	def by_request(self, request):
		billing_profile, created = BillingProfile.objects.new_or_get(request)
		return self.filter(billing_profile=billing_profile)

	def not_created(self):
		return self.exclude(status='created')

class OrderManager(models.Manager):
	def get_queryset(self):
		return OrderQuerySet(self.model, using=self._db)

	def new_or_get(self, billing_profile, cart_obj):
		created = False
		qs = self.get_queryset().filter(billing_profile=billing_profile, cart=cart_obj, active=True, status='created')
		if qs.count()==1:
			obj = qs.first()
		else:
			obj = self.model.objects.create(billing_profile=billing_profile, cart=cart_obj)
			created = True
		return obj, created

	def by_request(self, request):
		return self.get_queryset().by_request(request).not_created()

class Order(models.Model):

	STATUS_CHOICES = (
			('created', 'Created'),
			('paid', 'Paid'),
			('shipped', 'Shipped'),
			('refunded', 'Refunded')
		)
	billing_profile 	= models.ForeignKey(BillingProfile, on_delete='billing_profile', blank=True, null=True)
	order_id 			= models.CharField(max_length=120, blank=True)
	shipping_address	= models.ForeignKey(Address, related_name='shipping_address', on_delete='shipping_address', null=True, blank=True)
	billing_address		= models.ForeignKey(Address, related_name='billing_address', on_delete='billing_address', null=True, blank=True)
	cart 				= models.ForeignKey(Cart, on_delete='cart')
	status 				= models.CharField(max_length=120, default='created', choices=STATUS_CHOICES)
	shipping_total 		= models.DecimalField(default=29.99, max_digits=20, decimal_places=2)
	total 				= models.DecimalField(default=0.00, max_digits=20, decimal_places=2)
	active				= models.BooleanField(default=True)
	timestamp			= models.DateTimeField(auto_now_add=True)
	updated				= models.DateTimeField(auto_now=True)

	objects = OrderManager()

	class Meta:
		ordering = [
			'-timestamp',
			'-updated'
		]

	def get_absolute_url(self):
		return reverse('order_detail', kwargs={'order_id':self.order_id})

	def get_status(self):
		if self.status == 'refunded':
			return 'Refunded order'
		elif self.status == 'shipped':
			return 'Shipped'
		elif self.status == 'paid':
			return 'Shipped'
		return 'Shipping soon'

	def __str__(self):
		return self.order_id

	@property
	def name(self):
		return self.order_id

	def update_total(self):
		total = self.cart.total
		shipping_total = self.shipping_total
		formated_total = fsum([total, shipping_total])
		self.total = format(formated_total, '.2f')
		self.save()
		return self.total

	def check_done(self):
		shipping_address_required = not self.cart.is_all_digital
		if shipping_address_required and self.shipping_address:
			shipping_address_done = True
		elif shipping_address_required and not self.shipping_address:
			shipping_address_done = False
		else:
			shipping_address_done = True
		billing_profile = self.billing_profile
		billing_address = self.billing_address
		total = self.total
		if billing_profile and billing_address and shipping_address_done and total > 0:
			return True
		return False

	def update_product_purchase(self):
		for p in self.cart.products.all():
			obj, created = ProductPurchase.objects.get_or_create(
					order_id = self.order_id,
					billing_profile = self.billing_profile,
					product = p
				)
		return ProductPurchase.objects.filter(order_id=self.order_id).count()

	def mark_paid(self):
		if self.status != 'paid':
			if self.check_done():
				self.status = 'paid'
				self.save()
				self.update_product_purchase()
		return self.status

def order_id_pre_save_reciever(sender, instance, *args, **kwargs):
	plus = get_unique_path(10)
	if not instance.order_id:
		instance.order_id = instance.order_id + plus

	qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
	if qs.exists():
		qs.update(active=False)

pre_save.connect(order_id_pre_save_reciever, sender=Order)

def post_save_cart_save_reciever(sender, instance, created, *args, **kwargs):
	if not created:
		cart_id = instance.id
		qs = Order.objects.filter(cart__id=cart_id)
		if qs.count()==1:
			order_obj = qs.first()
			order_obj.update_total()

post_save.connect(post_save_cart_save_reciever, sender=Cart)

def post_save_order_save_reciever(sender, instance, created, *args, **kwargs):
	if created:
		instance.update_total()

post_save.connect(post_save_order_save_reciever, sender=Order)



class ProductPurchaseQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(refunded=False)

	def digital(self):
		return self.filter(product__is_digital=True)

	def by_request(self, request):
		billing_profile, created = BillingProfile.objects.new_or_get(request)
		return self.filter(billing_profile=billing_profile)

class ProductPurchaseManager(models.Manager):
	def get_queryset(self):
		return ProductPurchaseQuerySet(self.model, using=self._db)

	def all(self):
		return self.get_queryset().active()

	def by_request(self, request):
		return self.get_queryset().by_request(request).active() # .digital()

	def product_ids(self, request):
		qs = self.by_request(request)
		ids_ = [x.product.id for x in qs]
		return ids_

	def products_by_request(self, request):
		ids_ = self.product_ids(request)
		obj_list = Product.objects.filter(id__in=ids_).distinct()
		return obj_list


class ProductPurchase(models.Model):
	order_id 			= models.CharField(max_length=120)
	billing_profile 	= models.ForeignKey(BillingProfile, on_delete='billing_profile') # billing_profile.productpurchase_set.all()
	product 			= models.ForeignKey(Product, on_delete='product') # product.productpurchase_set.all()
	refunded 			= models.BooleanField(default=False)
	updated 			= models.DateTimeField(auto_now=True)
	timestamp 			= models.DateTimeField(auto_now_add=True)

	objects = ProductPurchaseManager()

	def __str__(self):
		return self.product.title