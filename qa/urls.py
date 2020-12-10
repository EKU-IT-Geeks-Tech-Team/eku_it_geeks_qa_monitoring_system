from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("geek/<int:geek_id>", views.geek_page)
]
