from rest_framework import serializers
from .models import AllProjects, AllUsers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AllUsers
        fields = ('id','username', 'bio', 'priojects','photo')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=AllProjects
        fields=('id','name','description','author','url')