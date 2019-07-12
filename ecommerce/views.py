from django.shortcuts import render, redirect

def jquery_test(request):
	return render(request, 'fasttracktojquery/index.html', {})