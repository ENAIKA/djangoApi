# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import datetime
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser
from django.db.models.signals import post_save 
from django.dispatch import receiver
from django.urls import reverse
from django.core.validators import RegexValidator

# Create your models here.
class UserProfile(models.Model):
    photo=models.ImageField(upload_to = 'profile/', blank=True)
    bio=models.TextField()
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name="profile")
    created=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User) 
def create_user_profile(sender, instance, created, **kwargs):
     if created:
         UserProfile.objects.create(user=instance)
@receiver(post_save, sender=User) 
def save_user_profile(sender, instance, **kwargs):
     instance.profile.save()



class Project(models.Model):
    author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    url=models.URLField(max_length = 200)
    description=models.TextField()
    like=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name="liked" )
    project_name=models.CharField(max_length=150)
    image=models.ImageField(upload_to = 'projects/', blank=True)
    posted=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name

    @classmethod
    def search_by_name(cls,search_term):
        projects = cls.objects.filter(name__icontains=search_term)
        return projects


class Rates(models.Model):
    project=models.ForeignKey(Project, on_delete=models.CASCADE)
    jury=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    design=models.IntegerField( validators=[RegexValidator(r'^\d{1,10}$')])
    content=models.IntegerField( validators=[RegexValidator(r'^\d{1,10}$')])
    usability=models.IntegerField( validators=[RegexValidator(r'^\d{1,10}$')])


class NewsLetterRecipients(models.Model):
    name=models.CharField(max_length=40) 
    email= models.EmailField()