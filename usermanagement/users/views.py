from django.shortcuts import render
from rest_framework.views import APIView
from .serializer import UserRegSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class UserProfileView(viewsets.ModelViewSet):
    serializer_class = UserRegSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class UserRegView(APIView):
    queryset = User.objects.all()
    serializer_class = UserRegSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UsersListView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegSerializer