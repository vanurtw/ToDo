from rest_framework.generics import GenericAPIView, get_object_or_404
from .serializers import UserSerializer, UserResetPasswordSerializer, TaskSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from datetime import datetime
from .models import Task
from rest_framework.authtoken.models import Token


# Create your views here


class UsersAPIView(GenericAPIView):
    serializer_class = UserSerializer

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'auth_token': token.key}, status=status.HTTP_201_CREATED)

    def patch(self, request):
        serializer = UserSerializer(data=request.data, instance=request.user, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def get_permissions(self):
        if self.request.method == 'POST':
            return (permissions.AllowAny(),)
        return (permissions.IsAuthenticated(),)


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
        return Response({'detail': 'Пароль не совпадает с текущим'}, status=status.HTTP_400_BAD_REQUEST)


class TaskAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        print(1)
        date_get = request.GET.get('date')
        if date_get:
            date = datetime.strptime(date_get, '%Y/%m/%d')
            data = request.user.user_tasks.filter(data_completed=date)
        else:
            data = request.user.user_tasks.all()
        print(data)
        serializer = TaskSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = TaskSerializer(data=data)
        serializer.is_valid()
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskDetailAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, id):
        data = request.data
        task = get_object_or_404(Task, id=id)
        serializer = TaskSerializer(data=data, instance=task, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        task = get_object_or_404(Task, id=id)
        if task.user != request.user:
            return Response({'detail': 'Это не ваша задача'}, status=status.HTTP_403_FORBIDDEN)
        task.delete()
        return Response({'detail': 'задача удалена'}, status=status.HTTP_200_OK)


class UserRegisterAPIView(GenericAPIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            print(2)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
