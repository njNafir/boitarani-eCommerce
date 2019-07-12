from django.contrib import admin

from .models import BillingProfile, Card, Charge

class AdminBillingProfile(admin.ModelAdmin):
	list_display = ('user', 'email', 'updated', 'created', 'active')
	list_filter = ('active', 'updated', 'created')
	search_fields = ('user', 'email')

admin.site.register(BillingProfile, AdminBillingProfile)

class AdminCard(admin.ModelAdmin):
	list_display = ('billing_profile','stripe_id','country','default','active','timestamp')
	list_filter = ('brand','exp_month','exp_year','default','active')
	search_fields = ('billing_profile', 'stripe_id')

admin.site.register(Card, AdminCard)

class AdminCharge(admin.ModelAdmin):
	list_display = ('billing_profile', 'stripe_id', 'paid', 'refunded', 'outcome_type', 'seller_message', 'risk_level')
	list_filter = ('paid', 'refunded', 'outcome_type', 'seller_message', 'risk_level')
	search_fields = ('billing_profile', 'stripe_id', 'outcome')

admin.site.register(Charge, AdminCharge)