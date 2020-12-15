from django.db.models import query
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.template import context, loader
from django.template.response import ContentNotRenderedError
from . import models
from datetime import datetime

# Create your views here.


def index(request):
    template = loader.get_template("qa/index.html.j2")

    error_names_counts = {}
    error_counts_by_day = {}

    queryset = models.Error.objects.order_by('found_date').all()

    for error in queryset:
        # error count
        error_names_counts.setdefault(error.type.name, 0)
        error_names_counts[error.type.name] += 1

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

    error_count_by_week = get_error_count_by_week()

    context = {
        # table
        "errors": models.Error.objects.order_by('-found_date').all()[:10],

        # pie chart
        'pie_chart_labels': list(error_names_counts.keys()),
        'pie_chart_data': list(error_names_counts.values()),

        # line graph
        "line_graph_labels": list(error_count_by_week.keys()),
        "line_graph_data": list(error_count_by_week.values()),

        # forms
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
    e = models.Error.objects.filter(id=error_id).first()

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
        "error": e,
        "formatted_found_date": e.found_date.strftime("%Y-%m-%d"),
        "formatted_committed_date": e.committed_date.strftime("%Y-%m-%d"),
        "available_error_types": available_error_types,
        "available_employees": available_employees,
        "available_coordinators": available_coordinators,
        "available_tags": available_tags
    }
    template = loader.get_template("qa/show_error.html.j2")

    return HttpResponse(template.render(context, request))


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


def update_error(request):
    print(request.POST)

    if request.method == "POST":  # update
        error = models.Error.objects.filter(id=request.POST.get("id")).first()

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

        error.notes = notes
        error.footprints_number = footprints_number
        error.found_date = found_date
        error.committed_date = committed_date
        error.type = error_type
        error.employees = employee
        error.coordinator = coordinator

        error.save()

        print(request.POST)

        error.tags.set(tags)

    return redirect("/")


def get_error_count_by_week():
    # https://stackoverflow.com/questions/8746014/django-group-by-date-day-month-year

    from django.db.models.functions import TruncWeek
    from django.db.models import Count
    from datetime import datetime

    queryset = list(
        models.Error.objects
        .annotate(week=TruncWeek("found_date"))
        .values("week")
        .annotate(c=Count("id"))
        .values("week", "c")
    )

    print(queryset)

    week_counts = {}

    for data in queryset:
        key = data["week"].strftime("%Y-%m-%d")
        value = data["c"]

        week_counts[key] = value

    return week_counts
