from rest_framework import serializers
from .models import UserProfile, Trip

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'country', 'date_visited']
        read_only_fields = ['id', 'user']