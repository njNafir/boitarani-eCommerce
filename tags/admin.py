from django.contrib import admin

from .models import ProductTag

class AdminProductTag(admin.ModelAdmin):
	list_display = ('__str__', 'slug', 'timestamp')
	list_filter = ('timestamp',)
	search_fields = ('title', 'products')
	prepopulated_fields = {'slug':('title',)}
	ordering = ['timestamp',]

admin.site.register(ProductTag, AdminProductTag)