from django.urls import path, include, re_path
import djoser.urls
import rest_framework.authentication
from .views import UsersAPIView, UserResetPasswordAPIView, TaskAPIView, UserRegisterAPIView, TaskDetailAPIView

urlpatterns = [
    path('users/register/', UserRegisterAPIView.as_view()),
    path('users/me/', UsersAPIView.as_view()),
    path('users/me/reset-password/', UserResetPasswordAPIView.as_view()),
    path('tasks/', TaskAPIView.as_view()),
    path('tasks/<int:id>/', TaskDetailAPIView.as_view()),
    # re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]
