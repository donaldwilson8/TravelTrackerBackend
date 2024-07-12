from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, TripViewSet, CountryList, UserVisitedCountries, SignupView

router = DefaultRouter()
router.register(r'user_profiles', UserProfileViewSet)
router.register(r'trips', TripViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('countries/', CountryList.as_view(), name='country-list'),
    path('visited-countries/', UserVisitedCountries.as_view(), name='user-visited-countries'),
]