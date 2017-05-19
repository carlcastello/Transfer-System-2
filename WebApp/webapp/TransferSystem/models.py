# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Article(models.Model):
    id = models.IntegerField(
        default = 0,
        primary_key = True,
    )
    name = models.CharField(
        max_length = 100
    )
    description = models.CharField(
        max_length = 200
    )
    price = models.DecimalField(
        max_digits = 10,
        decimal_places = 2
    )
    url = models.CharField(
        max_length = 200
    )

class User_Profile(models.Model):
    user = models.OneToOneField(
        User
    )
    first_name = models.CharField(
        max_length = 100
    )
    last_name = models.CharField(
        max_length = 100
    )

class Transfer(models.Model):
    LOCATION = (
        ('L1', 'Living Room'),
        ('L2', 'Kids'),
        ('L3', 'Bedrooms'),
        ('L4', 'Office Space'),
        ('L5', 'Kitchen'),
    )
    article = models.ForeignKey(
        Article
    )
    user = models.ForeignKey(
        User
    )
    quantity = models.IntegerField(
        default = 0
    )
    location = models.CharField(
        max_length = 2,
        choices = LOCATION,
    )
    date = models.DateTimeField(
        'date-time transfered'
    )
    
class Log(models.Model):
    transfer = models.ForeignKey(
        Transfer
    )
    status = models.BooleanField(
        default = False
    )

