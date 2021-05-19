from django.contrib import admin

from . import models

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','telegram_user')

admin.site.register(models.Profile, ProfileAdmin)