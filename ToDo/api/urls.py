from django.urls import path, include, re_path
import rest_framework.authentication
from rest_framework.routers import SimpleRouter
from .views import UsersAPIView, UserResetPasswordAPIView, TaskAPIView, TaskDetailAPIView, TaskTagAPIView

urlpatterns = [
    path('users/', UsersAPIView.as_view(), name='users'),
    path('users/reset-password/', UserResetPasswordAPIView.as_view()),
    path('tasks/', TaskAPIView.as_view(), name='tasks'),
    path('tasks-tag/', TaskTagAPIView.as_view()),
    path('tasks/<int:id>/', TaskDetailAPIView.as_view(), name='task_detail'),
    # re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),


]
