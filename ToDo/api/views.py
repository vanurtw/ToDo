from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.


class TestAPIView(APIView):
    def get(self, request):
        return Response({'status': 'ok'}, status=200)
