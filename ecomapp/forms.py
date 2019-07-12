from django.contrib.auth import get_user_model
from django import forms

class ContactForm(forms.Form):

	fullname = forms.CharField(widget=forms.TextInput(attrs={
			'class':'form-control',
			'placeholder':'Your name',
		}))

	email = forms.EmailField(widget=forms.EmailInput(attrs={
			'class':'form-control',
			'placeholder':'Your email',
		}))

	description = forms.CharField(widget=forms.Textarea(attrs={
			'class':'form-control',
			'placeholder':'Write description',
		}))

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if not 'gmail.com' in email:
			raise forms.ValidationError('Email has to be gmail.com')
		return email

	# def clean_description(self):
	# 	raise forms.ValidationError('Content is error but not errored')