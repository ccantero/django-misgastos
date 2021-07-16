from django.db import models

# Create your models here.
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()

import requests
from datetime import datetime

class Conversion(models.Model):
	name = models.CharField(max_length=100)
	last_update = models.DateTimeField(default=timezone.now)
	last_quote = models.FloatField(default=0.0)
	active_for_selection = models.BooleanField(default=False)

	def __str__(self):
		return self.name
	

class Invest(models.Model):
	name = models.CharField(max_length=100)
	amount = models.FloatField()
	initial_rate = models.FloatField()
	create_date = models.DateTimeField(default=timezone.now)
	factor = models.ForeignKey(	Conversion,
									related_name='factor',
									on_delete=models.PROTECT)
	user = models.ForeignKey(User,related_name='investments',on_delete=models.PROTECT)

	def get_absolute_url(self):
		return reverse('inversiones:all')

	@property
	def get_initial_amount(self):
		return round(self.initial_rate * self.amount,2)

	@property
	def get_actual_amount(self):
		if self.factor.name == 'ARS':
			return round(self.amount / self.get_actual_rate,2)

		return round(self.get_actual_rate * self.amount,2)		

	@property
	def get_actual_amount_ars(self):
		if self.factor.name != 'ARS':
			list_of_conversion_objs = Conversion.objects.filter(name__iexact="ARS")
			ars_conversion_obj = list_of_conversion_objs[0]
			return round(ars_conversion_obj.last_quote * self.get_actual_rate * self.amount,2)

		return round(self.amount,2)


	@property
	def get_actual_rate(self):
		return round(self.factor.last_quote,2)

