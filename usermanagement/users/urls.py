from rest_framework.routers import DefaultRouter
from .views import UsersListView, UserRegView, UserProfileView
from django.urls import path, include
router = DefaultRouter()
router.register('users', UsersListView, basename= 'users')
router.register('profile', UserProfileView, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegView.as_view(), name='user-register'),
]