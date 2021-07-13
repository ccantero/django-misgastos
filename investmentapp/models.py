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

	def __str__(self):
		return self.name

	def update_quote(self):
		last_update = self.last_update
		now = timezone.now()

		dt_begin = datetime.fromtimestamp(last_update.timestamp())
		dt_end = datetime.fromtimestamp(now.timestamp())

		difference = dt_end - dt_begin
		seconds = difference.total_seconds()

		if self.name == 'BTC' and seconds > 360:
			print("Calling the API")
			response = requests.get('https://api.alternative.me/v2/ticker/?convert=USD')
			data = response.json()['data']

			quote = self.last_quote
			for key in data.keys():
				if data[key]['name'] == 'Bitcoin':
					quote = data[key]['quotes']['USD']['price']
					break

			self.last_quote = quote
			self.last_update = timezone.now()

			

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
		return round(self.get_actual_rate * self.amount,2)

	@property
	def get_actual_rate(self):
		old_quote = self.factor.last_quote
		self.factor.update_quote()
		if self.factor.last_quote != old_quote:
			self.factor.save()

		return round(self.factor.last_quote,2)

