# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User

from django.contrib.sessions.models import Session

from django.utils import timezone

from django.shortcuts import render, redirect, HttpResponse

from django.contrib.auth.decorators import login_required

from django.core.exceptions import ValidationError

from .models import Article, Log, Transfer
from .forms import RegistrationForm


# Create your views here.


@login_required
def Home(request):
    # http://stackoverflow.com/questions/2723052/how-to-get-the-list-of-the-authenticated-users
    active_users_count = Session.objects.filter(expire_date__gte = timezone.now()).count()
    saved_articles_count = Article.objects.count()
    transfered_articles_count = Log.objects.filter(status = False).count()
 
    content = {
        "page" : "Home",
        "active_users_count" : active_users_count, 
        "transfered_articles_count" : transfered_articles_count,
        "saved_articles_count" : saved_articles_count
    }
    
    return render(request,"TransferContents/home.html", content)

@login_required
def Registered_Users(request):
    response = False
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save() 
            response = ("alert-success","<p><strong>Success!</strong> User is succesfully created</p>")
        else:
            response = ("alert-danger", form.errors)

    users = User.objects.all()
    form =  RegistrationForm()
    content = {
        'form' : form,
       'users' : users,
       'response' : response
    }
    return render(request,"TransferContents/registered-users.html",content)



@login_required
def Transfered_Articles(request):
    return HttpResponse("Transfered_Articles")

@login_required
def Saved_Articles(request):
    return HttpResponse("Saved_Articles")