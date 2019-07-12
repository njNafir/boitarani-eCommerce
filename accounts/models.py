from datetime import timedelta
from django.db import models
from django.contrib.auth.models import(
	AbstractBaseUser, BaseUserManager
)
from django.db.models.signals import pre_save, post_save
import random, string
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q

# send_mail(subject, message, from_email, reciepient_email, html_txt)

class UserManager(BaseUserManager):
	def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
		first_name = ''
		last_name = ''
		description = ''
		if not email:
			raise ValueError('User must be needed a email address.')
		if not password:
			raise ValueError('User must be needed a password for sequrity essue.')
		user_obj = self.model(
				email = self.normalize_email(email)
			)
		user_obj.set_password(password)
		user_obj.is_active = is_active
		user_obj.staff = is_staff
		user_obj.admin = is_admin
		user_obj.first_name = first_name
		user_obj.last_name = last_name
		user_obj.full_name = first_name + last_name
		user_obj.description = description
		user_obj.save(using=self._db)
		return user_obj

	def create_staffuser(self, email, password=None):
		user = self.create_user(
				email,
				password=password,
				is_staff=True
			)
		return user

	def create_superuser(self, email, password=None):
		user = self.create_user(
				email,
				password=password,
				is_staff=True,
				is_admin=True
			)
		return user

class User(AbstractBaseUser):
	# username  	= models.CharField(max_lenght=255, blank=True, null=True)
	email 			= models.EmailField(unique=True) # core for our custom user
	first_name 		= models.CharField(max_length=255, blank=True, null=True)
	last_name 		= models.CharField(max_length=255, blank=True, null=True)
	full_name 		= models.CharField(max_length=255, blank=True, null=True)
	description 	= models.TextField(blank=True, null=True)
	is_active		= models.BooleanField(default=True) # can login
	staff			= models.BooleanField(default=False) # staff user not superuser
	admin			= models.BooleanField(default=False) # activation for superuser
	timestamp		= models.DateTimeField(auto_now_add=True)
	# confirmed		= models.BooleanField(default=False)
	# confirmed_date	= models.DateTimeField(auto_now_add=True)

	objects = UserManager()

	USERNAME_FIELD = 'email' # username

	# USERNAME_FIELD and email are required by default
	REQUIRED_FIELD = [] # ['full_name', 'email']

	def __str__(self):
		return self.email

	def get_user(self):
		return self.email

	def get_full_name(self):
		if self.full_name:
			return self.full_name
		return self.email

	def get_short_name(self):
		if self.first_name:
			return self.first_name
		return self.email

	def has_perm(self, perm, obj=None):
		return True

	def has_module_perms(self, app_label):
		return True

	# @property
	# def is_active(self):
	# 	return self.active
	
	@property
	def is_staff(self):
		if self.is_admin:
			return True
		return self.staff

	@property
	def is_admin(self):
		return self.admin
	
class EmailActivationQuerySet(models.query.QuerySet):
	def confirmable(self):
		now = timezone.now()
		default_expires_day = getattr(settings, 'DEFAULT_EXPIRES_DAY', 7)
		start_time = now - timedelta(days=default_expires_day)
		end_time = now

		return self.filter(
				activated = False,
				forced_expired = False
			).filter(
				timestamp__gt = start_time,
				timestamp__lte = end_time
			)

class EmailActivationManager(models.Manager):
	def get_queryset(self):
		return EmailActivationQuerySet(self.model, using=self._db)

	def confirmable(self):
		return self.get_queryset().confirmable()

	def email_exists(self, email):
		return self.get_queryset().filter(
				Q(email=email) | Q(user__email=email)
			).filter(
				activated=False,
			)

class EmailActivation(models.Model):
	user 			= models.ForeignKey(User, on_delete='user')
	email 			= models.EmailField()
	key 			= models.CharField(max_length=120, unique=True, blank=True, null=True)
	activated 		= models.BooleanField(default=False)
	forced_expired 	= models.BooleanField(default=False)
	expires 		= models.IntegerField(default=7)
	timestamp 		= models.DateTimeField(auto_now_add=True)
	updated 		= models.DateTimeField(auto_now=True)

	objects = EmailActivationManager()

	def __str__(self):
		return self.email

	def can_activate(self):
		qs = EmailActivation.objects.filter(pk=self.pk).confirmable()
		if qs.exists():
			return True
		return False

	def activate(self):
		if self.can_activate:
			user = self.user
			user.is_active = True
			user.save()
			self.activated = True
			self.save()
			return True
		return False

	def regenerate(self):
		self.key = None
		self.save()
		if self.key is not None:
			return True
		return False

	def send_activation(self):
		if not self.activated and not self.forced_expired:
			if self.key:
				base_url = getattr(settings, 'BASE_URL', 'https://www.boitaranis.herokuapp.com/')
				path_key = reverse('email_activate', kwargs={'key':self.key})
				path 	= '{base}{key}'.format(base=base_url, key=path_key)
				context = {
					'email': self.email,
					'path': path,
				}
				subject = "1-click activation email."
				txt_ 	= get_template('registration/emails/varify.txt').render(context)
				html_ 	= get_template('registration/emails/varify.html').render(context)
				from_email 			= settings.DEFAULT_FROM_EMAIL
				reciepient_email 	= (self.email,)
				sent_mail 			= send_mail(
						subject,
						txt_,
						from_email,
						reciepient_email,
						html_,
					)
				return sent_mail
		return False

def pre_save_key_generator_reciever(sender, instance, *args, **kwargs):
	if not instance.activated and not instance.forced_expired:
		if not instance.key:
			chars = string.ascii_lowercase + string.digits
			key = ''.join(random.choice(chars) for _ in range(20))
			qs = EmailActivation.objects.filter(key__iexact=key)
			if qs.exists():
				key = ''.join(random.choice(chars) for _ in range(20))
			instance.key = key

pre_save.connect(pre_save_key_generator_reciever, sender=EmailActivation)


def post_save_create_reciever(sender, instance, created, *args, **kwargs):
	if created:
		obj = EmailActivation.objects.create(user=instance, email=instance.email)
		obj.send_activation()

post_save.connect(post_save_create_reciever, sender=User)



class GuestEmail(models.Model):
	email 		= models.EmailField()
	active 		= models.BooleanField(default=True)
	created 	= models.DateTimeField(auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True)

	def __str__(self):
		return 'null'

	@property
	def name(self):
		return 'null'
	