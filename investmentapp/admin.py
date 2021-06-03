from django.contrib import admin

from . import models

# Register your models here.
class ConversionAdmin(admin.ModelAdmin):
    list_display = ('name', )

class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('name','initial_rate', 'amount', 'factor')

admin.site.register(models.Invest, InvestmentAdmin)
admin.site.register(models.Conversion, ConversionAdmin)