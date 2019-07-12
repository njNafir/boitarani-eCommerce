from django.contrib import admin
from .models import ObjectViewed, UserSession

class ObjectViewdAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'user', 'content_type', 'object_id', 'ip_address', 'timestamp')
	list_filter = ('content_type', 'timestamp', 'user')
	search_fields = ('user', 'content_type', 'content_object')

admin.site.register(ObjectViewed, ObjectViewdAdmin)

class UserSessionAdmin(admin.ModelAdmin):
	list_display = ('user', 'ip_address', 'session_key', 'timestamp')
	search_fields = ('user', 'ip_address', 'session_key', 'timestamp')

admin.site.register(UserSession, UserSessionAdmin)