from django.db import models
from django.urls import reverse
from django.db.models import Q
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.core.files.storage import FileSystemStorage
import random, string
import os
from ecommerce.mixins import get_unique_path, get_filename
from ecommerce.aws.utils import PremProRootS3BotoStorage
from ecommerce.aws.download.utils import AWSDownload

def get_filename_ext(filepath):
	base_name = os.path.basename(filepath)
	name, ext = os.path.splitext(base_name)
	return name, ext

def upload_image_path(instance, filename):
	new_filename 	= random.randint(1, 9999999999)
	name, ext 		= get_filename_ext(filename)
	final_filename 	= '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
	return 'products/{new_filename}/{final_filename}'.format(new_filename=new_filename, final_filename=final_filename)

class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

	def featured(self):
		return self.filter(active=True, featured=True)

	def vagitable(self):
		return self.filter(active=True, category='vagitable')
	def book(self):
		return self.filter(active=True, category='book')
	def electronic(self):
		return self.filter(active=True, category='electronic')
	def mens_fashion(self):
		return self.filter(active=True, category='mens fashion')
	def womens_fashion(self):
		return self.filter(active=True, category='womens fashion')
	def home_appliences(self):
		return self.filter(active=True, category='home appliences')
	def helth(self):
		return self.filter(active=True, category='helth')
	def outdoor(self):
		return self.filter(active=True, category='outdoor')

	def search(self, query):
		lookups = Q(title__icontains=query)|Q(description__icontains=query)|Q(price__icontains=query)|Q(producttag__title__icontains=query)
		return self.filter(lookups).distinct()

class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def all(self):
		return self.get_queryset().active()

	def get_by_id(self, id):
		qs = self.get_queryset().filter(id=id, active=True)
		if qs.count()==1:
			return qs.first()
		else:
			return None

	def get_by_slug(self, slug):
		qs = self.get_queryset().filter(slug=slug, active=True)
		if qs.count()==1:
			return qs.first()
		else:
			return None

	def vagitable_product(self):
		return self.get_queryset().vagitable()
	def book_product(self):
		return self.get_queryset().book()
	def electronic_product(self):
		return self.get_queryset().electronic()
	def mens_fashion_product(self):
		return self.get_queryset().mens_fashion()
	def womens_fashion_product(self):
		return self.get_queryset().womens_fashion()
	def home_appliences_product(self):
		return self.get_queryset().home_appliences()
	def helth_product(self):
		return self.get_queryset().helth()
	def outdoor_product(self):
		return self.get_queryset().outdoor()

	def featured_all(self):
		return self.get_queryset().featured()

	def featured_get_by_id(self, id):
		qs = self.get_queryset().filter(id=id, featured=True, active=True)
		if qs.count()==1:
			return qs.first()
		else:
			return None

	def search(self, query):
		return self.get_queryset().active().search(query)

	def featured_search(self, query):
		return self.get_queryset().featured().search(query)

class Product(models.Model):

	STATUS_CHOICES = (
			('vagitable', 'Vagitable'),
			('book', 'book'),
			('electronic', 'Electronic'),
			('mens fashion', 'Mens fashion'),
			('womens fashion', 'Womens fashion'),
			('home appliences', 'Home appliences'),
			('helth', 'Helth'),
			('outdoor', 'Outdoor')
		)

	title 		= models.CharField(max_length=120)
	slug 		= models.SlugField(blank=True, unique=True)
	slugcom 	= models.BooleanField(default=False)
	description = models.TextField()
	price 		= models.DecimalField(decimal_places=2, max_digits=20, default=39.99)
	image 		= models.ImageField(upload_to=upload_image_path, null=True, blank=True)
	featured 	= models.BooleanField(default=False)
	active 		= models.BooleanField(default=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)
	category	= models.CharField(max_length=120, choices=STATUS_CHOICES, default='vagitable')
	is_digital	= models.BooleanField(default=False)

	objects = ProductManager()

	class Meta:
		ordering = [
			'-timestamp'
		]

	def get_product_detail_url(self):
		return reverse('ProductDetailSlugView', args=[self.slug])

	def get_featured_product_detail_url(self):
		return reverse('featured_product_detail_slug', args=[self.slug])

	def __str__(self):
		return self.title

	def get_downloads(self):
		qs = self.productfile_set.all()
		return qs

	@property
	def name(self):
		return self.title
	
def product_pre_save_reciever(sender, instance, *args, **kwargs):
	if instance.slugcom == False:
		plus = get_unique_path(20)
		if instance.slug:
			this = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
			if not instance.slug.endswith(this):
				instance.slug = instance.slug + '-' + str(plus)
		if not instance.slug:
			instance.slug = 'slug-' + str(plus)
pre_save.connect(product_pre_save_reciever, sender=Product)


def upload_product_file_path(instance, filename):
	id_ = instance.id
	if id_ is None:
		Klass = instance.__class__
		qs = Klass.objects.all().order_by('-pk')
		if qs.exists():
			id_ = qs.first().id + 1
	slug = instance.product.slug
	if not slug:
		slug = get_unique_path(20)
	path = "products/{slug}/{id_}/{filename}".format(slug=slug, id_=id_, filename=filename)
	return path

class ProductFile(models.Model):
	name 				= models.CharField(max_length=120, blank=True, null=True)
	product 			= models.ForeignKey(Product, on_delete='product')
	file 				= models.FileField(
											upload_to=upload_product_file_path, 
											storage=FileSystemStorage(location=settings.PREM_PRO_ROOT)
										) # PremProRootS3BotoStorage()
	free 				= models.BooleanField(default=False)
	user_required 		= models.BooleanField(default=False)

	def __str__(self):
		return str(self.file.name)

	def get_default_url(self):
		return self.product.get_product_detail_url()

	def get_download_url(self):
		return reverse('download', kwargs={
				'slug':self.product.slug, 
				'pk':self.pk
			})

	def generate_download_url(self):
		bucket = getattr(settings, 'AWS_STORAGE_BUCKET_NAME')
		region = getattr(settings, 'S3DIRECT_REGION')
		access_key = getattr(settings, 'AWS_ACCESS_KEY_ID')
		secret_key = getattr(settings, 'AWS_SECRET_ACCESS_KEY')
		PROTECTED_DIR_NAME = getattr(settings, 'PROTECTED_DIR_NAME')
		path = '{base}/{file}'.format(base=PROTECTED_DIR_NAME, file=str(self.file))
		if not bucket or not region or not access_key or not secret_key:
			return '/'
		aws_dl_object =  AWSDownload(access_key, secret_key, bucket, region)
		file_url = aws_dl_object.generate_url(path, new_filename=self.display_name)
		return file_url

	@property
	def get_name(self):
		return get_filename(self.file.name)

	@property
	def display_name(self):
		og_name = self.get_name
		if self.name:
			return self.name
		return og_name
