"""Django URLs - Habitica To Do Over tool
"""
from django.urls import path, re_path

from . import views

app_name = "to_do_overs_app"
urlpatterns = [
    path("", views.index, name="index"),
    re_path(r"^login/$", views.login, name="login"),
    re_path(r"^login_api_key/$", views.login_api_key, name="login_api_key"),
    re_path(r"^dashboard/$", views.dashboard, name="dashboard"),
    re_path(r"^create_task/$", views.create_task, name="create_task"),
    re_path(r"^create_task_action/$", views.create_task_action, name="create_task_action"),
    re_path(r"^logout/$", views.logout, name="logout"),
    re_path(r"^delete_task/(?P<task_pk>[-\w]+)/$", views.delete_task, name="delete_task"),
    re_path(
        r"^delete_task_confirm/(?P<task_pk>[-\w]+)/$",
        views.delete_task_confirm,
        name="delete_task_confirm",
    ),
    re_path(r"^edit_task/(?P<task_pk>[-\w]+)/$", views.edit_task, name="edit_task"),
    re_path(
        r"^edit_task_action/(?P<task_pk>[-\w]+)/$", views.edit_task_action, name="edit_task_action"
    ),
    re_path(r"^test_500/", views.test_500_view, name="test_500"),
]
