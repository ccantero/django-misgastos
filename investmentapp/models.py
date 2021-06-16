from django.db import models

# Create your models here.
from django.utils import timezone
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()


class Conversion(models.Model):
	name = models.CharField(max_length=100)

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