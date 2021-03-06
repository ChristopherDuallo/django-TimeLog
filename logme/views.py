import datetime
from django.http import HttpResponseRedirect, HttpRequest
from django.views import generic
from django.contrib import auth
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.contrib.auth.models import User
from logme.models import Account, History
from django.utils import timezone
from django.template import Context
from django.views.generic import FormView
from datetime import timedelta
from django.core.exceptions import ObjectDoesNotExist

from logme.forms import RegistrationForm

class Index(generic.TemplateView):
	template_name = 'logme/form.html'

	def get(self, request):

		if request.user.is_authenticated():
			return redirect('logat:home')
		else:
			return self.render_to_response({})


	def post(self, request, *args, **kwargs):	
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)

		if user is not None:

			try:				
				account = Account.objects.get(user=user)

			except ObjectDoesNotExist:
				return render(request, 'logme/form.html', {
	            'error_message': "Please Contact the Administrator for Activation",
	        	})
		
			else:

				auth.login(request,user)				
				log = History(account=account)						
				log.save()

				return redirect('logat:home')


		else:
			 return render(request, 'logme/form.html', {
            'error_message': "Username/Password Invalid. Please Try Again.",
        })



class Home_Page(generic.TemplateView):

	template_name = 'logme/home.html'


	def get(self, request):
		if request.user.is_authenticated():

			getting_last_history = self.request.user.account.history.last()
			sorting_history = self.request.user.account.history.order_by('-timein')
			filtered_history = self.request.user.account.history.filter(timein__startswith=datetime.date.today())
			
			timein = getting_last_history.timein

			today_total= timedelta(0)

			for total in filtered_history:
				today_total += total.totaltime

			return self.render_to_response({'sorts':sorting_history, 'timein':timein,'today_total':today_total})

		return redirect("logat:index")




	def post(self, request):
		
		logout = request.POST.get('logout', '')

		if logout is not None:	

			logout=self.request.user.account.history.last()
			
			logout.timeout = timezone.now()			

			logout.save()

			auth.logout(request)
			return redirect('logat:index')


class Register(FormView):
    template_name = 'logme/register.html'
    form_class = RegistrationForm
    success_url = '/'

    def post(self, request):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            form.save()
            return self.form_valid(form)

        else:
            return self.form_invalid(form)

