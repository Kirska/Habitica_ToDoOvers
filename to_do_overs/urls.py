from Habitica_ToDoOvers.urls import url

from . import views

app_name = 'to_do_overs'
urlpatterns = [
    url('^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
]
