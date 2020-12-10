from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return HttpResponse("Hello, world!")


def geek_page(request, geek_id: int):
    from . import models

    geek = models.Geek.objects.filter(id=geek_id).all().first()

    if geek:
        return HttpResponse(geek.name)
    else:
        return HttpResponse("No geek found")
