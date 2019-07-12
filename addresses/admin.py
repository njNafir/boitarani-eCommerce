from django.contrib import admin

from .models import Address

class AddressAdmin(admin.ModelAdmin):
	list_display = ('billing_profile', 'address_type', 'postal_code', 'country')
	list_filter = ('address_type', 'country', 'city', 'postal_code')
	search_fields = ('billing_profile', 'address_line_1', 'address_line_2', 'city', 'postal_code', 'state', 'country')

admin.site.register(Address, AddressAdmin)