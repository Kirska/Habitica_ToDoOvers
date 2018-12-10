# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.


class Users(models.Model):
    user_id = models.CharField(max_length=255, unique=True)
    api_key = models.CharField(max_length=255)
    username = models.CharField(max_length=255)


class Tasks(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    notes = models.TextField()
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

