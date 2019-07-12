from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import EmailActivation, GuestEmail
from django.utils.safestring import mark_safe
from django.urls import reverse
from .signals import user_loged_in_signal

User = get_user_model()

class ReactivateEmailForm(forms.Form):
	email = forms.EmailField(widget=forms.EmailInput(attrs={
			'class':'form-control',
			'placeholder':'example@ex.com'
		}))

	def clean_email(self):
		email = self.cleaned_data.get('email')
		qs = EmailActivation.objects.email_exists(email)
		if not qs.exists():
			register_link = reverse('register_page')
			msg = """Your email is not exists, Do you want to <a href="{register_l}">register</a> now?""".format(register_l=register_link)
			raise forms.ValidationError(mark_safe(msg))
		return email

class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserDetailChangeForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['first_name'].widget.attrs.update({'class':'form-control', 'placeholder':'First name'})
		self.fields['last_name'].widget.attrs.update({'class':'form-control', 'placeholder':'Last name'})
		self.fields['full_name'].widget.attrs.update({'class':'form-control', 'placeholder':'Full name'})

	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'full_name')

class UserAdminChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()
    class Meta:
        model = User
        fields = ('email', 'password', 'is_active', 'admin')

    def clean_password(self):
        return self.initial["password"]

class GuestForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['email'].widget.attrs.update({'class':'form-control', 'placeholder':'example@exm.com'})

	class Meta:
		model = GuestEmail
		fields = [
			'email'
		]

	def __init__(self, request, *args, **kwargs):
		self.request = request
		super(GuestForm, self).__init__(*args, **kwargs)

	def save(self, commit=True):
		request = self.request
		obj 	= super(GuestForm, self).save(commit=False)
		if commit:
			obj.save()
			request = self.request
			request.session['guest_user_id'] = obj.id
		return obj


class LoginForm(forms.Form):
	email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
			'class':'form-control',
			'placeholder':'Email',
		}))

	password = forms.CharField(widget=forms.PasswordInput(attrs={
			'class':'form-control',
			'placeholder':'Password',
		}))

	def __init__(self, request, *args, **kwargs):
		self.request = request
		super(LoginForm, self).__init__(*args, **kwargs)


	def clean(self):
		request = self.request
		data = self.cleaned_data
		email 			= data.get('email')
		password 		= data.get('password')
		qs = User.objects.filter(email=email)
		if qs.exists():
			not_active = qs.filter(is_active=False)
			if not_active.exists():
				resend_e_link = reverse('resend_activation')
				resend_e_msg = """<a href="{resend_link}">resend confirmation?</a>""".format(resend_link=resend_e_link)
				is_confirmable = EmailActivation.objects.filter(email=email).confirmable().exists()
				if is_confirmable:
					msg1 = """<h3>Please check mail and confirm email, or </h3>""" + resend_e_msg
					raise forms.ValidationError(mark_safe(msg1))
				is_email_exists = EmailActivation.objects.email_exists(email).exists()
				if is_email_exists:
					msg2 = """<h3>Email not confirmed, </h3>""" + resend_e_msg
					raise forms.ValidationError(mark_safe(msg2))
				if not is_confirmable and not is_email_exists:
					msg3 = """<h3>User is inactive.</h3>"""
					raise forms.ValidationError(mark_safe(msg3))

		user 			= authenticate(request, username=email, password=password)
		if user is None:
			raise forms.ValidationError('Invalid credentials')
		login(request, user)
		self.user = user
		user_loged_in_signal.send(user.__class__, instance=user, request=request)
		try:
			del request.session['guest_user_id']
		except:
			pass
		return data


class RegisterForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['first_name'].widget.attrs.update({
			'class': 'form-control', 
			'placeholder': 'Your first name (Not required)'
		})
		self.fields['last_name'].widget.attrs.update({
			'class': 'form-control', 
			'placeholder': 'Your last name (Not required)'
		})
		self.fields['email'].widget.attrs.update({
			'class': 'form-control', 
			'placeholder': 'Example: abc@gmail.com'
		})
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
    		'class': 'form-control',
    		'placeholder': 'Password'
    	}))
	password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(attrs={
    		'class': 'form-control',
    		'placeholder': 'Password confirmation'
    	}))
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'email',)

	def clean_password2(self):
		password1 = self.cleaned_data.get("password1")
		password2 = self.cleaned_data.get("password2")
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match")
		return password2

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		user.set_password(self.cleaned_data["password1"])
		user.is_active = False # send confirmation email via signals
		if commit:
			user.save()
		return user
	
	# class GuestForm(forms.Form):
	# 	email = forms.EmailField(widget=forms.EmailInput(attrs={
	# 			'class':'form-control',
	# 			'placeholder':'Email'
	# 		}))
	# def form_valid(self, form):
	# 	request = self.request
	# 	next_page 		= request.GET.get('next')
	# 	next_post 		= request.POST.get('next')
	# 	redirect_path 	= next_page or next_post or None
	# 	email 			= form.cleaned_data.get('email')
	# 	password 		= form.cleaned_data.get('password')
	# 	user 			= authenticate(request, username=email, password=password)

	# 	if user is not None:
	# 		if not user.is_active:
	# 			messages.error(request, 'The user is not active yet.')
	# 			return super(LoginView, self).form_invalid(form)
	# 		login(request, user)
	# 		user_loged_in_signal.send(user.__class__, instance=user, request=request)
	# 		try:
	# 			del request.session['guest_user_id']
	# 		except:
	# 			pass
	# 		if is_safe_url(redirect_path, request.get_host()):
	# 			return redirect(redirect_path)
	# 		else:
	# 			return redirect('/')
	# 	else:
	# 		return redirect('/register')
	# 	return super(LoginView, self).form_invalid(form)

	# class RegisterForm(forms.Form):
	# 	username = forms.CharField(widget=forms.TextInput(attrs={
	# 			'class':'form-control',
	# 			'placeholder':'Username'
	# 		}))

	# 	email = forms.EmailField(widget=forms.EmailInput(attrs={
	# 			'class':'form-control',
	# 			'placeholder':'Email'
	# 		}))

	# 	password = forms.CharField(widget=forms.PasswordInput(attrs={
	# 			'class':'form-control',
	# 			'placeholder':'Password'
	# 		}))

	# 	password2 = forms.CharField(label='Confirm password' , widget=forms.PasswordInput(attrs={
	# 			'class':'form-control',
	# 			'placeholder':'Confirm password'
	# 		}))

	# 	def clean_username(self):
	# 		User = get_user_model()
	# 		username = self.cleaned_data.get('username')
	# 		query = User.objects.filter(username=username)
	# 		if query.exists():
	# 			raise forms.ValidationError('Name already taken')
	# 		else:
	# 			return username

	# 	def clean_email(self):
	# 		User = get_user_model()
	# 		email = self.cleaned_data.get('email')
	# 		query = User.objects.filter(email=email)
	# 		if query.exists():
	# 			raise forms.ValidationError('Email already taken')
	# 		elif 'gmail.com' not in email:
	# 			raise forms.ValidationError('Email has to be gmail.com')
	# 		else:
	# 			return email


	# 	def clean(self):
	# 		data = self.cleaned_data
	# 		password = self.cleaned_data.get('password')
	# 		password2 = self.cleaned_data.get('password2')
	# 		if password2 != password:
	# 			raise forms.ValidationError('Password not matched')
	# 		else:
	# 			return data