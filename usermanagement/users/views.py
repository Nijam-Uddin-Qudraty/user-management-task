from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework import generics
from usermanagement import settings
from .serializer import UserRegSerializer, UserLoginSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
# mail related
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives,send_mail
# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .serializer import UserRegSerializer, UserProfileSerializer

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializer import UserProfileSerializer



from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User

class DeleteUserView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        password = request.data.get("password")

        if not password:
            return Response(
                {"password": "Password is required to delete the account."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(password):
            return Response(
                {"password": "Incorrect password."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.delete()
        return Response(
            {"detail": "Account deleted successfully."},
            status=status.HTTP_200_OK
        )



class UserPasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not user.check_password(current_password):
            return Response({"error": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"error": "New passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"success": "Password changed successfully."}, status=status.HTTP_200_OK)

class UserProfileView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect("login")


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(username=username, password=password)

            if user is not None:
                if not user.is_active:
                    return Response({"error": "Account not activated. Check your email."},
                                    status=status.HTTP_401_UNAUTHORIZED)
                token, created = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({"token": token.key, "user": user.username}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def active(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # redirect to frontend login page
        return redirect(f"{settings.FRONTEND_URL}/login")




class UserRegView(APIView):
    serializer_class = UserRegSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            confirm_link = f"http://127.0.0.1:8000/api/confirm/{uid}/{token}/"

            email_subject = "Confirm your email"
            email_body = render_to_string("confirm_mail.html", {
                "username": user.username,
                "confirm_link": confirm_link
            })

            email = EmailMultiAlternatives(email_subject, email_body, to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            return Response("Check your mail for confirmation link", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsersListView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegSerializer


