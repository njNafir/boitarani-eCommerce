from django.contrib import admin
from carts.models import Cart

class AdminCart(admin.ModelAdmin):
	list_display = ('user', 'total', 'updated', 'timestamp')
	list_filter = ('user', 'total', 'updated', 'timestamp')
	ordering = ['user', 'total', 'updated', 'timestamp']
	search_fields = ('user', 'total')

admin.site.register(Cart, AdminCart)