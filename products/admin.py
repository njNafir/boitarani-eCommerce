from django.contrib import admin

from .models import Product, ProductFile

class ProductFileInline(admin.TabularInline):
	model = ProductFile
	extra = 1

class ProductAdmin(admin.ModelAdmin):
	list_display 		= ('__str__', 'slug', 'price', 'timestamp')
	list_filter 		= ('price', 'timestamp')
	search_fields 		= ('title', 'description')
	prepopulated_fields ={'slug':('title',)}
	ordering 			= ['-price','-timestamp']

	inlines 			= [ProductFileInline]

	class Meta:
		model = Product

admin.site.register(Product, ProductAdmin)