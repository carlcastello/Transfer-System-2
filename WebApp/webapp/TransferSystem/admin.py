# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Article, Log, Transfer, User_Profile

# Register your models here.
admin.site.register(Article)
admin.site.register(Log)
admin.site.register(Transfer)
admin.site.register(User_Profile)