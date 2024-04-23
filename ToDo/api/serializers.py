from rest_framework.serializers import ModelSerializer
from .models import CustomUser


class UserSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'photo']

    def update(self, instance, validate_data):
        return super().update(instance, validate_data)
    
    
    def save(self, **kwargs):
        return super().save(**kwargs)
