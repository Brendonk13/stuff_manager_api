# from django.shortcuts import render
# from django.contrib.auth.models import User
from .models import User
# from rest_framework import permissions, serializers, viewsets
# from stuff_manager_api.stuff_manager_api.api import api

# from ninja.security import HttpBearer
# from ninja import NinjaAPI
# api = NinjaAPI()

from ninja import Router
from .authentication.clerk import ClerkBearerAuth

router = Router(auth=ClerkBearerAuth())

@router.get("/hello")
# def add(request, a: int, b: int):
    # return {"result": a + b}
def hello(request):
    return {"result": "hello"}



# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = "__all__"


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """

#     queryset = User.objects.all().order_by("-created")
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]
