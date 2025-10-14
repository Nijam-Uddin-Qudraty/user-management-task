from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import DashboardView

router = DefaultRouter()
router.register('users', DashboardView, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]