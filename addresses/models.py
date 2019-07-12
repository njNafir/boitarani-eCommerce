from django.db import models
from billing.models import BillingProfile

ADDRESS_TYPE = (
		('billing', 'Billing'),
		('shipping', 'Shipping')
	)

class Address(models.Model):
	billing_profile = models.ForeignKey(BillingProfile, on_delete='billing_profile')
	address_type = models.CharField(max_length=120, choices=ADDRESS_TYPE)
	address_line_1 = models.CharField(max_length=120)
	address_line_2 = models.CharField(max_length=120, null=True, blank=True)
	city = models.CharField(max_length=120)
	postal_code = models.CharField(max_length=120)
	state = models.CharField(max_length=120)
	country = models.CharField(max_length=120, default='United State')

	def __str__(self):
		return str((self.postal_code, self.address_line_1, self.city, self.state, self.country))

	@property
	def name(self):
		return str(self.billing_profile)
	
	def get_address(self):
		return '{line1}, {line2}, {city}, {state}, {postal}, {country}'.format(
				line1 	= self.address_line_1,
				line2 	= self.address_line_2 or '',
				city 	= self.city,
				state	= self.state,
				postal 	= self.postal_code,
				country = self.country
			)