# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from app_functions.to_do_overs_data import ToDoOversData
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
        return render(request, 'to_do_overs/index.html', {
            'error_message': 'Login failed',
        })


def dashboard(request):
    session_class = jsonpickle.decode(request.session['session_data'])
    username = session_class.username
    return render(request, 'to_do_overs/dashboard.html', {
            'username': username,
    })
