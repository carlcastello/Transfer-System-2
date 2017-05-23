import operator,datetime

from django.contrib.auth.models import User

from django.contrib.sessions.models import Session

from django.urls import reverse_lazy

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.db.models import Q

from .models import Article, Transfer, Log
from .forms import Registration_Form, Article_Creation_Form, Transfer_Form

from django.views.generic import ListView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import ArticleSerializer, TransferSerializer

# This is the Home View Class
@method_decorator(login_required, name='dispatch')
class Home_View(TemplateView):
    template_name = "TransferContents/home.html"

    def get_context_data(self, **kwargs):
        context = super(Home_View, self).get_context_data(**kwargs)

        # http://stackoverflow.com/questions/2723052/how-to-get-the-list-of-the-authenticated-users
        # active_users_count = Session.objects.filter(expire_date__gte = timezone.now()).count()
        # Counts how many registered user 
        active_users_count = User.objects.count()
        # Counts How many saved articles
        saved_articles_count = Article.objects.count()
        # Counts transfered unconfirmed article
        transfered_articles_count = Transfer.objects.count()

        # Pass in more content to be displayed in the home view
        context['page'] = 'Home'
        context['active_users_count'] = active_users_count
        context['saved_articles_count'] = saved_articles_count
        context['transfered_articles_count'] = transfered_articles_count 
        return context

# Displayes all registered user in the system
@method_decorator(login_required, name='dispatch')
class Registered_Users(TemplateView):
    template_name = "TransferContents/registered-users.html"

    def get_context_data(self, **kwargs):
        context = super(Registered_Users, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        context['curr_user'] = self.request.user
        return context

# Register User Create Form
@method_decorator(login_required, name='dispatch')
class Register_User(CreateView):
    model = User
    template_name = "TransferContents/creation-form.html"
    form_class = Registration_Form

    # Displaying messages and information to re-use the html page
    # This allows me to customize how I output the message
    content = {
        'title' : 'User Registration Form',
        'type' : 'user_register',
        'response' : None
    }

    # Displays an error message if the form is invalid
    def form_invalid(self, form):
        self.content['response'] = ("alert-danger", form.errors)
        return redirect('TransferSystem:register-user')

    # Displays a success message if the form is valid
    def form_valid(self,form):
        form.save()
        # Creates a Log 
        user = self.request.user
        username2 = form.cleaned_data["username"]
        Log.objects.create(
            user = user,
            comment = "User " + user.username + " created user " + username2 +"."
        )
        self.content['response'] = ("alert-success","<p><strong>Success!</strong> User is succesfully created</p>")
        return redirect('TransferSystem:register-user')

    def get_context_data(self, **kwargs):
        context = super(Register_User, self).get_context_data(**kwargs)
        for key in self.content:
            context[key] = self.content[key]
        # Clear the content once transfered to context
        self.content['response'] = None
        return context

@method_decorator(login_required, name='dispatch')
class Delete_User(DeleteView):
    model = User
    template_name = "TransferContents/delete-form.html"
    success_url = reverse_lazy('TransferSystem:registered-users')

    content = {
        'type' : 'user_deletion_form',
        'title' : 'User Deletion Form',
        'response' : None
    }

    def form_invalid(self, form):
        self.content['response'] = ("alert-danger", form.errors)
        return redirect('TransferSystem:delete-user')

    def get_context_data(self, **kwargs):
        context = super(Delete_User, self).get_context_data(**kwargs)
        for key in self.content:
            context[key] = self.content[key]
        self.content['response'] = None
        return context

@method_decorator(login_required, name='dispatch')
class Transfered_Articles(ListView):
    template_name = "TransferContents/transfered-articles.html"
    
    def get_queryset(self):
        results = Transfer.objects.all()
        return results

    def get_context_data(self, **kwargs):
        context = super(Transfered_Articles, self).get_context_data(**kwargs) 
        context['results'] = self.get_queryset()
        return context

@method_decorator(login_required, name='dispatch')
class Transfer_Article(CreateView):
    model = Transfer
    # response = None
    template_name = "TransferContents/transfer-article-form.html"
    form_class = Transfer_Form
    article = None 

    content = { 
        'response' : None
    }

    def form_invalid(self, form):
        self.content['response'] = ("alert-danger", form.errors)
        return redirect('TransferSystem:transfer-article')

    def form_valid(self,form):
        form.save()
        self.content['response'] = ("alert-success","<p><strong>Success!</strong> Article is succesfully transfered!</p>")
        return redirect('TransferSystem:transfer-article')

    def get_object(self):
        query = self.request.GET.get('search-form')
        if query:
            result = Article.objects.filter(id = query)
            if not result:
                self.content['response'] = ("alert-danger","<p><strong>Not Found!</strong> Article Number does not exist!</p>")
                return None
            return result[0]
 
    def get_initial(self): 
        initial = super(Transfer_Article, self).get_initial()
        self.article = self.get_object()
        initial['user'] = self.request.user
        initial['article'] = self.article
        return initial

    def get_context_data(self, **kwargs):
        context = super(Transfer_Article, self).get_context_data(**kwargs)
        objects = self.get_object()
        context['object'] = self.article
        context['response'] = self.content['response']
        self.content['response'] = None
        return context

@method_decorator(login_required, name='dispatch')
class Confirm_Article(TemplateView):
    template_name = "TransferContents/confirm-article-form.html"
    success_url = reverse_lazy('TransferSystem:transfered-articles')

    def get_queryset(self):
        article_ids = self.kwargs['article_ids'][1:].split('&')
        results = []
        for article_id in article_ids:
            results.append(Transfer.objects.filter(id = article_id)[0])
        return tuple(results)

    def post(self, request, article_ids):
        article_ids = article_ids[1:].split('&')
        for article_id in article_ids:
            Transfer.objects.filter(id = article_id).delete()
        return redirect(reverse_lazy('TransferSystem:transfered-articles'))

    def get_context_data(self, **kwargs):
        context = super(Confirm_Article, self).get_context_data(**kwargs)
        context['transfers'] = self.get_queryset();
        return context

@method_decorator(login_required, name='dispatch')
class Saved_Articles(ListView):
    template_name = "TransferContents/saved-articles.html"
    model = Article
    # form_class = Article_Search_Form
    
    def get_queryset(self):
        query = self.request.GET.get('search-form')
        if query:
            results = Article.objects.filter(
                Q(id__icontains = query) | Q(name__icontains = query) | Q(description__icontains = query))
            return results 
    
    def get_context_data(self, **kwargs):
        context = super(Saved_Articles, self).get_context_data(**kwargs)
        context['results'] = self.get_queryset()
        return context


@method_decorator(login_required, name='dispatch')
class Save_Article(CreateView):
    model = Article
    template_name = "TransferContents/creation-form.html"
    form_class = Article_Creation_Form

    content = {
        'title' : 'Article Creation Form',
        'type' : 'save_article',
        'response' : None
    }

    def form_invalid(self, form):
        self.content['response'] = ("alert-danger", form.errors)
        return redirect('TransferSystem:save-article')

    def form_valid(self,form):
        form.save()
        self.content['response'] = ("alert-success","<p><strong>Success!</strong> Article is succesfully created</p>")
        return redirect('TransferSystem:save-article')

    def get_context_data(self, **kwargs):
        context = super(Save_Article, self).get_context_data(**kwargs)
        for key in self.content:
            context[key] = self.content[key]

        self.content['response'] = None
        return context

@method_decorator(login_required, name='dispatch')
class Modify_Article(CreateView):
    model = Article
    template_name = "TransferContents/creation-form.html"
    form_class = Article_Creation_Form

    content = {
        'title' : 'Article Creation Form',
        'response' : None
    }

    def form_invalid(self, form):
        self.content['response'] = ("alert-danger", form.errors)
        return redirect('TransferSystem:save-article')

    def form_valid(self,form):
        form.save()
        self.content['response'] = ("alert-success","<p><strong>Success!</strong> Article is succesfully created</p>")
        return redirect('TransferSystem:save-article')

    def get_context_data(self, **kwargs):
        context = super(Modify_Article, self).get_context_data(**kwargs)
        for key in self.content:
            context[key] = self.content[key]

        self.content['response'] = None
        return context


@method_decorator(login_required, name='dispatch')
class Delete_Article(DeleteView):
    model = Article
    template_name = "TransferContents/delete-form.html"
    success_url = reverse_lazy('TransferSystem:saved-articles')

    content = {
        'type' : 'article_deletion_form',
        'title' : 'Article Deletion Form',
        'response' : None
    }

    def get_object(self):
        article_id = self.kwargs['article_id']
        return get_object_or_404(Article, id = article_id)
        
    def get_context_data(self, **kwargs):
        # print(kwargs['article_id'])
        context = super(Delete_Article, self).get_context_data(**kwargs)
        
        for key in self.content:
            context[key] = self.content[key]
        self.content['response'] = None

        return context


# This is the restAPI of the app. 
# This will allow an android app to communicate to the database
class Process_Transfer(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = TransferSerializer


    def get_object(self,article_id):
        return  get_object_or_404(Article, id = article_id)

    def get(self,request,article_id):
        user = request.user
        auth = request.auth
        print(auth)
        article = self.get_object(article_id)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def post(self,request,article_id):
        user = request.user
        auth = request.auth
        article = self.get_object(article_id)
        context = {
            'article' : article,
            'user' : user
        }
        serializer = TransferSerializer(data = request.data, context = context )
        if serializer.is_valid():
            serializer.create()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

