from django.db import models

# Create your models here.
from django.utils import timezone

class Conversion(models.Model):
	name = models.CharField(max_length=100)

class Invest(models.Model):
	name = models.CharField(max_length=100)
	amount = models.FloatField()
	initial_rate = models.FloatField()
	create_date = models.DateTimeField(default=timezone.now)
	factor = models.ForeignKey(	Conversion,
									related_name='factor',
									on_delete=models.PROTECT)