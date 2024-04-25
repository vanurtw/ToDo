from rest_framework.generics import GenericAPIView
from .serializers import UserSerializer, UserResetPasswordSerializer, TaskSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.views import APIView


# Create your views here


class UsersAPIView(GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserSerializer(data=request.data, instance=request.user)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


class UserResetPasswordAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        user = request.user
        serializer = UserResetPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        if user.check_password(data.get('current_password')):
            user.set_password(data.get('new_password'))
            user.save()
            return Response({'detail': 'Пароль изменен'})
        return Response({'detail': 'Пароль не совпадает с текущим'})


class TaskAPIView(GenericAPIView):
    def get(self, request):
        data = request.user.user_tasks.all()
        serializer = TaskSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = TaskSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data)
