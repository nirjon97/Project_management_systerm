from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ProjectViewSet, ProjectMemberViewSet, TaskViewSet, CommentViewSet, UserRegisterView, UserLoginView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'project-members', ProjectMemberViewSet)
router.register(r'tasks', TaskViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/users/register/', UserRegisterView.as_view(), name='user_register'),
    path('api/users/login/', UserLoginView.as_view(), name='user_login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


