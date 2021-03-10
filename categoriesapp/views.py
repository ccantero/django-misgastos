from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from categoriesapp.models import Category
from budgetsapp.models import Budget

from django.contrib.auth.models import User

# Create your views here.
class CreateCategory(LoginRequiredMixin,generic.CreateView):
	fields = ['name', 'description']
	model = Category

	def get_context_data(self, **kwargs):
	 	context = super().get_context_data(**kwargs)
	 	context['HTTP_REFERER'] = self.request.META.get('HTTP_REFERER')
	 	return context

	def form_valid(self,form):			
		self.object = form.save(commit=False)
		self.object.user = self.request.user

		query_set = User.objects.filter(username='admin')
		admin_pk = query_set[0].pk

		querySet = Category.objects.filter(
			user__in=[self.request.user.pk,admin_pk]).filter(
			name__iexact=self.object.name)

		http_path = self.request.path
		next = self.request.POST.get('next', '/')

		if len(querySet) > 0:
			form.add_error("name", 'No se pudo')
			return super().form_invalid(form)	

		self.object.save()

		if http_path in next:
			return HttpResponseRedirect('/')

		return HttpResponseRedirect(next)