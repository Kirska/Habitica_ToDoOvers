from Habitica_ToDoOvers.urls import url

from . import views

urlpatterns = [
    url('', views.index, name='index'),
]
