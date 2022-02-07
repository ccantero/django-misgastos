from django.db import models

# Create your models here.
class Loan(models.Model):
	amount_cuota = models.FloatField()
	amount_deuda = models.FloatField()
	
	def get_absolute_url(self):
		return reverse('home')

	def __str__(self):
		return 'LoanModel'