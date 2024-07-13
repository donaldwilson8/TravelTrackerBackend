from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, TripViewSet

router = DefaultRouter()
router.register(r'user_profiles', UserProfileViewSet)
router.register(r'trips', TripViewSet)

urlpatterns = [
    path('', include(router.urls)),
]