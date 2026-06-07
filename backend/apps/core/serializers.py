from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from . import models

class CustomTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        
        token['username'] = user.username
        token['role'] = user.role
        
        return token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            'password': {'write_only': True }
        }
        
    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)