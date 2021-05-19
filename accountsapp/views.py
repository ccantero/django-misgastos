from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy

from accountsapp import forms
from accountsapp.models import Profile

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from django.core.exceptions import PermissionDenied

from django.contrib.auth.models import User
# Create your views here.

class SignUpView(CreateView):
	form_class = forms.UserCreateForm
	success_url = reverse_lazy('login')
	template_name = 'accountsapp/signup.html'


class CreateProfile(LoginRequiredMixin,UserPassesTestMixin,generic.CreateView):
	form_class = forms.ProfileForm
	model = Profile

	def test_func(self):
		return True

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs

	def form_valid(self,form):

		list_user = User.objects.filter(username__iexact=self.request.user.username)
		admin_user = list_user[0]
		self.object = form.save(commit=False)
		self.object.user = admin_user
		self.object.save()	

		return super().form_valid(form)


class UpdateProfile(LoginRequiredMixin,UserPassesTestMixin,generic.UpdateView):
	form_class = forms.ProfileForm
	model = Profile

	def get_object(self):
		# Fix for django.db.utils.ProgrammingError: can't adapt type 'SimpleLazyObject'
		myuser = str(self.request.user)
		return Profile.objects.get(user__username__iexact=myuser)

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update({'user': self.request.user})
		return kwargs

	def test_func(self):
		#TODO: Finish
		return True

		#raise PermissionDenied("You are not authenticated to edit this.")


class ListProfile(LoginRequiredMixin,generic.ListView):
	model = Profile

	def get_queryset(self):
		queryset = super().get_queryset()
		# Fix for django.db.utils.ProgrammingError: can't adapt type 'SimpleLazyObject'
		myuser = str(self.request.user)
		return queryset.filter(user__username__iexact=myuser)
