from django import forms
from .models import Project, Rates, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class WelcomeForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email','username']

class SignUpForm(UserCreationForm):
  class Meta:
    model=UserProfile
    fields=['username','first_name','last_name','email', 'password1','password2','photo', 'bio']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['description','url','project_name','image']

class CommentForm(forms.ModelForm):
    class Meta:
        model=Rates
        fields=['usability','design','content']

    
        