from django import forms
from .models import MarketingPreference

class MarketingPreferenceUpdateForm(forms.ModelForm):
	subscribed = forms.BooleanField(label='Get marketing email? ', required=False)
	class Meta:
		model = MarketingPreference
		fields = [
			'subscribed',
		]