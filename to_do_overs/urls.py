"""Django URLs - Habitica To Do Over tool
"""
from Habitica_ToDoOvers.urls import url

from . import views

app_name = 'to_do_overs'
urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^login_api_key/$', views.login_api_key, name='login_api_key'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^create_task/$', views.create_task, name='create_task'),
    url(r'^create_task_action/$', views.create_task_action, name='create_task_action'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^delete_task/(?P<task_pk>[-\w]+)/$', views.delete_task, name='delete_task'),
    url(r'^delete_task_confirm/(?P<task_pk>[-\w]+)/$', views.delete_task_confirm, name='delete_task_confirm'),
    url(r'^edit_task/(?P<task_pk>[-\w]+)/$', views.edit_task, name='edit_task'),
    url(r'^edit_task_action/(?P<task_pk>[-\w]+)/$', views.edit_task_action, name='edit_task_action'),
    url(r'^test_500/', views.test_500_view, name='test_500'),
]
