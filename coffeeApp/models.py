from django.db import models

# Create your models here.

class Coffee(models.Model):
	coffeeName = models.CharField(max_length=100)
	coffeeDescription = models.TextField(blank=True,default='')
	coffeeIntensity = models.PositiveIntegerField(default=1)
	isRistretto = models.BooleanField(default=False)
	isEspresso = models.BooleanField(default=False)
	isLungo = models.BooleanField(default=False)

	class Meta:
		verbose_name_plural = 'Coffees'

	def __str__(self):
		return self.coffeeName

	def get_absolute_url(self):
		return reverse('home')

