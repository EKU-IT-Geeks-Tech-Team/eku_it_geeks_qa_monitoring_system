from django.conf.urls import url
from django.db.models import query
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.serializers import serialize
from django.template import context, loader
from django.template.response import ContentNotRenderedError
from . import models
from datetime import datetime, timedelta
from django.urls import reverse
from pprint import pprint

# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

    template = loader.get_template("qa/index.html.j2")

    error_names_counts = {}
    error_counts_by_day = {}

    queryset = models.Error.objects.order_by('committed_date').all()

    for error in queryset:
        # error count
        error_names_counts.setdefault(error.type.name, 0)
        error_names_counts[error.type.name] += 1

        # error count by week
        key = error.committed_date.strftime("%Y-%m-%d")
        error_counts_by_day.setdefault(key, 0)
        error_counts_by_day[key] += 1

    available_error_types = list(
        models.ErrorType.objects.values("id", "name").order_by("name").all()
    )

    available_employees = list(
        models.Employee.objects.values("id", "name").order_by("name").all()
    )

    available_coordinators = list(
        models.Employee.objects.filter(
            roles__name="Coordinator").values("id", "name").order_by("name").all()
    )

    available_tags = list(
        models.Tag.objects.values("id", "name").order_by("name").all()
    )

    error_count_by_week = get_error_count_by_week()

    week_ranges = []

    sorted_weeks = sorted(list(error_count_by_week.keys()))

    for monday in sorted_weeks:
        monday_dt = datetime.strptime(
            monday, "%Y-%m-%d")
        following_sunday = monday_dt + timedelta(days=6)
        week_ranges.append({
            "start": monday,
            "end": following_sunday.strftime("%Y-%m-%d")
        })

    context = {
        "title": "Home",
        # table
        "errors": models.Error.objects.order_by('-committed_date').all()[:30],

        # pie chart
        'pie_chart_labels': list(error_names_counts.keys()),
        'pie_chart_data': list(error_names_counts.values()),

        # line graph
        "line_graph_labels": sorted_weeks,
        "line_graph_data": [error_count_by_week[week] for week in sorted_weeks],

        # forms
        "available_error_types": available_error_types,
        "available_employees": available_employees,
        "available_coordinators": available_coordinators,
        "available_tags": available_tags,

        # buttons
        "weeks": [week_range for week_range in week_ranges if error_count_by_week[week_range["start"]] > 0],
    }

    return HttpResponse(template.render(context, request))


def employee_page(request, employee_id: int):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

    employee = models.Employee.objects.filter(id=employee_id).all().first()

    if employee:
        return HttpResponse(employee.name)
    else:
        return HttpResponse("No employee found")


def get_error(request, error_id: int):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

    e = models.Error.objects.filter(id=error_id).first()

    available_error_types = list(
        models.ErrorType.objects.values("id", "name").all()
    )

    available_employees = list(
        models.Employee.objects.values("id", "name").all()
    )

    available_coordinators = list(
        models.Employee.objects.filter(
            roles__name="Coordinator").values("id", "name").all()
    )

    available_tags = list(
        models.Tag.objects.values("id", "name").all()
    )

    context = {
        "title": f"Error: {e.id}",
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
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

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
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

    print(request.POST)

    prev = None

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

        prev = request.POST.get("prev")
        print(f"PREV TYPE: {type(prev)}")

    return redirect(prev if prev else "/")


def delete_error(request, error_id, _next):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

    error = models.Error.objects.filter(id=error_id).first()
    error.delete()

    return redirect(_next)


def get_error_count_by_week(query=None):

    # https://stackoverflow.com/questions/8746014/django-group-by-date-day-month-year

    from django.db.models.functions import TruncWeek
    from django.db.models import Count
    from datetime import datetime

    if not query:
        query = models.Error.objects.all()

    queryset = list(
        query
        .annotate(week=TruncWeek("committed_date"))
        .values("week")
        .annotate(c=Count("id"))
        .values("week", "c")
    )

    weeks = set([k['week'] for k in queryset])
    dict3 = []
    for week in weeks:
        temp_val = []
        for dict_ in queryset:
            if dict_['week'] == week:
                temp_val.append(dict_['c'])
        dict3.append({'week': week, 'c': sum(temp_val)})
    pprint(dict3)

    queryset = dict3

    # if query:

    # else:
    #     queryset = list(
    #         models.Error.objects
    #         .annotate(week=TruncWeek("committed_date"))
    #         .values("week")
    #         .annotate(c=Count("id"))
    #         .values("week", "c")
    #     )

    # [{"week": dt, "c": n}]

    # pprint(queryset)

    week_counts = {}

    if len(queryset) > 0:

        for data in queryset:
            key = data["week"].strftime("%Y-%m-%d")
            value = data["c"]

            week_counts[key] = value

        weeks_dt = [datetime.strptime(week, "%Y-%m-%d")
                    for week in week_counts.keys()]

        start_date = min(weeks_dt)
        end_date = max(weeks_dt)

        while start_date < end_date:
            week_counts.setdefault(
                start_date.strftime("%Y-%m-%d"),
                0
            )
            start_date += timedelta(days=7)

    return week_counts


def search_errors(request):
    if not request.user.is_authenticated:
        return redirect(reverse("login"))

    from django.utils.datastructures import MultiValueDictKeyError

    # gets list of every error
    # errors = models.Error.objects.all()
    errors = models.Error.objects

    # get tag names from URL
    tag_names = request.GET.getlist("tags")
    # Get data from database
    tags = models.Tag.objects.filter(name__in=tag_names)

    # filter out errors that dont have specified tags via loop
    for tag in tags:
        errors = errors.filter(tags__id=tag.id)

    start_date_str = request.GET.get("start")
    # if the startdate is not null (in other words a start date is specified)
    if start_date_str:
        # save that date in the right format
        start_date = datetime.strptime(
            # format it properly
            start_date_str,
            "%Y-%m-%d"
        )  # Dec. 16, 2020
        # do a search for all errors that were commited after start date
        errors = errors.filter(committed_date__gte=start_date)

    end_date_str = request.GET.get("end")
    # if the enddate is not null (in other words a end date is specified)
    if end_date_str:
        # save that date in the right format
        end_date = datetime.strptime(
            # format it properly
            end_date_str,
            "%Y-%m-%d"
        )  # Dec. 16, 2020
        # do a search for all errors that were commited before end date
        errors = errors.filter(committed_date__lte=end_date)

    employee_name = request.GET.get("employee")
    if employee_name:
        errors = errors.filter(employees__name=employee_name)

    coordinator_name = request.GET.get("coordinator")
    if coordinator_name:
        errors = errors.filter(coordinator__name=coordinator_name)

    fp_num = request.GET.get("fp_num")
    if fp_num:
        errors = errors.filter(footprints_number=fp_num)

    notes = request.GET.get("notes")
    if notes:
        errors = errors.filter(notes__contains=notes)

    _type = request.GET.get("type")
    if _type:
        errors = errors.filter(type__name=_type)

    available_error_types = list(
        models.ErrorType.objects.values("id", "name").all()
    )

    available_employees = list(
        models.Employee.objects.values("id", "name").all()
    )

    available_coordinators = list(
        models.Employee.objects.filter(
            roles__name="Coordinator").values("id", "name").all()
    )

    available_tags = list(
        models.Tag.objects.values("id", "name").all()
    )

    # sort by committed date
    errors = errors.order_by("-committed_date")

    error_count_by_week = get_error_count_by_week(query=errors)
    sorted_weeks = sorted(list(error_count_by_week.keys()))

    error_names_counts = {}
    for error in errors:
        # error count
        error_names_counts.setdefault(error.type.name, 0)
        error_names_counts[error.type.name] += 1

    context = {
        "title": "Search",
        # at this point all errors have the same tag
        "errors": errors,
        "available_error_types": available_error_types,
        "available_employees": available_employees,
        "available_coordinators": available_coordinators,
        "available_tags": available_tags,
        "current_query": {
            "notes": notes,
            "fp_num": fp_num,
            "start_date": start_date_str,
            "end_date": end_date_str,
            "type": _type,
            "employee": employee_name,
            "coordinator": coordinator_name,
            "tags": [tag.name for tag in list(tags.all())],
        },
        # pie chart
        'pie_chart_labels': list(error_names_counts.keys()),
        'pie_chart_data': list(error_names_counts.values()),
        # line graph
        "line_graph_labels": sorted_weeks,
        "line_graph_data": [error_count_by_week[week] for week in sorted_weeks],

    }
    template = loader.get_template("qa/search_errors.html.j2")

    return HttpResponse(template.render(context, request))
