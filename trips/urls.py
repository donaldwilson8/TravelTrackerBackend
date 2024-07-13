from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, TripViewSet, UserVisitedCountries

router = DefaultRouter()
router.register(r'user_profiles', UserProfileViewSet)
router.register(r'trips', TripViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('visited-countries/', UserVisitedCountries.as_view(), name='user-visited-countries'),
]