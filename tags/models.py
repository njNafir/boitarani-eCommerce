from django.db import models
from products.models import Product
from django.urls import reverse

class ProductTag(models.Model):
	title 		= models.CharField(max_length=120)
	slug 		= models.SlugField(unique=True)
	timestamp 	= models.DateTimeField(auto_now_add=True)
	active 		= models.BooleanField(default=True)
	products 	= models.ManyToManyField(Product, blank=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('tag_detail', args=[self.slug])