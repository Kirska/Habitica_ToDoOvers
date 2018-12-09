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
]
