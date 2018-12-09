# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from app_functions.to_do_overs_data import ToDoOversData
import django.contrib.messages as messages
import jsonpickle


# Create your views here.
def index(request):
    return render(request, 'to_do_overs/index.html')


def login(request):
    session_class = ToDoOversData()

    session_class.username = request.POST['username']
    session_class.password = request.POST['password']

    if session_class.login():
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
        return render(request, 'to_do_overs/create_task.html')
    else:
        messages.warning(request, 'You need to log in to view that page.')
        return redirect('to_do_overs:index')


def create_task_action(request):
    session_class = jsonpickle.decode(request.session['session_data'])
    if session_class.logged_in:
        print "in cta"
        session_class.task_name = request.POST['task']
        if session_class.create_task():
            messages.success(request, 'Task created successfully.')
            return redirect('to_do_overs:dashboard')
        else:
            messages.warning(request, 'Task creation failed.')
            return redirect('to_do_overs:create_task')
    else:
        messages.warning(request, 'You need to log in to view that page.')
        return redirect('to_do_overs:index')
