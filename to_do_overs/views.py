# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from app_functions.to_do_overs_data import ToDoOversData
from forms import TasksForm
from models import Users
import django.contrib.messages as messages
import jsonpickle


# Create your views here.
def index(request):
    return render(request, 'to_do_overs/index.html')


def login(request):
    session_class = ToDoOversData()

    session_class.username = request.POST['username']
    password = request.POST['password']

    if session_class.login(password):
        request.session['session_data'] = jsonpickle.encode(session_class)
        return redirect('to_do_overs:dashboard')
    else:
        messages.warning(request, 'Login failed.')
        return render(request, 'to_do_overs/index.html')


def login_api_key(request):
    session_class = ToDoOversData()

    session_class.hab_user_id = request.POST['user_id']
    session_class.api_token = request.POST['api_token']

    if session_class.login_api_key():
        request.session['session_data'] = jsonpickle.encode(session_class)
        return redirect('to_do_overs:dashboard')
    else:
        messages.warning(request, 'Login failed.')
        return redirect('to_do_overs:index')


def dashboard(request):
    session_class = jsonpickle.decode(request.session['session_data'])
    if session_class.logged_in:
        username = session_class.username
        return render(request, 'to_do_overs/dashboard.html', {
                'username': username,
        })
    else:
        messages.warning(request, 'You need to log in to view that page.')
        return redirect('to_do_overs:index')


def create_task(request):
    session_class = jsonpickle.decode(request.session['session_data'])
    if session_class.logged_in:
        form = TasksForm()
        return render(request, 'to_do_overs/create_task.html', {'form': form})
    else:
        messages.warning(request, 'You need to log in to view that page.')
        return redirect('to_do_overs:index')


def create_task_action(request):
    session_class = jsonpickle.decode(request.session['session_data'])
    if session_class.logged_in:
        form = TasksForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.notes += "\n\n:repeat:Automatically created by ToDoOvers API tool."
            task.owner = Users.objects.get(user_id=session_class.hab_user_id)

            session_class.notes = task.notes
            session_class.task_name = task.name
            session_class.task_days = task.days
            session_class.priority = task.priority

            if int(session_class.task_days) < 0:
                messages.warning(request, 'Invalid repeat day number.')
                return redirect('to_do_overs:create_task')
            if session_class.create_task():
                messages.success(request, 'Task created successfully.')
                task.task_id = session_class.task_id
                task.save()
                return redirect('to_do_overs:dashboard')
            else:
                messages.warning(request, 'Task creation failed.')
                return redirect('to_do_overs:create_task')
    else:
        messages.warning(request, 'You need to log in to view that page.')
        return redirect('to_do_overs:index')


def logout(request):
    request.session.flush()
    return render(request, 'to_do_overs/index.html')
