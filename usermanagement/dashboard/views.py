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


from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from .serializers import UserSerializer


class UserPagination(PageNumberPagination):
    page_size = 10  # default per page
    page_size_query_param = 'page_size'
    max_page_size = 100


class DashboardView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    pagination_class = UserPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['username', 'email', 'is_staff', 'is_active']

    def list(self, request, *args, **kwargs):
        """
        Override list() to include a global user count in the response.
        """
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)

        total_users = User.objects.count()
        total_active = User.objects.filter(is_active=True).count()
        total_staff = User.objects.filter(is_staff=True).count()

        response = self.get_paginated_response(serializer.data)
        response.data['total_users'] = total_users
        response.data['total_active'] = total_active
        response.data['total_staff'] = total_staff
        return response