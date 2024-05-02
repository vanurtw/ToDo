from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer, Serializer
from .models import CustomUser, Task
from rest_framework.validators import ValidationError
from rest_framework import serializers


class UserResetPasswordSerializer(Serializer):
    current_password = serializers.CharField()
    new_password = serializers.CharField()
    repeat_new_password = serializers.CharField()

    def validate(self, data):
        validate_password(data.get('current_password'))
        validate_password(data.get('new_password'))
        validate_password(data.get('repeat_new_password'))
        if data.get('new_password') != data.get('repeat_new_password'):
            raise ValidationError({'detail': 'Пароли не совпадают'})
        if data.get('current_password') == data.get('new_password'):
            raise ValidationError({'detail': 'Вы не можете заменить пароль на тот же самый'})
        return data


class TaskSerializer(ModelSerializer):
    # data_completed = serializers.DateTimeField(format = '%Y-%m-%d')
    # data_create = serializers.DateTimeField(format = '%Y-%m-%d', required=False)
    class Meta: 
        model = Task
        fields = ['id', 'user', 'title', 'description', 'color_code', 'data_completed', 'completed', 'tag']
        read_only_fields = ['id', 'data_create', 'user']

    def update(self, instance, validated_data):
        instance.__dict__.update(validated_data)
        instance.save()
        return instance
    
    def save(self, **kwargs):
        return super().save(**kwargs)



class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}
        read_only_fields = ['id']

    def validate_password(self, data):
        validate_password(data)
        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
