from django.db import models

# Create your models here.
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model
User = get_user_model()

class Budget(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(allow_unicode=True,unique=True)
	description = models.CharField(blank=True,default='',max_length=255)
	user = models.ForeignKey(User,related_name='budgets',on_delete=models.PROTECT)
	expired_date = models.DateField(blank=True,null=True)

	def get_absolute_url(self):
		return reverse('presupuestos:all')

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super().save(*args, **kwargs)

