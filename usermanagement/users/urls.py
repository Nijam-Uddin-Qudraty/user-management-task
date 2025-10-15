from rest_framework.routers import DefaultRouter
from .views import DeleteUserView, UsersListView, UserRegView, UserProfileView, UserLoginView, UserLogoutView, UserPasswordChangeView, active
from django.urls import path, include
router = DefaultRouter()
router.register('users', UsersListView, basename= 'users')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', UserRegView.as_view(), name='register'),
    path("confirm/<uidb64>/<token>/", active, name="user-activate"),
    path("login/",UserLoginView.as_view(), name="login"),
    path("logout/",UserLogoutView.as_view(), name="logout"),
     path("delete-profile/", DeleteUserView.as_view(), name="delete-profile"),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('change-password/', UserPasswordChangeView.as_view(), name='change-password'),
]