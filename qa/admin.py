from django.contrib import admin
from django.http import HttpResponse
import csv
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

    list_max_show_all = 10000
    list_per_page = 100

    actions = ["export_as_csv"]

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field)
                                   for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


# Register the models (make them appear on screen)
admin.site.register(models.Employee, AdminEmployee)
admin.site.register(models.Error, AdminError)
admin.site.register(models.ErrorType, AdminErrorType)
admin.site.register(models.Role)
admin.site.register(models.Tag)
