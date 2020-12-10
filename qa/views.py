from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.template import context, loader
from django.template.response import ContentNotRenderedError
from . import models

# Create your views here.


def index(request):
    template = loader.get_template("qa/index.html")

    error_counts = {}
    error_counts_by_day = {}

    queryset = models.Error.objects.order_by('found_date').all()

    for error in queryset:
        # error count
        error_counts.setdefault(error.type.name, 0)
        error_counts[error.type.name] += 1

        # error count by week
        key = error.found_date.strftime("%Y-%m-%d")
        error_counts_by_day.setdefault(key, 0)
        error_counts_by_day[key] += 1

    available_error_types = list(
        models.ErrorType.objects.values("id", "name").all()
    )

    available_employees = list(
        models.Employee.objects.values("id", "name").all()
    )

    available_coordinators = list(
        models.Employee.objects.values("id", "name").all()
    )

    available_tags = list(
        models.Tag.objects.values("id", "name").all()
    )

    context = {
        "errors": models.Error.objects.order_by('-found_date').all()[:10],
        'error_names': list(error_counts.keys()),
        'error_counts': list(error_counts.values()),
        "days": list(error_counts_by_day.keys()),
        "error_counts_by_day": list(error_counts_by_day.values()),
        "available_error_types": available_error_types,
        "available_employees": available_employees,
        "available_coordinators": available_coordinators,
        "available_tags": available_tags,
    }

    return HttpResponse(template.render(context, request))


def employee_page(request, employee_id: int):
    employee = models.Employee.objects.filter(id=employee_id).all().first()

    if employee:
        return HttpResponse(employee.name)
    else:
        return HttpResponse("No employee found")


def get_error(request, error_id: int):
    e = models.Error.objects.filter(id=error_id).values().first()

    return JsonResponse(e, safe=False)


def create_error(request):
    if request.method == "POST":
        notes = request.POST.get("notes")
        footprints_number = request.POST.get("footprints_number")
        found_date = request.POST.get("found_date")
        committed_date = request.POST.get("committed_date")
        error_type_id = request.POST.get("error_type_id")
        employee_id = request.POST.get("employee_id")
        coordinator_id = request.POST.get("coordinator_id")
        tag_ids = request.POST.getlist("tag_ids")

        print(tag_ids)

        error_type = models.ErrorType.objects.filter(id=error_type_id).first()
        employee = models.Employee.objects.filter(id=employee_id).first()
        coordinator = models.Employee.objects.filter(id=coordinator_id).first()

        tags = []
        for tag_id in tag_ids:
            tags.append(
                models.Tag.objects.filter(id=tag_id).first()
            )

        new_error = models.Error(
            notes=notes,
            footprints_number=footprints_number,
            found_date=found_date,
            committed_date=committed_date,
            type=error_type,
            employees=employee,
            coordinator=coordinator
        )

        new_error.save()

        print(request.POST)

        new_error.tags.set(tags)

    return redirect("/")
