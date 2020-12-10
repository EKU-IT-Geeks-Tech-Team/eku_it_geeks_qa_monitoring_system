from datetime import datetime
from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Role(models.Model):
    name = models.CharField(_("Name"), max_length=50)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(_("Name"), max_length=50)

    def __str__(self):
        return self.name


class ErrorType(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    severity = models.FloatField(_("Severity"))

    def __str__(self):
        return self.name


class Geek(models.Model):
    name = models.CharField(_("Name"), max_length=50)
    hire_date = models.DateField(
        _("Hire Date"), auto_now=False, auto_now_add=False
    )
    quit_date = models.DateField(
        _("Quit Date"), auto_now=False, auto_now_add=False, null=True
    )
    roles = models.ManyToManyField("qa.Role", verbose_name=_("Roles"))

    def __str__(self):
        return self.name


class Error(models.Model):
    type = models.ManyToManyField("qa.ErrorType", verbose_name=_("Error Type"))
    notes = models.TextField(_("Notes"))
    footprints_number = models.CharField(
        _("FP#"), max_length=10, default=None, blank=True, null=True)
    found_date = models.DateField(
        _("Found Date"), auto_now=False, auto_now_add=False, default=datetime.now()
    )
    committed_date = models.DateField(
        _("Committed Date"), auto_now=False, auto_now_add=False, null=True, default=None, blank=True
    )
    geeks = models.ManyToManyField("qa.Geek", verbose_name=_("Geeks"))
    coordinator = models.ForeignKey("qa.Geek", verbose_name=_(
        "Coordinator"), on_delete=models.CASCADE, related_name="error_coordinator"
    )
    tags = models.ManyToManyField("qa.Tag", verbose_name=_("Tags"))
