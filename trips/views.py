from django.shortcuts import render
from rest_framework import viewsets, permissions, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile, Trip
from .serializers import UserProfileSerializer, TripSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data)
    

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_trips(self, request):
        user_trips = Trip.objects.filter(user=request.user)
        serializer = self.get_serializer(user_trips, many=True)
        return Response(serializer.data)
    

class UserVisitedCountries(APIView):
    permission_classes = [permissions.IsAuthenticated]
  
    def get(self, request):
        print(f"User {request.user} is trying to get their visited countries")
        trips = Trip.objects.filter(user=request.user).values_list('country', flat=True).distinct()
        return Response(trips)
        

class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        home_country = request.data.get('home_country')
        if not username or not password or not home_country:
            return Response({'error': 'Username, password, and home_country are required'}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password, home_country=home_country)
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
        }, status=status.HTTP_201_CREATED)
    

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get('password')
        }

        if not User.objects.filter(username=credentials['username']).exists():
            raise serializers.ValidationError('No user with this username exists.')
        
        user = authenticate(username=credentials['username'], password=credentials['password'])

        if user is None:
            raise serializers.ValidationError('Invalid password.')
        
        data = super().validate(attrs)
        data['user_id'] = user.id
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_id'] = user.id
        return token
    

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer