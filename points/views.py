from __future__ import unicode_literals
from .email import send_welcome_email
import datetime as dt
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import  Project,UserProfile,NewsLetterRecipients,Rates
from django.http import JsonResponse
from rest_framework import status
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http  import HttpResponse,Http404
from .serializers import UserSerializer, ProjectSerializer
from .permissions import IsAdminOrReadOnly
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.views.generic import TemplateView,RedirectView
from .forms import RegisterForm,CommentForm,WelcomeForm,ProjectForm,SignUpForm
#Create your views here........
class UserList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        all_users =UserProfile.objects.all()       
        serializers = UserSerializer(all_users, many=True)
        
        return Response(serializers.data)
    
    def post(self, request, format=None):
          serializers = UserSerializer(data=request.data)
          if serializers.is_valid():
              serializers.save()
              return Response(serializers.data, status=status.HTTP_201_CREATED)
          return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ProjectList(APIView):
    
    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)
    permission_classes = (IsAdminOrReadOnly,)
    def post(self, request, format=None):
          serializers = ProjectSerializer(data=request.data)
          if serializers.is_valid():
              serializers.save()
              return Response(serializers.data, status=status.HTTP_201_CREATED)
          return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_user(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        user = self.get_user(pk)
        serializers =UserSerializer(user)
        return Response(serializers.data)

    def post(self, request, format=None):
          serializers = UserSerializer(data=request.data)
          if serializers.is_valid():
              serializers.save()
              return Response(serializers.data, status=status.HTTP_201_CREATED)
          return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        user= self.get_user(pk)
        serializers = UserSerializer(user, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_user(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProjectDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get_project(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        project = self.get_project(pk)
        serializers = ProjectSerializer(project)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        project = self.get_project(pk)
        serializers = ProjectSerializer(project, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        project = self.get_project(pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

def welcomeletter(request):
    name = request.POST.get('username')
    email = request.POST.get('email')

    recipient = NewsLetterRecipients(name=name, email=email)
    recipient.save()
    send_welcome_email(name, email)
    data = {'success': 'You have been successfully added to mailing list'}
    return JsonResponse(data)

def welcome(request):
    
    return render(request, 'home.html')


def registerPage(request):
    
    if request.method=="POST":
        form=RegisterForm(request.POST)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('login')
       
    else: 
        form=RegisterForm()
       
    
    return render(request, 'django_registration/registration_form.html', {'form':form})

def login_view(request):
    
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        
        if user is not None:

            login(request, user)

            return redirect('allprojects')
        else:
            return HttpResponse("invalid login credentials")
    
    return render(request, 'django_registration/login.html')

@login_required      
def logout_view(request):
    logout(request)
    return redirect('login')
@login_required 
def search_results(request):

    if 'project' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        searched_projects =Project.search_by_name(search_term)
        message = f"{search_term}"

        return render(request, 'all/search.html',{"message":message,"projects": searched_projects})

    else:
        message = "You haven't searched for any term"
        return render(request, 'all/search.html',{"message":message})


@login_required  
def increment_counter(request,project_id):
    if not request.user.is_authenticated:
        return redirect('django_registration/login.html')
    else:
        if request.method=="POST":
            if 'like' in request.POST:
                liked = get_object_or_404(Project, id=request.POST.get('project_id'))
                liked.like.add(request.user)
                
            return HttpResponseRedirect(reverse("liked", args=[str(project_id)]) )#check this too


@login_required  
def project(request,project_id):
    try:
        project = Project.objects.get(id =project_id)
    except DoesNotExist:
        raise Http404()
    return render(request,"all/project.html", {"project":project})

@login_required  
def allprojects(request):
    projects=Project.objects.all()
    return render(request, 'allprojects.html', {"projects":projects})

@login_required
def uploadproject(request,user_id):
    
    if request.method=="post":
        form=ProjectForm(request.POST, request.FILES,instance=request.user)
        if form.is_valid():
            instance=form.save(commit=False)
            values=form.cleaned_data()
            instance.save()
            values.save()
            print(values)
            print(instance)
            # form.save(commit=False)
            # project_name = form.cleaned_data['project_name']
            # description = form.cleaned_data['description']
            # url = form.cleaned_data['url']
            # image= form.cleaned_data['image']
            # user=request.user
            # project=Project(project_name=project_name,url=url, description=description,image=image,author=user)
            # project.save()
            
            # return HttpResponseRedirect('allprojects')
            return redirect('allprojects.html')
    else:
        form = ProjectForm()
    return render(request, 'uploadproject.html', {"form":form})


@login_required
def userprofile(request, user_id):
    if not request.user.is_authenticated:
        return redirect('django_registration/login.html')
    else:
        user=User.objects.get(id=user_id) 
              
        return render(request,'profile.html',{'user':user})
@login_required
def userprojects(request, user_id):
    if not request.user.is_authenticated:
        return redirect('django_registration/login.html')
    else:
        user=request.user
        projects= Project.objects.filter( author=user)       
        return render(request,'myprojects.html',{'projects':projects})
@login_required
def updateprofile(request,user_id):
    r_form=SignUpForm(request.POST, request.FILES,instance=request.user.profile)
    if request.method=='POST':
        if r_form.is_valid():
            bio=request.POST.get('bio')
            photo=request.POST.get('photo')
            new_user=UserProfile(bio=bio,photo=photo, user=request.user)
            new_user.save()            
            messages.success(request, ('Your profile was successfully updated!'))
            return HttpResponseRedirect("userprofile", args=[str(user_id)]) 
        else:
            messages.error(request, ('Please correct the error below.'))

    else:
        r_form=SignUpForm()

    return render(request, 'django_registration/update_form.html', {'r_form':r_form})
@login_required
def juryverdict(request, project_id):
    form=CommentForm(request.POST)
    if request.method=='POST':
        if form.is_valid():
            usability=request.POST.get('usability')
            content=request.POST.get('content')
            design=request.POST.get('design')
            project=Project.objects.filter(author_id=request.user)
            
            new_verdict=Rates(usability=usability,content=content,design=design, jury=request.user, project=project_id.Project.project)
            new_verdict.save()
            messages.success(request, ('Your verdict was successfully uploaded!'))

            return HttpResponseRedirect(reverse("projects", args=[str(project_id)] ))
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        form=CommentForm()

    return render(request, 'django_registration/comment_form.html', {'form':form})
