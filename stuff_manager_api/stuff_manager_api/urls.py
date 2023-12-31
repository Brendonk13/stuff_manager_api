"""
URL configuration for stuff_manager_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# from rest_framework import routers
# from stuff_manager_api.stuff_manager import views
# from stuff_manager import views
from .api import api
# from stuff_manager_api.stuff_manager.router import api_router as therouter
from stuff_manager.router import api_router

api.add_router("/", api_router)
# for route, router in api._routers:
#     print(dir(router))
# print(api._routers)

# router = routers.DefaultRouter()
# router.register(r"users", views.UserViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
