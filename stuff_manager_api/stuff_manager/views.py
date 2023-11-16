# from django.shortcuts import render
# from django.contrib.auth.models import User
from .models import User
from rest_framework import permissions, serializers, viewsets


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-created")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
