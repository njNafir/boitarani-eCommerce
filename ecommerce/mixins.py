from django.utils.http import is_safe_url
import random, string, os

class RequestAttachMixin(object):
	def get_form_kwargs(self):
		kwargs = super(RequestAttachMixin, self).get_form_kwargs()
		kwargs['request'] = self.request
		return kwargs

class NextUrlMixin(object):
	default_path = '/'
	def get_next_url(self):
		request = self.request
		next_page 		= request.GET.get('next')
		next_post 		= request.POST.get('next')
		redirect_path 	= next_page or next_post or None
		if is_safe_url(redirect_path, request.get_host()):
			return redirect_path
		else:
			return self.default_path

def get_unique_path(how_many=10):
	range_ = how_many
	chars = string.ascii_lowercase + string.digits
	plus = ''.join(random.choice(chars) for _ in range(range_))
	dig = range(0,9)
	plus = plus + str(random.randint(0,9))
	return plus

def get_filename(file):
	return os.path.basename(file)