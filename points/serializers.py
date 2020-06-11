from rest_framework import serializers
from .models import Project, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id','user', 'bio','photo')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=Project
        fields=('id','project_name','description','author','url')