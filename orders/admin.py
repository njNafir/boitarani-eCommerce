from django.contrib import admin
from .models import Order, ProductPurchase

class ProductPurchaseAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'order_id', 'billing_profile', 'refunded')
	list_filter = ('refunded', 'timestamp', 'updated')
	search_fields = ('__str__', 'billing_profile', 'order_id')

admin.site.register(ProductPurchase, ProductPurchaseAdmin)

class OrderAdmin(admin.ModelAdmin):
	list_display = ('order_id', 'status', 'shipping_total', 'total')
	list_filter = ('status', 'order_id')
	search_fields = ('order_id', 'shipping_total', 'total', 'status')

admin.site.register(Order, OrderAdmin)