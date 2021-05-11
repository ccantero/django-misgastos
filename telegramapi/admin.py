from django.contrib import admin

from telegramapi import models

# Register your models here.
class TelegramMessageAdmin(admin.ModelAdmin):
    list_display = ('message', 'chat_id')

admin.site.register(models.TelegramMessage, TelegramMessageAdmin)