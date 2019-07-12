from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView, DetailView, View, UpdateView
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.urls import reverse
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from .forms import LoginForm, RegisterForm, GuestForm, ReactivateEmailForm, UserDetailChangeForm
from .models import GuestEmail, EmailActivation
from ecommerce.mixins import RequestAttachMixin, NextUrlMixin

# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator

class AccountHomeView(LoginRequiredMixin, DetailView):
	template_name = 'accounts/home.html'
	def get_object(self):
		return self.request.user

class EmailActivationView(FormMixin, View):
	success_url = '/login/'
	form_class = ReactivateEmailForm
	key = None
	def get(self, request, key=None, *args, **kwargs):
		if key is not None:
			self.key = key
			qs = EmailActivation.objects.filter(key__iexact=key)
			not_active = qs.confirmable()
			if not_active.count() == 1:
				obj = not_active.first()
				obj.activate()
				messages.success(request, 'Your email is confirmed, please login.')
				return redirect('login_page')
			else:
				already_active = qs.filter(activated=True)
				if already_active.exists():
					reset_link = reverse('password_reset')
					msg = """Your email already has been confirmed,
					Do you need to reset <a href="{reset_link}">your password</a>?
					""".format(reset_link=reset_link)
					messages.success(request, mark_safe(msg))
					return redirect('login_page')
		context = {
			'form':self.get_form(),
			'key':self.key
		}
		return render(request, 'registration/activation_error.html', context)

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		request = self.request
		msg = """Activation link sent, please check your email."""
		messages.success(request, msg)
		email = form.cleaned_data.get('email')
		obj = EmailActivation.objects.email_exists(email).first()
		user = obj.user
		new_activation = EmailActivation.objects.create(user=user, email=email)
		new_activation.send_activation()
		return super(EmailActivationView, self).form_valid(form)

	def form_invalid(self, form):
		request = self.request
		context = {
			'form':form,
			'key':self.key
		}
		return render(request, 'registration/activation_error.html', context)

class GuestRegisterView(NextUrlMixin, RequestAttachMixin, CreateView):
	form_class = GuestForm
	default_path = '/register/'

	def get_success_url(self):
		return self.get_next_url()

	def form_invalid(self, form):
		return redirect(self.default_path)

class LoginView(NextUrlMixin, RequestAttachMixin, FormView):
	form_class = LoginForm
	template_name = 'auth/login.html'
	success_url = '/'
	default_path = '/'

	def form_valid(self, form):
		redirect_path = self.get_next_url()
		return redirect(redirect_path)


class RegisterView(CreateView):
	form_class = RegisterForm
	template_name = 'auth/register.html'
	success_url = '/login'

class UserDetailChangeView(LoginRequiredMixin, UpdateView):
	form_class = UserDetailChangeForm
	template_name = 'accounts/snippets/form.html'

	def get_object(self):
		return self.request.user

	def get_context_data(self, *args, **kwargs):
		context = super(UserDetailChangeView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Change your info...'
		return context

	def get_success_url(self):
		return reverse('account_home')

# def it_deletable(obj):

	# def guest_register(request):
	# 	next_page 		= request.GET.get('next')
	# 	next_post 		= request.POST.get('next')
	# 	redirect_path 	= next_page or next_post or None
	# 	guest_form 			= GuestForm(request.POST or None)

	# 	if guest_form.is_valid():
	# 		email 			= guest_form.cleaned_data.get('email')
	# 		guest_obj 		= GuestEmail.objects.create(email=email)
	# 		guest_obj_id 	= guest_obj.id
	# 		request.session['guest_user_id'] = guest_obj_id
	# 		if is_safe_url(redirect_path, request.get_host()):
	# 			return redirect(redirect_path)
	# 		else:
	# 			return redirect('/register/')

	# 	return redirect('/register/')

	# @login_required
	# def login_required_view(request):
	# 	return render(request, 'accounts/home.html', {})



	# class LoginRequiredMixin(object):
	# 	@method_decorator(login_required)
	# 	def dispatch(self, request, *args, **kwargs):
	# 		return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

	# class LoginRequiredView(LoginRequiredMixin, DetailView):
	# 	template_name = 'accounts/home.html'
	# 	def get_object(self):
	# 		return self.request.user



	# class LoginRequiredView(DetailView):
	# 	template_name = 'accounts/home.html'
	# 	def get_object(self):
	# 		return self.request.user

	# 	@method_decorator(login_required)
	# 	def dispatch(self, *args, **kwargs):
	# 		return super(LoginRequiredView, self).dispatch(*args, **kwargs)


	# def login_page(request):

	# 	login_form = LoginForm(request.POST or None)

	# 	context = {
	# 		'form':login_form,
	# 	}

	# 	next_page 		= request.GET.get('next')
	# 	next_post 		= request.POST.get('next')
	# 	redirect_path 	= next_page or next_post or None

	# 	if login_form.is_valid():
	# 		#print(request.user.is_authenticated)
	# 		print(login_form.cleaned_data)
	# 		email 	= login_form.cleaned_data.get('email')
	# 		password 	= login_form.cleaned_data.get('password')
	# 		user 		= authenticate(request, username=email, password=password)

	# 		if user is not None:
	# 			#print(request.user.is_authenticated)
	# 			login(request, user)
				
	# 			try:
	# 				del request.session['guest_user_id']
	# 			except:
	# 				pass

	# 			if is_safe_url(redirect_path, request.get_host()):
	# 				return redirect(redirect_path)
	# 			else:
	# 				return redirect('/')

	# 		else:
	# 			print('Error')

	# 	return render(request, 'auth/login.html', context)

	# def register_page(request):
	# 	User = get_user_model()
	# 	register_form = RegisterForm(request.POST or None)
	# 	context = {
	# 		'form':register_form,
	# 	}
	# 	if register_form.is_valid():
	# 		register_form.save()
	# 	return render(request, 'auth/register.html', context)