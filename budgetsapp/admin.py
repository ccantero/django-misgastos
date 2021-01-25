from django.contrib import admin

from . import models

# Register your models here.

class BudgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'user')

admin.site.register(models.Budget, BudgetAdmin)