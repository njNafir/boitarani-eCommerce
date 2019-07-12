from django import forms
from .models import Address

class AddressForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# self.fields['billing_profile'].widget.attrs.update({'class':'form-control'})
		# self.fields['address_type'].widget.attrs.update({'class':'form-control'})
		self.fields['address_line_1'].widget.attrs.update({'class':'form-control', 'placeholder':'Address line 1'})
		self.fields['address_line_2'].widget.attrs.update({'class':'form-control', 'placeholder':'Address line 2'})
		self.fields['city'].widget.attrs.update({'class':'form-control', 'placeholder':'City'})
		self.fields['postal_code'].widget.attrs.update({'class':'form-control', 'placeholder':'Postal code'})
		self.fields['state'].widget.attrs.update({'class':'form-control', 'placeholder':'State'})
		self.fields['country'].widget.attrs.update({'class':'form-control', 'placeholder':'Country'})

	class Meta:
		model = Address
		fields = [
			# 'billing_profile',
			# 'address_type',
			'address_line_1',
			'address_line_2',
			'city',
			'postal_code',
			'state',
			'country',
		]