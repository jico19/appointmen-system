from rest_framework import viewsets
from . import serializers
from . import models


class UserViewSets(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer