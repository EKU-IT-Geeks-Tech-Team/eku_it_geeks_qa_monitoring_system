from django.urls import path

from . import views

# define namespace
app_name = "qa"

# Defines URL by string to decide where to send the user
urlpatterns = [
    #path(route, function, name)
    path("", views.index, name="index"),
    # if you go to URL: (name)/employee/(num) to will go to the webpage based
    path("employee/<int:employee_id>", views.employee_page),
    path("error/<int:error_id>", views.get_error, name="view_error"),
    path("create_error", views.create_error),
    path("update_error", views.update_error),
    path("delete_error/<int:error_id>/<path:_next>",
         views.delete_error, name="delete_error"),
    path("search", views.search_errors, name="search")
]
