from django.db import models

# Create your models here.
from django.utils import timezone

class TelegramMessage(models.Model):
	message = models.TextField()
	chat_id = models.CharField(max_length=255)
	create_date = models.DateTimeField(default=timezone.now)