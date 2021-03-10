from django.contrib import admin

from categoriesapp import models

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'user')

admin.site.register(models.Category, CategoryAdmin)