from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save, post_save
from .signals import object_viewed_signal
from .utils import get_client_ip
from accounts.signals import user_loged_in_signal
# from django.contrib.auth.admin import User

User = settings.AUTH_USER_MODEL

FORCE_SESSION_TO_ONE = getattr('settings', 'FORCE_SESSION_TO_ONE', False)
FORCE_USER_END_SESSION_TO_ONE = getattr('settings', 'FORCE_USER_END_SESSION_TO_ONE', False)

class ObjectViewedQuerySet(models.query.QuerySet):
	def by_model(self, model_class, model_queryset):
		c_type = ContentType.objects.get_for_model(model_class)
		qs = self.filter(content_type=c_type)
		if model_queryset:
			viewed = [x.object_id for x in qs]
			model_qs = model_class.objects.filter(pk__in=viewed)
			return model_qs
		return qs

class ObjectViewedManager(models.Manager):
	def get_queryset(self):
		return ObjectViewedQuerySet(self.model, using=self._db)

	def by_model(self, model_class, model_queryset=False):
		return self.get_queryset().by_model(model_class, model_queryset)

class ObjectViewed(models.Model):

	user 			= models.ForeignKey(User, blank=True, null=True, on_delete='user') # user instance instance.id
	ip_address 		= models.CharField(max_length=220, blank=True, null=True) # get user ip address 
	content_type 	= models.ForeignKey(ContentType, on_delete='content_type') # Content type like User, Product, Order, Cart, Address etc
	object_id 		= models.PositiveIntegerField() # For Content type specific content like User id, Product id, Order id, Cart id, Address id etc
	content_object 	= GenericForeignKey('content_type', 'object_id') # Create a object with content type and specific content of this type
	timestamp 		= models.DateTimeField(auto_now_add=True)

	objects = ObjectViewedManager()

	def __str__(self):
		return '%s viewed %s'%(self.content_object, self.timestamp)

	class Meta:
		ordering = ['-timestamp'] # most recent saved show up first
		verbose_name = 'Object Viewed'
		verbose_name_plural = 'Objects Viewed'

def object_viewed_reciever(sender, instance, request, *args, **kwargs):
	# print(sender)
	# print(instance)
	# print(request)
	# print(request.user)
	# if request.user:
	# 	user = request.user
	# else:
	# 	user = 'mdanjebtmhjh2018@gmail.com'
	c_type = ContentType.objects.get_for_model(sender)
	if request.user.is_authenticated:
		new_view_obj = ObjectViewed.objects.create(
				user = request.user,
				content_type = c_type,
				object_id = instance.id,
				ip_address = get_client_ip(request)
			)

object_viewed_signal.connect(object_viewed_reciever)


class UserSession(models.Model):
	user 			= models.ForeignKey(User, blank=True, null=True, on_delete='user')
	ip_address 		= models.CharField(max_length=220, blank=True, null=True)
	session_key 	= models.CharField(max_length=100, blank=True, null=True)
	timestamp 		= models.DateTimeField(auto_now_add=True)
	active 			= models.BooleanField(default=True)
	ended 			= models.BooleanField(default=False)

	def end_session(self):
		session_key = self.session_key
		try:
			Session.objects.get(pk=session_key).delete()
			# print('Done')
			self.active = False
			self.ended = True
			self.save()
		except:
			pass
		return self.ended

def post_save_session_reciever(sender, instance, created, *args, **kwargs):
	if created:
		qs = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id)
		for i in qs:
			i.end_session()
	if not instance.active and not instance.ended:
		instance.end_session()

if FORCE_SESSION_TO_ONE:
	post_save.connect(post_save_session_reciever, sender=UserSession)

def post_save_user_changed_reciever(sender, instance, create, *args, **kwargs):
	if not created:
		if instance.is_active == False:
			qs = UserSession.objects.filter(user=instance.user, ended=False, active=False)
			for i in qs:
				i.end_session()

if FORCE_USER_END_SESSION_TO_ONE:
	post_save.connect(post_save_user_changed_reciever, sender=User)

def user_loged_in_reciever(sender, instance, request, *args, **kwargs):
	# print(instance)
	session_key = request.session.session_key
	UserSession.objects.create(
			user = instance,
			session_key = session_key,
			ip_address = get_client_ip(request)
 		)

user_loged_in_signal.connect(user_loged_in_reciever)