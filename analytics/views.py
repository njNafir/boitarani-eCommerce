from django.shortcuts import render, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from orders.models import Order
from django.utils import timezone

# https://www.codingforentrepreneurs.com/blog/datetime-monthly-ranges/

class SalesView(LoginRequiredMixin, TemplateView):
	template_name = 'analytics/sales.html'
	def dispatch(self, *args, **kwargs):
		user = self.request.user
		if not user.is_staff:
			return render(self.request, '400.html', {})
		return super(SalesView, self).dispatch(*args, **kwargs)

	def get_context_data(self, *args, **kwargs):
		context = super(SalesView, self).get_context_data(*args, **kwargs)
		context['title'] = 'Sales analytic view for staff and admin.'
		qs = Order.objects.all().not_created()
		context['today'] = qs.by_range(timezone.now().date()).get_recent_breakpoint()
		context['this_week'] = qs.by_weeks_range(week_ago=1, number_of_week=1).get_recent_breakpoint()
		context['last_four_week'] = qs.by_weeks_range(week_ago=5, number_of_week=4).get_recent_breakpoint()
		return context