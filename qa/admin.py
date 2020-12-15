from django.contrib import admin

from . import models


class AdminEmployee(admin.ModelAdmin):
    model = models.Employee
    list_display = ("name",)


class AdminErrorType(admin.ModelAdmin):
    model = models.ErrorType
    list_display = ("name", "severity")


class AdminError(admin.ModelAdmin):
    model = models.Error
    list_display = ("id", "coordinator", "employees", "found_date")
    ordering = ("found_date",)
    search_fields = ("notes",)


# Register the models (make them appear on screen)
admin.site.register(models.Employee, AdminEmployee)
admin.site.register(models.Error, AdminError)
admin.site.register(models.ErrorType, AdminErrorType)
admin.site.register(models.Role)
admin.site.register(models.Tag)
