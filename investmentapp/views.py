from django.shortcuts import render

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from investmentapp.models import Invest
from investmentapp import forms

# Create your views here.
class CreateInvestment(LoginRequiredMixin,generic.CreateView):
	#fields = ['name','amount','initial_rate', 'factor']
	model = Invest
	form_class = forms.InvestForm

	def form_valid(self,form):			
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()
		return super().form_valid(form)

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs

class UpdateInvestment(LoginRequiredMixin,UserPassesTestMixin,generic.UpdateView):
	form_class = forms.InvestForm
	model = Invest
	#fields = ['name']

	def test_func(self):
		invests = Invest.objects.filter(pk__exact=self.kwargs.get('pk'))
		if len(invests) == 1:
			myinvest = invests[0]

			if myinvest.user.username == self.request.user.username:
				return True

		raise PermissionDenied("You are not authenticated to edit this.")

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs


class DeleteInvestment(LoginRequiredMixin,UserPassesTestMixin,generic.DeleteView):
	model = Invest
	#select_related = ('user','group')
	success_url = reverse_lazy('inversiones:all')

	def test_func(self):
		investments = Invest.objects.filter(pk__exact=self.kwargs.get('pk'))
		if len(investments) == 1:
			myinvest = investments[0]

			if myinvest.user.username == self.request.user.username:
				return True

		raise PermissionDenied("You are not authenticated to edit this.")

	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(pk=self.kwargs.get('pk'))

	# TODO: Fix this! 20210329
	def get_success_url__(self):
		next_url = self.request.POST.get('next', 'home')
		print(next_url)
		return HttpResponseRedirect(next_url)

	def delete(self,*args,**kwargs):
		return super().delete(*args,**kwargs)


class ListInvestment(LoginRequiredMixin,generic.ListView):
	model = Invest

	def get_queryset(self):
		queryset = super().get_queryset()
		# Fix for django.db.utils.ProgrammingError: can't adapt type 'SimpleLazyObject'
		myuser = str(self.request.user)
		return queryset.filter(user__username__iexact=myuser).order_by('name')

	def get_context_data(self, **kwargs):
	 	context = super().get_context_data(**kwargs)
	 	myuser = str(self.request.user)
	 	investments = Invest.objects.filter(user__username__iexact=myuser)
	 	amount_usd = 0
	 	amount_ars = 0
	 	for investment in investments:
	 		amount_ars += investment.get_actual_amount_ars
	 		amount_usd += investment.get_actual_amount


	 	context['amount_ars'] = round(amount_ars,2)
	 	context['amount_usd'] = round(amount_usd,2)
	 	return context
