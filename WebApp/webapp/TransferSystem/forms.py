from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms  import UserCreationForm
from django.core.exceptions import NON_FIELD_ERRORS
from .models import Article, Transfer

import re

class Registration_Form(UserCreationForm):
    first_name = forms.CharField(
        required = True
    )
    last_name = forms.CharField(
        required = True
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'password1',
            'password2'
        )

    def save(self, commit = True):
        user = super(Registration_Form, self).save(commit = False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user

class Article_Creation_Form(forms.ModelForm):
    id = forms.CharField(
        required = True,
        max_length = 10,
        min_length = 8,
    )
    name = forms.CharField(
        required = True
    )
    price = forms.DecimalField(
        required = True
    )
    url = forms.URLField(
        required = False
    )

    def clean_id(self):
        data  = self.cleaned_data.get('id','')
        if not data:
            raise forms.ValidationError("Enter a valid article number")
        
        if data.isdigit() and len(data) == 8:
            print(data)
            return data
        else:
            data = "".join(re.findall(r"[\d']+", data))
            if data.isdigit() and len(data) == 8:
                return data
            else:
                raise forms.ValidationError("Invalid article number")
                
    class Meta:
        model = Article
        fields = (
            'id',
            'name',
            'description',
            'price',
            'url'
        )

class Transfer_Form(forms.ModelForm):
    # user =  forms.CharField(
    #     required = True
    # )
    # article = forms.CharField(
    #     required = True
    # )
    class Meta:
        model = Transfer
        fields = (
            'article',
            'user',
            'location',
            'quantity',
        )