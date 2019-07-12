from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import GuestEmail, EmailActivation

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    list_display = ('email', 'staff', 'admin', 'is_active')
    list_filter = ('staff', 'admin', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'full_name', 'description')}),
        ('Permissions', {'fields': ('staff', 'admin', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)

admin.site.unregister(Group)

class EmailActivationAdmin(admin.ModelAdmin):
    list_display = ('user', 'key', 'activated', 'forced_expired', 'expires', 'timestamp', 'updated')
    list_filter = ('activated', 'forced_expired', 'expires', 'timestamp', 'updated')
    search_fields = ('user', 'email', 'key')

    class Meta:
        Model = EmailActivation
        fields = [
            'user', 
            'email', 
            'key', 
            'activated', 
            'forced_expired', 
            'expires', 
            'timestamp', 
            'updated'
        ]

admin.site.register(EmailActivation, EmailActivationAdmin)

class GuestEmailAdmin(admin.ModelAdmin):
	list_display = ('email', 'created', 'active')
	list_filter = ('created', 'updated', 'active')
	search_fields = ('email',)

admin.site.register(GuestEmail, GuestEmailAdmin)