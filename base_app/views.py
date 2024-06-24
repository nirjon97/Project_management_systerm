from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from .models import users, projects, project_members, tasks, comments
from .serializers import UserSerializer, UserRegisterSerializer, UserLoginSerializer, ProjectSerializer, ProjectMemberSerializer, TaskSerializer, CommentSerializer
from django.contrib.auth import authenticate

class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data['email']
            password = serializer.data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = users.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = projects.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


    @action(detail=True, methods=['get'], url_path='tasks', url_name='tasks')
    def list_tasks(self, request, pk=None):
        project = self.get_object()
        tasks_list = tasks.objects.filter(project=project)
        serializer = TaskSerializer(tasks_list, many=True)
        return Response(serializer.data)
    


class ProjectMemberViewSet(viewsets.ModelViewSet):
    queryset = project_members.objects.all()
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsAuthenticated]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = tasks.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]


    def create(self, request, project_pk=None):
        project = projects.objects.get(pk=project_pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(project=project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'], url_path='tasks', url_name='tasks')
    def list_tasks(self, request, pk=None):
        project = self.get_object()
        tasks_list = tasks.objects.filter(project=project)
        serializer = TaskSerializer(tasks_list, many=True)
        return Response(serializer.data)
    

    @action(detail=True, methods=['get', 'post'])
    def comments(self, request, pk=None):
        task = self.get_object()
        if request.method == 'GET':
            task_comments = comments.objects.filter(task=task)
            serializer = CommentSerializer(task_comments, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(task=task, user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CommentViewSet(viewsets.ModelViewSet):
    queryset = comments.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

