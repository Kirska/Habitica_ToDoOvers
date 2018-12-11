# -*- coding: utf-8 -*-
"""Django Views - Habitica To Do Over tool
"""
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from app_functions.to_do_overs_data import ToDoOversData
from forms import TasksForm
from models import Users, Tasks
import django.contrib.messages as messages
import jsonpickle
from app_functions.cipher_functions import encrypt_text


def index(request):
    """Homepage/Index View

    Args:
        request: the request from user.

    Returns:
        Rendering of the index page.
    """
    return render(request, 'to_do_overs/index.html')


def login(request):
    """Login request with username and password.

    This view will never actually be displayed.

    Args:
        request: the request from user.

    Returns:
        Redirects the index page on error. Redirects to the dashboard on success.
    """
    session_class = ToDoOversData()

    session_class.username = request.POST['username']
    password = request.POST['password']

    if session_class.login(password):
        request.session['session_data'] = jsonpickle.encode(session_class)
        return redirect('to_do_overs:dashboard')
    else:
        messages.warning(request, 'Login failed.')
        return redirect('to_do_overs:index')


def login_api_key(request):
    """Login request with user ID and API token.

    This view will never actually be displayed.

    Args:
        request: the request from user.

    Returns:
        Redirects the index page on error. Redirects to the dashboard on success.
    """
    session_class = ToDoOversData()

    session_class.hab_user_id = request.POST['user_id']
    session_class.api_token = encrypt_text(request.POST['api_token'].encode('utf-8'))

    if session_class.login_api_key():
        request.session['session_data'] = jsonpickle.encode(session_class)
        return redirect('to_do_overs:dashboard')
    else:
        messages.warning(request, 'Login failed.')
        return redirect('to_do_overs:index')


def dashboard(request):
    """The dashboard view once a user has logged in.

    Args:
        request: the request from user.

    Returns:
        Renders the dashboard if user is logged in. Redirects to index if user is not logged in.
    """
    session_class = jsonpickle.decode(request.session['session_data'])

    task_list = Tasks.objects.filter(owner__user_id=session_class.hab_user_id)

    if session_class.logged_in:
        username = session_class.username
        return render(request, 'to_do_overs/dashboard.html', {
                'username': username,
                'tasks': task_list,
        })
    else:
        messages.warning(request, 'You need to log in to view that page.')
        return redirect('to_do_overs:index')


def create_task(request):
    """View to create a new task.

    Args:
        request: the request from user.

    Returns:
        Renders the create task page if user is logged in. Redirects to index if user is logged out.
    """
    session_class = jsonpickle.decode(request.session['session_data'])
    if session_class.logged_in:
        form = TasksForm()
        return render(request, 'to_do_overs/create_task.html', {'form': form})
    else:
        messages.warning(request, 'You need to log in to view that page.')
        return redirect('to_do_overs:index')


def create_task_action(request):
    """Action to create task. This view is never displayed.

    Args:
        request: the request from user.

    Returns:
        Redirects to index if user is logged out. Otherwise attempts to create task. If creation is successful,
        redirects to dashboard. If creation fails, redirect back to create task page.
    """
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
    """Logout and clear the session.

    Args:
        request: the request from user.

    Returns:
        Renders index page.
    """
    request.session.flush()
    return render(request, 'to_do_overs/index.html')


def delete_task(request, task_pk):
    """Deletes the requested task from the tool database.

    Args:
        request: the request from user.
        task_id: the ID of the task to be deleted.

    Returns:
        Renders dashboard page with error or success.
    """
    session_class = jsonpickle.decode(request.session['session_data'])

    if not session_class.logged_in:
        messages.warning(request, 'You need to log in to view that page.')
        return redirect('to_do_overs:index')

    # first we need to check that this user owns this task
    task = Tasks.objects.get(pk=task_pk)
    owner = Users.objects.get(pk=task.owner.pk)

    logged_in_user = Users.objects.get(user_id=session_class.hab_user_id)
    print logged_in_user
    print owner
    if logged_in_user.pk == owner.pk:
        task.delete()
        messages.success(request, 'Task deleted successfully.')
        return redirect('to_do_overs:dashboard')
    else:
        messages.warning(request, 'You are not authorized to delete that task.')
        return redirect('to_do_overs:dashboard')
