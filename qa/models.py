from datetime import datetime
from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone

# Create your models here.

# Role refers to the position they hold (i.e. Coordinator, marketing or standard geek)


class Role(models.Model):
    name = models.CharField(_("Name"), max_length=50)

    def __str__(self):
        return self.name

# Tags are associated with errors. One error can have multiple tags (i.e. closing, paperwork etc.)


class Tag(models.Model):
    name = models.CharField(_("Name"), max_length=50)

    def __str__(self):
        return self.name

# Error type refers to a more specific description than tag. It can refer to things like "Late For Work"


class ErrorType(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    severity = models.FloatField(_("Severity"))

    def __str__(self):
        return self.name

# Employee referes to each employee that can be associated with an error. This data will be used for reports


class Employee(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    hire_date = models.DateField(
        _("Hire Date"), auto_now=False, auto_now_add=False
    )
    quit_date = models.DateField(
        _("Leave Date"), auto_now=False, auto_now_add=False, null=True, default=None, blank=True
    )
    roles = models.ManyToManyField("qa.Role", verbose_name=_("Roles"))

    def __str__(self):
        return self.name

# Specifically for errors. Includes all relevant data to an error


class Error(models.Model):
    notes = models.TextField(_("Notes"))
    footprints_number = models.CharField(
        _("FP#"), max_length=10, default=None, blank=True, null=True)
    found_date = models.DateField(
        _("Found Date"), auto_now=False, auto_now_add=False, default=timezone.now
    )
    committed_date = models.DateField(
        _("Committed Date"), auto_now=False, auto_now_add=False, null=True, default=None, blank=True
    )
    type = models.ForeignKey("qa.ErrorType", verbose_name=_(
        "Error Type"), on_delete=models.CASCADE
    )
    employees = models.ForeignKey("qa.Employee", verbose_name=_(
        "Employee"), on_delete=models.CASCADE, related_name="error_employee")
    coordinator = models.ForeignKey("qa.Employee", verbose_name=_(
        "Coordinator"), on_delete=models.CASCADE, related_name="error_coordinator"
    )
    tags = models.ManyToManyField("qa.Tag", verbose_name=_("Tags"))

    @property
    def get_employees(self):
        return ", ".join([e.name for e in self.employees.all()])
