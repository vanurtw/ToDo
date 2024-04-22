from django.urls import path, include, re_path
import djoser.urls
import rest_framework.authentication

urlpatterns = [
    # re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

]
