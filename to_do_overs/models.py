# -*- coding: utf-8 -*-
"""Django Models - Habitica To Do Over tool
"""
from __future__ import unicode_literals
from django.db import models


class Users(models.Model):
    """Model for the users of the tool.

    Fields:
        username (str): Username from Habitica.
        user_id (str): User ID from Habitica.
        api_key (str): API token from Habitica.
    """
    user_id = models.CharField(max_length=255, unique=True)
    api_key = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

    def __str__(self):
        return str(self.pk) + ':' + str(self.user_id) + ':' + str(self.username)


class Tasks(models.Model):
    """Model for the tasks created by users.

    Fields:
        task_id (str): Task ID from Habitica.
        name (str): Name/title of task.
        notes (str): The notes/description of the task.
        priority (str): Difficulty of task.
        days (int): Number of days until task expires from the creation.
        owner (int/Foreign Key): The owner from the users model.
    """
    task_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    TRIVIAL = '0.1'
    EASY = '1.0'
    MEDIUM = '1.5'
    HARD = '2'
    PRIORITY_CHOICES = (
        (TRIVIAL, 'Trivial'),
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
    )
    priority = models.CharField(max_length=3, choices=PRIORITY_CHOICES, blank=False, default=EASY)
    days = models.PositiveIntegerField(default=0)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk) + ':' + str(self.name) + ':' + str(self.task_id)

