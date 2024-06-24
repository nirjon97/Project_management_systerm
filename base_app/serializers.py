from rest_framework import serializers
from .models import users, projects, project_members, tasks, comments

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = users
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = users(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = projects
        fields = '__all__'

class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = project_members
        fields = '__all__'

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = tasks
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = comments
        fields = '__all__'