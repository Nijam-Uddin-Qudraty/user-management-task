from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView

from rest_framework import viewsets, pagination
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend

class UserPagination(pagination.PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class DashboardView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = UserPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'email', 'is_staff', 'is_active']