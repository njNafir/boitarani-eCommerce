from decimal import Decimal
from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import pre_save, post_save, m2m_changed

User = settings.AUTH_USER_MODEL

class CartManager(models.Manager):
	def new_or_get(self, request):
		cart_id = request.session.get('cart_id', None)
		qs = self.get_queryset().filter(id=cart_id)
		if qs.exists() and qs.count()==1:
			cart_obj = qs.first()
			new_obj = False
			if request.user.is_authenticated and cart_obj.user is None:
				cart_obj.user = request.user
				cart_obj.save()
		else:
			cart_obj = Cart.objects.new(user=request.user)
			request.session['cart_id'] = cart_obj.id
			new_obj = True
		return cart_obj, new_obj

	def new(self, user=None):
		user_obj = None
		if user is not None:
			if user.is_authenticated:
				user_obj = user
		return self.model.objects.create(user=user_obj)

class Cart(models.Model):
	user 		= models.ForeignKey(User, null=True, blank=True, on_delete='user')
	products 	= models.ManyToManyField(Product, blank=True)
	subtotal 	= models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	total 		= models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
	updated 	= models.DateTimeField(auto_now=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)

	objects = CartManager()

	def __str__(self):
		return str(self.id)

	@property
	def name(self):
		return self.user

	@property
	def is_all_digital(self):
		qs = self.products.all()
		not_digital = qs.filter(is_digital=False)
		if not_digital.exists():
			return False
		return True
	
	

def cart_m2m_changed_reciever(sender, instance, action, *args, **kwargs):
	if action == 'post_remove' or action == 'post_add' or action == 'post_clear':
		products = instance.products.all()
		total = 0
		subtotal = 0
		for x in products:
			total += x.price
		if instance.subtotal != total:
			instance.subtotal = total
			instance.save()

m2m_changed.connect(cart_m2m_changed_reciever, sender=Cart.products.through)

def cart_pre_save_reciever(sender, instance, *args, **kwargs):
	if instance.subtotal > 0:
		total = Decimal(instance.subtotal) * Decimal(1.05)
		instance.total = format(total, '.2f')
	else:
		instance.total = 0.00

pre_save.connect(cart_pre_save_reciever, sender=Cart)