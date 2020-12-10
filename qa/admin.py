from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Geek)
admin.site.register(models.Error)
admin.site.register(models.ErrorType)
admin.site.register(models.Role)
admin.site.register(models.Tag)
