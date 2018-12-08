# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.


class Users(models.Model):
    user_id = models.CharField(max_length=255)
    api_key = models.CharField(max_length=255)
    username = models.CharField(max_length=255)

