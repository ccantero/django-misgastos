from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from budgetsapp.models import Budget

User = get_user_model()

class Category(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(blank=True,default='',max_length=255)
	user = models.ForeignKey(User,related_name='categories',null=True, blank=True,on_delete=models.PROTECT)

	class Meta:
		verbose_name_plural = 'Categories'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('home')