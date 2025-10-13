from rest_framework.routers import DefaultRouter
from .views import UsersListView, UserRegView, UserProfileView, active,UserLoginView, UserLogOutView
from django.urls import path, include
router = DefaultRouter()
router.register('users', UsersListView, basename= 'users')
router.register('profile', UserProfileView, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegView.as_view(), name='register'),
    path("confirm/<uidb64>/<token>/", active, name="user-activate"),
    path("login/",UserLoginView.as_view(), name="login"),
    path("logout/",UserLogOutView.as_view(), name="logout"),
]