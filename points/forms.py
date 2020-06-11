from django import forms
from .models import Project, Rates, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class WelcomeForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['email','username']
class SignUpForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['photo', 'bio']

class RegisterForm(UserCreationForm):
  class Meta:
    model=User
    fields=['username','first_name','last_name','email', 'password1','password2']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['description','url','project_name','image']

class CommentForm(forms.ModelForm):
    class Meta:
        model=Rates
        fields=['usability','design','content']

    
        