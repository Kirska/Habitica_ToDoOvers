# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return render(request, 'to_do_overs/index.html')


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    return render(request, 'to_do_overs/dashboard.html', {
        'username': username,
    })

