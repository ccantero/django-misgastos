from django.db import models
from django.contrib import auth

from django.contrib.auth import get_user_model

# Create your models here.
class User(auth.models.User,auth.models.PermissionsMixin):
	def __str__(self):
		return "@{}".format(self.username)

class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    telegram_user = models.CharField(max_length=255)
    chat_id = models.CharField(max_length=255, default='')

    def get_absolute_url(self):
        return reverse('/')

