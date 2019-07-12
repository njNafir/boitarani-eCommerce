from django.urls import path, re_path
from .views import MarketingPreferenceUpdateView, MarketingWebhookView

urlpatterns = [
	re_path(r'marketing/email/', MarketingPreferenceUpdateView.as_view(), name='marketing_pref'),
	re_path(r'webhooks/mailchimp/', MarketingWebhookView.as_view(), name='webhooks_mailchimp'),
]