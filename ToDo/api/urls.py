from django.urls import path, include, re_path
import djoser.urls
import rest_framework.authentication
from .views import UsersAPIView, UserResetPasswordAPIView

urlpatterns = [
    path('users/me/', UsersAPIView.as_view()),
    path('users/me/reset-password/', UserResetPasswordAPIView.as_view()),
    # path('task/', ),
    # re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

]
